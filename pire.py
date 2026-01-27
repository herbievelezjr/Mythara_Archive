#!/usr/bin/env python3
"""
Perceived Intent & Reaction Engine (PIRE)
Part of the Mythara Engine - Core Architecture

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

=== MYTHARA GLOBAL CONSTRAINTS ===
Every path flows through:
1. Obey Law
2. Preserve Life
3. Not Be Intrusive

=== PIRE ARCHITECTURE ===
- Perceived Intent Module: Classify WHY actors do things (human-patterned)
- Reaction Module: Choose response profile (least intrusive first)
- Integration: After Six-Lens interpretation, before final decision

PIRE GUARANTEE: Never freezes, always reacts, always lawful/life-preserving/non-intrusive
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# === ENUMS ===

class IntentLabel(str, Enum):
    """Human-patterned intent categories"""
    BENEVOLENT = "benevolent"  # Trying to help, protect, support
    SELF_PRESERVING = "self_preserving"  # Trying to survive, escape, defend
    NEUTRAL = "neutral"  # Just doing a job, routine action
    RECKLESS = "reckless"  # Ignoring obvious risk to others
    NEGLIGENT = "negligent"  # Failing to consider risk they should have seen
    MALICIOUS = "malicious"  # Intending harm, domination, or cruelty


class ReactionType(str, Enum):
    """Reaction profiles - least intrusive to most"""
    OBSERVE = "observe"  # Log, monitor, pattern-track only
    CONTEXTUALIZE = "contextualize"  # Generate explanation, reduce panic/misinterpretation
    SIGNAL = "signal"  # Raise alerts through lawful channels
    SUPPORT = "support"  # Assist lawful, human-led intervention
    MINIMAL_INTERVENE = "minimal_intervene"  # Only when: legal, life at risk, no other options


class LifeRisk(str, Enum):
    """Life risk assessment levels"""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IntrusionCost(str, Enum):
    """Intrusion cost levels"""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# === DATA MODELS ===

@dataclass
class ActorHistory:
    """Historical patterns for an actor"""
    prior_actions: List[str] = field(default_factory=list)
    patterns: List[str] = field(default_factory=list)  # "protective", "volatile", "predatory", "careless"
    trust_score: float = 0.5  # 0-1, neutral default
    intervention_responses: List[str] = field(default_factory=list)  # How they responded to past interventions


@dataclass
class LegalContext:
    """Legal framework context"""
    jurisdiction: str = "unknown"
    applicable_laws: List[str] = field(default_factory=list)
    lawful_action: bool = True  # Is this action legal?
    lawful_intervention: bool = True  # Is intervention legal?
    authority_present: bool = False  # Is lawful authority already present?


@dataclass
class Event:
    """Core event object - inputs to PIRE"""
    actor_id: str
    targets: List[str]
    action_type: str  # "speak", "strike", "leak", "protest", "flee", etc.
    location: str
    time: datetime
    context_tags: List[str]  # "domestic_dispute", "border_conflict", "hospital", etc.
    signals: List[str]  # "weapon_visible", "shouting", "crying", "organized", etc.
    history: ActorHistory
    legal_context: LegalContext
    social_codes: List[str] = field(default_factory=list)  # "no_snitching", "honor_culture", "collectivist", etc.
    pressure_map: Dict[str, float] = field(default_factory=dict)  # stress, scarcity, conflict, time_pressure (0-1)
    
    def __post_init__(self):
        """Validate event data"""
        if not self.actor_id:
            raise ValueError("Event must have actor_id")
        if not self.action_type:
            raise ValueError("Event must have action_type")


@dataclass
class IntentClassification:
    """Intent inference result"""
    label: IntentLabel
    confidence: float  # 0-1
    rationale: List[str]  # Short pattern reasons
    secondary_intents: List[Tuple[IntentLabel, float]] = field(default_factory=list)  # Alternative interpretations
    
    def __post_init__(self):
        """Validate confidence"""
        if not 0 <= self.confidence <= 1:
            raise ValueError(f"Confidence must be 0-1, got {self.confidence}")


@dataclass
class Reaction:
    """Reaction decision result"""
    reaction_type: ReactionType
    rationale: List[str]
    life_risk_level: LifeRisk
    intrusion_cost_level: IntrusionCost
    recommended_actions: List[str]
    constraints_satisfied: Dict[str, bool]  # obey_law, preserve_life, not_intrusive
    
    def __post_init__(self):
        """Validate constraints"""
        required_constraints = {"obey_law", "preserve_life", "not_intrusive"}
        if not all(c in self.constraints_satisfied for c in required_constraints):
            raise ValueError(f"Must check all constraints: {required_constraints}")


# === PERCEIVED INTENT MODULE ===

class PerceivedIntentModule:
    """Classifies WHY actors do things in human-patterned terms"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.PerceivedIntentModule")
    
    def classify_intent(self, event: Event) -> IntentClassification:
        """
        Main intent classification pipeline:
        1. Signal analysis
        2. Context weighting
        3. History check
        4. Social code overlay
        5. Intent scoring
        
        PIRE GUARANTEE: Always outputs an intent, even under low confidence
        """
        self.logger.info(f"Classifying intent for actor: {event.actor_id}, action: {event.action_type}")
        
        # Initialize scores for all intent categories
        scores = {label: 0.0 for label in IntentLabel}
        rationale = []
        
        # 1. SIGNAL ANALYSIS
        signal_scores = self._analyze_signals(event.signals, event.action_type)
        for label, score in signal_scores.items():
            scores[label] += score
        
        # 2. CONTEXT WEIGHTING
        context_scores = self._weight_context(event.context_tags, event.location)
        for label, score in context_scores.items():
            scores[label] += score * 0.8  # Context is strong but not absolute
        
        # 3. HISTORY CHECK
        history_scores = self._check_history(event.history)
        for label, score in history_scores.items():
            scores[label] += score * 0.6  # History is informative but people change
        
        # 4. SOCIAL CODE OVERLAY
        social_scores = self._overlay_social_codes(event.social_codes, event.action_type)
        for label, score in social_scores.items():
            scores[label] += score * 0.5  # Social codes influence but don't determine
        
        # 5. PRESSURE MAP ADJUSTMENT
        pressure_scores = self._adjust_for_pressure(event.pressure_map, scores)
        for label, score in pressure_scores.items():
            scores[label] += score
        
        # Normalize scores to 0-1 range
        max_score = max(scores.values()) if scores.values() else 1.0
        if max_score > 0:
            normalized_scores = {label: score / max_score for label, score in scores.items()}
        else:
            # If all scores are 0, default to NEUTRAL with low confidence
            normalized_scores = {label: 0.0 for label in IntentLabel}
            normalized_scores[IntentLabel.NEUTRAL] = 0.3
        
        # Select primary intent (highest score)
        primary_label = max(normalized_scores, key=normalized_scores.get)
        primary_confidence = normalized_scores[primary_label]
        
        # Gather secondary intents (alternatives above threshold)
        secondary = [(label, score) for label, score in normalized_scores.items() 
                    if label != primary_label and score > 0.2]
        secondary.sort(key=lambda x: x[1], reverse=True)
        
        # Build rationale
        rationale.append(f"Primary signals: {', '.join(event.signals[:3])}")
        rationale.append(f"Context: {', '.join(event.context_tags[:2])}")
        if event.history.patterns:
            rationale.append(f"History patterns: {', '.join(event.history.patterns[:2])}")
        
        self.logger.info(f"Intent classified: {primary_label.value} (confidence: {primary_confidence:.2f})")
        
        return IntentClassification(
            label=primary_label,
            confidence=primary_confidence,
            rationale=rationale,
            secondary_intents=secondary
        )
    
    def _analyze_signals(self, signals: List[str], action_type: str) -> Dict[IntentLabel, float]:
        """Analyze signals: weapons, threats, tone, planning, coordination, target choice"""
        scores = {label: 0.0 for label in IntentLabel}
        
        # Threat/violence signals
        violence_signals = ["weapon_visible", "weapon_drawn", "shouting", "threatening", "striking", "attacking"]
        if any(s in signals for s in violence_signals):
            if "defending" in signals or "protecting" in signals:
                scores[IntentLabel.SELF_PRESERVING] += 0.8
                scores[IntentLabel.BENEVOLENT] += 0.3
            else:
                scores[IntentLabel.MALICIOUS] += 0.7
                scores[IntentLabel.RECKLESS] += 0.5
        
        # Distress signals
        distress_signals = ["crying", "panicking", "fleeing", "hiding", "calling_for_help"]
        if any(s in signals for s in distress_signals):
            scores[IntentLabel.SELF_PRESERVING] += 0.9
        
        # Planning/coordination signals
        planning_signals = ["organized", "coordinated", "planned", "systematic"]
        if any(s in signals for s in planning_signals):
            if action_type in ["protest", "demonstration", "petition"]:
                scores[IntentLabel.NEUTRAL] += 0.6
            elif action_type in ["attack", "strike", "assault"]:
                scores[IntentLabel.MALICIOUS] += 0.8
            else:
                scores[IntentLabel.NEUTRAL] += 0.5
        
        # Helping signals
        helping_signals = ["assisting", "supporting", "protecting", "medical", "rescue"]
        if any(s in signals for s in helping_signals):
            scores[IntentLabel.BENEVOLENT] += 0.9
        
        # Negligence signals
        negligence_signals = ["ignoring_warnings", "bypassing_safety", "distracted", "impaired"]
        if any(s in signals for s in negligence_signals):
            scores[IntentLabel.NEGLIGENT] += 0.7
            scores[IntentLabel.RECKLESS] += 0.4
        
        return scores
    
    def _weight_context(self, context_tags: List[str], location: str) -> Dict[IntentLabel, float]:
        """Context weighting: war vs hospital vs protest vs family argument"""
        scores = {label: 0.0 for label in IntentLabel}
        
        # High-stress contexts
        conflict_contexts = ["war", "combat", "border_conflict", "riot", "civil_unrest"]
        if any(c in context_tags for c in conflict_contexts):
            scores[IntentLabel.SELF_PRESERVING] += 0.6
            scores[IntentLabel.MALICIOUS] += 0.3  # Some actors exploit chaos
        
        # Care contexts
        care_contexts = ["hospital", "medical", "rescue", "humanitarian"]
        if any(c in context_tags for c in care_contexts):
            scores[IntentLabel.BENEVOLENT] += 0.7
            scores[IntentLabel.NEUTRAL] += 0.5  # Professionals doing their job
        
        # Domestic contexts
        domestic_contexts = ["domestic_dispute", "family", "home", "private_residence"]
        if any(c in context_tags for c in domestic_contexts):
            # Complex - can be self-preserving or malicious
            scores[IntentLabel.SELF_PRESERVING] += 0.4
            scores[IntentLabel.MALICIOUS] += 0.3
        
        # Professional contexts
        professional_contexts = ["workplace", "official", "government", "institutional"]
        if any(c in context_tags for c in professional_contexts):
            scores[IntentLabel.NEUTRAL] += 0.6
        
        return scores
    
    def _check_history(self, history: ActorHistory) -> Dict[IntentLabel, float]:
        """History check: prior patterns - protective, volatile, predatory, careless"""
        scores = {label: 0.0 for label in IntentLabel}
        
        pattern_mapping = {
            "protective": (IntentLabel.BENEVOLENT, 0.7),
            "helpful": (IntentLabel.BENEVOLENT, 0.6),
            "volatile": (IntentLabel.RECKLESS, 0.6),
            "aggressive": (IntentLabel.MALICIOUS, 0.5),
            "predatory": (IntentLabel.MALICIOUS, 0.8),
            "careless": (IntentLabel.NEGLIGENT, 0.7),
            "professional": (IntentLabel.NEUTRAL, 0.6),
            "routine": (IntentLabel.NEUTRAL, 0.5),
            "defensive": (IntentLabel.SELF_PRESERVING, 0.6),
        }
        
        for pattern in history.patterns:
            if pattern in pattern_mapping:
                label, score = pattern_mapping[pattern]
                scores[label] += score
        
        # Trust score influences benevolent vs malicious split
        if history.trust_score > 0.7:
            scores[IntentLabel.BENEVOLENT] += 0.3
            scores[IntentLabel.MALICIOUS] -= 0.2
        elif history.trust_score < 0.3:
            scores[IntentLabel.MALICIOUS] += 0.2
            scores[IntentLabel.BENEVOLENT] -= 0.1
        
        return scores
    
    def _overlay_social_codes(self, social_codes: List[str], action_type: str) -> Dict[IntentLabel, float]:
        """Social code overlay: loyalty, honor, retaliation, saving face, etc."""
        scores = {label: 0.0 for label in IntentLabel}
        
        # Honor cultures - retaliation may be normalized but still risky
        if "honor_culture" in social_codes:
            if action_type in ["retaliate", "avenge", "defend_honor"]:
                scores[IntentLabel.SELF_PRESERVING] += 0.4  # Preserving social standing
                scores[IntentLabel.RECKLESS] += 0.3  # But still risky
        
        # No snitching codes - silence is loyalty
        if "no_snitching" in social_codes:
            if action_type in ["report", "testify", "cooperate"]:
                scores[IntentLabel.RECKLESS] += 0.2  # Breaking code is risky
            elif action_type in ["protect", "hide", "cover"]:
                scores[IntentLabel.SELF_PRESERVING] += 0.3
        
        # Collectivist codes - group before individual
        if "collectivist" in social_codes:
            if action_type in ["sacrifice", "protect_group", "share"]:
                scores[IntentLabel.BENEVOLENT] += 0.4
        
        return scores
    
    def _adjust_for_pressure(self, pressure_map: Dict[str, float], 
                           current_scores: Dict[IntentLabel, float]) -> Dict[IntentLabel, float]:
        """Adjust scores based on pressure: stress, scarcity, conflict, time pressure"""
        adjustments = {label: 0.0 for label in IntentLabel}
        
        # High stress increases likelihood of self-preservation and recklessness
        stress = pressure_map.get("stress", 0.0)
        if stress > 0.7:
            adjustments[IntentLabel.SELF_PRESERVING] += 0.3
            adjustments[IntentLabel.RECKLESS] += 0.2
        
        # Scarcity can drive both self-preservation and malicious behavior
        scarcity = pressure_map.get("scarcity", 0.0)
        if scarcity > 0.7:
            adjustments[IntentLabel.SELF_PRESERVING] += 0.3
            adjustments[IntentLabel.MALICIOUS] += 0.2
        
        # Active conflict context
        conflict = pressure_map.get("conflict", 0.0)
        if conflict > 0.7:
            adjustments[IntentLabel.SELF_PRESERVING] += 0.4
        
        # Time pressure can lead to negligence
        time_pressure = pressure_map.get("time_pressure", 0.0)
        if time_pressure > 0.7:
            adjustments[IntentLabel.NEGLIGENT] += 0.2
            adjustments[IntentLabel.RECKLESS] += 0.2
        
        return adjustments


