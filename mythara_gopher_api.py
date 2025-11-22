#!/usr/bin/env python3
"""
Mythara Gopher API - Employment Law Crisis Assistant
Built using QuickFix Bot methodology: intelligent, resourceful, gets it done.

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

Mythara Gopher connects workers facing legal crises with attorneys using:
- Soul Cradle: Emotional intelligence paradox detection
- Blessings Reservoir: Ethical credit system rewarding good faith users
- Messenger Protocol: SHA-256 integrity-verified attorney matching
"""

import os
import sys
import hashlib
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import uvicorn
import psycopg2
from psycopg2.extras import RealDictCursor, Json
from psycopg2.pool import SimpleConnectionPool

# Import Soul Cradle algorithm
from soul_cradle_production import calculate_paradox_severity

logging.basicConfig(level=logging.INFO, format='%(asctime)s - GOPHER - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================================
# POSTGRES CONNECTION
# ============================================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/mythara_gopher"
)

# Connection pool - will be None if Postgres unavailable
db_pool = None
POSTGRES_AVAILABLE = False

try:
    db_pool = SimpleConnectionPool(1, 20, DATABASE_URL)
    POSTGRES_AVAILABLE = True
    logger.info("✅ PostgreSQL connection pool initialized")
except Exception as e:
    logger.warning(f"⚠️ PostgreSQL unavailable, falling back to in-memory mode: {e}")
    # In-memory fallback databases
    MEMORY_USERS = {"gopher_test_key_001": "test_user_1", "gopher_demo_key_002": "demo_user_1"}
    MEMORY_BLESSINGS = {}
    MEMORY_ANALYSES = []
    MEMORY_ATTORNEYS = [
        {"attorney_id": "ATT001", "name": "Frank Azar", "specialization": ["employment_law", "wage_theft"], 
         "location": "Denver, CO", "contact": "frank@thestrongarm.com", 
         "match_keywords": ["wage_theft", "unpaid_overtime", "retaliation"], "active": True},
        {"attorney_id": "ATT002", "name": "Employment Rights Attorney", 
         "specialization": ["harassment", "discrimination"], "location": "Virtual/Nationwide",
         "contact": "intake@employmentrights.com", "match_keywords": ["harassment", "discrimination"], "active": True}
    ]
    MEMORY_AUDIT = []

def get_db_conn():
    """Get database connection from pool (or None if unavailable)"""
    if not POSTGRES_AVAILABLE:
        return None
    return db_pool.getconn()

def release_db_conn(conn):
    """Return connection to pool"""
    if conn and POSTGRES_AVAILABLE:
        db_pool.putconn(conn)

