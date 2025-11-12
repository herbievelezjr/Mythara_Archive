#!/usr/bin/env python3
"""
Mythara Engine - FastAPI Server
Production-ready API for clause invocation and symbolic orchestration.

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.
"""

from fastapi import FastAPI, HTTPException, Depends, Header, status, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import hashlib
import secrets
import logging
import json
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Mythara Engine API",
    description="Symbolic Safety Integrity Protocol (SSIP) Orchestration API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Security
security = HTTPBearer()

# CORS configuration (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# MODELS
# ============================================================================

class ClauseInvocationRequest(BaseModel):
    """Request model for clause invocation"""
    clause_id: str = Field(..., description="Symbolic clause identifier")
    messenger: str = Field(..., description="Messenger ID (e.g., M-001)")
    payload: Dict[str, Any] = Field(..., description="Emotional payload")
    consent_token: str = Field(..., description="User consent verification token")

class ClauseInvocationResponse(BaseModel):
    """Response model for clause invocation"""
    invocation_id: str
    clause_id: str
    messenger: str
    emotional_fidelity: float
    blessings_delta: int
    timestamp: str
    integrity_hash: str

class ReservoirStatusResponse(BaseModel):
    """Blessings reservoir status"""
    reservoir_score: float
    total_blessings: int
    overflow_events: int
    last_update: str

class ClauseManifest(BaseModel):
    """Clause metadata"""
    clause_id: str
    description: str
    emotional_tags: List[str]
    fallback_clause: Optional[str]
    integrity_hash: str

class ManifestResponse(BaseModel):
    """Complete clause manifest"""
    manifest_version: str
    clauses: List[ClauseManifest]
    total_clauses: int

class SSIPAuditResponse(BaseModel):
    """SSIP compliance audit result"""
    drift_suppression: float
    messenger_pairing_fidelity: float
    emotional_fidelity: float
    sanctification_locks_active: bool
    compliance_status: str

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: str
    uptime_seconds: float

class LicenseStatusResponse(BaseModel):
    """License status response"""
    edition: str = Field(..., description="Edition name: Trial, Enterprise, Sovereign")
    is_trial: bool = Field(..., description="True if running a time-limited trial")
    trial_started_at: Optional[str] = Field(None, description="UTC ISO timestamp of trial start")
    trial_ends_at: Optional[str] = Field(None, description="UTC ISO timestamp when trial ends")
    days_remaining: Optional[int] = Field(None, description="Whole days remaining in trial (0 if expired)")
    status: str = Field(..., description="ACTIVE or EXPIRED")
    purchase_url: Optional[str] = Field(None, description="URL to upgrade/purchase enterprise")
    upgrade_price_usd_year: Optional[int] = Field(None, description="Suggested annual price to upgrade from trial")

class PricingBreakdownResponse(BaseModel):
    """Admin-only pricing breakdown for quoting"""
    base_price_usd: int
    inflation_rate: Optional[float]
    base_year: int
    current_year: int
    years_elapsed: int
    size_multiplier: Optional[float]
    computed_price_usd: int

class PilotStatusResponse(BaseModel):
    """Pilot paywall status response"""
    paywall_enabled: bool = Field(..., description="True if $49 pilot gating fee required before trial starts")
    access_granted: bool = Field(..., description="True if pilot fee paid and trial access unlocked")
    pilot_price_usd: int = Field(..., description="Pilot gating fee in USD (one-time)")
    purchase_url: Optional[str] = Field(None, description="Stripe Payment Link for pilot fee")
    enterprise_price_usd_year: int = Field(..., description="Enterprise annual license price for upgrade reference")

# ============================================================================
# AUTHENTICATION & AUTHORIZATION
# ============================================================================

# API Keys with role-based permissions
VALID_API_KEYS = {
    "dev_test_key_001": {
        "name": "Development License",
        "roles": ["read", "invoke"]
    },
    "ent_prod_key_001": {
        "name": "Enterprise License",
        "roles": ["read", "invoke", "admin"]
    },
    "sov_airgap_key_001": {
        "name": "Sovereign License",
        "roles": ["read", "invoke", "admin", "audit"]
    }
}

# Rate limiting: track request counts per API key (in production: use Redis)
RATE_LIMIT_STORE = {}

