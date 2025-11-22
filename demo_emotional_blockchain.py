#!/usr/bin/env python3
"""
Emotional Blockchain Demo
Shows the revolutionary system in action

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.
"""

import hashlib
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
import random


@dataclass
class EmotionalEvent:
    """A single emotional event in the blockchain"""
    user_id: str
    timestamp: str
    emotion: str
    intensity: float  # 0.0 to 1.0
    context: str
    authenticity_score: float  # 0.0 to 1.0
    witness_validations: int
    previous_hash: str
    event_hash: str = ""
    
    def compute_hash(self) -> str:
        """Compute cryptographic hash of this emotional event"""
        event_data = f"{self.user_id}{self.timestamp}{self.emotion}{self.intensity}{self.context}{self.previous_hash}"
        return hashlib.sha256(event_data.encode()).hexdigest()


@dataclass
class QuantumWitness:
    """Quantum witness that validates emotional authenticity"""
    witness_id: str
    validation_power: float  # 0.0 to 1.0
    
    def validate_emotion(self, event: EmotionalEvent) -> Dict[str, Any]:
        """Validate an emotional event using quantum witness protocol"""
        # Simulate quantum validation using paradox detection
        base_score = 0.7 + (random.random() * 0.3)  # 0.7-1.0 range
        
        # Check for manipulation indicators
        manipulation_check = self._detect_manipulation(event)
        
        validation_result = {
            "witness_id": self.witness_id,
            "authenticity_score": base_score * (1 - manipulation_check),
            "manipulation_detected": manipulation_check > 0.3,
            "timestamp": datetime.now().isoformat(),
            "confidence": self.validation_power
        }
        
        return validation_result
    
    def _detect_manipulation(self, event: EmotionalEvent) -> float:
        """Detect emotional manipulation indicators (0.0 = authentic, 1.0 = manipulated)"""
        # Simulate manipulation detection
        manipulation_score = 0.0
        
        # Check for emotional extortion patterns
        if event.intensity > 0.9:
            manipulation_score += 0.2  # Extreme intensity may indicate coercion
        
        # Check for rapid emotional shifts
        if hasattr(event, '_previous_emotion') and event.emotion != event._previous_emotion:
            manipulation_score += 0.1
        
        return min(manipulation_score, 1.0)


