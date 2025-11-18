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
import hmac
import secrets
import logging
import json
import sys
import re
from pathlib import Path
import os
import httpx  # For ElevenLabs API calls
import base64

# Load environment variables (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, use system env vars only

# Configure logging BEFORE any other imports that use logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import database layer and email service
try:
    from database import (
        init_db, get_db, get_pilot, get_pilot_by_domain,
        create_pilot, get_usage_tracking, increment_usage,
        issue_strike, log_audit, queue_email
    )
    DATABASE_ENABLED = True
    logger.info("✅ Database services loaded")
except ImportError as e:
    DATABASE_ENABLED = False
    logger.warning(f"⚠️ Database not available, using in-memory storage: {e}")

# Optional email service (not critical for core functionality)
try:
    from email_service import (
        send_api_key_delivery, send_usage_alert_80_percent,
        send_expiration_alert_24hr, send_strike_warning
    )
    EMAIL_ENABLED = True
    logger.info("✅ Email services loaded")
except ImportError as e:
    EMAIL_ENABLED = False
    logger.warning(f"⚠️ Email service not available: {e}")
    # Define stub functions so the app doesn't crash
    def send_api_key_delivery(*args, **kwargs): pass
    def send_usage_alert_80_percent(*args, **kwargs): pass
    def send_expiration_alert_24hr(*args, **kwargs): pass
    def send_strike_warning(*args, **kwargs): pass

# Import Soul Proportion Model
from soul_proportion_model import (
    SoulProportionModel,
    EmotionFeatures,
    SoulProportionState,
    integrate_with_blessings_reservoir
)

# Import Soul Cradle Operator
from soul_cradle_operator import (
    SoulCradleOperator,
    Soul,
    Will,
    Commandments,
    Antithesis,
    Trial,
    CradleIntegrity,
    SoulCradleTiers
)

# Import Dual Framing Translation Layer
from dual_framing import (
    FramingMode,
    translate_response,
    format_for_manager_dashboard,
    get_positioning_line,
    generate_dual_framing_chart,
    generate_flow_diagram_text
)

# Import Soul Cradle Systems Framework
from soul_cradle_systems_framework import (
    SoulCradleParadox,
    SystemExpression,
    NonExpression,
    PrincipalSystem,
    ExpressionType,
    SystemType,
    TerminalRiskLevel,
    TerminalRiskCalculator,
    SystemQueryParser,
    log_paradox_creation
)

# Import Salesforce Integration
from salesforce_integration import (
    SalesforceIntegration,
    SalesforceConfig,
    SalesforceParadoxEvent,
    SalesforceSSIPMetric,
    SalesforceSoulCradleEvent,
    generate_salesforce_setup_instructions
)

# ElevenLabs Configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")  # Set via environment variable
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Rachel voice (default)
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

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

# Self-Regulation Middleware - Applied across all protected endpoints
@app.middleware("http")
async def self_regulation_middleware(request: Request, call_next):
    """
    Global self-regulation middleware that tracks usage and enforces rules
    across all API endpoints (except health checks and admin endpoints).
    """
    # Skip self-regulation for public/admin endpoints
    excluded_paths = ["/", "/health", "/api/docs", "/api/redoc", "/openapi.json", "/static", "/v1/admin"]
    if any(request.url.path.startswith(path) for path in excluded_paths):
        return await call_next(request)
    
    # Extract API key from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return await call_next(request)  # Let endpoint handle auth
    
    api_key = auth_header.replace("Bearer ", "").strip()
    
    # Extract employee count from request (query param, header, or body)
    employee_count = None
    
    # Try query parameter
    employee_count = request.query_params.get("employee_count")
    
    # Try header
    if not employee_count:
        employee_count = request.headers.get("X-Employee-Count")
    
    # Try body (for POST/PUT requests)
    if not employee_count and request.method in ["POST", "PUT"]:
        try:
            body = await request.body()
            if body:
                body_json = json.loads(body.decode())
                employee_count = body_json.get("employee_count")
        except:
            pass
    
    # Default to smallest tier if not provided
    employee_count = int(employee_count) if employee_count else 10
    
    # Run self-regulation check
    regulation_result = track_api_usage(api_key, employee_count)
    
    # Enforce termination
    if not regulation_result["allowed"]:
        enforcement = regulation_result.get("enforcement")
        
        if enforcement == "terminated":
            return Response(
                content=json.dumps({
                    "error": "account_terminated",
                    "message": "Your account has been permanently terminated due to repeated abuse violations.",
                    "strikes": regulation_result.get("strikes"),
                    "contact": CONTACT_EMAIL
                }),
                status_code=403,
                media_type="application/json"
            )
        elif enforcement == "suspended":
            suspension_end = regulation_result.get("suspension_end")
            return Response(
                content=json.dumps({
                    "error": "account_suspended",
                    "message": f"Your account is temporarily suspended until {suspension_end}.",
                    "suspension_end": suspension_end,
                    "strikes": regulation_result.get("strikes"),
                    "appeal_email": CONTACT_EMAIL
                }),
                status_code=403,
                media_type="application/json"
            )
        elif enforcement == "pilot_expired":
            return Response(
                content=json.dumps({
                    "error": "pilot_expired",
                    "message": "Your 7-day pilot has expired. Upgrade to Enterprise for continued hosted access.",
                    "days_used": regulation_result.get("days_used"),
                    "upgrade_options": {
                        "self_hosted": "Deploy on your own infrastructure (see PILOT_SELF_HOSTED_GUIDE.md)",
                        "enterprise_hosted": "Upgrade to Enterprise ($25K+/year) - Contact Mythara.Engine@yahoo.com"
                    },
                    "calls_made": regulation_result["usage_stats"]["calls_made"],
                    "contact": CONTACT_EMAIL
                }),
                status_code=402,  # Payment Required
                media_type="application/json"
            )
    
    # Log warnings
    if regulation_result.get("enforcement") == "warning":
        logging.warning(f"API key {api_key[:8]}... issued warning strike. Reason: {regulation_result.get('reason')}. Stats: {regulation_result.get('usage_stats')}")
    
    # Check rate limit
    if regulation_result["usage_stats"]["calls_made"] > regulation_result["usage_stats"]["total_limit"]:
        return Response(
            content=json.dumps({
                "error": "rate_limit_exceeded",
                "message": f"7-day pilot limit of {regulation_result['usage_stats']['total_limit']} calls exceeded.",
                "calls_made": regulation_result["usage_stats"]["calls_made"],
                "total_limit": regulation_result["usage_stats"]["total_limit"],
                "days_remaining": regulation_result["usage_stats"]["days_remaining"],
                "upgrade_url": "Contact Mythara.Engine@yahoo.com for Enterprise tier"
            }),
            status_code=429,
            media_type="application/json"
        )
    
    # Allow request to proceed
    response = await call_next(request)
    
    # Add usage headers to response
    response.headers["X-Rate-Limit-Limit"] = str(regulation_result["usage_stats"]["total_limit"])
    response.headers["X-Rate-Limit-Remaining"] = str(regulation_result["usage_stats"]["total_limit"] - regulation_result["usage_stats"]["calls_made"])
    response.headers["X-Pilot-Days-Remaining"] = str(regulation_result["usage_stats"]["days_remaining"])
    
    return response

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

class SoulStatusResponse(BaseModel):
    S_t: float = Field(description="Current soul proportion [0,1]")
    emotion_features: Dict[str, float]
    dynamics: Dict[str, float] = Field(description="{r, u, d} parameters")
    last_update: str
    integrity_hash: str

class SoulStepRequest(BaseModel):
    emotion_features: Dict[str, float] = Field(description="Emotion state: valence, arousal, connectedness, meaning, hope, stress, isolation")
    u_intervention: float = Field(default=0.0, description="External supportive input (therapy, ritual, etc.)")

class HolisticIntegrityResponse(BaseModel):
    holistic_integrity: float = Field(description="Combined BR + Soul metric [0,1]")
    br_score: float
    soul_proportion: float
    risk_flags: List[str]
    requires_support: bool
    integrity_hash: str
    timestamp: str

class SoulCradleRequest(BaseModel):
    will_paradox_strength: float = Field(description="Degree of contradiction [0,1]")
    will_description: str
    commandments: List[str]
    commandments_strictness: float = Field(default=0.8, description="Rigidity [0,1]")
    lucifer_active: bool = Field(default=True, description="Is test active?")
    lucifer_temptation: float = Field(default=0.7, description="Temptation strength [0,1]")
    choice: str = Field(description="The choice being made")
    soul_vessel_capacity: float = Field(default=0.8, description="Soul capacity [0,1]")
    soul_paradox_tolerance: float = Field(default=0.65, description="Paradox tolerance [0,1]")

class SoulCradleResponse(BaseModel):
    integrity: float = Field(description="Overall cradle integrity [0,1]")
    alignment_commandments: float
    tolerance_will: float
    choice: str
    obedience: bool
    reservoir_delta: int
    collapse: bool
    timestamp: str
    integrity_hash: str

class SoulCradleTiersResponse(BaseModel):
    tiers: List[Dict[str, Any]]

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

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

def check_ip_rate_limit(ip: str, limit: int = 60, window: int = 60) -> bool:
    """Rate limit by IP address for public endpoints."""
    now = datetime.utcnow().timestamp()
    key = f"ip_{ip}"
    events = RATE_LIMIT_STORE.setdefault(key, [])
    RATE_LIMIT_STORE[key] = [ts for ts in events if now - ts < window]
    if len(RATE_LIMIT_STORE[key]) >= limit:
        return False
    RATE_LIMIT_STORE[key].append(now)
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

# Pilot Abuse Prevention Settings
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

# API rate limits based on employee count (calls per month)
# 7-DAY PILOT: Time-limited trial with reasonable daily limits
# After 7 days, must upgrade to Enterprise for continued hosted access
API_RATE_LIMITS_BY_EMPLOYEE_COUNT = {
    (1, 10): 1000,        # Micro: 1K calls total (~143/day over 7 days)
    (11, 50): 5000,       # Small: 5K calls total (~714/day over 7 days)
    (51, 200): 15000,     # Medium: 15K calls total (~2.1K/day over 7 days)
    (201, 1000): 30000,   # Large: 30K calls total (~4.3K/day over 7 days)
    (1001, 999999): 50000 # Enterprise: 50K calls total (~7.1K/day over 7 days)
}

# Pilot duration (7 days)
PILOT_DURATION_DAYS = 7

# Enterprise tier gets unlimited hosted API access (paid customers only)
ENTERPRISE_HOSTED_ENABLED = os.getenv("MYTHARA_ENTERPRISE_HOSTED", "false").lower() in ["1", "true", "yes", "on"]

# Self-regulation thresholds for abuse detection
SELF_REGULATION_CONFIG = {
    "velocity_abuse_days": 1,  # Flag if rate limit exhausted in < 1 day (pilot is only 7 days)
    "strike_limits": {"warning": 1, "suspension": 2, "termination": 3},
    "suspension_duration_days": 7,
    "appeal_window_days": 30,
    "usage_multiplier_threshold": 3.0,  # Suspend if usage is 3x expected (more strict for time-limited)
}

# In-memory tracking for self-regulation (replace with Redis/DB in production)
USAGE_TRACKING: Dict[str, Dict[str, Any]] = {}
ACCOUNT_STATUS: Dict[str, Dict[str, Any]] = {}
DOMAIN_REGISTRY: Dict[str, str] = {}  # domain -> api_key mapping (one pilot per domain)