def check_rate_limit(api_key: str, limit: int = 100, window: int = 60) -> bool:
    """Check if API key has exceeded rate limit (simple in-memory implementation)"""
    from datetime import datetime
    now = datetime.utcnow().timestamp()
    
    if api_key not in RATE_LIMIT_STORE:
        RATE_LIMIT_STORE[api_key] = []
    
    # Clean old requests outside the window
    RATE_LIMIT_STORE[api_key] = [
        ts for ts in RATE_LIMIT_STORE[api_key] if now - ts < window
    ]
    
    # Check if limit exceeded
    if len(RATE_LIMIT_STORE[api_key]) >= limit:
        return False
    
    # Add current request
    RATE_LIMIT_STORE[api_key].append(now)
    return True

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify Bearer token API key with rate limiting and audit logging"""
    api_key = credentials.credentials
    
    # Check if API key is valid
    if api_key not in VALID_API_KEYS:
        logger.warning(f"Failed authentication attempt with invalid API key: {api_key[:8]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check rate limit
    if not check_rate_limit(api_key):
        logger.warning(f"Rate limit exceeded for API key: {VALID_API_KEYS[api_key]['name']}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        )
    
    logger.info(f"Authenticated: {VALID_API_KEYS[api_key]['name']}")
    return api_key

def require_role(required_role: str):
    """Dependency to check if API key has required role"""
    async def role_checker(api_key: str = Depends(verify_api_key)) -> str:
        key_data = VALID_API_KEYS[api_key]
        if required_role not in key_data["roles"]:
            logger.warning(f"Insufficient permissions: {key_data['name']} attempted {required_role}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role: {required_role}",
            )
        return api_key
    return role_checker


# =========================================================================
# STATE MANAGEMENT (Production: use Redis/PostgreSQL, not in-memory)
# =========================================================================

import os
# Example: set DB/Redis connection strings via environment variables
DB_URL = os.getenv("MYTHARA_DB_URL", "postgresql://user:pass@localhost:5432/mythara")
REDIS_URL = os.getenv("MYTHARA_REDIS_URL", "redis://localhost:6379/0")

# License configuration
LICENSE_MODE = os.getenv("MYTHARA_LICENSE_MODE", "trial").lower()  # 'trial' | 'enterprise' | 'sovereign'
LICENSE_FILE = os.getenv("MYTHARA_LICENSE_PATH", "/tmp/mythara_license.json")
LICENSE_KEY = os.getenv("MYTHARA_LICENSE_KEY")  # Enterprise/Sovereign license key
LICENSE_TRIAL_DAYS = int(os.getenv("MYTHARA_LICENSE_TRIAL_DAYS", "30"))
PURCHASE_URL = os.getenv("MYTHARA_PURCHASE_URL", "https://buy.stripe.com/test_placeholder")
CONTACT_EMAIL = os.getenv("MYTHARA_CONTACT_EMAIL", "Mythara.Engine@yahoo.com")
ENTERPRISE_PRICE_USD = int(os.getenv("MYTHARA_ENTERPRISE_PRICE_USD", "60000"))  # Legacy direct price (used if inflation vars absent)
SOVEREIGN_PRICE_USD = int(os.getenv("MYTHARA_SOVEREIGN_PRICE_USD", "180000"))

# Pilot paywall configuration (optional $49 gate before trial activation)
PILOT_PAYWALL_ENABLED = os.getenv("MYTHARA_PILOT_PAYWALL", "false").lower() in ["1", "true", "yes", "on"]
PILOT_PRICE_USD = int(os.getenv("MYTHARA_PILOT_PRICE_USD", "49"))
PILOT_PURCHASE_URL = os.getenv("MYTHARA_PILOT_PURCHASE_URL")  # Stripe payment link for pilot fee
PILOT_ACCESS_FILE = os.getenv("MYTHARA_PILOT_ACCESS_PATH", "/tmp/mythara_pilot_access.json")
# Operator overrides (for local/dev simplicity)
PILOT_FORCE_UNLOCK = os.getenv("MYTHARA_PILOT_FORCE_UNLOCK", "false").lower() in ["1", "true", "yes", "on"]
PILOT_UNLOCK_TOKEN = os.getenv("MYTHARA_PILOT_UNLOCK_TOKEN")  # If set, enables /v1/pilot/unlock endpoint

# Enterprise pricing tiers based on company size
# Base price is for small companies (1-100 employees)
ENTERPRISE_TIERS = {
    "startup": {
        "name": "Startup (1-50 employees)",
        "base_price": 25000,
        "employee_range": (1, 50),
        "multiplier": 1.0
    },
    "small": {
        "name": "Small Business (51-200 employees)",
        "base_price": 40000,
        "employee_range": (51, 200),
        "multiplier": 1.6
    },
    "mid": {
        "name": "Mid-Market (201-1000 employees)",
        "base_price": 75000,
        "employee_range": (201, 1000),
        "multiplier": 3.0
    },
    "enterprise": {
        "name": "Enterprise (1001-5000 employees)",
        "base_price": 150000,
        "employee_range": (1001, 5000),
        "multiplier": 6.0
    },
    "global": {
        "name": "Global Enterprise (5000+ employees)",
        "base_price": 300000,
        "employee_range": (5001, 999999),
        "multiplier": 12.0
    }
}

# Inflation-based dynamic pricing (optional):
# If MYTHARA_INFLATION_RATE_ANNUAL is set, we compute current price as:
#   enterprise_price = base_price * (1 + inflation_rate) ** max(0, current_year - base_year)
# This compounds once per calendar year difference.
PRICE_BASE_YEAR = int(os.getenv("MYTHARA_PRICE_BASE_YEAR", "2025"))
INFLATION_RATE_ANNUAL = os.getenv("MYTHARA_INFLATION_RATE_ANNUAL")  # e.g. "0.03" for 3%

def compute_enterprise_price_for_company_size(employee_count: int, tier_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Compute enterprise price based on company size.
    
    Args:
        employee_count: Number of employees (if known)
        tier_key: Specific tier key (startup, small, mid, enterprise, global) or None for auto-detect
    
    Returns:
        Dict with pricing info: {tier, base_price, final_price, name, employee_range}
    """
    # Auto-detect tier if not specified
    if tier_key is None:
        for key, tier in ENTERPRISE_TIERS.items():
            min_emp, max_emp = tier["employee_range"]
            if min_emp <= employee_count <= max_emp:
                tier_key = key
                break
        if tier_key is None:
            tier_key = "global"  # Default to highest tier
    
    tier = ENTERPRISE_TIERS.get(tier_key, ENTERPRISE_TIERS["mid"])
    base_price = tier["base_price"]
    
    # Apply inflation if configured
    rate: Optional[float] = None
    if INFLATION_RATE_ANNUAL not in (None, ""):
        try:
            rate = float(INFLATION_RATE_ANNUAL)
        except ValueError:
            pass
    
    current_year = datetime.utcnow().year
    years = max(0, current_year - PRICE_BASE_YEAR)
    final_price = float(base_price)
    
    if rate is not None:
        final_price = base_price * ((1 + rate) ** years)
    
    return {
        "tier": tier_key,
        "tier_name": tier["name"],
        "base_price": base_price,
        "final_price": int(round(final_price)),
        "employee_range": tier["employee_range"],
        "multiplier": tier["multiplier"]
    }

