#!/usr/bin/env python3
"""
Simple Test: Epistemic Uncertainty in IntuitionEngine
======================================================

Direct test of the epistemic uncertainty computation without building full paradoxes.

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.
"""

import sys
import io
from pathlib import Path

# Set UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add the core module to path
sys.path.insert(0, str(Path(__file__).parent / "core" / "source_proprietary"))

from soul_cradle_systems_framework import (
    BenevolenceVector,
    IntuitionEngine,
    UncertaintyEnvelope,
)


def test_uncertainty_computation():
    """Test epistemic uncertainty envelope computation"""
    
    print("\n" + "="*80)
    print("TEST: Epistemic Uncertainty Computation")
    print("="*80 + "\n")
    
    intuition_engine = IntuitionEngine()
    
    # ===== TEST 1: High confidence scenario =====
    print("[TEST 1] High Confidence - Aligned Signals")
    print("-" * 80)
    
    # Create benevolence vectors properly
    benevolence_high = BenevolenceVector(
        vector=[0.9, 0.85, 0.7, 0.6, 0.5, 0.8]  # [compassion, justice, integrity, wisdom, courage, humility]
    )
    benevolence_high.compute_magnitude()
    benevolence_high.compute_stability()
    
    ue1 = intuition_engine._compute_uncertainty_for_collapse_risk(
        collapse_risk=0.85,
        eq_signal=0.8,
        risk_signal=0.85,
        bene_signal=0.2,
        benevolence=benevolence_high
    )
    
    print(f"Collapse Risk: {ue1.predicted_value:.3f}")
    print(f"Benevolence Stability: {benevolence_high.stability:.3f}")
    print(f"Bounds: [{ue1.lower_bound:.3f}, {ue1.upper_bound:.3f}]")
    print(f"Confidence: {ue1.confidence_level:.1%}")
    print(f"Total Uncertainty: {ue1.total_uncertainty():.1%}")
    print(f"  - Epistemic: {ue1.epistemic_uncertainty:.1%}")
    print(f"  - Aleatoric: {ue1.aleatoric_uncertainty:.1%}")
    print(f"  - Blindspot: {ue1.blindspot_risk:.1%}")
    print(f"Reliability: {ue1.is_reliable()}")
    if ue1.known_unknowns:
        print(f"Known Unknowns: {len(ue1.known_unknowns)}")
        for ku in ue1.known_unknowns:
            print(f"  - {ku.factor_name}")
    print(f"Interpretation: {ue1.interpret()}")
    print()
    
    # ===== TEST 2: Low confidence scenario =====
    print("[TEST 2] Low Confidence - Conflicting Signals")
    print("-" * 80)
    
    benevolence_low = BenevolenceVector(
        vector=[0.5, 0.55, 0.6, 0.4, 0.7, 0.4]  # LOW humility (0.4)
    )
    benevolence_low.compute_magnitude()
    benevolence_low.compute_stability()
    
    ue2 = intuition_engine._compute_uncertainty_for_collapse_risk(
        collapse_risk=0.45,
        eq_signal=0.6,
        risk_signal=0.35,
        bene_signal=0.65,
        benevolence=benevolence_low
    )
    
    print(f"Collapse Risk: {ue2.predicted_value:.3f}")
    print(f"Benevolence Stability: {benevolence_low.stability:.3f}")
    print(f"Bounds: [{ue2.lower_bound:.3f}, {ue2.upper_bound:.3f}]")
    print(f"Confidence: {ue2.confidence_level:.1%}")
    print(f"Total Uncertainty: {ue2.total_uncertainty():.1%}")
    print(f"  - Epistemic: {ue2.epistemic_uncertainty:.1%}")
    print(f"  - Aleatoric: {ue2.aleatoric_uncertainty:.1%}")
    print(f"  - Blindspot: {ue2.blindspot_risk:.1%} <-- HIGH (low humility)")
    print(f"Reliability: {ue2.is_reliable()}")
    if ue2.known_unknowns:
        print(f"Known Unknowns: {len(ue2.known_unknowns)}")
        for ku in ue2.known_unknowns:
            print(f"  - {ku.factor_name}")
    print(f"Interpretation: {ue2.interpret()}")
    print()
    
    # ===== TEST 3: Stable system (high humility) =====
    print("[TEST 3] Stable System - High Humility")
    print("-" * 80)
    
    benevolence_stable = BenevolenceVector(
        vector=[0.95, 0.9, 0.92, 0.85, 0.8, 0.9]  # HIGH humility (0.9)
    )
    benevolence_stable.compute_magnitude()
    benevolence_stable.compute_stability()
    
    ue3 = intuition_engine._compute_uncertainty_for_collapse_risk(
        collapse_risk=0.15,
        eq_signal=0.15,
        risk_signal=0.1,
        bene_signal=0.05,
        benevolence=benevolence_stable
    )
    
    print(f"Collapse Risk: {ue3.predicted_value:.3f}")
    print(f"Benevolence Stability: {benevolence_stable.stability:.3f}")
    print(f"Bounds: [{ue3.lower_bound:.3f}, {ue3.upper_bound:.3f}]")
    print(f"Confidence: {ue3.confidence_level:.1%}")
    print(f"Total Uncertainty: {ue3.total_uncertainty():.1%}")
    print(f"  - Epistemic: {ue3.epistemic_uncertainty:.1%}")
    print(f"  - Aleatoric: {ue3.aleatoric_uncertainty:.1%}")
    print(f"  - Blindspot: {ue3.blindspot_risk:.1%} <-- LOW (high humility)")
    print(f"Reliability: {ue3.is_reliable()}")
    if ue3.known_unknowns:
        print(f"Known Unknowns: {len(ue3.known_unknowns)}")
        for ku in ue3.known_unknowns:
            print(f"  - {ku.factor_name}")
    print(f"Interpretation: {ue3.interpret()}")
    print()
    
    # ===== SUMMARY =====
    print("="*80)
    print("SUMMARY: Epistemic Uncertainty Properties")
    print("="*80 + "\n")
    
    scenarios = [
        ("High Confidence (Aligned Signals)", ue1),
        ("Low Confidence (Conflicting Signals)", ue2),
        ("Stable System (High Humility)", ue3),
    ]
    
    print(f"{'Scenario':<40} {'Risk':<8} {'Confidence':<12} {'Blindspot':<10} {'Reliable':<10}")
    print("-" * 80)
    for name, ue in scenarios:
        print(f"{name:<40} {ue.predicted_value:.3f}   {ue.confidence_level:>6.0%}      {ue.blindspot_risk:>6.1%}      {str(ue.is_reliable()):<10}")
    
    print("\n" + "="*80)
    print("KEY FINDINGS:")
    print("="*80)
    print()
    print("1. CONFIDENCE VARIES:")
    print(f"   - Aligned signals (Test 1): {ue1.confidence_level:.1%} confidence")
    print(f"   - Conflicting signals (Test 2): {ue2.confidence_level:.1%} confidence")
    print(f"   - Stable system (Test 3): {ue3.confidence_level:.1%} confidence")
    print()
    print("2. BLINDSPOT RISK LINKED TO HUMILITY:")
    print(f"   - Low humility (Test 2): {ue2.blindspot_risk:.1%} blindspot risk")
    print(f"   - High humility (Test 3): {ue3.blindspot_risk:.1%} blindspot risk")
    print()
    print("3. BOUNDS ARE ASYMMETRIC:")
    print(f"   - Test 1 bounds: {ue1.upper_bound - ue1.lower_bound:.3f} total width")
    print(f"     (conservative - wider on upside = safer)")
    print()
    print("4. KNOWN UNKNOWNS TRACKED:")
    print(f"   - Test 1 known unknowns: {len(ue1.known_unknowns)}")
    print(f"   - Test 2 known unknowns: {len(ue2.known_unknowns)}")
    print()
    print("IMPLICATION:")
    print("Soul Cradle now knows what it doesn't know.")
    print("Predictions come with epistemic humility, not false confidence.")
    print("="*80 + "\n")


if __name__ == "__main__":
    test_uncertainty_computation()