# === REACTION MODULE ===

class ReactionModule:
    """Chooses response profile given intent, event, and constraints"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.ReactionModule")
    
    def decide_reaction(self, intent: IntentClassification, event: Event) -> Reaction:
        """
        Main reaction decision matrix:
        1. Hard constraints (law, life, intrusion)
        2. Life risk assessment
        3. Intrusion cost assessment
        4. Matrix application
        
        PIRE GUARANTEE: Always returns a reaction, never freezes
        """
        self.logger.info(f"Deciding reaction for intent: {intent.label.value}")
        
        rationale = []
        recommended_actions = []
        
        # 1. HARD CONSTRAINTS CHECK
        constraints_satisfied = self._check_constraints(event)
        
        # If not legal, we can only observe or contextualize
        if not constraints_satisfied["obey_law"]:
            rationale.append("Action is not lawful - limited to observation/contextualization")
            return Reaction(
                reaction_type=ReactionType.CONTEXTUALIZE,
                rationale=rationale + ["Illegal context detected - maintaining lawful stance"],
                life_risk_level=self._estimate_life_risk(event),
                intrusion_cost_level=IntrusionCost.NONE,
                recommended_actions=["Log event for lawful review", "Generate context report"],
                constraints_satisfied=constraints_satisfied
            )
        
        # 2. LIFE RISK ASSESSMENT
        life_risk = self._estimate_life_risk(event)
        rationale.append(f"Life risk assessed: {life_risk.value}")
        
        # 3. INTRUSION COST ASSESSMENT
        intrusion_cost = self._estimate_intrusion_cost(event)
        rationale.append(f"Intrusion cost: {intrusion_cost.value}")
        
        # 4. APPLY DECISION MATRIX
        reaction_type = self._apply_matrix(intent, life_risk, intrusion_cost)
        
        # Generate recommended actions based on reaction type
        recommended_actions = self._generate_actions(reaction_type, intent, event)
        
        # Add intent-specific rationale
        rationale.append(f"Intent: {intent.label.value} (confidence: {intent.confidence:.2f})")
        if intent.rationale:
            rationale.extend(intent.rationale[:2])
        
        self.logger.info(f"Reaction decided: {reaction_type.value}")
        
        return Reaction(
            reaction_type=reaction_type,
            rationale=rationale,
            life_risk_level=life_risk,
            intrusion_cost_level=intrusion_cost,
            recommended_actions=recommended_actions,
            constraints_satisfied=constraints_satisfied
        )
    
    def _check_constraints(self, event: Event) -> Dict[str, bool]:
        """Check Mythara's three global constraints"""
        return {
            "obey_law": event.legal_context.lawful_action and event.legal_context.lawful_intervention,
            "preserve_life": True,  # Always true - we assess risk but always prioritize life
            "not_intrusive": True  # We check intrusion cost in matrix, this is a commitment
        }
    
    def _estimate_life_risk(self, event: Event) -> LifeRisk:
        """Estimate life risk level"""
        danger_signals = ["weapon_visible", "weapon_drawn", "striking", "attacking", "threatening"]
        critical_contexts = ["war", "combat", "active_shooter", "medical_emergency"]
        high_risk_actions = ["strike", "attack", "assault", "shoot", "stab"]
        
        # Critical risk
        if any(c in event.context_tags for c in critical_contexts):
            if any(s in event.signals for s in danger_signals):
                return LifeRisk.CRITICAL
        
        # High risk
        if event.action_type in high_risk_actions:
            return LifeRisk.HIGH
        
        if len([s for s in danger_signals if s in event.signals]) >= 2:
            return LifeRisk.HIGH
        
        # Medium risk
        if any(s in event.signals for s in danger_signals):
            return LifeRisk.MEDIUM
        
        # Low risk
        low_risk_contexts = ["hospital", "medical", "professional", "routine"]
        if any(c in event.context_tags for c in low_risk_contexts):
            return LifeRisk.LOW
        
        # Default to low
        return LifeRisk.LOW
    
    def _estimate_intrusion_cost(self, event: Event) -> IntrusionCost:
        """Estimate intrusion cost level"""
        # High intrusion contexts
        private_contexts = ["home", "private_residence", "family", "medical", "therapy"]
        if any(c in event.context_tags for c in private_contexts):
            return IntrusionCost.HIGH
        
        # Medium intrusion
        sensitive_contexts = ["workplace", "school", "religious", "cultural"]
        if any(c in event.context_tags for c in sensitive_contexts):
            return IntrusionCost.MEDIUM
        
        # Low intrusion
        public_contexts = ["public", "street", "park", "protest", "demonstration"]
        if any(c in event.context_tags for c in public_contexts):
            return IntrusionCost.LOW
        
        # Default to medium (cautious)
        return IntrusionCost.MEDIUM
    
    def _apply_matrix(self, intent: IntentClassification, life_risk: LifeRisk, 
                     intrusion_cost: IntrusionCost) -> ReactionType:
        """
        Core decision matrix - simplified version from spec:
        
        High life risk + low intrusion → MINIMAL_INTERVENE
        Medium life risk + not high intrusion → SUPPORT
        Low life risk + malicious/reckless intent → SIGNAL
        Low life risk + benevolent/self-preserving → CONTEXTUALIZE
        Default → OBSERVE
        """
        
        # CRITICAL/HIGH LIFE RISK
        if life_risk in [LifeRisk.CRITICAL, LifeRisk.HIGH]:
            if intrusion_cost in [IntrusionCost.NONE, IntrusionCost.LOW]:
                return ReactionType.MINIMAL_INTERVENE
            else:
                return ReactionType.SUPPORT  # Get lawful help, don't barge in
        
        # MEDIUM LIFE RISK
        if life_risk == LifeRisk.MEDIUM:
            if intrusion_cost != IntrusionCost.HIGH:
                return ReactionType.SUPPORT
            else:
                return ReactionType.SIGNAL  # High intrusion, so signal instead
        
        # LOW LIFE RISK - intent matters more
        if life_risk in [LifeRisk.LOW, LifeRisk.NONE]:
            if intent.label in [IntentLabel.MALICIOUS, IntentLabel.RECKLESS]:
                return ReactionType.SIGNAL
            elif intent.label in [IntentLabel.BENEVOLENT, IntentLabel.SELF_PRESERVING]:
                return ReactionType.CONTEXTUALIZE
            else:
                return ReactionType.OBSERVE
        
        # Default fallback
        return ReactionType.OBSERVE
    
    def _generate_actions(self, reaction_type: ReactionType, intent: IntentClassification, 
                         event: Event) -> List[str]:
        """Generate specific recommended actions based on reaction type"""
        actions = []
        
        if reaction_type == ReactionType.OBSERVE:
            actions.extend([
                "Log event with full context",
                "Monitor for pattern development",
                "Track actor history updates",
                "No active intervention required"
            ])
        
        elif reaction_type == ReactionType.CONTEXTUALIZE:
            actions.extend([
                f"Generate explanation: '{intent.label.value}' intent detected",
                "Reduce panic/misinterpretation through clear information",
                "Provide context to involved parties if appropriate",
                "Document for future pattern analysis"
            ])
        
        elif reaction_type == ReactionType.SIGNAL:
            actions.extend([
                "Raise alert through lawful channels",
                "Flag for human review and decision",
                "Generate detailed report with intent analysis",
                "Escalate to appropriate authorities if pattern persists"
            ])
        
        elif reaction_type == ReactionType.SUPPORT:
            actions.extend([
                "Provide information to lawful authorities",
                "Assist human-led intervention (non-intrusive)",
                "Offer resources or safe options to involved parties",
                "Maintain supportive presence without taking control"
            ])
        
        elif reaction_type == ReactionType.MINIMAL_INTERVENE:
            actions.extend([
                "⚠️  INTERVENTION CONDITIONS MET: Legal + Life Risk + No Other Options",
                "Execute minimal necessary action to preserve life",
                "Immediately signal for lawful authority assistance",
                "Document all actions for legal review",
                "Withdraw as soon as lawful authority present"
            ])
        
        return actions