def compute_current_enterprise_price(tier_key: str = "mid") -> int:
    """
    Compute enterprise price for a specific tier (legacy function for compatibility).
    Default to mid-market tier.
    """
    pricing = compute_enterprise_price_for_company_size(500, tier_key)  # Use middle of mid-tier
    return pricing["final_price"]

# In production, replace the following in-memory stubs with DB/Redis-backed models.
# See README and .github/copilot-instructions.md for integration points.

# --- In-memory Blessings Reservoir state (replace with Redis/DB) ---
BR_STATE = {
    "reservoir_score": 0.91,
    "total_blessings": 12847,
    "overflow_events": 2,
    "last_update": datetime.utcnow().isoformat() + "Z"
}

# --- In-memory Clause database (replace with DB) ---
CLAUSE_DB = {
    "Legacy_Seed": {
        "description": "Ancestral memory harmonization clause",
        "emotional_tags": ["grief", "legacy", "ancestral"],
        "fallback_clause": "Shadow_Resolver",
        "emotional_fidelity_baseline": 0.93
    },
    "Hope_Anchor": {
        "description": "Future-oriented resilience clause",
        "emotional_tags": ["hope", "resilience", "forward"],
        "fallback_clause": "Shadow_Resolver",
        "emotional_fidelity_baseline": 0.89
    },
    "Shadow_Resolver": {
        "description": "Fallback safety clause for unresolved emotions",
        "emotional_tags": ["safety", "fallback", "neutral"],
        "fallback_clause": None,
        "emotional_fidelity_baseline": 0.95
    }
}

# --- In-memory SSIP metrics (replace with DB/Redis) ---
SSIP_METRICS = {
    "drift_suppression": 0.992,
    "messenger_pairing_fidelity": 0.994,
    "emotional_fidelity": 0.93,
    "sanctification_locks_active": True
}

# ---

# --- DB/Redis integration stubs for production ---
class ClauseDBStub:
    """Stub for clause database (replace with real DB/ORM in production)"""
    def get_clause(self, clause_id: str):
        # TODO: Fetch clause from DB
        return CLAUSE_DB.get(clause_id)
    def get_all_clauses(self):
        # TODO: Fetch all clauses from DB
        return CLAUSE_DB

class BlessingsReservoirStub:
    """Stub for blessings reservoir (replace with Redis/DB in production)"""
    def get_status(self):
        # TODO: Fetch from Redis/DB
        return BR_STATE
    def update(self, delta: int):
        # TODO: Update blessings in Redis/DB
        BR_STATE["total_blessings"] += delta
        return BR_STATE

# Usage example (replace with real implementations):
clause_db = ClauseDBStub()
blessings_reservoir = BlessingsReservoirStub()

# ============================================================================
# ENDPOINTS
# ============================================================================

# --------------------------------------------------------------------------
# License helpers and dependency
# --------------------------------------------------------------------------