def init_database():
    """Initialize database schema"""
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            # Users table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id VARCHAR(255) PRIMARY KEY,
                    api_key VARCHAR(255) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(50) DEFAULT 'ACTIVE'
                )
            """)
            
            # Blessings Reservoir (credit system)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS blessings_reservoir (
                    user_id VARCHAR(255) PRIMARY KEY REFERENCES users(user_id),
                    credits INTEGER DEFAULT 0,
                    status VARCHAR(50) DEFAULT 'NEUTRAL',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Credit history
            cur.execute("""
                CREATE TABLE IF NOT EXISTS credit_history (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) REFERENCES users(user_id),
                    event VARCHAR(100) NOT NULL,
                    credits_change INTEGER NOT NULL,
                    new_balance INTEGER NOT NULL,
                    reason TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Soul Cradle analyses
            cur.execute("""
                CREATE TABLE IF NOT EXISTS soul_cradle_analyses (
                    id SERIAL PRIMARY KEY,
                    request_id VARCHAR(255) UNIQUE NOT NULL,
                    user_id VARCHAR(255) REFERENCES users(user_id),
                    input_text TEXT NOT NULL,
                    paradox_severity REAL NOT NULL,
                    severity_classification VARCHAR(50) NOT NULL,
                    distress_score REAL NOT NULL,
                    coercion_score REAL NOT NULL,
                    contradiction_score REAL NOT NULL,
                    detected_patterns JSONB,
                    integrity_hash VARCHAR(64) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Attorney database
            cur.execute("""
                CREATE TABLE IF NOT EXISTS attorneys (
                    attorney_id VARCHAR(50) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    specialization TEXT[] NOT NULL,
                    location VARCHAR(255),
                    contact VARCHAR(255),
                    match_keywords TEXT[],
                    active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Attorney matches/referrals
            cur.execute("""
                CREATE TABLE IF NOT EXISTS attorney_referrals (
                    id SERIAL PRIMARY KEY,
                    request_id VARCHAR(255) REFERENCES soul_cradle_analyses(request_id),
                    user_id VARCHAR(255) REFERENCES users(user_id),
                    attorney_id VARCHAR(50) REFERENCES attorneys(attorney_id),
                    match_score REAL NOT NULL,
                    why_matched TEXT,
                    contacted BOOLEAN DEFAULT FALSE,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Messenger Protocol audit trail
            cur.execute("""
                CREATE TABLE IF NOT EXISTS audit_trail (
                    id SERIAL PRIMARY KEY,
                    event_type VARCHAR(100) NOT NULL,
                    user_id VARCHAR(255) REFERENCES users(user_id),
                    request_id VARCHAR(255),
                    data JSONB,
                    integrity_hash VARCHAR(64) NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for performance
            cur.execute("CREATE INDEX IF NOT EXISTS idx_analyses_user ON soul_cradle_analyses(user_id)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_analyses_severity ON soul_cradle_analyses(paradox_severity)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_trail(user_id)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_trail(timestamp)")
            
            conn.commit()
            logger.info("✅ Database schema initialized")
            
            # Insert demo attorneys if table is empty
            cur.execute("SELECT COUNT(*) FROM attorneys")
            if cur.fetchone()[0] == 0:
                demo_attorneys = [
                    ("ATT001", "Frank Azar", ["employment_law", "wage_theft", "discrimination"], 
                     "Denver, CO", "frank@thestrongarm.com", ["wage_theft", "unpaid_overtime", "retaliation"]),
                    ("ATT002", "Employment Rights Attorney", ["harassment", "discrimination", "hostile_work_environment"],
                     "Virtual/Nationwide", "intake@employmentrights.com", ["harassment", "discrimination", "hostile"]),
                    ("ATT003", "Whistleblower Protection Attorney", ["whistleblower", "retaliation", "qui_tam"],
                     "Virtual/Nationwide", "protect@whistleblowerlegal.com", ["whistleblower", "reporting", "illegal"])
                ]
                for att in demo_attorneys:
                    cur.execute("""
                        INSERT INTO attorneys (attorney_id, name, specialization, location, contact, match_keywords)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (attorney_id) DO NOTHING
                    """, att)
                conn.commit()
                logger.info(f"✅ Inserted {len(demo_attorneys)} demo attorneys")
                
            # Insert demo API keys if table is empty
            cur.execute("SELECT COUNT(*) FROM users")
            if cur.fetchone()[0] == 0:
                demo_users = [
                    ("test_user_1", "gopher_test_key_001"),
                    ("demo_user_1", "gopher_demo_key_002")
                ]
                for user_id, api_key in demo_users:
                    cur.execute("""
                        INSERT INTO users (user_id, api_key)
                        VALUES (%s, %s)
                        ON CONFLICT (user_id) DO NOTHING
                    """, (user_id, api_key))
                    cur.execute("""
                        INSERT INTO blessings_reservoir (user_id, credits, status)
                        VALUES (%s, 0, 'NEUTRAL')
                        ON CONFLICT (user_id) DO NOTHING
                    """, (user_id,))
                conn.commit()
                logger.info(f"✅ Inserted {len(demo_users)} demo users")
    finally:
        release_db_conn(conn)

# ============================================================================
# DATA MODELS
# ============================================================================

class UserInput(BaseModel):
    """User's legal situation submitted for analysis"""
    text: str = Field(..., min_length=10, max_length=10000, description="Description of legal situation")
    category: Optional[str] = Field(None, description="Employment, wage theft, discrimination, retaliation, etc.")
    urgency: Optional[str] = Field("normal", description="normal, urgent, emergency")
    
    @validator('text')
    def sanitize_text(cls, v):
        # Basic sanitization
        return v.strip()


class SoulCradleAnalysis(BaseModel):
    """Soul Cradle emotional intelligence analysis results"""
    paradox_severity: float = Field(..., ge=0.0, le=1.0, description="0.0=minimal, 1.0=critical")
    severity_classification: str = Field(..., description="MINIMAL, LOW, MEDIUM, HIGH, CRITICAL")
    distress_score: float = Field(..., ge=0.0, le=1.0)
    coercion_score: float = Field(..., ge=0.0, le=1.0)
    contradiction_score: float = Field(..., ge=0.0, le=1.0)
    detected_patterns: Dict[str, List[str]] = Field(default_factory=dict)
    integrity_hash: str = Field(..., description="SHA-256 tamper-evident timestamp")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class AttorneyMatch(BaseModel):
    """Attorney referral recommendation"""
    attorney_id: str
    name: str
    specialization: List[str]
    match_score: float = Field(..., ge=0.0, le=1.0, description="Compatibility with user's emotional/legal context")
    location: str
    contact: str
    why_matched: str = Field(..., description="Explanation of why this attorney fits the case")


class BlessingsReservoirStatus(BaseModel):
    """User's ethical credit balance"""
    user_id: str
    credits: int = Field(..., description="Positive = good faith user, negative = bad faith")
    credit_history: List[Dict[str, Any]] = Field(default_factory=list)
    status: str = Field(..., description="EXCELLENT, GOOD, NEUTRAL, WARNING, BLOCKED")


class GopherResponse(BaseModel):
    """Complete Gopher analysis and referral"""
    request_id: str
    soul_cradle: SoulCradleAnalysis
    blessings_reservoir: BlessingsReservoirStatus
    attorney_recommendations: List[AttorneyMatch]
    emergency_resources: Optional[List[str]] = None
    next_steps: List[str]
    legal_notice_acknowledged: bool


# ============================================================================
# DATABASE HELPER FUNCTIONS
# ============================================================================

def get_user_by_api_key(api_key: str) -> Optional[str]:
    """Look up user_id by API key"""
    if not POSTGRES_AVAILABLE:
        return MEMORY_USERS.get(api_key)
    
    conn = get_db_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT user_id FROM users WHERE api_key = %s AND status = 'ACTIVE'", (api_key,))
            result = cur.fetchone()
            return result['user_id'] if result else None
    finally:
        release_db_conn(conn)

# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="Mythara Gopher API",
    description="Employment Law Crisis Assistant with Soul Cradle Emotional Intelligence",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS for web app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# AUTHENTICATION (QuickFix: Simple API key for MVP)
# ============================================================================

def verify_api_key(x_api_key: str = Header(...)) -> str:
    """Verify API key and return user_id"""
    user_id = get_user_by_api_key(x_api_key)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Update last_active timestamp (only if Postgres available)
    if POSTGRES_AVAILABLE:
        conn = get_db_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE user_id = %s", (user_id,))
                conn.commit()
        finally:
            release_db_conn(conn)
    
    return user_id


# ============================================================================
# BLESSINGS RESERVOIR LOGIC
# ============================================================================

def get_blessings_status(user_id: str) -> BlessingsReservoirStatus:
    """Get Blessings Reservoir status (from database or memory)"""
    if not POSTGRES_AVAILABLE:
        if user_id not in MEMORY_BLESSINGS:
            MEMORY_BLESSINGS[user_id] = {
                "credits": 0,
                "status": "NEUTRAL",
                "history": []
            }
        data = MEMORY_BLESSINGS[user_id]
        return BlessingsReservoirStatus(
            user_id=user_id,
            credits=data["credits"],
            status=data["status"],
            credit_history=data["history"]
        )
    
    conn = get_db_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Get current status
            cur.execute("""
                SELECT user_id, credits, status
                FROM blessings_reservoir
                WHERE user_id = %s
            """, (user_id,))
            result = cur.fetchone()
            
            if not result:
                # Create new entry
                cur.execute("""
                    INSERT INTO blessings_reservoir (user_id, credits, status)
                    VALUES (%s, 0, 'NEUTRAL')
                    RETURNING user_id, credits, status
                """, (user_id,))
                conn.commit()
                result = cur.fetchone()
            
            # Get credit history
            cur.execute("""
                SELECT event, credits_change, new_balance, reason, timestamp
                FROM credit_history
                WHERE user_id = %s
                ORDER BY timestamp DESC
                LIMIT 50
            """, (user_id,))
            history = cur.fetchall()
            
            return BlessingsReservoirStatus(
                user_id=result['user_id'],
                credits=result['credits'],
                status=result['status'],
                credit_history=[dict(h) for h in history]
            )
    finally:
        release_db_conn(conn)


def award_credits(user_id: str, credits: int, reason: str):
    """Award ethical clarity credits (database or memory)"""
    if not POSTGRES_AVAILABLE:
        if user_id not in MEMORY_BLESSINGS:
            MEMORY_BLESSINGS[user_id] = {"credits": 0, "status": "NEUTRAL", "history": []}
        
        MEMORY_BLESSINGS[user_id]["credits"] += credits
        new_balance = MEMORY_BLESSINGS[user_id]["credits"]
        
        # Calculate status
        if new_balance >= 10:
            new_status = "EXCELLENT"
        elif new_balance >= 5:
            new_status = "GOOD"
        elif new_balance >= -5:
            new_status = "NEUTRAL"
        elif new_balance >= -10:
            new_status = "WARNING"
        else:
            new_status = "BLOCKED"
        
        MEMORY_BLESSINGS[user_id]["status"] = new_status
        MEMORY_BLESSINGS[user_id]["history"].insert(0, {
            "event": "credit_awarded" if credits > 0 else "credit_deducted",
            "credits_change": credits,
            "new_balance": new_balance,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        })
        logger.info(f"💎 User {user_id}: {credits:+d} credits ({reason}) → Balance: {new_balance}")
        return
    
    conn = get_db_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Update credits atomically
            cur.execute("""
                UPDATE blessings_reservoir
                SET credits = credits + %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s
                RETURNING credits
            """, (credits, user_id))
            result = cur.fetchone()
            new_balance = result['credits']
            
            # Calculate new status
            if new_balance >= 10:
                new_status = "EXCELLENT"
            elif new_balance >= 5:
                new_status = "GOOD"
            elif new_balance >= -5:
                new_status = "NEUTRAL"
            elif new_balance >= -10:
                new_status = "WARNING"
            else:
                new_status = "BLOCKED"
            
            # Update status
            cur.execute("""
                UPDATE blessings_reservoir
                SET status = %s
                WHERE user_id = %s
            """, (new_status, user_id))
            
            # Log to credit history
            cur.execute("""
                INSERT INTO credit_history (user_id, event, credits_change, new_balance, reason)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                user_id,
                "credit_awarded" if credits > 0 else "credit_deducted",
                credits,
                new_balance,
                reason
            ))
            
            conn.commit()
            logger.info(f"💎 User {user_id}: {credits:+d} credits ({reason}) → Balance: {new_balance}")
    finally:
        release_db_conn(conn)


# ============================================================================
# ATTORNEY MATCHING LOGIC
# ============================================================================

def match_attorneys(text: str, soul_cradle: SoulCradleAnalysis, top_n: int = 3) -> List[AttorneyMatch]:
    """Match user with attorneys (database or memory)"""
    if not POSTGRES_AVAILABLE:
        attorneys = MEMORY_ATTORNEYS
    else:
        conn = get_db_conn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM attorneys WHERE active = TRUE")
                attorneys = cur.fetchall()
        finally:
            release_db_conn(conn)
    
    matches = []
    text_lower = text.lower()
    
    for attorney in attorneys:
        # Calculate match score
        keyword_matches = sum(1 for kw in attorney["match_keywords"] if kw in text_lower)
        match_score = min(1.0, (keyword_matches / max(len(attorney["match_keywords"]), 1)) + 
                          (soul_cradle.paradox_severity * 0.3))  # Higher severity = prioritize specialists
        
        if match_score > 0.1:  # Minimum threshold
            matches.append(AttorneyMatch(
                attorney_id=attorney["attorney_id"],
                name=attorney["name"],
                specialization=attorney["specialization"],
                match_score=match_score,
                location=attorney["location"],
                contact=attorney["contact"],
                why_matched=f"Specializes in {', '.join(attorney['specialization'][:2])}. "
                           f"Detected {len(soul_cradle.detected_patterns.get('coercion', []))} coercion patterns, "
                           f"{len(soul_cradle.detected_patterns.get('contradiction', []))} legal contradictions."
            ))
    
    # Sort by match score, return top N
    matches.sort(key=lambda x: x.match_score, reverse=True)
    return matches[:top_n]


# ============================================================================
# MESSENGER PROTOCOL (Integrity Verification)
# ============================================================================

def create_integrity_hash(data: dict) -> str:
    """Generate SHA-256 integrity hash for audit trail"""
    # Sort keys for consistency
    canonical = json.dumps(data, sort_keys=True).encode('utf-8')
    return hashlib.sha256(canonical).hexdigest()


def log_audit_trail(event_type: str, user_id: str, data: dict):
    """Log event to tamper-evident audit trail (database or memory)"""
    integrity_hash = create_integrity_hash({"event": event_type, "user": user_id, "data": data})
    
    if not POSTGRES_AVAILABLE:
        MEMORY_AUDIT.append({
            "event_type": event_type,
            "user_id": user_id,
            "request_id": data.get("request_id"),
            "data": data,
            "integrity_hash": integrity_hash,
            "timestamp": datetime.utcnow().isoformat()
        })
        logger.info(f"📝 Audit: {event_type} for {user_id} [{integrity_hash[:16]}...]")
        return
    
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO audit_trail (event_type, user_id, request_id, data, integrity_hash)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                event_type,
                user_id,
                data.get("request_id"),
                Json(data),
                integrity_hash
            ))
            conn.commit()
            logger.info(f"📝 Audit: {event_type} for {user_id} [{integrity_hash[:16]}...]")
    finally:
        release_db_conn(conn)


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    """Health check"""
    return {
        "service": "Mythara Gopher API",
        "status": "operational",
        "version": "1.0.0",
        "subsystems": {
            "soul_cradle": "online",
            "blessings_reservoir": "online",
            "messenger_protocol": "online"
        }
    }


@app.post("/v1/analyze", response_model=GopherResponse)
def analyze_situation(
    user_input: UserInput,
    legal_notice_acknowledged: bool = False,
    user_id: str = Depends(verify_api_key)
):
    """
    Analyze user's legal situation using Soul Cradle and match with attorneys
    
    **Requires:** 
    - Valid API key in X-API-Key header
    - User must acknowledge legal notice (monitoring, no attorney-client privilege yet)
    """
    
    # Check legal notice acknowledgment
    if not legal_notice_acknowledged:
        raise HTTPException(
            status_code=428,  # Precondition Required
            detail="You must acknowledge the Mythara Gopher Legal Notice before using this service. "
                   "All communications are monitored. No attorney-client privilege exists until formal retention."
        )
    
    # Award credit for acknowledging legal notice (+1 ethical clarity)
    award_credits(user_id, 1, "Acknowledged legal notice and monitoring disclosure")
    
    # Generate request ID
    request_id = hashlib.sha256(
        f"{user_id}:{user_input.text}:{datetime.utcnow().isoformat()}".encode()
    ).hexdigest()[:16]
    
    logger.info(f"🔍 Analyzing request {request_id} for user {user_id}")
    
    # Run Soul Cradle analysis
    result = calculate_paradox_severity(user_input.text)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    severity = result["paradox_severity"]
    classification = result["classification"]
    distress = result["analysis"]["distress_score"]
    coercion = result["analysis"]["coercion_score"]
    contradiction = result["analysis"]["contradiction_score"]
    
    # Extract detected patterns
    detected_patterns_dict = {
        "distress": [f"distress_keyword_count: {result['analysis']['distress_keywords_found']}"],
        "coercion": result["analysis"]["coercion_patterns"],
        "contradiction": result["analysis"]["contradiction_patterns"]
    }
    
    # Create integrity hash
    analysis_data = {
        "text": user_input.text,
        "severity": severity,
        "timestamp": datetime.utcnow().isoformat()
    }
    integrity_hash = create_integrity_hash(analysis_data)
    
    # Save analysis to database (if available)
    if POSTGRES_AVAILABLE:
        conn = get_db_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO soul_cradle_analyses 
                    (request_id, user_id, input_text, paradox_severity, severity_classification,
                     distress_score, coercion_score, contradiction_score, detected_patterns, integrity_hash)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    request_id, user_id, user_input.text, severity, classification,
                    distress, coercion, contradiction, Json(detected_patterns_dict), integrity_hash
                ))
                conn.commit()
        finally:
            release_db_conn(conn)
    else:
        MEMORY_ANALYSES.append({
            "request_id": request_id,
            "user_id": user_id,
            "severity": severity,
            "classification": classification
        })
    
    soul_cradle_result = SoulCradleAnalysis(
        paradox_severity=severity,
        severity_classification=classification,
        distress_score=distress,
        coercion_score=coercion,
        contradiction_score=contradiction,
        detected_patterns=detected_patterns_dict,
        integrity_hash=integrity_hash
    )
    
    # Award credits based on severity (seeking help for genuine issues = ethical)
    if severity >= 0.3:
        award_credits(user_id, 2, f"Seeking help for {classification} severity situation")
    
    # Get Blessings Reservoir status
    blessings_status = get_blessings_status(user_id)
    
    # Check if user is blocked
    if blessings_status.status == "BLOCKED":
        raise HTTPException(
            status_code=403,
            detail="Account temporarily suspended due to platform abuse. Contact support."
        )
    
    # Match with attorneys
    attorney_matches = match_attorneys(user_input.text, soul_cradle_result)
    
    # Save attorney referrals to database (if available)
    if POSTGRES_AVAILABLE:
        conn = get_db_conn()
        try:
            with conn.cursor() as cur:
                for match in attorney_matches:
                    cur.execute("""
                        INSERT INTO attorney_referrals 
                        (request_id, user_id, attorney_id, match_score, why_matched)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (request_id, user_id, match.attorney_id, match.match_score, match.why_matched))
                conn.commit()
        finally:
            release_db_conn(conn)
    
    # Emergency resources for critical situations
    emergency_resources = None
    if severity >= 0.7:
        emergency_resources = [
            "National Suicide Prevention Lifeline: 988",
            "National Domestic Violence Hotline: 1-800-799-7233",
            "OSHA Whistleblower Hotline: 1-800-321-6742",
            "Immediate risk? Call 911 or go to nearest emergency room"
        ]
    
    # Next steps guidance
    next_steps = [
        f"Your situation has been classified as {classification} severity ({severity:.3f})",
        f"We've matched you with {len(attorney_matches)} attorneys who specialize in your type of case",
        "Review attorney profiles and contact the one that feels right for you",
        "Once you formally retain an attorney, attorney-client privilege will protect your communications"
    ]
    
    if severity >= 0.5:
        next_steps.insert(1, "⚠️ HIGH PRIORITY: Contact an attorney within 48 hours")
    
    # Log to audit trail
    log_audit_trail("situation_analyzed", user_id, {
        "request_id": request_id,
        "severity": severity,
        "classification": classification,
        "attorneys_matched": len(attorney_matches)
    })
    
    return GopherResponse(
        request_id=request_id,
        soul_cradle=soul_cradle_result,
        blessings_reservoir=blessings_status,
        attorney_recommendations=attorney_matches,
        emergency_resources=emergency_resources,
        next_steps=next_steps,
        legal_notice_acknowledged=legal_notice_acknowledged
    )


@app.get("/v1/blessings", response_model=BlessingsReservoirStatus)
def get_user_credits(user_id: str = Depends(verify_api_key)):
    """Get user's Blessings Reservoir credit status"""
    return get_blessings_status(user_id)


@app.get("/v1/attorneys")
def list_attorneys(
    specialization: Optional[str] = None,
    location: Optional[str] = None,
    user_id: str = Depends(verify_api_key)
):
    """List available attorneys from database (optional filters)"""
    conn = get_db_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = "SELECT * FROM attorneys WHERE active = TRUE"
            params = []
            
            if specialization:
                query += " AND %s = ANY(specialization)"
                params.append(specialization.lower())
            
            if location:
                query += " AND location ILIKE %s"
                params.append(f"%{location}%")
            
            cur.execute(query, params)
            attorneys = [dict(row) for row in cur.fetchall()]
            
            return {"attorneys": attorneys, "count": len(attorneys)}
    finally:
        release_db_conn(conn)


@app.get("/v1/audit/{request_id}")
def get_audit_trail(request_id: str, user_id: str = Depends(verify_api_key)):
    """Retrieve audit trail for specific request from database (user can only see their own)"""
    conn = get_db_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT event_type, user_id, request_id, data, integrity_hash, timestamp
                FROM audit_trail
                WHERE user_id = %s AND request_id = %s
                ORDER BY timestamp DESC
            """, (user_id, request_id))
            
            entries = [dict(row) for row in cur.fetchall()]
            
            if not entries:
                raise HTTPException(status_code=404, detail="Audit trail not found")
            
            return {"audit_trail": entries, "count": len(entries)}
    finally:
        release_db_conn(conn)


@app.get("/health")
def health_check():
    """Detailed health check (database or memory mode)"""
    if not POSTGRES_AVAILABLE:
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "in-memory (PostgreSQL unavailable)",
            "subsystems": {
                "soul_cradle": "operational",
                "blessings_reservoir": f"{len(MEMORY_BLESSINGS)} users tracked",
                "attorney_database": f"{len(MEMORY_ATTORNEYS)} attorneys available",
                "audit_trail": f"{len(MEMORY_AUDIT)} events logged",
                "analyses_completed": f"{len(MEMORY_ANALYSES)} total"
            }
        }
    
    conn = get_db_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Get counts
            cur.execute("SELECT COUNT(*) as count FROM users WHERE status = 'ACTIVE'")
            user_count = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM attorneys WHERE active = TRUE")
            attorney_count = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM audit_trail")
            audit_count = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM soul_cradle_analyses")
            analysis_count = cur.fetchone()['count']
            
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "database": "PostgreSQL connected",
                "subsystems": {
                    "soul_cradle": "operational",
                    "blessings_reservoir": f"{user_count} users tracked",
                    "attorney_database": f"{attorney_count} attorneys available",
                    "audit_trail": f"{audit_count} events logged",
                    "analyses_completed": f"{analysis_count} total"
                }
            }
    except Exception as e:
        return {
            "status": "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "database": f"error: {str(e)}",
            "subsystems": {
                "soul_cradle": "operational (algorithm only)",
                "blessings_reservoir": "offline",
                "attorney_database": "offline",
                "audit_trail": "offline"
            }
        }
    finally:
        release_db_conn(conn)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════╗
║           🦎 MYTHARA GOPHER API SERVER 🦎                 ║
║      Employment Law Crisis Assistant with Soul AI         ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Initialize database schema (if Postgres available)
    if POSTGRES_AVAILABLE:
        print("Initializing PostgreSQL database...")
        init_database()
    
    db_status = "PostgreSQL connected" if POSTGRES_AVAILABLE else "In-Memory Mode (Install PostgreSQL for persistence)"
    
    print(f"""
✅ Server ready!

Starting on http://0.0.0.0:8000

📖 API Docs: http://localhost:8000/api/docs
🏥 Health: http://localhost:8000/health
🗄️  Database: {db_status}

Test with:
  curl -X POST http://localhost:8000/v1/analyze \\
    -H "X-API-Key: gopher_test_key_001" \\
    -H "Content-Type: application/json" \\
    -d '{{"text": "My boss says I have to work unpaid overtime...", "legal_notice_acknowledged": true}}'
    """)
    
    uvicorn.run(
        "mythara_gopher_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