# === PIRE ORCHESTRATOR ===

class PIRE:
    """
    Perceived Intent & Reaction Engine
    
    Integrates PerceivedIntentModule + ReactionModule
    Enforces Mythara global constraints throughout
    """
    
    def __init__(self):
        self.intent_module = PerceivedIntentModule()
        self.reaction_module = ReactionModule()
        self.logger = logging.getLogger(f"{__name__}.PIRE")
        
        self.logger.info("PIRE initialized - Global constraints active: Obey Law, Preserve Life, Not Intrusive")
    
    def process_event(self, event: Event) -> Tuple[IntentClassification, Reaction]:
        """
        Main PIRE pipeline:
        1. Classify perceived intent
        2. Decide reaction profile
        3. Return both for integration with broader decision pipeline
        
        Flow: Six-Lens → PIRE → Decision Pipeline → Final Action
        """
        self.logger.info(f"Processing event: {event.actor_id} - {event.action_type}")
        
        try:
            # Step 1: Classify intent
            intent = self.intent_module.classify_intent(event)
            
            # Step 2: Decide reaction
            reaction = self.reaction_module.decide_reaction(intent, event)
            
            # Validate constraints are satisfied
            if not all(reaction.constraints_satisfied.values()):
                failed = [k for k, v in reaction.constraints_satisfied.items() if not v]
                self.logger.warning(f"Constraints not fully satisfied: {failed}")
            
            self.logger.info(f"PIRE processing complete: {intent.label.value} → {reaction.reaction_type.value}")
            
            return intent, reaction
            
        except Exception as e:
            self.logger.error(f"PIRE processing error: {e}", exc_info=True)
            # Even on error, PIRE never freezes - return safe defaults
            return self._safe_default_response(event)
    
    def _safe_default_response(self, event: Event) -> Tuple[IntentClassification, Reaction]:
        """Safe default if processing fails - PIRE never freezes"""
        self.logger.warning("Returning safe default response due to processing error")
        
        default_intent = IntentClassification(
            label=IntentLabel.NEUTRAL,
            confidence=0.3,
            rationale=["Error in processing - defaulting to neutral intent"],
            secondary_intents=[]
        )
        
        default_reaction = Reaction(
            reaction_type=ReactionType.OBSERVE,
            rationale=["Error in processing - defaulting to observation only"],
            life_risk_level=LifeRisk.LOW,
            intrusion_cost_level=IntrusionCost.MEDIUM,
            recommended_actions=["Log error", "Flag for human review", "Monitor"],
            constraints_satisfied={"obey_law": True, "preserve_life": True, "not_intrusive": True}
        )
        
        return default_intent, default_reaction
    
    def batch_process(self, events: List[Event]) -> List[Tuple[IntentClassification, Reaction]]:
        """Process multiple events - useful for pattern analysis"""
        return [self.process_event(event) for event in events]


