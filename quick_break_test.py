#!/usr/bin/env python3
"""Quick Break Test - Fast validation of all 5 fixes"""
import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor

BASE = "http://localhost:8000"

print("\n" + "="*60)
print("MYTHARA QUICK BREAK TEST")
print("="*60 + "\n")

# Test 1: Rate Limiting
print("[1/5] Rate Limiting Test...")
try:
    blocked = 0
    for i in range(120):
        r = requests.get(f"{BASE}/health", timeout=1)
        if r.status_code == 429: blocked += 1
    print(f"   Result: {blocked}/120 blocked by rate limiter")
    print(f"   Status: {'PASS' if blocked > 0 else 'FAIL - no rate limiting!'}\n")
except Exception as e:
    print(f"   FAIL: {e}\n")

# Test 2: CORS Check
print("[2/5] CORS Configuration Test...")
try:
    has_db = os.getenv("DATABASE_URL", "").startswith(("postgres://", "postgresql://"))
    has_cors = bool(os.getenv("MYTHARA_ALLOWED_ORIGINS"))
    r = requests.get(f"{BASE}/health")
    cors_header = r.headers.get("Access-Control-Allow-Origin")
    print(f"   Production mode: {has_db}")
    print(f"   CORS configured: {has_cors}")
    print(f"   CORS header: {cors_header}")
    print(f"   Status: {'PASS' if cors_header else 'WARN'}\n")
except Exception as e:
    print(f"   FAIL: {e}\n")

# Test 3: Database Pool
print("[3/5] Database Pool Test (30 concurrent)...")
try:
    def req(n):
        try:
            return requests.get(f"{BASE}/health", timeout=5).status_code
        except: return 0
    
    with ThreadPoolExecutor(max_workers=30) as pool:
        results = list(pool.map(req, range(30)))
    
    success = sum(1 for r in results if r == 200)
    print(f"   Successful: {success}/30")
    print(f"   Status: {'PASS' if success >= 25 else 'FAIL'}\n")
except Exception as e:
    print(f"   FAIL: {e}\n")

# Test 4: Exception Handling
print("[4/5] Exception Handling Test...")
try:
    with open("core/source_proprietary/main.py", 'r') as f:
        bare = sum(1 for line in f if line.strip() == "except:")
    print(f"   Bare except clauses: {bare}")
    print(f"   Status: {'PASS' if bare == 0 else 'FAIL'}\n")
except Exception as e:
    print(f"   FAIL: {e}\n")

# Test 5: Load Test
print("[5/5] Load Test (200 requests)...")
try:
    start = time.time()
    success = 0
    for i in range(200):
        try:
            if requests.get(f"{BASE}/health", timeout=2).status_code == 200:
                success += 1
        except: pass
        if i % 50 == 0: print(f"   Progress: {i}/200...")
    
    elapsed = time.time() - start
    print(f"   Successful: {success}/200")
    print(f"   Time: {elapsed:.1f}s ({200/elapsed:.0f} req/s)")
    print(f"   Status: {'PASS' if success >= 150 else 'FAIL'}\n")
except Exception as e:
    print(f"   FAIL: {e}\n")

print("="*60)
print("TEST COMPLETE")
print("="*60)
