#!/usr/bin/env python3
"""
Mythara Engine - Performance Tests
Load testing and performance benchmarks for API endpoints.

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.
"""

import time
import statistics
from typing import List
import sys
from pathlib import Path

# Add source directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "core" / "source_proprietary"))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
VALID_API_KEY = "dev_test_key_001"


def measure_response_time(func, iterations: int = 100) -> dict:
    """
    Measure response time statistics for a function.
    
    Returns:
        {
            "min": float,
            "max": float,
            "mean": float,
            "median": float,
            "p95": float,
            "p99": float
        }
    """
    times = []
    
    for _ in range(iterations):
        start = time.time()
        func()
        end = time.time()
        times.append((end - start) * 1000)  # Convert to ms
    
    times.sort()
    
    return {
        "iterations": iterations,
        "min_ms": round(min(times), 2),
        "max_ms": round(max(times), 2),
        "mean_ms": round(statistics.mean(times), 2),
        "median_ms": round(statistics.median(times), 2),
        "p95_ms": round(times[int(len(times) * 0.95)], 2),
        "p99_ms": round(times[int(len(times) * 0.99)], 2),
    }


def test_health_check_performance():
    """Benchmark health check endpoint."""
    def health_check():
        response = client.get("/health")
        assert response.status_code == 200
    
    stats = measure_response_time(health_check, iterations=1000)
    
    print("\n" + "=" * 60)
    print("HEALTH CHECK PERFORMANCE")
    print("=" * 60)
    for key, value in stats.items():
        print(f"{key:15s}: {value}")
    
    # Performance assertions
    assert stats["mean_ms"] < 50, f"Health check too slow: {stats['mean_ms']}ms"
    assert stats["p95_ms"] < 100, f"P95 latency too high: {stats['p95_ms']}ms"
    
    return stats


def test_reservoir_status_performance():
    """Benchmark reservoir status endpoint."""
    def reservoir_status():
        response = client.get(
            "/v1/reservoir/status",
            headers={"Authorization": f"Bearer {VALID_API_KEY}"}
        )
        assert response.status_code == 200
    
    stats = measure_response_time(reservoir_status, iterations=500)
    
    print("\n" + "=" * 60)
    print("RESERVOIR STATUS PERFORMANCE")
    print("=" * 60)
    for key, value in stats.items():
        print(f"{key:15s}: {value}")
    
    # Performance assertions
    assert stats["mean_ms"] < 100, f"Reservoir status too slow: {stats['mean_ms']}ms"
    assert stats["p95_ms"] < 200, f"P95 latency too high: {stats['p95_ms']}ms"
    
    return stats


def test_clause_invocation_performance():
    """Benchmark clause invocation endpoint."""
    def invoke_clause():
        response = client.post(
            "/v1/clauses/invoke",
            headers={"Authorization": f"Bearer {VALID_API_KEY}"},
            json={
                "clause_id": "Legacy_Seed",
                "messenger": "M-001",
                "payload": {"emotion": "gratitude", "intensity": 0.8},
                "consent_token": "test"
            }
        )
        assert response.status_code == 200
    
    stats = measure_response_time(invoke_clause, iterations=100)
    
    print("\n" + "=" * 60)
    print("CLAUSE INVOCATION PERFORMANCE")
    print("=" * 60)
    for key, value in stats.items():
        print(f"{key:15s}: {value}")
    
    # Performance assertions
    assert stats["mean_ms"] < 150, f"Clause invocation too slow: {stats['mean_ms']}ms"
    assert stats["p95_ms"] < 300, f"P95 latency too high: {stats['p95_ms']}ms"
    
    return stats


def test_manifest_performance():
    """Benchmark manifest endpoint."""
    def get_manifest():
        response = client.get(
            "/v1/manifest/clauses",
            headers={"Authorization": f"Bearer {VALID_API_KEY}"}
        )
        assert response.status_code == 200
    
    stats = measure_response_time(get_manifest, iterations=500)
    
    print("\n" + "=" * 60)
    print("MANIFEST RETRIEVAL PERFORMANCE")
    print("=" * 60)
    for key, value in stats.items():
        print(f"{key:15s}: {value}")
    
    # Performance assertions
    assert stats["mean_ms"] < 100, f"Manifest retrieval too slow: {stats['mean_ms']}ms"
    assert stats["p95_ms"] < 200, f"P95 latency too high: {stats['p95_ms']}ms"
    
    return stats


def test_concurrent_requests():
    """Test concurrent request handling."""
    import concurrent.futures
    
    def make_request():
        response = client.get(
            "/v1/reservoir/status",
            headers={"Authorization": f"Bearer {VALID_API_KEY}"}
        )
        return response.status_code
    
    print("\n" + "=" * 60)
    print("CONCURRENT REQUEST TEST")
    print("=" * 60)
    
    start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(100)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    end = time.time()
    
    total_time = (end - start) * 1000
    requests_per_second = 100 / (total_time / 1000)
    
    print(f"Total time:     {total_time:.2f}ms")
    print(f"Requests/sec:   {requests_per_second:.2f}")
    print(f"Success rate:   {sum(1 for r in results if r == 200)}/100")
    
    assert sum(1 for r in results if r == 200) >= 95, "Too many failed requests"
    
    return {
        "total_time_ms": round(total_time, 2),
        "requests_per_second": round(requests_per_second, 2),
        "success_count": sum(1 for r in results if r == 200)
    }


def run_all_performance_tests():
    """Run all performance tests and generate summary."""
    print("\n" + "=" * 60)
    print("MYTHARA ENGINE - PERFORMANCE TEST SUITE")
    print("=" * 60)
    
    results = {}
    
    try:
        results["health_check"] = test_health_check_performance()
    except AssertionError as e:
        print(f"\n❌ Health check failed: {e}")
    
    try:
        results["reservoir_status"] = test_reservoir_status_performance()
    except AssertionError as e:
        print(f"\n❌ Reservoir status failed: {e}")
    
    try:
        results["clause_invocation"] = test_clause_invocation_performance()
    except AssertionError as e:
        print(f"\n❌ Clause invocation failed: {e}")
    
    try:
        results["manifest"] = test_manifest_performance()
    except AssertionError as e:
        print(f"\n❌ Manifest failed: {e}")
    
    try:
        results["concurrent"] = test_concurrent_requests()
    except AssertionError as e:
        print(f"\n❌ Concurrent test failed: {e}")
    
    print("\n" + "=" * 60)
    print("PERFORMANCE TEST SUMMARY")
    print("=" * 60)
    print(f"Tests completed: {len(results)}/5")
    print("\nTarget SLAs:")
    print("  - Health check P95: < 100ms")
    print("  - Reservoir status P95: < 200ms")
    print("  - Clause invocation P95: < 300ms")
    print("  - Manifest retrieval P95: < 200ms")
    print("  - Concurrent success rate: > 95%")
    print("\n✅ Performance tests complete")


if __name__ == "__main__":
    run_all_performance_tests()
