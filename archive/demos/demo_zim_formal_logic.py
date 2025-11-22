#!/usr/bin/env python3
"""
Zim Formal Logic Demo
Shows corrected Zim notation in action (separate from Mythara core)

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from tests.test_zim_formal_logic import ZimFormalExpression, ZimAdapter


def main():
    print("=" * 70)
    print("Zim Formal Logic Extension Demo")
    print("Corrected Implementation - Separate from Mythara Core")
    print("=" * 70)
    print()
    
    # ===== EXAMPLE 1: Hospital Discharge Paradox =====
    print("📋 EXAMPLE 1: Hospital Discharge Paradox")
    print("-" * 70)
    
    print("\n🔵 Mythara Core (What frontline workers see):")
    print("  Expression A: 'Hospital policy requires discharge after 72 hours'")
    print("  Expression B: 'Patient will be homeless if discharged'")
    print("  Formula: P(t) = |0.9 - 0.8| × (1 - 0.0) = 0.1")
    
    print("\n🟢 Zim Extension (Optional formal verification):")
    
    # Create formal expressions
    policy = ZimFormalExpression(
        universal_quantifier=["Policy", "Insurance"],
        existential_operator="+",
        existential_quantifier=["Discharge", "Compliance"],
        negation=["Safety", "Stability"]
    )
    
    safety = ZimFormalExpression(
        universal_quantifier=["Safety", "Care"],
        existential_operator="+",
        existential_quantifier=["Retention", "Stability"],
        negation=["Discharge", "Compliance"]
    )
    
    print(f"  Policy (FOL):   {policy.to_first_order_logic()}")
    print(f"  Safety (FOL):   {safety.to_first_order_logic()}")
    print(f"\n  Policy (Prolog):\n    {policy.to_prolog()}")
    print(f"  Safety (Prolog):\n    {safety.to_prolog()}")
    print(f"\n  Policy (Lambda): {policy.to_lambda_calculus()}")
    print(f"  Safety (Lambda): {safety.to_lambda_calculus()}")
    
    contradiction = ZimAdapter.verify_contradiction(policy, safety)
    print(f"\n  ✅ Contradiction Detected: {contradiction}")
    
    # ===== EXAMPLE 2: Nonprofit Budget Paradox =====
    print("\n\n📋 EXAMPLE 2: Nonprofit Budget Paradox")
    print("-" * 70)
    
    print("\n🔵 Mythara Core:")
    print("  Expression A: 'Board requires 30% budget cuts for solvency'")
    print("  Expression B: 'Mission requires serving all community members'")
    print("  Formula: P(t) = |0.95 - 0.9| × (1 - 0.0) = 0.05")
    
    print("\n🟢 Zim Extension:")
    
    budget = ZimFormalExpression(
        universal_quantifier=["Budget", "Board"],
        existential_operator="+",
        existential_quantifier=["Cuts", "Solvency"],
        negation=["Programs", "Service"]
    )
    
    mission = ZimFormalExpression(
        universal_quantifier=["Mission", "Community"],
        existential_operator="+",
        existential_quantifier=["Programs", "Service"],
        negation=["Cuts", "Reduction"]
    )
    
    print(f"  Budget (FOL):  {budget.to_first_order_logic()}")
    print(f"  Mission (FOL): {mission.to_first_order_logic()}")
    
    contradiction = ZimAdapter.verify_contradiction(budget, mission)
    print(f"\n  ✅ Contradiction Detected: {contradiction}")
    
    # ===== EXAMPLE 3: Operator Comparison =====
    print("\n\n📋 EXAMPLE 3: Logical Operators")
    print("-" * 70)
    
    conjunction = ZimFormalExpression(
        universal_quantifier=["X"],
        existential_operator="+",  # AND
        existential_quantifier=["A", "B", "C"],
        negation=["D"]
    )
    
    disjunction = ZimFormalExpression(
        universal_quantifier=["X"],
        existential_operator="-",  # OR
        existential_quantifier=["A", "B", "C"],
        negation=["D"]
    )
    
    print("\n🔷 Conjunction (AND - all must be true):")
    print(f"  FOL: {conjunction.to_first_order_logic()}")
    print(f"  Meaning: For all X, exists (A AND B AND C) and NOT D")
    
    print("\n🔷 Disjunction (OR - at least one must be true):")
    print(f"  FOL: {disjunction.to_first_order_logic()}")
    print(f"  Meaning: For all X, exists (A OR B OR C) and NOT D")
    
    # ===== KEY INSIGHTS =====
    print("\n\n" + "=" * 70)
    print("🎯 KEY INSIGHTS")
    print("=" * 70)
    
    print("\n✅ Separation of Concerns:")
    print("   • Mythara Core: Plain English + Simple Math (P(t), R(t), U)")
    print("   • Zim Extension: Formal Logic (FOL, Prolog, Lambda)")
    print("   • Mythara works perfectly WITHOUT Zim")
    
    print("\n✅ Standard Notation:")
    print("   • First-Order Logic (FOL): ∀x ∃y ¬z")
    print("   • Prolog: forall([x], (y, \\+z))")
    print("   • Lambda Calculus: λx.λy.(z ∧ ¬w)")
    print("   • NOT custom Every()Any()Some()Non() syntax")
    
    print("\n✅ Use Cases:")
    print("   • Frontline Workers: Use Mythara core only")
    print("   • Researchers: Optional Zim export for formal verification")
    print("   • Automated Systems: Prolog/Coq integration via Zim")
    
    print("\n✅ Integration:")
    print("   • ZimAdapter.from_mythara_paradox() converts when needed")
    print("   • Bridge pattern maintains separation")
    print("   • No Zim dependency in Mythara core")
    
    print("\n" + "=" * 70)
    print("Demo Complete - Zim Logic Tested Successfully")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