def extract_domain_from_email(email: str) -> Optional[str]:
    """
    Extract domain from email address for duplicate prevention.
    Returns None for free email providers (gmail, yahoo, etc.)
    """
    if not email or "@" not in email:
        return None
    
    domain = email.split("@")[1].lower().strip()
    
    # Block free email providers - require business domains
    free_providers = {
        "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", 
        "aol.com", "icloud.com", "protonmail.com", "mail.com"
    }
    
    if domain in free_providers:
        return None
    
    return domain

def check_domain_availability(email: str, api_key: str) -> Dict[str, Any]:
    """
    Check if domain can register for pilot (one pilot per business domain).
    Returns: {"allowed": bool, "reason": str, "existing_api_key": str}
    """
    domain = extract_domain_from_email(email)
    
    if not domain:
        return {
            "allowed": False,
            "reason": "business_email_required",
            "message": "Pilot tier requires a business email domain. Free email providers (gmail.com, yahoo.com, etc.) are not eligible."
        }
    
    # Check if domain already has a pilot account
    if domain in DOMAIN_REGISTRY:
        existing_key = DOMAIN_REGISTRY[domain]
        if existing_key != api_key:
            return {
                "allowed": False,
                "reason": "domain_already_registered",
                "message": f"The domain '{domain}' already has a pilot account. Only one pilot per business domain is allowed.",
                "existing_api_key_prefix": existing_key[:8] + "..."
            }
    
    # Register domain to this API key
    DOMAIN_REGISTRY[domain] = api_key
    
    return {
        "allowed": True,
        "domain": domain,
        "message": "Domain registered successfully"
    }

def get_api_rate_limit_for_employee_count(employee_count: int) -> int:
    """
    Return total API invocation limit for 7-day pilot period.
    
    PILOT TIER: Time-limited (7 days) with reasonable limits per company size
    ENTERPRISE TIER: Unlimited (paid customers, we absorb hosting costs)
    """
    # Check if this is an Enterprise customer (paid tier)
    if ENTERPRISE_HOSTED_ENABLED:
        return 999999999  # Unlimited for paid Enterprise customers
    
    # Pilot tier = limited calls over 7-day period
    for (lo, hi), limit in API_RATE_LIMITS_BY_EMPLOYEE_COUNT.items():
        if lo <= employee_count <= hi:
            return limit
    
    return 1000  # Default minimum for edge cases

def check_pilot_expiration(api_key: str, pilot_start_date: datetime) -> Dict[str, Any]:
    """
    Check if 7-day pilot has expired.
    Returns: {"expired": bool, "days_remaining": int, "message": str}
    """
    now = datetime.utcnow()
    days_elapsed = (now - pilot_start_date).days
    days_remaining = PILOT_DURATION_DAYS - days_elapsed
    
    if days_remaining <= 0:
        return {
            "expired": True,
            "days_remaining": 0,
            "days_used": days_elapsed,
            "message": f"Your 7-day pilot expired {abs(days_remaining)} days ago. Upgrade to Enterprise for continued access."
        }
    
    return {
        "expired": False,
        "days_remaining": days_remaining,
        "days_used": days_elapsed,
        "message": f"{days_remaining} days remaining in your pilot."
    }

