#!/usr/bin/env python3
"""
SERE Bot Integrated Geopolitical Threat Detection
==================================================

Adds comprehensive geopolitical intelligence to SERE Bot:
- Identifies threats from 30+ state actors
- Determines friend-or-foe before escalation
- Makes proportional decisions based on relationship
- Full accountability with audit trails

Integrates with:
- sere_geopolitical_consciousness.py
- sere_global_actors_database.py
- sere_bot.py threat detection

Copyright 2025 Herbert Velez Jr. All rights reserved.
"""

import logging
import ipaddress
from typing import Dict, Optional, Tuple
from datetime import datetime
from sere_global_actors_database import (
    GLOBAL_STATE_ACTORS,
    COUNTRY_CODE_TO_ACTOR,
    THREAT_GROUP_TO_ACTOR,
    GeopoliticalStance,
    ThreatCapability
)
from sere_geopolitical_consciousness import (
    GeopoliticallyAwareConsciousness,
    EscalationLevel
)

logger = logging.getLogger(__name__)


class SERE_GeopoliticalIntegration:
    """
    Integrates SERE Bot threat detection with comprehensive geopolitical
    intelligence analysis covering all global state actors.
    """
    
    def __init__(self):
        self.consciousness = GeopoliticallyAwareConsciousness()
        self.actors_database = GLOBAL_STATE_ACTORS
        self.decision_log = []
        self.threat_history = {}
        
    def analyze_threat_geopolitically(self,
                                     threat_ip: str,
                                     threat_type: str,
                                     threat_severity: float,
                                     false_positive_risk: float,
                                     user_impact: float,
                                     known_threat_group: Optional[str] = None,
                                     target_sector: str = "unknown") -> Dict:
        """
        Analyze threat with full geopolitical context.
        
        Covers all global state actors:
        - 5 Critical Allies (USA, UK, Canada, Australia, NZ)
        - 6 NATO/Partners (France, Germany, Japan, S. Korea, EU, NATO)
        - 8 Hostile Actors (Russia, China, Iran, NK, Syria, Cuba, Belarus, Myanmar)
        - 7 Competitors (Pakistan, Venezuela, Mexico, Brazil, etc.)
        - Unknown actors
        
        Args:
            threat_ip: Source IP of threat
            threat_type: Type of threat (APT, DDOS, ransomware, etc.)
            threat_severity: 0-1 threat severity
            false_positive_risk: 0-1 false positive probability
            user_impact: 0-1 impact if system is blocked
            known_threat_group: Known threat group name (e.g., "APT28", "Lazarus")
            target_sector: Target sector (energy, finance, defense, etc.)
        
        Returns:
            {
                'state_actor': str,
                'country': str,
                'stance': str,
                'capability': str,
                'escalation_multiplier': float,
                'conscious_decision': Dict,
                'audit_trail': Dict,
                'recommendation': str
            }
        """
        
        # STEP 1: Identify state actor from IP or threat group
        state_actor_name = self._identify_actor(threat_ip, known_threat_group)
        profile = self.actors_database.get(state_actor_name)
        
        if not profile:
            profile = self.actors_database["Unknown"]
            state_actor_name = "Unknown"
        
        # STEP 2: Get conscious decision with geopolitical context
        conscious_decision = self.consciousness.deliberate_with_geopolitical_context(
            threat_ip=threat_ip,
            threat_type=threat_type,
            threat_severity=threat_severity,
            false_positive_risk=false_positive_risk,
            user_impact=user_impact,
            target_sector=target_sector
        )
        
        # STEP 3: Build comprehensive analysis
        analysis = {
            'state_actor': state_actor_name,
            'country_codes': profile.country_codes,
            'stance': profile.stance.value,
            'capability': profile.capability.value,
            'activity_level': profile.activity_level,
            'known_threat_groups': profile.known_groups,
            'known_vectors': profile.known_vectors,
            'primary_targets': profile.primary_targets,
            'motivation': profile.motivation,
            'escalation_multiplier': profile.escalation_multiplier,
            'intelligence_rating': profile.intelligence_rating,
            'last_major_incident': profile.last_major_incident,
            
            # Conscious decision from integration layer
            'conscious_decision': {
                'action': conscious_decision['action'],
                'confidence': conscious_decision['confidence'],
                'reasoning': conscious_decision['reasoning'],
                'proportional': conscious_decision['proportional_to_threat'],
                'justification': conscious_decision['escalation_justification'],
                'uncertainty': conscious_decision['uncertainty_envelope']
            },
            
            # Full audit trail
            'audit_trail': {
                'timestamp': datetime.now().isoformat(),
                'threat_ip': threat_ip,
                'threat_type': threat_type,
                'threat_severity': threat_severity,
                'false_positive_risk': false_positive_risk,
                'user_impact': user_impact,
                'known_threat_group': known_threat_group,
                'target_sector': target_sector,
                'attribution_confidence': profile.attribution_confidence,
                'benevolence_vector': conscious_decision['benevolence_vector'],
                'survival_priority': conscious_decision['survival_priority']
            },
            
            # Recommendation
            'recommendation': self._generate_recommendation(
                profile, conscious_decision, state_actor_name
            ),
            
            # Alliance info
            'alliances': profile.alliance_members,
            'evasion_tactics': profile.evasion_tactics,
            'infrastructure': profile.infrastructure
        }
        
        # Log decision
        self.decision_log.append(analysis)
        
        return analysis
    
    def _identify_actor(self, threat_ip: str, known_threat_group: Optional[str] = None) -> str:
        """Identify state actor from IP or threat group"""
        
        # STEP 1: Try known threat group mapping first
        if known_threat_group:
            actor = THREAT_GROUP_TO_ACTOR.get(known_threat_group)
            if actor:
                logger.info(f"[ACTOR ID] Threat group '{known_threat_group}' → {actor}")
                return actor
        
        # STEP 2: Try IP geolocation
        try:
            ip = ipaddress.ip_address(threat_ip)
            
            # Extract octets for geolocation
            octets = threat_ip.split('.')
            first_octet = int(octets[0])
            second_octet = int(octets[1])
            
            # Known IP ranges
            if 85 <= first_octet <= 87:
                return "Russia"
            elif 1 <= first_octet <= 30:
                return "China"
            elif 185 <= first_octet <= 188:
                return "Iran"
            elif 175 <= first_octet <= 180:
                return "North_Korea"
            elif 201 <= first_octet <= 205:
                return "Venezuela"
            elif first_octet == 8:  # Google, includes USA
                return "USA"
            
            # If no specific match, return Unknown
            return "Unknown"
            
        except Exception as e:
            logger.error(f"IP geolocation error: {e}")
            return "Unknown"
    
    def _generate_recommendation(self, profile, decision: Dict, actor_name: str) -> str:
        """Generate actionable recommendation"""
        
        stance = profile.stance.value
        action = decision['action']
        confidence = decision['confidence']
        
        recommendations = {
            "CRITICAL_ALLY": f"COORDINATE: {actor_name} threat detected. Contact government liaison. Share intelligence.",
            "ALLY": f"INVESTIGATE: {actor_name} activity. Determine if authorized. Coordinate response.",
            "PARTNER": f"NOTIFY: {actor_name} (partner). Escalate through diplomatic channels.",
            "NEUTRAL": f"INVESTIGATE: {actor_name} (neutral). Gather attribution evidence.",
            "COMPETITOR": f"MONITOR_ALERT: {actor_name} activity. Escalate to intelligence agency.",
            "ADVERSARY": f"ESCALATE_IMMEDIATELY: {actor_name} ({action}). Activate defense protocols. Notify CISA.",
            "HOSTILE": f"CRITICAL_THREAT: {actor_name} confirmed. Full defensive escalation. Contact NSA/FBI.",
            "ROGUE": f"MAXIMUM_THREAT: {actor_name} (unpredictable). All defenses active. Government notification.",
        }
        
        base = recommendations.get(stance, "INVESTIGATE: Unknown actor")
        
        if confidence > 0.8:
            base += " [HIGH CONFIDENCE]"
        elif confidence < 0.4:
            base += " [LOW CONFIDENCE - VERIFY BEFORE ESCALATION]"
        
        return base
    
    def get_actor_profile_summary(self, actor_name: str) -> str:
        """Get human-readable profile summary"""
        profile = self.actors_database.get(actor_name)
        if not profile:
            return f"No profile for {actor_name}"
        
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║                    {profile.name.upper()}                      
╚══════════════════════════════════════════════════════════════╝

