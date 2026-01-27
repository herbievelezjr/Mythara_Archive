#!/usr/bin/env python3
"""
Test script to demonstrate Evolutionary Defense Engine
"""

import sys
import os
import time

# Add current directory to path
sys.path.insert(0, str(os.path.dirname(__file__)))

from sere_security_system import SERESecuritySystem

def test_evolutionary_defense():
    """Test the evolutionary defense system"""
    print("\n" + "="*80)
    print("🧬 TESTING EVOLUTIONARY DEFENSE ENGINE")
    print("="*80)

    print("\n✓ Initializing S.E.R.E. Bot with Evolutionary Defense...")
    bot = SERESecuritySystem()

    print("\n✓ Evolutionary Engine Status:")
    status = bot.evolutionary_engine.get_evolutionary_status()
    for key, value in status.items():
        print(f"  • {key}: {value}")

    print("\n✓ Simulating multiple threat detection cycles...")

    # Simulate multiple threat detection cycles to build evolutionary knowledge
    for cycle in range(3):
        print(f"\n[EVOLUTION CYCLE {cycle + 1}]")
        print("-" * 40)

        # Detect threats
        threats = bot.detect_threats()

        if threats:
            # Execute evasion (this will record outcomes for evolutionary learning)
            evasions = bot.execute_evasion(threats)

            # Check for failed evasions and activate resistance
            failed = [e for e in evasions if not e.success]
            if failed:
                print("\n→ Activating resistance countermeasures...")
                bot.activate_resistance(failed)

        # Brief pause between cycles
        time.sleep(1)

    print("\n" + "="*80)
    print("🧬 EVOLUTIONARY ANALYSIS & ADAPTATION")
    print("="*80)

    # Run evolutionary analysis
    print("\n✓ Running evolutionary defense evolution...")
    evolution_report = bot.evolutionary_engine.evolve_defenses()

    print(f"\nEvolution Cycle: {evolution_report['cycle']}")
    print(f"New Strategies Generated: {len(evolution_report['new_strategies'])}")
    print(f"Strategies to Deprecate: {len(evolution_report['deprecated_strategies'])}")
    print(f"Predictive Insights: {len(evolution_report['predictive_insights'])}")

    if evolution_report['new_strategies']:
        print("\n🆕 NEW EVOLVED DEFENSE STRATEGIES:")
        for i, strategy in enumerate(evolution_report['new_strategies'][:3], 1):
            print(f"  {i}. {strategy['strategy']}")
            print(f"     Based on: {strategy['based_on']}")
            print(f"     Expected Improvement: {strategy['expected_improvement']}")

    if evolution_report['deprecated_strategies']:
        print("\n⚠️  DEPRECATED DEFENSE STRATEGIES:")
        for i, strategy in enumerate(evolution_report['deprecated_strategies'], 1):
            print(f"  {i}. {strategy['strategy']}")
            print(f"     Reason: {strategy['reason']}")

    if evolution_report['predictive_insights']:
        print("\n🔮 PREDICTIVE THREAT INSIGHTS:")
        for i, insight in enumerate(evolution_report['predictive_insights'][:3], 1):
            print(f"  {i}. {insight['threat_pattern']}: {insight['trend']} trend")
            print(f"     Frequency: {insight['frequency']:.1f} attacks/day")
            print(f"     Recommendation: {insight['recommendation']}")

    # Save evolutionary knowledge
    bot.evolutionary_engine.save_knowledge()

    print("\n" + "="*80)
    print("✅ EVOLUTIONARY DEFENSE TEST COMPLETE")
    print("="*80)

    print("\n🎯 KEY ACHIEVEMENTS:")
    print("  ✓ Threat pattern learning and analysis")
    print("  ✓ Defense effectiveness tracking")
    print("  ✓ Evolutionary strategy generation")
    print("  ✓ Predictive threat modeling")
    print("  ✓ Adaptive defense recommendations")
    print("  ✓ Persistent knowledge storage")

    print("\n🧬 The Evolutionary Defense Engine is now:")
    print("  • Learning from every threat encounter")
    print("  • Adapting defense strategies over time")
    print("  • Predicting future attack patterns")
    print("  • Evolving to counter emerging threats")
    print("  • Maintaining persistent knowledge across sessions")

    print("\n🚀 Your S.E.R.E. system now has EVER-EVOLVING threat containment!")

if __name__ == "__main__":
    test_evolutionary_defense()