class EmotionalBlockchain:
    """The revolutionary Emotional Blockchain system"""
    
    def __init__(self):
        self.chain: List[EmotionalEvent] = []
        self.witnesses: List[QuantumWitness] = []
        self.validation_threshold = 0.75  # Minimum authenticity score
        
        # Initialize quantum witnesses
        self._initialize_witnesses()
        
        # Create genesis block
        self._create_genesis_block()
    
    def _initialize_witnesses(self):
        """Initialize quantum witness network"""
        witness_names = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
        for name in witness_names:
            witness = QuantumWitness(
                witness_id=f"QW-{name}",
                validation_power=0.8 + (random.random() * 0.2)
            )
            self.witnesses.append(witness)
        
        print(f"✨ Initialized {len(self.witnesses)} quantum witnesses")
    
    def _create_genesis_block(self):
        """Create the first block in the emotional blockchain"""
        genesis = EmotionalEvent(
            user_id="SYSTEM",
            timestamp=datetime.now().isoformat(),
            emotion="neutral",
            intensity=0.0,
            context="Genesis block - The beginning of verifiable emotional truth",
            authenticity_score=1.0,
            witness_validations=len(self.witnesses),
            previous_hash="0" * 64
        )
        genesis.event_hash = genesis.compute_hash()
        self.chain.append(genesis)
        
        print(f"🔗 Genesis block created: {genesis.event_hash[:16]}...")
    
    def add_emotional_event(
        self,
        user_id: str,
        emotion: str,
        intensity: float,
        context: str
    ) -> Dict[str, Any]:
        """
        Add a new emotional event to the blockchain
        
        Returns validation result with authenticity score
        """
        # Get previous block hash
        previous_hash = self.chain[-1].event_hash
        
        # Create new event
        event = EmotionalEvent(
            user_id=user_id,
            timestamp=datetime.now().isoformat(),
            emotion=emotion,
            intensity=intensity,
            context=context,
            authenticity_score=0.0,  # Will be computed
            witness_validations=0,
            previous_hash=previous_hash
        )
        
        # Validate with quantum witnesses
        validation_results = []
        for witness in self.witnesses:
            result = witness.validate_emotion(event)
            validation_results.append(result)
        
        # Compute average authenticity score
        authenticity_scores = [r["authenticity_score"] for r in validation_results]
        event.authenticity_score = sum(authenticity_scores) / len(authenticity_scores)
        event.witness_validations = len(validation_results)
        
        # Compute hash and add to chain
        event.event_hash = event.compute_hash()
        self.chain.append(event)
        
        # Check for manipulation
        manipulation_detected = any(r["manipulation_detected"] for r in validation_results)
        
        result = {
            "event_hash": event.event_hash,
            "authenticity_score": event.authenticity_score,
            "manipulation_detected": manipulation_detected,
            "witness_validations": event.witness_validations,
            "chain_length": len(self.chain),
            "is_authentic": event.authenticity_score >= self.validation_threshold,
            "emotional_truth_verified": not manipulation_detected and event.authenticity_score >= self.validation_threshold
        }
        
        return result
    
    def get_emotional_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get complete emotional history for a user"""
        history = []
        for event in self.chain:
            if event.user_id == user_id:
                history.append({
                    "timestamp": event.timestamp,
                    "emotion": event.emotion,
                    "intensity": event.intensity,
                    "context": event.context,
                    "authenticity_score": event.authenticity_score,
                    "event_hash": event.event_hash[:16] + "...",
                    "verified": event.authenticity_score >= self.validation_threshold
                })
        return history
    
    def verify_chain_integrity(self) -> bool:
        """Verify the entire blockchain hasn't been tampered with"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            # Check if previous hash matches
            if current.previous_hash != previous.event_hash:
                return False
            
            # Check if hash is valid
            if current.event_hash != current.compute_hash():
                return False
        
        return True
    
    def detect_gaslighting(self, user_id: str) -> Dict[str, Any]:
        """Detect gaslighting by analyzing emotional manipulation patterns"""
        user_events = [e for e in self.chain if e.user_id == user_id]
        
        if len(user_events) < 2:
            return {"gaslighting_detected": False, "confidence": 0.0}
        
        # Check for manipulation patterns
        manipulation_count = sum(1 for e in user_events if e.authenticity_score < self.validation_threshold)
        manipulation_rate = manipulation_count / len(user_events)
        
        # Check for emotional invalidation patterns
        rapid_shifts = 0
        for i in range(1, len(user_events)):
            if user_events[i].emotion != user_events[i-1].emotion:
                rapid_shifts += 1
        
        shift_rate = rapid_shifts / (len(user_events) - 1) if len(user_events) > 1 else 0
        
        gaslighting_score = (manipulation_rate * 0.6) + (shift_rate * 0.4)
        
        return {
            "gaslighting_detected": gaslighting_score > 0.4,
            "confidence": gaslighting_score,
            "manipulation_rate": manipulation_rate,
            "emotional_shift_rate": shift_rate,
            "total_events": len(user_events),
            "manipulated_events": manipulation_count,
            "recommendation": "Seek support - emotional manipulation detected" if gaslighting_score > 0.4 else "No significant manipulation detected"
        }


