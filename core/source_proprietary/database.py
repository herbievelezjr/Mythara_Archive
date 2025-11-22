#!/usr/bin/env python3
"""
Mythara Engine - Database Layer
PostgreSQL persistence for pilots, usage tracking, and domain registry.

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.
"""

from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import Optional, Dict, Any, List
import os
import logging

logger = logging.getLogger(__name__)

# Database URL from environment (Railway provides DATABASE_URL automatically)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mythara_pilots.db")

# Fix for Railway's postgres:// URLs (SQLAlchemy needs postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before using
    pool_timeout=30,  # Timeout waiting for connection from pool (seconds)
    pool_recycle=3600,  # Recycle connections after 1 hour to prevent stale connections
    echo=False  # Set to True for SQL debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Pilot(Base):
    """
    Pilot tier customer - tracks API key, domain, and pilot start date.
    One pilot per business domain enforced by unique domain constraint.
    """
    __tablename__ = "pilots"

    api_key = Column(String, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    domain = Column(String, unique=True, nullable=False, index=True)  # Unique domain constraint
    company_name = Column(String, nullable=False)
    employee_count = Column(Integer, nullable=False)
    pilot_start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    stripe_payment_id = Column(String, nullable=True)  # Track payment source
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Self-regulation fields
    strike_count = Column(Integer, default=0)
    suspended_until = Column(DateTime, nullable=True)
    termination_reason = Column(String, nullable=True)


class UsageTracking(Base):
    """
    API call usage tracking per pilot - enforces 7-day total limits.
    Separate table allows efficient queries without loading full pilot data.
    """
    __tablename__ = "usage_tracking"

    api_key = Column(String, primary_key=True, index=True)
    call_count = Column(Integer, default=0, nullable=False)
    total_limit = Column(Integer, nullable=False)
    last_call = Column(DateTime, nullable=True)
    
    # Abuse detection metrics
    first_call_date = Column(DateTime, nullable=True)
    velocity_abuse_detected = Column(Boolean, default=False)
    usage_mismatch_detected = Column(Boolean, default=False)
    
    # Alert tracking
    sent_80_percent_alert = Column(Boolean, default=False)
    sent_24hr_expiration_alert = Column(Boolean, default=False)


class AuditLog(Base):
    """
    Immutable audit log for compliance and forensics.
    Tracks all critical actions: pilot creation, API calls, strikes, terminations.
    """
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    api_key = Column(String, index=True, nullable=True)
    action = Column(String, nullable=False)  # e.g., "pilot_created", "api_call", "strike_issued"
    details = Column(JSON, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)


class EmailQueue(Base):
    """
    Outbound email queue for async delivery.
    Ensures emails are sent even if SendGrid is temporarily down.
    """
    __tablename__ = "email_queue"

    id = Column(Integer, primary_key=True, autoincrement=True)
    to_email = Column(String, nullable=False, index=True)
    subject = Column(String, nullable=False)
    body_html = Column(String, nullable=False)
    body_text = Column(String, nullable=False)
    template_type = Column(String, nullable=False)  # e.g., "api_key_delivery", "80_percent_alert"
    api_key = Column(String, nullable=True, index=True)
    
    # Delivery tracking
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    sent_at = Column(DateTime, nullable=True)
    failed_at = Column(DateTime, nullable=True)
    retry_count = Column(Integer, default=0)
    error_message = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, sent, failed


# Database helper functions
def get_db() -> Session:
    """
    Dependency for FastAPI endpoints to get database session.
    Ensures proper connection cleanup after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database schema - creates all tables if they don't exist.
    Call this on application startup.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


def get_pilot(db: Session, api_key: str) -> Optional[Pilot]:
    """Get pilot by API key."""
    return db.query(Pilot).filter(Pilot.api_key == api_key).first()


def get_pilot_by_domain(db: Session, domain: str) -> Optional[Pilot]:
    """Get pilot by business domain - enforces one pilot per domain."""
    return db.query(Pilot).filter(Pilot.domain == domain).first()


def create_pilot(
    db: Session,
    api_key: str,
    email: str,
    domain: str,
    company_name: str,
    employee_count: int,
    pilot_start_date: datetime,
    stripe_payment_id: Optional[str] = None
) -> Pilot:
    """
    Create new pilot account.
    Raises exception if domain already exists (one pilot per domain).
    """
    pilot = Pilot(
        api_key=api_key,
        email=email,
        domain=domain,
        company_name=company_name,
        employee_count=employee_count,
        pilot_start_date=pilot_start_date,
        stripe_payment_id=stripe_payment_id,
        is_active=True
    )
    db.add(pilot)
    db.commit()
    db.refresh(pilot)
    
    # Initialize usage tracking
    usage = UsageTracking(
        api_key=api_key,
        call_count=0,
        total_limit=get_api_rate_limit_for_employee_count(employee_count)
    )
    db.add(usage)
    db.commit()
    
    # Audit log
    audit = AuditLog(
        api_key=api_key,
        action="pilot_created",
        details={
            "domain": domain,
            "employee_count": employee_count,
            "stripe_payment_id": stripe_payment_id
        }
    )
    db.add(audit)
    db.commit()
    
    logger.info(f"Pilot created: {domain} ({api_key[:8]}...)")
    return pilot


def get_usage_tracking(db: Session, api_key: str) -> Optional[UsageTracking]:
    """Get usage tracking for API key."""
    return db.query(UsageTracking).filter(UsageTracking.api_key == api_key).first()


def increment_usage(db: Session, api_key: str) -> UsageTracking:
    """
    Increment call count for API key.
    Creates usage record if it doesn't exist (defensive).
    """
    usage = get_usage_tracking(db, api_key)
    if not usage:
        # Defensive: create usage record if missing
        pilot = get_pilot(db, api_key)
        if pilot:
            usage = UsageTracking(
                api_key=api_key,
                call_count=0,
                total_limit=get_api_rate_limit_for_employee_count(pilot.employee_count)
            )
            db.add(usage)
            db.commit()
            db.refresh(usage)
    
    if usage:
        usage.call_count += 1
        usage.last_call = datetime.utcnow()
        if usage.first_call_date is None:
            usage.first_call_date = datetime.utcnow()
        db.commit()
        db.refresh(usage)
    
    return usage


def issue_strike(db: Session, api_key: str, reason: str) -> Pilot:
    """
    Issue strike to pilot for self-regulation violation.
    Graduated enforcement: 1 = warning, 2 = 7-day suspension, 3 = termination.
    """
    pilot = get_pilot(db, api_key)
    if not pilot:
        raise ValueError(f"Pilot not found: {api_key}")
    
    pilot.strike_count += 1
    
    if pilot.strike_count == 2:
        # Second strike = 7-day suspension
        pilot.suspended_until = datetime.utcnow() + timedelta(days=7)
    elif pilot.strike_count >= 3:
        # Third strike = termination
        pilot.is_active = False
        pilot.termination_reason = reason
    
    db.commit()
    
    # Audit log
    audit = AuditLog(
        api_key=api_key,
        action="strike_issued",
        details={
            "reason": reason,
            "strike_count": pilot.strike_count,
            "suspended_until": pilot.suspended_until.isoformat() if pilot.suspended_until else None,
            "terminated": pilot.strike_count >= 3
        }
    )
    db.add(audit)
    db.commit()
    
    logger.warning(f"Strike issued to {api_key[:8]}...: {reason} (strike {pilot.strike_count})")
    return pilot


def log_audit(
    db: Session,
    action: str,
    api_key: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
):
    """
    Log audit event for compliance tracking.
    Immutable record of all system actions.
    """
    audit = AuditLog(
        api_key=api_key,
        action=action,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.add(audit)
    db.commit()


def queue_email(
    db: Session,
    to_email: str,
    subject: str,
    body_html: str,
    body_text: str,
    template_type: str,
    api_key: Optional[str] = None
) -> EmailQueue:
    """
    Queue email for async delivery.
    Ensures email is sent even if SendGrid is temporarily down.
    """
    email = EmailQueue(
        to_email=to_email,
        subject=subject,
        body_html=body_html,
        body_text=body_text,
        template_type=template_type,
        api_key=api_key,
        status="pending"
    )
    db.add(email)
    db.commit()
    db.refresh(email)
    logger.info(f"Email queued: {template_type} to {to_email}")
    return email


def get_api_rate_limit_for_employee_count(employee_count: int) -> int:
    """
    Return 7-day total API call limit based on employee count.
    Matches API_RATE_LIMITS_BY_EMPLOYEE_COUNT in main.py.
    """
    if employee_count <= 10:
        return 1_000
    elif employee_count <= 50:
        return 5_000
    elif employee_count <= 200:
        return 15_000
    elif employee_count <= 1_000:
        return 30_000
    else:
        return 50_000


# Ensure timedelta is imported for issue_strike function
from datetime import timedelta