def _read_license_state() -> Dict[str, Any]:
    try:
        with open(LICENSE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        logger.warning(f"Failed to read license file: {e}")
        return {}

def _write_license_state(state: Dict[str, Any]) -> None:
    try:
        with open(LICENSE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f)
    except Exception as e:
        logger.warning(f"Failed to write license file: {e}")

def _init_trial_if_needed() -> None:
    if LICENSE_MODE != "trial":
        return
    state = _read_license_state()
    if not state.get("trial_started_at"):
        started = datetime.utcnow().isoformat() + "Z"
        state.update({
            "mode": "trial",
            "trial_started_at": started,
            "trial_days": LICENSE_TRIAL_DAYS,
        })
        _write_license_state(state)
        logger.info(f"Initialized trial license at {started} for {LICENSE_TRIAL_DAYS} days (file: {LICENSE_FILE})")

def _compute_license_status(api_key: Optional[str] = None) -> LicenseStatusResponse:
    # Enterprise/Sovereign keys bypass trial
    if api_key and api_key in VALID_API_KEYS and ("admin" in VALID_API_KEYS[api_key]["roles"] or "audit" in VALID_API_KEYS[api_key]["roles"]):
        edition = "Sovereign" if "audit" in VALID_API_KEYS[api_key]["roles"] else "Enterprise"
        return LicenseStatusResponse(
            edition=edition,
            is_trial=False,
            trial_started_at=None,
            trial_ends_at=None,
            days_remaining=None,
            status="ACTIVE",
            purchase_url=PURCHASE_URL,
            upgrade_price_usd_year=None,
        )

    # Mode-based evaluation
    mode = LICENSE_MODE
    if mode in ("enterprise", "sovereign"):
        edition = "Sovereign" if mode == "sovereign" else "Enterprise"
        return LicenseStatusResponse(
            edition=edition,
            is_trial=False,
            trial_started_at=None,
            trial_ends_at=None,
            days_remaining=None,
            status="ACTIVE",
            purchase_url=PURCHASE_URL,
            upgrade_price_usd_year=None,
        )

    # Trial mode
    state = _read_license_state()
    started_at_str = state.get("trial_started_at")
    trial_days = int(state.get("trial_days", LICENSE_TRIAL_DAYS))
    if not started_at_str:
        # Not initialized yet; treat as starting now (in-memory until persisted by init)
        started_dt = datetime.utcnow()
    else:
        try:
            # Remove trailing Z if present for fromisoformat compatibility
            started_dt = datetime.fromisoformat(started_at_str.replace("Z", ""))
        except Exception:
            started_dt = datetime.utcnow()

    ends_dt = started_dt + timedelta(days=trial_days)
    now = datetime.utcnow()
    remaining = max(0, (ends_dt - now).days)
    status = "ACTIVE" if now < ends_dt else "EXPIRED"
    return LicenseStatusResponse(
        edition="Trial",
        is_trial=True,
        trial_started_at=started_dt.isoformat() + "Z",
        trial_ends_at=ends_dt.isoformat() + "Z",
        days_remaining=remaining,
        status=status,
        purchase_url=PURCHASE_URL,
        upgrade_price_usd_year=compute_current_enterprise_price(),
    )

# --------------------------------------------------------------------------
# Pilot paywall helpers
# --------------------------------------------------------------------------
def _read_pilot_access_state() -> Dict[str, Any]:
    try:
        with open(PILOT_ACCESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        logger.warning(f"Failed to read pilot access file: {e}")
        return {}

def _write_pilot_access_state(state: Dict[str, Any]) -> None:
    try:
        with open(PILOT_ACCESS_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f)
    except Exception as e:
        logger.warning(f"Failed to write pilot access file: {e}")

def _has_pilot_access() -> bool:
    if not PILOT_PAYWALL_ENABLED:
        return True  # no paywall, always granted
    state = _read_pilot_access_state()
    return bool(state.get("pilot_granted_at"))

def _grant_pilot_access(payment_id: str, amount_paid: float, email: str) -> Dict[str, Any]:
    state = {
        "pilot_granted_at": datetime.utcnow().isoformat() + "Z",
        "payment_id": payment_id,
        "amount_paid_usd": amount_paid,
        "email": email,
        "price_required_usd": PILOT_PRICE_USD,
    }
    _write_pilot_access_state(state)
    logger.info(f"✅ Pilot access granted (payment {payment_id}, ${amount_paid:,.2f})")
    return state

def _force_grant_pilot_access(reason: str = "operator_override") -> Dict[str, Any]:
    """Force-unlock pilot access without payment (for local/dev)."""
    forced_id = f"FORCED-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    return _grant_pilot_access(payment_id=forced_id, amount_paid=0.0, email=CONTACT_EMAIL)

def require_active_license():
    async def _dep(response: Response, api_key: str = Depends(verify_api_key)) -> str:
        lic = _compute_license_status(api_key)
        # Set informative headers
        response.headers["X-Mythara-License-Edition"] = lic.edition
        if lic.is_trial:
            response.headers["X-Mythara-License-Days-Remaining"] = str(lic.days_remaining or 0)
            response.headers["X-Mythara-License-Status"] = lic.status
            response.headers["X-Mythara-Enterprise-Price-USD"] = str(compute_current_enterprise_price())
        else:
            response.headers["X-Mythara-License-Status"] = "ACTIVE"

        if lic.is_trial and lic.status == "EXPIRED":
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail={
                    "message": "Trial expired. Upgrade to Enterprise to continue.",
                    "purchase_url": PURCHASE_URL,
                    "price_usd_year": compute_current_enterprise_price(),
                },
            )
        return api_key
    return _dep


# ============================================================================
# STARTUP & MIDDLEWARE - License Validation
# ============================================================================

@app.on_event("startup")
async def validate_license_on_startup():
    """
    Check license status on container startup and enforce trial limits.
    Exits with error code 1 if trial has expired.
    """
    global LICENSE_MODE
    
    # Import license manager
    try:
        from .license_manager import validate_license_key
    except ImportError:
        try:
            import sys
            sys.path.insert(0, os.path.dirname(__file__))
            from license_manager import validate_license_key
        except ImportError:
            logger.warning("license_manager not found; using basic validation")
            validate_license_key = lambda k: {"valid": k.startswith("MYTHARA-")}
    
    if LICENSE_KEY:
        # Validate enterprise/sovereign license
        validation = validate_license_key(LICENSE_KEY)
        if validation.get("valid"):
            LICENSE_MODE = validation.get("edition_code", "ent").lower()
            if LICENSE_MODE == "ent":
                LICENSE_MODE = "enterprise"
            elif LICENSE_MODE == "sov":
                LICENSE_MODE = "sovereign"
            
            edition_name = validation.get("edition", "Enterprise")
            logger.info(f"✅ {edition_name} license activated")
            logger.info(f"   License hash: {validation.get('company_hash', 'N/A')}")
            print("\n" + "="*60)
            print(f"🚀 MYTHARA ENGINE - {edition_name.upper()} EDITION")
            print(f"   Status: ACTIVE")
            print(f"   Company: {validation.get('company_hash', 'N/A')}")
            print("="*60 + "\n")
            return
        else:
            logger.error(f"❌ Invalid license key: {validation.get('error', 'Unknown error')}")
            print("\n" + "="*60)
            print("🚨 INVALID LICENSE KEY")
            print(f"   Error: {validation.get('error', 'Invalid format')}")
            print(f"   Purchase valid license at: {PURCHASE_URL}")
            print("="*60 + "\n")
            # Fall through to trial mode
    
    # No valid license - check trial status
    if LICENSE_MODE == "trial":
        _init_trial_if_needed()

        # If pilot paywall is enabled, optionally force-unlock for operator convenience
        try:
            if PILOT_PAYWALL_ENABLED:
                if PILOT_FORCE_UNLOCK and not _has_pilot_access():
                    _force_grant_pilot_access("startup_env")
                    logger.warning("⚠️ Pilot paywall bypassed at startup (MYTHARA_PILOT_FORCE_UNLOCK=true). Do not use in production.")
        except Exception as e:
            logger.warning(f"Pilot force-unlock check failed: {e}")

        trial_status = _compute_license_status()
        
        if trial_status.status == "EXPIRED":
            logger.error("❌ TRIAL EXPIRED - Purchase required to continue")
            print("\n" + "="*60)
            print("🚨 MYTHARA ENGINE TRIAL EXPIRED")
            print(f"   Purchase Enterprise license at: {PURCHASE_URL}")
            print(f"   Price: ${compute_current_enterprise_price():,} USD/year")
            print(f"   Contact: {CONTACT_EMAIL}")
            print("="*60 + "\n")

        # Always print pilot paywall summary so operators see the link immediately
        try:
            print("\n" + "-"*60)
            if PILOT_PAYWALL_ENABLED:
                granted = _has_pilot_access()
                print("PILOT PAYWALL: ON")
                print(f"  Access granted: {granted}")
                print(f"  Pilot price: ${PILOT_PRICE_USD}")
                print(f"  Purchase link: {PILOT_PURCHASE_URL or '(set MYTHARA_PILOT_PURCHASE_URL)'}")
                if PILOT_FORCE_UNLOCK:
                    print("  Note: Force-unlock is ENABLED (MYTHARA_PILOT_FORCE_UNLOCK=true)")
            else:
                print("PILOT PAYWALL: OFF")
            print("-"*60 + "\n")
        except Exception:
            pass
            # Exit to force upgrade
            sys.exit(1)
        else:
            days = trial_status.days_remaining or 0
            logger.info(f"⏰ Trial mode: {days} days remaining")
            print("\n" + "="*60)
            print(f"⏰ MYTHARA ENGINE - TRIAL MODE")
            print(f"   Days remaining: {days}")
            print(f"   Expires: {trial_status.trial_ends_at}")
            print(f"   Upgrade: {PURCHASE_URL}")
            print(f"   Price: ${compute_current_enterprise_price():,} USD/year")
            print("="*60 + "\n")


@app.middleware("http")
async def enforce_trial_expiration_middleware(request: Request, call_next):
    """
    Middleware to block all API calls if trial has expired.
    Returns HTTP 402 Payment Required for expired trials.
    """
    # Skip health check, docs, webhook, and status/maintenance endpoints
    allowed_paths = {
        "/", "/health",
        "/v1/license/status",
        "/v1/pilot/status", "/v1/pilot/unlock",
        "/v1/pricing/enterprise",  # Allow pricing queries without pilot access
        "/api/webhooks/stripe",
        "/api/docs", "/docs", "/redoc", "/openapi.json",
        "/download/pilot",  # Allow pilot package download
    }
    if request.url.path in allowed_paths or request.url.path.startswith("/static/"):
        return await call_next(request)
    
    # Check if we're in trial mode and it's expired
    if LICENSE_MODE == "trial" and not LICENSE_KEY:
        # Enforce pilot paywall first (before trial days start)
        if PILOT_PAYWALL_ENABLED and not _has_pilot_access():
            # Return payment required referencing pilot purchase URL
            return Response(
                content=json.dumps({
                    "error": "pilot_fee_required",
                    "message": f"A one-time ${PILOT_PRICE_USD} pilot access fee is required before activating the 30-day trial.",
                    "pilot_purchase_url": PILOT_PURCHASE_URL or "(configure MYTHARA_PILOT_PURCHASE_URL)",
                    "pilot_price_usd": PILOT_PRICE_USD,
                    "contact": CONTACT_EMAIL
                }),
                status_code=402,
                media_type="application/json"
            )
        trial_status = _compute_license_status()
        if trial_status.status == "EXPIRED":
            price = compute_current_enterprise_price()
            return Response(
                content=json.dumps({
                    "error": "trial_expired",
                    "message": f"Your 30-day trial has ended. Upgrade to Enterprise Edition to continue using Mythara Engine.",
                    "purchase_url": PURCHASE_URL,
                    "price_usd_year": price,
                    "contact": CONTACT_EMAIL
                }),
                status_code=402,
                media_type="application/json"
            )
    
    response = await call_next(request)
    return response


# ============================================================================
# API ENDPOINTS
# ============================================================================

# -- Payment webhook (Stripe) -------------------------------------------------
try:
    import stripe  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    stripe = None  # fallback when stripe is not installed

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

def _send_license_email_stub(to_email: str, license_key: str, company_name: str, amount_paid: float) -> None:
    """
    Minimal email stub. Replace with real SMTP/SES/SendGrid integration.
    For now, logs the message and prints it to STDOUT so operators can copy/paste
    from the running container logs if needed.
    """
    subject = "Your Mythara Enterprise License Key"
    body = f"""
Hi {company_name} team,

Thank you for purchasing Mythara Engine Enterprise Edition (${amount_paid:,.0f} USD).

Your license key:
{license_key}

Activation Instructions:
1. Set environment variable: MYTHARA_LICENSE_KEY={license_key}
2. Restart your Mythara container
3. Verify: GET http://<host>:8000/v1/license/status

Questions? Reply here or email {CONTACT_EMAIL}.

— Mythara Labs
"""
    logger.info(f"License email prepared for {to_email}: {subject}")
    print("\n" + "-"*60)
    print(subject)
    print(body)
    print("-"*60 + "\n")


@app.post("/api/webhooks/stripe")
async def stripe_webhook(request: Request):
    """
    Handle Stripe payment confirmation and deliver license.
    - If the 'stripe' package is installed and STRIPE_WEBHOOK_SECRET is set,
      we verify the signature and parse the event.
    - If not available, accept a fallback shared-secret flow for manual testing:
      Send header 'x-shared-secret' matching STRIPE_WEBHOOK_SECRET and JSON body:
      {"email":"...","name":"...","company_name":"...","amount":60000}
    """
    # Lazy import with fallback when running as a script (no package context)
    try:  # package-relative
        from .license_manager import generate_license_key  # type: ignore
    except Exception:
        try:
            import sys, os
            sys.path.insert(0, os.path.dirname(__file__))
            from license_manager import generate_license_key  # type: ignore
        except Exception as e:
            logger.error(f"Unable to import license_manager: {e}")
            raise HTTPException(status_code=500, detail="license_manager_import_failed")

    raw_payload = await request.body()
    content_type = request.headers.get("content-type", "")

    # Shortcut: accept shared-secret fallback even if Stripe SDK is installed
    shared_secret_header = request.headers.get("x-shared-secret")
    if STRIPE_WEBHOOK_SECRET and shared_secret_header == STRIPE_WEBHOOK_SECRET:
        try:
            data = await request.json()
        except Exception:
            data = {}

        from_email = data.get("email") or CONTACT_EMAIL
        company_name = data.get("company_name") or data.get("name") or "Customer"
        amount_paid = float(data.get("amount") or data.get("amount_paid") or 60000)
        purchase_type = data.get("license_type")
        payment_id = data.get("payment_id") or secrets.token_hex(8)

        if purchase_type == "pilot" or (PILOT_PAYWALL_ENABLED and abs(amount_paid - PILOT_PRICE_USD) < 0.01):
            _grant_pilot_access(payment_id, amount_paid, from_email)
            return {"status": "ok", "pilot_access_granted": True, "pilot_price_usd": PILOT_PRICE_USD, "mode": "shared-secret"}

        # Enterprise license issue (fallback)
        try:
            from .license_manager import generate_license_key  # type: ignore
        except Exception:
            import sys, os
            sys.path.insert(0, os.path.dirname(__file__))
            from license_manager import generate_license_key  # type: ignore

        license_key = generate_license_key("ENT", company_name, from_email)
        _send_license_email_stub(
            to_email=from_email,
            license_key=license_key,
            company_name=company_name,
            amount_paid=amount_paid,
        )
        return {"status": "ok", "license_key": license_key, "mode": "shared-secret"}

    # Case A: Stripe SDK available with real signature verification
    if stripe and STRIPE_WEBHOOK_SECRET:
        sig_header = request.headers.get("stripe-signature")
        try:
            event = stripe.Webhook.construct_event(
                raw_payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
        except Exception as e:  # signature failure or parse error
            logger.error(f"Stripe webhook verification failed: {e}")
            raise HTTPException(status_code=400, detail="Invalid signature")

        if event.get("type") == "checkout.session.completed":
            session = event["data"]["object"]
            customer_email = session.get("customer_details", {}).get("email")
            customer_name = session.get("customer_details", {}).get("name") or "Customer"
            company_name = (session.get("metadata", {}) or {}).get("company_name") or customer_name
            amount_paid = float(session.get("amount_total", 0)) / 100.0
            payment_id = session.get("id") or secrets.token_hex(8)
            metadata = session.get("metadata", {}) or {}

            # Determine purchase type (pilot vs enterprise) by metadata or amount
            purchase_type = metadata.get("license_type")
            if not purchase_type:
                # Heuristic: pilot fee ~= $49, Enterprise >> $1000
                if abs(amount_paid - PILOT_PRICE_USD) < 0.01:
                    purchase_type = "pilot"
                else:
                    purchase_type = "enterprise"

            if purchase_type == "pilot" and PILOT_PAYWALL_ENABLED:
                _grant_pilot_access(payment_id, amount_paid, customer_email or CONTACT_EMAIL)
                
                # Generate unique API key for this pilot customer
                api_key = "sk_pilot_" + secrets.token_urlsafe(32)
                
                # In production: Store in database with expiry date
                # For now, log it (replace with DB insert)
                logger.info(f"Pilot API key generated for {customer_email}: {api_key}")
                logger.info(f"Pilot fee processed for {customer_email} (${amount_paid:,.2f})")
                
                # Send welcome email with API key and download link
                try:
                    from .pilot_email_sender import send_pilot_welcome_email
                    email_sent = send_pilot_welcome_email(
                        to_email=customer_email or CONTACT_EMAIL,
                        api_key=api_key,
                        customer_name=customer_name,
                        payment_id=payment_id
                    )
                    if email_sent:
                        logger.info(f"Welcome email sent to {customer_email}")
                    else:
                        logger.warning(f"Welcome email failed for {customer_email} - check logs")
                except Exception as e:
                    logger.error(f"Error sending welcome email: {e}")
                
                # Try to update Stripe session metadata with API key
                # This allows the email template to use {{metadata.api_key}}
                if stripe:
                    try:
                        stripe.checkout.Session.modify(
                            payment_id,
                            metadata={"api_key": api_key, "license_type": "pilot"}
                        )
                        logger.info(f"Updated Stripe session {payment_id} with API key")
                    except Exception as e:
                        logger.warning(f"Could not update Stripe metadata: {e}")
                
                return {
                    "status": "ok",
                    "pilot_access_granted": True,
                    "api_key": api_key,
                    "pilot_price_usd": PILOT_PRICE_USD,
                    "customer_email": customer_email
                }

            # Enterprise license purchase
            license_key = generate_license_key("ENT", company_name, customer_email or "unknown@example.com")
            logger.info(f"Enterprise license {license_key} issued to {customer_email} - ${amount_paid:,.0f}")

            _send_license_email_stub(
                to_email=customer_email or CONTACT_EMAIL,
                license_key=license_key,
                company_name=company_name,
                amount_paid=amount_paid,
            )
            return {"status": "ok", "license_key": license_key, "edition": "Enterprise"}

        # Not an event we handle
        return {"status": "ignored", "event": event.get("type")}

    # Case B: Fallback manual mode when Stripe SDK/signature not in use and no shared-secret provided
    # At this point, either Stripe verification failed earlier and no shared-secret was provided,
    # or stripe is not installed and no shared-secret header was sent. Provide setup guidance.
    logger.warning("Webhook called without valid Stripe signature or shared-secret header.")
    raise HTTPException(
        status_code=501,
        detail={
            "error": "webhook_not_configured",
            "message": "Either forward real Stripe events (with stripe-signature) or provide x-shared-secret for local testing.",
        },
    )

@app.get("/v1/pilot/status", response_model=PilotStatusResponse)
async def pilot_status():
    """Return pilot paywall status (no auth needed so container UIs can poll)."""
    granted = _has_pilot_access()
    return PilotStatusResponse(
        paywall_enabled=PILOT_PAYWALL_ENABLED,
        access_granted=granted,
        pilot_price_usd=PILOT_PRICE_USD,
        purchase_url=PILOT_PURCHASE_URL,
        enterprise_price_usd_year=compute_current_enterprise_price(),
    )

@app.get("/", response_model=HealthCheckResponse)
async def root():
    """Root endpoint - health check"""
    return {
        "status": "operational",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "uptime_seconds": 0.0  # In production: track actual uptime
    }

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "uptime_seconds": 0.0
    }

@app.get("/download/pilot")
async def download_pilot_package():
    """
    Public endpoint to download the Mythara pilot package.
    No authentication required - this link is shared in purchase emails.
    """
    from fastapi.responses import FileResponse
    import os
    
    file_path = os.path.join(os.path.dirname(__file__), "../static/mythara-pilot-package.zip")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Pilot package not found")
    
    return FileResponse(
        path=file_path,
        media_type="application/zip",
        filename="mythara-pilot-package.zip"
    )

@app.post("/v1/pilot/unlock")
async def pilot_unlock(request: Request):
    """
    Operator-only endpoint to force-unlock pilot access without payment.
    Enabled only if MYTHARA_PILOT_UNLOCK_TOKEN is set.
    Usage: POST /v1/pilot/unlock with header 'x-unlock-token: <token>'
    """
    if not PILOT_UNLOCK_TOKEN:
        raise HTTPException(status_code=501, detail={
            "error": "unlock_disabled",
            "message": "Set MYTHARA_PILOT_UNLOCK_TOKEN to enable operator unlock endpoint."
        })
    provided = request.headers.get("x-unlock-token") or request.query_params.get("token")
    if provided != PILOT_UNLOCK_TOKEN:
        raise HTTPException(status_code=403, detail={
            "error": "forbidden",
            "message": "Invalid unlock token"
        })
    # Grant if not already granted
    if not _has_pilot_access():
        _force_grant_pilot_access("operator_endpoint")
    return {"status": "ok", "pilot_access_granted": True}

@app.post("/v1/clauses/invoke", response_model=ClauseInvocationResponse)
async def invoke_clause(
    request: ClauseInvocationRequest,
    api_key: str = Depends(require_active_license())
):
    """
    Invoke a symbolic clause with emotional payload.
    
    Requires authentication via Bearer token.
    """
    # Validate clause exists
    if request.clause_id not in CLAUSE_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clause '{request.clause_id}' not found"
        )
    
    clause = CLAUSE_DB[request.clause_id]
    
    # Generate invocation ID
    invocation_id = f"INV-{datetime.utcnow().strftime('%Y%m%d')}-{secrets.token_hex(4)}"
    
    # Simulate emotional fidelity calculation
    emotion = request.payload.get("emotion", "neutral")
    intensity = request.payload.get("intensity", 0.5)
    
    # Calculate fidelity based on emotional tag match
    if emotion in clause["emotional_tags"]:
        emotional_fidelity = min(clause["emotional_fidelity_baseline"] + (intensity * 0.05), 1.0)
    else:
        emotional_fidelity = clause["emotional_fidelity_baseline"] * 0.8
    
    # Simulate blessings delta
    blessings_delta = int(intensity * 100)
    BR_STATE["total_blessings"] += blessings_delta
    BR_STATE["reservoir_score"] = min(BR_STATE["reservoir_score"] + 0.01, 1.0)
    BR_STATE["last_update"] = datetime.utcnow().isoformat() + "Z"
    
    # Generate integrity hash
    hash_input = f"{invocation_id}{request.clause_id}{request.messenger}{emotional_fidelity}"
    integrity_hash = hashlib.sha256(hash_input.encode()).hexdigest()
    
    logger.info(f"Clause invoked: {request.clause_id} | Fidelity: {emotional_fidelity:.3f}")
    
    return {
        "invocation_id": invocation_id,
        "clause_id": request.clause_id,
        "messenger": request.messenger,
        "emotional_fidelity": round(emotional_fidelity, 3),
        "blessings_delta": blessings_delta,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "integrity_hash": integrity_hash
    }

