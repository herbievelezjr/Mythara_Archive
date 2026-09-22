#!/usr/bin/env python3
"""
Mythara Engine - Redis-backed Rate Limiter
Distributed rate limiting with tiered quotas and graceful degradation.

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.
"""

import time
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

# Try to import Redis, fall back to in-memory if not available
try:
    import redis
    from redis.exceptions import RedisError

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available, using in-memory rate limiting")


class RateLimiter:
    """
    Rate limiter with Redis backend and in-memory fallback.
    Implements sliding window algorithm for accurate rate limiting.
    """

    def __init__(self, redis_url: Optional[str] = None):
        """
        Initialize rate limiter.

        Args:
            redis_url: Redis connection URL (e.g., redis://localhost:6379)
                      If None, uses in-memory fallback
        """
        self.redis_client = None
        self.memory_store: Dict[str, list] = {}

        if REDIS_AVAILABLE and redis_url:
            try:
                self.redis_client = redis.from_url(
                    redis_url,
                    decode_responses=True,
                    socket_connect_timeout=2,
                    socket_timeout=2,
                )
                # Test connection
                self.redis_client.ping()
                logger.info("✅ Redis rate limiter initialized")
            except (RedisError, Exception) as e:
                logger.warning(
                    f"Redis connection failed, using in-memory fallback: {e}"
                )
                self.redis_client = None

    def check_rate_limit(self, key: str, limit: int, window: int) -> bool:
        """
        Check if request is within rate limit.

        Args:
            key: Unique identifier (e.g., API key, IP address)
            limit: Maximum requests allowed
            window: Time window in seconds

        Returns:
            True if request is allowed, False if rate limit exceeded
        """
        if self.redis_client:
            return self._redis_check(key, limit, window)
        else:
            return self._memory_check(key, limit, window)

    def _redis_check(self, key: str, limit: int, window: int) -> bool:
        """Redis-backed sliding window rate limiting."""
        try:
            now = time.time()
            redis_key = f"rate_limit:{key}"

            # Use Redis sorted set for sliding window
            pipe = self.redis_client.pipeline()

            # Remove old entries
            pipe.zremrangebyscore(redis_key, 0, now - window)

            # Count current entries
            pipe.zcard(redis_key)

            # Add current request
            pipe.zadd(redis_key, {str(now): now})

            # Set expiry
            pipe.expire(redis_key, window)

            results = pipe.execute()
            current_count = results[1]

            return current_count < limit

        except RedisError as e:
            logger.error(f"Redis error in rate limiting: {e}")
            # Graceful degradation: allow request on Redis failure
            return True

    def _memory_check(self, key: str, limit: int, window: int) -> bool:
        """In-memory sliding window rate limiting (fallback)."""
        now = time.time()

        # Get or create request history
        events = self.memory_store.setdefault(key, [])

        # Remove old events
        self.memory_store[key] = [ts for ts in events if now - ts < window]

        # Check limit
        if len(self.memory_store[key]) >= limit:
            return False

        # Add current request
        self.memory_store[key].append(now)
        return True

    def get_remaining(self, key: str, limit: int, window: int) -> int:
        """
        Get remaining requests in current window.

        Returns:
            Number of requests remaining before rate limit
        """
        if self.redis_client:
            try:
                now = time.time()
                redis_key = f"rate_limit:{key}"

                # Clean old entries and count
                pipe = self.redis_client.pipeline()
                pipe.zremrangebyscore(redis_key, 0, now - window)
                pipe.zcard(redis_key)
                results = pipe.execute()

                current_count = results[1]
                return max(0, limit - current_count)
            except RedisError:
                return limit  # Assume full quota on error
        else:
            now = time.time()
            events = self.memory_store.get(key, [])
            valid_events = [ts for ts in events if now - ts < window]
            return max(0, limit - len(valid_events))

    def reset(self, key: str):
        """Reset rate limit for a key (admin function)."""
        if self.redis_client:
            try:
                redis_key = f"rate_limit:{key}"
                self.redis_client.delete(redis_key)
            except RedisError as e:
                logger.error(f"Failed to reset rate limit: {e}")
        else:
            self.memory_store.pop(key, None)


class TieredRateLimiter(RateLimiter):
    """
    Rate limiter with tiered quotas based on license type.
    """

    # Default tier configurations
    TIER_LIMITS = {
        "trial": {"requests_per_minute": 10, "requests_per_hour": 100},
        "pilot": {"requests_per_minute": 100, "requests_per_hour": 5000},
        "enterprise": {"requests_per_minute": 1000, "requests_per_hour": 50000},
        "sovereign": {"requests_per_minute": 10000, "requests_per_hour": 500000},
    }

    def check_tiered_limit(self, key: str, tier: str) -> Dict[str, any]:
        """
        Check rate limit with tier-specific quotas.

        Returns:
            {
                "allowed": bool,
                "limit_type": str,  # "minute" or "hour"
                "remaining_minute": int,
                "remaining_hour": int
            }
        """
        limits = self.TIER_LIMITS.get(tier, self.TIER_LIMITS["trial"])

        # Check minute limit
        minute_ok = self.check_rate_limit(
            f"{key}:minute", limits["requests_per_minute"], 60
        )

        # Check hour limit
        hour_ok = self.check_rate_limit(
            f"{key}:hour", limits["requests_per_hour"], 3600
        )

        allowed = minute_ok and hour_ok
        limit_type = "minute" if not minute_ok else "hour" if not hour_ok else None

        return {
            "allowed": allowed,
            "limit_type": limit_type,
            "remaining_minute": self.get_remaining(
                f"{key}:minute", limits["requests_per_minute"], 60
            ),
            "remaining_hour": self.get_remaining(
                f"{key}:hour", limits["requests_per_hour"], 3600
            ),
        }
