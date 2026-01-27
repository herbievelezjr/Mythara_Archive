#!/usr/bin/env python3
"""
Demo script showing the restored S.E.R.E. Threat Hierarchy Display

This demonstrates all major threat types in the comprehensive hierarchy:
- Man-in-the-Middle (MitM)
- DDoS Attacks
- Malware/Ransomware
- Zero-Day Exploits
- SQL Injection & XSS
- Brute Force & Phishing
"""

import sys
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

# Import threat detection structures
sys.path.insert(0, '.')
from sere_security_system import ThreatLevel, AttackType, ThreatDetection, GeoLocation

def demo_threat_hierarchy():
    """Demonstrate comprehensive threat hierarchy display"""
    
    print("\n" + "="*70)
    print("🛡️  S.E.R.E. THREAT HIERARCHY - DEMO")
    print("="*70)
    print("\nRestored comprehensive threat detection showing all major threat types:\n")
    
    # Create sample threats across all threat vectors
    demo_threats = [
        # Network Threats
        ThreatDetection(
            source_ip="192.168.1.50",
            attack_type=AttackType.MITM,
            severity=ThreatLevel.SEVERE,
            indicators=["ARP spoofing detected", "DNS interception"],
            confidence=0.85,
            timestamp=datetime.utcnow()
        ),
        ThreatDetection(
            source_ip="10.0.0.100",
            attack_type=AttackType.DDOS,
            severity=ThreatLevel.CRITICAL,
            indicators=["SYN flood", "Request rate: 50k/min"],
            confidence=0.95,
            timestamp=datetime.utcnow()
        ),
        ThreatDetection(
            source_ip="172.16.0.1",
            attack_type=AttackType.BRUTE_FORCE,
            severity=ThreatLevel.SUBSTANTIAL,
            indicators=["SSH login attempts", "Failed: 2341"],
            confidence=0.92,
            timestamp=datetime.utcnow()
        ),
        # System Threats
        ThreatDetection(
            source_ip="LOCAL",
            attack_type=AttackType.MALWARE,
            severity=ThreatLevel.SEVERE,
            indicators=["suspicious.exe", "Registry modification"],
            confidence=0.88,
            timestamp=datetime.utcnow()
        ),
        ThreatDetection(
            source_ip="LOCAL",
            attack_type=AttackType.RANSOMWARE,
            severity=ThreatLevel.CRITICAL,
            indicators=["File encryption", "Ransom note created"],
            confidence=0.99,
            timestamp=datetime.utcnow()
        ),
        ThreatDetection(
            source_ip="203.0.113.42",
            attack_type=AttackType.SQL_INJECTION,
            severity=ThreatLevel.SUBSTANTIAL,
            indicators=["SQL payload detected", "DB query: UNION SELECT"],
            confidence=0.87,
            timestamp=datetime.utcnow()
        ),
        ThreatDetection(
            source_ip="198.51.100.89",
            attack_type=AttackType.XSS,
            severity=ThreatLevel.MODERATE,
            indicators=["Script tag injection", "Cookie stealing attempt"],
            confidence=0.79,
            timestamp=datetime.utcnow()
        ),
        ThreatDetection(
            source_ip="192.0.2.5",
            attack_type=AttackType.PHISHING,
            severity=ThreatLevel.MODERATE,
            indicators=["Spoofed email domain", "Credential harvesting"],
            confidence=0.82,
            timestamp=datetime.utcnow()
        ),
    ]
    
    # Count threats by type
    threat_counts = {
        'MITM': 0,
        'DDOS': 0,
        'MALWARE': 0,
        'RANSOMWARE': 0,
        'PHISHING': 0,
        'SQL_INJECTION': 0,
        'XSS': 0,
        'BRUTE_FORCE': 0,
        'ZERO_DAY': 0
    }
    
    for threat in demo_threats:
        if threat.attack_type.value in threat_counts:
            threat_counts[threat.attack_type.value] += 1
    
    # Display threat vectors
    print("📡 NETWORK THREATS:")
    print(f"   🔗 Man-in-the-Middle (MitM):     {threat_counts['MITM']:3d} active")
    print(f"   💥 DDoS Attacks:                  {threat_counts['DDOS']:3d} active")
    print(f"   🔓 Brute Force Attempts:          {threat_counts['BRUTE_FORCE']:3d} active")
    
    print("\n💻 SYSTEM THREATS:")
    print(f"   🦠 Malware Detected:              {threat_counts['MALWARE']:3d} active")
    print(f"   🔐 Ransomware Instances:          {threat_counts['RANSOMWARE']:3d} active")
    print(f"   💣 Zero-Day Exploits:             {threat_counts['ZERO_DAY']:3d} active")
    
    print("\n🕸️  APPLICATION THREATS:")
    print(f"   💉 SQL Injection:                 {threat_counts['SQL_INJECTION']:3d} active")
    print(f"   <> Cross-Site Scripting (XSS):    {threat_counts['XSS']:3d} active")
    print(f"   📧 Phishing Campaigns:            {threat_counts['PHISHING']:3d} active")
    
    # Overall threat assessment
    total_active = sum(threat_counts.values())
    
    print("\n" + "="*70)
    print(f"⚠️  TOTAL ACTIVE THREATS: {total_active}")
    print("🔴 THREAT STATUS: CRITICAL ACTIVITY")
    
    # Detail view
    print("\n📊 THREAT DETAIL (All Detected):")
    for i, threat in enumerate(demo_threats, 1):
        print(f"\n   [{i}] {threat.attack_type.value}")
        print(f"       Source: {threat.source_ip}")
        print(f"       Severity: {threat.severity.name}")
        print(f"       Confidence: {threat.confidence*100:.0f}%")
        print(f"       Indicators: {', '.join(threat.indicators[:2])}")
    
    print("\n" + "="*70)
    print("\n✅ Comprehensive Threat Hierarchy Restored!")
    print("\nThe S.E.R.E. Bot now displays ALL major threat types:")
    print("  • Man-in-the-Middle (MitM) attacks")
    print("  • DDoS attacks")
    print("  • Malware detection")
    print("  • Ransomware threats")
    print("  • Zero-day exploits")
    print("  • SQL Injection attacks")
    print("  • Cross-Site Scripting (XSS)")
    print("  • Brute force attempts")
    print("  • Phishing campaigns")
    print("\nRun 'python sere_bot.py' to access the full S.E.R.E. threat detection system")
    print("="*70 + "\n")

if __name__ == '__main__':
    demo_threat_hierarchy()
