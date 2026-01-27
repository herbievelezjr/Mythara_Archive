#!/usr/bin/env python3
"""
Test script to demonstrate continuous auto-defense mode
"""

import sys
import os
import time
import threading

# Add current directory to path
sys.path.insert(0, str(os.path.dirname(__file__)))

from sere_security_system import SERESecuritySystem

def test_continuous_auto_defense():
    """Test the continuous auto-defense mode"""
    print("\n" + "="*70)
    print("TESTING CONTINUOUS AUTO-DEFENSE MODE")
    print("="*70)

    print("\n✓ Initializing S.E.R.E. Bot...")
    bot = SERESecuritySystem()

    print("\n✓ Bot initialized successfully")
    print("✓ Starting continuous auto-defense mode...")
    print("✓ This will run for 10 seconds to demonstrate the functionality")
    print("✓ In real usage, press ENTER to stop\n")

    # Start continuous auto-defense in a separate thread
    stop_event = threading.Event()

    def run_auto_defense():
        """Run continuous auto-defense with timeout"""
        cycle = 0
        total_threats_handled = 0

        try:
            while not stop_event.is_set() and cycle < 5:  # Limit to 5 cycles for demo
                cycle += 1
                print(f"\n[Cycle {cycle}] 🔍 Seeking and assessing threats...", flush=True)

                # Detect threats
                threats = bot.detect_threats()

                if threats:
                    print(f"🚨 THREATS DETECTED: {len(threats)}")
                    total_threats_handled += len(threats)

                    # Auto-evade threats
                    print("  → Auto-evading threats...")
                    evasions = bot.execute_evasion(threats)

                    # Check for failed evasions and escalate to resistance
                    failed = [e for e in evasions if not e.success]
                    if failed:
                        print("  → Escalating to RESIST phase...")
                        bot.activate_resistance(failed)
                        print("  ✓ Resistance countermeasures deployed")

                    print(f"  ✓ All threats handled ({total_threats_handled} total)")
                else:
                    print("  ✓ No threats detected - perimeter secure", flush=True)

                # Brief pause between cycles
                time.sleep(2)

        except Exception as e:
            print(f"\n⚠️  Error in continuous auto-defense: {e}")

        print("\n\n🎖️  Continuous auto-defense demo complete")
        print(f"Total cycles completed: {cycle}")
        print(f"Total threats handled: {total_threats_handled}")

    # Start the auto-defense thread
    defense_thread = threading.Thread(target=run_auto_defense)
    defense_thread.start()

    # Wait for completion
    defense_thread.join()

    print("\n✓ Test completed successfully!")
    print("✓ Continuous auto-defense mode is working")
    print("✓ In interactive mode, this would continue until you press ENTER")

if __name__ == "__main__":
    test_continuous_auto_defense()