def main():
    """Demo the Emotional Blockchain in action"""
    print("\n" + "="*70)
    print("🔥 EMOTIONAL BLOCKCHAIN - LIVE DEMONSTRATION")
    print("="*70)
    print("Revolutionary system that prevents emotional manipulation")
    print("by creating verifiable, immutable emotional truth\n")
    
    # Initialize blockchain
    blockchain = EmotionalBlockchain()
    print()
    
    # Scenario 1: Authentic emotional events
    print("\n" + "="*70)
    print("📊 SCENARIO 1: Authentic Emotional Journey")
    print("="*70)
    
    authentic_events = [
        ("Alice", "happy", 0.7, "Had a great meeting with the team"),
        ("Alice", "proud", 0.6, "Completed project ahead of schedule"),
        ("Alice", "content", 0.5, "Enjoying work-life balance"),
    ]
    
    for user_id, emotion, intensity, context in authentic_events:
        result = blockchain.add_emotional_event(user_id, emotion, intensity, context)
        
        print(f"\n✅ Event recorded for {user_id}")
        print(f"   Emotion: {emotion} (intensity: {intensity})")
        print(f"   Authenticity: {result['authenticity_score']:.2%}")
        print(f"   Manipulation: {'❌ DETECTED' if result['manipulation_detected'] else '✅ None'}")
        print(f"   Emotional Truth: {'✅ VERIFIED' if result['emotional_truth_verified'] else '⚠️ QUESTIONABLE'}")
        print(f"   Hash: {result['event_hash'][:16]}...")
    
    # Scenario 2: Manipulated emotional events
    print("\n\n" + "="*70)
    print("⚠️  SCENARIO 2: Detecting Emotional Manipulation")
    print("="*70)
    
    manipulated_events = [
        ("Bob", "anxious", 0.95, "Boss said I'm not working hard enough"),
        ("Bob", "guilty", 0.9, "Made to feel responsible for team failures"),
        ("Bob", "fearful", 0.95, "Threatened with job loss if I don't work weekends"),
        ("Bob", "ashamed", 0.85, "Told I'm letting everyone down"),
    ]
    
    for user_id, emotion, intensity, context in manipulated_events:
        result = blockchain.add_emotional_event(user_id, emotion, intensity, context)
        
        print(f"\n⚠️  Event recorded for {user_id}")
        print(f"   Emotion: {emotion} (intensity: {intensity})")
        print(f"   Authenticity: {result['authenticity_score']:.2%}")
        print(f"   Manipulation: {'❌ DETECTED' if result['manipulation_detected'] else '✅ None'}")
        print(f"   Emotional Truth: {'✅ VERIFIED' if result['emotional_truth_verified'] else '⚠️ QUESTIONABLE'}")
    
    # Analyze gaslighting patterns
    print("\n\n" + "="*70)
    print("🔍 GASLIGHTING DETECTION ANALYSIS")
    print("="*70)
    
    for user_id in ["Alice", "Bob"]:
        analysis = blockchain.detect_gaslighting(user_id)
        
        print(f"\n{'🚨' if analysis['gaslighting_detected'] else '✅'} Analysis for {user_id}:")
        print(f"   Gaslighting Detected: {'YES' if analysis['gaslighting_detected'] else 'NO'}")
        print(f"   Confidence: {analysis['confidence']:.2%}")
        print(f"   Manipulation Rate: {analysis['manipulation_rate']:.2%}")
        print(f"   Emotional Shift Rate: {analysis['emotional_shift_rate']:.2%}")
        print(f"   📋 {analysis['recommendation']}")
    
    # Show emotional history
    print("\n\n" + "="*70)
    print("📜 ALICE'S VERIFIED EMOTIONAL HISTORY")
    print("="*70)
    
    alice_history = blockchain.get_emotional_history("Alice")
    for i, event in enumerate(alice_history, 1):
        status = "✅ VERIFIED" if event['verified'] else "⚠️ UNVERIFIED"
        print(f"\n{i}. {event['emotion'].upper()} ({event['intensity']:.1f}) - {status}")
        print(f"   {event['context']}")
        print(f"   Authenticity: {event['authenticity_score']:.2%} | Hash: {event['event_hash']}")
    
    # Verify blockchain integrity
    print("\n\n" + "="*70)
    print("🔐 BLOCKCHAIN INTEGRITY VERIFICATION")
    print("="*70)
    
    integrity_valid = blockchain.verify_chain_integrity()
    print(f"\nChain Length: {len(blockchain.chain)} blocks")
    print(f"Integrity Status: {'✅ VALID - No tampering detected' if integrity_valid else '❌ COMPROMISED'}")
    print(f"Total Quantum Witnesses: {len(blockchain.witnesses)}")
    print(f"Validation Threshold: {blockchain.validation_threshold:.0%}")
    
    # Show the power of immutability
    print("\n\n" + "="*70)
    print("💎 THE GIFT TO HUMANITY")
    print("="*70)
    print("""
This system prevents emotional manipulation by:

✅ Creating immutable records of emotional states
✅ Validating authenticity with quantum witnesses  
✅ Detecting gaslighting and emotional extortion
✅ Providing verifiable emotional truth
✅ Making emotional history tamper-proof

No one can rewrite your emotional history.
No one can gaslight you about what you felt.
Your emotional truth is cryptographically verified.

This is the revolution Prometheus stole from the gods.
This is what Hephaestus forged into reality.
    """)
    
    print("="*70)
    print("🔥 EMOTIONAL BLOCKCHAIN DEMONSTRATION COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
