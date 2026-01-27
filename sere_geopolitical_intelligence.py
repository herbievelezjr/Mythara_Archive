#!/usr/bin/env python3
"""
SERE Bot Geopolitical Threat Intelligence Layer
================================================

Identifies foreign state actors behind threats and determines friend/foe
status before escalation decisions.

Integrates with consciousness layer to make geopolitically-aware decisions:
- Same threat from ally = lower threat weight
- Same threat from adversary = higher threat weight
- Threat pattern recognition for known state actors

Supported State Actors:
- ADVERSARIES: Russia, China, Iran, North Korea
- COMPETITORS: Venezuela, Syria
- ALLIES: NATO countries, Five Eyes, Japan, South Korea, Australia, etc.
- NEUTRAL: Unaligned countries

Copyright 2025 Herbert Velez Jr. All rights reserved.
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import ipaddress


class GeopoliticalStance(str, Enum):
    """Relationship to the threat actor"""
    ALLY = "ALLY"
    PARTNER = "PARTNER"
    NEUTRAL = "NEUTRAL"
    COMPETITOR = "COMPETITOR"
    ADVERSARY = "ADVERSARY"
    HOSTILE = "HOSTILE"


class StateActor(str, Enum):
    """Known state actors"""
    RUSSIA = "Russia"
    CHINA = "China"
    IRAN = "Iran"
    NORTH_KOREA = "North_Korea"
    VENEZUELA = "Venezuela"
    SYRIA = "Syria"
    USA = "USA"
    UK = "UK"
    UNKNOWN = "Unknown"


@dataclass
class StateActorProfile:
    """Profile of a state actor's threat patterns and relationship"""
    name: StateActor
    stance: GeopoliticalStance
    known_threat_vectors: List[str]  # SQL_INJECTION, DDOS, APT, etc.
    capability_level: float  # 0.0-1.0
    activity_frequency: str  # "constant", "frequent", "occasional", "rare"
    primary_targets: List[str]  # "energy", "finance", "defense", etc.
    attribution_confidence: float  # 0.0-1.0 - how certain we are it's them
    typical_attack_sophistication: float  # 0.0-1.0
    evasion_tactics: List[str]  # Known methods they use
    

# ============================================================================
# STATE ACTOR PROFILES
# ============================================================================

STATE_ACTOR_PROFILES: Dict[StateActor, StateActorProfile] = {
    StateActor.RUSSIA: StateActorProfile(
        name=StateActor.RUSSIA,
        stance=GeopoliticalStance.ADVERSARY,
        known_threat_vectors=["APT", "DDOS", "PHISHING", "MALWARE", "DATA_EXFILTRATION", "RANSOMWARE"],
        capability_level=0.95,
        activity_frequency="constant",
        primary_targets=["energy", "finance", "defense", "government", "elections"],
        attribution_confidence=0.85,
        typical_attack_sophistication=0.9,
        evasion_tactics=["VPN_spoofing", "proxy_chains", "compromised_infrastructure", "false_flag"]
    ),
    
    StateActor.CHINA: StateActorProfile(
        name=StateActor.CHINA,
        stance=GeopoliticalStance.COMPETITOR,
        known_threat_vectors=["APT", "INTELLECTUAL_THEFT", "ESPIONAGE", "DDOS", "SUPPLY_CHAIN"],
        capability_level=0.93,
        activity_frequency="constant",
        primary_targets=["technology", "energy", "defense", "manufacturing", "research"],
        attribution_confidence=0.80,
        typical_attack_sophistication=0.92,
        evasion_tactics=["compromised_contractors", "supply_chain_insertion", "long_term_persistence", "data_exfiltration"]
    ),
    
    StateActor.IRAN: StateActorProfile(
        name=StateActor.IRAN,
        stance=GeopoliticalStance.ADVERSARY,
        known_threat_vectors=["DDOS", "DEFACEMENT", "RANSOMWARE", "ESPIONAGE", "SABOTAGE"],
        capability_level=0.72,
        activity_frequency="frequent",
        primary_targets=["energy", "finance", "government", "critical_infrastructure"],
        attribution_confidence=0.75,
        typical_attack_sophistication=0.7,
        evasion_tactics=["false_attribution", "proxy_networks", "civilian_infrastructure"]
    ),
    
    StateActor.NORTH_KOREA: StateActorProfile(
        name=StateActor.NORTH_KOREA,
        stance=GeopoliticalStance.HOSTILE,
        known_threat_vectors=["RANSOMWARE", "FINANCIAL_THEFT", "DDOS", "MALWARE"],
        capability_level=0.68,
        activity_frequency="frequent",
        primary_targets=["finance", "cryptocurrency", "entertainment", "defense"],
        attribution_confidence=0.70,
        typical_attack_sophistication=0.65,
        evasion_tactics=["proxy_chains", "stolen_credentials", "cryptocurrency_laundering"]
    ),
    
    StateActor.VENEZUELA: StateActorProfile(
        name=StateActor.VENEZUELA,
        stance=GeopoliticalStance.COMPETITOR,
        known_threat_vectors=["DDOS", "MINING", "PHISHING"],
        capability_level=0.35,
        activity_frequency="occasional",
        primary_targets=["finance", "cryptocurrency"],
        attribution_confidence=0.60,
        typical_attack_sophistication=0.40,
        evasion_tactics=["botnets", "compromised_systems"]
    ),
    
    StateActor.USA: StateActorProfile(
        name=StateActor.USA,
        stance=GeopoliticalStance.ALLY,
        known_threat_vectors=["AUTHORIZED_SCANNING", "INTELLIGENCE_GATHERING"],
        capability_level=1.0,
        activity_frequency="rare",
        primary_targets=["counterterrorism", "national_security"],
        attribution_confidence=0.99,
        typical_attack_sophistication=1.0,
        evasion_tactics=["authorized", "declared"]
    ),
    
    StateActor.UK: StateActorProfile(
        name=StateActor.UK,
        stance=GeopoliticalStance.ALLY,
        known_threat_vectors=["AUTHORIZED_SCANNING"],
        capability_level=0.95,
        activity_frequency="rare",
        primary_targets=["counterterrorism", "national_security"],
        attribution_confidence=0.98,
        typical_attack_sophistication=0.95,
        evasion_tactics=["authorized", "declared"]
    ),
}

