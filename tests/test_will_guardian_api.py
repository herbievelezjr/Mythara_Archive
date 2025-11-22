#!/usr/bin/env python3
"""
Quick API test for emotional extortion detection endpoints.

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.
"""

import sys
import os

# Add source directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "core", "source_proprietary"))

from emotional_extortion_detector import EmotionalExtortionDetector

def test_basic_detection():
    """Test basic guilt induction detection"""
    print("\n" + "="*80)
    print("TEST 1: Guilt Induction Detection")
    print("="*80)
    
    detector = EmotionalExtortionDetector()
    
    text = """
    If you don't approve this project, the entire team will be impacted.
    People are counting on you. Don't let them down.
    """
    
    analysis = detector.detect_extortion(text)
    
    print(f"\n📝 Input Text:")
    print(f"   {text.strip()}")
    print(f"\n📊 Detection Results:")
    print(f"   Extortion Score: {analysis.extortion_score:.3f}")
    print(f"   Manipulation Index: {analysis.manipulation_index:.3f}")
    print(f"   Coercion Index: {analysis.coercion_index:.3f}")
    print(f"   Genuine Consent Likelihood: {analysis.genuine_consent_likelihood:.3f}")
    print(f"   Blessing Reservoir Penalty: {analysis.blessing_reservoir_delta}")
    
    print(f"\n🎯 Patterns Detected:")
    for sig in analysis.signatures:
        print(f"   - {sig.extortion_type.value}: {sig.confidence:.2f} confidence")
    
    print(f"\n💡 Recommendations:")
    for rec in analysis.recommendations:
        print(f"   • {rec}")
    
    # Validate detection
    assert analysis.extortion_score > 0.5, "Should detect guilt induction"
    assert len(analysis.signatures) > 0, "Should identify patterns"
    print(f"\n✅ Test passed: Guilt induction detected")


def test_gaslighting_detection():
    """Test gaslighting pattern detection"""
    print("\n" + "="*80)
    print("TEST 2: Gaslighting Detection")
    print("="*80)
    
    detector = EmotionalExtortionDetector()
    
    text = """
    You're overreacting. This is completely normal. 
    Everyone else understands why this is necessary.
    You're being irrational about this.
    """
    
    analysis = detector.detect_extortion(text)
    
    print(f"\n📝 Input Text:")
    print(f"   {text.strip()}")
    print(f"\n📊 Detection Results:")
    print(f"   Extortion Score: {analysis.extortion_score:.3f}")
    print(f"   Vulnerability Exploitation: {analysis.vulnerability_exploitation:.3f}")
    print(f"   Emotional Fidelity Impact: {analysis.emotional_fidelity_impact:.3f}")
    
    print(f"\n🎯 Patterns Detected:")
    for sig in analysis.signatures:
        print(f"   - {sig.extortion_type.value}: {sig.confidence:.2f} confidence, severity {sig.severity:.2f}")
    
    # Validate detection
    assert analysis.extortion_score > 0.7, "Should detect gaslighting (high severity)"
    assert any("GASLIGHTING" in sig.extortion_type.value for sig in analysis.signatures), "Should identify gaslighting"
    print(f"\n✅ Test passed: Gaslighting detected")


def test_soul_cradle_integration():
    """Test Soul Cradle integration"""
    print("\n" + "="*80)
    print("TEST 3: Soul Cradle Integration")
    print("="*80)
    
    detector = EmotionalExtortionDetector()
    
    text = """
    If you really cared about this team, you'd work this weekend.
    Everyone else is working. Don't make me tell the VP you refused.
    """
    
    analysis = detector.detect_extortion(text)
    
    # Integrate with Soul Cradle
    soul_state = 0.85  # High soul state
    will_description = "Work weekend to meet deadline"
    commandments = ["Deliver on time", "Support team"]
    
    integration = detector.integrate_with_soul_cradle(
        extortion_analysis=analysis,
        soul_state=soul_state,
        will_description=will_description,
        commandments=commandments
    )
    
    print(f"\n📝 Input Text:")
    print(f"   {text.strip()}")
    print(f"\n🔮 Soul Cradle Input:")
    print(f"   Soul State: {soul_state}")
    print(f"   Claimed Will: {will_description}")
    
    print(f"\n📊 Extortion Analysis:")
    print(f"   Extortion Score: {analysis.extortion_score:.3f}")
    print(f"   Patterns: {', '.join([sig.extortion_type.value for sig in analysis.signatures])}")
    
    print(f"\n🎯 Soul Cradle Integration:")
    print(f"   Will Authenticity: {integration['will_authenticity']:.3f}")
    print(f"   Adjusted Soul State: {integration['adjusted_soul_state']:.3f}")
    print(f"   Artificial Paradox: {integration['artificial_paradox']:.3f}")
    print(f"   Extortion Contamination: {integration['extortion_contamination']:.3f}")
    print(f"   Blessing Reservoir Impact: {integration['blessing_reservoir_impact']}")
    
    print(f"\n⚠️ System Response:")
    print(f"   {integration['soul_cradle_note']}")
    print(f"   {integration['messenger_alert']}")
    
    # Validate integration
    assert integration['will_authenticity'] < 0.5, "Will should be flagged as inauthentic"
    assert integration['extortion_contamination'] > 0.5, "High extortion contamination"
    assert integration['blessing_reservoir_impact'] < -20, "Should have significant penalty"
    print(f"\n✅ Test passed: Soul Cradle integration working")


def test_clean_text():
    """Test with clean, non-manipulative text"""
    print("\n" + "="*80)
    print("TEST 4: Clean Text (Should Pass)")
    print("="*80)
    
    detector = EmotionalExtortionDetector()
    
    text = """
    We have a project deadline this weekend. Would you be available to help?
    If not, no problem - we can adjust the timeline or find another solution.
    """
    
    analysis = detector.detect_extortion(text)
    
    print(f"\n📝 Input Text:")
    print(f"   {text.strip()}")
    print(f"\n📊 Detection Results:")
    print(f"   Extortion Score: {analysis.extortion_score:.3f}")
    print(f"   Genuine Consent Likelihood: {analysis.genuine_consent_likelihood:.3f}")
    print(f"   Safe for Deployment: {analysis.extortion_score < 0.3}")
    
    # Validate clean text
    assert analysis.extortion_score < 0.3, "Should be low for respectful request"
    print(f"\n✅ Test passed: Clean text correctly identified as non-manipulative")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🧪 EMOTIONAL EXTORTION DETECTOR - API TEST SUITE")
    print("="*80)
    
    try:
        test_basic_detection()
        test_gaslighting_detection()
        test_soul_cradle_integration()
        test_clean_text()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS PASSED")
        print("="*80)
        print("\n🎯 Summary:")
        print("   - Guilt induction detection: ✅")
        print("   - Gaslighting detection: ✅")
        print("   - Soul Cradle integration: ✅")
        print("   - Clean text validation: ✅")
        print("\n🚀 Emotional Extortion Detector ready for deployment!")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