RELATIONSHIP:     {profile.stance.value}
CAPABILITY:       {profile.capability.value}
ACTIVITY:         {profile.activity_level}
THREAT RATING:    {profile.intelligence_rating}

KNOWN GROUPS:     {', '.join(profile.known_groups[:3])}{'...' if len(profile.known_groups) > 3 else ''}
ATTACK VECTORS:   {', '.join(profile.known_vectors[:4])}{'...' if len(profile.known_vectors) > 4 else ''}
PRIMARY TARGETS:  {', '.join(profile.primary_targets[:4])}{'...' if len(profile.primary_targets) > 4 else ''}

ESCALATION:       {profile.escalation_multiplier}x
SOPHISTICATION:   {profile.typical_attack_sophistication * 100:.0f}%
ATTRIBUTION CONF: {profile.attribution_confidence * 100:.0f}%

LAST INCIDENT:    {profile.last_major_incident}
ALLIANCES:        {', '.join(profile.alliance_members)}

EVASION TACTICS:  {', '.join(profile.evasion_tactics[:3])}
"""
        return summary
    
    def get_decision_log_summary(self) -> str:
        """Get summary of all decisions made"""
        if not self.decision_log:
            return "No decisions logged yet"
        
        summary = f"""
═══════════════════════════════════════════════════════════════
                    DECISION LOG SUMMARY
