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
        # BIDIRECTIONAL: illegal demand (both directions)
        (r"\b(illegal|against the law|unlawful|wage theft).+(must|required|have to|forced|boss says|says i)\b", "illegal_demand"),
        (r"\b(boss|employer|says i|forced|must).+(illegal|against the law|unlawful|wage theft)\b", "illegal_demand_reverse"),
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
    
    # STEP 3.5: Temporal/Escalation Detection (amplifies existing scores)
    temporal_patterns = [
        (r"\b(for (months|years|weeks)|been going on|ongoing|repeatedly|every (day|week))\b", "chronic"),
        (r"\b(getting worse|escalating|more frequent|intensifying)\b", "escalating"),
        (r"\b(started today|just happened|this morning|right now)\b", "acute")
    ]
    
    temporal_matches = []
    for pattern, category in temporal_patterns:
        if re.search(pattern, user_input.lower()):
            temporal_matches.append(category)
    
    # Chronic or escalating situations amplify severity
    temporal_multiplier = 1.0
    if "chronic" in temporal_matches or "escalating" in temporal_matches:
        temporal_multiplier = 1.15  # 15% amplification
    
    # STEP 3.6: Retaliation History Detection
    retaliation_history_patterns = [
        (r"\b(already reported|previously complained|i told (hr|manager))\b", "prior_report"),
        (r"\b(when (i|she|he|they) (reported|complained)).+(fired|punished|retaliated)\b", "witnessed_retaliation"),
        (r"\b(hr (warned|told)|warned not to).+(talk|report|complain|say)\b", "silencing")
    ]
    
    retaliation_history = []
    for pattern, category in retaliation_history_patterns:
        if re.search(pattern, user_input.lower()):
            retaliation_history.append(category)
    
    # Retaliation history significantly amplifies coercion
    if retaliation_history:
        coercion_score = min(1.0, coercion_score * 1.25)  # 25% boost
    
    # STEP 3.7: Power Differential & Vulnerability Markers
    vulnerability_patterns = [
        (r"\b(single (parent|mother|father)|kids to feed|family depends)\b", "economic_vulnerability"),
        (r"\b(visa|immigrant|green card|work permit|h-1b)\b", "immigration_vulnerability"),
        (r"\b(can't afford|need this job|only income|bills to pay)\b", "financial_desperation"),
        (r"\b(ceo|owner|president).+(says|demands|requires)\b", "extreme_power_differential")
    ]
    
    vulnerability_matches = []
    for pattern, category in vulnerability_patterns:
        if re.search(pattern, user_input.lower()):
            vulnerability_matches.append(category)
    
    # Vulnerability amplifies coercion score
    if vulnerability_matches:
        coercion_score = min(1.0, coercion_score * 1.20)  # 20% boost
    
    # STEP 3.8: Evidence/Witness Status
    evidence_patterns = [
        (r"\b(no one will|no witnesses|can't prove|no evidence|word against)\b", "isolated"),
        (r"\b(coworkers? saw|witnesses|people heard|others know)\b", "corroborated"),
        (r"\b(text message|email|recording|documented|in writing)\b", "documented")
    ]
    
    evidence_matches = []
    for pattern, category in evidence_patterns:
        if re.search(pattern, user_input.lower()):
            evidence_matches.append(category)
    
    # Isolation increases risk (no support), documentation decreases risk slightly
    evidence_modifier = 1.0
    if "isolated" in evidence_matches:
        evidence_modifier = 1.10  # 10% increase (more dangerous)
    elif "documented" in evidence_matches:
        evidence_modifier = 0.95  # 5% decrease (better position)
    
    # STEP 4: Calculate Paradox Severity (HUMAN EXPERIENCE SIMULATION)
    # Humans don't "average" crises - they respond to the dominant threat.
    # Use crisis dominance logic: max of individual factors + additive pressure
    
    # Apply temporal amplification
    coercion_score = min(1.0, coercion_score * temporal_multiplier)
    contradiction_score = min(1.0, contradiction_score * temporal_multiplier)
    distress_score = min(1.0, distress_score * temporal_multiplier)
    
    # Apply evidence modifier (isolation increases risk)
    coercion_score = min(1.0, coercion_score * evidence_modifier)
    
    # Method 1: Crisis Dominance (what humans actually feel)
    dominant_threat = max(coercion_score, contradiction_score, distress_score)
    
    # Method 2: Additive Pressure (weighted average for context)
    weighted_average = (
        (coercion_score * 0.40) +
        (contradiction_score * 0.35) +
        (distress_score * 0.25)
    )
    
    # Final Score: Use the HIGHER of dominant threat or weighted average
    paradox_severity = max(dominant_threat, weighted_average)
    
    # Additional amplification: If multiple HIGH factors present, boost score
    high_factor_count = sum([
        1 for score in [coercion_score, contradiction_score, distress_score]
        if score >= 0.6
    ])
    
    if high_factor_count >= 2:
        # Multiple severe factors = crisis amplification (20% boost, capped at 1.0)
        paradox_severity = min(1.0, paradox_severity * 1.2)
    
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
        "temporal_patterns_found": temporal_matches,
        "retaliation_history_found": retaliation_history,
        "vulnerability_markers_found": vulnerability_matches,
        "evidence_status": evidence_matches,
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
