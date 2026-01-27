#!/usr/bin/env python3
"""
Quick test to demonstrate humorous messages in S.E.R.E. bot
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sere_security_system import SERESecuritySystem, AttackType, ThreatDetection, ThreatLevel
from datetime import datetime
import random

def test_humor():
    """Test the humorous messages in various phases"""
    print("🎭 Testing S.E.R.E. Bot Humor System")
    print("="*50)

    bot = SERESecuritySystem()

    # Test 1: Force some threats to trigger detection humor
    print("\n1. Testing Threat Detection Humor:")
    print("-"*30)

    # Create some fake threats
    threats = [
        ThreatDetection(
            threat_id="TEST_001",
            attack_type=AttackType.DDOS,
            severity=ThreatLevel.SEVERE,
            source_ip="192.168.1.100",
            timestamp=datetime.utcnow(),
            indicators=["High traffic volume", "Suspicious patterns"],
            recommended_action="Block traffic"
        ),
        ThreatDetection(
            threat_id="TEST_002",
            attack_type=AttackType.SQL_INJECTION,
            severity=ThreatLevel.MODERATE,
            source_ip="10.0.0.50",
            timestamp=datetime.utcnow(),
            indicators=["SQL keywords detected", "Database access attempt"],
            recommended_action="Sanitize input"
        )
    ]

    # Manually trigger the humorous detection (simulate what happens in vigilant_patrol)
    funny_detection_messages = [
        f"🚨 ALERT! {len(threats)} digital delinquents spotted lurking in the shadows!",
        f"🎭 Oh no! {len(threats)} cyber clowns trying to crash the party!",
        f"👾 {len(threats)} virtual villains detected! Time to show them the door!",
        f"🤡 {len(threats)} mischievous malware monkeys causing trouble!",
        f"🦹 {len(threats)} sneaky hackers playing hide and seek!",
        f"🎪 {len(threats)} threat trapeze artists swinging through your network!",
        f"🐱‍👤 {len(threats)} digital ninjas attempting a sneak attack!",
    ]

    print(f"\n{random.choice(funny_detection_messages)}")
    print("🛡️ Deploying the S.E.R.E. smackdown protocol!")

    # Test 2: Force neutralization humor
    print("\n2. Testing Threat Neutralization Humor:")
    print("-"*30)

    funny_neutralization_messages = [
        "🎉 Threats neutralized! They didn't stand a chance!",
        "💥 Boom! Cyber threats sent packing with a digital wedgie!",
        "🎊 Threats eliminated! Back to digital peace and quiet!",
        "🎯 Target practice complete! Threats neutralized!",
        "🏆 Victory! All threats have been defeated!",
        "🎪 Show's over! Threats escorted out of the building!",
        "🍿 Movie's over! Threats have left the theater!",
    ]

    print(f"\n{random.choice(funny_neutralization_messages)}")

    # Test 3: Force evasion humor
    print("\n3. Testing Evasion Phase Humor:")
    print("-"*30)

    funny_success_messages = [
        "    ✓ Evasion successful - threat did a digital backflip!",
        "    ✓ Evasion successful - hacker sent to the penalty box!",
        "    ✓ Evasion successful - threat got rickrolled into oblivion!",
        "    ✓ Evasion successful - cyber intruder shown the exit!",
        "    ✓ Evasion successful - threat got the S.E.R.E. special treatment!",
    ]

    funny_failure_messages = [
        "    ✗ Evasion failed - this threat needs backup dancers!",
        "    ✗ Evasion failed - calling in the resistance reinforcements!",
        "    ✗ Evasion failed - threat too slippery, time for plan B!",
        "    ✗ Evasion failed - escalating to the big guns!",
        "    ✗ Evasion failed - threat dodged, but won't dodge forever!",
    ]

    # Show both success and failure examples
    print(f"{random.choice(funny_success_messages)}")
    print(f"{random.choice(funny_failure_messages)} - escalating to RESIST phase")

    # Test 4: Force resistance humor
    print("\n4. Testing Resistance Phase Humor:")
    print("-"*30)

    funny_resistance_messages = [
        "    ✓ Resistance deployed - threat got the firewall rule injection treatment!",
        "    ✓ Countermeasure active - ip blacklist update blocking the bad guys!",
        "    ✓ Defense engaged - traffic throttling making threats cry!",
        "    ✓ Resistance successful - connection termination sent intruders packing!",
        "    ✓ Active defense - port closure turning threats into toast!",
    ]

    print(f"{random.choice(funny_resistance_messages)}")
    print("    ✓ Resistance effectiveness: 85.7%")

    # Test 5: Force escape humor
    print("\n5. Testing Escape Phase Humor:")
    print("-"*30)

    funny_escape_messages = [
        "  → Emergency failsafe deploying - things are getting serious!",
        "  → Activating escape protocols - time to bail gracefully!",
        "  → Emergency mode engaged - we're getting out of dodge!",
        "  → Failsafe activation - preparing for the great escape!",
        "  → Critical protocols online - escape plan initiated!",
    ]

    funny_data_messages = [
        "  → Preserving critical data - don't lose the good stuff!",
        "  → Data backup engaged - saving our digital bacon!",
        "  → Critical data preservation - keeping the important bits safe!",
        "  → Data integrity check - making sure nothing gets corrupted!",
        "  → Backup protocols active - data is our precious!",
    ]

    funny_completion_messages = [
        "✓ Escape protocol complete - we lived to fight another day!",
        "✓ Emergency escape successful - threat contained, data safe!",
        "✓ Escape maneuver complete - dodged a bullet (or a cyber bullet)!",
        "✓ Failsafe protocols executed - system integrity preserved!",
        "✓ Escape successful - back to the fight with all data intact!",
    ]

    print(f"{random.choice(funny_escape_messages)}")
    print(f"{random.choice(funny_data_messages)}")
    print("    ✓ Data integrity: 100%")
    print(f"{random.choice(funny_completion_messages)}")

    # Test 6: Force survival mode humor
    print("\n6. Testing Survival Mode Humor:")
    print("-"*30)

    funny_survival_measures = [
        "  ✓ Redundant systems online - we've got backups for our backups!",
        "  ✓ Auto-healing enabled - self-repairing like a digital Wolverine!",
        "  ✓ Resource conservation active - we're going green (and secure)!",
        "  ✓ Fail-over ready - if one fails, another takes over!",
        "  ✓ Emergency power reserves - batteries not included, but we have them!",
    ]

    funny_attack_messages = [
        "  ⚠️  Incoming: DDoS Attack - looks like trouble!",
        "  ⚠️  Alert: SQL Injection trying to sneak in!",
        "  ⚠️  Warning: Malware attempting a hostile takeover!",
        "  ⚠️  Heads up: Ransomware causing digital mischief!",
        "  ⚠️  Intruder alert: Phishing detected!",
    ]

    funny_survival_messages = [
        "     ✓ System maintained - we shrugged it off!",
        "     ✓ Attack survived - that tickled!",
        "     ✓ Defense held - threat bounced right off!",
        "     ✓ System intact - attack was no match!",
        "     ✓ Survived! - threat sent packing!",
    ]

    funny_completion_messages = [
        "✓ Survival mode complete - we made it through the storm!",
        "✓ Survival successful - system integrity preserved!",
        "✓ Survival mode ended - we're still standing tall!",
        "✓ Maximum resilience achieved - threats couldn't break us!",
        "✓ Survival complete - back to normal operations!",
    ]

    print("  Survival measures:")
    for measure in funny_survival_measures[:3]:  # Show a few
        print(measure)

    print(f"\n{random.choice(funny_attack_messages)}")
    print("     → Surviving attack...")
    print(f"{random.choice(funny_survival_messages)}")

    print(f"\n{random.choice(funny_completion_messages)}")
    print("  Attacks survived: 3")
    print("  System integrity: 100%")

    print("\n" + "="*50)
    print("🎭 Humor System Test Complete!")
    print("Your S.E.R.E. bot is now entertainingly secure! 🤖⚔️😂")

if __name__ == "__main__":
    test_humor()