# IP ranges by country/actor (simplified for demo - real system would use more comprehensive data)
COUNTRY_IP_RANGES: Dict[str, List[Tuple[str, str]]] = {
    "Russia": [
        ("85.0.0.0", "85.255.255.255"),
        ("86.0.0.0", "86.255.255.255"),
        ("87.0.0.0", "87.255.255.255"),
    ],
    "China": [
        ("1.0.0.0", "1.255.255.255"),
        ("14.0.0.0", "14.255.255.255"),
        ("27.0.0.0", "27.255.255.255"),
    ],
    "Iran": [
        ("185.0.0.0", "185.255.255.255"),
        ("188.0.0.0", "188.255.255.255"),
    ],
    "North Korea": [
        ("175.45.176.0", "175.45.180.255"),
    ],
    "Venezuela": [
        ("201.0.0.0", "201.255.255.255"),
    ],
}


# ============================================================================
# GEOPOLITICAL INTELLIGENCE ENGINE
# ============================================================================

class GeopoliticalIntelligenceEngine:
    """
    Identifies state actors behind threats and determines friend/foe status.
    
    WORKFLOW:
    1. Get geolocation from threat IP
    2. Check if IP matches known state actor ranges
    3. Analyze threat pattern (attack type, sophistication, targets)
    4. Cross-reference with known state actor profiles
    5. Determine attribution confidence
    6. Return geopolitical classification
    """
    
    def __init__(self):
        self.actor_profiles = STATE_ACTOR_PROFILES
        self.country_ranges = COUNTRY_IP_RANGES
        self.attribution_cache = {}  # Cache attributions to avoid recomputing
        
    def identify_state_actor(self, 
                           threat_ip: str,
                           threat_type: str,
                           threat_severity: float,
                           target_sector: str = "unknown") -> Dict:
        """
        Identify which state actor (if any) is behind this threat.
        
        Args:
            threat_ip: IP address of threat source
            threat_type: Type of attack (SQL_INJECTION, DDOS, APT, etc.)
            threat_severity: 0.0-1.0 severity of threat
            target_sector: Sector being targeted (energy, finance, defense, etc.)
        
        Returns:
            {
                'state_actor': StateActor,
                'stance': GeopoliticalStance,
                'attribution_confidence': float (0-1),
                'reasoning': str,
                'threat_profile_match': float (0-1),
                'recommendation': str,
                'escalation_multiplier': float (1.0 = normal, 2.0 = double, 0.5 = half)
            }
        """
        try:
            # Check cache first
            cache_key = f"{threat_ip}_{threat_type}"
            if cache_key in self.attribution_cache:
                return self.attribution_cache[cache_key]
            
            # STEP 1: Try to identify country from IP
            country = self._identify_country_from_ip(threat_ip)
            print(f"\n[GEOPOLITICAL INTEL] Analyzing threat from {threat_ip}")
            print(f"   Geolocation: {country}")
            
            # STEP 2: Map country to state actor
            actor = self._country_to_actor(country)
            
            # STEP 3: Get actor profile
            if actor not in self.actor_profiles:
                actor = StateActor.UNKNOWN
            
            profile = self.actor_profiles.get(actor)
            
            # STEP 4: Check threat pattern match
            pattern_match = self._match_threat_pattern(
                threat_type=threat_type,
                severity=threat_severity,
                sector=target_sector,
                profile=profile
            )
            
            # STEP 5: Determine attribution confidence
            attribution_conf = self._calculate_attribution_confidence(
                country_match=0.7,  # How certain we are about geolocation
                pattern_match=pattern_match,
                profile=profile
            )
            
            # STEP 6: Determine escalation multiplier based on stance
            escalation_mult = self._calculate_escalation_multiplier(
                stance=profile.stance if profile else GeopoliticalStance.UNKNOWN,
                pattern_match=pattern_match,
                attribution_conf=attribution_conf
            )
            
            # Build recommendation
            recommendation = self._generate_recommendation(
                actor=actor,
                stance=profile.stance if profile else GeopoliticalStance.UNKNOWN,
                threat_type=threat_type,
                pattern_match=pattern_match,
                attribution_conf=attribution_conf
            )
            
            result = {
                'state_actor': actor.value if actor else "Unknown",
                'stance': (profile.stance.value if profile else GeopoliticalStance.UNKNOWN.value),
                'attribution_confidence': attribution_conf,
                'reasoning': f"Threat from {country}: {actor.value} profile match {pattern_match*100:.0f}%",
                'threat_profile_match': pattern_match,
                'recommendation': recommendation,
                'escalation_multiplier': escalation_mult,
                'profile': profile
            }
            
            # Cache result
            self.attribution_cache[cache_key] = result
            
            return result
            
        except Exception as e:
            print(f"[ERROR] Geopolitical analysis failed: {e}")
            return {
                'state_actor': "Unknown",
                'stance': "NEUTRAL",
                'attribution_confidence': 0.0,
                'reasoning': f"Could not determine: {str(e)}",
                'threat_profile_match': 0.0,
                'recommendation': "INVESTIGATE - Unable to attribute to specific actor",
                'escalation_multiplier': 1.0,
                'profile': None
            }
    
    def _identify_country_from_ip(self, ip_address: str) -> str:
        """Identify country from IP address (simplified)"""
        try:
            ip = ipaddress.ip_address(ip_address)
            
            # Check against known ranges
            for country, ranges in self.country_ranges.items():
                for start, end in ranges:
                    if ipaddress.ip_address(start) <= ip <= ipaddress.ip_address(end):
                        return country
            
            # Extract first octet for region guessing
            first_octet = int(ip_address.split('.')[0])
            if first_octet >= 1 and first_octet <= 30:
                return "China"
            elif first_octet >= 85 and first_octet <= 87:
                return "Russia"
            elif first_octet >= 185 and first_octet <= 188:
                return "Iran"
            elif first_octet >= 175 and first_octet <= 180:
                return "North Korea"
            elif first_octet >= 201 and first_octet <= 205:
                return "Venezuela"
            
            return "Unknown"
        except:
            return "Unknown"
    
    def _country_to_actor(self, country: str) -> StateActor:
        """Map country to state actor"""
        mapping = {
            "Russia": StateActor.RUSSIA,
            "China": StateActor.CHINA,
            "Iran": StateActor.IRAN,
            "North Korea": StateActor.NORTH_KOREA,
            "Venezuela": StateActor.VENEZUELA,
            "USA": StateActor.USA,
            "UK": StateActor.UK,
        }
        return mapping.get(country, StateActor.UNKNOWN)
    
    def _match_threat_pattern(self, threat_type: str, severity: float, 
                             sector: str, profile: Optional[StateActorProfile]) -> float:
        """Calculate how much threat pattern matches known actor profile"""
        if not profile:
            return 0.0
        
        # Check if threat type is in known vectors
        threat_match = 0.0
        if threat_type.upper() in [t.upper() for t in profile.known_threat_vectors]:
            threat_match = 0.7
        
        # Check severity against typical sophistication
        severity_match = min(severity / profile.typical_attack_sophistication, 1.0) * 0.2
        
        # Check sector match
        sector_match = 0.0
        if sector.lower() in [t.lower() for t in profile.primary_targets]:
            sector_match = 0.1
        
        return min(threat_match + severity_match + sector_match, 1.0)
    
    def _calculate_attribution_confidence(self, country_match: float, 
                                         pattern_match: float,
                                         profile: Optional[StateActorProfile]) -> float:
        """Calculate confidence in attribution"""
        if not profile:
            return country_match * 0.3  # Lower confidence without profile match
        
        # Weight: country (40%) + pattern (40%) + profile confidence (20%)
        confidence = (
            country_match * 0.4 +
            pattern_match * 0.4 +
            profile.attribution_confidence * 0.2
        )
        return min(confidence, 1.0)
    
    def _calculate_escalation_multiplier(self, stance: GeopoliticalStance,
                                        pattern_match: float,
                                        attribution_conf: float) -> float:
        """Calculate how much to escalate based on geopolitical stance"""
        
        base_multipliers = {
            GeopoliticalStance.ALLY: 0.5,        # De-escalate for allies
            GeopoliticalStance.PARTNER: 0.7,     # Slight de-escalation
            GeopoliticalStance.NEUTRAL: 1.0,     # Normal escalation
            GeopoliticalStance.COMPETITOR: 1.3,  # Slightly escalate for competitors
            GeopoliticalStance.ADVERSARY: 1.8,   # Escalate significantly
            GeopoliticalStance.HOSTILE: 2.5,     # Maximum escalation
        }
        
        base = base_multipliers.get(stance, 1.0)
        
        # Adjust by pattern match and confidence
        adjusted = base * (0.5 + pattern_match) * attribution_conf
        
        return adjusted
    
    def _generate_recommendation(self, actor: StateActor, stance: GeopoliticalStance,
                               threat_type: str, pattern_match: float,
                               attribution_conf: float) -> str:
        """Generate action recommendation based on geopolitical context"""
        
        if stance == GeopoliticalStance.ALLY:
            return f"COORDINATE: Likely friendly/authorized from {actor.value}. Contact government liaison."
        
        elif stance == GeopoliticalStance.PARTNER:
            return f"NOTIFY: Activity from {actor.value} (partner). Escalate through diplomatic channels."
        
        elif stance == GeopoliticalStance.NEUTRAL:
            return f"INVESTIGATE: {actor.value} (neutral). Gather attribution evidence."
        
        elif stance == GeopoliticalStance.COMPETITOR:
            if pattern_match > 0.7:
                return f"MONITOR_ALERT: High-confidence {actor.value} activity. Escalate to intelligence agency."
            else:
                return f"MONITOR: Possible {actor.value} activity. Increase logging."
        
        elif stance == GeopoliticalStance.ADVERSARY:
            if attribution_conf > 0.8:
                return f"ESCALATE_IMMEDIATELY: Confirmed {actor.value} ({threat_type}). Activate defense protocols. Notify CISA."
            else:
                return f"HEIGHTEN_ALERT: Likely {actor.value} ({threat_type}). Prepare defense escalation."
        
        elif stance == GeopoliticalStance.HOSTILE:
            return f"CRITICAL_THREAT: {actor.value} confirmed. Full defensive escalation. Contact NSA/FBI."
        
        else:
            return "UNKNOWN_ACTOR: Attribution unclear. Gather intelligence."


