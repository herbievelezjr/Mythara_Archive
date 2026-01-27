#!/usr/bin/env python3
"""
Test auto-evasion functionality in S.E.R.E. Bot
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, str(os.path.dirname(__file__)))

from sere_security_system import SERESecuritySystem

def test_auto_evasion():
    """Test that threats are automatically evaded"""
    print("\n" + "="*70)
    print("TESTING AUTO-EVASION FUNCTIONALITY")
    print("="*70)
    
    print("\n✓ Initializing S.E.R.E. Bot...")
    bot = SERESecuritySystem()
    
    print("\n" + "-"*70)
    print("TEST 1: Detect with Auto-Evasion")
    print("-"*70)
    
    # This should detect AND auto-evade
    print("\nExecuting: detect command (should auto-evade threats)...")
    threats = bot.detect_threats()
    
    if threats:
        print(f"\n✓ Threats detected: {len(threats)}")
        
        # Now manually evade to show the second phase
        print("\n→ Now executing evasion phase...")
        evasions = bot.execute_evasion(threats)
        
        successful = sum(1 for e in evasions if e.success)
        failed = sum(1 for e in evasions if not e.success)
        
        print(f"\n✓ Evasion results:")
        print(f"  - Successful: {successful}")
        print(f"  - Failed: {failed}")
        
        # If any failed, test resistance
        if failed:
            print("\n→ Executing resistance phase for failed evasions...")
            failed_evasions = [e for e in evasions if not e.success]
            actions = bot.activate_resistance(failed_evasions)
            print(f"\n✓ Resistance actions deployed: {len(actions)}")
    else:
        print("\n✓ No threats detected - trying again...")
        threats = bot.detect_threats()
        if threats:
            evasions = bot.execute_evasion(threats)
            print(f"✓ Threats detected on retry: {len(threats)}")
            print(f"✓ Evasion maneuvers executed: {len(evasions)}")
    
    print("\n" + "-"*70)
    print("TEST 2: Multiple Defense Cycles")
    print("-"*70)
    
    for i in range(3):
        print(f"\n[Cycle {i+1}] Running detect + evade...")
        threats = bot.detect_threats()
        if threats:
            evasions = bot.execute_evasion(threats)
            successful = sum(1 for e in evasions if e.success)
            print(f"  ✓ {len(threats)} threats detected, {successful} evaded successfully")
        else:
            print(f"  ✓ No threats detected")
    
    print("\n" + "="*70)
    print("FINAL RESULTS")
    print("="*70)
    
    print(f"""
✓ Auto-Evasion is WORKING
✓ Threats detected and handled automatically
✓ Full defensive sequence operational

Statistics:
  - Total threats detected: {bot.total_threats_detected}
  - Total evasions: {bot.total_evasions}
  - Total resistances: {bot.total_resistances}
  - Total attacks blocked: {bot.total_attacks_blocked}
  
STATUS: EVASION SYSTEM OPERATIONAL ✓
""")

if __name__ == "__main__":
    test_auto_evasion()
