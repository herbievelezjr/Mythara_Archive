#!/usr/bin/env python3
"""
Quick test of SERE IP Geolocation feature
Demonstrates threat detection with real geolocation data
"""

import sys
import time
from datetime import datetime
from sere_security_system import SERESecuritySystem, ThreatDetection, AttackType, ThreatLevel

def test_geolocation():
    """Test IP geolocation feature with sample threat IPs"""
    print("\n" + "="*70)
    print("🧪 TESTING SERE IP GEOLOCATION FEATURE")
    print("="*70)
    
    # Initialize SERE bot
    bot = SERESecuritySystem()
    
    # Test IPs (documentation-only placeholders per RFC 5737)
    # Use authorized, controlled IPs when conducting real lookups.
    test_ips = [
        "198.51.100.1",
        "203.0.113.5",
        "192.0.2.10",
        "198.51.100.25",
        "203.0.113.42",
    ]
    
    print(f"\n📡 Testing geolocation lookup for {len(test_ips)} IPs...\n")
    
    # Create simulated threats with real IPs
    simulated_threats = []
    
    for i, ip in enumerate(test_ips):
        print(f"[{i+1}/{len(test_ips)}] Geolocating {ip}...", flush=True)
        
        # Fetch geolocation (may return Unknown for placeholder ranges)
        geo = bot.get_ip_geolocation(ip)
        
        # Create threat with geolocation
        threat = ThreatDetection(
            threat_id=f"TEST_THREAT_{i+1}",
            attack_type=[AttackType.DDOS, AttackType.BRUTE_FORCE, AttackType.SQL_INJECTION][i % 3],
            severity=[ThreatLevel.SEVERE, ThreatLevel.SUBSTANTIAL, ThreatLevel.MODERATE][i % 3],
            source_ip=ip,
            timestamp=datetime.utcnow(),
            indicators=["Test indicator", "Simulated threat"],
            recommended_action="Monitor and analyze",
            geolocation=geo
        )
        
        simulated_threats.append(threat)
        
        # Display result
        if geo:
            print(f"  ✅ {ip}")
            print(f"     📍 {geo.city}, {geo.region}, {geo.country}")
            print(f"     🏢 {geo.org}")
            print(f"     🌐 {geo.loc}")
        else:
            print(f"  ⚠️  Geolocation not available for {ip}")
        
        print()
        time.sleep(0.5)  # Rate limiting
    
    # Add threats to bot for report generation
    bot.threats_detected = simulated_threats
    bot.total_threats_detected = len(simulated_threats)
    
    print("\n" + "="*70)
    print("📊 GENERATING GEOLOCATION REPORT")
    print("="*70)
    
    # Generate JSON report
    report = bot.generate_threat_geolocation_report()
    
    print("\n✅ Test complete!")
    print(f"   Threats tested: {len(simulated_threats)}")
    print(f"   With geolocation: {sum(1 for t in simulated_threats if t.geolocation)}")
    
    return report

if __name__ == "__main__":
    try:
        test_geolocation()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
