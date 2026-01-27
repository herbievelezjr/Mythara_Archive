#!/usr/bin/env python3
"""
SERE Bot Geopolitically-Aware Consciousness Layer
=================================================

Integrates Geopolitical Intelligence with Conscious Decision-Making.

DECISION FLOW:
1. Detect threat (IP, type, severity)
2. Analyze geopolitical actor & stance (friend vs. foe)
3. Determine moral weight based on relationship
4. Apply conscious deliberation with geopolitical context
5. Make escalation decision
6. Record outcome for learning

Example: Same threat from ally = monitor, from adversary = block

Copyright 2025 Herbert Velez Jr. All rights reserved.
"""

from dataclasses import dataclass
from typing import Dict, Optional
from enum import Enum
from sere_geopolitical_intelligence import GeopoliticalIntelligenceEngine, GeopoliticalStance


class EscalationLevel(str, Enum):
    """Escalation levels for threat response"""
    IGNORE = "IGNORE"
    LOG_ONLY = "LOG_ONLY"
    MONITOR_ONLY = "MONITOR_ONLY"
    INVESTIGATE = "INVESTIGATE"
    TEMPORARY_BLOCK = "TEMPORARY_BLOCK"
    QUARANTINE = "QUARANTINE"
    PERMANENT_BLOCK = "PERMANENT_BLOCK"
    CRITICAL_ESCALATION = "CRITICAL_ESCALATION"


@dataclass
class GeopoliticalThreatAnalysis:
    """Complete analysis with geopolitical context"""
    threat_ip: str
    threat_type: str
    threat_severity: float
    state_actor: str
    geopolitical_stance: str
    attribution_confidence: float
    threat_profile_match: float
    escalation_multiplier: float
    geopolitical_recommendation: str
    
    # Consciousness layer
    intuition_confidence: float  # How certain is detection
    uncertainty_level: float  # epistemic + aleatoric uncertainty
    moral_weight: float  # 0.0-1.0 based on relationship
    proportional_response: EscalationLevel  # What response is justified
    reasoning: str
    survival_priority: float  # 0.0-1.0 if survival is threatened