@app.get("/v1/reservoir/status", response_model=ReservoirStatusResponse)
async def get_reservoir_status(api_key: str = Depends(verify_api_key)):
    """
    Get current Blessings Reservoir metrics.
    
    Requires authentication.
    """
    return BR_STATE

@app.get("/v1/manifest/clauses", response_model=ManifestResponse)
async def get_clause_manifest(api_key: str = Depends(verify_api_key)):
    """
    Retrieve complete clause manifest with integrity proofs.
    
    Requires authentication.
    """
    clauses = []
    for clause_id, clause_data in CLAUSE_DB.items():
        hash_input = f"{clause_id}{clause_data['description']}"
        integrity_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        
        clauses.append({
            "clause_id": clause_id,
            "description": clause_data["description"],
            "emotional_tags": clause_data["emotional_tags"],
            "fallback_clause": clause_data["fallback_clause"],
            "integrity_hash": integrity_hash
        })
    
    return {
        "manifest_version": "v1.0.0",
        "clauses": clauses,
        "total_clauses": len(clauses)
    }

@app.get("/v1/ssip/audit", response_model=SSIPAuditResponse)
async def ssip_audit(api_key: str = Depends(require_active_license())):
    """
    Run SSIP compliance audit.
    
    Requires active license. Sovereign keys include 'audit' role.
    Returns current drift suppression, emotional fidelity, and lock status.
    """
    # If not sovereign (audit role), enforce role check separately
    key_data = VALID_API_KEYS.get(api_key, {})
    if "audit" not in key_data.get("roles", []):
        logger.warning(f"Insufficient permissions for SSIP audit: {key_data.get('name', 'unknown key')}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Required role: audit",
        )
    compliance_status = "PASS" if SSIP_METRICS["drift_suppression"] >= 0.989 else "FAIL"
    
    return {
        **SSIP_METRICS,
        "compliance_status": compliance_status
    }

