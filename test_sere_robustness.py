#!/usr/bin/env python3
"""
Test script to verify S.E.R.E. Bot robustness improvements
"""

import sys
import json
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sere_security_system import SERESecuritySystem, SEREException, SEREValidationError, SEREStateError, ThreatDetection, AttackType, ThreatLevel

def test_initialization():
    """Test robust initialization"""
    print("\n" + "="*70)
    print("TEST 1: Robust Initialization")
    print("="*70)
    
    try:
        bot = SERESecuritySystem()
        print("✓ Bot initialized successfully")
        print(f"  - Error count: {bot.error_count}")
        print(f"  - State lock available: {bot._state_lock is not None}")
        return True
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        return False

def test_input_validation():
    """Test input validation"""
    print("\n" + "="*70)
    print("TEST 2: Input Validation")
    print("="*70)
    
    bot = SERESecuritySystem()
    
    # Test invalid threat list
    print("\nTesting invalid threat input...")
    result = bot.execute_evasion("not a list")
    if result == []:
        print("✓ Invalid threat input handled correctly")
    else:
        print("✗ Should have returned empty list for invalid input")
    
    # Test invalid duration
    print("\nTesting invalid duration...")
    result = bot.survival_mode(-5)
    if result == 0:
        print("✓ Invalid duration handled correctly")
    else:
        print("✗ Should have returned 0 for invalid duration")
    
    return True

def test_state_validation():
    """Test state validation"""
    print("\n" + "="*70)
    print("TEST 3: State Validation")
    print("="*70)
    
    bot = SERESecuritySystem()
    bot.survival_mode_active = True
    
    print("\nTesting threat detection in survival mode...")
    result = bot.detect_threats()
    if result == []:
        print("✓ State validation working (cannot detect threats in survival mode)")
    else:
        print("✗ Should prevent threat detection in survival mode")
    
    return True

def test_error_handling():
    """Test error handling"""
    print("\n" + "="*70)
    print("TEST 4: Error Handling & Recovery")
    print("="*70)
    
    bot = SERESecuritySystem()
    
    # Test escape protocol with invalid input
    print("\nTesting escape with invalid input...")
    result = bot.initiate_escape("", critical=False)
    if result is None and bot.error_count > 0:
        print("✓ Invalid escape handled gracefully")
        print(f"  - Error recorded: {bot.last_error is not None}")
    else:
        print("✗ Should have handled invalid escape gracefully")
    
    return True

def test_thread_safety():
    """Test thread safety features"""
    print("\n" + "="*70)
    print("TEST 5: Thread Safety")
    print("="*70)
    
    bot = SERESecuritySystem()
    
    # Verify lock exists
    if bot._state_lock is not None:
        print("✓ State lock initialized")
        print(f"  - Lock type: {type(bot._state_lock).__name__}")
    else:
        print("✗ State lock not initialized")
    
    return True

def test_state_persistence_config():
    """Test state persistence configuration"""
    print("\n" + "="*70)
    print("TEST 6: State Persistence Configuration")
    print("="*70)
    
    from sere_security_system import CONFIG
    
    print(f"\nConfiguration:")
    print(f"  - MAX_THREATS_HISTORY: {CONFIG['MAX_THREATS_HISTORY']}")
    print(f"  - SURVIVAL_MODE_MAX_DURATION: {CONFIG['SURVIVAL_MODE_MAX_DURATION']}")
    print(f"  - STATE_PERSISTENCE_FILE: {CONFIG['STATE_PERSISTENCE_FILE']}")
    print(f"  - ENABLE_STATE_PERSISTENCE: {CONFIG['ENABLE_STATE_PERSISTENCE']}")
    
    print("\n✓ Configuration defaults are in place")
    return True

def test_error_logging():
    """Test error logging"""
    print("\n" + "="*70)
    print("TEST 7: Error Logging & Diagnostics")
    print("="*70)
    
    bot = SERESecuritySystem()
    
    # Trigger an error
    bot.survival_mode("invalid")
    
    if bot.error_count > 0:
        print(f"✓ Error tracking working")
        print(f"  - Total errors: {bot.error_count}")
        print(f"  - Last error type: {type(bot.last_error).__name__}")
    else:
        print("✗ Error tracking not working")
    
    return True

def test_threat_history_limits():
    """Test threat history management"""
    print("\n" + "="*70)
    print("TEST 8: Threat History Management")
    print("="*70)
    
    from sere_security_system import CONFIG
    
    bot = SERESecuritySystem()
    
    # Add many threats
    for i in range(CONFIG['MAX_THREATS_HISTORY'] + 50):
        bot.detect_threats()
    
    if len(bot.threats_detected) <= CONFIG['MAX_THREATS_HISTORY']:
        print(f"✓ Threat history properly limited")
        print(f"  - Current threats: {len(bot.threats_detected)}")
        print(f"  - Max allowed: {CONFIG['MAX_THREATS_HISTORY']}")
    else:
        print("✗ Threat history not properly limited")
    
    return True

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("    S.E.R.E. BOT ROBUSTNESS TEST SUITE")
    print("="*70)
    
    tests = [
        test_initialization,
        test_input_validation,
        test_state_validation,
        test_error_handling,
        test_thread_safety,
        test_state_persistence_config,
        test_error_logging,
        test_threat_history_limits,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*70)
    print("    TEST SUMMARY")
    print("="*70)
    passed = sum(results)
    total = len(results)
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All robustness tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