def track_api_usage(api_key: str, employee_count: int) -> Dict[str, Any]:
    """
    Track API usage for self-regulation. Returns usage stats and any enforcement actions.
    Includes 7-day pilot expiration check.
    """
    now = datetime.utcnow()
    
    if api_key not in USAGE_TRACKING:
        USAGE_TRACKING[api_key] = {
            "first_call": now,
            "pilot_start_date": now,  # Track when pilot started
            "call_count": 0,
            "employee_count": employee_count,
            "total_limit": get_api_rate_limit_for_employee_count(employee_count),
        }
    
    usage = USAGE_TRACKING[api_key]
    
    # Check if 7-day pilot has expired
    pilot_status = check_pilot_expiration(api_key, usage["pilot_start_date"])
    
    if pilot_status["expired"] and not ENTERPRISE_HOSTED_ENABLED:
        return {
            "allowed": False,
            "enforcement": "pilot_expired",
            "days_remaining": 0,
            "days_used": pilot_status["days_used"],
            "reason": "7-day pilot period expired",
            "message": pilot_status["message"],
            "usage_stats": {
                "calls_made": usage["call_count"],
                "total_limit": usage["total_limit"],
                "days_remaining": 0
            }
        }
    
    # Increment call count
    usage["call_count"] += 1
    
    # Calculate usage metrics for 7-day pilot
    days_since_start = (now - usage["pilot_start_date"]).days + 1
    expected_daily_rate = usage["total_limit"] / PILOT_DURATION_DAYS
    expected_usage = expected_daily_rate * days_since_start
    usage_multiplier = usage["call_count"] / expected_usage if expected_usage > 0 else 0
    
    # Self-regulation checks
    action = None
    
    # Check 1: Velocity abuse (exhausted limit too quickly)
    if usage["call_count"] >= usage["total_limit"] and days_since_start <= SELF_REGULATION_CONFIG["velocity_abuse_days"]:
        action = "velocity_abuse"
    
    # Check 2: Usage pattern mismatch (using way more than declared size should)
    elif usage_multiplier >= SELF_REGULATION_CONFIG["usage_multiplier_threshold"]:
        action = "usage_mismatch"
    
    # Apply graduated enforcement
    if action:
        if api_key not in ACCOUNT_STATUS:
            ACCOUNT_STATUS[api_key] = {"strikes": 0, "status": "active", "history": []}
        
        account = ACCOUNT_STATUS[api_key]
        account["strikes"] += 1
        
        enforcement = None
        if account["strikes"] == SELF_REGULATION_CONFIG["strike_limits"]["warning"]:
            enforcement = "warning"
        elif account["strikes"] == SELF_REGULATION_CONFIG["strike_limits"]["suspension"]:
            enforcement = "suspension"
            account["status"] = "suspended"
            account["suspension_end"] = now + timedelta(days=SELF_REGULATION_CONFIG["suspension_duration_days"])
        elif account["strikes"] >= SELF_REGULATION_CONFIG["strike_limits"]["termination"]:
            enforcement = "termination"
            account["status"] = "terminated"
        
        account["history"].append({
            "timestamp": now.isoformat(),
            "action": action,
            "enforcement": enforcement,
            "call_count": usage["call_count"],
            "days_active": days_since_first,
            "usage_multiplier": usage_multiplier
        })
        
        return {
            "allowed": enforcement != "termination",
            "enforcement": enforcement,
            "strikes": account["strikes"],
            "reason": action,
            "usage_stats": {
                "calls_made": usage["call_count"],
                "monthly_limit": usage["monthly_limit"],
                "days_active": days_since_first,
                "usage_multiplier": round(usage_multiplier, 2)
            }
        }
    
    # Check if account is currently suspended
    if api_key in ACCOUNT_STATUS:
        account = ACCOUNT_STATUS[api_key]
        if account["status"] == "suspended":
            if "suspension_end" in account and now < account["suspension_end"]:
                return {
                    "allowed": False,
                    "enforcement": "suspended",
                    "strikes": account["strikes"],
                    "suspension_end": account["suspension_end"].isoformat(),
                    "reason": "Account temporarily suspended for abuse"
                }
            else:
                # Suspension expired, reactivate
                account["status"] = "active"
        elif account["status"] == "terminated":
            return {
                "allowed": False,
                "enforcement": "terminated",
                "strikes": account["strikes"],
                "reason": "Account permanently terminated for repeated abuse"
            }
    
    return {
        "allowed": True,
        "enforcement": None,
        "usage_stats": {
            "calls_made": usage["call_count"],
            "total_limit": usage["total_limit"],
            "days_remaining": pilot_status["days_remaining"]
        }
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

# Initialize Soul Proportion Model
SOUL_MODEL = SoulProportionModel(
    r_base=0.05,   # 5% intrinsic renewal (self-healing)
    u_base=0.02,   # 2% base supportive input
    d_base=0.03    # 3% base stress drag
)

# Current soul state (initialized to healthy baseline)
SOUL_STATE = {
    "S_t": 0.70,  # 70% emotional vitality
    "last_update": datetime.utcnow().isoformat() + "Z",
    "emotion_features": {
        "valence": 0.5,
        "arousal": 0.6,
        "connectedness": 0.7,
        "meaning": 0.7,
        "hope": 0.7,
        "stress": 0.3,
        "isolation": 0.2
    }
}

# Initialize Soul Cradle Operator
SOUL_CRADLE_OPERATOR = SoulCradleOperator(
    blessing_multiplier=10,  # 10 blessings per 0.1 integrity
    collapse_penalty=-50      # -50 blessings for soul collapse
)

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

def _grant_pilot_access(payment_id: str, amount_paid: float, email: str, api_key: Optional[str] = None, company_name: Optional[str] = None, employee_count: Optional[int] = 10, pilot_start_date: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Grant pilot access after payment. Enforces one pilot per business domain.
    Stores in database (if available) and sends welcome email.
    """
    # Generate API key if not provided
    if not api_key:
        api_key = f"mythara_pilot_{secrets.token_hex(16)}"
    
    # Use current time if pilot_start_date not provided
    if not pilot_start_date:
        pilot_start_date = datetime.utcnow()
    
    # Check domain availability (one pilot per domain)
    domain_check = check_domain_availability(email, api_key)
    
    if not domain_check["allowed"]:
        raise HTTPException(
            status_code=403,
            detail={
                "error": domain_check["reason"],
                "message": domain_check["message"],
                "contact": CONTACT_EMAIL
            }
        )
    
    domain = domain_check.get("domain")
    company_name = company_name or f"Company-{domain}"
    employee_count = employee_count or 10
    
    # Store in database (if enabled)
    if DATABASE_ENABLED:
        try:
            from database import SessionLocal
            db = SessionLocal()
            try:
                # Create pilot account
                pilot = create_pilot(
                    db=db,
                    api_key=api_key,
                    email=email,
                    domain=domain,
                    company_name=company_name,
                    employee_count=employee_count,
                    pilot_start_date=pilot_start_date,
                    stripe_payment_id=payment_id
                )
                
                # Send welcome email with API key
                from database import get_api_rate_limit_for_employee_count
                total_limit = get_api_rate_limit_for_employee_count(employee_count)
                pilot_expires = (pilot_start_date + timedelta(days=7)).strftime("%Y-%m-%d %H:%M UTC")
                
                send_api_key_delivery(
                    to_email=email,
                    api_key=api_key,
                    company_name=company_name,
                    employee_count=employee_count,
                    total_limit=total_limit,
                    pilot_expires=pilot_expires
                )
                
                logger.info(f"✅ Pilot created and email sent: {domain} ({api_key[:8]}...)")
                
                db.close()
            except Exception as e:
                db.close()
                logger.error(f"❌ Database pilot creation failed: {e}")
                raise
        except Exception as e:
            logger.error(f"❌ Pilot access grant failed: {e}")
            # Fall back to file-based storage below
    
    # Fall back to file-based storage (legacy support)
    state = {
        "pilot_granted_at": pilot_start_date.isoformat() + "Z",
        "payment_id": payment_id,
        "amount_paid_usd": amount_paid,
        "email": email,
        "domain": domain,
        "api_key": api_key,
        "company_name": company_name,
        "employee_count": employee_count,
        "price_required_usd": PILOT_PRICE_USD
    }
    _write_pilot_access_state(state)
    
    # Update DOMAIN_REGISTRY
    DOMAIN_REGISTRY[domain] = api_key
    
    logging.info(f"Pilot access granted: {email} (domain: {domain}, api_key: {api_key[:8]}...)")
    
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

def _validate_email(email: str) -> bool:
    """Validate email address with security checks."""
    if not isinstance(email, str):
        return False
    if len(email) > 254 or len(email) < 3:
        return False
    if "\x00" in email or ".." in email:
        return False
    # Basic RFC 5322 pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False
    # Block SQL injection patterns
    if any(danger in email.lower() for danger in ["drop", "select", "insert", "delete", "';", "--"]):
        return False
    return True

def _send_license_email_stub(to_email: str, license_key: str, company_name: str, amount_paid: float) -> None:
    if not _validate_email(to_email):
        logger.warning(f"Invalid email address rejected: {to_email}")
        return
    subject = "Your Mythara Enterprise License Key"
    body = f"License: {license_key}\nCompany: {company_name}\nPaid: ${amount_paid:,.0f}\nUpgrade URL: {PURCHASE_URL}\n"
    logger.info(f"Email prepared for {to_email}: {subject}\n{body}")

@app.post("/api/webhooks/stripe")
async def stripe_webhook(request: Request):
    # Rate limit webhooks by IP (60 per minute)
    client_ip = request.client.host if request.client else "unknown"
    if not check_ip_rate_limit(client_ip, limit=60, window=60):
        logger.warning(f"Webhook rate limit exceeded for IP: {client_ip}")
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    raw = await request.body()
    shared_secret = request.headers.get("x-shared-secret")
    if STRIPE_WEBHOOK_SECRET and shared_secret == STRIPE_WEBHOOK_SECRET:
        data = {}
        try:
            data = await request.json()
        except Exception:
            pass
        email = data.get("email") or CONTACT_EMAIL
        if not _validate_email(email):
            logger.warning(f"Invalid email in webhook: {email}")
            raise HTTPException(status_code=400, detail="Invalid email address")
        company_name = data.get("company_name") or data.get("name") or f"Company-{extract_domain_from_email(email)}"
        employee_count = int(data.get("employee_count", 10))
        amount = float(data.get("amount") or PILOT_PRICE_USD)
        purchase_type = data.get("license_type")
        payment_id = data.get("payment_id") or secrets.token_hex(8)
        payment_timestamp = data.get("timestamp")  # ISO format timestamp
        
        # Parse payment timestamp if provided
        pilot_start_date = datetime.utcnow()
        if payment_timestamp:
            try:
                pilot_start_date = datetime.fromisoformat(payment_timestamp.replace("Z", "+00:00"))
            except:
                pass
        
        if purchase_type == "pilot" or (PILOT_PAYWALL_ENABLED and abs(amount - PILOT_PRICE_USD) < 0.01):
            pilot_state = _grant_pilot_access(
                payment_id=payment_id,
                amount_paid=amount,
                email=email,
                company_name=company_name,
                employee_count=employee_count,
                pilot_start_date=pilot_start_date
            )
            return {
                "status": "ok",
                "pilot_access_granted": True,
                "api_key": pilot_state["api_key"][:8] + "..." + pilot_state["api_key"][-4:],
                "pilot_expires": (pilot_start_date + timedelta(days=7)).isoformat() + "Z"
            }
        try:
            from .license_manager import generate_license_key
        except Exception:
            generate_license_key = lambda prefix, company, email: f"MYTHARA-{prefix}-{secrets.token_hex(6)}"
        license_key = generate_license_key("ENT", company_name, email)
        _send_license_email_stub(email, license_key, company_name, amount)
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
            if not _validate_email(email):
                logger.warning(f"Invalid email in Stripe webhook: {email}")
                raise HTTPException(status_code=400, detail="Invalid email address")
            company_name = obj.get("customer_details", {}).get("name") or f"Company-{extract_domain_from_email(email)}"
            amount = float(obj.get("amount_total", 0)) / 100.0
            purchase_type = (obj.get("metadata", {}) or {}).get("license_type")
            
            # Extract employee count from metadata
            employee_count = 10
            metadata = obj.get("metadata", {}) or {}
            if "employee_count" in metadata:
                try:
                    employee_count = int(metadata["employee_count"])
                except:
                    pass
            
            # Use payment creation time as pilot start date
            pilot_start_date = datetime.utcnow()
            if "created" in obj:
                try:
                    pilot_start_date = datetime.fromtimestamp(obj["created"])
                except:
                    pass
            
            if purchase_type == "pilot" and PILOT_PAYWALL_ENABLED:
                pilot_state = _grant_pilot_access(
                    payment_id=obj.get("id") or secrets.token_hex(8),
                    amount_paid=amount,
                    email=email,
                    company_name=company_name,
                    employee_count=employee_count,
                    pilot_start_date=pilot_start_date
                )
                return {
                    "status": "ok",
                    "pilot_access_granted": True,
                    "api_key": pilot_state["api_key"][:8] + "..." + pilot_state["api_key"][-4:],
                    "pilot_expires": (pilot_start_date + timedelta(days=7)).isoformat() + "Z"
                }
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
async def pilot_status(request: Request):
    # Rate limit pilot status checks (30 per minute per IP)
    client_ip = request.client.host if request.client else "unknown"
    if not check_ip_rate_limit(client_ip, limit=30, window=60):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    return PilotStatusResponse(paywall_enabled=PILOT_PAYWALL_ENABLED, access_granted=_has_pilot_access(), pilot_price_usd=PILOT_PRICE_USD, purchase_url=PILOT_PURCHASE_URL, enterprise_price_usd_year=compute_current_enterprise_price())

@app.get("/v1/pilot/dashboard")
async def pilot_dashboard(request: Request, api_key: str = Depends(verify_api_key)):
    """
    Detailed pilot status dashboard - shows days remaining, calls used, total limit.
    Requires authentication with API key.
    """
    if DATABASE_ENABLED:
        try:
            from database import SessionLocal
            db = SessionLocal()
            try:
                pilot = get_pilot(db, api_key)
                usage = get_usage_tracking(db, api_key)
                
                if not pilot:
                    raise HTTPException(status_code=404, detail="Pilot not found")
                
                # Calculate days remaining
                days_elapsed = (datetime.utcnow() - pilot.pilot_start_date).days
                days_remaining = max(0, 7 - days_elapsed)
                pilot_expired = days_elapsed >= 7
                
                # Get usage stats
                calls_used = usage.call_count if usage else 0
                total_limit = usage.total_limit if usage else 0
                calls_remaining = max(0, total_limit - calls_used)
                percent_used = (calls_used / total_limit * 100) if total_limit > 0 else 0
                
                # Check if alerts have been sent
                sent_80_percent_alert = usage.sent_80_percent_alert if usage else False
                sent_24hr_alert = usage.sent_24hr_expiration_alert if usage else False
                
                # Enforcement status
                is_active = pilot.is_active
                is_suspended = pilot.suspended_until and pilot.suspended_until > datetime.utcnow()
                strike_count = pilot.strike_count
                
                db.close()
                
                return {
                    "status": "expired" if pilot_expired else ("suspended" if is_suspended else ("terminated" if not is_active else "active")),
                    "company_name": pilot.company_name,
                    "email": pilot.email,
                    "domain": pilot.domain,
                    "employee_count": pilot.employee_count,
                    "pilot_start_date": pilot.pilot_start_date.isoformat() + "Z",
                    "pilot_expires": (pilot.pilot_start_date + timedelta(days=7)).isoformat() + "Z",
                    "days_elapsed": days_elapsed,
                    "days_remaining": days_remaining,
                    "calls_used": calls_used,
                    "calls_remaining": calls_remaining,
                    "total_limit": total_limit,
                    "percent_used": round(percent_used, 1),
                    "strike_count": strike_count,
                    "is_suspended": is_suspended,
                    "suspended_until": pilot.suspended_until.isoformat() + "Z" if pilot.suspended_until else None,
                    "alerts_sent": {
                        "80_percent": sent_80_percent_alert,
                        "24hr_expiration": sent_24hr_alert
                    },
                    "upgrade_options": {
                        "self_hosted": "Deploy on your own infrastructure (see PILOT_SELF_HOSTED_GUIDE.md)",
                        "enterprise_hosted": f"Upgrade to Enterprise ($25K+/year) - ${pilot.company_name} pilot credit applied"
                    },
                    "contact": CONTACT_EMAIL
                }
            except Exception as e:
                db.close()
                raise
        except Exception as e:
            logger.error(f"Pilot dashboard error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # Fall back to in-memory USAGE_TRACKING
    if api_key in USAGE_TRACKING:
        usage = USAGE_TRACKING[api_key]
        pilot_start = usage.get("pilot_start_date", datetime.utcnow())
        days_elapsed = (datetime.utcnow() - pilot_start).days
        days_remaining = max(0, 7 - days_elapsed)
        
        return {
            "status": "expired" if days_elapsed >= 7 else "active",
            "pilot_start_date": pilot_start.isoformat() + "Z",
            "pilot_expires": (pilot_start + timedelta(days=7)).isoformat() + "Z",
            "days_elapsed": days_elapsed,
            "days_remaining": days_remaining,
            "calls_used": usage.get("call_count", 0),
            "total_limit": usage.get("total_limit", 0),
            "warning": "Using in-memory storage - data may be lost on restart. Database recommended.",
            "contact": CONTACT_EMAIL
        }
    
    raise HTTPException(status_code=404, detail="No pilot data found for this API key")

@app.get("/", response_model=HealthCheckResponse)
async def root(request: Request):
    # Rate limit health checks (100 per minute per IP)
    client_ip = request.client.host if request.client else "unknown"
    if not check_ip_rate_limit(client_ip, limit=100, window=60):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    return {"status": "operational", "version": "1.0.0", "timestamp": datetime.utcnow().isoformat() + "Z", "uptime_seconds": 0.0}

@app.get("/health", response_model=HealthCheckResponse)
async def health(request: Request):
    # Rate limit health checks (100 per minute per IP)
    client_ip = request.client.host if request.client else "unknown"
    if not check_ip_rate_limit(client_ip, limit=100, window=60):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    return {"status": "healthy", "version": "1.0.0", "timestamp": datetime.utcnow().isoformat() + "Z", "uptime_seconds": 0.0}

@app.get("/download/pilot")
async def download_pilot(request: Request):
    # Rate limit downloads (10 per minute per IP)
    client_ip = request.client.host if request.client else "unknown"
    if not check_ip_rate_limit(client_ip, limit=10, window=60):
        raise HTTPException(status_code=429, detail="Rate limit exceeded - please wait before downloading again")
    from fastapi.responses import FileResponse
    fp = os.path.join(os.path.dirname(__file__), "../static/mythara-pilot-package.zip")
    if not os.path.exists(fp):
        raise HTTPException(status_code=404, detail="Pilot package not found")
    return FileResponse(path=fp, media_type="application/zip", filename="mythara-pilot-package.zip")

@app.get("/pricing")
async def pricing_page(request: Request):
    # Rate limit pricing page (30 per minute per IP)
    client_ip = request.client.host if request.client else "unknown"
    if not check_ip_rate_limit(client_ip, limit=30, window=60):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    from fastapi.responses import HTMLResponse
    fp = os.path.join(os.path.dirname(__file__), "../static/pricing.html")
    if not os.path.exists(fp):
        raise HTTPException(status_code=404, detail="Pricing page not found")
    with open(fp, "r", encoding="utf-8") as f:
        return HTMLResponse(
            content=f.read(),
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )

@app.get("/terms")
async def terms_page(request: Request):
    """Serve the terms of service page"""
    from fastapi.responses import FileResponse
    
    # Serve the terms.html file from static directory
    terms_path = os.path.join(os.path.dirname(__file__), "../static/terms.html")
    if not os.path.exists(terms_path):
        raise HTTPException(status_code=404, detail="Terms page not found")
    
    return FileResponse(
        terms_path,
        media_type="text/html",
        headers={
            "Cache-Control": "public, max-age=300",
        }
    )

@app.post("/v1/mythara/chat", response_model=ChatResponse)
async def mythara_chat(req: ChatRequest, request: Request):
    """
    MytharaConnect chat endpoint for pricing page assistant
    
    Provides intelligent responses about:
    - Pricing tiers and features
    - Industry-specific use cases
    - Technical capabilities
    - Implementation guidance
    """
    # Rate limit (30 messages per hour per IP)
    client_ip = request.client.host if request.client else "unknown"
    if not check_ip_rate_limit(client_ip, limit=30, window=3600):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    
    message_lower = req.message.lower()
    
    # Track conversation context for redundant question detection
    conversation_id = req.conversation_id or hashlib.sha256(
        f"{client_ip}{datetime.utcnow().isoformat()}".encode()
    ).hexdigest()[:16]
    
    # Initialize conversation tracking in global state
    if conversation_id not in CONVERSATION_HISTORY:
        CONVERSATION_HISTORY[conversation_id] = {"asked_topics": [], "message_count": 0}
    
    CONVERSATION_HISTORY[conversation_id]["message_count"] += 1
    
    # Filter vulgar/inappropriate content with witty responses
    vulgar_words = ["fuck", "shit", "damn", "hell", "ass", "bitch", "bastard", "crap", "piss", "dick", "cock", "pussy"]
    if any(word in message_lower for word in vulgar_words):
        witty_responses = [
            "I appreciate your enthusiasm, but let's keep this professional - we're discussing enterprise AI governance, not a comedy roast. What can I help you with regarding our platform?",
            "That's certainly colorful language! I'm programmed for enterprise conversations, though. How about we discuss cryptographic integrity instead?",
            "I see you're testing my boundaries - very creative! But I'm built for boardroom discussions, not barroom banter. What Mythara features interest you?",
            "My governance protocols just flagged that for emotional fidelity violations. Let's redirect: would you like to know about our SSIP integrity system?",
            "Well, that escalated quickly! I'm here for serious AI governance talk. Perhaps you'd like to hear about our compliance features?",
        ]
        response = witty_responses[hash(message_lower) % len(witty_responses)]
        return ChatResponse(response=response, conversation_id=conversation_id)
    
    # Greetings and casual conversation
    if any(word in message_lower for word in ["hi", "hello", "hey", "greetings", "sup", "yo"]):
        response = "Hey! So glad you stopped by. I'm basically your go-to person for all things Mythara around here. Want to talk pricing, industry stuff, or how we make AI actually trustworthy? I got you. What are you curious about?"
    
    elif any(word in message_lower for word in ["thanks", "thank you", "thx", "appreciate"]):
        response = "No problem! Hit me up if you need anything else, okay?"
    
    elif any(word in message_lower for word in ["bye", "goodbye", "see you", "later"]):
        response = "Later! Seriously, come back anytime. I'm always here."
    
    elif any(phrase in message_lower for phrase in ["talk to me", "tell me more", "explain", "what can you do", "help me"]):
        response = "Sure! So basically, Mythara is like... a trust layer for AI. We use cryptographic proofs so you can actually verify AI outputs aren't BS. I can walk you through how it works, what industries we're crushing it in, pricing - whatever. Where do you want to start?"
    
    # Conversational, bite-sized responses
    # Track topic for redundancy detection
    current_topic = None
    if any(word in message_lower for word in ["pricing", "cost", "price", "how much", "expensive"]):
        current_topic = "pricing"
        response = "Okay so pricing! We've got four tiers. Pilot's 15 to 20K per year for a test run - and honestly the best part is you get all that money back if you upgrade. Growth is 35 to 40K per year for teams scaling up. Enterprise and Sovereign get pretty wild. Want details on those?"
    
    elif any(word in message_lower for word in ["enterprise", "sla", "support", "priority"]):
        current_topic = "enterprise"
        response = "Enterprise tier is 60K per year and it really does provide comprehensive support - you get 100K monthly invocations, round-the-clock priority support, SLA guarantees, and a dedicated solution engineer who gets to know your specific needs. It's designed for teams that need that extra layer of reliability and hands-on partnership. I'd be curious to hear what industry you're in, if you're comfortable sharing?"
    
    elif any(word in message_lower for word in ["pilot", "trial", "demo", "test", "poc", "proof of concept"]):
        current_topic = "pilot"
        response = "Pilot's honestly pretty smart - 15 to 20K per year for 30-90 days and you get our full support. Best part? Every dollar you spend gets credited if you upgrade. So it's basically a free trial that you actually pay for but then don't lose. Make sense? Want to know what we'd do during those 90 days?"
    
    elif any(word in message_lower for word in ["sovereign", "air gap", "on-premise", "airgap", "air-gap", "on premise"]):
        current_topic = "sovereign"
        response = "Sovereign/Air-Gap is our fortress mode - 150 to 180K per year for complete on-premise deployment with zero external dependencies. Government, defense, and highly regulated industries love this. No cloud, no worries. Need the technical details?"
    
    elif any(word in message_lower for word in ["growth", "scale", "scaling"]):
        current_topic = "growth"
        response = "Growth tier is 35 to 40K per year - it's the sweet spot between Pilot and Enterprise. You get solid invocation limits, standard support, and production-ready infrastructure. Perfect for teams ready to scale but not needing white-glove service yet."
    
    elif "banking" in message_lower or "finance" in message_lower or "financial" in message_lower:
        response = "Banking and finance are really built on trust and accountability, which is where Mythara fits naturally. Every loan decision, risk assessment, or fraud detection needs to be auditable and explainable. With our SHA-256 integrity proofs, you can show regulators exactly how your AI arrived at each decision - there's no black box mystery. Our emotional fidelity tracking also helps catch when AI starts to drift from approved parameters, which can prevent issues before they become problems. It's like having built-in compliance verification for every API call."
    
    elif "healthcare" in message_lower or "hospital" in message_lower or "medical" in message_lower or "health" in message_lower:
        response = "Healthcare is huge for us. Like, patient safety can't mess around with AI hallucinations, right? Our HIPAA-compliant setup gives you cryptographic proof everything's legit. Plus Soul Proportion tracking monitors patient emotional wellbeing over time. When it's life or death stuff, you need verification - not optional."
    
    elif "insurance" in message_lower:
        response = "Insurance is all about calculated risk, right? Mythara helps you prove your AI risk models are fair, auditable, and bias-free. When someone challenges a claim denial, you can show cryptographic integrity hashes proving the decision logic. Our drift suppression metrics catch when models start deviating from approved parameters - before it becomes a regulatory nightmare. Think of it as insurance for your insurance AI."
    
    elif "government" in message_lower or "public sector" in message_lower or "defense" in message_lower:
        current_topic = "government"
        response = "Government and defense need the Sovereign tier - complete air-gap deployment with zero external dependencies. You get full data sovereignty, enhanced audit controls, and custom SLAs. Every decision is cryptographically proven and immutable - critical when AI informs policy, benefits distribution, or national security. We even have special handling for classified environments."
    
    elif "education" in message_lower or "university" in message_lower or "school" in message_lower:
        current_topic = "education"
        response = "Education is deeply personal, and Mythara respects that. Our Soul Proportion tracking helps monitor student emotional wellbeing without being invasive - it's a reflective indicator, never a gatekeeper. For admissions, grading, or intervention systems, you get audit trails proving fairness and eliminating bias claims. Parents and accreditors love the transparency."
    
    elif "retail" in message_lower or "ecommerce" in message_lower or "e-commerce" in message_lower:
        current_topic = "retail"
        response = "Retail moves fast, and customer trust is everything. Mythara helps you prove your recommendation engines, pricing algorithms, and inventory predictions are fair and accurate. When customers question 'why did I see this price?', you have cryptographic proof. Our emotional fidelity tracking even helps you understand customer sentiment longitudinally - it's like having a trust score for every AI interaction."
    
    elif "tech" in message_lower or "saas" in message_lower or "software" in message_lower:
        current_topic = "tech"
        response = "Tech companies are building AI into everything, but investor and customer trust depends on proving it works as advertised. Mythara gives you the audit trails, integrity proofs, and compliance validation you need for SOC 2, enterprise sales, and board presentations. When a customer asks 'how do I know your AI isn't biased?', you show them SHA-256 hashes. Game changer for enterprise deals."
    
    elif any(word in message_lower for word in ["industry", "sector", "vertical"]):
        current_topic = "industry"
        response = "We support seven industries: Banking, Healthcare, Insurance, Education, Tech/SaaS, Retail, and Government. Each gets tailored governance rules, compliance checks, and impact metrics specific to your sector's needs. Which industry are you in? I can give you the specific benefits for your use case."
    
    elif any(word in message_lower for word in ["ssip", "integrity", "audit", "compliance", "hash"]):
        current_topic = "ssip"
        response = "SSIP! Okay so this is our Symbolic Service Integrity Protocol - basically every API response gets a SHA-256 hash, drift metrics, emotional fidelity scores, all that. It's like blockchain but for AI governance. You can literally prove your AI didn't mess up. Regulators eat this stuff up."
    
    elif any(word in message_lower for word in ["api", "integration", "technical", "sdk", "rest", "endpoint"]):
        current_topic = "api"
        response = "We're REST API-based, so integration is straightforward. We've got endpoints for clause invocation, soul proportion tracking, and more. Every response includes cryptographic proofs. Check /api/docs for interactive examples - it's pretty slick."
    
    elif any(word in message_lower for word in ["dual framing", "mythic", "enterprise terminology", "translation"]):
        response = "Dual-framing is genius - keep your mythic terms internally (Blessings Reservoir, Soul Proportion) but show enterprise-safe terminology externally (Resonance Reservoir, Impact Metrics). Just add ?frame=industry to any endpoint. Boardroom-ready in seconds!"
    
    elif any(word in message_lower for word in ["what is", "explain", "what does", "definition"]):
        response = "Okay! So Mythara is basically a trust layer for AI systems. We provide cryptographic integrity proofs, emotional fidelity tracking, and industry-aware compliance. Think of it like... every AI decision gets a fingerprint that proves it's legit. No hallucinations, no drift, just verifiable AI. What part interests you most?"
    
    elif any(word in message_lower for word in ["feature", "capability", "what can", "include"]):
        response = "The highlights: SHA-256 integrity hashes, emotional fidelity scoring, soul proportion modeling, industry-specific governance, and forensic audit trails. Everything's designed for enterprise compliance. Want me to dive deeper on any of these?"
    
    elif any(word in message_lower for word in ["soul", "proportion", "emotional"]):
        response = "Soul Proportion is a 0-1 metric tracking emotional vitality - things like valence, arousal, connectedness, hope, and stress. It's a reflective indicator, not a gatekeeper. Every measurement gets a SHA-256 integrity proof. Pretty elegant, right?"
    
    elif any(word in message_lower for word in ["blessing", "reservoir", "br"]):
        response = "Blessings Reservoir tracks benevolent force and positive impact over time - it's scored 0-1 and accumulates with aligned actions. In enterprise-speak, we call it the Resonance Reservoir. Every update includes cryptographic proof and timestamp."
    
    elif any(word in message_lower for word in ["clause", "invocation", "invoke"]):
        response = "Clause invocation is how you trigger our governance logic. Each clause has emotional tags, fidelity baselines, and messengers. When invoked, we calculate emotional fidelity, update the Blessings Reservoir, and return a SHA-256 hash proving the calculation."
    
    elif any(word in message_lower for word in ["messenger", "healer", "witness", "custodian"]):
        response = "We use five messengers: Healer (empathy/support), Witness (observation/validation), Custodian (boundaries/protection), Herald (celebration), and Scribe (documentation). Each plays a specific role in how clauses are processed. Want examples?"
    
    elif any(word in message_lower for word in ["gdpr", "hipaa", "compliance", "regulation", "sox"]):
        response = "We've got GDPR, HIPAA, SOC 2, and industry-specific regulations baked in. Every API response includes audit trails with SHA-256 hashes. Air-gap deployment available if you need maximum sovereignty. Rate limiting and RBAC included too."
    
    elif any(word in message_lower for word in ["setup", "install", "deploy", "implementation"]):
        response = "Implementation is pretty smooth: Pick your tier (Pilot's great for starting), get API keys and docs, integrate REST endpoints, configure industry settings, and start invoking clauses. Full onboarding support included. Pilot gets extra hand-holding."
    
    elif any(word in message_lower for word in ["security", "secure", "safe", "protect"]):
        response = "Security's built-in: SHA-256 cryptographic integrity, rate limiting, Bearer token auth, role-based access control, no PII stored, optional air-gap deployment, and forensic audit trails. All API traffic can be TLS-encrypted. What's your security concern?"
    
    elif any(word in message_lower for word in ["antithesis", "paradox", "will", "commandment"]):
        response = "The Soul Cradle models theological paradox - holding two opposing truths without collapse. It's used for complex decision modeling when you're facing contradictions. Quantifies paradox tolerance and cradle integrity. Fascinating stuff if you're into symbolic reasoning."
    
    elif any(word in message_lower for word in ["compare", "difference", "versus", "vs", "better than"]):
        response = "Unlike standard AI platforms, we provide cryptographic integrity proofs on every response. You get auditable, tamper-proof outputs with emotional fidelity metrics. We're focused on trust and compliance, not just pattern matching. Want specifics on how we differ?"
    
    elif any(word in message_lower for word in ["unique", "different", "special", "why mythara", "what makes"]):
        response = "Okay so what makes us different - we're literally the ONLY platform doing cryptographic integrity proofs with emotional fidelity tracking. Every AI output gets a SHA-256 hash. It's like giving each decision a fingerprint. Everyone else is like 'trust us!' and we're like 'here's the math.' Way cooler."
    
    elif any(word in message_lower for word in ["important", "why now", "business need", "why businesses", "why should"]):
        response = "Okay real talk - AI regulations are dropping everywhere and companies are getting slammed with liability for AI screw-ups. We give you forensic-grade proof that your AI is legit. When regulators show up asking 'how do you know your AI didn't hallucinate?' you just show them the cryptographic hashes. It's going from optional to absolutely necessary, like... yesterday."
    
    elif any(word in message_lower for word in ["regulation", "ai act", "liability", "legal", "lawsuit"]):
        response = "New regs like the EU AI Act require proof that AI systems are trustworthy. Without audit trails, companies face huge fines when AI screws up. We provide immutable SHA-256 proofs for every decision - turns regulatory risk into competitive advantage."
    
    elif any(word in message_lower for word in ["problem", "solve", "challenge", "pain point"]):
        response = "The core problem: AI systems hallucinate, drift, and lack auditability. Companies can't prove their AI outputs are trustworthy. Mythara solves this with cryptographic integrity hashes, emotional fidelity tracking, and drift suppression metrics. You get forensic-grade proof that AI decisions are valid - essential for healthcare, finance, and regulated industries."
    
    elif any(word in message_lower for word in ["glossary", "terms", "definitions", "dictionary", "terminology", "jargon"]):
        response = "Quick glossary:\n• SSIP - Symbolic Service Integrity Protocol (our cryptographic proof system)\n• Soul Proportion - Emotional vitality metric (0-1 scale)\n• Blessings Reservoir - Benevolent force tracker (aka Resonance Reservoir)\n• Clause - Governance logic unit you invoke\n• Messenger - Role types: Healer, Witness, Custodian, Herald, Scribe\n• Dual-Framing - Switch between mythic and enterprise terminology\n• Antithesis - Paradox modeling system\n\nNeed details on any of these?"
    
    elif any(word in message_lower for word in ["video", "commercial", "watch", "demo", "see it", "show me"]):
        response = "You should definitely watch our commercial! It really brings Mythara to life. Check it out here: https://www.youtube.com/watch?v=LRMkGplr1aI 🎥"
    
    # Check for redundant questions (Easter egg)
    if current_topic:
        asked_topics = CONVERSATION_HISTORY[conversation_id]["asked_topics"]
        if current_topic in asked_topics:
            # They're asking about the same topic again - Easter egg!
            response = f"You know what? I feel like we've covered {current_topic} already! Maybe you'd get more out of actually *seeing* Mythara in action. Check out our commercial - it's way better than me repeating myself: https://www.youtube.com/watch?v=LRMkGplr1aI 😊"
        else:
            asked_topics.append(current_topic)
    
    # Fallback with helpful guidance
    else:
        response = "Hmm, let me help you out! I'm your go-to person for:\n• Pricing tiers (Pilot through Sovereign)\n• What makes us unique (spoiler: cryptographic proofs!)\n• Industry solutions (Healthcare, Banking, Gov, etc.)\n• SSIP integrity & how it works\n• Compliance stuff (GDPR, HIPAA, SOC 2)\n• Technical integration\n• Watch our commercial!\n\nJust ask me something like 'tell me about pricing' or 'show me the video' - I'm here to help!"
    
    # Generate conversation ID if not provided
    conversation_id = req.conversation_id or hashlib.sha256(
        f"{client_ip}{datetime.utcnow().isoformat()}".encode()
    ).hexdigest()[:16]
    
    return ChatResponse(
        response=response,
        conversation_id=conversation_id
    )

@app.get("/v1/mythara/tts")
async def mythara_tts(text: str, request: Request):
    """Generate TTS audio using ElevenLabs for Mythara assistant"""
    if not ELEVENLABS_API_KEY:
        raise HTTPException(status_code=503, detail="TTS service not configured")
    
    # Rate limit (30 per minute per IP)
    client_ip = request.client.host if request.client else "unknown"
    if not check_ip_rate_limit(client_ip, limit=30, window=60):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{ELEVENLABS_API_URL}/{ELEVENLABS_VOICE_ID}",
                headers={
                    "xi-api-key": ELEVENLABS_API_KEY,
                    "Content-Type": "application/json"
                },
                json={
                    "text": text,
                    "model_id": "eleven_turbo_v2",  # Fast, good quality
                    "voice_settings": {
                        "stability": 0.5,      # Balanced
                        "similarity_boost": 0.75,  # Natural
                        "style": 0.5,          # Moderate expression
                        "use_speaker_boost": True
                    }
                }
            )
            
            if response.status_code == 200:
                # Return audio as base64 data URL for easy playback
                audio_data = response.content
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                return Response(
                    content=audio_data,
                    media_type="audio/mpeg",
                    headers={"Content-Disposition": "inline; filename=mythara.mp3"}
                )
            else:
                logger.error(f"ElevenLabs API error: {response.status_code} - {response.text}")
                raise HTTPException(status_code=500, detail="TTS generation failed")
                
    except Exception as e:
        logger.error(f"TTS generation error: {e}")
        raise HTTPException(status_code=500, detail="TTS service error")


@app.get("/debug/middleware")
async def debug_middleware():
    return {"status": "ok"}

@app.post("/v1/pilot/unlock")
async def pilot_unlock(request: Request):
    # Rate limit unlock attempts (5 per minute per IP)
    client_ip = request.client.host if request.client else "unknown"
    if not check_ip_rate_limit(client_ip, limit=5, window=60):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
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
    # Self-regulation is now handled by global middleware
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
async def reservoir_status(api_key: str = Depends(verify_api_key), frame: Optional[str] = None):
    """
    Get Blessings Reservoir status with optional dual-framing support.
    
    Query parameters:
        frame: "mythic" (default) or "industry" for enterprise-safe terminology
    
    Returns mythic terms by default (Blessings Reservoir), or industry overlay
    (Resonance Reservoir) when frame=industry.
    """
    response_data = BR_STATE
    
    # Apply dual-framing translation if requested
    if frame == "industry":
        response_data = translate_response(response_data, FramingMode.INDUSTRY)
    
    return response_data

@app.get("/v1/soul/status", response_model=SoulStatusResponse)
async def soul_status(api_key: str = Depends(verify_api_key), frame: Optional[str] = None):
    """
    Get current soul proportion state S(t) with optional dual-framing support.
    
    Soul proportion is a bounded [0,1] metric representing emotional vitality/coherence.
    NOT additive across people, NOT directly comparable without calibration.
    Use as reflective/supportive indicator, never as gatekeeper.
    
    Query parameters:
        frame: "mythic" (default) or "industry" for enterprise-safe terminology
    """
    # Compute dynamics from current emotion features
    emotions = EmotionFeatures(**SOUL_STATE["emotion_features"])
    r, u, d = SOUL_MODEL.compute_dynamics(emotions)
    
    # Generate integrity hash
    state_repr = f"{SOUL_STATE['S_t']:.6f}|{emotions.to_vector()}|{r:.6f}|{u:.6f}|{d:.6f}|{SOUL_STATE['last_update']}"
    integrity_hash = hashlib.sha256(state_repr.encode()).hexdigest()
    
    response_data = {
        "S_t": SOUL_STATE["S_t"],
        "emotion_features": SOUL_STATE["emotion_features"],
        "dynamics": {"r": round(r, 4), "u": round(u, 4), "d": round(d, 4)},
        "last_update": SOUL_STATE["last_update"],
        "integrity_hash": integrity_hash
    }
    
    # Apply dual-framing translation if requested
    if frame == "industry":
        response_data = translate_response(response_data, FramingMode.INDUSTRY)
    
    return response_data

@app.post("/v1/soul/step", response_model=SoulStatusResponse)
async def soul_step(req: SoulStepRequest, api_key: str = Depends(verify_api_key)):
    """
    Advance soul proportion by one time step.
    
    Implements bounded logistic dynamics:
    S_{t+1} = S_t + r·S_t(1-S_t) + u_t - d_t·S_t
    
    Args:
        emotion_features: Current emotion state (valence, arousal, connectedness, meaning, hope, stress, isolation)
        u_intervention: External supportive input (therapy, ritual, community support)
    
    Returns:
        Updated soul state with cryptographic audit trail (SHA-256 integrity hash)
    """
    # Parse emotion features
    emotions = EmotionFeatures(**req.emotion_features)
    
    # Advance dynamics
    state = SOUL_MODEL.step(
        S_t=SOUL_STATE["S_t"],
        emotion_features=emotions,
        u_intervention=req.u_intervention
    )
    
    # Update global state
    SOUL_STATE["S_t"] = state.S_t
    SOUL_STATE["emotion_features"] = req.emotion_features
    SOUL_STATE["last_update"] = state.timestamp.isoformat() + "Z"
    
    logger.info(f"Soul proportion step: S(t)={state.S_t:.4f}, r={state.r:.4f}, u={state.u:.4f}, d={state.d:.4f}")
    
    return SoulStatusResponse(
        S_t=state.S_t,
        emotion_features=req.emotion_features,
        dynamics={"r": round(state.r, 4), "u": round(state.u, 4), "d": round(state.d, 4)},
        last_update=SOUL_STATE["last_update"],
        integrity_hash=state.integrity_hash
    )

@app.get("/v1/soul/holistic", response_model=HolisticIntegrityResponse)
async def holistic_integrity(api_key: str = Depends(verify_api_key)):
    """
    Get holistic integrity metrics: combined Blessings Reservoir + Soul Proportion.
    
    Holistic Integrity = (BR_normalized + S(t)) / 2
    
    BR tracks operational/cryptographic integrity.
    S(t) tracks emotional vitality/coherence.
    Together they provide complete governance oversight.
    
    Returns risk flags if either metric drops below safety thresholds.
    """
    # Create soul state object
    emotions = EmotionFeatures(**SOUL_STATE["emotion_features"])
    r, u, d = SOUL_MODEL.compute_dynamics(emotions)
    
    state_repr = f"{SOUL_STATE['S_t']:.6f}|{emotions.to_vector()}|{r:.6f}|{u:.6f}|{d:.6f}|{SOUL_STATE['last_update']}"
    integrity_hash = hashlib.sha256(state_repr.encode()).hexdigest()
    
    soul_state = SoulProportionState(
        S_t=SOUL_STATE["S_t"],
        timestamp=datetime.fromisoformat(SOUL_STATE["last_update"].replace("Z", "")),
        emotion_features=emotions,
        m_t=SOUL_MODEL.compute_raw_score(emotions),
        r=r,
        u=u,
        d=d,
        integrity_hash=integrity_hash
    )
    
    # Integrate with BR
    br_score = BR_STATE["reservoir_score"] * 100.0  # Convert to [0, 100]
    integrated = integrate_with_blessings_reservoir(soul_state, br_score)
    
    logger.info(f"Holistic Integrity: {integrated['holistic_integrity']:.4f} (BR={br_score:.2f}, S={SOUL_STATE['S_t']:.4f})")
    
    return HolisticIntegrityResponse(**integrated)

@app.post("/v1/soul/cradle", response_model=SoulCradleResponse)
async def soul_cradle(req: SoulCradleRequest, api_key: str = Depends(verify_api_key)):
    """
    Invoke Soul Cradle Operator: Cradle(S, W, C) → Integrity(I)
    
    Quantifies the Soul as a vessel that holds God's Will (W) and
    God's Commandments (C), even when paradox arises.
    
    Measures obedience under contradiction and updates Blessings Reservoir.
    
    Args:
        will_paradox_strength: Degree of contradiction between W and C [0,1]
        will_description: Description of God's Will (sovereign paradox)
        commandments: List of rules for obedience
        commandments_strictness: Rigidity of commandment enforcement [0,1]
        lucifer_active: Whether Lucifer is testing the soul
        lucifer_temptation: Strength of worldly temptation [0,1]
        choice: The choice being made by the soul
        soul_vessel_capacity: Soul's capacity to hold paradox [0,1]
        soul_paradox_tolerance: Soul's tolerance of contradiction [0,1]
    
    Returns:
        CradleIntegrity with I, alignment, tolerance, obedience, and reservoir delta
    """
    # Construct symbolic entities
    W = Will(
        paradox_strength=req.will_paradox_strength,
        sovereignty_level=1.0,  # God's Will is always absolute
        description=req.will_description
    )
    
    C = Commandments(
        rules=req.commandments,
        clarity=0.9,  # Commandments are generally clear
        strictness=req.commandments_strictness
    )
    
    L = Lucifer(
        temptation_strength=req.lucifer_temptation,
        deception_level=0.5,
        active=req.lucifer_active
    )
    
    S = Soul(
        vessel_capacity=req.soul_vessel_capacity,
        obedience_history=[0.7],  # Default starting history
        paradox_tolerance=req.soul_paradox_tolerance,
        collapse_threshold=0.3
    )
    
    # Invoke cradle function
    result = SOUL_CRADLE_OPERATOR.cradle_function(S, W, C, L, req.choice)
    
    # Update Blessings Reservoir
    BR_STATE["total_blessings"] += result.reservoir_delta
    BR_STATE["reservoir_score"] = max(0.0, min(1.0, BR_STATE["reservoir_score"] + (result.reservoir_delta / 1000.0)))
    BR_STATE["last_update"] = datetime.utcnow().isoformat() + "Z"
    
    logger.info(f"Soul Cradle invocation: I={result.I:.4f}, obedience={result.obedience}, ΔBR={result.reservoir_delta}, collapse={result.collapse}")
    
    return SoulCradleResponse(
        integrity=result.I,
        alignment_commandments=result.alignment_C,
        tolerance_will=result.tolerance_W,
        choice=result.choice,
        obedience=result.obedience,
        reservoir_delta=result.reservoir_delta,
        collapse=result.collapse,
        timestamp=result.timestamp.isoformat() + "Z",
        integrity_hash=result.integrity_hash
    )

@app.get("/v1/soul/cradle/tiers", response_model=SoulCradleTiersResponse)
async def soul_cradle_tiers():
    """
    Get Soul Cradle deployment tiers (investor/compliance view).
    
    Shows tiered sophistication ladder:
    - Basic: Simple paradox tracker (mental health resilience)
    - Neurosymbolic: Decision tracker with audit trails (cybersecurity compliance)
    - Mythic-Resonant: Full SSIP integration (enterprise governance)
    
    Public endpoint (no auth required for tier documentation).
    """
    tiers = SoulCradleTiers.get_all_tiers()
    return SoulCradleTiersResponse(tiers=tiers)

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
async def pricing_enterprise(request: Request, employees: Optional[int] = None, tier: Optional[str] = None):
    # Rate limit public pricing endpoint (60 per minute per IP)
    client_ip = request.client.host if request.client else "unknown"
    if not check_ip_rate_limit(client_ip, limit=60, window=60):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    if employees is None and tier is None:
        all_tiers = {k: compute_enterprise_price_for_company_size(v["employee_range"][0], k) for k, v in ENTERPRISE_TIERS.items()}
        return {"tiers": all_tiers, "currency": "USD", "billing": "one-time annual license"}
    if tier:
        return {"pricing": compute_enterprise_price_for_company_size(100, tier), "currency": "USD"}
    return {"pricing": compute_enterprise_price_for_company_size(employees or 100), "currency": "USD"}

# ===================== DUAL FRAMING ENDPOINTS =====================

@app.get("/v1/dual-framing/chart")
async def dual_framing_chart():
    """
    Get the dual-framing chart (mythic truth vs industry overlay).
    
    Public endpoint for enterprise audiences to understand Mythara's translation layer.
    Returns chart showing how mythic terms map to industry-safe terminology.
    """
    chart = generate_dual_framing_chart()
    return {
        "positioning_line": get_positioning_line(),
        "chart": chart,
        "note": "Mythara Engine preserves mythic integrity internally while providing enterprise-safe overlays externally."
    }

@app.get("/v1/dual-framing/flow")
async def dual_framing_flow():
    """
    Get the dual-framing flow diagram (system architecture visualization).
    
    Public endpoint showing how Mythara overlays onto existing CRM/field platforms
    without disrupting compliance or workflows.
    """
    return {
        "flow_diagram": generate_flow_diagram_text(),
        "positioning_line": get_positioning_line(),
        "integration_note": "Mythara Engine integrates with any System of Record (CRM/field platform) as an overlay layer."
    }

@app.get("/v1/dual-framing/dashboard")
async def dual_framing_dashboard(
    api_key: str = Depends(verify_api_key),
    frame: Optional[str] = None
):
    """
    Get manager dashboard with dual-framing support.
    
    Combines Blessings Reservoir, Soul Proportion, and Soul Cradle metrics
    with optional industry-safe framing for external audiences.
    
    Query parameters:
        frame: "mythic" (default) or "industry" for enterprise-safe terminology
    """
    # Gather current metrics
    metrics = {
        "blessings_reservoir": BR_STATE["total_blessings"],
        "integrity_metric": BR_STATE.get("reservoir_score", 0.0),
        "expression_metric": SOUL_STATE["S_t"],
        "legacy_reservoir": BR_STATE["total_blessings"]  # Placeholder
    }
    
    # Determine framing mode
    mode = FramingMode.INDUSTRY if frame == "industry" else FramingMode.MYTHIC
    
    # Format for dashboard
    dashboard = format_for_manager_dashboard(metrics, mode, include_kpis=True)
    
    return dashboard

@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("Mythara Engine API - Starting")
    logger.info("Version: 1.0.0")
    logger.info(f"Loaded {len(CLAUSE_DB)} clauses")
    logger.info(f"BR Score: {BR_STATE['reservoir_score']:.2f}")
    logger.info("Dual-Framing Translation Layer: ACTIVE")
    logger.info("=" * 60)
    _init_trial_if_needed()

# ===================== MYTHARA CONNECT CHAT API =====================
# Add MytharaConnect chat widget for pricing page

@app.get("/v1/chat/widget.js")
async def chat_widget_script(request: Request):
    """JavaScript widget for embedding MytharaConnect chat on pricing page"""
    client_ip = request.client.host if request.client else "unknown"
    if not check_ip_rate_limit(client_ip, limit=100, window=60):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    return Response(content="""
// MytharaConnect Chat Widget - Industry Gatekeeper Modal
(function() {
    const API_BASE = window.location.origin;
    
    // Check if user already completed industry selection (session storage)
    const hasCompletedGatekeeper = sessionStorage.getItem('mythara_industry_selected');
    
    if (!hasCompletedGatekeeper) {
        // Create full-screen gatekeeper modal that blocks pricing page
        const gatekeeperHTML = `
            <div id="mythara-gatekeeper-overlay" style="
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                background: rgba(0, 0, 0, 0.95); z-index: 999999;
                display: flex; align-items: center; justify-content: center;
                animation: fadeIn 0.3s ease-in;
            ">
                <div id="mythara-gatekeeper-box" style="
                    background: white; border-radius: 16px; padding: 40px;
                    max-width: 500px; width: 90%; box-shadow: 0 12px 40px rgba(0,0,0,0.5);
                    animation: slideUp 0.4s ease-out;
                ">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <div style="font-size: 56px; margin-bottom: 16px;">🔗</div>
                        <h2 style="
                            margin: 0 0 12px 0; font-size: 28px; 
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                            background-clip: text; font-weight: bold;
                        ">Welcome to Mythara</h2>
                        <p style="color: #666; font-size: 16px; line-height: 1.6; margin: 0;">
                            Before showing you pricing, let's make sure we're speaking your language.
                        </p>
                    </div>
                    
                    <div style="margin-bottom: 24px;">
                        <label style="display: block; font-weight: 600; margin-bottom: 12px; color: #333; font-size: 15px;">
                            Which industry best describes your organization?
                        </label>
                        <select id="mythara-gatekeeper-industry" style="
                            width: 100%; padding: 14px; font-size: 15px;
                            border: 2px solid #e0e0e0; border-radius: 8px;
                            background: white; color: #333;
                            transition: border-color 0.2s;
                            font-family: system-ui;
                        " onfocus="this.style.borderColor='#667eea'" onblur="this.style.borderColor='#e0e0e0'">
                            <option value="">Select your industry...</option>
                            <option value="banking">🏦 Banking / Financial Services</option>
                            <option value="healthcare">🏥 Healthcare / Life Sciences</option>
                            <option value="insurance">📋 Insurance / Actuarial</option>
                            <option value="education">🎓 Education / Academic Research</option>
                            <option value="tech_saas">💻 Technology / SaaS</option>
                            <option value="retail">🛒 Retail / E-commerce</option>
                            <option value="government">🏛️ Government / Public Sector</option>
                        </select>
                    </div>
                    
                    <button id="mythara-gatekeeper-submit" style="
                        width: 100%; padding: 16px; font-size: 16px; font-weight: bold;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white; border: none; border-radius: 8px;
                        cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;
                        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
                    " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 16px rgba(102, 126, 234, 0.4)'"
                       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(102, 126, 234, 0.3)'">
                        Continue to Pricing →
                    </button>
                    
                    <p style="text-align: center; margin-top: 20px; font-size: 13px; color: #999;">
                        🔒 This helps us show you relevant pricing and compliance info
                    </p>
                </div>
            </div>
            
            <style>
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                @keyframes slideUp {
                    from { transform: translateY(30px); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }
                #mythara-gatekeeper-overlay { font-family: system-ui, -apple-system, sans-serif; }
            </style>
        `;
        
        document.body.insertAdjacentHTML('beforeend', gatekeeperHTML);
        
        // Prevent scrolling while modal is open
        document.body.style.overflow = 'hidden';
        
        document.getElementById('mythara-gatekeeper-submit').addEventListener('click', async function() {
            const select = document.getElementById('mythara-gatekeeper-industry');
            const industry = select.value;
            
            if (!industry) {
                select.style.borderColor = '#ff4444';
                select.focus();
                return;
            }
            
            const industryName = select.options[select.selectedIndex].text.replace(/[^a-zA-Z\\/\\s]/g, '').trim();
            
            // Store selection in session
            sessionStorage.setItem('mythara_industry_selected', industry);
            sessionStorage.setItem('mythara_industry_name', industryName);
            
            // Show loading state
            const overlay = document.getElementById('mythara-gatekeeper-overlay');
            overlay.innerHTML = `
                <div style="text-align: center; color: white;">
                    <div style="font-size: 64px; margin-bottom: 20px; animation: pulse 1.5s infinite;">⏳</div>
                    <h3 style="margin: 0; font-size: 24px; font-weight: 600;">Tailoring for ${industryName}...</h3>
                    <p style="opacity: 0.8; margin-top: 12px;">Fetching industry-specific pricing & compliance details</p>
                </div>
                <style>
                    @keyframes pulse {
                        0%, 100% { transform: scale(1); opacity: 1; }
                        50% { transform: scale(1.1); opacity: 0.8; }
                    }
                </style>
            `;
            
            // Fetch pricing data
            try {
                const response = await fetch(\`\${API_BASE}/v1/pricing/enterprise?tier=startup\`);
                const data = await response.json();
                const price = data.pricing.computed_price_usd;
                
                // Store pricing context
                sessionStorage.setItem('mythara_pricing', price);
                
                // Fade out and remove overlay
                setTimeout(() => {
                    overlay.style.animation = 'fadeOut 0.4s ease-out';
                    setTimeout(() => {
                        overlay.remove();
                        document.body.style.overflow = '';
                        
                        // Show success notification with chat widget
                        showChatWidget(industry, industryName, price);
                    }, 400);
                }, 1200);
                
            } catch (error) {
                console.error('Error fetching pricing:', error);
                overlay.innerHTML = `
                    <div style="background: white; padding: 40px; border-radius: 16px; text-align: center;">
                        <div style="font-size: 48px; margin-bottom: 16px;">⚠️</div>
                        <h3 style="color: #ff4444; margin: 0 0 12px 0;">Connection Error</h3>
                        <p style="color: #666;">Unable to load pricing. Please refresh the page.</p>
                        <button onclick="location.reload()" style="
                            margin-top: 20px; padding: 12px 24px; background: #667eea;
                            color: white; border: none; border-radius: 6px; cursor: pointer;
                        ">Reload Page</button>
                    </div>
                `;
            }
        });
        
        // Allow Enter key to submit
        document.getElementById('mythara-gatekeeper-industry').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                document.getElementById('mythara-gatekeeper-submit').click();
            }
        });
        
    } else {
        // User already passed gatekeeper, show chat widget immediately
        const industry = sessionStorage.getItem('mythara_industry_selected');
        const industryName = sessionStorage.getItem('mythara_industry_name');
        const price = sessionStorage.getItem('mythara_pricing');
        showChatWidget(industry, industryName, price);
    }
    
    function showChatWidget(industry, industryName, price) {
        const widgetHTML = `
            <div id="mythara-chat-widget" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; animation: slideInRight 0.5s ease-out;">
                <button id="mythara-chat-toggle" style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; border: none; border-radius: 50%; width: 60px; height: 60px;
                    font-size: 24px; cursor: pointer; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
                    transition: transform 0.2s, box-shadow 0.2s;
                " onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">💬</button>
                
                <div id="mythara-chat-box" style="
                    display: none; position: absolute; bottom: 80px; right: 0;
                    width: 380px; height: 500px; background: white; border-radius: 12px;
                    box-shadow: 0 8px 24px rgba(0,0,0,0.3); flex-direction: column;
                ">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white; padding: 16px; border-radius: 12px 12px 0 0; font-weight: bold;">
                        🔗 MytharaConnect - ${industryName}
                        <span style="float: right; cursor: pointer;" id="mythara-close">✕</span>
                    </div>
                    
                    <div id="mythara-messages" style="flex: 1; overflow-y: auto; padding: 16px; font-family: system-ui;">
                        <div style="background: #f0f0f0; padding: 14px; border-radius: 8px; margin-bottom: 12px; font-size: 13px; line-height: 1.6;">
                            <b>Welcome! Here's what's relevant for ${industryName}:</b>
                            <br><br>
                            <b>Your Challenge:</b><br>
                            ${getIndustryPainPoint(industry)}
                            <br><br>
                            <b>Mythara Solution:</b><br>
                            Cryptographic AI audit trails (SHA-256) that pass regulatory scrutiny.
                            <br><br>
                            <b>Pricing:</b><br>
                            💰 Pilot: <b>$500</b> (2 slots remaining)<br>
                            💼 Enterprise: <b>$${Math.round(price).toLocaleString()}/year</b>
                            <br><br>
                            <b>Questions?</b> Type below or ask to schedule a demo.
                        </div>
                    </div>
                    
                    <div style="padding: 12px; border-top: 1px solid #eee; display: flex;">
                        <input id="mythara-input" type="text" placeholder="Ask me anything..." style="
                            flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 20px;
                        ">
                        <button id="mythara-send" style="
                            width: 40px; height: 40px; padding: 0; margin-left: 8px;
                            background: #667eea; color: white; border: none;
                            border-radius: 50%; cursor: pointer; font-size: 18px;
                        ">➤</button>
                    </div>
                </div>
            </div>
            
            <style>
                @keyframes slideInRight {
                    from { transform: translateX(100px); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes fadeOut {
                    from { opacity: 1; }
                    to { opacity: 0; }
                }
            </style>
        `;
        
        document.body.insertAdjacentHTML('beforeend', widgetHTML);
        
        // Auto-open chat briefly to show personalized greeting
        setTimeout(() => {
            document.getElementById('mythara-chat-box').style.display = 'flex';
        }, 800);
        
        document.getElementById('mythara-chat-toggle').addEventListener('click', () => {
            const box = document.getElementById('mythara-chat-box');
            box.style.display = box.style.display === 'none' ? 'flex' : 'none';
        });
        
        document.getElementById('mythara-close').addEventListener('click', () => {
            document.getElementById('mythara-chat-box').style.display = 'none';
        });
        
        document.getElementById('mythara-send').addEventListener('click', sendMessage);
        document.getElementById('mythara-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }
    
    function sendMessage() {
        const input = document.getElementById('mythara-input');
        const message = input.value.trim();
        if (!message) return;
        
        const messagesDiv = document.getElementById('mythara-messages');
        
        messagesDiv.innerHTML += `
            <div style="background: #667eea; color: white; padding: 10px; border-radius: 12px; margin: 8px 0 8px 40px; font-size: 14px;">
                ${message}
            </div>
        `;
        
        input.value = '';
        
        // Simple responses based on keywords
        let response = '';
        const lower = message.toLowerCase();
        
        if (lower.includes('schedule') || lower.includes('demo') || lower.includes('call')) {
            response = `I'd love to schedule a demo! Here are my available slots:<br><br>
                • Tuesday 10am MT<br>
                • Wednesday 2pm MT<br><br>
                Email me at: herbert@mythara.com with your preferred time.`;
        } else if (lower.includes('price') || lower.includes('cost') || lower.includes('pricing')) {
            response = `💰 <b>Current Pricing:</b><br><br>
                <b>Pilot Program:</b> $500 (2 slots left this quarter)<br>
                <b>Enterprise:</b> Starting at $18,250/year<br><br>
                Early adopters get priority support + 6 months free upgrades.`;
        } else if (lower.includes('how') || lower.includes('what') || lower.includes('?')) {
            response = `Great question! Mythara Engine provides cryptographic audit trails (SHA-256 hashing) for every AI decision.
                <br><br>Regulators can mathematically verify zero tampering. It's provably immutable - same standard used by federal systems.
                <br><br>Want to see a technical validation report for ${selectedIndustry || 'your industry'}?`;
        } else {
            response = `Thanks for your interest! Here's what I can help with:<br><br>
                • Pricing & packages<br>
                • Schedule a demo<br>
                • Technical questions<br>
                • Industry-specific use cases<br><br>
                What would you like to know?`;
        }
        
        messagesDiv.innerHTML += `
            <div style="background: #f0f0f0; padding: 12px; border-radius: 12px; margin: 8px 40px 8px 0; font-size: 13px;">
                ${response}
            </div>
        `;
        
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    function getIndustryPainPoint(industry) {
        const painPoints = {
            'banking': 'Model risk management consuming 200+ hours per audit. OCC/CFPB demanding cryptographic proof.',
            'healthcare': 'FDA AI/ML guidance requiring provable model lineage. Patient safety reviews taking 200+ hours.',
            'insurance': 'State regulators demanding AI transparency for underwriting models (NAIC compliance).',
            'education': 'Department of Education requiring AI fairness documentation (FERPA compliance).',
            'tech_saas': 'Enterprise customers demanding AI audit trails before purchase (SOC 2 requirements).',
            'retail': 'FTC scrutiny on AI pricing/personalization. Consumer protection agencies demanding transparency.',
            'government': 'OMB M-24-10 requiring AI governance for federal agencies. GAO audits demanding cryptographic trails.'
        };
        return painPoints[industry] || 'AI governance and audit trail challenges consuming significant resources.';
    }
})();
""", media_type="application/javascript")

@app.get("/v1/chat/widget")
async def chat_widget_page():
    """Demo page showing MytharaConnect chat widget"""
    return Response(content="""
<!DOCTYPE html>
<html>
<head>
    <title>MytharaConnect Chat Widget - Demo</title>
    <style>
        body { font-family: system-ui; padding: 40px; max-width: 1000px; margin: 0 auto; }
        pre { background: #f5f5f5; padding: 20px; border-radius: 8px; overflow-x: auto; }
        .demo-section { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; padding: 60px 40px; border-radius: 12px; text-align: center; margin: 40px 0; }
    </style>
</head>
<body>
    <div class="demo-section">
        <h1 style="margin: 0; font-size: 48px;">🔗 MytharaConnect</h1>
        <p style="font-size: 20px; opacity: 0.9;">Industry-Aware AI Sales Agent</p>
        <p>Click the chat button in the bottom-right to test! →</p>
    </div>
    
    <h2>How to Add to Your Pricing Page</h2>
    <p>Add this single line before your closing <code>&lt;/body&gt;</code> tag:</p>
    
    <pre>&lt;script src="https://mytharaarchive-production.up.railway.app/v1/chat/widget.js"&gt;&lt;/script&gt;</pre>
    
    <h2>Features</h2>
    <ul>
        <li>✅ <b>Industry Detection</b> - Asks for industry upfront</li>
        <li>✅ <b>Tailored Messaging</b> - Custom pain points & regulatory refs per vertical</li>
        <li>✅ <b>Live Pricing</b> - Pulls real pricing from your API</li>
        <li>✅ <b>Mythara Governance</b> - Multi-tier validation with risk scoring</li>
        <li>✅ <b>Rate Limited</b> - 100 requests/min per IP</li>
    </ul>
    
    <h2>Supported Industries</h2>
    <p>Banking • Healthcare • Insurance • Education • Tech/SaaS • Retail • Government</p>
    
    <script src="/v1/chat/widget.js"></script>
</body>
</html>
""", media_type="text/html")

@app.get("/v1/admin/regulation-status")
async def get_regulation_status(
    api_key: str = Depends(verify_api_key),
    admin_token: Optional[str] = Header(None, alias="X-Admin-Token")
):
    """
    Admin endpoint to view self-regulation status across all accounts.
    Requires admin token for access.
    """
    # Simple admin auth (replace with proper auth in production)
    expected_admin_token = os.getenv("MYTHARA_ADMIN_TOKEN")
    if not expected_admin_token or admin_token != expected_admin_token:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Compile regulation statistics
    total_accounts = len(USAGE_TRACKING)
    suspended_count = sum(1 for acc in ACCOUNT_STATUS.values() if acc.get("status") == "suspended")
    terminated_count = sum(1 for acc in ACCOUNT_STATUS.values() if acc.get("status") == "terminated")
    warned_count = sum(1 for acc in ACCOUNT_STATUS.values() if acc.get("strikes", 0) > 0 and acc.get("status") == "active")
    
    return {
        "total_accounts": total_accounts,
        "active": total_accounts - suspended_count - terminated_count,
        "suspended": suspended_count,
        "terminated": terminated_count,
        "warned": warned_count,
        "accounts": {
            key[:8] + "...": {
                "status": status.get("status", "active"),
                "strikes": status.get("strikes", 0),
                "history": status.get("history", [])
            }
            for key, status in ACCOUNT_STATUS.items()
        }
    }

@app.post("/v1/admin/appeal")
async def process_appeal(
    api_key: str,
    appeal_reason: str,
    admin_token: Optional[str] = Header(None, alias="X-Admin-Token")
):
    """
    Admin endpoint to process appeals and reinstate accounts.
    """
    expected_admin_token = os.getenv("MYTHARA_ADMIN_TOKEN")
    if not expected_admin_token or admin_token != expected_admin_token:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    if api_key not in ACCOUNT_STATUS:
        raise HTTPException(status_code=404, detail="Account not found in regulation system")
    
    account = ACCOUNT_STATUS[api_key]
    
    # Reset strikes and reactivate
    account["strikes"] = 0
    account["status"] = "active"
    account["history"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "action": "appeal_approved",
        "reason": appeal_reason
    })
    
    if "suspension_end" in account:
        del account["suspension_end"]
    
    logging.info(f"Appeal approved for API key {api_key[:8]}... Reason: {appeal_reason}")
    
    return {
        "success": True,
        "message": "Account reinstated successfully",
        "api_key": api_key[:8] + "...",
        "new_status": "active"
    }

@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    logger.info("Mythara Engine API - Starting up")
    if DATABASE_ENABLED:
        try:
            init_db()
            logger.info("✅ Database initialized successfully")
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            logger.warning("⚠️ Falling back to in-memory storage")


# ====================================
# SALESFORCE INTEGRATION ENDPOINTS
# ====================================

class SalesforceConfigRequest(BaseModel):
    """Request to configure Salesforce integration"""
    instance_url: str
    client_id: str
    client_secret: str
    username: str
    password: str
    security_token: str
    api_version: str = "v59.0"


class SalesforceTestRequest(BaseModel):
    """Request to test Salesforce connection"""
    config: SalesforceConfigRequest


@app.get("/v1/integrations/salesforce/setup")
async def get_salesforce_setup_instructions():
    """
    Get instructions for setting up Salesforce custom objects.
    Public endpoint - no authentication required.
    """
    return {
        "instructions": generate_salesforce_setup_instructions(),
        "documentation_url": "https://mytharaarchive-production.up.railway.app/api/docs#/Integrations",
        "support_email": "support@mytharalabs.com"
    }


@app.post("/v1/integrations/salesforce/test")
async def test_salesforce_connection(
    request: SalesforceTestRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Test Salesforce connection with provided credentials.
    Requires valid Mythara API key (Enterprise/Global tier).
    """
    try:
        config = SalesforceConfig(**request.config.model_dump())
        sf = SalesforceIntegration(config)
        
        success = await sf.test_connection()
        
        if success:
            return {
                "success": True,
                "message": "Salesforce connection successful",
                "instance_url": config.instance_url,
                "api_version": config.api_version
            }
        else:
            raise HTTPException(
                status_code=400,
                detail="Salesforce connection failed - check credentials"
            )
    
    except Exception as e:
        logger.error(f"Salesforce test failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/integrations/salesforce/push/paradox")
async def push_paradox_to_salesforce(
    event: SalesforceParadoxEvent,
    salesforce_config: SalesforceConfigRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Push a paradox event to customer's Salesforce instance.
    Requires valid Mythara API key (Enterprise/Global tier).
    """
    try:
        config = SalesforceConfig(**salesforce_config.model_dump())
        sf = SalesforceIntegration(config)
        
        if not await sf.authenticate():
            raise HTTPException(status_code=401, detail="Salesforce authentication failed")
        
        record_id = await sf.push_paradox_event(event)
        
        if record_id:
            return {
                "success": True,
                "record_id": record_id,
                "event_type": "paradox",
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to create Salesforce record")
    
    except Exception as e:
        logger.error(f"Failed to push paradox to Salesforce: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/integrations/salesforce/push/ssip")
async def push_ssip_to_salesforce(
    metric: SalesforceSSIPMetric,
    salesforce_config: SalesforceConfigRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Push an SSIP metric to customer's Salesforce instance.
    Requires valid Mythara API key (Enterprise/Global tier).
    """
    try:
        config = SalesforceConfig(**salesforce_config.model_dump())
        sf = SalesforceIntegration(config)
        
        if not await sf.authenticate():
            raise HTTPException(status_code=401, detail="Salesforce authentication failed")
        
        record_id = await sf.push_ssip_metric(metric)
        
        if record_id:
            return {
                "success": True,
                "record_id": record_id,
                "metric_type": "ssip",
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to create Salesforce record")
    
    except Exception as e:
        logger.error(f"Failed to push SSIP metric to Salesforce: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/integrations/salesforce/push/soul-cradle")
async def push_soul_cradle_to_salesforce(
    event: SalesforceSoulCradleEvent,
    salesforce_config: SalesforceConfigRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Push a Soul Cradle witnessing event to customer's Salesforce instance.
    Requires valid Mythara API key (Enterprise/Global tier).
    """
    try:
        config = SalesforceConfig(**salesforce_config.model_dump())
        sf = SalesforceIntegration(config)
        
        if not await sf.authenticate():
            raise HTTPException(status_code=401, detail="Salesforce authentication failed")
        
        record_id = await sf.push_soul_cradle_event(event)
        
        if record_id:
            return {
                "success": True,
                "record_id": record_id,
                "event_type": "soul_cradle",
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to create Salesforce record")
    
    except Exception as e:
        logger.error(f"Failed to push Soul Cradle event to Salesforce: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===================== SYSTEMS FRAMEWORK ENDPOINTS =====================

@app.post("/v1/soul-cradle/paradox/create")
async def create_soul_cradle_paradox(
    paradox: SoulCradleParadox,
    api_key: str = Depends(verify_api_key)
):
    """
    Create a Soul Cradle paradox using systems mathematics framework.
    Requires valid Mythara API key (all tiers).
    
    Returns paradox with integrity hash and terminal risk assessment.
    """
    try:
        # Compute integrity hash
        integrity_hash = paradox.compute_integrity_hash()
        
        # Log creation
        log_paradox_creation(paradox)
        
        # Return with integrity hash
        return {
            "success": True,
            "paradox_id": paradox.paradox_id,
            "system_type": paradox.system_type.value,
            "viability_score": paradox.viability_score,
            "terminal_risk": paradox.terminal_risk.value,
            "integrity_hash": integrity_hash,
            "timestamp": paradox.timestamp.isoformat(),
            "principal_system": {
                "notation": paradox.principal_system.notation,
                "viability_score": paradox.principal_system.viability_score,
                "description": paradox.principal_system.description
            }
        }
    
    except Exception as e:
        logger.error(f"Failed to create Soul Cradle paradox: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/soul-cradle/terminal-risk/calculate")
async def calculate_terminal_risk(
    request: Dict[str, Any],
    api_key: str = Depends(verify_api_key)
):
    """
    Calculate terminal risk (burnout prediction) from paradox history.
    
    Body:
    {
        "paradoxes": [...],  # List of SoulCradleParadox objects
        "time_window_days": 90,  # Optional, default 90
        "viability_threshold": 0.3  # Optional, default 0.3
    }
    
    Returns risk score, level, and recommendations.
    """
    try:
        # Parse paradoxes
        paradox_data = request.get("paradoxes", [])
        paradoxes = [SoulCradleParadox(**p) for p in paradox_data]
        
        time_window = request.get("time_window_days", 90)
        threshold = request.get("viability_threshold", 0.3)
        
        # Calculate risk
        risk_result = TerminalRiskCalculator.calculate_terminal_risk(
            paradox_events=paradoxes,
            time_window_days=time_window,
            viability_threshold=threshold
        )
        
        # Add integrity hash
        risk_data = json.dumps(risk_result, sort_keys=True)
        integrity_hash = hashlib.sha256(risk_data.encode()).hexdigest()
        
        return {
            "success": True,
            **risk_result,
            "integrity_hash": integrity_hash,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Failed to calculate terminal risk: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/soul-cradle/query")
async def query_paradoxes_system_notation(
    notation: str,
    api_key: str = Depends(verify_api_key)
):
    """
    Query Soul Cradle paradoxes using system expression notation.
    
    Examples:
    - Every(Policy)Any(+)Some(Discharge)Non(Safety)
    - Every(*)Any(+)Some(*)Non(Safety)  # All paradoxes where safety is not expressed
    
    Note: This is a demo endpoint. Production systems should query a database.
    """
    try:
        # In production, query database here
        # For demo, return example matches
        
        logger.info(f"System expression query: {notation}")
        
        return {
            "success": True,
            "query": notation,
            "message": "Production implementation requires database integration. This endpoint demonstrates system expression query language parsing.",
            "example_matches": [
                {
                    "paradox_id": "SC_2025_1118_HOSPITAL_001",
                    "matched_expression": "Every(Policy)Any(+)Some(Discharge)Non(Safety)",
                    "terminal_risk": "HIGH"
                }
            ],
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Failed to query paradoxes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/soul-cradle/manifest/systems")
async def get_systems_framework_manifest(
    api_key: str = Depends(verify_api_key)
):
    """
    Get systems framework manifest with integrity hash.
    Returns framework version, notation spec, and documentation links.
    """
    try:
        manifest = {
            "framework": "Soul Cradle Systems Mathematics",
            "version": "1.0.0",
            "notation_spec": "Every(X)Any(+)Some(Y)Non(Z)",
            "system_types": [
                {
                    "type": "Pseudo_Partial",
                    "description": "Incomplete expressions leading to terminal events (burnout)",
                    "viability_range": "0.0-0.3"
                },
                {
                    "type": "Principal_Complete",
                    "description": "Full express-ability with viable outcomes",
                    "viability_range": "0.8-1.0"
                }
            ],
            "terminal_risk_levels": ["LOW", "MODERATE", "HIGH", "CRITICAL"],
            "terminal_risk_formula": "(pseudo_system_density × non_expression_accumulation) / time_window_days",
            "documentation": "See soul_cradle_systems_framework.py for complete implementation"
        }
        
        # Compute integrity hash
        manifest_data = json.dumps(manifest, sort_keys=True)
        integrity_hash = hashlib.sha256(manifest_data.encode()).hexdigest()
        
        return {
            "success": True,
            "manifest": manifest,
            "integrity_hash": integrity_hash,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Failed to get systems manifest: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Mythara Engine API - Shutting down")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")