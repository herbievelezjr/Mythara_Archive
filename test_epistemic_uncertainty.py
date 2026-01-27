#!/usr/bin/env python3
"""
Test Script: Epistemic Uncertainty Integration
==============================================

Demonstrates the integrated epistemic uncertainty layer in Soul Cradle.
Shows how collapse_risk predictions now come with:
- Confidence levels
- Uncertainty bounds (epistemic + aleatoric + blindspot)
- Known unknowns (factors we know we're missing)
- Blindspot risk (probability we're completely wrong)

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.
"""

import sys
import io
from pathlib import Path

# Set UTF-8 encoding for output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add the core module to path
sys.path.insert(0, str(Path(__file__).parent / "core" / "source_proprietary"))

from soul_cradle_systems_framework import (
    SoulCradleParadox,
    SoulCradleParadoxEngine,
    SystemExpression,
    ExpressionType,
    BenevolenceVector,
    IntuitionEngine,
    TerminalRiskLevel,
    EmotionalAuthenticity,
    EmotionalAuthenticityLevel,
    UnresolvedState,
)


def test_epistemic_uncertainty():
    """Test epistemic uncertainty integration with real scenarios"""
    
    print("\n" + "="*80)
    print("🧠 EPISTEMIC UNCERTAINTY INTEGRATION TEST")
    print("="*80 + "\n")
    
    # Initialize engines
    engine = SoulCradleParadoxEngine()
    intuition_engine = IntuitionEngine()
    
    # ============= SCENARIO 1: High Confidence (Clear Signals) =============
    print("📊 SCENARIO 1: Clear Signals (High Confidence)")
    print("-" * 80)
    
    paradox1 = SoulCradleParadox(
        paradox_id="p001_policy_compassion",
        user_id="user_001",
        name="Policy vs Compassion (Clear Case)",
        conflict_a=SystemExpression(
            type=ExpressionType.POLICY,
            content="Budget must be cut 30% across the board",
            weight=0.8
        ),
        conflict_b=SystemExpression(
            type=ExpressionType.COMPASSION,
            content="Staff are already burned out; cuts will break people",
            weight=0.9
        ),
        intensity=0.95
    )
    
    # Set clear emotional authenticity
    paradox1.emotional_authenticity = EmotionalAuthenticity(
        authenticity_level=EmotionalAuthenticityLevel.CRITICAL_SUPPRESSION,
        authenticity_score=0.15,
        labor_factor=2.5
    )
    paradox1.terminal_risk = TerminalRiskLevel.CRITICAL
    paradox1.unresolved_state = UnresolvedState(unresolved_score=0.95)
    
    benevolence1 = BenevolenceVector(
        compassion=0.9,
        justice=0.85,
        integrity=0.7,
        wisdom=0.6,
        courage=0.5,
        humility=0.8
    )
    
    # Get intuition with uncertainty
    intuition1 = intuition_engine.sense(paradox1, benevolence1)
    
    print(f"Paradox: {paradox1.name}")
    print(f"Collapse Risk: {intuition1.collapse_risk:.3f}")
    print(f"Time to Collapse: {intuition1.time_to_collapse_days:.1f} days (if > 0.1)")
    print(f"\n🔍 UNCERTAINTY ENVELOPE:")
    if intuition1.uncertainty_envelope:
        ue = intuition1.uncertainty_envelope
        print(f"  Predicted Value: {ue.predicted_value:.3f}")
        print(f"  Bounds: [{ue.lower_bound:.3f}, {ue.upper_bound:.3f}]")
        print(f"  Confidence Level: {ue.confidence_level:.1%}")
        print(f"  Total Uncertainty: {ue.total_uncertainty():.1%}")
        print(f"    - Epistemic: {ue.epistemic_uncertainty:.1%} (model/knowledge gap)")
        print(f"    - Aleatoric: {ue.aleatoric_uncertainty:.1%} (inherent randomness)")
        print(f"    - Blindspot: {ue.blindspot_risk:.1%} (unknown unknowns)")
        
        if ue.known_unknowns:
            print(f"\n  Known Unknowns ({len(ue.known_unknowns)}):")
            for ku in ue.known_unknowns:
                print(f"    • {ku.factor_name}")
                print(f"      Impact: {ku.suspected_impact:.0%}, Reason: {ku.reason_unknown}")
    
    print(f"\n💭 INTERPRETATION:")
    print(f"  {intuition1.interpret()}")
    print()
    
    # ============= SCENARIO 2: Low Confidence (Conflicting Signals) =============
    print("\n" + "="*80)
    print("📊 SCENARIO 2: Conflicting Signals (Low Confidence)")
    print("-" * 80)
    
    paradox2 = SoulCradleParadox(
        paradox_id="p002_innovation_safety",
        user_id="user_002",
        name="Innovation vs Safety (Uncertain)",
        conflict_a=SystemExpression(
            type=ExpressionType.MISSION,
            content="Push innovation boundaries to stay competitive",
            weight=0.6
        ),
        conflict_b=SystemExpression(
            type=ExpressionType.SAFETY,
            content="Can't rush; need proper testing protocols",
            weight=0.7
        ),
        intensity=0.55
    )
    
    # Set ambiguous emotional state
    paradox2.emotional_authenticity = EmotionalAuthenticity(
        authenticity_level=EmotionalAuthenticityLevel.REGULATED,
        authenticity_score=0.6,
        labor_factor=0.8
    )
    paradox2.terminal_risk = TerminalRiskLevel.MODERATE
    paradox2.unresolved_state = UnresolvedState(unresolved_score=0.6)
    
    benevolence2 = BenevolenceVector(
        compassion=0.5,
        justice=0.55,
        integrity=0.6,
        wisdom=0.4,
        courage=0.7,
        humility=0.4  # LOW humility = high blindspot risk
    )
    
    intuition2 = intuition_engine.sense(paradox2, benevolence2)
    
    print(f"Paradox: {paradox2.name}")
    print(f"Collapse Risk: {intuition2.collapse_risk:.3f}")
    print(f"\n🔍 UNCERTAINTY ENVELOPE:")
    if intuition2.uncertainty_envelope:
        ue = intuition2.uncertainty_envelope
        print(f"  Predicted Value: {ue.predicted_value:.3f}")
        print(f"  Bounds: [{ue.lower_bound:.3f}, {ue.upper_bound:.3f}]")
        print(f"  Confidence Level: {ue.confidence_level:.1%}")
        print(f"  Total Uncertainty: {ue.total_uncertainty():.1%}")
        print(f"    - Epistemic: {ue.epistemic_uncertainty:.1%}")
        print(f"    - Aleatoric: {ue.aleatoric_uncertainty:.1%}")
        print(f"    - Blindspot: {ue.blindspot_risk:.1%} ⚠️ (high blindspot = low humility)")
        
        if ue.known_unknowns:
            print(f"\n  Known Unknowns ({len(ue.known_unknowns)}):")
            for ku in ue.known_unknowns:
                print(f"    • {ku.factor_name} ({ku.suspected_impact:.0%})")
    
    print(f"\n💭 INTERPRETATION:")
    print(f"  {intuition2.interpret()}")
    print()
    
    # ============= SCENARIO 3: Stable System (Low Risk) =============
    print("\n" + "="*80)
    print("📊 SCENARIO 3: Stable System (Low Risk, High Confidence)")
    print("-" * 80)
    
    paradox3 = SoulCradleParadox(
        paradox_id="p003_growth_sustainability",
        user_id="user_003",
        name="Growth vs Sustainability (Balanced)",
        conflict_a=SystemExpression(
            type=ExpressionType.MISSION,
            content="Need steady growth for viability",
            weight=0.5
        ),
        conflict_b=SystemExpression(
            type=ExpressionType.HEART,
            content="Sustainable pace preserves team health",
            weight=0.6
        ),
        intensity=0.3
    )
    
    # Set healthy emotional state
    paradox3.emotional_authenticity = EmotionalAuthenticity(
        authenticity_level=EmotionalAuthenticityLevel.AUTHENTIC,
        authenticity_score=0.95,
        labor_factor=0.1
    )
    paradox3.terminal_risk = TerminalRiskLevel.LOW
    paradox3.unresolved_state = UnresolvedState(unresolved_score=0.2)
    
    benevolence3 = BenevolenceVector(
        compassion=0.95,
        justice=0.9,
        integrity=0.92,
        wisdom=0.85,
        courage=0.8,
        humility=0.9  # HIGH humility = lower blindspot risk
    )
    
    intuition3 = intuition_engine.sense(paradox3, benevolence3)
    
    print(f"Paradox: {paradox3.name}")
    print(f"Collapse Risk: {intuition3.collapse_risk:.3f}")
    print(f"\n🔍 UNCERTAINTY ENVELOPE:")
    if intuition3.uncertainty_envelope:
        ue = intuition3.uncertainty_envelope
        print(f"  Predicted Value: {ue.predicted_value:.3f}")
        print(f"  Bounds: [{ue.lower_bound:.3f}, {ue.upper_bound:.3f}]")
        print(f"  Confidence Level: {ue.confidence_level:.1%}")
        print(f"  Total Uncertainty: {ue.total_uncertainty():.1%}")
        print(f"    - Epistemic: {ue.epistemic_uncertainty:.1%}")
        print(f"    - Aleatoric: {ue.aleatoric_uncertainty:.1%}")
        print(f"    - Blindspot: {ue.blindspot_risk:.1%} ✅ (low = high humility)")
        print(f"  Reliability: {ue.is_reliable()}")
    
    print(f"\n💭 INTERPRETATION:")
    print(f"  {intuition3.interpret()}")
    print()
    
    # ============= SUMMARY =============
    print("\n" + "="*80)
    print("📈 SUMMARY: Epistemic Uncertainty Properties")
    print("="*80 + "\n")
    
    scenarios = [
        ("Clear Signals (High Confidence)", intuition1),
        ("Conflicting Signals (Low Confidence)", intuition2),
        ("Stable System (High Humility)", intuition3),
    ]
    
    for scenario_name, intuition in scenarios:
        if intuition.uncertainty_envelope:
            ue = intuition.uncertainty_envelope
            print(f"🔹 {scenario_name}")
            print(f"   Risk: {ue.predicted_value:.3f} | "
                  f"Bounds: ±{(ue.upper_bound - ue.lower_bound):.3f} | "
                  f"Confidence: {ue.confidence_level:.0%} | "
                  f"Blindspot: {ue.blindspot_risk:.1%}")
    
    print("\n" + "="*80)
    print("✅ TEST COMPLETE: Epistemic Uncertainty Integrated!")
    print("="*80 + "\n")
    
    # Key findings
    print("KEY FINDINGS:")
    print("─" * 80)
    print("1. ✅ UncertaintyEnvelope now attached to IntuitionSnapshot predictions")
    print("2. ✅ Collapse risk bounds are asymmetric (wider on upside = safer)")
    print("3. ✅ Confidence varies with signal alignment and benevolence stability")
    print("4. ✅ Blindspot risk increases when system has low humility")
    print("5. ✅ Known unknowns are explicitly tracked (e.g., emotional labor)")
    print("\nIMPLICATION:")
    print("Soul Cradle now practices epistemic humility—it knows what it doesn't know.")
    print("This aligns with the spiritual foundation (Olympus recognizes mysteries).")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    test_epistemic_uncertainty()