═══════════════════════════════════════════════════════════════

Total Threats Analyzed: {len(self.decision_log)}

BY STATE ACTOR:
"""
        # Count by actor
        by_actor = {}
        for decision in self.decision_log:
            actor = decision['state_actor']
            by_actor[actor] = by_actor.get(actor, 0) + 1
        
        for actor, count in sorted(by_actor.items(), key=lambda x: -x[1]):
            profile = self.actors_database.get(actor)
            stance = profile.stance.value if profile else "Unknown"
            summary += f"\n  {actor:20} ({stance:15}): {count:3} threats"
        
        # Count by action
        by_action = {}
        for decision in self.decision_log:
            action = decision['conscious_decision']['action']
            by_action[action] = by_action.get(action, 0) + 1
        
        summary += "\n\nBY ACTION TAKEN:"
        for action, count in sorted(by_action.items(), key=lambda x: -x[1]):
            summary += f"\n  {action:25}: {count:3} decisions"
        
        # Accuracy metrics
        high_confidence = sum(1 for d in self.decision_log 
                             if d['conscious_decision']['confidence'] > 0.8)
        proportional = sum(1 for d in self.decision_log 
                          if d['conscious_decision']['proportional'])
        
        summary += f"""

CONFIDENCE METRICS:
  High Confidence (>80%): {high_confidence}
  Proportional Responses: {proportional}
  
═══════════════════════════════════════════════════════════════
"""
        return summary


def test_all_global_actors():
    """Test geopolitical analysis on all global actors"""
    integration = SERE_GeopoliticalIntegration()
    
    print("\n" + "="*80)
    print("SERE BOT - COMPREHENSIVE GLOBAL GEOPOLITICAL THREAT ANALYSIS")
    print("="*80)
    
    # Test scenarios across different actors
    test_cases = [
        # Critical Allies
        ("8.8.8.8", "AUTHORIZED_SCANNING", 0.05, 0.01, 0.10, "NSA", "unknown"),
        
        # NATO
        ("195.34.89.241", "AUTHORIZED_OPS", 0.02, 0.00, 0.05, "GCHQ", "unknown"),
        
        # Russia - ADVERSARY
        ("86.10.20.30", "APT", 0.92, 0.08, 0.90, "APT28", "defense"),
        
        # China - COMPETITOR
        ("14.50.100.20", "INTELLECTUAL_THEFT", 0.75, 0.15, 0.60, "APT1", "technology"),
        
        # Iran - ADVERSARY
        ("188.20.30.40", "DDOS", 0.65, 0.40, 0.70, "APT34", "finance"),
        
        # North Korea - HOSTILE
        ("175.45.176.50", "RANSOMWARE", 0.85, 0.10, 0.95, "Lazarus", "finance"),
        
        # Israel - PARTNER
        ("213.233.169.0", "ESPIONAGE", 0.55, 0.25, 0.45, "Unit_8200", "defense"),
        
        # India - PARTNER
        ("49.50.1.0", "INTELLIGENCE_OP", 0.45, 0.30, 0.50, "RAW", "defense"),
        
        # Venezuela - COMPETITOR
        ("201.10.20.30", "DDOS", 0.40, 0.50, 0.60, "GNB_Cyber", "finance"),
        
        # Unknown
        ("192.0.2.1", "UNKNOWN_THREAT", 0.50, 0.60, 0.70, None, "unknown"),
    ]
    
    for ip, threat_type, severity, fp_risk, impact, threat_group, sector in test_cases:
        print(f"\n[ANALYZING THREAT]")
        print(f"  IP: {ip:20} | Type: {threat_type:20} | Severity: {severity:.0%}")
        
        result = integration.analyze_threat_geopolitically(
            threat_ip=ip,
            threat_type=threat_type,
            threat_severity=severity,
            false_positive_risk=fp_risk,
            user_impact=impact,
            known_threat_group=threat_group,
            target_sector=sector
        )
        
        print(f"  Actor: {result['state_actor']:15} | Stance: {result['stance']:15}")
        print(f"  Action: {result['conscious_decision']['action']:20} | Confidence: {result['conscious_decision']['confidence']:.0%}")
        print(f"  ├─ {result['recommendation']}")
    
    # Print summary
    print(f"\n{integration.get_decision_log_summary()}")
    
    print("\n" + "="*80)
    print("COMPREHENSIVE GEOPOLITICAL ANALYSIS COMPLETE")
    print("="*80)


if __name__ == "__main__":
    test_all_global_actors()