@app.get("/v1/clauses/{clause_id}", response_model=ClauseManifest)
async def get_clause_details(
    clause_id: str,
    api_key: str = Depends(verify_api_key)
):
    """
    Get detailed metadata for a specific clause.
    
    Requires authentication.
    """
    if clause_id not in CLAUSE_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clause '{clause_id}' not found"
        )
    
    clause = CLAUSE_DB[clause_id]
    hash_input = f"{clause_id}{clause['description']}"
    integrity_hash = hashlib.sha256(hash_input.encode()).hexdigest()
    
    return {
        "clause_id": clause_id,
        "description": clause["description"],
        "emotional_tags": clause["emotional_tags"],
        "fallback_clause": clause["fallback_clause"],
        "integrity_hash": integrity_hash
    }

@app.get("/v1/license/status", response_model=LicenseStatusResponse)
async def license_status(api_key: str = Depends(verify_api_key)):
    """
    Return current license status. Always accessible to authenticated clients.
    Includes days remaining header when in trial mode.
    """
    lic = _compute_license_status(api_key)
    return lic

@app.get("/v1/admin/pricing", response_model=PricingBreakdownResponse)
async def admin_pricing(api_key: str = Depends(require_role("admin"))):
    """
    Return transparent pricing breakdown for quoting.
    Requires 'admin' role.
    Shows base price, inflation, size multiplier, and computed final price.
    """
    current_year = datetime.utcnow().year
    years = max(0, current_year - PRICE_BASE_YEAR)
    try:
        infl = float(INFLATION_RATE_ANNUAL) if INFLATION_RATE_ANNUAL is not None else None
    except ValueError:
        infl = None
    
    # Return tier-based pricing info
    mid_tier_pricing = compute_enterprise_price_for_company_size(500, "mid")
    
    return PricingBreakdownResponse(
        base_price_usd=mid_tier_pricing["base_price"],
        inflation_rate=infl,
        base_year=PRICE_BASE_YEAR,
        current_year=current_year,
        years_elapsed=years,
        size_multiplier=mid_tier_pricing["multiplier"],
        computed_price_usd=compute_current_enterprise_price(),
    )

