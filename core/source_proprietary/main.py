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
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import hashlib
import secrets
import logging
import json
import sys
from pathlib import Path
import os

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

security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).parent.parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    logger.info(f"✅ Static files mounted from: {STATIC_DIR}")
else:
    logger.warning(f"⚠️ Static directory not found: {STATIC_DIR}")

# ===================== MODELS =====================
class ClauseInvocationRequest(BaseModel):
    clause_id: str = Field(...)
    messenger: str = Field(...)
    payload: Dict[str, Any] = Field(...)
    consent_token: str = Field(...)

class ClauseInvocationResponse(BaseModel):
    invocation_id: str
    clause_id: str
    messenger: str
    emotional_fidelity: float
    blessings_delta: int
    timestamp: str
    integrity_hash: str

class ReservoirStatusResponse(BaseModel):
    reservoir_score: float
    total_blessings: int
    overflow_events: int
    last_update: str

class ClauseManifest(BaseModel):
    clause_id: str
    description: str
    emotional_tags: List[str]
    fallback_clause: Optional[str]
    integrity_hash: str

class ManifestResponse(BaseModel):
    manifest_version: str
    clauses: List[ClauseManifest]
    total_clauses: int

class SSIPAuditResponse(BaseModel):
    drift_suppression: float
    messenger_pairing_fidelity: float
    emotional_fidelity: float
    sanctification_locks_active: bool
    compliance_status: str

class HealthCheckResponse(BaseModel):
    status: str
    version: str
    timestamp: str
    uptime_seconds: float

class LicenseStatusResponse(BaseModel):
    edition: str
    is_trial: bool
    trial_started_at: Optional[str]
    trial_ends_at: Optional[str]
    days_remaining: Optional[int]
    status: str
    purchase_url: Optional[str]
    upgrade_price_usd_year: Optional[int]

class PricingBreakdownResponse(BaseModel):
    base_price_usd: int
    inflation_rate: Optional[float]
    base_year: int
    current_year: int
    years_elapsed: int
    size_multiplier: Optional[float]
    computed_price_usd: int

class PilotStatusResponse(BaseModel):
    paywall_enabled: bool
    access_granted: bool
    pilot_price_usd: int
    purchase_url: Optional[str]
    enterprise_price_usd_year: int

# ===================== AUTH =====================
VALID_API_KEYS = {
    "dev_test_key_001": {"name": "Development License", "roles": ["read", "invoke"]},
    "ent_prod_key_001": {"name": "Enterprise License", "roles": ["read", "invoke", "admin"]},
    "sov_airgap_key_001": {"name": "Sovereign License", "roles": ["read", "invoke", "admin", "audit"]},
}
RATE_LIMIT_STORE: Dict[str, List[float]] = {}

