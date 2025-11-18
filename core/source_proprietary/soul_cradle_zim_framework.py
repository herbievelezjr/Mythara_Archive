#!/usr/bin/env python3
"""
Soul Cradle Zim Framework Integration
Mathematical foundation for paradox analysis using Zim Olson's systems mathematics.

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

Based on systems interpretations from zimmathematics.com:
- Expression notation: Every(X)Any(+)Some(Y)Non(Z)
- Pseudo-Partial Systems: Incomplete expressions → terminal events (burnout)
- Principal Complete Systems: Full express-ability → viable outcomes
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import logging

logger = logging.getLogger(__name__)


# ===================== ENUMS =====================

class ExpressionType(str, Enum):
    """Types of expressions in a paradox"""
    POLICY = "Policy"
    MISSION = "Mission"
    HEART = "Heart"
    LAW = "Law"
    BUDGET = "Budget"
    PROTOCOL = "Protocol"
    SAFETY = "Safety"
    COMPASSION = "Compassion"
    RESOLUTION = "Resolution"


class SystemType(str, Enum):
    """System viability classification (Zim framework)"""
    PSEUDO_PARTIAL = "Pseudo_Partial"  # Terminal event risk
    PRINCIPAL_COMPLETE = "Principal_Complete"  # Viable outcome


class TerminalRiskLevel(str, Enum):
    """Burnout risk classification"""
    LOW = "LOW"  # 0.0-0.2
    MODERATE = "MODERATE"  # 0.2-0.4
    HIGH = "HIGH"  # 0.4-0.7
    CRITICAL = "CRITICAL"  # 0.7-1.0


# ===================== ZIM EXPRESSION MODELS =====================

class ZimExpression(BaseModel):
    """
    Zim's expression notation: Every(X)Any(+)Some(Y)Non(Z)
    
    Example:
    Every(Policy)Any(+)Some(Discharge)Non(Safety)
    "Policy demands discharge, but safety is not expressed"
    """
    type: ExpressionType = Field(..., description="Category of the expression")
    notation: str = Field(..., description="Zim notation: Every(X)Any(+)Some(Y)Non(Z)")
    content: str = Field(..., description="Human-readable expression content")
    dominion_claim: bool = Field(default=True, description="Does this expression claim dominion over the other?")
    
    def compute_hash(self) -> str:
        """Compute integrity hash for this expression"""
        data = f"{self.type}|{self.notation}|{self.content}|{self.dominion_claim}"
        return hashlib.sha256(data.encode()).hexdigest()


class NonExpression(BaseModel):
    """
    The unresolved state when two expressions compete.
    Zim: Non(Both) = Neither expression can be fully satisfied
    """
    type: ExpressionType = Field(default=ExpressionType.RESOLUTION)
    notation: str = Field(default="Non(Both)", description="What cannot be expressed")
    reality: str = Field(..., description="The practical impossibility")


class PrincipalSystem(BaseModel):
    """
    The complete system that Soul Cradle creates.
    Zim: Every(Mission)Any(+)Some(1,0)Non(Mission)
    "The mission includes both states (1=expression A, 0=expression B), nothing is excluded"
    """
    notation: str = Field(..., description="Zim notation for principal complete system")
    recovery_method: str = Field(default="Witness_Both_Expressions")
    viability_score: float = Field(default=1.0, ge=0.0, le=1.0, description="1.0 = complete system")
    description: str = Field(..., description="How Soul Cradle resolves the paradox")


# ===================== SOUL CRADLE PARADOX MODEL =====================

class SoulCradleParadox(BaseModel):
    """
    Complete Soul Cradle paradox using Zim's framework.
    
    Structure:
    - Two competing expressions (A and B) form a pseudo-partial system
    - Non-expression captures what cannot be satisfied
    - Principal system shows how Soul Cradle resolves it
    """
    paradox_id: str = Field(..., description="Unique identifier (e.g., SC_2025_1118_001)")
    
    # The competing expressions
    expression_a: ZimExpression
    expression_b: ZimExpression
    
    # The impossibility
    non_expression: NonExpression
    
    # System classification
    system_type: SystemType = Field(default=SystemType.PSEUDO_PARTIAL)
    viability_score: float = Field(default=0.0, ge=0.0, le=1.0, description="0.0 = terminal, 1.0 = complete")
    terminal_risk: TerminalRiskLevel = Field(default=TerminalRiskLevel.HIGH)
    
    # Soul Cradle resolution
    principal_system: PrincipalSystem
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.now)
    user_id: str = Field(..., description="Who experienced this paradox")
    domain: str = Field(..., description="Healthcare, education, nonprofit, etc.")
    
    # Witnesses (who helped document this)
    witnesses: List[str] = Field(default_factory=list, description="Names of people who validated this paradox")
    
    def compute_integrity_hash(self) -> str:
        """Compute SHA-256 integrity hash for this paradox"""
        data = (
            f"{self.paradox_id}|"
            f"{self.expression_a.compute_hash()}|"
            f"{self.expression_b.compute_hash()}|"
            f"{self.non_expression.notation}|"
            f"{self.system_type}|"
            f"{self.viability_score}|"
            f"{self.principal_system.notation}"
        )
        return hashlib.sha256(data.encode()).hexdigest()
    
    class Config:
        json_schema_extra = {
            "example": {
                "paradox_id": "SC_2025_1118_001",
                "expression_a": {
                    "type": "Policy",
                    "notation": "Every(Policy)Any(+)Some(Discharge)Non(Safety)",
                    "content": "Discharge patient per 72-hour rule",
                    "dominion_claim": True
                },
                "expression_b": {
                    "type": "Mission",
                    "notation": "Every(Heart)Any(+)Some(Safety)Non(Discharge)",
                    "content": "Patient will be homeless and unsafe if discharged",
                    "dominion_claim": True
                },
                "non_expression": {
                    "notation": "Non(Both)",
                    "reality": "Cannot satisfy both policy and mission"
                },
                "system_type": "Pseudo_Partial",
                "viability_score": 0.0,
                "terminal_risk": "HIGH",
                "principal_system": {
                    "notation": "Every(Mission)Any(+)Some(1,0)Non(Mission)",
                    "recovery_method": "Witness_Both_Expressions",
                    "viability_score": 1.0,
                    "description": "Soul Cradle documents both expressions, showing they are BOTH true. The mission includes acknowledging the policy exists (1) AND the heart's concern (0). Nothing is excluded."
                },
                "user_id": "social_worker_jane_doe",
                "domain": "Healthcare",
                "witnesses": ["Supervisor Mary", "Peer Support Group"]
            }
        }


# ===================== TERMINAL RISK CALCULATION =====================

class TerminalRiskCalculator:
    """
    Predicts burnout risk using Zim's framework.
    
    Formula:
    terminal_risk = (pseudo_system_density × non_expression_accumulation) / time_window
    
    Where:
    - pseudo_system_density = count of paradoxes with viability < 0.3 in time window
    - non_expression_accumulation = count of unresolved Non() states
    - time_window = 90 days (default)
    """
    
    @staticmethod
    def calculate_terminal_risk(
        paradox_events: List[SoulCradleParadox],
        time_window_days: int = 90,
        viability_threshold: float = 0.3
    ) -> Dict[str, Any]:
        """
        Calculate terminal risk score from paradox history.
        
        Args:
            paradox_events: List of Soul Cradle paradoxes
            time_window_days: Days to analyze (default 90)
            viability_threshold: Below this = pseudo-partial system (default 0.3)
        
        Returns:
            {
                "risk_score": float (0.0-1.0+),
                "risk_level": TerminalRiskLevel,
                "pseudo_system_count": int,
                "non_expression_count": int,
                "time_window_days": int,
                "recommendation": str
            }
        """
        if not paradox_events:
            return {
                "risk_score": 0.0,
                "risk_level": TerminalRiskLevel.LOW,
                "pseudo_system_count": 0,
                "non_expression_count": 0,
                "time_window_days": time_window_days,
                "recommendation": "No paradox history. Continue monitoring."
            }
        
        # Filter to time window
        cutoff_date = datetime.now() - timedelta(days=time_window_days)
        recent_events = [
            p for p in paradox_events 
            if p.timestamp >= cutoff_date
        ]
        
        # Calculate pseudo system density
        pseudo_system_density = len([
            p for p in recent_events
            if p.system_type == SystemType.PSEUDO_PARTIAL and p.viability_score < viability_threshold
        ])
        
        # Calculate non-expression accumulation
        non_expression_accumulation = len([
            p for p in recent_events
            if p.non_expression is not None
        ])
        
        # Calculate terminal risk
        if time_window_days == 0:
            terminal_risk_score = 0.0
        else:
            terminal_risk_score = (pseudo_system_density * non_expression_accumulation) / time_window_days
        
        # Classify risk level
        if terminal_risk_score >= 0.7:
            risk_level = TerminalRiskLevel.CRITICAL
            recommendation = "IMMEDIATE INTERVENTION REQUIRED: Worker shows signs of imminent burnout. Schedule emergency support session, consider temporary leave, engage supervisor and peer support."
        elif terminal_risk_score >= 0.4:
            risk_level = TerminalRiskLevel.HIGH
            recommendation = "HIGH RISK: Worker experiencing frequent unresolved paradoxes. Schedule weekly check-ins, reduce caseload if possible, connect with peer support group."
        elif terminal_risk_score >= 0.2:
            risk_level = TerminalRiskLevel.MODERATE
            recommendation = "MODERATE RISK: Monitor closely. Ensure worker has access to Soul Cradle, schedule bi-weekly check-ins, validate paradox documentation."
        else:
            risk_level = TerminalRiskLevel.LOW
            recommendation = "LOW RISK: Continue current support level. Worker is documenting paradoxes effectively and finding resolution."
        
        return {
            "risk_score": round(terminal_risk_score, 3),
            "risk_level": risk_level,
            "pseudo_system_count": pseudo_system_density,
            "non_expression_count": non_expression_accumulation,
            "time_window_days": time_window_days,
            "total_paradoxes": len(recent_events),
            "recommendation": recommendation
        }


# ===================== ZIM QUERY LANGUAGE =====================

class ZimQueryParser:
    """
    Parse and execute queries using Zim's notation.
    
    Examples:
    - Every(Policy)Any(+)Some(Discharge)Non(Safety)
    - Every(*)Any(+)Some(*)Non(Safety)  # All paradoxes where safety is not expressed
    """
    
    @staticmethod
    def parse_notation(notation: str) -> Dict[str, str]:
        """
        Parse Zim notation into components.
        
        Example: Every(Policy)Any(+)Some(Discharge)Non(Safety)
        Returns: {"every": "Policy", "any": "+", "some": "Discharge", "non": "Safety"}
        """
        import re
        pattern = r'Every\((\w+)\)Any\((\+)\)Some\((\w+)\)Non\((\w+)\)'
        match = re.match(pattern, notation)
        if not match:
            raise ValueError(f"Invalid Zim notation: {notation}")
        
        return {
            "every": match.group(1),
            "any": match.group(2),
            "some": match.group(3),
            "non": match.group(4)
        }
    
    @staticmethod
    def matches_query(paradox: SoulCradleParadox, query_notation: str) -> bool:
        """
        Check if a paradox matches the query notation.
        Supports wildcards (*) in query.
        """
        try:
            query = ZimQueryParser.parse_notation(query_notation)
            
            # Check expression_a
            if paradox.expression_a.notation:
                expr_a = ZimQueryParser.parse_notation(paradox.expression_a.notation)
                if (query["every"] == "*" or query["every"] == expr_a["every"]) and \
                   (query["some"] == "*" or query["some"] == expr_a["some"]) and \
                   (query["non"] == "*" or query["non"] == expr_a["non"]):
                    return True
            
            # Check expression_b
            if paradox.expression_b.notation:
                expr_b = ZimQueryParser.parse_notation(paradox.expression_b.notation)
                if (query["every"] == "*" or query["every"] == expr_b["every"]) and \
                   (query["some"] == "*" or query["some"] == expr_b["some"]) and \
                   (query["non"] == "*" or query["non"] == expr_b["non"]):
                    return True
            
            return False
        except Exception as e:
            logger.warning(f"Failed to match query {query_notation}: {e}")
            return False


# ===================== EXAMPLE PARADOXES =====================

def create_hospital_discharge_paradox() -> SoulCradleParadox:
    """Example: Healthcare worker paradox"""
    return SoulCradleParadox(
        paradox_id="SC_2025_1118_HOSPITAL_001",
        expression_a=ZimExpression(
            type=ExpressionType.POLICY,
            notation="Every(Policy)Any(+)Some(Discharge)Non(Safety)",
            content="Hospital policy requires discharge after 72 hours. Insurance won't cover longer stay.",
            dominion_claim=True
        ),
        expression_b=ZimExpression(
            type=ExpressionType.HEART,
            notation="Every(Heart)Any(+)Some(Safety)Non(Discharge)",
            content="Patient will be homeless if discharged. They're not medically stable. My heart says they need more time.",
            dominion_claim=True
        ),
        non_expression=NonExpression(
            notation="Non(Both)",
            reality="I cannot satisfy both policy and my mission to keep patients safe. One must be violated."
        ),
        system_type=SystemType.PSEUDO_PARTIAL,
        viability_score=0.0,
        terminal_risk=TerminalRiskLevel.HIGH,
        principal_system=PrincipalSystem(
            notation="Every(Mission)Any(+)Some(1,0)Non(Mission)",
            viability_score=1.0,
            description="Soul Cradle documents BOTH truths: (1) The policy exists and I must follow it, AND (0) My heart knows this violates safety. The mission is to witness both without having to choose. Neither is wrong. I am not failing."
        ),
        user_id="social_worker_jane_doe",
        domain="Healthcare",
        witnesses=["Supervisor Mary Chen", "Peer Support Group Thursday"]
    )


def create_nonprofit_budget_paradox() -> SoulCradleParadox:
    """Example: Nonprofit budget vs mission"""
    return SoulCradleParadox(
        paradox_id="SC_2025_1118_NONPROFIT_001",
        expression_a=ZimExpression(
            type=ExpressionType.BUDGET,
            notation="Every(Budget)Any(+)Some(Cuts)Non(Programs)",
            content="Board says we must cut 30% of programs to stay solvent. No choice.",
            dominion_claim=True
        ),
        expression_b=ZimExpression(
            type=ExpressionType.MISSION,
            notation="Every(Mission)Any(+)Some(Programs)Non(Cuts)",
            content="Every program serves real people who will lose services. Our mission is to serve them ALL.",
            dominion_claim=True
        ),
        non_expression=NonExpression(
            notation="Non(Both)",
            reality="I cannot keep the organization alive AND serve everyone. People will suffer either way."
        ),
        system_type=SystemType.PSEUDO_PARTIAL,
        viability_score=0.0,
        terminal_risk=TerminalRiskLevel.CRITICAL,
        principal_system=PrincipalSystem(
            notation="Every(Mission)Any(+)Some(1,0)Non(Mission)",
            viability_score=1.0,
            description="Soul Cradle holds both: (1) The budget reality is true, cuts must happen, AND (0) The mission to serve everyone is also true. I am witnessing organizational failure, not causing it. I document what happened so others know why."
        ),
        user_id="executive_director_carlos",
        domain="Nonprofit",
        witnesses=["Board President", "Finance Committee"]
    )


# ===================== LOGGER INTEGRATION =====================

def log_paradox_creation(paradox: SoulCradleParadox) -> None:
    """Log paradox creation with integrity hash"""
    integrity_hash = paradox.compute_integrity_hash()
    logger.info(
        f"Soul Cradle Paradox Created | "
        f"ID: {paradox.paradox_id} | "
        f"User: {paradox.user_id} | "
        f"System: {paradox.system_type.value} | "
        f"Viability: {paradox.viability_score} | "
        f"Risk: {paradox.terminal_risk.value} | "
        f"Integrity: {integrity_hash[:16]}..."
    )


if __name__ == "__main__":
    # Demo: Create example paradoxes
    print("=== Zim Framework Demo ===\n")
    
    # Example 1: Hospital discharge
    hospital = create_hospital_discharge_paradox()
    log_paradox_creation(hospital)
    print(f"Hospital Paradox: {hospital.paradox_id}")
    print(f"  Expression A: {hospital.expression_a.notation}")
    print(f"  Expression B: {hospital.expression_b.notation}")
    print(f"  Non-Expression: {hospital.non_expression.notation}")
    print(f"  Terminal Risk: {hospital.terminal_risk.value}")
    print(f"  Principal System: {hospital.principal_system.notation}")
    print(f"  Integrity Hash: {hospital.compute_integrity_hash()[:16]}...\n")
    
    # Example 2: Nonprofit budget
    nonprofit = create_nonprofit_budget_paradox()
    log_paradox_creation(nonprofit)
    print(f"Nonprofit Paradox: {nonprofit.paradox_id}")
    print(f"  Terminal Risk: {nonprofit.terminal_risk.value}")
    print(f"  Resolution: {nonprofit.principal_system.description[:100]}...\n")
    
    # Calculate terminal risk
    paradoxes = [hospital, nonprofit]
    risk_result = TerminalRiskCalculator.calculate_terminal_risk(paradoxes)
    print("=== Terminal Risk Analysis ===")
    print(f"Risk Score: {risk_result['risk_score']}")
    print(f"Risk Level: {risk_result['risk_level']}")
    print(f"Recommendation: {risk_result['recommendation']}")