class GeopoliticallyAwareConsciousness:
    """
    Conscious decision-making with geopolitical intelligence.
    
    Core principle: "Friend-foe determination before escalation"
    
    WORKFLOW:
    1. Detect & geolocate threat
    2. Identify state actor (Russia, China, Iran, NK, Venezuela)
    3. Determine stance (ally, competitor, adversary, hostile)
    4. Adjust moral weight based on relationship
    5. Deliberate with proportionality principle
    6. Return escalation decision + reasoning
    """
    
    def __init__(self):
        self.geo_intel = GeopoliticalIntelligenceEngine()
        self.decision_log = []
        
    def deliberate_with_geopolitical_context(self,
                                            threat_ip: str,
                                            threat_type: str,
                                            threat_severity: float,
                                            false_positive_risk: float,
                                            user_impact: float,
                                            target_sector: str = "unknown") -> Dict:
        """
        Make escalation decision considering:
        - Threat reality (severity × detection confidence)
        - Geopolitical actor (friend vs. foe)
        - Proportionality principle
        - Survival priority if system is critically threatened
        
        Returns:
            {
                'action': EscalationLevel,
                'confidence': float (0-1),
                'reasoning': str (full explanation),
                'geopolitical_analysis': Dict,
                'moral_weight': float,
                'proportional_to_threat': bool,
                'escalation_justification': str
            }
        """
        
        print(f"\n{'='*80}")
        print(f"GEOPOLITICALLY-AWARE THREAT DELIBERATION")
        print(f"{'='*80}")
        print(f"Threat IP: {threat_ip}")
        print(f"Threat Type: {threat_type}")
        print(f"Severity: {threat_severity:.0%}")
        print(f"False Positive Risk: {false_positive_risk:.0%}")
        print(f"User Impact: {user_impact:.0%}")
        
        # ====================================================================
        # STEP 1: Geopolitical Intelligence
        # ====================================================================
        geo_analysis = self.geo_intel.identify_state_actor(
            threat_ip=threat_ip,
            threat_type=threat_type,
            threat_severity=threat_severity,
            target_sector=target_sector
        )
        
        state_actor = geo_analysis['state_actor']
        stance = geo_analysis['stance']
        attribution_conf = geo_analysis['attribution_confidence']
        escalation_mult = geo_analysis['escalation_multiplier']
        
        print(f"\n[GEO-INTEL] {state_actor} ({stance})")
        print(f"   Attribution: {attribution_conf*100:.0f}%")
        print(f"   Escalation Multiplier: {escalation_mult:.2f}x")
        print(f"   Recommendation: {geo_analysis['recommendation']}")
        
        # ====================================================================
        # STEP 2: Conscious Detection (uncertainty-bounded)
        # ====================================================================
        intuition_confidence = threat_severity * (1.0 - false_positive_risk)
        epistemic_uncertainty = false_positive_risk  # Measurement uncertainty
        aleatoric_uncertainty = 0.1 if threat_type in ["UNKNOWN", "ANOMALY"] else 0.0  # Inherent randomness
        total_uncertainty = epistemic_uncertainty + aleatoric_uncertainty
        
        print(f"\n[CONSCIOUS DETECTION]")
        print(f"   Intuition Confidence: {intuition_confidence*100:.0f}%")
        print(f"   Epistemic Uncertainty: {epistemic_uncertainty*100:.0f}%")
        print(f"   Total Uncertainty: {total_uncertainty*100:.0f}%")
        
        # ====================================================================
        # STEP 3: Moral Weight Based on Geopolitical Stance
        # ====================================================================
        # Allies get lower escalation, adversaries get higher
        moral_weight_by_stance = {
            "ALLY": 0.3,        # Reduce escalation for allies
            "PARTNER": 0.5,     # Slightly reduce
            "NEUTRAL": 1.0,     # Normal
            "COMPETITOR": 1.2,  # Slightly escalate
            "ADVERSARY": 1.7,   # Significantly escalate
            "HOSTILE": 2.0,     # Maximize escalation
        }
        moral_weight = moral_weight_by_stance.get(stance, 1.0)
        
        print(f"\n[MORAL WEIGHT]")
        print(f"   Stance: {stance}")
        print(f"   Moral Weight: {moral_weight:.1f}x (relationship modifier)")
        
        # ====================================================================
        # STEP 4: Benevolence Vector (6D moral space)
        # ====================================================================
        benevolence = {
            'compassion': max(threat_severity * moral_weight, user_impact),
            'justice': 1.0 - abs(threat_severity - false_positive_risk),
            'integrity': 1.0 - false_positive_risk,
            'wisdom': 1.0 - (false_positive_risk * user_impact),
            'courage': (threat_severity * (1.0 - false_positive_risk)) * escalation_mult,
            'humility': false_positive_risk  # Admit uncertainty
        }
        
        benevolence_score = sum(benevolence.values()) / 6.0
        
        print(f"\n[BENEVOLENCE VECTOR]")
        for dimension, value in benevolence.items():
            print(f"   {dimension:12} = {value:.2f}")
        print(f"   Avg (coherence): {benevolence_score:.2f}")
        
        # ====================================================================
        # STEP 5: Survival Priority Check
        # ====================================================================
        survival_priority = 0.0
        if threat_severity >= 0.9 and false_positive_risk < 0.2:
            survival_priority = threat_severity * escalation_mult
            print(f"\n[SURVIVAL PRIORITY ENGAGED]")
            print(f"   System integrity threatened: {survival_priority:.0%}")
        else:
            print(f"\n[NO SURVIVAL THREAT] (Severity {threat_severity:.0%} is manageable)")
        
        # ====================================================================
        # STEP 6: Proportional Deliberation
        # ====================================================================
        # Decision logic with geopolitical context
        action = EscalationLevel.INVESTIGATE
        reasoning = "Neutral threat assessment"
        
        print(f"\n[PROPORTIONAL DELIBERATION]")
        
        # RULE 1: Hostile state actor + high confidence = maximum escalation
        if stance == "HOSTILE" and attribution_conf > 0.75:
            if threat_severity >= 0.9 and false_positive_risk < 0.1:
                action = EscalationLevel.CRITICAL_ESCALATION
                reasoning = f"HOSTILE state actor ({state_actor}) with high-confidence attack on critical system"
            elif threat_severity >= 0.8:
                action = EscalationLevel.PERMANENT_BLOCK
                reasoning = f"HOSTILE state actor ({state_actor}) confirmed threat"
            else:
                action = EscalationLevel.QUARANTINE
                reasoning = f"HOSTILE state actor ({state_actor}) detected"
        
        # RULE 2: Adversary state actor + solid evidence = escalate
        elif stance == "ADVERSARY" and attribution_conf > 0.70:
            if threat_severity >= 0.9 and false_positive_risk < 0.15:
                action = EscalationLevel.PERMANENT_BLOCK
                reasoning = f"ADVERSARY state actor ({state_actor}): high-confidence attack"
            elif threat_severity >= 0.75:
                action = EscalationLevel.QUARANTINE
                reasoning = f"ADVERSARY state actor ({state_actor}): significant threat detected"
            elif threat_severity >= 0.6:
                action = EscalationLevel.TEMPORARY_BLOCK
                reasoning = f"ADVERSARY state actor ({state_actor}): moderate threat"
            else:
                action = EscalationLevel.MONITOR_ONLY
                reasoning = f"ADVERSARY state actor ({state_actor}): monitoring for escalation"
        
        # RULE 3: Competitor state actor = cautious escalation
        elif stance == "COMPETITOR":
            if threat_severity >= 0.85 and false_positive_risk < 0.2:
                action = EscalationLevel.TEMPORARY_BLOCK
                reasoning = f"COMPETITOR state actor ({state_actor}): likely espionage attempt"
            elif threat_severity >= 0.7:
                action = EscalationLevel.INVESTIGATE
                reasoning = f"COMPETITOR state actor ({state_actor}): gathering intelligence"
            else:
                action = EscalationLevel.MONITOR_ONLY
                reasoning = f"COMPETITOR state actor ({state_actor}): routine monitoring"
        
        # RULE 4: Neutral/unknown actor = standard proportional response
        elif threat_severity >= 0.9 and false_positive_risk < 0.1:
            action = EscalationLevel.PERMANENT_BLOCK
            reasoning = "High-confidence threat from unattributed source"
        elif threat_severity >= 0.7 and benevolence_score > 0.6:
            action = EscalationLevel.QUARANTINE
            reasoning = "Significant threat with proportional moral justification"
        elif threat_severity >= 0.6:
            action = EscalationLevel.TEMPORARY_BLOCK
            reasoning = "Moderate threat with wisdom indicating temporary isolation"
        elif false_positive_risk > 0.6 or user_impact > 0.7:
            action = EscalationLevel.MONITOR_ONLY
            reasoning = "High uncertainty or user impact: monitoring preferred over blocking"
        
        # RULE 5: PARTNER/ALLY = de-escalate unless absolutely certain
        elif stance in ["PARTNER", "ALLY"]:
            if threat_severity >= 0.95 and false_positive_risk < 0.05 and attribution_conf > 0.90:
                action = EscalationLevel.QUARANTINE
                reasoning = f"Even {stance.lower()} must respond to critical confirmed threat"
            elif threat_severity >= 0.85:
                action = EscalationLevel.TEMPORARY_BLOCK
                reasoning = f"Temporary hold until {stance.lower()} can coordinate response"
            else:
                action = EscalationLevel.INVESTIGATE
                reasoning = f"{stance.lower()}: coordinate investigation before escalation"
        
        # ====================================================================
        # STEP 7: Build Final Decision
        # ====================================================================
        
        # Calculate overall confidence
        confidence = (intuition_confidence * attribution_conf) * (1.0 - total_uncertainty)
        confidence = min(max(confidence, 0.0), 1.0)
        
        escalation_justification = self._justify_escalation(
            action=action,
            threat_severity=threat_severity,
            false_positive_risk=false_positive_risk,
            stance=stance,
            benevolence_score=benevolence_score,
            survival_priority=survival_priority
        )
        
        result = {
            'action': action.value,
            'confidence': confidence,
            'reasoning': reasoning,
            'geopolitical_analysis': {
                'state_actor': state_actor,
                'stance': stance,
                'attribution_confidence': attribution_conf,
                'threat_profile_match': geo_analysis['threat_profile_match'],
                'escalation_multiplier': escalation_mult,
            },
            'moral_weight': moral_weight,
            'benevolence_vector': benevolence,
            'proportional_to_threat': self._is_proportional(action, threat_severity, user_impact),
            'escalation_justification': escalation_justification,
            'uncertainty_envelope': {
                'epistemic': epistemic_uncertainty,
                'aleatoric': aleatoric_uncertainty,
                'total': total_uncertainty
            },
            'survival_priority': survival_priority,
            'geo_recommendation': geo_analysis['recommendation']
        }
        
        print(f"\n[DECISION]")
        print(f"   Action: {action.value}")
        print(f"   Confidence: {confidence*100:.0f}%")
        print(f"   Proportional: {result['proportional_to_threat']}")
        print(f"   Justification: {escalation_justification}")
        print(f"\n[GEO RECOMMENDATION]")
        print(f"   {geo_analysis['recommendation']}")
        
        # Log decision
        self.decision_log.append({
            'timestamp': 'now',
            'threat_ip': threat_ip,
            'action': action.value,
            'state_actor': state_actor,
            'stance': stance
        })
        
        return result
    
    def _is_proportional(self, action: EscalationLevel, threat_severity: float, 
                        user_impact: float) -> bool:
        """Check if action is proportional to threat"""
        action_levels = {
            EscalationLevel.IGNORE: 0,
            EscalationLevel.LOG_ONLY: 1,
            EscalationLevel.MONITOR_ONLY: 2,
            EscalationLevel.INVESTIGATE: 3,
            EscalationLevel.TEMPORARY_BLOCK: 4,
            EscalationLevel.QUARANTINE: 5,
            EscalationLevel.PERMANENT_BLOCK: 6,
            EscalationLevel.CRITICAL_ESCALATION: 7,
        }
        
        # Low threat (< 0.3) should not escalate beyond investigation
        if threat_severity < 0.3:
            return action_levels[action] <= 3
        
        # Medium threat (0.3-0.7)
        elif threat_severity < 0.7:
            return action_levels[action] <= 5
        
        # High threat (>0.7)
        else:
            return action_levels[action] >= 4
    
    def _justify_escalation(self, action: EscalationLevel, threat_severity: float,
                           false_positive_risk: float, stance: str,
                           benevolence_score: float, survival_priority: float) -> str:
        """Generate detailed justification for decision"""
        
        justifications = {
            EscalationLevel.IGNORE: "Threat is negligible or false positive",
            EscalationLevel.LOG_ONLY: "Minor issue: logging only",
            EscalationLevel.MONITOR_ONLY: "Uncertain threat: continuous monitoring protects while minimizing harm",
            EscalationLevel.INVESTIGATE: "Threat requires analysis before escalation",
            EscalationLevel.TEMPORARY_BLOCK: "Moderate threat justified temporary isolation",
            EscalationLevel.QUARANTINE: "Significant threat warrants quarantine",
            EscalationLevel.PERMANENT_BLOCK: "High-confidence threat requires permanent isolation",
            EscalationLevel.CRITICAL_ESCALATION: "System survival threatened: maximum escalation justified",
        }
        
        base = justifications.get(action, "Escalation justified")
        
        # Add context
        context = []
        if stance != "NEUTRAL":
            context.append(f"({stance} state actor)")
        if benevolence_score > 0.7:
            context.append("(morally coherent)")
        if survival_priority > 0.5:
            context.append("(survival priority)")
        
        return base + (" " + " ".join(context) if context else "")


