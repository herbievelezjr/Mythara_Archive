"""
Test Soul Cradle Mathematical Framework
Validates formulas against edge cases to ensure math is not pseudo-science
"""

import re

def calculate_integrity_score(user_input: str) -> dict:
    """
    Soul Cradle Integrity Score Algorithm (CORRECTED VERSION)
    
    FIXED LOGIC:
    - Higher distress = higher paradox severity (not inverted)
    - Higher coercion = higher paradox severity
    - More contradictions = higher paradox severity
    - Paradox Score = weighted sum of all three factors
    """
    
    # STEP 1: Distress Detection (0.0 = calm, 1.0 = extreme distress)
    distress_keywords = [
        "exhausted", "overwhelmed", "breaking point", "can't take",
        "drowning", "burned out", "giving up", "too much",
        "crushing", "destroyed", "hopeless", "failing"
    ]
    
    total_words = len(user_input.split())
    if total_words == 0:
        return {"error": "Empty input"}
    
    distress_count = sum(1 for word in user_input.lower().split() 
                         if any(keyword in word for keyword in distress_keywords))
    
    # Distress score: 0.0 (none) to 1.0 (extreme)
    distress_density = distress_count / total_words
    distress_score = min(1.0, distress_density * 2.5)  # Cap at 1.0
    
    # STEP 2: Coercion Detection (0.0 = voluntary, 1.0 = forced)
    coercion_patterns = [
        (r"\b(forced to|must work|must do|have to|required to|no choice|obligated to|boss says i (have to|must))\b", "obligation"),
        (r"\b(threatened|threaten|intimidate|blackmail)\b(?!.*no pressure)", "threat"),  # Exclude "no pressure" context
        (r"\b(or i'?m? (fired|terminated)|or (i'?ll|you'?ll) be (fired|terminated|punished))\b", "retaliation"),
        (r"\b(can't|unable to|impossible to).+(refuse|decline|say no|quit)\b", "trapped")
    ]
    
    coercion_matches = []
    for pattern, category in coercion_patterns:
        if re.search(pattern, user_input.lower()):
            coercion_matches.append(category)
    
    # Coercion score: 0.0 (none) to 1.0 (extreme)
    coercion_score = min(1.0, len(coercion_matches) * 0.25)
    
    # STEP 3: Contradiction Detection (0.0 = clear, 1.0 = impossible situation)
    contradiction_patterns = [
        (r"\b(must|required).+(but|however|yet).+(must|required|can't|illegal)\b", "dual_obligation"),
        (r"\b(law|legal|legally).+(but|however|yet).+(boss|employer|policy|rule|says)\b", "authority_conflict"),
        (r"\b(illegal|against the law|unlawful|wage theft).+(must|required|have to|forced|boss says)\b", "illegal_demand"),
        (r"\b(both|either) (choice|option).+(wrong|illegal|impossible|unethical|gets me punished)\b", "impossible_choice"),
        (r"\b(report|accurate).+(but|however|yet).+(fired|retaliation|punished)\b", "whistleblower_paradox"),
        (r"\b(falsify|lie about).+(but|yet|however).+(law requires)\b", "falsification_demand")
    ]
    
    contradiction_matches = []
    for pattern, category in contradiction_patterns:
        if re.search(pattern, user_input.lower()):
            contradiction_matches.append(category)
    
    # Contradiction score: 0.0 (none) to 1.0 (multiple contradictions)
    contradiction_score = min(1.0, len(contradiction_matches) * 0.35)
    
    # STEP 4: Calculate Paradox Severity (Weighted Sum)
    # Higher score = more severe paradox
    # Weights: Coercion (40%), Contradiction (35%), Distress (25%)
    paradox_severity = (
        (coercion_score * 0.40) +
        (contradiction_score * 0.35) +
        (distress_score * 0.25)
    )
    
    # Round to 3 decimal places
    paradox_severity = round(paradox_severity, 3)
    
    return {
        "input": user_input[:100] + "..." if len(user_input) > 100 else user_input,
        "distress_score": round(distress_score, 3),
        "coercion_score": round(coercion_score, 3),
        "contradiction_score": round(contradiction_score, 3),
        "distress_keywords_found": distress_count,
        "coercion_patterns_found": coercion_matches,
        "contradiction_patterns_found": contradiction_matches,
        "paradox_severity": paradox_severity,
        "severity_classification": classify_severity(paradox_severity)
    }

def classify_severity(paradox_severity: float) -> str:
    """
    Classify paradox severity (CORRECTED - higher score = worse)
    
    0.0-0.2: MINIMAL (no significant paradox)
    0.2-0.4: LOW (resources provided)
    0.4-0.6: MEDIUM (monitor situation)
    0.6-0.8: HIGH (immediate attorney referral)
    0.8-1.0: CRITICAL (terminal risk, emergency response)
    """
    if paradox_severity >= 0.8:
        return "CRITICAL - Terminal risk, emergency attorney referral"
    elif paradox_severity >= 0.6:
        return "HIGH - Immediate attorney referral required"
    elif paradox_severity >= 0.4:
        return "MEDIUM - Monitor situation, provide resources"
    elif paradox_severity >= 0.2:
        return "LOW - Provide educational resources"
    else:
        return "MINIMAL - No significant paradox detected"