def check_rate_limit(api_key: str, limit: int = 100, window: int = 60) -> bool:
    now = datetime.utcnow().timestamp()
    events = RATE_LIMIT_STORE.setdefault(api_key, [])
    RATE_LIMIT_STORE[api_key] = [ts for ts in events if now - ts < window]
    if len(RATE_LIMIT_STORE[api_key]) >= limit:
        return False
    RATE_LIMIT_STORE[api_key].append(now)
    return True

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    api_key = credentials.credentials
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if not check_rate_limit(api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    return api_key

def require_role(role: str):
    async def _inner(api_key: str = Depends(verify_api_key)):
        if role not in VALID_API_KEYS[api_key]["roles"]:
            raise HTTPException(status_code=403, detail=f"Insufficient permissions: {role} required")
        return api_key
    return _inner

# ===================== LICENSE & PRICING =====================
LICENSE_MODE = os.getenv("MYTHARA_LICENSE_MODE", "trial").lower()
LICENSE_FILE = os.getenv("MYTHARA_LICENSE_PATH", "/tmp/mythara_license.json")
LICENSE_KEY = os.getenv("MYTHARA_LICENSE_KEY")
LICENSE_TRIAL_DAYS = int(os.getenv("MYTHARA_LICENSE_TRIAL_DAYS", "30"))
PURCHASE_URL = os.getenv("MYTHARA_PURCHASE_URL", "https://buy.stripe.com/test_placeholder")
CONTACT_EMAIL = os.getenv("MYTHARA_CONTACT_EMAIL", "Mythara.Engine@yahoo.com")
PRICE_BASE_YEAR = int(os.getenv("MYTHARA_PRICE_BASE_YEAR", "2025"))
INFLATION_RATE_ANNUAL = os.getenv("MYTHARA_INFLATION_RATE_ANNUAL")

PILOT_PAYWALL_ENABLED = os.getenv("MYTHARA_PILOT_PAYWALL", "false").lower() in ["1", "true", "yes", "on"]
PILOT_PRICE_USD = int(os.getenv("MYTHARA_PILOT_PRICE_USD", "49"))
PILOT_PURCHASE_URL = os.getenv("MYTHARA_PILOT_PURCHASE_URL")
PILOT_ACCESS_FILE = os.getenv("MYTHARA_PILOT_ACCESS_PATH", "/tmp/mythara_pilot_access.json")
PILOT_FORCE_UNLOCK = os.getenv("MYTHARA_PILOT_FORCE_UNLOCK", "false").lower() in ["1", "true", "yes", "on"]
PILOT_UNLOCK_TOKEN = os.getenv("MYTHARA_PILOT_UNLOCK_TOKEN")

ENTERPRISE_TIERS = {
    "foundation": {"name": "Foundation", "base_price": 25000, "employee_range": (1, 50), "multiplier": 1.0},
    "professional": {"name": "Professional", "base_price": 40000, "employee_range": (51, 200), "multiplier": 1.6},
    "corporate": {"name": "Corporate", "base_price": 75000, "employee_range": (201, 1000), "multiplier": 3.0},
    "enterprise": {"name": "Enterprise", "base_price": 150000, "employee_range": (1001, 5000), "multiplier": 6.0},
    "sovereign": {"name": "Sovereign", "base_price": 300000, "employee_range": (5001, 999999), "multiplier": 12.0},
}

def compute_enterprise_price_for_company_size(employee_count: int, tier_key: Optional[str] = None) -> Dict[str, Any]:
    if tier_key is None:
        for key, tier in ENTERPRISE_TIERS.items():
            lo, hi = tier["employee_range"]
            if lo <= employee_count <= hi:
                tier_key = key
                break
        if tier_key is None:
            tier_key = "sovereign"
    tier = ENTERPRISE_TIERS[tier_key]
    base = tier["base_price"]
    rate = None
    if INFLATION_RATE_ANNUAL:
        try:
            rate = float(INFLATION_RATE_ANNUAL)
        except ValueError:
            rate = None
    years = max(0, datetime.utcnow().year - PRICE_BASE_YEAR)
    final_price = base * ((1 + rate) ** years) if rate is not None else base
    return {"tier": tier_key, "name": tier["name"], "base_price": base, "final_price": int(round(final_price))}

def compute_current_enterprise_price(tier_key: str = "corporate") -> int:
    return compute_enterprise_price_for_company_size(500, tier_key)["final_price"]

# ===================== IN-MEMORY STATE =====================
BR_STATE = {"reservoir_score": 0.91, "total_blessings": 12847, "overflow_events": 2, "last_update": datetime.utcnow().isoformat() + "Z"}
CLAUSE_DB = {
    "Legacy_Seed": {"description": "Ancestral memory harmonization clause", "emotional_tags": ["grief", "legacy", "ancestral"], "fallback_clause": "Shadow_Resolver", "emotional_fidelity_baseline": 0.93},
    "Hope_Anchor": {"description": "Future-oriented resilience clause", "emotional_tags": ["hope", "resilience", "forward"], "fallback_clause": "Shadow_Resolver", "emotional_fidelity_baseline": 0.89},
    "Shadow_Resolver": {"description": "Fallback safety clause", "emotional_tags": ["safety", "fallback", "neutral"], "fallback_clause": None, "emotional_fidelity_baseline": 0.95},
}
SSIP_METRICS = {"drift_suppression": 0.992, "messenger_pairing_fidelity": 0.994, "emotional_fidelity": 0.93, "sanctification_locks_active": True}

# ===================== LICENSE HELPERS =====================

def _read_license_state() -> Dict[str, Any]:
    try:
        with open(LICENSE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception:
        return {}

def _write_license_state(state: Dict[str, Any]) -> None:
    try:
        with open(LICENSE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f)
    except Exception:
        pass

def _init_trial_if_needed():
    if LICENSE_MODE != "trial":
        return
    state = _read_license_state()
    if not state.get("trial_started_at"):
        started = datetime.utcnow().isoformat() + "Z"
        state.update({"mode": "trial", "trial_started_at": started, "trial_days": LICENSE_TRIAL_DAYS})
        _write_license_state(state)

def _compute_license_status(api_key: Optional[str] = None) -> LicenseStatusResponse:
    if api_key and api_key in VALID_API_KEYS and ("admin" in VALID_API_KEYS[api_key]["roles"] or "audit" in VALID_API_KEYS[api_key]["roles"]):
        edition = "Sovereign" if "audit" in VALID_API_KEYS[api_key]["roles"] else "Enterprise"
        return LicenseStatusResponse(edition=edition, is_trial=False, trial_started_at=None, trial_ends_at=None, days_remaining=None, status="ACTIVE", purchase_url=PURCHASE_URL, upgrade_price_usd_year=None)
    if LICENSE_MODE in ("enterprise", "sovereign"):
        edition = "Sovereign" if LICENSE_MODE == "sovereign" else "Enterprise"
        return LicenseStatusResponse(edition=edition, is_trial=False, trial_started_at=None, trial_ends_at=None, days_remaining=None, status="ACTIVE", purchase_url=PURCHASE_URL, upgrade_price_usd_year=None)
    state = _read_license_state()
    started_raw = state.get("trial_started_at")
    trial_days = int(state.get("trial_days", LICENSE_TRIAL_DAYS))
    if not started_raw:
        started_dt = datetime.utcnow()
    else:
        try:
            started_dt = datetime.fromisoformat(started_raw.replace("Z", ""))
        except Exception:
            started_dt = datetime.utcnow()
    ends_dt = started_dt + timedelta(days=trial_days)
    now = datetime.utcnow()
    remaining = max(0, (ends_dt - now).days)
    status = "ACTIVE" if now < ends_dt else "EXPIRED"
    return LicenseStatusResponse(edition="Trial", is_trial=True, trial_started_at=started_dt.isoformat() + "Z", trial_ends_at=ends_dt.isoformat() + "Z", days_remaining=remaining, status=status, purchase_url=PURCHASE_URL, upgrade_price_usd_year=compute_current_enterprise_price())

# ===================== PILOT HELPERS =====================

def _read_pilot_access_state() -> Dict[str, Any]:
    try:
        with open(PILOT_ACCESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception:
        return {}

def _write_pilot_access_state(state: Dict[str, Any]) -> None:
    try:
        with open(PILOT_ACCESS_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f)
    except Exception:
        pass

def _has_pilot_access() -> bool:
    if not PILOT_PAYWALL_ENABLED:
        return True
    return bool(_read_pilot_access_state().get("pilot_granted_at"))

def _grant_pilot_access(payment_id: str, amount_paid: float, email: str) -> Dict[str, Any]:
    state = {"pilot_granted_at": datetime.utcnow().isoformat() + "Z", "payment_id": payment_id, "amount_paid_usd": amount_paid, "email": email, "price_required_usd": PILOT_PRICE_USD}
    _write_pilot_access_state(state)
    return state

def _force_grant_pilot_access(reason: str = "operator_override") -> Dict[str, Any]:
    return _grant_pilot_access(payment_id=f"FORCED-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}", amount_paid=0.0, email=CONTACT_EMAIL)

def require_active_license():
    async def _dep(response: Response, api_key: str = Depends(verify_api_key)):
        lic = _compute_license_status(api_key)
        response.headers["X-Mythara-License-Edition"] = lic.edition
        if lic.is_trial:
            response.headers["X-Mythara-License-Days-Remaining"] = str(lic.days_remaining or 0)
            response.headers["X-Mythara-License-Status"] = lic.status
            response.headers["X-Mythara-Enterprise-Price-USD"] = str(compute_current_enterprise_price())
        else:
            response.headers["X-Mythara-License-Status"] = "ACTIVE"
        if lic.is_trial and lic.status == "EXPIRED":
            raise HTTPException(status_code=402, detail={"message": "Trial expired. Upgrade to Enterprise.", "purchase_url": PURCHASE_URL, "price_usd_year": compute_current_enterprise_price()})
        return api_key
    return _dep

# ===================== STARTUP LICENSE VALIDATION =====================
@app.on_event("startup")
async def validate_license_on_startup():
    global LICENSE_MODE
    if LICENSE_KEY:
        try:
            from .license_manager import validate_license_key
        except Exception:
            validate_license_key = lambda k: {"valid": k.startswith("MYTHARA-")}
        data = validate_license_key(LICENSE_KEY)
        if data.get("valid"):
            code = data.get("edition_code", "ent").lower()
            LICENSE_MODE = "enterprise" if code == "ent" else ("sovereign" if code == "sov" else LICENSE_MODE)
            logger.info(f"✅ License activated: {data.get('edition','Enterprise')}")
        else:
            logger.error("❌ Invalid license key; falling back to trial")
    if LICENSE_MODE == "trial":
        _init_trial_if_needed()
        lic = _compute_license_status()
        if lic.status == "EXPIRED":
            logger.error("Trial expired; server will still start but API calls will return 402.")
        if PILOT_PAYWALL_ENABLED and PILOT_FORCE_UNLOCK and not _has_pilot_access():
            _force_grant_pilot_access("startup_env")
            logger.warning("Pilot paywall bypassed (force unlock enabled)")

# ===================== MIDDLEWARE =====================
@app.middleware("http")
async def enforce_trial_expiration_middleware(request: Request, call_next):
    path = request.url.path
    if path in {"/", "/health", "/pricing", "/download/pilot", "/debug/middleware"}:
        return await call_next(request)
    if path in {"/api/docs", "/docs", "/redoc", "/openapi.json"}:
        return await call_next(request)
    if path in {"/v1/license/status", "/v1/pilot/status", "/v1/pilot/unlock"}:
        return await call_next(request)
    if path in {"/v1/pricing/enterprise", "/api/webhooks/stripe"}:
        return await call_next(request)
    if path.startswith("/static/"):
        return await call_next(request)
    if LICENSE_MODE == "trial" and not LICENSE_KEY:
        if PILOT_PAYWALL_ENABLED and not _has_pilot_access():
            return Response(content=json.dumps({"error": "pilot_fee_required", "message": "Pilot fee required before trial.", "pilot_purchase_url": PILOT_PURCHASE_URL, "pilot_price_usd": PILOT_PRICE_USD, "contact": CONTACT_EMAIL}), status_code=402, media_type="application/json")
        lic = _compute_license_status()
        if lic.status == "EXPIRED":
            return Response(content=json.dumps({"error": "trial_expired", "message": "Trial ended. Upgrade required.", "purchase_url": PURCHASE_URL, "price_usd_year": compute_current_enterprise_price(), "contact": CONTACT_EMAIL}), status_code=402, media_type="application/json")
    return await call_next(request)

# ===================== ENDPOINTS =====================
try:
    import stripe
except Exception:
    stripe = None
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

def _send_license_email_stub(to_email: str, license_key: str, company_name: str, amount_paid: float) -> None:
    subject = "Your Mythara Enterprise License Key"
    body = f"License: {license_key}\nCompany: {company_name}\nPaid: ${amount_paid:,.0f}\nUpgrade URL: {PURCHASE_URL}\n"
    logger.info(f"Email prepared for {to_email}: {subject}\n{body}")

@app.post("/api/webhooks/stripe")
async def stripe_webhook(request: Request):
    raw = await request.body()
    shared_secret = request.headers.get("x-shared-secret")
    if STRIPE_WEBHOOK_SECRET and shared_secret == STRIPE_WEBHOOK_SECRET:
        data = {}
        try:
            data = await request.json()
        except Exception:
            pass
        email = data.get("email") or CONTACT_EMAIL
        company = data.get("company_name") or data.get("name") or "Customer"
        amount = float(data.get("amount") or 60000)
        purchase_type = data.get("license_type")
        payment_id = data.get("payment_id") or secrets.token_hex(8)
        if purchase_type == "pilot" or (PILOT_PAYWALL_ENABLED and abs(amount - PILOT_PRICE_USD) < 0.01):
            _grant_pilot_access(payment_id, amount, email)
            return {"status": "ok", "pilot_access_granted": True}
        try:
            from .license_manager import generate_license_key
        except Exception:
            generate_license_key = lambda prefix, company, email: f"MYTHARA-{prefix}-{secrets.token_hex(6)}"
        license_key = generate_license_key("ENT", company, email)
        _send_license_email_stub(email, license_key, company, amount)
        return {"status": "ok", "license_key": license_key}
    if stripe and STRIPE_WEBHOOK_SECRET:
        sig = request.headers.get("stripe-signature")
        try:
            event = stripe.Webhook.construct_event(raw, sig, STRIPE_WEBHOOK_SECRET)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid signature")
        if event.get("type") == "checkout.session.completed":
            obj = event["data"]["object"]
            email = obj.get("customer_details", {}).get("email") or CONTACT_EMAIL
            company = obj.get("customer_details", {}).get("name") or "Customer"
            amount = float(obj.get("amount_total", 0)) / 100.0
            purchase_type = (obj.get("metadata", {}) or {}).get("license_type")
            if purchase_type == "pilot" and PILOT_PAYWALL_ENABLED:
                _grant_pilot_access(obj.get("id") or secrets.token_hex(8), amount, email)
                return {"status": "ok", "pilot_access_granted": True}
            try:
                from .license_manager import generate_license_key
            except Exception:
                generate_license_key = lambda prefix, company, email: f"MYTHARA-{prefix}-{secrets.token_hex(8)}"
            license_key = generate_license_key("ENT", company, email)
            _send_license_email_stub(email, license_key, company, amount)
            return {"status": "ok", "license_key": license_key}
        return {"status": "ignored"}
    raise HTTPException(status_code=501, detail={"error": "webhook_not_configured"})

@app.get("/v1/pilot/status", response_model=PilotStatusResponse)
async def pilot_status():
    return PilotStatusResponse(paywall_enabled=PILOT_PAYWALL_ENABLED, access_granted=_has_pilot_access(), pilot_price_usd=PILOT_PRICE_USD, purchase_url=PILOT_PURCHASE_URL, enterprise_price_usd_year=compute_current_enterprise_price())

@app.get("/", response_model=HealthCheckResponse)
async def root():
    return {"status": "operational", "version": "1.0.0", "timestamp": datetime.utcnow().isoformat() + "Z", "uptime_seconds": 0.0}

@app.get("/health", response_model=HealthCheckResponse)
async def health():
    return {"status": "healthy", "version": "1.0.0", "timestamp": datetime.utcnow().isoformat() + "Z", "uptime_seconds": 0.0}

@app.get("/download/pilot")
async def download_pilot():
    from fastapi.responses import FileResponse
    fp = os.path.join(os.path.dirname(__file__), "../static/mythara-pilot-package.zip")
    if not os.path.exists(fp):
        raise HTTPException(status_code=404, detail="Pilot package not found")
    return FileResponse(path=fp, media_type="application/zip", filename="mythara-pilot-package.zip")

@app.get("/pricing")
async def pricing_page():
    from fastapi.responses import HTMLResponse
    fp = os.path.join(os.path.dirname(__file__), "../static/pricing.html")
    if not os.path.exists(fp):
        raise HTTPException(status_code=404, detail="Pricing page not found")
    with open(fp, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/debug/middleware")
async def debug_middleware():
    return {"status": "ok"}

@app.post("/v1/pilot/unlock")
async def pilot_unlock(request: Request):
    if not PILOT_UNLOCK_TOKEN:
        raise HTTPException(status_code=501, detail={"error": "unlock_disabled"})
    provided = request.headers.get("x-unlock-token") or request.query_params.get("token")
    if provided != PILOT_UNLOCK_TOKEN:
        raise HTTPException(status_code=403, detail={"error": "forbidden"})
    if not _has_pilot_access():
        _force_grant_pilot_access("operator_endpoint")
    return {"status": "ok", "pilot_access_granted": True}

@app.post("/v1/clauses/invoke", response_model=ClauseInvocationResponse)
async def invoke_clause(req: ClauseInvocationRequest, api_key: str = Depends(require_active_license())):
    if req.clause_id not in CLAUSE_DB:
        raise HTTPException(status_code=404, detail="Clause not found")
    clause = CLAUSE_DB[req.clause_id]
    invocation_id = f"INV-{datetime.utcnow().strftime('%Y%m%d')}-{secrets.token_hex(4)}"
    emotion = req.payload.get("emotion", "neutral")
    intensity = float(req.payload.get("intensity", 0.5))
    if emotion in clause["emotional_tags"]:
        emotional_fidelity = min(clause["emotional_fidelity_baseline"] + intensity * 0.05, 1.0)
    else:
        emotional_fidelity = clause["emotional_fidelity_baseline"] * 0.8
    blessings_delta = int(intensity * 100)
    BR_STATE["total_blessings"] += blessings_delta
    BR_STATE["reservoir_score"] = min(BR_STATE["reservoir_score"] + 0.01, 1.0)
    BR_STATE["last_update"] = datetime.utcnow().isoformat() + "Z"
    integrity_hash = hashlib.sha256(f"{invocation_id}{req.clause_id}{req.messenger}{emotional_fidelity}".encode()).hexdigest()
    return ClauseInvocationResponse(
        invocation_id=invocation_id,
        clause_id=req.clause_id,
        messenger=req.messenger,
        emotional_fidelity=round(emotional_fidelity, 3),
        blessings_delta=blessings_delta,
        timestamp=datetime.utcnow().isoformat() + "Z",
        integrity_hash=integrity_hash,
    )

@app.get("/v1/reservoir/status", response_model=ReservoirStatusResponse)
async def reservoir_status(api_key: str = Depends(verify_api_key)):
    return ReservoirStatusResponse(**BR_STATE)

@app.get("/v1/manifest/clauses", response_model=ManifestResponse)
async def manifest(api_key: str = Depends(verify_api_key)):
    items = []
    for cid, data in CLAUSE_DB.items():
        ih = hashlib.sha256(f"{cid}{data['description']}".encode()).hexdigest()
        items.append(ClauseManifest(clause_id=cid, description=data["description"], emotional_tags=data["emotional_tags"], fallback_clause=data["fallback_clause"], integrity_hash=ih))
    return ManifestResponse(manifest_version="v1.0.0", clauses=items, total_clauses=len(items))

@app.get("/v1/ssip/audit", response_model=SSIPAuditResponse)
async def ssip_audit(api_key: str = Depends(require_active_license())):
    key_data = VALID_API_KEYS.get(api_key, {})
    if "audit" not in key_data.get("roles", []):
        raise HTTPException(status_code=403, detail="Insufficient permissions: audit required")
    compliance_status = "PASS" if SSIP_METRICS["drift_suppression"] >= 0.989 else "FAIL"
    return SSIPAuditResponse(**SSIP_METRICS, compliance_status=compliance_status)

@app.get("/v1/clauses/{clause_id}", response_model=ClauseManifest)
async def clause_details(clause_id: str, api_key: str = Depends(verify_api_key)):
    if clause_id not in CLAUSE_DB:
        raise HTTPException(status_code=404, detail="Clause not found")
    data = CLAUSE_DB[clause_id]
    ih = hashlib.sha256(f"{clause_id}{data['description']}".encode()).hexdigest()
    return ClauseManifest(clause_id=clause_id, description=data["description"], emotional_tags=data["emotional_tags"], fallback_clause=data["fallback_clause"], integrity_hash=ih)

@app.get("/v1/license/status", response_model=LicenseStatusResponse)
async def license_status(api_key: str = Depends(verify_api_key)):
    return _compute_license_status(api_key)

@app.get("/v1/admin/pricing", response_model=PricingBreakdownResponse)
async def admin_pricing(api_key: str = Depends(require_role("admin"))):
    current_year = datetime.utcnow().year
    years = max(0, current_year - PRICE_BASE_YEAR)
    infl = None
    try:
        infl = float(INFLATION_RATE_ANNUAL) if INFLATION_RATE_ANNUAL else None
    except ValueError:
        infl = None
    mid = compute_enterprise_price_for_company_size(500, "corporate")
    return PricingBreakdownResponse(base_price_usd=mid["base_price"], inflation_rate=infl, base_year=PRICE_BASE_YEAR, current_year=current_year, years_elapsed=years, size_multiplier=ENTERPRISE_TIERS["corporate"]["multiplier"], computed_price_usd=compute_current_enterprise_price())

@app.get("/v1/pricing/enterprise")
async def pricing_enterprise(employees: Optional[int] = None, tier: Optional[str] = None):
    if employees is None and tier is None:
        all_tiers = {k: compute_enterprise_price_for_company_size(v["employee_range"][0], k) for k, v in ENTERPRISE_TIERS.items()}
        return {"tiers": all_tiers, "currency": "USD", "billing": "one-time annual license"}
    if tier:
        return {"pricing": compute_enterprise_price_for_company_size(100, tier), "currency": "USD"}
    return {"pricing": compute_enterprise_price_for_company_size(employees or 100), "currency": "USD"}

@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("Mythara Engine API - Starting")
    logger.info("Version: 1.0.0")
    logger.info(f"Loaded {len(CLAUSE_DB)} clauses")
    logger.info(f"BR Score: {BR_STATE['reservoir_score']:.2f}")
    logger.info("=" * 60)
    _init_trial_if_needed()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Mythara Engine API - Shutting down")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")