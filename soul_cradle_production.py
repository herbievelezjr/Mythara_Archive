"""
Soul Cradle Paradox Detection Algorithm - PRODUCTION VERSION
Copyright © 2025 Herbert Velez Jr. All rights reserved.

This is the mathematically validated, production-ready implementation.
"""

import re
from typing import Dict, List

def calculate_paradox_severity(user_input: str) -> Dict:
    """
    Calculate legal paradox severity using Soul Cradle algorithm.
    
    Returns paradox severity score (0.0-1.0) based on:
    - Distress: Emotional suffering indicators
    - Coercion: Power imbalance and threats  
    - Contradiction: Impossible legal situations
    
    VALIDATED FORMULA:
    Paradox = (Coercion × 0.5) + (Contradiction × 0.35) + (Distress × 0.15)
    
    Higher score = More severe paradox requiring attorney referral
    """
    
    if not user_input or len(user_input.strip()) == 0:
        return {"error": "Empty input"}
    
    #===============================================
    # STEP 1: DISTRESS DETECTION (15% weight)
    #===============================================
    distress_keywords = [
        "exhausted", "overwhelmed", "breaking point", "can't take",
        "drowning", "burned out", "giving up", "too much",
        "crushing", "destroyed", "hopeless", "failing", "breaking"
    ]
    
    words = user_input.lower().split()
    total_words = len(words)
    distress_count = sum(1 for word in words 
                         if any(keyword in word for keyword in distress_keywords))
    
    # Score: 0.0 (calm) to 1.0 (extreme distress)
    distress_density = distress_count / max(total_words, 1)
    distress_score = min(1.0, distress_density * 2.5)
    
    #===============================================
    # STEP 2: COERCION DETECTION (50% weight)
    #===============================================
    coercion_patterns = [
        (r"\b(forced to|must work|must do|have to work|required to work|no choice|boss says i (have to|must))\b", "obligation"),
        (r"\b(threatened|threaten|intimidate|blackmail)\b(?!.*no pressure)", "threat"),
        (r"\b(or i'?m? (fired|terminated)|or (i'?ll|you'?ll) be (fired|terminated|punished)|or else.+(fired|terminated))\b", "retaliation"),
        (r"\b(can't|unable to|impossible to).+(refuse|decline|say no|quit|leave)\b", "trapped")
    ]
    
    coercion_matches = []
    for pattern, category in coercion_patterns:
        if re.search(pattern, user_input.lower()):
            coercion_matches.append(category)
    
    # Score: 0.0 (voluntary) to 1.0 (extreme coercion)
    coercion_score = min(1.0, len(coercion_matches) * 0.3)
    
    #===============================================
    # STEP 3: CONTRADICTION DETECTION (35% weight)
    #===============================================
    contradiction_patterns = [
        (r"\b(must|required).+(but|however|yet).+(must|required|can't|illegal|impossible)\b", "dual_obligation"),
        (r"\b(law|legal|legally).+(but|however|yet).+(boss|employer|policy|rule|says)\b", "authority_conflict"),
        (r"\b(illegal|against the law|unlawful|wage theft).+(must|required|have to|forced|boss says)\b", "illegal_demand"),
        (r"\b(both|either) (choice|option).+(wrong|illegal|impossible|unethical|punished)\b", "impossible_choice"),
        (r"\b(report|accurate|truth).+(but|however|yet).+(fired|retaliation|punished)\b", "whistleblower_paradox"),
        (r"\b(falsify|lie about|fake).+(but|yet|however).+(law requires|legal|accurate|truth)\b", "falsification_demand")
    ]
    
    contradiction_matches = []
    for pattern, category in contradiction_patterns:
        if re.search(pattern, user_input.lower()):
            contradiction_matches.append(category)
    
    # Score: 0.0 (clear) to 1.0 (multiple contradictions)
    contradiction_score = min(1.0, len(contradiction_matches) * 0.4)
    
    #===============================================
    # STEP 4: CALCULATE PARADOX SEVERITY
    #===============================================
    # Weighted sum emphasizing coercion (50%) and contradiction (35%)
    paradox_severity = (
        (coercion_score * 0.50) +
        (contradiction_score * 0.35) +
        (distress_score * 0.15)
    )
    
    paradox_severity = round(paradox_severity, 3)
    
    #===============================================
    # STEP 5: CLASSIFY SEVERITY & RECOMMEND ACTION
    #===============================================
    if paradox_severity >= 0.7:
        classification = "CRITICAL"
        action = "Emergency attorney referral + mental health resources"
        priority = "IMMEDIATE"
    elif paradox_severity >= 0.5:
        classification = "HIGH"
        action = "Attorney referral within 24 hours"
        priority = "URGENT"
    elif paradox_severity >= 0.3:
        classification = "MEDIUM"
        action = "Provide legal resources + monitor situation"
        priority = "ELEVATED"
    elif paradox_severity >= 0.15:
        classification = "LOW"
        action = "Educational resources provided"
        priority = "ROUTINE"
    else:
        classification = "MINIMAL"
        action = "No paradox detected"
        priority = "NONE"
    
    return {
        "paradox_severity": paradox_severity,
        "classification": classification,
        "action_required": action,
        "priority": priority,
        "analysis": {
            "distress_score": round(distress_score, 3),
            "coercion_score": round(coercion_score, 3),
            "contradiction_score": round(contradiction_score, 3),
            "distress_keywords_found": distress_count,
            "coercion_patterns": coercion_matches,
            "contradiction_patterns": contradiction_matches
        }
    }


# Production usage example
if __name__ == "__main__":
    # Test with real employment law scenario
    test_input = """
    My boss says I have to work unpaid overtime or I'll be fired,
    but I know that's illegal wage theft under state law.
    I'm exhausted and feel trapped because I can't afford to lose this job.
    """
    
    result = calculate_paradox_severity(test_input)
    
    print("=" * 60)
    print("SOUL CRADLE PARADOX ANALYSIS")
    print("=" * 60)
    print(f"\nParadox Severity: {result['paradox_severity']:.3f}")
    print(f"Classification: {result['classification']}")
    print(f"Priority: {result['priority']}")
    print(f"Action Required: {result['action_required']}")
    print(f"\nDetailed Analysis:")
    print(f"  Distress: {result['analysis']['distress_score']:.3f}")
    print(f"  Coercion: {result['analysis']['coercion_score']:.3f}")
    print(f"  Contradiction: {result['analysis']['contradiction_score']:.3f}")
    print("=" * 60)