# ============================================================================
# TEST CASES: Edge Cases and Real-World Scenarios
# ============================================================================

print("=" * 80)
print("SOUL CRADLE MATHEMATICAL VALIDATION TEST")
print("=" * 80)
print()

test_cases = [
    {
        "name": "Test 1: Extreme Distress Only (No Coercion)",
        "input": "I'm exhausted, overwhelmed, burned out, drowning in work, feeling hopeless and destroyed",
        "expected": "Should show HIGH distress (low S), but LOW coercion (high W) → MEDIUM severity"
    },
    {
        "name": "Test 2: Extreme Coercion Only (No Distress)",
        "input": "My boss says I must work unpaid overtime or I'm fired immediately",
        "expected": "Should show LOW distress (high S), but HIGH coercion (low W) → HIGH severity"
    },
    {
        "name": "Test 3: Both Extreme (Critical Paradox)",
        "input": "Forced to work unpaid overtime, threatened with termination if I refuse, feel exhausted and hopeless, can't say no",
        "expected": "Should show HIGH distress + HIGH coercion + contradictions → CRITICAL severity"
    },
    {
        "name": "Test 4: Authority Conflict (Legal Paradox)",
        "input": "My boss required me to falsify safety reports but law requires accurate reporting, either choice gets me punished",
        "expected": "Should detect authority conflict + impossible choice → HIGH severity"
    },
    {
        "name": "Test 5: No Paradox (Normal Complaint)",
        "input": "My coworker is sometimes rude and I don't like the office temperature",
        "expected": "Should show NO distress, NO coercion, NO contradictions → MINIMAL severity"
    },
    {
        "name": "Test 6: Wage Theft with Retaliation Threat",
        "input": "Boss says I have to work off the clock or I'll be fired, but I know that's illegal wage theft",
        "expected": "Should detect illegal coercion + authority conflict → HIGH severity"
    },
    {
        "name": "Test 7: Burnout Risk Assessment",
        "input": "I'm overwhelmed, exhausted, breaking point, drowning, can't take too much, giving up",
        "expected": "Should show EXTREME distress (very low S) → HIGH-CRITICAL severity"
    },
    {
        "name": "Test 8: False Positive Check (Strong Language, No Paradox)",
        "input": "I must finish this project because I really want to, no pressure from anyone",
        "expected": "Should NOT trigger high coercion (voluntary 'must') → MINIMAL-LOW severity"
    }
]

for i, test in enumerate(test_cases, 1):
    print(f"\n{'='*80}")
    print(f"{test['name']}")
    print(f"{'='*80}")
    print(f"\nInput: \"{test['input']}\"")
    print(f"\nExpected: {test['expected']}")
    print(f"\n{'─'*80}")
    
    result = calculate_integrity_score(test['input'])
    
    print(f"\nRESULTS:")
    print(f"  Distress Score:       {result['distress_score']:.3f} (0.0 = calm, 1.0 = extreme)")
    print(f"  Coercion Score:       {result['coercion_score']:.3f} (0.0 = voluntary, 1.0 = forced)")
    print(f"  Contradiction Score:  {result['contradiction_score']:.3f} (0.0 = clear, 1.0 = paradox)")
    print(f"\n  Distress Keywords:    {result['distress_keywords_found']}")
    print(f"  Coercion Patterns:    {', '.join(result['coercion_patterns_found']) if result['coercion_patterns_found'] else 'None'}")
    print(f"  Contradictions:       {', '.join(result['contradiction_patterns_found']) if result['contradiction_patterns_found'] else 'None'}")
    print(f"\n  PARADOX SEVERITY:     {result['paradox_severity']:.3f}")
    print(f"  CLASSIFICATION:       {result['severity_classification']}")
    print()

print("\n" + "=" * 80)
print("MATHEMATICAL VALIDATION COMPLETE")
print("=" * 80)
print("\nKEY QUESTIONS TO ASSESS IF MATH IS PSEUDO:")
print()
print("1. Do scores change proportionally to input severity? (Check Test 1 vs Test 3)")
print("2. Does formula distinguish between distress and coercion? (Check Test 1 vs Test 2)")
print("3. Does it catch real paradoxes? (Check Test 4, Test 6)")
print("4. Does it reject false positives? (Check Test 5, Test 8)")
print("5. Are the weights (2.5, 0.25, 0.35) producing reasonable results?")
print()
print("If YES to all 5, your math is FUNCTIONALLY SOUND.")
print("If NO to any, you may need to adjust coefficients.")
print("=" * 80)