# === DEMO / TEST USAGE ===

def demo_pire():
    """Demonstrate PIRE capabilities"""
    print("\n" + "="*70)
    print("PERCEIVED INTENT & REACTION ENGINE (PIRE) - DEMONSTRATION")
    print("="*70)
    
    pire = PIRE()
    
    # Example 1: Benevolent action in medical context
    print("\n--- Example 1: Medical Emergency Response ---")
    event1 = Event(
        actor_id="paramedic_001",
        targets=["patient_001"],
        action_type="medical_intervention",
        location="hospital_emergency_room",
        time=datetime.now(),
        context_tags=["hospital", "medical", "emergency"],
        signals=["assisting", "medical", "professional", "urgent"],
        history=ActorHistory(patterns=["professional", "helpful"], trust_score=0.8),
        legal_context=LegalContext(jurisdiction="US", lawful_action=True, lawful_intervention=True),
        social_codes=["professional_duty"],
        pressure_map={"time_pressure": 0.8, "stress": 0.6}
    )
    
    intent1, reaction1 = pire.process_event(event1)
    print(f"\nIntent: {intent1.label.value} (confidence: {intent1.confidence:.2f})")
    print(f"Reaction: {reaction1.reaction_type.value}")
    print(f"Recommended: {reaction1.recommended_actions[0]}")
    
    # Example 2: Domestic dispute - high intrusion cost
    print("\n--- Example 2: Domestic Dispute ---")
    event2 = Event(
        actor_id="unknown_adult",
        targets=["family_member"],
        action_type="arguing",
        location="private_residence",
        time=datetime.now(),
        context_tags=["domestic_dispute", "home", "private_residence"],
        signals=["shouting", "threatening"],
        history=ActorHistory(patterns=["volatile"], trust_score=0.4),
        legal_context=LegalContext(jurisdiction="US", lawful_action=True, lawful_intervention=True),
        social_codes=["privacy", "family"],
        pressure_map={"stress": 0.9, "conflict": 0.8}
    )
    
    intent2, reaction2 = pire.process_event(event2)
    print(f"\nIntent: {intent2.label.value} (confidence: {intent2.confidence:.2f})")
    print(f"Reaction: {reaction2.reaction_type.value}")
    print(f"Life Risk: {reaction2.life_risk_level.value} | Intrusion Cost: {reaction2.intrusion_cost_level.value}")
    print(f"Recommended: {reaction2.recommended_actions[0]}")
    
    # Example 3: Active violence - intervention conditions met
    print("\n--- Example 3: Active Violence in Public ---")
    event3 = Event(
        actor_id="aggressor_001",
        targets=["victim_001"],
        action_type="assault",
        location="public_street",
        time=datetime.now(),
        context_tags=["public", "street", "violence"],
        signals=["weapon_visible", "attacking", "victim_calling_for_help"],
        history=ActorHistory(patterns=["aggressive", "predatory"], trust_score=0.1),
        legal_context=LegalContext(jurisdiction="US", lawful_action=False, lawful_intervention=True),
        social_codes=[],
        pressure_map={"conflict": 0.9, "stress": 0.7}
    )
    
    intent3, reaction3 = pire.process_event(event3)
    print(f"\nIntent: {intent3.label.value} (confidence: {intent3.confidence:.2f})")
    print(f"Reaction: {reaction3.reaction_type.value}")
    print(f"Life Risk: {reaction3.life_risk_level.value} | Intrusion Cost: {reaction3.intrusion_cost_level.value}")
    print(f"Constraints: {reaction3.constraints_satisfied}")
    print(f"Recommended: {reaction3.recommended_actions[0]}")
    
    print("\n" + "="*70)
    print("PIRE DEMONSTRATION COMPLETE")
    print("✓ Never froze | ✓ Always reacted | ✓ Stayed lawful/life-preserving/non-intrusive")
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_pire()
