#!/usr/bin/env python3
"""
SERE Bot Comprehensive Geopolitical Actors Database
====================================================

Complete global state actor profiles including:
- Hostile State Actors (Russia, China, Iran, North Korea)
- Adversarial States (Syria, Cuba, Belarus, Myanmar)
- Competitors (Israel, India, Pakistan, Brazil, Mexico)
- Partners & Allies (NATO, Five Eyes, EU, ASEAN, etc.)
- Critical Infrastructure Allies (Singapore, Japan, South Korea, Australia)

ATTRIBUTION REFERENCE:
- MITRE ATT&CK for known threat groups
- CISA alerts for state-sponsored threats
- Five Eyes intelligence assessments
- Open-source cyber threat intelligence

Copyright 2025 Herbert Velez Jr. All rights reserved.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple
from datetime import datetime


class GeopoliticalStance(str, Enum):
    """Global relationship stances"""
    CRITICAL_ALLY = "CRITICAL_ALLY"     # Five Eyes, NATO core
    ALLY = "ALLY"                        # NATO, close partners
    PARTNER = "PARTNER"                  # Friendly nations
    NEUTRAL = "NEUTRAL"                  # Unaligned
    COMPETITOR = "COMPETITOR"            # Strategic competitors
    ADVERSARY = "ADVERSARY"              # Hostile but constrained
    HOSTILE = "HOSTILE"                  # Maximum hostility
    ROGUE = "ROGUE"                      # Unpredictable/isolated


class ThreatCapability(str, Enum):
    """Threat capability levels"""
    ELITE = "ELITE"              # 95-100/100
    ADVANCED = "ADVANCED"        # 85-95/100
    SOPHISTICATED = "SOPHISTICATED"  # 70-85/100
    MODERATE = "MODERATE"        # 50-70/100
    LIMITED = "LIMITED"          # 30-50/100
    MINIMAL = "MINIMAL"          # <30/100


@dataclass
class StateActorProfile:
    """Comprehensive state actor profile"""
    name: str
    country_codes: List[str]           # ISO country codes
    stance: GeopoliticalStance
    capability: ThreatCapability
    activity_level: str                # constant, frequent, occasional, rare
    known_groups: List[str]            # APT28, APT29, Lazarus, etc.
    known_vectors: List[str]           # Attack types
    primary_targets: List[str]         # Sectors
    motivation: str                    # espionage, financial, political, etc.
    attribution_confidence: float      # 0-1
    infrastructure: List[str]          # ASNs, IP ranges, hosting providers
    evasion_tactics: List[str]         # Methods they use
    alliance_members: List[str]        # Allied actors
    typical_sophistication: float      # 0-1
    escalation_multiplier: float       # 0.5-2.5x
    intelligence_rating: str           # HIGH, MEDIUM, LOW confidence in profiles
    last_major_incident: str           # Date of last known major attack
    notes: str = ""


# ============================================================================
# GLOBAL STATE ACTOR DATABASE
# ============================================================================

GLOBAL_STATE_ACTORS: Dict[str, StateActorProfile] = {
    
    # ========================================================================
    # CRITICAL ALLIES (Five Eyes + NATO Core)
    # ========================================================================
    
    "USA": StateActorProfile(
        name="United States",
        country_codes=["US"],
        stance=GeopoliticalStance.CRITICAL_ALLY,
        capability=ThreatCapability.ELITE,
        activity_level="authorized",
        known_groups=["NSA", "CISA", "FBI Cyber", "USCYBERCOM"],
        known_vectors=["authorized_scanning", "intelligence_gathering"],
        primary_targets=["counterterrorism", "national_security"],
        motivation="defense",
        attribution_confidence=0.99,
        infrastructure=["AS15169", "AS16509", "AS14061"],  # Google, AWS, Akamai
        evasion_tactics=["declared", "authorized", "coordination"],
        alliance_members=["UK", "Canada", "Australia", "New Zealand"],
        typical_sophistication=1.0,
        escalation_multiplier=0.5,
        intelligence_rating="HIGHEST",
        last_major_incident="N/A - authorized"
    ),
    
    "UK": StateActorProfile(
        name="United Kingdom",
        country_codes=["GB", "UK"],
        stance=GeopoliticalStance.CRITICAL_ALLY,
        capability=ThreatCapability.ELITE,
        activity_level="authorized",
        known_groups=["GCHQ", "UK National Crime Agency"],
        known_vectors=["authorized_scanning"],
        primary_targets=["counterterrorism", "national_security"],
        motivation="defense",
        attribution_confidence=0.98,
        infrastructure=["AS2856", "AS3352", "AS8452"],  # BT, Virgin, TalkTalk
        evasion_tactics=["authorized", "five_eyes_coordination"],
        alliance_members=["USA", "Canada", "Australia", "New Zealand"],
        typical_sophistication=0.95,
        escalation_multiplier=0.5,
        intelligence_rating="HIGHEST",
        last_major_incident="N/A - authorized"
    ),
    
    "Canada": StateActorProfile(
        name="Canada",
        country_codes=["CA"],
        stance=GeopoliticalStance.CRITICAL_ALLY,
        capability=ThreatCapability.ADVANCED,
        activity_level="rare",
        known_groups=["Canadian Centre for Cyber Security"],
        known_vectors=["authorized_scanning"],
        primary_targets=["national_security", "critical_infrastructure"],
        motivation="defense",
        attribution_confidence=0.98,
        infrastructure=["AS577", "AS701", "AS7922"],
        evasion_tactics=["authorized", "five_eyes"],
        alliance_members=["USA", "UK", "Australia", "New Zealand"],
        typical_sophistication=0.90,
        escalation_multiplier=0.5,
        intelligence_rating="HIGHEST",
        last_major_incident="N/A - authorized"
    ),
    
    "Australia": StateActorProfile(
        name="Australia",
        country_codes=["AU"],
        stance=GeopoliticalStance.CRITICAL_ALLY,
        capability=ThreatCapability.ADVANCED,
        activity_level="rare",
        known_groups=["Australian Signals Directorate"],
        known_vectors=["authorized_scanning"],
        primary_targets=["counterterrorism", "critical_infrastructure"],
        motivation="defense",
        attribution_confidence=0.98,
        infrastructure=["AS1221", "AS1200", "AS2914"],
        evasion_tactics=["authorized", "five_eyes"],
        alliance_members=["USA", "UK", "Canada", "New Zealand"],
        typical_sophistication=0.90,
        escalation_multiplier=0.5,
        intelligence_rating="HIGHEST",
        last_major_incident="N/A - authorized"
    ),
    
    "New_Zealand": StateActorProfile(
        name="New Zealand",
        country_codes=["NZ"],
        stance=GeopoliticalStance.CRITICAL_ALLY,
        capability=ThreatCapability.ADVANCED,
        activity_level="rare",
        known_groups=["Government Communications Security Bureau"],
        known_vectors=["authorized_scanning"],
        primary_targets=["counterterrorism", "critical_infrastructure"],
        motivation="defense",
        attribution_confidence=0.98,
        infrastructure=["AS1234", "AS9816", "AS2109"],
        evasion_tactics=["authorized", "five_eyes"],
        alliance_members=["USA", "UK", "Canada", "Australia"],
        typical_sophistication=0.90,
        escalation_multiplier=0.5,
        intelligence_rating="HIGHEST",
        last_major_incident="N/A - authorized"
    ),
    
    # ========================================================================
    # NATO ALLIES
    # ========================================================================
    
    "France": StateActorProfile(
        name="France",
        country_codes=["FR"],
        stance=GeopoliticalStance.ALLY,
        capability=ThreatCapability.ADVANCED,
        activity_level="rare",
        known_groups=["DGSE"],
        known_vectors=["authorized_ops"],
        primary_targets=["counterterrorism", "national_security"],
        motivation="defense",
        attribution_confidence=0.95,
        infrastructure=["AS3352", "AS15557", "AS12389"],
        evasion_tactics=["authorized"],
        alliance_members=["USA", "UK", "EU"],
        typical_sophistication=0.90,
        escalation_multiplier=0.6,
        intelligence_rating="HIGH",
        last_major_incident="N/A - authorized"
    ),
    
    "Germany": StateActorProfile(
        name="Germany",
        country_codes=["DE"],
        stance=GeopoliticalStance.ALLY,
        capability=ThreatCapability.ADVANCED,
        activity_level="rare",
        known_groups=["BSI", "BND"],
        known_vectors=["authorized_scanning"],
        primary_targets=["national_security"],
        motivation="defense",
        attribution_confidence=0.95,
        infrastructure=["AS3352", "AS12634", "AS6830"],
        evasion_tactics=["authorized"],
        alliance_members=["USA", "EU", "NATO"],
        typical_sophistication=0.90,
        escalation_multiplier=0.6,
        intelligence_rating="HIGH",
        last_major_incident="N/A - authorized"
    ),
    
    "Japan": StateActorProfile(
        name="Japan",
        country_codes=["JP"],
        stance=GeopoliticalStance.ALLY,
        capability=ThreatCapability.ADVANCED,
        activity_level="rare",
        known_groups=["NICT", "Ministry of Defense"],
        known_vectors=["authorized_scanning"],
        primary_targets=["national_security"],
        motivation="defense",
        attribution_confidence=0.95,
        infrastructure=["AS2507", "AS2914", "AS7684"],
        evasion_tactics=["authorized"],
        alliance_members=["USA", "Australia", "South_Korea"],
        typical_sophistication=0.90,
        escalation_multiplier=0.6,
        intelligence_rating="HIGH",
        last_major_incident="N/A - authorized"
    ),
    
    "South_Korea": StateActorProfile(
        name="South Korea",
        country_codes=["KR"],
        stance=GeopoliticalStance.ALLY,
        capability=ThreatCapability.ADVANCED,
        activity_level="rare",
        known_groups=["National Intelligence Service"],
        known_vectors=["authorized_ops"],
        primary_targets=["north_korea_monitoring"],
        motivation="defense",
        attribution_confidence=0.94,
        infrastructure=["AS3786", "AS9318", "AS4766"],
        evasion_tactics=["authorized"],
        alliance_members=["USA", "Japan"],
        typical_sophistication=0.88,
        escalation_multiplier=0.6,
        intelligence_rating="HIGH",
        last_major_incident="N/A - authorized"
    ),
    
    "NATO": StateActorProfile(
        name="NATO Members (Collective)",
        country_codes=["NATO"],
        stance=GeopoliticalStance.ALLY,
        capability=ThreatCapability.ADVANCED,
        activity_level="rare",
        known_groups=["CCDCOE", "NATO Cyber Operations Centre"],
        known_vectors=["authorized_defense"],
        primary_targets=["collective_defense"],
        motivation="collective_defense",
        attribution_confidence=0.95,
        infrastructure=["SHARED"],
        evasion_tactics=["coordinated", "authorized"],
        alliance_members=["USA", "UK", "France", "Germany", "Canada"],
        typical_sophistication=0.90,
        escalation_multiplier=0.6,
        intelligence_rating="HIGH",
        last_major_incident="N/A - authorized"
    ),
    
    "EU": StateActorProfile(
        name="European Union",
        country_codes=["EU"],
        stance=GeopoliticalStance.PARTNER,
        capability=ThreatCapability.ADVANCED,
        activity_level="rare",
        known_groups=["ENISA"],
        known_vectors=["authorized_coordination"],
        primary_targets=["critical_infrastructure"],
        motivation="defense",
        attribution_confidence=0.90,
        infrastructure=["SHARED"],
        evasion_tactics=["coordinated"],
        alliance_members=["USA", "UK"],
        typical_sophistication=0.85,
        escalation_multiplier=0.7,
        intelligence_rating="HIGH",
        last_major_incident="N/A - authorized"
    ),
    
    # ========================================================================
    # CRITICAL PARTNERS (Strategic Importance)
    # ========================================================================
    
    "Israel": StateActorProfile(
        name="Israel",
        country_codes=["IL"],
        stance=GeopoliticalStance.PARTNER,
        capability=ThreatCapability.ELITE,
        activity_level="frequent",
        known_groups=["Unit 8200", "Israeli Cyber Directorate"],
        known_vectors=["APT_operations", "espionage"],
        primary_targets=["iran", "hezbollah", "hamas"],
        motivation="regional_security",
        attribution_confidence=0.85,
        infrastructure=["AS15003", "AS12453", "AS16252"],
        evasion_tactics=["advanced_techniques", "false_flag"],
        alliance_members=["USA", "Saudi_Arabia"],
        typical_sophistication=0.95,
        escalation_multiplier=0.7,
        intelligence_rating="HIGH",
        last_major_incident="2021-SolarWinds_related_ops"
    ),
    
    "India": StateActorProfile(
        name="India",
        country_codes=["IN"],
        stance=GeopoliticalStance.PARTNER,
        capability=ThreatCapability.ADVANCED,
        activity_level="occasional",
        known_groups=["RAW", "C-DOC"],
        known_vectors=["espionage", "defensive_operations"],
        primary_targets=["pakistan", "china", "terror_groups"],
        motivation="regional_security",
        attribution_confidence=0.75,
        infrastructure=["AS4788", "AS10029", "AS6293"],
        evasion_tactics=["advanced_techniques"],
        alliance_members=["USA", "Japan", "Australia"],
        typical_sophistication=0.85,
        escalation_multiplier=0.75,
        intelligence_rating="MEDIUM-HIGH",
        last_major_incident="2020-Pakistan_ops"
    ),
    
    "Singapore": StateActorProfile(
        name="Singapore",
        country_codes=["SG"],
        stance=GeopoliticalStance.PARTNER,
        capability=ThreatCapability.ADVANCED,
        activity_level="rare",
        known_groups=["CSA", "ISD"],
        known_vectors=["critical_infrastructure_defense"],
        primary_targets=["regional_security"],
        motivation="defense",
        attribution_confidence=0.90,
        infrastructure=["AS3786", "AS9394", "AS6453"],
        evasion_tactics=["authorized"],
        alliance_members=["USA", "Singapore"],
        typical_sophistication=0.85,
        escalation_multiplier=0.7,
        intelligence_rating="HIGH",
        last_major_incident="N/A"
    ),
    
    # ========================================================================
    # HOSTILE STATE ACTORS (Maximum Threat)
    # ========================================================================
    
    "Russia": StateActorProfile(
        name="Russia (Russian Federation)",
        country_codes=["RU"],
        stance=GeopoliticalStance.ADVERSARY,
        capability=ThreatCapability.ELITE,
        activity_level="constant",
        known_groups=["APT28", "APT29", "Cozy Bear", "Fancy Bear", "Turla", "Gamaredon"],
        known_vectors=["APT", "DDOS", "phishing", "malware", "ransomware", "data_exfiltration", "supply_chain"],
        primary_targets=["energy", "finance", "defense", "government", "elections", "infrastructure"],
        motivation="geopolitical", 
        attribution_confidence=0.85,
        infrastructure=["AS12389", "AS28645", "AS48920", "AS35000"],
        evasion_tactics=["VPN_spoofing", "proxy_chains", "compromised_infrastructure", "false_flag"],
        alliance_members=["Belarus", "Syria"],
        typical_sophistication=0.92,
        escalation_multiplier=1.8,
        intelligence_rating="HIGHEST",
        last_major_incident="2022-Ukraine_cyberwarfare"
    ),
    
    "China": StateActorProfile(
        name="China (PRC)",
        country_codes=["CN"],
        stance=GeopoliticalStance.COMPETITOR,
        capability=ThreatCapability.ELITE,
        activity_level="constant",
        known_groups=["APT1", "Comment Crew", "Equation Group", "APT10", "APT40", "Lazarus_affiliated"],
        known_vectors=["espionage", "IP_theft", "supply_chain", "DDOS", "APT"],
        primary_targets=["technology", "energy", "defense", "manufacturing", "research", "government"],
        motivation="economic_espionage",
        attribution_confidence=0.80,
        infrastructure=["AS4134", "AS9929", "AS7922", "AS37963"],
        evasion_tactics=["compromised_contractors", "supply_chain_insertion", "long_term_persistence"],
        alliance_members=["Russia", "Iran"],
        typical_sophistication=0.94,
        escalation_multiplier=1.3,
        intelligence_rating="HIGHEST",
        last_major_incident="2021-Microsoft_Exchange_breach"
    ),
    
    "Iran": StateActorProfile(
        name="Iran (Islamic Republic)",
        country_codes=["IR"],
        stance=GeopoliticalStance.ADVERSARY,
        capability=ThreatCapability.SOPHISTICATED,
        activity_level="frequent",
        known_groups=["APT33", "APT34", "Wizard Spider", "MuddyWater"],
        known_vectors=["DDOS", "defacement", "ransomware", "espionage", "sabotage"],
        primary_targets=["energy", "finance", "government", "critical_infrastructure", "regional"],
        motivation="political_sabotage",
        attribution_confidence=0.75,
        infrastructure=["AS39798", "AS44843", "AS48693"],
        evasion_tactics=["false_attribution", "proxy_networks", "civilian_infrastructure"],
        alliance_members=["Russia", "Syria", "Hezbollah"],
        typical_sophistication=0.72,
        escalation_multiplier=1.8,
        intelligence_rating="HIGH",
        last_major_incident="2019-Saudi_Aramco_attack"
    ),
    
    "North_Korea": StateActorProfile(
        name="North Korea (DPRK)",
        country_codes=["KP"],
        stance=GeopoliticalStance.HOSTILE,
        capability=ThreatCapability.SOPHISTICATED,
        activity_level="frequent",
        known_groups=["Lazarus Group", "Hidden Cobra", "Kimsuky"],
        known_vectors=["ransomware", "financial_theft", "DDOS", "malware"],
        primary_targets=["finance", "cryptocurrency", "entertainment", "defense"],
        motivation="financial_espionage",
        attribution_confidence=0.70,
        infrastructure=["AS38019", "AS45839", "AS201965"],
        evasion_tactics=["proxy_chains", "stolen_credentials", "cryptocurrency_laundering"],
        alliance_members=["Russia", "Iran"],
        typical_sophistication=0.68,
        escalation_multiplier=2.5,
        intelligence_rating="HIGH",
        last_major_incident="2017-WannaCry_attack"
    ),
    
    "Syria": StateActorProfile(
        name="Syria",
        country_codes=["SY"],
        stance=GeopoliticalStance.ADVERSARY,
        capability=ThreatCapability.MODERATE,
        activity_level="occasional",
        known_groups=["Electronic Army of Syria"],
        known_vectors=["DDOS", "defacement", "espionage"],
        primary_targets=["regional_opponents", "israel", "opposition"],
        motivation="political_sabotage",
        attribution_confidence=0.60,
        infrastructure=["AS29386", "AS45839"],
        evasion_tactics=["false_flag", "proxy_networks"],
        alliance_members=["Russia", "Iran"],
        typical_sophistication=0.50,
        escalation_multiplier=1.5,
        intelligence_rating="MEDIUM",
        last_major_incident="2013-Syrian_Electronic_Army"
    ),
    
    "Cuba": StateActorProfile(
        name="Cuba",
        country_codes=["CU"],
        stance=GeopoliticalStance.ADVERSARY,
        capability=ThreatCapability.MODERATE,
        activity_level="occasional",
        known_groups=["Cuban Intelligence"],
        known_vectors=["espionage", "DDOS"],
        primary_targets=["usa", "regional"],
        motivation="political",
        attribution_confidence=0.55,
        infrastructure=["AS27725", "AS53360"],
        evasion_tactics=["hidden_infrastructure"],
        alliance_members=["Russia"],
        typical_sophistication=0.45,
        escalation_multiplier=1.4,
        intelligence_rating="MEDIUM",
        last_major_incident="2015-Cuba_relations"
    ),
    
    "Belarus": StateActorProfile(
        name="Belarus",
        country_codes=["BY"],
        stance=GeopoliticalStance.ADVERSARY,
        capability=ThreatCapability.MODERATE,
        activity_level="frequent",
        known_groups=["Belarusian Intelligence"],
        known_vectors=["espionage", "political"],
        primary_targets=["regional", "opposition"],
        motivation="political_control",
        attribution_confidence=0.65,
        infrastructure=["AS6679", "AS20473"],
        evasion_tactics=["russian_coordination"],
        alliance_members=["Russia"],
        typical_sophistication=0.55,
        escalation_multiplier=1.6,
        intelligence_rating="MEDIUM",
        last_major_incident="2020-Presidential_elections"
    ),
    
    "Myanmar": StateActorProfile(
        name="Myanmar (Burma)",
        country_codes=["MM"],
        stance=GeopoliticalStance.COMPETITOR,
        capability=ThreatCapability.LIMITED,
        activity_level="occasional",
        known_groups=["Myanmar Military Cyber Unit"],
        known_vectors=["DDOS", "surveillance"],
        primary_targets=["opposition", "civil_society"],
        motivation="political_control",
        attribution_confidence=0.50,
        infrastructure=["AS45839", "AS55662"],
        evasion_tactics=["local_infrastructure"],
        alliance_members=["China", "Russia"],
        typical_sophistication=0.35,
        escalation_multiplier=1.2,
        intelligence_rating="LOW-MEDIUM",
        last_major_incident="2021-Military_coup"
    ),
    
    # ========================================================================
    # COMPETITIVE/STRATEGIC COMPETITORS
    # ========================================================================
    
    "Pakistan": StateActorProfile(
        name="Pakistan",
        country_codes=["PK"],
        stance=GeopoliticalStance.COMPETITOR,
        capability=ThreatCapability.MODERATE,
        activity_level="occasional",
        known_groups=["ISI_Cyber"],
        known_vectors=["espionage", "APT"],
        primary_targets=["india", "regional"],
        motivation="strategic_advantage",
        attribution_confidence=0.60,
        infrastructure=["AS9541", "AS24499"],
        evasion_tactics=["proxy_networks"],
        alliance_members=["China"],
        typical_sophistication=0.60,
        escalation_multiplier=1.2,
        intelligence_rating="MEDIUM",
        last_major_incident="2016-India_operations"
    ),
    
    "Venezuela": StateActorProfile(
        name="Venezuela",
        country_codes=["VE"],
        stance=GeopoliticalStance.COMPETITOR,
        capability=ThreatCapability.LIMITED,
        activity_level="occasional",
        known_groups=["GNB Cyber"],
        known_vectors=["DDOS", "cryptocurrency_mining"],
        primary_targets=["opposition", "finance"],
        motivation="political_control",
        attribution_confidence=0.50,
        infrastructure=["AS27725", "AS265419"],
        evasion_tactics=["botnets"],
        alliance_members=["Russia", "Cuba", "Iran"],
        typical_sophistication=0.40,
        escalation_multiplier=1.2,
        intelligence_rating="LOW-MEDIUM",
        last_major_incident="2019-Power_grid"
    ),
    
    "Mexico": StateActorProfile(
        name="Mexico",
        country_codes=["MX"],
        stance=GeopoliticalStance.PARTNER,
        capability=ThreatCapability.LIMITED,
        activity_level="rare",
        known_groups=["CISEN", "Secretariat of Defense"],
        known_vectors=["intelligence_gathering"],
        primary_targets=["drug_trafficking", "organized_crime"],
        motivation="national_security",
        attribution_confidence=0.70,
        infrastructure=["AS8118", "AS27969"],
        evasion_tactics=["localized"],
        alliance_members=["USA"],
        typical_sophistication=0.50,
        escalation_multiplier=0.8,
        intelligence_rating="MEDIUM",
        last_major_incident="N/A"
    ),
    
    "Brazil": StateActorProfile(
        name="Brazil",
        country_codes=["BR"],
        stance=GeopoliticalStance.PARTNER,
        capability=ThreatCapability.MODERATE,
        activity_level="rare",
        known_groups=["ABIN"],
        known_vectors=["intelligence_gathering"],
        primary_targets=["regional_security"],
        motivation="national_security",
        attribution_confidence=0.70,
        infrastructure=["AS4230", "AS27699"],
        evasion_tactics=["regional_infrastructure"],
        alliance_members=["USA", "regional_partners"],
        typical_sophistication=0.60,
        escalation_multiplier=0.8,
        intelligence_rating="MEDIUM",
        last_major_incident="N/A"
    ),
    
    # ========================================================================
    # MISCELLANEOUS & EMERGING THREATS
    # ========================================================================
    
    "North_Korea_Affiliated": StateActorProfile(
        name="North Korea Affiliated Groups",
        country_codes=["KP"],
        stance=GeopoliticalStance.HOSTILE,
        capability=ThreatCapability.SOPHISTICATED,
        activity_level="frequent",
        known_groups=["Lazarus", "BlueNoroff", "Andariel"],
        known_vectors=["ransomware", "malware", "financial_theft"],
        primary_targets=["global_finance", "cryptocurrency"],
        motivation="financial_gain",
        attribution_confidence=0.72,
        infrastructure=["AS38019", "AS45839"],
        evasion_tactics=["distributed_proxies"],
        alliance_members=["North_Korea"],
        typical_sophistication=0.70,
        escalation_multiplier=2.4,
        intelligence_rating="HIGH",
        last_major_incident="2021-Colonial_Pipeline"
    ),
    
    "Unknown": StateActorProfile(
        name="Unknown Actor",
        country_codes=["XX"],
        stance=GeopoliticalStance.NEUTRAL,
        capability=ThreatCapability.MINIMAL,
        activity_level="unknown",
        known_groups=[],
        known_vectors=[],
        primary_targets=[],
        motivation="unknown",
        attribution_confidence=0.0,
        infrastructure=[],
        evasion_tactics=[],
        alliance_members=[],
        typical_sophistication=0.0,
        escalation_multiplier=1.0,
        intelligence_rating="NO_DATA",
        last_major_incident="N/A"
    ),
}

# ============================================================================
# HELPER LOOKUPS
# ============================================================================

# Country code to actor name mapping
COUNTRY_CODE_TO_ACTOR = {code: name for name, profile in GLOBAL_STATE_ACTORS.items() 
                         for code in profile.country_codes}

# Stance to escalation multiplier
STANCE_ESCALATION_MAP = {
    GeopoliticalStance.CRITICAL_ALLY: 0.5,
    GeopoliticalStance.ALLY: 0.6,
    GeopoliticalStance.PARTNER: 0.8,
    GeopoliticalStance.NEUTRAL: 1.0,
    GeopoliticalStance.COMPETITOR: 1.3,
    GeopoliticalStance.ADVERSARY: 1.8,
    GeopoliticalStance.HOSTILE: 2.5,
    GeopoliticalStance.ROGUE: 2.8,
}

# Known threat groups to actors mapping
THREAT_GROUP_TO_ACTOR = {
    "APT28": "Russia",
    "APT29": "Russia",
    "Cozy Bear": "Russia",
    "Fancy Bear": "Russia",
    "Turla": "Russia",
    "Gamaredon": "Russia",
    "APT1": "China",
    "Comment Crew": "China",
    "APT10": "China",
    "APT40": "China",
    "APT33": "Iran",
    "APT34": "Iran",
    "MuddyWater": "Iran",
    "Lazarus": "North_Korea",
    "Hidden Cobra": "North_Korea",
    "Kimsuky": "North_Korea",
    "Electronic Army of Syria": "Syria",
    "Unit 8200": "Israel",
}


if __name__ == "__main__":
    # Print summary
    print("\n" + "="*80)
    print("COMPREHENSIVE GLOBAL STATE ACTOR DATABASE")
    print("="*80)
    
    # Count by stance
    by_stance = {}
    for actor, profile in GLOBAL_STATE_ACTORS.items():
        stance = profile.stance.value
        by_stance[stance] = by_stance.get(stance, 0) + 1
    
    print("\nACTORS BY STANCE:")
    for stance, count in sorted(by_stance.items()):
        print(f"  {stance}: {count}")
    
    # Total
    print(f"\nTOTAL STATE ACTORS: {len(GLOBAL_STATE_ACTORS)}")
    
    print("\n" + "="*80)
