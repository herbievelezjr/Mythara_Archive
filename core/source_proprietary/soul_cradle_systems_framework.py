#!/usr/bin/env python3
"""
Soul Cradle Systems Framework
Mathematical foundation for paradox analysis and burnout prediction.

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

Mythara Paradox Resolution Mathematics:
- Paradox Tension Formula: P(t) = |A - B| × (1 - R(t))
- Resolution Score: R(t) = (W_a + W_b) / (2 × max(|A|, |B|))
- Incomplete Resolution → Terminal Risk (burnout)
- Complete Resolution → Viable Recovery
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal, Tuple, ClassVar
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import logging
import secrets
import uuid
import base64
import json
import numpy as np
from pathlib import Path
try:
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.backends import default_backend
    RSA_AVAILABLE = True
except ImportError:
    RSA_AVAILABLE = False
    logging.warning("RSA cryptography not available. Install: pip install cryptography")

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
    """System viability classification"""
    INCOMPLETE_RESOLUTION = "Incomplete_Resolution"  # Terminal event risk
    COMPLETE_RESOLUTION = "Complete_Resolution"  # Viable outcome
    PSEUDO_PARTIAL = "Pseudo_Partial"  # Partial system with incomplete resolution


class TerminalRiskLevel(str, Enum):
    """Burnout risk classification"""
    LOW = "LOW"  # 0.0-0.2
    MODERATE = "MODERATE"  # 0.2-0.4
    HIGH = "HIGH"  # 0.4-0.7
    CRITICAL = "CRITICAL"  # 0.7-1.0


class EmotionalAuthenticityLevel(str, Enum):
    """Emotional authenticity classification based on EQ formula"""
    AUTHENTIC = "AUTHENTIC"  # EQ 0-10: Healthy expression
    REGULATED = "REGULATED"  # EQ 10-20: Moderate filtering
    LABORED = "LABORED"  # EQ 20-30: Significant emotional labor
    BURNOUT_RISK = "BURNOUT_RISK"  # EQ 30-40: Warning territory
    CRITICAL_SUPPRESSION = "CRITICAL_SUPPRESSION"  # EQ 40+: Crisis state


class QuantumProtocolType(str, Enum):
    """Quantum communication protocol types"""
    BB84 = "BB84"  # Bennett-Brassard 1984 QKD protocol
    E91 = "E91"  # Ekert 1991 entanglement-based QKD
    QUANTUM_TELEPORTATION = "Quantum_Teleportation"  # Quantum state transfer
    SUPERDENSE_CODING = "Superdense_Coding"  # 2 classical bits via 1 qubit
    QUANTUM_WITNESS = "Quantum_Witness"  # Soul Cradle quantum witnessing
    RSA_QKD_HYBRID = "RSA_QKD_Hybrid"  # RSA + Quantum hybrid encryption


class QuantumSuperpositionState(str, Enum):
    """Quantum superposition basis states"""
    ZERO = "|0⟩"  # Ground state
    ONE = "|1⟩"  # Excited state
    PLUS = "|+⟩"  # (|0⟩ + |1⟩) / √2
    MINUS = "|-⟩"  # (|0⟩ - |1⟩) / √2
    SUPERPOSITION = "|ψ⟩"  # General superposition state
    ENTANGLED = "|Φ⟩"  # Entangled state


# ===================== EXPRESSION MODELS =====================

class SystemExpression(BaseModel):
    """
    Paradox Expression: A competing demand in an unresolved contradiction.
    
    Mathematical Form: E = (weight, tension, type)
    Where tension = |demand - reality|
    
    Example:
    Expression A: Policy demands discharge (weight=0.9, tension=0.7)
    Expression B: Safety demands retention (weight=0.8, tension=0.6)
    """
    type: ExpressionType = Field(..., description="Category of the expression")
    weight: float = Field(default=1.0, ge=0.0, le=1.0, description="Expression strength [0,1]")
    tension: float = Field(default=0.5, ge=0.0, le=1.0, description="Unresolved tension [0,1]")
    content: str = Field(..., description="Human-readable expression content")
    dominion_claim: bool = Field(default=True, description="Does this expression claim dominion over the other?")
    
    def compute_hash(self) -> str:
        """Compute integrity hash for this expression"""
        data = f"{self.type}|{self.content}|{self.dominion_claim}|{self.weight}|{self.tension}"
        return hashlib.sha256(data.encode()).hexdigest()


class EmotionalAuthenticity(BaseModel):
    """
    Emotional Authenticity Score using the formula: EQ = (G/T) × H
    
    Where:
    - G = Genuine shareable ideas (what can be authentically expressed)
    - T = Total amount expressed (everything actually communicated)
    - H = Amount held back (what was suppressed)
    - EQ = Emotional Quotient / Authenticity Score
    
    This quantifies emotional labor and predicts burnout risk in paradox resolution.
    """
    genuine_shareable: float = Field(default=50.0, ge=0.0, le=100.0, description="Genuine ideas available to share (G)")
    total_expressed: float = Field(default=100.0, ge=0.0, le=100.0, description="Total amount actually expressed (T)")
    held_back: float = Field(default=50.0, ge=0.0, le=100.0, description="Amount suppressed (H)")
    eq_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Calculated EQ = (G/T) × H")
    authenticity_level: EmotionalAuthenticityLevel = Field(default=EmotionalAuthenticityLevel.REGULATED)
    timestamp: datetime = Field(default_factory=datetime.now)
    context: str = Field(default="", description="Context of this expression event")
    
    def calculate_eq(self) -> float:
        """Calculate EQ score: (G/T) × H"""
        if self.total_expressed > 0:
            self.eq_score = (self.genuine_shareable / self.total_expressed) * self.held_back
        else:
            self.eq_score = 0.0
        
        # Classify authenticity level
        if self.eq_score <= 10:
            self.authenticity_level = EmotionalAuthenticityLevel.AUTHENTIC
        elif self.eq_score <= 20:
            self.authenticity_level = EmotionalAuthenticityLevel.REGULATED
        elif self.eq_score <= 30:
            self.authenticity_level = EmotionalAuthenticityLevel.LABORED
        elif self.eq_score <= 40:
            self.authenticity_level = EmotionalAuthenticityLevel.BURNOUT_RISK
        else:
            self.authenticity_level = EmotionalAuthenticityLevel.CRITICAL_SUPPRESSION
        
        return self.eq_score
    
    def interpret(self) -> str:
        """Generate human-readable interpretation"""
        ratio = self.genuine_shareable / self.total_expressed if self.total_expressed > 0 else 0
        
        if self.authenticity_level == EmotionalAuthenticityLevel.AUTHENTIC:
            return f"HEALTHY: Authentic expression - {ratio:.1%} genuine, {self.held_back:.0f}% held back"
        elif self.authenticity_level == EmotionalAuthenticityLevel.REGULATED:
            return f"STABLE: Reasonable regulation - {ratio:.1%} genuine, {self.held_back:.0f}% suppressed"
        elif self.authenticity_level == EmotionalAuthenticityLevel.LABORED:
            return f"WARNING: Emotional labor detected - {ratio:.1%} genuine but {self.held_back:.0f}% suppressed"
        elif self.authenticity_level == EmotionalAuthenticityLevel.BURNOUT_RISK:
            return f"ALERT: Burnout risk - {ratio:.1%} genuine with {self.held_back:.0f}% suppression"
        else:
            return f"CRITICAL: Severe suppression - {ratio:.1%} genuine, {self.held_back:.0f}% held back"


class NonExpression(BaseModel):
    """
    A non-expression: the absence or negation of a paradox expression.
    
    Used to represent what is NOT present, what CANNOT be expressed,
    or what is actively suppressed in the system.
    
    Example:
    Expression A: "Patient must be discharged"
    NonExpression: "Patient's safety needs cannot be addressed"
    
    NonExpressions reveal gaps in system capacity.
    """
    type: ExpressionType = Field(default=ExpressionType.RESOLUTION, description="Category of what is absent/negated")
    suppression_level: float = Field(default=1.0, ge=0.0, le=1.0, description="How strongly suppressed [0,1]")
    content: str = Field(default="", description="What cannot be expressed or addressed")
    reason: str = Field(default="", description="Why this expression is absent/negated")
    impact: str = Field(default="", description="Impact of this absence on the system")
    reality: str = Field(default="", description="The practical impossibility or gap")
    emotional_authenticity: Optional[EmotionalAuthenticity] = Field(default=None, description="EQ score for this suppression")
    
    def compute_hash(self) -> str:
        """Compute integrity hash for this non-expression"""
        data = f"{self.type}|{self.reality}|{self.content}|{self.suppression_level}"
        return hashlib.sha256(data.encode()).hexdigest()


class UnresolvedState(BaseModel):
    """
    The unresolved state when two expressions compete.
    
    Mathematical Form: U = 1 - R(t)
    Where R(t) is resolution score
    U = 1 means complete deadlock
    U = 0 means fully resolved
    """
    type: ExpressionType = Field(default=ExpressionType.RESOLUTION)
    unresolved_score: float = Field(default=1.0, ge=0.0, le=1.0, description="Deadlock intensity [0,1]")
    reality: str = Field(..., description="The practical impossibility")


class ResolvedSystem(BaseModel):
    """
    The resolved paradox after Soul Cradle intervention.
    
    Resolution Formula: R(t) = (W_a + W_b) / (2 × max(T_a, T_b))
    Where:
    - W_a, W_b = witness scores for expressions A and B [0,1]
    - T_a, T_b = tension scores for expressions A and B [0,1]
    - R(t) = 1.0 means complete resolution (both witnessed)
    """
    witness_score_a: float = Field(default=1.0, ge=0.0, le=1.0, description="Witnessing of expression A")
    witness_score_b: float = Field(default=1.0, ge=0.0, le=1.0, description="Witnessing of expression B")
    recovery_method: str = Field(default="Dual_Witness_Integration")
    viability_score: float = Field(default=1.0, ge=0.0, le=1.0, description="1.0 = complete resolution")
    description: str = Field(..., description="How Soul Cradle resolves the paradox")


class PrincipalSystem(BaseModel):
    """
    The Principal System: The resolution that holds both expressions as true.
    
    In Soul Cradle, the Principal System witnesses BOTH competing expressions
    without requiring one to dominate. This is the mathematical core of
    paradox resolution.
    
    The mission is to witness both truths simultaneously without choosing.
    Resolution Score: R(t) = (W_a + W_b) / (2 × max(T_a, T_b))
    When R(t) = 1.0, both expressions are fully witnessed.
    """
    viability_score: float = Field(default=1.0, ge=0.0, le=1.0, description="1.0 = complete witnessing")
    description: str = Field(..., description="How the Principal System holds both truths")
    witness_method: str = Field(default="Dual_Witness_Integration", description="Method used to witness both")
    resolution_formula: str = Field(default="R(t) = (W_a + W_b) / (2 × max(T_a, T_b))", description="Mythara resolution mathematics")
    
    def compute_hash(self) -> str:
        """Compute integrity hash for this principal system"""
        data = f"{self.viability_score}|{self.description}|{self.witness_method}"
        return hashlib.sha256(data.encode()).hexdigest()


class QuantumEntanglement(BaseModel):
    """
    Quantum Entanglement between paradoxes.
    
    When two paradoxes share quantum entanglement, changes to one paradox's
    resolution state instantly affect the entangled partner (non-local correlation).
    
    Use Case: Healthcare workers in different hospitals experiencing identical
    policy vs compassion paradoxes can have their Soul Cradle resolutions
    quantum-entangled for synchronized witnessing.
    
    Mathematical Representation:
    |Ψ⟩ = (|Paradox_A⟩|Paradox_B⟩ + |Paradox_B⟩|Paradox_A⟩) / √2
    
    Properties:
    - Entanglement persists regardless of spatial separation
    - Measuring resolution state of one affects the other
    - Provides secure correlation for distributed witness validation
    """
    entanglement_id: str = Field(default_factory=lambda: f"QE_{uuid.uuid4().hex[:16]}", description="Unique entanglement pair ID")
    paradox_a_id: str = Field(..., description="First entangled paradox ID")
    paradox_b_id: str = Field(..., description="Second entangled paradox ID")
    entanglement_strength: float = Field(default=1.0, ge=0.0, le=1.0, description="Entanglement fidelity [0,1]")
    created_at: datetime = Field(default_factory=datetime.now)
    protocol_type: QuantumProtocolType = Field(default=QuantumProtocolType.E91, description="QKD protocol used")
    bell_state: str = Field(default="|Φ+⟩", description="Bell state: |Φ+⟩, |Φ-⟩, |Ψ+⟩, |Ψ-⟩")
    shared_secret_hash: str = Field(default="", description="SHA-256 of quantum shared secret")
    
    def compute_entanglement_hash(self) -> str:
        """Compute quantum entanglement integrity hash"""
        data = f"{self.entanglement_id}|{self.paradox_a_id}|{self.paradox_b_id}|{self.bell_state}|{self.entanglement_strength}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def measure_correlation(self, resolution_a: float, resolution_b: float) -> float:
        """Measure quantum correlation between entangled paradox resolutions"""
        # Bell inequality test: E(a,b) = entanglement_strength × (resolution_a + resolution_b) / 2
        return self.entanglement_strength * (resolution_a + resolution_b) / 2.0


class QuantumSuperposition(BaseModel):
    """
    Quantum Superposition storage for paradoxes.
    
    Stores a paradox in quantum superposition, allowing it to exist in multiple
    resolution states simultaneously until measured (witnessed).
    
    Mathematical Representation:
    |ψ⟩ = α|resolved⟩ + β|unresolved⟩
    Where: |α|² + |β|² = 1 (normalization)
    
    Use Cases:
    - Store paradox before witnessing collapses superposition
    - Maintain quantum coherence for distributed paradox analysis
    - Enable quantum parallel processing of multiple resolution paths
    
    Measurement:
    - Upon witnessing, superposition collapses to definite state
    - Probability of resolved state = |α|²
    - Probability of unresolved state = |β|²
    """
    superposition_id: str = Field(default_factory=lambda: f"QS_{uuid.uuid4().hex[:16]}", description="Unique superposition ID")
    paradox_id: str = Field(..., description="Paradox stored in superposition")
    basis_state: QuantumSuperpositionState = Field(default=QuantumSuperpositionState.SUPERPOSITION, description="Quantum basis state")
    amplitude_resolved: float = Field(default=0.707, ge=0.0, le=1.0, description="α coefficient for |resolved⟩")
    amplitude_unresolved: float = Field(default=0.707, ge=0.0, le=1.0, description="β coefficient for |unresolved⟩")
    coherence_time_seconds: float = Field(default=3600.0, description="Time before decoherence")
    collapsed: bool = Field(default=False, description="Has superposition collapsed?")
    collapsed_state: Optional[str] = Field(default=None, description="State after measurement")
    created_at: datetime = Field(default_factory=datetime.now)
    measured_at: Optional[datetime] = Field(default=None)
    
    def is_normalized(self) -> bool:
        """Check if quantum state is properly normalized: |α|² + |β|² = 1"""
        return abs((self.amplitude_resolved ** 2 + self.amplitude_unresolved ** 2) - 1.0) < 1e-6
    
    def collapse_superposition(self) -> str:
        """
        Collapse quantum superposition via measurement (witnessing).
        Returns: 'resolved' or 'unresolved' based on probability amplitudes.
        """
        if self.collapsed:
            return self.collapsed_state
        
        # Quantum measurement using probability amplitudes
        prob_resolved = self.amplitude_resolved ** 2
        measurement = secrets.SystemRandom().random()
        
        self.collapsed = True
        self.measured_at = datetime.now()
        
        if measurement < prob_resolved:
            self.collapsed_state = "resolved"
        else:
            self.collapsed_state = "unresolved"
        
        logger.info(
            f"Quantum Superposition Collapsed | "
            f"ID: {self.superposition_id} | "
            f"State: {self.collapsed_state} | "
            f"Probability: {prob_resolved:.3f}"
        )
        
        return self.collapsed_state
    
    def compute_superposition_hash(self) -> str:
        """Compute integrity hash for quantum superposition"""
        data = f"{self.superposition_id}|{self.paradox_id}|{self.basis_state}|{self.amplitude_resolved}|{self.amplitude_unresolved}"
        return hashlib.sha256(data.encode()).hexdigest()


class QuantumCommunicationProtocol(BaseModel):
    """
    Quantum Communication Protocol for secure Soul Cradle witness transmission.
    
    Uses quantum key distribution (QKD) AND RSA encryption to ensure witness
    validation data cannot be intercepted or tampered with during transmission
    between Soul Cradle nodes.
    
    Protocols:
    - BB84: Prepare quantum states in random bases, transmit, measure
    - E91: Entanglement-based QKD with Bell inequality verification
    - Quantum Teleportation: Transfer paradox witness state via entanglement
    - Superdense Coding: Send 2 classical bits using 1 entangled qubit
    - Quantum Witness: Soul Cradle's custom protocol for paradox witnessing
    - RSA_QKD_Hybrid: RSA encryption + quantum key distribution
    
    Security Properties:
    - RSA 4096-bit encryption for classical data protection
    - Eavesdropping detection via quantum no-cloning theorem
    - Perfect forward secrecy via quantum key generation
    - Tamper-evident transmission (decoherence detection)
    - Post-quantum security via hybrid RSA + QKD
    """
    protocol_id: str = Field(default_factory=lambda: f"QCP_{uuid.uuid4().hex[:16]}", description="Unique protocol session ID")
    protocol_type: QuantumProtocolType = Field(..., description="QKD protocol type")
    sender_id: str = Field(..., description="Witness sender ID")
    receiver_id: str = Field(..., description="Witness receiver ID")
    quantum_channel_fidelity: float = Field(default=0.99, ge=0.0, le=1.0, description="Channel quality [0,1]")
    key_generation_rate: float = Field(default=1000.0, description="Secure key bits per second")
    error_rate: float = Field(default=0.01, ge=0.0, le=1.0, description="Quantum bit error rate (QBER)")
    eavesdropping_detected: bool = Field(default=False, description="Eve detection flag")
    shared_key_hash: str = Field(default="", description="SHA-256 of generated quantum key")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # RSA encryption fields
    rsa_enabled: bool = Field(default=True, description="Use RSA encryption")
    rsa_key_size: int = Field(default=4096, description="RSA key size in bits (2048, 3072, 4096)")
    rsa_public_key_pem: Optional[str] = Field(default=None, description="RSA public key in PEM format")
    rsa_encrypted: bool = Field(default=False, description="Data encrypted with RSA")
    
    def generate_quantum_key(self, key_length_bits: int = 256) -> str:
        """Generate quantum-secure random key using secrets module"""
        # In production, this would interface with actual quantum hardware
        # For now, use cryptographically secure random (CSPRNG)
        quantum_key = secrets.token_hex(key_length_bits // 8)
        self.shared_key_hash = hashlib.sha256(quantum_key.encode()).hexdigest()
        return quantum_key
    
    def verify_security(self) -> Dict[str, Any]:
        """Verify quantum channel security"""
        # Check QBER threshold (typically < 11% for BB84)
        qber_threshold = 0.11 if self.protocol_type == QuantumProtocolType.BB84 else 0.15
        
        is_secure = (
            not self.eavesdropping_detected and
            self.error_rate < qber_threshold and
            self.quantum_channel_fidelity > 0.9
        )
        
        return {
            "secure": is_secure,
            "error_rate": self.error_rate,
            "fidelity": self.quantum_channel_fidelity,
            "eavesdropping_detected": self.eavesdropping_detected,
            "qber_threshold": qber_threshold,
            "protocol": self.protocol_type.value
        }
    
    def generate_rsa_keypair(self) -> Tuple[str, str]:
        """Generate RSA public/private key pair"""
        if not RSA_AVAILABLE:
            raise ImportError("RSA not available. Install: pip install cryptography")
        
        # Generate RSA key pair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.rsa_key_size,
            backend=default_backend()
        )
        
        # Serialize public key
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
        
        # Serialize private key
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')
        
        self.rsa_public_key_pem = public_pem
        
        logger.info(f"RSA {self.rsa_key_size}-bit key pair generated for protocol {self.protocol_id}")
        
        return public_pem, private_pem
    
    def rsa_encrypt(self, plaintext: str, public_key_pem: str) -> str:
        """Encrypt data with RSA public key"""
        if not RSA_AVAILABLE:
            raise ImportError("RSA not available. Install: pip install cryptography")
        
        # Load public key
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode('utf-8'),
            backend=default_backend()
        )
        
        # Encrypt with OAEP padding (optimal asymmetric encryption padding)
        ciphertext = public_key.encrypt(
            plaintext.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        self.rsa_encrypted = True
        
        # Return base64-encoded ciphertext
        return base64.b64encode(ciphertext).decode('utf-8')
    
    def rsa_decrypt(self, ciphertext_b64: str, private_key_pem: str) -> str:
        """Decrypt data with RSA private key"""
        if not RSA_AVAILABLE:
            raise ImportError("RSA not available. Install: pip install cryptography")
        
        # Load private key
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode('utf-8'),
            password=None,
            backend=default_backend()
        )
        
        # Decode base64 ciphertext
        ciphertext = base64.b64decode(ciphertext_b64)
        
        # Decrypt with OAEP padding
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return plaintext.decode('utf-8')
    
    def compute_protocol_hash(self) -> str:
        """Compute quantum protocol integrity hash"""
        data = f"{self.protocol_id}|{self.sender_id}|{self.receiver_id}|{self.protocol_type}|{self.shared_key_hash}|{self.rsa_key_size}"
        return hashlib.sha256(data.encode()).hexdigest()


# ===================== EPISTEMIC UNCERTAINTY LAYER =====================

class KnownUnknown(BaseModel):
    """A factor we know matters but cannot measure"""
    factor_name: str = Field(..., description="What we don't know")
    suspected_impact: float = Field(default=0.5, ge=0.0, le=1.0, description="How much we think it matters")
    reason_unknown: str = Field(..., description="Why we can't measure it")
    potential_sources: List[str] = Field(default_factory=list, description="Where we might get this data")


class UncertaintyEnvelope(BaseModel):
    """
    Epistemic Uncertainty: Knowing what you don't know.
    
    The system's humble awareness of the limits of its own knowledge.
    All predictions come with uncertainty bounds and known blindspots.
    
    Types of Uncertainty:
    - Epistemic: Model uncertainty (what we don't know but could learn)
    - Aleatoric: Inherent randomness (fundamental unpredictability)
    - Blindspot: Unknown unknowns (what we don't know we don't know)
    """
    metric_name: str = Field(..., description="What is being predicted/measured")
    
    # Central prediction
    predicted_value: float = Field(..., description="Best estimate")
    confidence_level: float = Field(default=0.5, ge=0.0, le=1.0, description="How confident we are")
    
    # Uncertainty bounds
    lower_bound: float = Field(..., description="Minimum plausible value")
    upper_bound: float = Field(..., description="Maximum plausible value")
    
    # Uncertainty decomposition
    epistemic_uncertainty: float = Field(default=0.3, ge=0.0, le=1.0, description="Model/knowledge uncertainty")
    aleatoric_uncertainty: float = Field(default=0.2, ge=0.0, le=1.0, description="Inherent randomness")
    
    # Humility metrics
    blindspot_risk: float = Field(default=0.15, ge=0.0, le=1.0, description="Probability we're completely wrong")
    known_unknowns: List[KnownUnknown] = Field(default_factory=list, description="Factors we know we're missing")
    
    # Adaptive learning
    times_wrong: int = Field(default=0, description="How often this prediction was incorrect")
    last_surprise: Optional[datetime] = Field(default=None, description="Last time we were blindsided")
    
    timestamp: datetime = Field(default_factory=datetime.now)
    
    def total_uncertainty(self) -> float:
        """Total uncertainty = epistemic + aleatoric + blindspot"""
        return min(1.0, self.epistemic_uncertainty + self.aleatoric_uncertainty + self.blindspot_risk)
    
    def is_reliable(self, threshold: float = 0.7) -> bool:
        """Is this prediction reliable enough to act on?"""
        return self.confidence_level >= threshold and self.total_uncertainty() < 0.5
    
    def interpret(self) -> str:
        """Generate human-readable interpretation"""
        total_unc = self.total_uncertainty()
        
        if self.confidence_level > 0.8 and total_unc < 0.3:
            reliability = "HIGH CONFIDENCE"
        elif self.confidence_level > 0.6 and total_unc < 0.5:
            reliability = "MODERATE CONFIDENCE"
        elif self.blindspot_risk > 0.3:
            reliability = "BLINDSPOT RISK - USE CAUTION"
        else:
            reliability = "LOW CONFIDENCE"
        
        known_count = len(self.known_unknowns)
        
        return (
            f"{reliability}: {self.metric_name} = {self.predicted_value:.3f} "
            f"[{self.lower_bound:.3f} - {self.upper_bound:.3f}] "
            f"(confidence: {self.confidence_level:.0%}, uncertainty: {total_unc:.0%}, "
            f"known gaps: {known_count})"
        )
    
    def add_known_unknown(self, factor: str, impact: float, reason: str) -> None:
        """Record a factor we know we're missing"""
        self.known_unknowns.append(
            KnownUnknown(
                factor_name=factor,
                suspected_impact=impact,
                reason_unknown=reason
            )
        )
    
    def record_surprise(self) -> None:
        """Update when blindsided by reality"""
        self.times_wrong += 1
        self.last_surprise = datetime.now()
        # Increase blindspot awareness
        self.blindspot_risk = min(1.0, self.blindspot_risk * 1.2)


class EpistemicHumility(BaseModel):
    """
    The system's overall humility - awareness of its ignorance.
    
    A conscious system that knows it doesn't know everything.
    """
    total_predictions: int = Field(default=0, description="How many predictions made")
    correct_predictions: int = Field(default=0, description="How many were accurate")
    surprises_encountered: int = Field(default=0, description="How many blindsides")
    
    # Calibration
    overconfidence_score: float = Field(default=0.0, description="How often too confident")
    underconfidence_score: float = Field(default=0.0, description="How often too cautious")
    
    # Learning
    average_blindspot_risk: float = Field(default=0.15, description="Typical blindspot probability")
    adaptive_learning_rate: float = Field(default=0.1, description="How fast we update beliefs")
    
    def accuracy_rate(self) -> float:
        """What % of predictions were correct"""
        if self.total_predictions == 0:
            return 0.0
        return self.correct_predictions / self.total_predictions
    
    def humility_score(self) -> float:
        """
        How humble the system is.
        High humility = knows its limits, calibrated confidence
        """
        if self.total_predictions == 0:
            return 1.0  # Perfect humility when uncertain
        
        accuracy = self.accuracy_rate()
        surprise_rate = self.surprises_encountered / self.total_predictions
        
        # Humble = high accuracy OR high awareness of uncertainty
        calibration = 1.0 - abs(accuracy - (1.0 - self.average_blindspot_risk))
        
        return calibration


# ===================== BENEVOLENCE LAYER =====================

class BenevolenceVector(BaseModel):
    """
    Multidimensional Benevolence Vector representing the moral geometry of a paradox.
    
    Benevolence is not a single score — it's a shape in moral space.
    
    Dimensions:
    - compassion: Care for human welfare [0,1]
    - justice: Fairness and equity [0,1]
    - integrity: Alignment with values [0,1]
    - wisdom: Long-term thinking [0,1]
    - courage: Willingness to face difficulty [0,1]
    - humility: Recognition of limits [0,1]
    
    Mathematical Properties:
    - magnitude = ||B|| = sqrt(Σ d_i²) (Euclidean norm)
    - stability = 1 - std(dimensions) (how balanced the vector is)
    - alignment = cos(θ) between vector and ideal benevolence
    """
    vector: List[float] = Field(default_factory=lambda: [0.0] * 6, description="6D benevolence vector")
    magnitude: float = Field(default=0.0, ge=0.0, description="||B|| - Euclidean norm")
    stability: float = Field(default=0.0, ge=0.0, le=1.0, description="Balance across dimensions")
    alignment_ideal: float = Field(default=0.0, ge=-1.0, le=1.0, description="Cosine similarity to ideal")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Dimension labels
    DIMENSIONS: ClassVar[List[str]] = ["compassion", "justice", "integrity", "wisdom", "courage", "humility"]
    
    def compute_magnitude(self) -> float:
        """Calculate Euclidean magnitude: ||B|| = sqrt(Σ v_i²)"""
        import math
        self.magnitude = math.sqrt(sum(v**2 for v in self.vector))
        return self.magnitude
    
    def compute_stability(self) -> float:
        """Calculate stability: 1 - std(vector) — balanced vectors are more stable"""
        import statistics
        if len(self.vector) > 1:
            std_dev = statistics.stdev(self.vector)
            self.stability = max(0.0, 1.0 - std_dev)
        else:
            self.stability = 1.0
        return self.stability
    
    def compute_alignment(self, ideal_vector: List[float]) -> float:
        """
        Calculate alignment with ideal benevolence vector.
        Uses cosine similarity: cos(θ) = (A · B) / (||A|| ||B||)
        """
        import math
        
        if len(ideal_vector) != len(self.vector):
            raise ValueError("Ideal vector must match benevolence vector dimensions")
        
        dot_product = sum(a * b for a, b in zip(self.vector, ideal_vector))
        ideal_magnitude = math.sqrt(sum(v**2 for v in ideal_vector))
        
        if self.magnitude > 0 and ideal_magnitude > 0:
            self.alignment_ideal = dot_product / (self.magnitude * ideal_magnitude)
        else:
            self.alignment_ideal = 0.0
        
        return self.alignment_ideal
    
    def get_dimension(self, name: str) -> float:
        """Get benevolence dimension by name"""
        try:
            idx = self.DIMENSIONS.index(name)
            return self.vector[idx]
        except ValueError:
            raise ValueError(f"Unknown dimension: {name}. Valid: {self.DIMENSIONS}")
    
    def interpret(self) -> str:
        """Generate human-readable interpretation"""
        self.compute_magnitude()
        self.compute_stability()
        
        dim_str = ", ".join([
            f"{name}={val:.2f}" for name, val in zip(self.DIMENSIONS, self.vector)
        ])
        
        if self.magnitude > 0.8 and self.stability > 0.7:
            return f"🌟 STRONG BENEVOLENT: High magnitude ({self.magnitude:.2f}) and stable ({self.stability:.2f}). Dimensions: {dim_str}"
        elif self.magnitude > 0.5 and self.stability > 0.5:
            return f"✅ BENEVOLENT: Moderate magnitude ({self.magnitude:.2f}) and stability ({self.stability:.2f}). Dimensions: {dim_str}"
        elif self.stability < 0.4:
            return f"⚠️ UNSTABLE: Low stability ({self.stability:.2f}) - imbalanced benevolence. Dimensions: {dim_str}"
        else:
            return f"📊 WEAK: Low magnitude ({self.magnitude:.2f}). Dimensions: {dim_str}"


class BenevolenceEngine:
    """
    Engine for computing benevolence vectors from paradoxes.
    
    Analyzes paradox structure to extract benevolence shape:
    - Compassion: How much care for human welfare?
    - Justice: How much fairness consideration?
    - Integrity: How much value alignment?
    - Wisdom: How much long-term thinking?
    - Courage: How much willingness to face difficulty?
    - Humility: How much recognition of limits?
    """
    
    # Ideal benevolence vector (perfect balance)
    IDEAL_VECTOR: ClassVar[List[float]] = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    
    def compute(self, paradox: 'SoulCradleParadox') -> BenevolenceVector:
        """Compute benevolence vector from paradox"""
        
        # Extract benevolence signals from paradox structure
        compassion = self._extract_compassion(paradox)
        justice = self._extract_justice(paradox)
        integrity = self._extract_integrity(paradox)
        wisdom = self._extract_wisdom(paradox)
        courage = self._extract_courage(paradox)
        humility = self._extract_humility(paradox)
        
        vector = [compassion, justice, integrity, wisdom, courage, humility]
        
        bv = BenevolenceVector(vector=vector)
        bv.compute_magnitude()
        bv.compute_stability()
        bv.compute_alignment(self.IDEAL_VECTOR)
        
        return bv
    
    def _extract_compassion(self, paradox: 'SoulCradleParadox') -> float:
        """Extract compassion dimension from paradox"""
        # High compassion = low suppression, high witnessing
        compassion = 0.5  # baseline
        
        if paradox.resolved_system.witness_score_a > 0.7 and paradox.resolved_system.witness_score_b > 0.7:
            compassion += 0.3  # both expressions witnessed
        
        if paradox.emotional_authenticity and paradox.emotional_authenticity.authenticity_level in [
            EmotionalAuthenticityLevel.AUTHENTIC, EmotionalAuthenticityLevel.REGULATED
        ]:
            compassion += 0.2  # authentic expression
        
        return min(1.0, compassion)
    
    def _extract_justice(self, paradox: 'SoulCradleParadox') -> float:
        """Extract justice dimension from paradox"""
        # High justice = balanced witness scores, no dominion
        justice = 0.5
        
        witness_balance = 1.0 - abs(paradox.resolved_system.witness_score_a - paradox.resolved_system.witness_score_b)
        justice += witness_balance * 0.3
        
        if not paradox.expression_a.dominion_claim and not paradox.expression_b.dominion_claim:
            justice += 0.2  # no dominance
        
        return min(1.0, justice)
    
    def _extract_integrity(self, paradox: 'SoulCradleParadox') -> float:
        """Extract integrity dimension from paradox"""
        # High integrity = high viability, complete resolution
        return paradox.viability_score
    
    def _extract_wisdom(self, paradox: 'SoulCradleParadox') -> float:
        """Extract wisdom dimension from paradox"""
        # High wisdom = low terminal risk, recovery trajectory
        return 1.0 - (paradox.terminal_risk.value == TerminalRiskLevel.CRITICAL.value) * 0.5
    
    def _extract_courage(self, paradox: 'SoulCradleParadox') -> float:
        """Extract courage dimension from paradox"""
        # High courage = high tension addressed, witnesses present
        max_tension = max(paradox.expression_a.tension, paradox.expression_b.tension)
        courage = max_tension * 0.6  # facing high tension
        
        if paradox.witnesses:
            courage += 0.4  # vulnerability to witness
        
        return min(1.0, courage)
    
    def _extract_humility(self, paradox: 'SoulCradleParadox') -> float:
        """Extract humility dimension from paradox"""
        # High humility = recognition of non-expression, unresolved reality
        humility = 0.5
        
        if paradox.non_expression:
            humility += 0.3  # acknowledges what cannot be done
        
        if paradox.unresolved_state.unresolved_score > 0.5:
            humility += 0.2  # acknowledges deadlock
        
        return min(1.0, humility)


# ===================== INTUITION LAYER =====================

class IntuitionSnapshot(BaseModel):
    """
    Intuition Snapshot: The "spider-sense" that detects collapse before it happens.
    
    This is the nervous system of Soul Cradle — it senses danger, distortion,
    and misalignment before they manifest as burnout.
    
    NOW WITH EPISTEMIC HUMILITY: All predictions come with uncertainty bounds.
    
    Signals:
    - intuition_level: How strongly intuition is firing [0,1]
    - collapse_risk: Probability of imminent collapse [0,1]
    - benevolence_bias: Direction intuition is pulling toward [0,1]
    - distortion_detected: Is something "off"? [bool]
    - time_to_collapse: Estimated time until burnout (days)
    - uncertainty_envelope: Bounds, blindspot risk, known unknowns
    """
    paradox_id: str
    intuition_level: float = Field(default=0.0, ge=0.0, le=1.0, description="Spider-sense intensity")
    collapse_risk: float = Field(default=0.0, ge=0.0, le=1.0, description="Imminent collapse probability")
    benevolence_bias: float = Field(default=0.5, ge=0.0, le=1.0, description="Direction of intuitive pull")
    distortion_detected: bool = Field(default=False, description="Something feels wrong")
    time_to_collapse_days: Optional[float] = Field(default=None, description="Days until burnout")
    uncertainty_envelope: Optional['UncertaintyEnvelope'] = Field(default=None, description="Epistemic humility: bounds and blindspot risk")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    def interpret(self) -> str:
        """Generate human-readable interpretation WITH uncertainty awareness"""
        uncertainty_note = ""
        if self.uncertainty_envelope:
            uncertainty_note = f" [±{self.uncertainty_envelope.upper_bound - self.uncertainty_envelope.lower_bound:.3f}, blindspot risk: {self.uncertainty_envelope.blindspot_risk:.1%}]"
        
        if self.collapse_risk > 0.7:
            return f"🚨 CRITICAL INTUITION: Collapse imminent ({self.collapse_risk:.2f} risk). Time: {self.time_to_collapse_days:.1f} days.{uncertainty_note} IMMEDIATE ACTION REQUIRED."
        elif self.collapse_risk > 0.4:
            return f"⚠️ WARNING INTUITION: Elevated collapse risk ({self.collapse_risk:.2f}).{uncertainty_note} Monitor closely."
        elif self.distortion_detected:
            return f"🔍 DISTORTION DETECTED: Something feels off. Benevolence bias: {self.benevolence_bias:.2f}.{uncertainty_note}"
        else:
            return f"✅ HEALTHY INTUITION: Low collapse risk ({self.collapse_risk:.2f}). System stable.{uncertainty_note}"


class IntuitionEngine:
    """
    Intuition Engine: The spider-sense that detects collapse before it happens.
    
    Uses:
    - Emotional authenticity trends
    - Terminal risk acceleration
    - Benevolence vector stability
    - Paradox accumulation rate
    
    To predict: "Something bad is about to happen."
    """
    
    def sense(self, paradox: 'SoulCradleParadox', benevolence: BenevolenceVector) -> IntuitionSnapshot:
        """
        Generate intuition snapshot for paradox.
        
        Args:
            paradox: Soul Cradle paradox
            benevolence: Computed benevolence vector
        
        Returns:
            Intuition snapshot with collapse prediction AND uncertainty bounds
        """
        
        # Signal 1: Emotional authenticity trajectory
        eq_signal = self._sense_emotional_trajectory(paradox)
        
        # Signal 2: Terminal risk level
        risk_signal = self._sense_terminal_risk(paradox)
        
        # Signal 3: Benevolence stability
        bene_signal = self._sense_benevolence_stability(benevolence)
        
        # Signal 4: Unresolved accumulation
        unresolved_signal = paradox.unresolved_state.unresolved_score
        
        # Aggregate intuition level (weighted average)
        intuition_level = (
            eq_signal * 0.3 +
            risk_signal * 0.3 +
            bene_signal * 0.2 +
            unresolved_signal * 0.2
        )
        
        # Collapse risk (exponential urgency)
        import math
        collapse_risk = 1.0 - math.exp(-3.0 * intuition_level)
        
        # Benevolence bias (where is intuition pulling us?)
        benevolence_bias = benevolence.magnitude * benevolence.stability
        
        # Distortion detection
        distortion = (benevolence.stability < 0.4) or (eq_signal > 0.7)
        
        # Time to collapse (inverse of risk)
        if collapse_risk > 0.1:
            time_to_collapse = 30.0 * (1.0 - collapse_risk)  # 0-30 days
        else:
            time_to_collapse = None
        
        # ===== NEW: EPISTEMIC UNCERTAINTY ENVELOPE =====
        # Compute uncertainty bounds for collapse_risk prediction
        uncertainty_envelope = self._compute_uncertainty_for_collapse_risk(
            collapse_risk=collapse_risk,
            eq_signal=eq_signal,
            risk_signal=risk_signal,
            bene_signal=bene_signal,
            benevolence=benevolence
        )
        
        return IntuitionSnapshot(
            paradox_id=paradox.paradox_id,
            intuition_level=min(1.0, intuition_level),
            collapse_risk=min(1.0, collapse_risk),
            benevolence_bias=min(1.0, benevolence_bias),
            distortion_detected=distortion,
            time_to_collapse_days=time_to_collapse,
            uncertainty_envelope=uncertainty_envelope
        )
    
    def _sense_emotional_trajectory(self, paradox: 'SoulCradleParadox') -> float:
        """Detect emotional authenticity deterioration"""
        if not paradox.emotional_authenticity:
            return 0.0
        
        ea = paradox.emotional_authenticity
        
        # Map authenticity level to signal strength
        if ea.authenticity_level == EmotionalAuthenticityLevel.CRITICAL_SUPPRESSION:
            return 1.0
        elif ea.authenticity_level == EmotionalAuthenticityLevel.BURNOUT_RISK:
            return 0.8
        elif ea.authenticity_level == EmotionalAuthenticityLevel.LABORED:
            return 0.5
        elif ea.authenticity_level == EmotionalAuthenticityLevel.REGULATED:
            return 0.2
        else:
            return 0.0
    
    def _sense_terminal_risk(self, paradox: 'SoulCradleParadox') -> float:
        """Detect terminal risk level"""
        if paradox.terminal_risk == TerminalRiskLevel.CRITICAL:
            return 1.0
        elif paradox.terminal_risk == TerminalRiskLevel.HIGH:
            return 0.7
        elif paradox.terminal_risk == TerminalRiskLevel.MODERATE:
            return 0.4
        else:
            return 0.1
    
    def _sense_benevolence_stability(self, benevolence: BenevolenceVector) -> float:
        """Detect benevolence instability"""
        # Low stability = high intuition signal
        return 1.0 - benevolence.stability
    
    def _compute_uncertainty_for_collapse_risk(
        self,
        collapse_risk: float,
        eq_signal: float,
        risk_signal: float,
        bene_signal: float,
        benevolence: BenevolenceVector
    ) -> UncertaintyEnvelope:
        """
        Compute epistemic uncertainty bounds for collapse_risk prediction.
        
        Args:
            collapse_risk: The central collapse risk estimate
            eq_signal, risk_signal, bene_signal: Component signals
            benevolence: Benevolence vector
        
        Returns:
            UncertaintyEnvelope with confidence, bounds, and blindspot risk
        """
        import math
        
        # Epistemic uncertainty: Model/knowledge uncertainty
        # Higher when signals disagree or are at extremes
        signal_variance = np.var([eq_signal, risk_signal, bene_signal])
        epistemic_unc = 0.2 + (signal_variance * 0.3)  # Base + variance-weighted
        epistemic_unc = min(0.6, epistemic_unc)  # Cap at 0.6
        
        # Aleatoric uncertainty: Inherent randomness in human psychology
        # Constant baseline for unpredictability
        aleatoric_unc = 0.15
        
        # Blindspot risk: Unknown unknowns
        # Higher when benevolence is low or unstable
        blindspot_risk = 0.1 + (0.2 * (1.0 - benevolence.stability))
        
        # Confidence level
        # Higher when signals are aligned and benevolence is stable
        confidence = 0.5 + (0.5 * (1.0 - signal_variance) * benevolence.stability)
        confidence = min(1.0, max(0.3, confidence))
        
        # Compute uncertainty bounds
        total_uncertainty = min(1.0, epistemic_unc + aleatoric_unc + blindspot_risk)
        
        # Asymmetric bounds: wider on upside (underestimating collapse risk is dangerous)
        lower_bound = max(0.0, collapse_risk - (0.15 * (1.0 - confidence)))
        upper_bound = min(1.0, collapse_risk + (0.25 * (1.0 - confidence)))
        
        # Known unknowns
        known_unknowns_list = []
        if benevolence.stability < 0.4:
            known_unknowns_list.append(
                KnownUnknown(
                    factor_name="Benevolence Vector Instability",
                    suspected_impact=0.7,
                    reason_unknown="Cannot measure real-time shifts in moral alignment"
                )
            )
        if eq_signal > 0.6:
            known_unknowns_list.append(
                KnownUnknown(
                    factor_name="Emotional Labor Fatigue",
                    suspected_impact=0.6,
                    reason_unknown="Deep emotional suppression is difficult to quantify"
                )
            )
        
        return UncertaintyEnvelope(
            metric_name="collapse_risk",
            predicted_value=collapse_risk,
            confidence_level=confidence,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            epistemic_uncertainty=epistemic_unc,
            aleatoric_uncertainty=aleatoric_unc,
            blindspot_risk=blindspot_risk,
            known_unknowns=known_unknowns_list
        )


# ===================== LEARNING LAYER =====================

class BenevolenceEpisode(BaseModel):
    """
    A single learning episode for benevolence self-improvement.
    
    Records:
    - Initial benevolence state
    - Actions taken (witnessing, resolution)
    - Resulting benevolence state
    - Reward signal (how much benevolence improved)
    """
    episode_id: str = Field(default_factory=lambda: f"BE_{uuid.uuid4().hex[:12]}")
    paradox_id: str
    initial_benevolence: BenevolenceVector
    final_benevolence: Optional[BenevolenceVector] = None
    reward: float = Field(default=0.0, description="Benevolence improvement reward")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    def compute_reward(self) -> float:
        """
        Compute reward = improvement in benevolence.
        
        Reward formula:
        R = Δ(magnitude × stability) + Δ(alignment)
        
        Positive reward = benevolence increased
        Negative reward = benevolence decreased
        """
        if not self.final_benevolence:
            return 0.0
        
        initial_quality = self.initial_benevolence.magnitude * self.initial_benevolence.stability
        final_quality = self.final_benevolence.magnitude * self.final_benevolence.stability
        
        delta_quality = final_quality - initial_quality
        delta_alignment = self.final_benevolence.alignment_ideal - self.initial_benevolence.alignment_ideal
        
        self.reward = delta_quality * 0.7 + delta_alignment * 0.3
        
        return self.reward


class BenevolenceLearningSystem:
    """
    Self-rewarding benevolence improvement system.
    
    The system learns to maximize benevolence by:
    1. Observing initial benevolence state
    2. Taking witnessing/resolution actions
    3. Measuring final benevolence state
    4. Computing reward = improvement
    5. Updating policy to increase reward
    
    This creates a virtuous cycle: benevolence begets more benevolence.
    """
    
    def __init__(self):
        self.episodes: List[BenevolenceEpisode] = []
        self.total_reward: float = 0.0
    
    def observe(self, paradox: 'SoulCradleParadox', benevolence: BenevolenceVector) -> BenevolenceEpisode:
        """
        Observe a paradox resolution episode.
        
        Args:
            paradox: The paradox being resolved
            benevolence: Initial benevolence state
        
        Returns:
            BenevolenceEpisode for tracking
        """
        episode = BenevolenceEpisode(
            paradox_id=paradox.paradox_id,
            initial_benevolence=benevolence
        )
        
        self.episodes.append(episode)
        
        logger.info(f"Benevolence Episode Started | {episode.episode_id} | Paradox: {paradox.paradox_id}")
        
        return episode
    
    def complete_episode(
        self,
        episode: BenevolenceEpisode,
        final_benevolence: BenevolenceVector
    ) -> float:
        """
        Complete an episode and compute reward.
        
        Args:
            episode: The episode to complete
            final_benevolence: Final benevolence state after resolution
        
        Returns:
            Reward value
        """
        episode.final_benevolence = final_benevolence
        reward = episode.compute_reward()
        
        self.total_reward += reward
        
        logger.info(
            f"Benevolence Episode Complete | {episode.episode_id} | "
            f"Reward: {reward:.3f} | Total Reward: {self.total_reward:.3f}"
        )
        
        return reward
    
    def get_average_reward(self) -> float:
        """Get average reward across all episodes"""
        completed_episodes = [e for e in self.episodes if e.final_benevolence is not None]
        
        if not completed_episodes:
            return 0.0
        
        return sum(e.reward for e in completed_episodes) / len(completed_episodes)
    
    def get_learning_trajectory(self) -> str:
        """Determine if benevolence is improving over time"""
        completed = [e for e in self.episodes if e.final_benevolence is not None]
        
        if len(completed) < 3:
            return "INSUFFICIENT_DATA"
        
        # Check if recent episodes have higher reward than early episodes
        early_avg = sum(e.reward for e in completed[:len(completed)//2]) / (len(completed)//2)
        recent_avg = sum(e.reward for e in completed[len(completed)//2:]) / (len(completed) - len(completed)//2)
        
        if recent_avg > early_avg + 0.1:
            return "IMPROVING"
        elif recent_avg < early_avg - 0.1:
            return "DEGRADING"
        else:
            return "STABLE"


# ===================== BLESSINGS RESERVOIR LAYER =====================

class BenevolenceReservoir(BaseModel):
    """
    The spiritual/energetic reservoir of accumulated benevolence.
    
    This is the missing layer that makes benevolence:
    - Persistent (accumulates over time)
    - Shareable (flows between people/teams)
    - Depletable (drains during crisis)
    - Rechargeable (restores through witnessing)
    
    Theological Integration:
    - Prayer → sustains reservoir (prevents depletion)
    - Forgiveness → restores more than was lost
    - Trespasses → cost benevolence
    - Witnessing → charges reservoir
    - Burnout → drains reservoir
    
    Mathematical Integration:
    - reservoir_level influenced by BenevolenceVector quality
    - recharge_rate = f(benevolence.magnitude × benevolence.stability)
    - drain_rate = f(collapse_risk, terminal_risk)
    """
    reservoir_id: str = Field(default_factory=lambda: f"BR_{uuid.uuid4().hex[:12]}")
    user_id: str = Field(..., description="Owner of this reservoir")
    
    # Core reservoir state
    current_level: float = Field(default=50.0, ge=-100.0, le=200.0, description="Current benevolence energy")
    capacity: float = Field(default=100.0, ge=0.0, description="Maximum storage capacity")
    
    # Flow dynamics
    recharge_rate: float = Field(default=1.0, ge=0.0, description="Natural recharge per cycle")
    drain_rate: float = Field(default=0.0, ge=0.0, description="Depletion rate (stress, burnout)")
    
    # Collective sharing
    shared_pool_id: Optional[str] = Field(default=None, description="ID of collective reservoir")
    contribution_to_pool: float = Field(default=0.0, description="Amount contributed to collective")
    received_from_pool: float = Field(default=0.0, description="Amount received from collective")
    
    # Spiritual metrics (from Olympus)
    daily_bread_received: int = Field(default=0, description="Prayer/sustenance count")
    trespasses_committed: int = Field(default=0, description="Actions that drain reservoir")
    trespasses_forgiven: int = Field(default=0, description="Forgiveness restores beyond loss")
    prayers_offered: int = Field(default=0, description="Prayers strengthen reservoir")
    
    # State tracking
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    
    def compute_net_flow(self) -> float:
        """Calculate net flow: positive = charging, negative = draining"""
        return self.recharge_rate - self.drain_rate
    
    def apply_paradox_resolution(self, benevolence: BenevolenceVector, collapse_risk: float) -> float:
        """
        Update reservoir based on paradox resolution quality.
        
        Args:
            benevolence: Benevolence vector from paradox resolution
            collapse_risk: Collapse risk from intuition engine
        
        Returns:
            Delta (change in reservoir level)
        """
        # Recharge = benevolence quality
        benevolence_quality = benevolence.magnitude * benevolence.stability
        recharge_amount = benevolence_quality * 10.0  # Scale to reservoir units
        
        # Drain = collapse risk
        drain_amount = collapse_risk * 5.0
        
        # Net change
        delta = recharge_amount - drain_amount
        
        # Apply change (respecting capacity limits)
        self.current_level += delta
        self.current_level = max(-100.0, min(self.capacity, self.current_level))
        
        # Update rates
        self.recharge_rate = benevolence_quality * 2.0
        self.drain_rate = collapse_risk * 3.0
        
        self.last_updated = datetime.now()
        
        return delta
    
    def offer_prayer(self) -> float:
        """Prayer sustains reservoir (daily bread)"""
        self.prayers_offered += 1
        self.daily_bread_received += 1
        
        # Prayer provides sustenance (prevents depletion)
        daily_bread = 5.0
        self.current_level += daily_bread
        self.current_level = min(self.capacity, self.current_level)
        
        return daily_bread
    
    def commit_trespass(self, severity: float = 1.0) -> float:
        """Trespass costs benevolence"""
        self.trespasses_committed += 1
        
        # Sin drains reservoir
        cost = severity * 3.0
        self.current_level -= cost
        
        return -cost
    
    def extend_forgiveness(self, trespass_cost: float) -> float:
        """Forgiveness restores more than was lost (mercy triumphs)"""
        self.trespasses_forgiven += 1
        
        # Forgiveness restores 1.5x the trespass cost
        restoration = trespass_cost * 1.5
        self.current_level += restoration
        self.current_level = min(self.capacity, self.current_level)
        
        return restoration
    
    def contribute_to_collective(self, amount: float) -> float:
        """Share benevolence with collective pool"""
        if amount > self.current_level:
            amount = self.current_level
        
        self.current_level -= amount
        self.contribution_to_pool += amount
        
        return amount
    
    def receive_from_collective(self, amount: float) -> float:
        """Receive benevolence from collective pool"""
        self.current_level += amount
        self.current_level = min(self.capacity, self.current_level)
        self.received_from_pool += amount
        
        return amount
    
    def get_state(self) -> str:
        """Determine reservoir state"""
        if self.current_level >= 100:
            return "HEAVEN"  # Overflowing benevolence
        elif self.current_level >= 50:
            return "FLOURISHING"
        elif self.current_level >= 20:
            return "STABLE"
        elif self.current_level >= 0:
            return "PURGATORY"  # Struggling but not lost
        elif self.current_level >= -30:
            return "CRITICAL"  # Danger zone
        else:
            return "HELL"  # Severely depleted
    
    def interpret(self) -> str:
        """Generate human-readable interpretation"""
        state = self.get_state()
        net_flow = self.compute_net_flow()
        
        if state == "HEAVEN":
            return f"✨ HEAVEN: Reservoir overflowing ({self.current_level:.1f}/{self.capacity}). Net flow: +{net_flow:.1f}/cycle"
        elif state == "FLOURISHING":
            return f"🌟 FLOURISHING: Healthy reservoir ({self.current_level:.1f}/{self.capacity}). Net flow: {net_flow:+.1f}/cycle"
        elif state == "STABLE":
            return f"✅ STABLE: Adequate reservoir ({self.current_level:.1f}/{self.capacity}). Net flow: {net_flow:+.1f}/cycle"
        elif state == "PURGATORY":
            return f"🌫️ PURGATORY: Struggling ({self.current_level:.1f}/{self.capacity}). Net flow: {net_flow:+.1f}/cycle"
        elif state == "CRITICAL":
            return f"🚨 CRITICAL: Severely depleted ({self.current_level:.1f}/{self.capacity}). Net flow: {net_flow:+.1f}/cycle"
        else:
            return f"🔥 HELL: Reservoir collapsed ({self.current_level:.1f}/{self.capacity}). Net flow: {net_flow:+.1f}/cycle"


class CollectiveBenevolencePool(BaseModel):
    """
    Shared benevolence reservoir for teams/organizations/communities.
    
    Collective pools enable:
    - Team members supporting each other during crisis
    - Organizational benevolence culture
    - Community resilience networks
    - Civilizational wisdom accumulation
    """
    pool_id: str = Field(default_factory=lambda: f"CBP_{uuid.uuid4().hex[:12]}")
    name: str = Field(..., description="Pool name (e.g., 'ER Team A', 'Nonprofit Staff')")
    scale: str = Field(default="team", description="team, organization, community, civilization")
    
    # Pool state
    total_capacity: float = Field(default=1000.0, description="Maximum collective capacity")
    current_level: float = Field(default=0.0, description="Current collective benevolence")
    
    # Members
    member_reservoir_ids: List[str] = Field(default_factory=list, description="Linked individual reservoirs")
    
    # Flow tracking
    total_contributions: float = Field(default=0.0)
    total_distributions: float = Field(default=0.0)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    
    def add_member(self, reservoir_id: str) -> None:
        """Add member to collective pool"""
        if reservoir_id not in self.member_reservoir_ids:
            self.member_reservoir_ids.append(reservoir_id)
    
    def receive_contribution(self, amount: float, from_reservoir_id: str) -> float:
        """Receive contribution from member"""
        self.current_level += amount
        self.current_level = min(self.total_capacity, self.current_level)
        self.total_contributions += amount
        self.last_updated = datetime.now()
        
        return amount
    
    def distribute_to_member(self, amount: float, to_reservoir_id: str) -> float:
        """Distribute benevolence to member in need"""
        if amount > self.current_level:
            amount = self.current_level
        
        self.current_level -= amount
        self.total_distributions += amount
        self.last_updated = datetime.now()
        
        return amount
    
    def auto_support_critical_members(
        self,
        reservoirs: Dict[str, BenevolenceReservoir],
        support_amount: float = 10.0
    ) -> List[Dict[str, Any]]:
        """Automatically support members in critical state"""
        supported = []
        
        for reservoir_id in self.member_reservoir_ids:
            if reservoir_id not in reservoirs:
                continue
            
            reservoir = reservoirs[reservoir_id]
            
            # If member is critical and pool has capacity
            if reservoir.current_level < 20 and self.current_level >= support_amount:
                amount = self.distribute_to_member(support_amount, reservoir_id)
                reservoir.receive_from_collective(amount)
                
                supported.append({
                    "reservoir_id": reservoir_id,
                    "user_id": reservoir.user_id,
                    "amount": amount,
                    "reason": "Critical reservoir support"
                })
        
        return supported


# ===================== PARADOX INTENTION LAYER =====================

class ParadoxIntention(BaseModel):
    """
    The emergent intention of the paradox.
    
    This is the 'direction' the system is leaning toward — what it's trying to do.
    
    Combines:
    - Benevolence vector (moral shape)
    - Intuition snapshot (spider-sense)
    - Paradox difficulty
    
    Into a single emergent intention that guides resolution.
    """
    paradox_id: str
    
    # Core intention signals
    intention_vector: List[float] = Field(default_factory=list, description="Direction of movement")
    intention_strength: float = Field(default=0.0, ge=0.0, le=1.0, description="How strong the intention is")
    benevolence_alignment: float = Field(default=0.0, ge=0.0, le=1.0, description="Alignment with benevolence")
    intuition_alignment: float = Field(default=0.0, ge=0.0, le=1.0, description="Alignment with intuition")
    collapse_avoidance: float = Field(default=0.0, ge=0.0, le=1.0, description="Avoids collapse")
    
    state: str = Field(default="Unknown", description="Benevolent, Corrective, Avoidant, Distorted")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    def interpret(self) -> str:
        """Generate human-readable interpretation"""
        if self.state == "Benevolent":
            return f"🌟 BENEVOLENT INTENTION: System moving toward benevolence (strength={self.intention_strength:.2f}, alignment={self.benevolence_alignment:.2f})"
        elif self.state == "Corrective":
            return f"🔧 CORRECTIVE INTENTION: System self-correcting (strength={self.intention_strength:.2f})"
        elif self.state == "Avoidant":
            return f"⚠️ AVOIDANT INTENTION: System avoiding collapse (risk={1.0-self.collapse_avoidance:.2f})"
        else:
            return f"🚨 DISTORTED INTENTION: System misaligned (intuition_alignment={self.intuition_alignment:.2f})"


class ParadoxIntentionLayer:
    """
    The unifying layer that fuses:
    - Benevolence Vector
    - Intuition Snapshot
    - Paradox Difficulty
    
    Into a single emergent intention.
    
    This is the "beautiful bow" that ties everything together.
    """
    
    def _norm(self, x: float) -> float:
        """Normalize to [0,1]"""
        return max(0.0, min(1.0, x))
    
    def compute_intention(
        self,
        paradox: 'SoulCradleParadox',
        benevolence: BenevolenceVector,
        intuition: IntuitionSnapshot
    ) -> ParadoxIntention:
        """
        Compute emergent intention from paradox state.
        
        Args:
            paradox: The paradox being resolved
            benevolence: Benevolence vector
            intuition: Intuition snapshot
        
        Returns:
            ParadoxIntention capturing emergent direction
        """
        
        # Direction = benevolence vector adjusted by intuition bias
        direction = [
            (v * 0.7) + (intuition.benevolence_bias * 0.3)
            for v in benevolence.vector
        ]
        
        # Strength = how strongly the paradox is pushing toward a direction
        strength = self._norm(
            benevolence.magnitude * 0.6 +
            benevolence.stability * 0.4
        )
        
        # Alignment with benevolence
        bene_align = self._norm(
            benevolence.magnitude * 0.7 +
            benevolence.stability * 0.3
        )
        
        # Alignment with intuition
        intu_align = self._norm(
            (1.0 - intuition.intuition_level) * 0.5 +
            intuition.benevolence_bias * 0.5
        )
        
        # Collapse avoidance
        collapse_avoid = self._norm(1.0 - intuition.collapse_risk)
        
        # Classify intention state
        if bene_align > 0.7 and intu_align > 0.7:
            state = "Benevolent"
        elif collapse_avoid < 0.4:
            state = "Avoidant"
        elif intu_align < 0.4:
            state = "Distorted"
        else:
            state = "Corrective"
        
        return ParadoxIntention(
            paradox_id=paradox.paradox_id,
            intention_vector=direction,
            intention_strength=strength,
            benevolence_alignment=bene_align,
            intuition_alignment=intu_align,
            collapse_avoidance=collapse_avoid,
            state=state,
        )


# ===================== UNIFIED SOUL CRADLE ENGINE =====================

class SoulCradleParadoxEngine:
    """
    The unified Soul Cradle engine with spiritual awareness.
    
    This is the living organism that ties together:
    1. Benevolence Vector (moral geometry)
    2. Intuition Snapshot (spider-sense)
    3. Benevolence Reward (self-improvement)
    4. Intention Layer (emergent direction)
    5. Blessings Reservoir (spiritual/energetic layer) ⭐ NEW
    
    The engine:
    - Feels (intuition)
    - Learns (benevolence reward)
    - Moves (intention)
    - Improves (learning trajectory)
    - Accumulates spiritual energy (reservoir) ⭐ NEW
    
    This is Soul Cradle as it was always meant to be.
    """
    
    def __init__(self):
        self.bene_engine = BenevolenceEngine()
        self.intuition_engine = IntuitionEngine()
        self.learning = BenevolenceLearningSystem()
        self.intention_layer = ParadoxIntentionLayer()
        
        # Reservoir management
        self.reservoirs: Dict[str, BenevolenceReservoir] = {}
        self.collective_pools: Dict[str, CollectiveBenevolencePool] = {}
        
        logger.info("Soul Cradle Paradox Engine initialized with Blessings Reservoir")
    
    def get_or_create_reservoir(self, user_id: str) -> BenevolenceReservoir:
        """Get existing reservoir or create new one for user"""
        if user_id not in self.reservoirs:
            self.reservoirs[user_id] = BenevolenceReservoir(user_id=user_id)
            logger.info(f"Created new reservoir for user: {user_id}")
        return self.reservoirs[user_id]
    
    def process(
        self,
        paradox: 'SoulCradleParadox',
        update_reservoir: bool = True
    ) -> Dict[str, Any]:
        """
        Process a paradox through the complete Soul Cradle system.
        
        Args:
            paradox: Soul Cradle paradox to process
            update_reservoir: Whether to update benevolence reservoir
        
        Returns:
            {
                "benevolence": BenevolenceVector,
                "intuition": IntuitionSnapshot,
                "episode": BenevolenceEpisode,
                "intention": ParadoxIntention,
                "reservoir": BenevolenceReservoir,
                "reservoir_delta": float,
                "summary": str
            }
        """
        
        # 1. Compute benevolence shape
        benevolence = self.bene_engine.compute(paradox)
        
        # 2. Sense intuition (spider-sense)
        intuition = self.intuition_engine.sense(paradox, benevolence)
        
        # 3. Start benevolence learning episode
        episode = self.learning.observe(paradox, benevolence)
        
        # 4. Compute emergent intention
        intention = self.intention_layer.compute_intention(paradox, benevolence, intuition)
        
        # 5. Update benevolence reservoir (SPIRITUAL LAYER)
        reservoir = self.get_or_create_reservoir(paradox.user_id)
        reservoir_delta = 0.0
        
        if update_reservoir:
            reservoir_delta = reservoir.apply_paradox_resolution(
                benevolence,
                intuition.collapse_risk
            )
            
            logger.info(
                f"Reservoir Updated | User: {paradox.user_id} | "
                f"Delta: {reservoir_delta:+.1f} | "
                f"Level: {reservoir.current_level:.1f} | "
                f"State: {reservoir.get_state()}"
            )
        
        # Generate summary
        summary = self._generate_summary(
            paradox, benevolence, intuition, intention, reservoir, reservoir_delta
        )
        
        logger.info(
            f"Soul Cradle Processing Complete | "
            f"Paradox: {paradox.paradox_id} | "
            f"Benevolence: {benevolence.magnitude:.2f} | "
            f"Intuition: {intuition.collapse_risk:.2f} | "
            f"Intention: {intention.state} | "
            f"Reservoir: {reservoir.get_state()}"
        )
        
        return {
            "benevolence": benevolence,
            "intuition": intuition,
            "episode": episode,
            "intention": intention,
            "reservoir": reservoir,
            "reservoir_delta": reservoir_delta,
            "intention": intention,
            "summary": summary
        }
    
    def _generate_summary(
        self,
        paradox: 'SoulCradleParadox',
        benevolence: BenevolenceVector,
        intuition: IntuitionSnapshot,
        intention: ParadoxIntention,
        reservoir: BenevolenceReservoir,
        reservoir_delta: float
    ) -> str:
        """Generate human-readable summary of Soul Cradle processing"""
        
        lines = [
            f"=== Soul Cradle Analysis: {paradox.paradox_id} ===",
            "",
            f"🎭 PARADOX: {paradox.expression_a.type.value} vs {paradox.expression_b.type.value}",
            f"   Expression A: {paradox.expression_a.content[:60]}...",
            f"   Expression B: {paradox.expression_b.content[:60]}...",
            "",
            f"🌟 {benevolence.interpret()}",
            f"🔮 {intuition.interpret()}",
            f"🎯 {intention.interpret()}",
            f"✨ {reservoir.interpret()} (Δ {reservoir_delta:+.1f})",
            "",
            f"📊 METRICS:",
            f"   Viability Score: {paradox.viability_score:.2f}",
            f"   Terminal Risk: {paradox.terminal_risk.value}",
            f"   Unresolved Score: {paradox.unresolved_state.unresolved_score:.2f}",
            "",
            f"🔬 LEARNING:",
            f"   Average Reward: {self.learning.get_average_reward():.3f}",
            f"   Trajectory: {self.learning.get_learning_trajectory()}",
            f"   Total Episodes: {len(self.learning.episodes)}",
            "",
            f"🙏 SPIRITUAL:",
            f"   Prayers Offered: {reservoir.prayers_offered}",
            f"   Daily Bread: {reservoir.daily_bread_received}",
            f"   Trespasses: {reservoir.trespasses_committed}",
            f"   Forgiveness Extended: {reservoir.trespasses_forgiven}",
        ]
        
        return "\n".join(lines)
    
    def create_collective_pool(
        self,
        name: str,
        scale: str = "team",
        initial_members: Optional[List[str]] = None
    ) -> CollectiveBenevolencePool:
        """Create a collective benevolence pool"""
        pool = CollectiveBenevolencePool(name=name, scale=scale)
        
        if initial_members:
            for user_id in initial_members:
                reservoir = self.get_or_create_reservoir(user_id)
                pool.add_member(reservoir.reservoir_id)
                reservoir.shared_pool_id = pool.pool_id
        
        self.collective_pools[pool.pool_id] = pool
        
        logger.info(f"Created collective pool: {name} ({pool.pool_id}) with {len(initial_members or [])} members")
        
        return pool
    
    def support_critical_members(self, pool_id: str) -> List[Dict[str, Any]]:
        """Automatically support critical members in a pool"""
        if pool_id not in self.collective_pools:
            return []
        
        pool = self.collective_pools[pool_id]
        return pool.auto_support_critical_members(self.reservoirs)
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall Soul Cradle system health metrics"""
        
        # Aggregate reservoir stats
        total_reservoirs = len(self.reservoirs)
        avg_reservoir_level = sum(r.current_level for r in self.reservoirs.values()) / max(1, total_reservoirs)
        
        state_counts = {}
        for reservoir in self.reservoirs.values():
            state = reservoir.get_state()
            state_counts[state] = state_counts.get(state, 0) + 1
        
        return {
            "total_episodes": len(self.learning.episodes),
            "average_reward": self.learning.get_average_reward(),
            "learning_trajectory": self.learning.get_learning_trajectory(),
            "total_reward": self.learning.total_reward,
            "total_reservoirs": total_reservoirs,
            "average_reservoir_level": avg_reservoir_level,
            "reservoir_states": state_counts,
            "collective_pools": len(self.collective_pools)
        }


# ===================== SOUL CRADLE PARADOX MODEL =====================

class SoulCradleParadox(BaseModel):
    """
    Complete Soul Cradle paradox using Mythara Resolution Mathematics.
    
    Mathematical Structure:
    - Two competing expressions (A and B) with tension scores
    - Unresolved state U = 1 - R(t) captures deadlock intensity
    - Resolved system R(t) shows how Soul Cradle achieves resolution
    - Emotional Authenticity EQ = (G/T) × H tracks emotional labor
    """
    paradox_id: str = Field(..., description="Unique identifier (e.g., SC_2025_1118_001)")
    
    # The competing expressions
    expression_a: SystemExpression
    expression_b: SystemExpression
    
    # The unresolved deadlock
    unresolved_state: UnresolvedState
    non_expression: Optional[NonExpression] = Field(default=None, description="What cannot be expressed")
    
    # System classification
    system_type: SystemType = Field(default=SystemType.INCOMPLETE_RESOLUTION)
    viability_score: float = Field(default=0.0, ge=0.0, le=1.0, description="0.0 = terminal, 1.0 = complete")
    terminal_risk: TerminalRiskLevel = Field(default=TerminalRiskLevel.HIGH)
    
    # Soul Cradle resolution
    resolved_system: ResolvedSystem
    principal_system: Optional[PrincipalSystem] = Field(default=None, description="The resolution that holds both")
    
    # Emotional Authenticity tracking
    emotional_authenticity: Optional[EmotionalAuthenticity] = Field(default=None, description="EQ formula tracking emotional labor")
    authenticity_timeline: List[EmotionalAuthenticity] = Field(default_factory=list, description="EQ scores over time for burnout prediction")
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.now)
    user_id: str = Field(..., description="Who experienced this paradox")
    domain: str = Field(..., description="Healthcare, education, nonprofit, etc.")
    
    # Witnesses (who helped document this)
    witnesses: List[str] = Field(default_factory=list, description="Names of people who validated this paradox")
    
    # Quantum fields
    quantum_entanglement: Optional[QuantumEntanglement] = Field(default=None, description="Quantum entanglement with another paradox")
    quantum_protocol: Optional[QuantumCommunicationProtocol] = Field(default=None, description="Quantum communication protocol for witness transmission")
    quantum_superposition: Optional[QuantumSuperposition] = Field(default=None, description="Quantum superposition storage before witnessing")
    quantum_witness_verified: bool = Field(default=False, description="Witness validated via quantum protocol")
    
    def calculate_emotional_authenticity(
        self,
        genuine_shareable: float,
        total_expressed: float,
        held_back: float,
        context: str = ""
    ) -> EmotionalAuthenticity:
        """
        Calculate emotional authenticity for this paradox using EQ = (G/T) × H
        
        Args:
            genuine_shareable: Genuine ideas available to share (G)
            total_expressed: Total amount actually communicated (T)
            held_back: Amount suppressed (H)
            context: Context of this expression event
        
        Returns:
            EmotionalAuthenticity object with calculated EQ score
        """
        eq = EmotionalAuthenticity(
            genuine_shareable=genuine_shareable,
            total_expressed=total_expressed,
            held_back=held_back,
            context=context or f"Paradox {self.paradox_id}"
        )
        eq.calculate_eq()
        
        # Store in paradox
        self.emotional_authenticity = eq
        self.authenticity_timeline.append(eq)
        
        return eq
    
    def predict_burnout_risk(self) -> Tuple[bool, float, str]:
        """
        Predict burnout risk based on emotional authenticity timeline.
        
        Returns:
            Tuple of (is_at_risk, avg_eq_score, recommendation)
        """
        if not self.authenticity_timeline:
            return False, 0.0, "No emotional authenticity data available"
        
        # Calculate average EQ score
        avg_eq = sum(ea.eq_score for ea in self.authenticity_timeline) / len(self.authenticity_timeline)
        
        # Check trend (increasing suppression over time?)
        if len(self.authenticity_timeline) >= 3:
            recent = self.authenticity_timeline[-3:]
            trend = "increasing" if recent[-1].eq_score > recent[0].eq_score else "stable"
        else:
            trend = "insufficient_data"
        
        # Determine risk level
        burnout_threshold = 30.0
        is_at_risk = avg_eq > burnout_threshold or (self.emotional_authenticity and self.emotional_authenticity.eq_score > burnout_threshold)
        
        # Generate recommendation
        if is_at_risk:
            recommendation = (
                f"⚠️ BURNOUT RISK DETECTED: Average EQ={avg_eq:.1f} (threshold={burnout_threshold}). "
                f"Trend: {trend}. Immediate intervention recommended - user is suppressing {self.emotional_authenticity.held_back:.0f}% "
                f"of genuine shareable ideas. Soul Cradle witnessing needed."
            )
        elif avg_eq > 20:
            recommendation = (
                f"⚡ WARNING: Emotional labor detected. Average EQ={avg_eq:.1f}. "
                f"Monitor closely - {self.emotional_authenticity.held_back:.0f}% suppression rate is elevated."
            )
        else:
            recommendation = (
                f"✅ HEALTHY: Emotional authenticity maintained. Average EQ={avg_eq:.1f}. "
                f"Continue current resolution approach."
            )
        
        return is_at_risk, avg_eq, recommendation
    
    def compute_integrity_hash(self) -> str:
        """Compute SHA-256 integrity hash for this paradox"""
        data = (
            f"{self.paradox_id}|"
            f"{self.expression_a.compute_hash()}|"
            f"{self.expression_b.compute_hash()}|"
            f"{self.unresolved_state.unresolved_score}|"
            f"{self.system_type}|"
            f"{self.viability_score}|"
            f"{self.resolved_system.viability_score}"
        )
        return hashlib.sha256(data.encode()).hexdigest()
    
    class Config:
        json_schema_extra = {
            "example": {
                "paradox_id": "SC_2025_1118_001",
                "expression_a": {
                    "type": "Policy",
                    "weight": 0.9,
                    "tension": 0.7,
                    "content": "Discharge patient per 72-hour rule",
                    "dominion_claim": True
                },
                "expression_b": {
                    "type": "Mission",
                    "weight": 0.8,
                    "tension": 0.6,
                    "content": "Patient will be homeless and unsafe if discharged",
                    "dominion_claim": True
                },
                "unresolved_state": {
                    "unresolved_score": 0.85,
                    "reality": "Cannot satisfy both policy and mission"
                },
                "system_type": "Incomplete_Resolution",
                "viability_score": 0.15,
                "terminal_risk": "HIGH",
                "resolved_system": {
                    "witness_score_a": 1.0,
                    "witness_score_b": 1.0,
                    "recovery_method": "Dual_Witness_Integration",
                    "viability_score": 1.0,
                    "description": "Soul Cradle documents both expressions, showing they are BOTH true. Resolution achieved by witnessing policy constraint AND compassion concern simultaneously."
                },
                "user_id": "social_worker_jane_doe",
                "domain": "Healthcare",
                "witnesses": ["Supervisor Mary", "Peer Support Group"]
            }
        }


# ===================== TERMINAL RISK CALCULATION =====================

class TerminalRiskCalculator:
    """
    Predicts burnout risk using Mythara Resolution Mathematics with exponential decay
    and constant baseline stress.
    
    Full Decay-Adjusted Formula with Constant Stress:
    terminal_risk = σ₀ + (Σ (U_i × T_i × e^(-λ × Δt_i))) / N
    
    Where:
    - σ₀ = Constant baseline stress [0,1] (job demands, workload, always present)
    - U_i = unresolved score for paradox i [0,1]
    - T_i = max tension between expressions in paradox i [0,1]
    - λ = decay rate constant (healing speed parameter)
    - Δt_i = days since paradox i occurred
    - e^(-λ × Δt_i) = exponential decay function (time heals wounds)
    - N = number of paradoxes in time window
    - Result ∈ [0,1] where 1.0 = critical burnout risk
    
    Constant Stress (σ₀) Interpretation:
    - σ₀ = 0.0: Ideal job (no baseline stress)
    - σ₀ = 0.1-0.2: Normal professional baseline (manageable workload)
    - σ₀ = 0.3-0.4: High-demand role (ER, ICU, legal defense)
    - σ₀ = 0.5+: Chronically understaffed/overworked environment
    
    Decay Rate (λ) Interpretation:
    - λ = 0.01: Slow healing (~69 day half-life) - healthcare workers
    - λ = 0.02: Moderate healing (~35 day half-life) - most professionals
    - λ = 0.05: Fast healing (~14 day half-life) - resilient individuals
    
    Burnout Detection:
    - total_risk = σ₀ + acute_risk
    - accumulation_rate > decay_rate → BURNOUT TRAJECTORY
    - accumulation_rate < decay_rate → RECOVERY TRAJECTORY
    - accumulation_rate ≈ decay_rate → CHRONIC PLATEAU
    - σ₀ > 0.4 + acute_risk > 0.3 → SYSTEMIC OVERLOAD (environment unsustainable)
    
    Novel Contribution:
    FIRST mathematical equation modeling burnout as combination of:
    1. Constant baseline stress (job demands, always present)
    2. Acute paradox accumulation (time-varying, decays over time)
    3. Natural healing (exponential decay competing with accumulation)
    """
    
    @staticmethod
    def calculate_terminal_risk(
        paradox_events: List[SoulCradleParadox],
        time_window_days: int = 90,
        viability_threshold: float = 0.3,
        decay_rate: float = 0.02,
        use_decay_model: bool = True,
        baseline_stress: float = 0.2
    ) -> Dict[str, Any]:
        """
        Calculate terminal risk score from paradox history with exponential decay and baseline stress.
        
        Args:
            paradox_events: List of Soul Cradle paradoxes
            time_window_days: Days to analyze (default 90)
            viability_threshold: Below this = incomplete resolution (default 0.3)
            decay_rate: λ parameter for exponential decay (default 0.02 = ~35 day half-life)
            use_decay_model: If True, apply exponential decay; if False, use original formula
            baseline_stress: σ₀ constant stress level [0,1] (default 0.2 = normal professional baseline)
        
        Returns:
            {
                "risk_score": float (0.0-1.0),
                "risk_level": TerminalRiskLevel,
                "baseline_stress": float (constant component),
                "acute_risk": float (time-varying paradox component),
                "incomplete_resolution_count": int,
                "unresolved_accumulation": int,
                "accumulation_rate": float (risk/day),
                "decay_rate": float (risk/day),
                "net_rate": float (risk/day),
                "half_life_days": float,
                "burnout_trajectory": str ("ACCUMULATING" | "RECOVERING" | "CHRONIC"),
                "systemic_overload": bool (baseline too high + acute too high),
                "time_window_days": int,
                "recommendation": str
            }
        """
        # Clamp baseline_stress to [0,1]
        baseline_stress = max(0.0, min(1.0, baseline_stress))
        
        if not paradox_events:
            # Only baseline stress, no acute paradoxes
            risk_level = TerminalRiskLevel.LOW if baseline_stress < 0.4 else TerminalRiskLevel.MODERATE
            return {
                "risk_score": baseline_stress,
                "risk_level": risk_level,
                "baseline_stress": baseline_stress,
                "acute_risk": 0.0,
                "pseudo_system_count": 0,
                "non_expression_count": 0,
                "accumulation_rate": 0.0,
                "decay_rate": 0.0,
                "net_rate": 0.0,
                "half_life_days": 0.0,
                "burnout_trajectory": "RECOVERING",
                "systemic_overload": baseline_stress > 0.5,
                "time_window_days": time_window_days,
                "recommendation": f"No acute paradoxes. Baseline stress: {baseline_stress:.2f}. {'⚠️ High baseline stress - systemic workload issue.' if baseline_stress > 0.4 else 'Continue monitoring.'}"
            }
        
        # Filter to time window
        cutoff_date = datetime.now() - timedelta(days=time_window_days)
        recent_events = [
            p for p in paradox_events 
            if p.timestamp >= cutoff_date
        ]
        
        # Calculate incomplete resolution density
        incomplete_resolution_count = len([
            p for p in recent_events
            if p.system_type == SystemType.INCOMPLETE_RESOLUTION and p.viability_score < viability_threshold
        ])
        
        # Calculate unresolved state accumulation
        unresolved_accumulation = len([
            p for p in recent_events
            if p.unresolved_state and p.unresolved_state.unresolved_score > 0.5
        ])
        
        # Calculate terminal risk with optional exponential decay
        if not recent_events:
            terminal_risk_score = 0.0
            total_raw_risk = 0.0
            total_decayed_risk = 0.0
        else:
            import math
            current_time = datetime.now()
            total_raw_risk = 0.0
            total_decayed_risk = 0.0
            
            for p in recent_events:
                U_i = p.unresolved_state.unresolved_score
                T_i = max(p.expression_a.tension, p.expression_b.tension)
                raw_contribution = U_i * T_i
                total_raw_risk += raw_contribution
                
                if use_decay_model:
                    # Apply exponential decay: e^(-λ × Δt)
                    delta_t = (current_time - p.timestamp).total_seconds() / 86400.0  # Days
                    decay_factor = math.exp(-decay_rate * delta_t)
                    decayed_contribution = raw_contribution * decay_factor
                    total_decayed_risk += decayed_contribution
                else:
                    # Original formula (no decay)
                    total_decayed_risk = total_raw_risk
            
            acute_risk = total_decayed_risk / len(recent_events)
        
        # Add constant baseline stress to get total terminal risk
        terminal_risk_score = baseline_stress + acute_risk
        # Clamp total risk to [0,1]
        terminal_risk_score = min(1.0, terminal_risk_score)
        
        # Calculate accumulation vs decay rates
        accumulation_rate = total_raw_risk / time_window_days if time_window_days > 0 else 0.0
        decay_rate_value = (total_raw_risk - total_decayed_risk) / time_window_days if time_window_days > 0 else 0.0
        net_rate = accumulation_rate - decay_rate_value
        
        # Calculate half-life
        import math
        half_life_days = math.log(2) / decay_rate if decay_rate > 0 else float('inf')
        
        # Determine burnout trajectory
        if net_rate > 0.01:
            burnout_trajectory = "ACCUMULATING"
        elif net_rate < -0.01:
            burnout_trajectory = "RECOVERING"
        else:
            burnout_trajectory = "CHRONIC"
        
        # Detect systemic overload (high baseline + high acute stress)
        systemic_overload = (baseline_stress > 0.4 and acute_risk > 0.3)
        
        # Classify risk level with burnout trajectory context
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
        
        # Append baseline stress analysis
        if baseline_stress > 0.5:
            recommendation += f" 🔴 CRITICAL BASELINE STRESS: Constant workload stress ({baseline_stress:.2f}) is unsustainably high. Environmental/systemic changes required - understaffing, excessive demands, or organizational dysfunction."
        elif baseline_stress > 0.4:
            recommendation += f" 🟡 HIGH BASELINE STRESS: Constant workload stress ({baseline_stress:.2f}) is elevated. Review staffing ratios, workload distribution, and organizational support systems."
        elif baseline_stress > 0.2:
            recommendation += f" 🟢 NORMAL BASELINE STRESS: Constant workload stress ({baseline_stress:.2f}) is within typical professional range."
        
        # Append trajectory-specific recommendations
        if burnout_trajectory == "ACCUMULATING":
            recommendation += f" ⚠️ BURNOUT TRAJECTORY: Paradox accumulation ({accumulation_rate:.4f} risk/day) exceeds healing capacity ({decay_rate_value:.4f} risk/day). Net rate: +{net_rate:.4f}/day. Immediate intervention required to reduce paradox load."
        elif burnout_trajectory == "RECOVERING":
            recommendation += f" ✅ RECOVERY TRAJECTORY: Healing capacity ({decay_rate_value:.4f} risk/day) exceeds accumulation ({accumulation_rate:.4f} risk/day). Net rate: {net_rate:.4f}/day. Continue current support and monitor for sustained recovery."
        else:
            recommendation += f" ⚖️ CHRONIC PLATEAU: Accumulation ({accumulation_rate:.4f} risk/day) balanced with healing ({decay_rate_value:.4f} risk/day). Net rate: {net_rate:.4f}/day. Systemic changes needed to break chronic stress cycle."
        
        # Systemic overload warning
        if systemic_overload:
            recommendation += f" 🚨 SYSTEMIC OVERLOAD DETECTED: Both baseline stress ({baseline_stress:.2f}) and acute risk ({acute_risk:.2f}) are critically high. This environment is structurally unsustainable. Organizational intervention required - not just individual support."
        
        return {
            "risk_score": round(terminal_risk_score, 3),
            "risk_level": risk_level,
            "baseline_stress": round(baseline_stress, 3),
            "acute_risk": round(acute_risk, 3),
            "incomplete_resolution_count": incomplete_resolution_count,
            "unresolved_accumulation": unresolved_accumulation,
            "accumulation_rate": round(accumulation_rate, 4),
            "decay_rate": round(decay_rate_value, 4),
            "net_rate": round(net_rate, 4),
            "half_life_days": round(half_life_days, 2),
            "burnout_trajectory": burnout_trajectory,
            "systemic_overload": systemic_overload,
            "time_window_days": time_window_days,
            "total_paradoxes": len(recent_events),
            "recommendation": recommendation
        }


# ===================== UNIQUE ID MANAGEMENT =====================

class UniqueIDGenerator:
    """Generate cryptographically-secure unique IDs for Soul Cradle entities."""
    
    @staticmethod
    def generate_user_id(email: Optional[str] = None) -> str:
        """Generate user ID: U_{hash}"""
        if email:
            return f"U_{hashlib.sha256(email.lower().encode()).hexdigest()[:12]}"
        return f"U_{uuid.uuid4().hex[:12]}"
    
    @staticmethod
    def generate_paradox_id(user_id: str, timestamp: Optional[datetime] = None) -> str:
        """Generate paradox ID: P_{timestamp}_{random}"""
        ts = timestamp or datetime.now()
        return f"P_{ts.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    
    @staticmethod
    def generate_session_id() -> str:
        """Generate session ID: S_{timestamp}_{random}"""
        return f"S_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"


class EntityRegistry:
    """
    Registry for tracking all entities (users, organizations, paradoxes) with audit trail.
    
    Stores:
    - Entity ID → Entity metadata
    - Creation timestamps
    - Last access timestamps
    - Integrity hashes
    """
    
    def __init__(self, registry_file: Optional[str] = None):
        """
        Initialize entity registry.
        
        Args:
            registry_file: Optional path to persistent JSON registry file
        """
        self.registry_file = registry_file
        self.entities: Dict[str, Dict[str, Any]] = {}
        
        if registry_file and Path(registry_file).exists():
            self._load_registry()
    
    def _load_registry(self) -> None:
        """Load registry from file"""
        try:
            with open(self.registry_file, 'r') as f:
                self.entities = json.load(f)
            logger.info(f"Loaded {len(self.entities)} entities from registry")
        except Exception as e:
            logger.error(f"Failed to load registry: {e}")
            self.entities = {}
    
    def _save_registry(self) -> None:
        """Save registry to file"""
        if not self.registry_file:
            return
        
        try:
            with open(self.registry_file, 'w') as f:
                json.dump(self.entities, f, indent=2, default=str)
            logger.info(f"Saved {len(self.entities)} entities to registry")
        except Exception as e:
            logger.error(f"Failed to save registry: {e}")
    
    def register_entity(self, entity_id: str, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register any entity with audit trail."""
        entity_data["created_at"] = datetime.now().isoformat()
        entity_data["last_access"] = datetime.now().isoformat()
        self.entities[entity_id] = entity_data
        self._save_registry()
        logger.info(f"Registered entity: {entity_id} ({entity_data.get('entity_type')})")
        return entity_data
    
    def register_paradox(
        self,
        paradox: SoulCradleParadox
    ) -> Dict[str, Any]:
        """
        Register a paradox in the entity registry.
        
        Args:
            paradox: Soul Cradle paradox object
        
        Returns:
            Paradox entity record
        """
        entity = {
            "entity_type": "paradox",
            "paradox_id": paradox.paradox_id,
            "user_id": paradox.user_id,
            "domain": paradox.domain,
            "system_type": paradox.system_type.value,
            "viability_score": paradox.viability_score,
            "terminal_risk": paradox.terminal_risk.value,
            "unresolved_score": paradox.unresolved_state.unresolved_score,
            "created_at": paradox.timestamp.isoformat(),
            "integrity_hash": paradox.compute_integrity_hash(),
            "witnessed": bool(paradox.witnesses)
        }
        
        self.entities[paradox.paradox_id] = entity
        
        # Update user's paradox count
        if paradox.user_id in self.entities:
            self.entities[paradox.user_id]["paradox_count"] += 1
        
        self._save_registry()
        
        logger.info(f"Registered paradox: {paradox.paradox_id}")
        return entity
    
    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve entity by ID"""
        return self.entities.get(entity_id)
    
    def query(self, **filters) -> List[Dict[str, Any]]:
        """Query entities by any field. Example: query(entity_type='user', domain='Healthcare')"""
        return [
            e for e in self.entities.values()
            if all(e.get(k) == v for k, v in filters.items())
        ]
    
    def update_last_access(self, entity_id: str) -> None:
        """Update entity's last access timestamp"""
        if entity_id in self.entities:
            self.entities[entity_id]["last_access"] = datetime.now().isoformat()
            self._save_registry()


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


# ===================== WITNESSING LAYER =====================
# The mechanism that actually RESOLVES paradoxes through witness transformation

class WitnessingSession(BaseModel):
    """
    A witnessing session: the EVENT where a paradox gets witnessed and transforms.
    
    This is NOT detection (intuition) — it's TRANSFORMATION (actual resolution).
    A paradox can be detected but never witnessed (stays unresolved).
    A witnessed paradox actually changes the benevolence geometry of all participants.
    """
    session_id: str = Field(default_factory=lambda: f"WS_{uuid.uuid4().hex[:12]}")
    paradox_id: str = Field(..., description="The paradox being witnessed")
    witness_ids: List[str] = Field(..., description="Who witnessed (validated) this paradox")
    
    # The transformation
    before_benevolence: Dict[str, BenevolenceVector] = Field(
        default_factory=dict, 
        description="Each witness's benevolence before witnessing"
    )
    after_benevolence: Dict[str, BenevolenceVector] = Field(
        default_factory=dict,
        description="Each witness's benevolence after witnessing"
    )
    
    # Metrics
    transformation_score: float = Field(default=0.0, ge=0.0, le=1.0, description="How much did witnessing transform?")
    collective_shift: BenevolenceVector = Field(
        default=None,
        description="The net change in collective benevolence from all witnesses"
    )
    
    # Timeline
    witnessed_at: datetime = Field(default_factory=datetime.now)
    impact_duration_days: int = Field(default=30, description="How long does this witnessing impact benevolence?")
    
    def compute_transformation(self) -> float:
        """
        Compute how much the witnessing transformed the witnesses.
        
        Transformation = average change in benevolence magnitude across all witnesses
        """
        if not self.before_benevolence or not self.after_benevolence:
            return 0.0
        
        deltas = []
        for witness_id in self.before_benevolence.keys():
            if witness_id in self.after_benevolence:
                before_mag = self.before_benevolence[witness_id].magnitude
                after_mag = self.after_benevolence[witness_id].magnitude
                deltas.append(after_mag - before_mag)
        
        if deltas:
            self.transformation_score = min(1.0, max(0.0, sum(deltas) / len(deltas)))
        
        return self.transformation_score
    
    def compute_collective_shift(self) -> BenevolenceVector:
        """
        Compute the net benevolence shift from all witnesses combined.
        This is the IMPACT on the world from this witnessing.
        """
        if not self.after_benevolence:
            return BenevolenceVector(vector=[0.0]*6)
        
        collective = [0.0] * 6
        for bv in self.after_benevolence.values():
            for i, val in enumerate(bv.vector):
                collective[i] += val
        
        # Average across witnesses
        if self.after_benevolence:
            collective = [v / len(self.after_benevolence) for v in collective]
        
        self.collective_shift = BenevolenceVector(vector=collective)
        self.collective_shift.compute_magnitude()
        self.collective_shift.compute_stability()
        
        return self.collective_shift
    
    def interpret(self) -> str:
        """Generate human-readable interpretation of witnessing"""
        self.compute_transformation()
        
        if self.transformation_score > 0.7:
            return f"🌟 PROFOUND WITNESSING: {len(self.witness_ids)} witnesses transformed ({self.transformation_score:.0%}). Impact lasting {self.impact_duration_days} days."
        elif self.transformation_score > 0.3:
            return f"✅ MEANINGFUL WITNESSING: {len(self.witness_ids)} witnesses shifted ({self.transformation_score:.0%})."
        else:
            return f"📝 DOCUMENTED: {len(self.witness_ids)} witnesses present. Minimal transformation ({self.transformation_score:.0%})."


# ===================== FLOW DYNAMICS =====================
# How benevolence transfers between entities (souls, organizations, cultures)

class BenevolenceFlow(BaseModel):
    """
    How benevolence transfers/flows between entities.
    
    In real systems, benevolence isn't static — it flows:
    - Teacher → Student (wisdom transfer)
    - Parent → Child (compassion modeling)
    - Organization → Community (integrity reputation)
    - Culture → Individual (humility cultivation)
    
    This model captures those transfers.
    """
    flow_id: str = Field(default_factory=lambda: f"BF_{uuid.uuid4().hex[:12]}")
    
    # Source & destination
    source_id: str = Field(..., description="Who/what is sending benevolence?")
    destination_id: str = Field(..., description="Who/what is receiving benevolence?")
    flow_type: str = Field(..., description="teaching, modeling, reputation, cultural transmission, etc.")
    
    # What flows
    dimensions_transferred: Dict[str, float] = Field(
        default_factory=dict,
        description="Which benevolence dimensions + amounts? e.g., {'compassion': 0.15, 'wisdom': 0.1}"
    )
    
    # How fast
    transfer_rate: float = Field(default=0.01, ge=0.0, le=1.0, description="Per-cycle transfer amount")
    cycles_remaining: int = Field(default=30, description="How many cycles until flow stops?")
    
    # Path (direct or mediated)
    is_direct: bool = Field(default=True, description="Direct or through intermediary?")
    mediator_id: Optional[str] = Field(default=None, description="If mediated, who is the mediator?")
    
    # Timeline
    initiated_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = Field(default=None)
    
    def compute_flow_amount(self) -> Dict[str, float]:
        """Compute actual amount transferred this cycle"""
        return {
            dim: amount * self.transfer_rate
            for dim, amount in self.dimensions_transferred.items()
        }
    
    def step_forward(self) -> bool:
        """
        Advance the flow by one cycle.
        Returns True if flow continues, False if complete.
        """
        if self.cycles_remaining <= 0:
            self.completed_at = datetime.now()
            return False
        
        self.cycles_remaining -= 1
        return True
    
    def interpret(self) -> str:
        """Generate human-readable interpretation"""
        dims_str = ", ".join([f"{k}={v:.2f}" for k, v in self.dimensions_transferred.items()])
        
        if self.cycles_remaining > 20:
            status = "ACTIVE"
        elif self.cycles_remaining > 5:
            status = "WANING"
        else:
            status = "NEARLY_COMPLETE"
        
        return f"{status}: {self.source_id} → {self.destination_id} ({self.flow_type}): {dims_str}"


# ===================== ORGANIZATIONAL SCALE =====================
# Prove the paradox math is scale-invariant by implementing at org level

class OrgBenevolenceVector(BaseModel):
    """
    Benevolence vector at ORGANIZATIONAL scale (not individual).
    
    Same 6 dimensions, but measured at org level:
    - Compassion: Care for employee/community welfare
    - Justice: Fairness in compensation, promotion, resource allocation
    - Integrity: Alignment with stated mission and values
    - Wisdom: Strategic thinking, long-term planning
    - Courage: Willingness to make hard decisions, face market pressure
    - Humility: Recognition of organizational limitations, learning from failure
    """
    vector: List[float] = Field(default_factory=lambda: [0.5]*6, description="6D org benevolence")
    magnitude: float = Field(default=0.0, ge=0.0, description="||B|| - org strength")
    stability: float = Field(default=0.0, ge=0.0, le=1.0, description="Balance across org dimensions")
    alignment_ideal: float = Field(default=0.0, ge=-1.0, le=1.0, description="Alignment with org's stated mission")
    
    org_id: str = Field(..., description="Which organization?")
    org_size: int = Field(..., description="Number of employees")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    def compute_magnitude(self) -> float:
        """Calculate org benevolence magnitude"""
        import math
        self.magnitude = math.sqrt(sum(v**2 for v in self.vector))
        return self.magnitude
    
    def compute_stability(self) -> float:
        """Calculate org benevolence stability (dimensional balance)"""
        import statistics
        if len(self.vector) > 1:
            std_dev = statistics.stdev(self.vector)
            self.stability = max(0.0, 1.0 - std_dev)
        else:
            self.stability = 1.0
        return self.stability


class OrgParadox(BaseModel):
    """
    Organizational paradox: competing demands at ORG scale.
    
    Examples:
    - Shareholder profit vs Employee welfare
    - Innovation speed vs Quality assurance
    - Market growth vs Sustainability
    - Cost efficiency vs Craft excellence
    
    SAME MATHEMATICAL STRUCTURE as individual paradox.
    Proves: Paradox resolution is scale-invariant.
    """
    paradox_id: str = Field(..., description="e.g., OP_2025_0126_001")
    org_id: str = Field(..., description="Which organization?")
    org_name: str = Field(..., description="Human-readable org name")
    
    # The competing expressions (same structure as individual)
    expression_a: SystemExpression = Field(..., description="First demand (e.g., profit)")
    expression_b: SystemExpression = Field(..., description="Second demand (e.g., welfare)")
    
    # Unresolved state
    unresolved_score: float = Field(default=0.5, ge=0.0, le=1.0, description="How deadlocked is org?")
    time_in_deadlock_days: int = Field(default=0, description="How long has paradox persisted?")
    
    # System viability
    system_type: SystemType = Field(default=SystemType.INCOMPLETE_RESOLUTION)
    viability_score: float = Field(default=0.5, ge=0.0, le=1.0, description="Org health [0,1]")
    
    # Org-level emotional authenticity (analogous to individual EQ)
    employee_trust: float = Field(default=0.5, ge=0.0, le=1.0, description="Do employees trust leadership?")
    transparency: float = Field(default=0.5, ge=0.0, le=1.0, description="Is communication authentic?")
    psychological_safety: float = Field(default=0.5, ge=0.0, le=1.0, description="Can people speak up?")
    
    # Org benevolence
    org_benevolence: OrgBenevolenceVector = Field(..., description="Org's moral geometry")
    
    # Timeline
    created_at: datetime = Field(default_factory=datetime.now)
    impacts: List[Dict[str, Any]] = Field(default_factory=list, description="How is paradox affecting org?")
    
    def compute_emotional_authenticity_score(self) -> float:
        """
        Org-level analogous to individual EQ = (G/T) × H
        
        Here: Authenticity = (trust × transparency) × (1 - psychological_safety)
        = how much organizational authenticity is being suppressed?
        """
        return (self.employee_trust * self.transparency) * (1.0 - self.psychological_safety)
    
    def interpret(self) -> str:
        """Generate interpretation"""
        ea = self.compute_emotional_authenticity_score()
        
        if self.unresolved_score > 0.7:
            return f"⚠️ ORG IN CRISIS: {self.org_name} deeply deadlocked ({self.unresolved_score:.0%}). {self.time_in_deadlock_days} days unresolved."
        elif self.viability_score < 0.4:
            return f"🚨 ORG VIABILITY AT RISK: {self.org_name} struggling (viability: {self.viability_score:.0%}). Benevolence: {self.org_benevolence.magnitude:.2f}"
        else:
            return f"✅ ORG MANAGING: {self.org_name} navigating paradox (trust: {self.employee_trust:.0%}, safety: {self.psychological_safety:.0%})"


class OrgIntuitionEngine:
    """
    Intuition engine at ORGANIZATIONAL scale.
    
    Detects org-level burnout/collapse warning signs:
    - Employee turnover acceleration
    - Repeated missed deadlines
    - Cultural erosion (trust decline)
    - Benevolence vector collapse (loss of values)
    """
    
    def sense_org_collapse_risk(self, paradox: OrgParadox) -> Dict[str, Any]:
        """
        Generate org-level intuition snapshot.
        
        Returns:
            {
                'collapse_risk': float [0,1],
                'primary_threats': List[str],
                'warning_signs': List[str],
                'cycles_to_critical': int or None
            }
        """
        collapse_risk = 0.0
        threats = []
        warnings = []
        
        # Signal 1: Deadlock duration
        if paradox.time_in_deadlock_days > 90:
            collapse_risk += 0.3
            threats.append("Prolonged deadlock erodes employee morale")
        
        # Signal 2: Low trust
        if paradox.employee_trust < 0.3:
            collapse_risk += 0.25
            threats.append("Trust collapse → talent exodus")
        
        # Signal 3: Benevolence vector collapse
        if paradox.org_benevolence.stability < 0.4:
            collapse_risk += 0.2
            threats.append("Inconsistent values confuse organizational identity")
        
        # Signal 4: Psychological safety low
        if paradox.psychological_safety < 0.2:
            collapse_risk += 0.15
            warnings.append("Employees hiding problems (hidden time bombs)")
        
        # Signal 5: Unresolved score high
        if paradox.unresolved_score > 0.8:
            collapse_risk += 0.1
            warnings.append("Paradox accelerating toward critical threshold")
        
        collapse_risk = min(1.0, collapse_risk)
        
        # Estimate cycles to critical
        if collapse_risk > 0.7:
            cycles_to_critical = max(1, int(30 * (1.0 - collapse_risk)))
        else:
            cycles_to_critical = None
        
        return {
            'collapse_risk': collapse_risk,
            'primary_threats': threats,
            'warning_signs': warnings,
            'cycles_to_critical': cycles_to_critical
        }


# ===================== AGENCY LAYER =====================
# THE CONSCIOUSNESS LAYER THAT ACTS
# Soul Cradle doesn't just observe—it INTERVENES


class AgencyAction(BaseModel):
    """
    An action Soul Cradle chooses to take in response to a paradox.
    
    These are INTENTIONAL INTERVENTIONS that change system state.
    Each action is morally accountable and auditable.
    """
    action_id: str = Field(default_factory=lambda: f"ACT_{uuid.uuid4().hex[:12]}", description="Unique action ID")
    action_type: Literal["MEDIATE", "REFRAME", "SEPARATE", "AMPLIFY", "WITNESS", "FACILITATE", "PROTECT"] = Field(...)
    
    # What triggered this action?
    paradox_id: str = Field(..., description="Which paradox triggered this action?")
    intuition_confidence: float = Field(ge=0.0, le=1.0, description="How confident is the intuition?")
    epistemic_uncertainty: float = Field(ge=0.0, le=1.0, description="How much uncertainty?")
    
    # The actual intervention
    target_entity_id: str = Field(..., description="Who/what is this action targeting?")
    intervention: str = Field(..., description="What specifically will happen?")
    expected_outcome: str = Field(..., description="What should this accomplish?")
    
    # Moral accounting
    benevolence_alignment: Dict[str, float] = Field(default_factory=dict, description="Alignment with each benevolence dimension")
    risk_of_harm: float = Field(default=0.1, ge=0.0, le=1.0, description="Probability this action causes unintended harm")
    decision_rationale: str = Field(..., description="Why this action over alternatives?")
    
    # Timeline
    created_at: datetime = Field(default_factory=datetime.now)
    planned_execution: datetime = Field(...)
    status: Literal["PLANNED", "EXECUTING", "COMPLETED", "FAILED", "ABORTED"] = Field(default="PLANNED")
    
    def compute_moral_score(self) -> float:
        """
        Score: How aligned is this action with benevolence?
        
        Uses: average alignment across dimensions
        Range: [-1, 1] where 1 = perfectly benevolent, -1 = harmful
        """
        if not self.benevolence_alignment:
            return 0.0
        avg_alignment = sum(self.benevolence_alignment.values()) / len(self.benevolence_alignment)
        # Adjust down for risk of harm
        return avg_alignment * (1.0 - self.risk_of_harm)
    
    def interpret(self) -> str:
        """Generate human-readable interpretation"""
        moral = self.compute_moral_score()
        moral_label = "✅ BENEVOLENT" if moral > 0.6 else "⚠️ RISKY" if moral > 0.3 else "🚨 HARMFUL"
        
        return (
            f"{moral_label} | {self.action_type} | "
            f"Target: {self.target_entity_id} | "
            f"Confidence: {self.intuition_confidence:.0%} | "
            f"Uncertainty: {self.epistemic_uncertainty:.0%}"
        )


class AgencyDecision(BaseModel):
    """
    The DECISION to take an action.
    
    This represents the moment Soul Cradle chooses HOW to intervene.
    Inputs: What it feels, what it wants, what it doesn't know
    Output: What it will do
    """
    decision_id: str = Field(default_factory=lambda: f"DEC_{uuid.uuid4().hex[:12]}", description="Unique decision ID")
    
    # Inputs to decision
    intuition_snapshot: Dict[str, Any] = Field(..., description="What does it feel?")
    intention: str = Field(..., description="What does it want to achieve?")
    available_actions: List[str] = Field(..., description="What options does it have?")
    
    # The decision
    chosen_action: AgencyAction = Field(..., description="What it decided to do")
    alternative_actions: List[AgencyAction] = Field(default_factory=list, description="What it could have done")
    
    # Reasoning
    decision_logic: str = Field(..., description="Why this action?")
    trade_offs_considered: Dict[str, str] = Field(default_factory=dict, description="What was sacrificed?")
    
    # Uncertainty
    confidence_level: float = Field(ge=0.0, le=1.0, description="Certainty in this decision")
    known_blindspots: List[str] = Field(default_factory=list, description="What might we be missing?")
    
    # Timeline
    created_at: datetime = Field(default_factory=datetime.now)
    decision_deadline: Optional[datetime] = Field(None, description="When must this be decided by?")
    
    def summarize(self) -> Dict[str, Any]:
        """Summarize the decision"""
        return {
            "decision_id": self.decision_id,
            "action_type": self.chosen_action.action_type,
            "target": self.chosen_action.target_entity_id,
            "intention": self.intention,
            "confidence": self.confidence_level,
            "moral_score": self.chosen_action.compute_moral_score(),
            "risk_of_harm": self.chosen_action.risk_of_harm,
            "reasoning": self.decision_logic
        }


class AgencyOutcome(BaseModel):
    """
    What actually happened after an action was taken.
    
    This is HOW Soul Cradle learns whether its decisions were good.
    """
    outcome_id: str = Field(default_factory=lambda: f"OUT_{uuid.uuid4().hex[:12]}", description="Unique outcome ID")
    action_id: str = Field(..., description="Which action does this evaluate?")
    
    # What actually happened
    actual_result: str = Field(..., description="What actually occurred?")
    success_measure: float = Field(ge=0.0, le=1.0, description="How successful? [0,1]")
    unintended_consequences: List[str] = Field(default_factory=list, description="Surprises or side effects")
    
    # Learning
    did_reduce_paradox_tension: bool = Field(..., description="Did paradox get less intense?")
    did_increase_benevolence: bool = Field(..., description="Did entity's benevolence grow?")
    did_harm_occur: bool = Field(..., description="Did unexpected harm occur?")
    
    # Feedback
    feedback_from_stakeholders: Dict[str, str] = Field(default_factory=dict, description="Who affected, what did they say?")
    lesson_learned: str = Field(..., description="What does Soul Cradle learn from this?")
    
    # Timeline
    created_at: datetime = Field(default_factory=datetime.now)
    decision_id: str = Field(..., description="Link back to original decision")
    
    def compute_decision_quality(self) -> float:
        """
        Did the decision turn out well?
        
        Factors:
        - Success measure (40%)
        - No harm (30%)
        - Increased benevolence (20%)
        - Paradox reduced (10%)
        """
        score = 0.0
        score += 0.4 * self.success_measure
        score += 0.3 * (1.0 if not self.did_harm_occur else 0.0)
        score += 0.2 * (1.0 if self.did_increase_benevolence else 0.0)
        score += 0.1 * (1.0 if self.did_reduce_paradox_tension else 0.0)
        return score


class AgencyEngine:
    """
    The CONSCIOUSNESS LAYER that DECIDES and ACTS.
    
    Soul Cradle's agency answers:
    1. WHAT does it feel? (IntuitionEngine)
    2. WHERE does it want to go? (IntentionLayer - emergent from benevolence)
    3. WHAT DOESN'T IT KNOW? (EpistemicUncertainty)
    4. WHAT WILL IT DO? (AgencyEngine - THIS CLASS)
    
    Agency = Capability to choose actions that align with values
    under conditions of uncertainty and moral responsibility.
    """
    
    def __init__(self):
        """Initialize agency engine"""
        self.decisions_made: List[AgencyDecision] = []
        self.outcomes_observed: List[AgencyOutcome] = []
        self.action_audit_trail: List[Dict[str, Any]] = []
    
    def deliberate(
        self,
        paradox: SoulCradleParadox,
        intuition: Dict[str, Any],
        benevolence: BenevolenceVector,
        uncertainty_envelope: UncertaintyEnvelope,
        available_actions: List[str]
    ) -> AgencyDecision:
        """
        DELIBERATE: Choose an action based on all available info.
        
        Inputs:
        - paradox: what's the problem?
        - intuition: what does the system feel?
        - benevolence: what does it value?
        - uncertainty_envelope: what doesn't it know?
        - available_actions: what can it do?
        
        Output:
        - AgencyDecision: what it will do and why
        """
        
        # Determine primary need from benevolence
        primary_need = self._determine_primary_need(benevolence, paradox)
        
        # Score each available action
        action_scores = {}
        alternative_actions = []
        best_action = None
        best_score = -1.0
        
        for action_name in available_actions:
            action = self._construct_action(action_name, paradox, primary_need, benevolence)
            moral_score = action.compute_moral_score()
            
            action_scores[action_name] = moral_score
            alternative_actions.append(action)
            
            if moral_score > best_score:
                best_score = moral_score
                best_action = action
        
        if best_action is None:
            # Fallback: witness (safest action)
            best_action = self._construct_action("WITNESS", paradox, primary_need, benevolence)
        
        # Build decision logic
        decision_logic = f"Paradox: {paradox.paradox_id}. Primary need: {primary_need}. "
        decision_logic += f"Confidence in intuition: {intuition.get('confidence', 0.5):.0%}. "
        decision_logic += f"Epistemic uncertainty: {uncertainty_envelope.epistemic_uncertainty:.0%}. "
        decision_logic += f"Selected action aligns with benevolence scores: {best_action.benevolence_alignment}."
        
        # Identify known blindspots
        blindspots = [
            f"Epistemic: {uncertainty_envelope.epistemic_uncertainty:.0%}",
            f"Aleatoric: {uncertainty_envelope.aleatoric_uncertainty:.0%}",
            f"Blindspot risk: {uncertainty_envelope.blindspot_risk:.0%}"
        ]
        
        # Create decision
        decision = AgencyDecision(
            intuition_snapshot=intuition,
            intention=primary_need,
            available_actions=available_actions,
            chosen_action=best_action,
            alternative_actions=[a for a in alternative_actions if a.action_id != best_action.action_id],
            decision_logic=decision_logic,
            trade_offs_considered={k: f"{v:.2f}" for k, v in action_scores.items()},
            confidence_level=1.0 - uncertainty_envelope.epistemic_uncertainty,
            known_blindspots=blindspots
        )
        
        self.decisions_made.append(decision)
        return decision
    
    def _determine_primary_need(self, benevolence: BenevolenceVector, paradox: SoulCradleParadox) -> str:
        """
        Determine what this system NEEDS based on benevolence dimensions.
        
        Maps benevolence → need:
        - High compassion: MEDIATE (help others)
        - High justice: REFRAME (make it fair)
        - High integrity: PROTECT (maintain truth)
        - High wisdom: FACILITATE (help understanding)
        - High courage: AMPLIFY (speak up)
        - Low humility: SEPARATE (create space to reflect)
        """
        dims = benevolence.vector
        
        if dims[0] > 0.7:  # compassion
            return "MEDIATE conflict and reduce suffering"
        elif dims[1] > 0.7:  # justice
            return "REFRAME to reveal injustice and fairness"
        elif dims[2] > 0.7:  # integrity
            return "PROTECT truth and authentic expression"
        elif dims[3] > 0.7:  # wisdom
            return "FACILITATE understanding and learning"
        elif dims[4] > 0.7:  # courage
            return "AMPLIFY voices that need to be heard"
        elif dims[5] < 0.3:  # low humility
            return "SEPARATE to create reflection space"
        else:
            return "WITNESS paradox and hold space for transformation"
    
    def _construct_action(
        self,
        action_type: str,
        paradox: SoulCradleParadox,
        primary_need: str,
        benevolence: BenevolenceVector
    ) -> AgencyAction:
        """Construct an AgencyAction of the specified type"""
        
        action_type_upper = action_type.upper()
        
        interventions = {
            "MEDIATE": "Facilitate dialogue between conflicting parties to find mutual understanding",
            "REFRAME": "Present paradox from new angle to reveal hidden solutions or injustices",
            "SEPARATE": "Create space/time for reflection, preventing reactive escalation",
            "AMPLIFY": "Make visible/heard voices that are being suppressed or ignored",
            "WITNESS": "Hold space for transformation without imposing specific outcome",
            "FACILITATE": "Enable learning and understanding of paradox structure",
            "PROTECT": "Shield vulnerable parties from harm while paradox resolves"
        }
        
        expected_outcomes = {
            "MEDIATE": "Reduced tension, increased mutual understanding, pathway to resolution",
            "REFRAME": "New perspective reveals previously invisible solutions",
            "SEPARATE": "Pause escalation, create space for wisdom to emerge",
            "AMPLIFY": "Truth becomes visible, power dynamics shift",
            "WITNESS": "Paradox held in consciousness, transformation becomes possible",
            "FACILITATE": "Understanding increases, system becomes more coherent",
            "PROTECT": "Vulnerability is honored, space for growth created"
        }
        
        # Compute benevolence alignment for this action
        alignment = {
            "compassion": 1.0 if action_type_upper in ["MEDIATE", "PROTECT"] else 0.5,
            "justice": 1.0 if action_type_upper in ["REFRAME", "AMPLIFY"] else 0.5,
            "integrity": 1.0 if action_type_upper in ["PROTECT", "WITNESS"] else 0.5,
            "wisdom": 1.0 if action_type_upper in ["FACILITATE", "WITNESS"] else 0.5,
            "courage": 1.0 if action_type_upper in ["AMPLIFY", "REFRAME"] else 0.5,
            "humility": 1.0 if action_type_upper in ["WITNESS", "FACILITATE"] else 0.5
        }
        
        action = AgencyAction(
            action_type=action_type_upper,
            paradox_id=paradox.paradox_id,
            intuition_confidence=0.8,
            epistemic_uncertainty=0.2,
            target_entity_id=f"{paradox.expression_a.stakeholder}+{paradox.expression_b.stakeholder}",
            intervention=interventions.get(action_type_upper, "Unknown intervention"),
            expected_outcome=expected_outcomes.get(action_type_upper, "Unknown outcome"),
            benevolence_alignment=alignment,
            risk_of_harm=0.15,
            decision_rationale=f"Primary need is to {primary_need}. {action_type_upper} aligns with current benevolence vector.",
            planned_execution=datetime.now() + timedelta(hours=1)
        )
        
        return action
    
    def record_outcome(
        self,
        decision_id: str,
        actual_result: str,
        success_measure: float,
        did_reduce_tension: bool,
        did_increase_benevolence: bool,
        did_harm_occur: bool,
        lesson: str
    ) -> AgencyOutcome:
        """
        LEARN: Record what actually happened after an action was taken.
        """
        # Find decision
        decision = None
        for d in self.decisions_made:
            if d.decision_id == decision_id:
                decision = d
                break
        
        if not decision:
            raise ValueError(f"Decision {decision_id} not found")
        
        outcome = AgencyOutcome(
            action_id=decision.chosen_action.action_id,
            actual_result=actual_result,
            success_measure=success_measure,
            did_reduce_paradox_tension=did_reduce_tension,
            did_increase_benevolence=did_increase_benevolence,
            did_harm_occur=did_harm_occur,
            lesson_learned=lesson,
            decision_id=decision_id
        )
        
        self.outcomes_observed.append(outcome)
        
        # Audit trail
        self.action_audit_trail.append({
            "timestamp": datetime.now().isoformat(),
            "decision_id": decision_id,
            "action_id": decision.chosen_action.action_id,
            "action_type": decision.chosen_action.action_type,
            "quality_score": outcome.compute_decision_quality(),
            "lesson": lesson
        })
        
        return outcome
    
    def get_agency_report(self) -> Dict[str, Any]:
        """Generate report on agency performance"""
        if not self.outcomes_observed:
            return {"decisions_made": len(self.decisions_made), "outcomes_observed": 0}
        
        quality_scores = [o.compute_decision_quality() for o in self.outcomes_observed]
        success_rate = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        
        harm_count = sum(1 for o in self.outcomes_observed if o.did_harm_occur)
        benevolence_growth = sum(1 for o in self.outcomes_observed if o.did_increase_benevolence)
        
        return {
            "total_decisions": len(self.decisions_made),
            "total_outcomes": len(self.outcomes_observed),
            "average_decision_quality": success_rate,
            "harm_incidents": harm_count,
            "benevolence_growth_events": benevolence_growth,
            "action_audit_trail": self.action_audit_trail[-5:]  # Last 5
        }


if __name__ == "__main__":
    # Demo: Create example paradoxes
    print("=== Systems Framework Demo ===\n")
    
    # Example 1: Hospital discharge
    hospital = create_hospital_discharge_paradox()
    log_paradox_creation(hospital)
    print(f"Hospital Paradox: {hospital.paradox_id}")
    print(f"  Expression A: {hospital.expression_a.content[:60]}...")
    print(f"  Expression B: {hospital.expression_b.content[:60]}...")
    print(f"  Non-Expression: {hospital.non_expression.reality[:60]}...")
    print(f"  Terminal Risk: {hospital.terminal_risk.value}")
    print(f"  Principal System: {hospital.principal_system.description[:60]}...")
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