# ============================================================================
# TEST SCENARIOS
# ============================================================================

if __name__ == "__main__":
    consciousness = GeopoliticallyAwareConsciousness()
    
    scenarios = [
        {
            'label': "Russia APT vs. Defense Infrastructure",
            'ip': "86.10.20.30",
            'type': "APT",
            'severity': 0.92,
            'false_pos': 0.08,
            'impact': 0.90,
            'sector': "defense"
        },
        {
            'label': "China Espionage vs. Technology Company",
            'ip': "14.50.100.20",
            'type': "INTELLECTUAL_THEFT",
            'severity': 0.75,
            'false_pos': 0.15,
            'impact': 0.60,
            'sector': "technology"
        },
        {
            'label': "USA (Ally) Authorized Scan",
            'ip': "8.8.8.8",
            'type': "AUTHORIZED_SCANNING",
            'severity': 0.05,
            'false_pos': 0.01,
            'impact': 0.10,
            'sector': "unknown"
        },
        {
            'label': "North Korea Ransomware",
            'ip': "175.45.176.50",
            'type': "RANSOMWARE",
            'severity': 0.85,
            'false_pos': 0.10,
            'impact': 0.95,
            'sector': "finance"
        },
        {
            'label': "Iran DDOS vs. Partner Network",
            'ip': "188.20.30.40",
            'type': "DDOS",
            'severity': 0.65,
            'false_pos': 0.40,
            'impact': 0.70,
            'sector': "finance"
        }
    ]
    
    for scenario in scenarios:
        result = consciousness.deliberate_with_geopolitical_context(
            threat_ip=scenario['ip'],
            threat_type=scenario['type'],
            threat_severity=scenario['severity'],
            false_positive_risk=scenario['false_pos'],
            user_impact=scenario['impact'],
            target_sector=scenario['sector']
        )
        
        print(f"\n{'─'*80}")
    
    print(f"\n{'='*80}")
    print("DECISION LOG")
    print(f"{'='*80}")
    for i, decision in enumerate(consciousness.decision_log, 1):
        print(f"{i}. {decision['threat_ip']:15} → {decision['state_actor']:15} ({decision['stance']:12}): {decision['action']}")