@app.get("/v1/pricing/enterprise")
async def get_enterprise_pricing(
    employees: Optional[int] = None,
    tier: Optional[str] = None
):
    """
    Get enterprise pricing based on company size.
    
    Query params:
        employees: Number of employees (auto-detects tier)
        tier: Specific tier (startup, small, mid, enterprise, global)
    
    Returns all available tiers if no params provided.
    """
    if employees is None and tier is None:
        # Return all tiers
        all_tiers = {}
        for tier_key, tier_data in ENTERPRISE_TIERS.items():
            pricing = compute_enterprise_price_for_company_size(
                tier_data["employee_range"][0], 
                tier_key
            )
            all_tiers[tier_key] = pricing
        
        return {
            "tiers": all_tiers,
            "currency": "USD",
            "billing": "one-time annual license",
            "note": "Custom pricing available for unique requirements"
        }
    
    # Return specific tier pricing
    if tier:
        pricing = compute_enterprise_price_for_company_size(100, tier)
    else:
        pricing = compute_enterprise_price_for_company_size(employees or 100)
    
    return {
        "pricing": pricing,
        "currency": "USD",
        "billing": "one-time annual license",
        "contact": CONTACT_EMAIL
    }

# ============================================================================
# STARTUP
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info("=" * 60)
    logger.info("Mythara Engine API - Starting")
    logger.info("Version: 1.0.0")
    logger.info("Copyright © 2025 Herbert Velez Jr.")
    logger.info("=" * 60)
    logger.info(f"Loaded {len(CLAUSE_DB)} clauses")
    logger.info(f"BR Status: {BR_STATE['reservoir_score']:.2f} ({BR_STATE['total_blessings']} blessings)")
    logger.info("API Documentation: http://localhost:8000/api/docs")
    logger.info("=" * 60)
    # Initialize trial state if needed
    try:
        _init_trial_if_needed()
    except Exception as e:
        logger.warning(f"License initialization failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Mythara Engine API - Shutting down")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