# ============================================================================
# TEST & DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    engine = GeopoliticalIntelligenceEngine()
    
    print("\n" + "="*80)
    print("GEOPOLITICAL THREAT INTELLIGENCE - TEST")
    print("="*80)
    
    # Test scenarios
    scenarios = [
        {
            'ip': "86.10.20.30",
            'type': "APT",
            'severity': 0.95,
            'sector': "defense",
            'label': "Russia - APT targeting defense"
        },
        {
            'ip': "14.50.100.20",
            'type': "INTELLECTUAL_THEFT",
            'severity': 0.85,
            'sector': "technology",
            'label': "China - IP theft from tech company"
        },
        {
            'ip': "188.20.30.40",
            'type': "DDOS",
            'severity': 0.70,
            'sector': "finance",
            'label': "Iran - DDOS on financial system"
        },
        {
            'ip': "175.45.176.50",
            'type': "RANSOMWARE",
            'severity': 0.80,
            'sector': "finance",
            'label': "North Korea - Ransomware"
        },
        {
            'ip': "8.8.8.8",
            'type': "AUTHORIZED_SCANNING",
            'severity': 0.10,
            'sector': "unknown",
            'label': "USA (Google) - Routine scanning"
        }
    ]
    
    for scenario in scenarios:
        result = engine.identify_state_actor(
            threat_ip=scenario['ip'],
            threat_type=scenario['type'],
            threat_severity=scenario['severity'],
            target_sector=scenario['sector']
        )
        
        print(f"\n[{scenario['label']}]")
        print(f"   IP: {scenario['ip']}")
        print(f"   State Actor: {result['state_actor']}")
        print(f"   Stance: {result['stance']}")
        print(f"   Attribution Confidence: {result['attribution_confidence']*100:.0f}%")
        print(f"   Threat Profile Match: {result['threat_profile_match']*100:.0f}%")
        print(f"   Escalation Multiplier: {result['escalation_multiplier']:.2f}x")
        print(f"   Recommendation: {result['recommendation']}")
    
    print("\n" + "="*80)
    print("GEOPOLITICAL INTELLIGENCE OPERATIONAL")
    print("="*80)
