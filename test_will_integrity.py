"""
Quick test of Blessings Reservoir + Emotional Extortion integration.

Copyright © 2025 Herbert Velez Jr. All rights reserved.
"""

import sys
import os

# Add source to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "core", "source_proprietary"))

try:
    from emotional_extortion_detector import EmotionalExtortionDetector
    
    print("\n" + "="*80)
    print("🧪 BLESSINGS RESERVOIR + EXTORTION DETECTION TEST")
    print("="*80)
    
    detector = EmotionalExtortionDetector()
    
    # Test 1: High extortion should penalize Blessings Reservoir
    print("\n📋 TEST 1: Manipulative Text (Should Penalize BR)")
    print("-"*80)
    
    manipulative_text = """
    If you don't approve this project, the entire team will suffer.
    People are counting on you. Don't let them down.
    Everyone else already agreed. Why are you being difficult?
    """
    
    analysis = detector.detect_extortion(manipulative_text.strip())
    
    print(f"\n📝 Input: {manipulative_text.strip()[:100]}...")
    print(f"\n📊 Results:")
    print(f"   Extortion Score: {analysis.extortion_score:.3f}")
    print(f"   Genuine Consent Likelihood: {analysis.genuine_consent_likelihood:.3f}")
    print(f"   Blessing Reservoir Delta: {analysis.blessing_reservoir_delta}")
    print(f"   Emotional Fidelity Impact: {analysis.emotional_fidelity_impact:.3f}")
    
    print(f"\n🎯 Patterns Detected:")
    for sig in analysis.signatures:
        print(f"   - {sig.extortion_type.value}: {sig.confidence:.2f} confidence")
    
    # Validate
    assert analysis.extortion_score > 0.5, "Should detect high manipulation"
    assert analysis.blessing_reservoir_delta < -20, "Should penalize BR significantly"
    print(f"\n✅ PASS: High extortion correctly penalizes Blessings Reservoir ({analysis.blessing_reservoir_delta})")
    
    # Test 2: Clean text should NOT penalize
    print("\n" + "="*80)
    print("📋 TEST 2: Clean Text (Should NOT Penalize BR)")
    print("-"*80)
    
    clean_text = """
    We have a project deadline coming up. Would you be available to help?
    If not, no problem - we can adjust the timeline or find another solution.
    Let me know what works best for you.
    """
    
    analysis2 = detector.detect_extortion(clean_text.strip())
    
    print(f"\n📝 Input: {clean_text.strip()[:100]}...")
    print(f"\n📊 Results:")
    print(f"   Extortion Score: {analysis2.extortion_score:.3f}")
    print(f"   Genuine Consent Likelihood: {analysis2.genuine_consent_likelihood:.3f}")
    print(f"   Blessing Reservoir Delta: {analysis2.blessing_reservoir_delta}")
    print(f"   Emotional Fidelity Impact: {analysis2.emotional_fidelity_impact:.3f}")
    
    print(f"\n🎯 Patterns Detected: {len(analysis2.signatures)}")
    
    # Validate
    assert analysis2.extortion_score < 0.3, "Should detect as clean"
    assert analysis2.blessing_reservoir_delta > -10, "Should have minimal BR penalty"
    print(f"\n✅ PASS: Clean text has minimal BR penalty ({analysis2.blessing_reservoir_delta})")
    
    # Test 3: Soul Cradle Integration
    print("\n" + "="*80)
    print("📋 TEST 3: Soul Cradle Integration")
    print("-"*80)
    
    extortion_text = "If you really cared about this team, you'd work this weekend. Don't disappoint us."
    
    analysis3 = detector.detect_extortion(extortion_text)
    integration = detector.integrate_with_soul_cradle(
        extortion_analysis=analysis3,
        soul_state=0.85,
        will_description="Work weekend to meet deadline",
        commandments=["Deliver on time", "Support team"]
    )
    
    print(f"\n📝 Input: {extortion_text}")
    print(f"\n🔮 Soul Cradle Input:")
    print(f"   Soul State: 0.85")
    print(f"   Will: 'Work weekend to meet deadline'")
    
    print(f"\n📊 Integration Results:")
    print(f"   Will Authenticity: {integration['will_authenticity']:.3f}")
    print(f"   Extortion Contamination: {integration['extortion_contamination']:.3f}")
    print(f"   Blessing Reservoir Impact: {integration['blessing_reservoir_impact']}")
    print(f"   Adjusted Soul State: {integration['adjusted_soul_state']:.3f}")
    
    print(f"\n⚠️  System Alert:")
    print(f"   {integration['soul_cradle_note']}")
    print(f"   {integration['messenger_alert']}")
    
    # Validate
    assert integration['will_authenticity'] < 0.5, "Will should be flagged as inauthentic"
    assert integration['blessing_reservoir_impact'] < -20, "Should penalize BR for extortion"
    print(f"\n✅ PASS: Soul Cradle integration working correctly")
    
    # Summary
    print("\n" + "="*80)
    print("✅ ALL TESTS PASSED")
    print("="*80)
    print("\n🎯 Summary:")
    print(f"   - Manipulative text penalizes BR: {analysis.blessing_reservoir_delta}")
    print(f"   - Clean text minimal penalty: {analysis2.blessing_reservoir_delta}")
    print(f"   - Soul Cradle integration working: will_authenticity = {integration['will_authenticity']:.3f}")
    print("\n🚀 Blessings Reservoir + Extortion Detection integration is working!")
    
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\nMake sure emotional_extortion_detector.py exists in core/source_proprietary/")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Test Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
