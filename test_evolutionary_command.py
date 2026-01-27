#!/usr/bin/env python3
"""
Test script for evolutionary defense command
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from sere_security_system import SERESecuritySystem

def test_evolutionary_command():
    """Test the evolutionary defense command"""
    print("🧬 Testing Evolutionary Defense Command")
    print("=" * 50)

    # Initialize bot
    bot = SERESecuritySystem()

    # Simulate some threat encounters first
    print("\n📊 Simulating threat encounters for learning...")

    # Simulate a few threat encounters
    test_threats = [
        {"attack_type": "phishing", "severity": "high", "source": "email"},
        {"attack_type": "malware", "severity": "critical", "source": "download"},
        {"attack_type": "ddos", "severity": "medium", "source": "network"}
    ]

    for threat in test_threats:
        print(f"  → Processing {threat['attack_type']} threat...")
        # Analyze threat
        insights = bot.evolutionary_engine.analyze_threat(threat)
        print(f"    Evolutionary insights: {insights}")

        # Record defense outcome
        bot.evolutionary_engine.record_defense_outcome(
            threat_type=threat["attack_type"],
            defense_used="Traffic dispersal protocol",
            success=True
        )

    print("\n🧬 Running evolutionary analysis...")
    print("-" * 30)

    # Run the evolve command
    try:
        result = bot.evolutionary_engine.evolve_defenses()
        print("✓ Evolution cycle completed")
        print(f"📈 New strategies generated: {len(result.get('new_strategies', []))}")
        print(f"🔮 Predictions made: {len(result.get('predictions', []))}")

        # Show some results
        if result.get('new_strategies'):
            print(f"\n🆕 New evolved strategy: {result['new_strategies'][0]}")

        if result.get('predictions'):
            print(f"🔮 Threat prediction: {result['predictions'][0]}")

    except Exception as e:
        print(f"❌ Error during evolution: {e}")

    print("\n✅ Evolutionary defense test completed")

if __name__ == "__main__":
    test_evolutionary_command()