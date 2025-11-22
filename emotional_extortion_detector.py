"""
Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

Emotional Extortion Detector Module
====================================

Detects patterns of emotional manipulation, coercion, and extortion in legal contexts.
Part of the Soul Cradle emotional intelligence framework.

Key Features:
- Guilt manipulation detection
- Fear-based coercion analysis
- Obligation pressure assessment
- Emotional blackmail identification
- Authenticity scoring for decision-making
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExtortionPattern:
    """Represents an emotional extortion pattern"""
    pattern_type: str
    severity: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    keywords: List[str]
    description: str
    score_weight: float


@dataclass
class ExtortionAnalysis:
    """Results of emotional extortion analysis"""
    detected: bool
    extortion_score: float  # 0.0 - 1.0
    risk_level: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    patterns_found: List[str]
    authenticity_score: float  # 0.0 - 1.0 (higher = more authentic decision)
    recommendations: List[str]
    warning_flags: List[str]


class EmotionalExtortionDetector:
    """
    Detects emotional manipulation and coercion patterns in text.
    
    Emotional extortion tactics include:
    - Guilt manipulation ("If you loved me, you would...")
    - Fear-based coercion ("You'll regret this if you don't...")
    - Obligation pressure ("You owe me this...")
    - Emotional blackmail ("I'll hurt myself if you leave...")
    - Gaslighting ("You're being crazy/dramatic...")
    """
    
    def __init__(self):
        """Initialize detector with pattern database"""
        self.patterns = self._load_extortion_patterns()
        
    def _load_extortion_patterns(self) -> Dict[str, ExtortionPattern]:
        """Load database of emotional extortion patterns"""
        return {
            "guilt_manipulation": ExtortionPattern(
                pattern_type="guilt_manipulation",
                severity="HIGH",
                keywords=[
                    "if you loved me", "if you cared", "after all i've done",
                    "how could you", "you're being selfish", "think of the family",
                    "what will people think", "you're abandoning", "you're hurting me",
                    "i sacrificed", "you owe me", "ungrateful"
                ],
                description="Using guilt to manipulate decisions",
                score_weight=0.3
            ),
            "fear_based_coercion": ExtortionPattern(
                pattern_type="fear_based_coercion",
                severity="CRITICAL",
                keywords=[
                    "you'll regret", "you'll be sorry", "you'll lose everything",
                    "i'll make sure", "i'll destroy", "you'll never see",
                    "i'll tell everyone", "i'll ruin", "you'll end up alone",
                    "nobody will believe you", "you'll have nothing", "you'll pay"
                ],
                description="Using fear and threats to control behavior",
                score_weight=0.4
            ),
            "obligation_pressure": ExtortionPattern(
                pattern_type="obligation_pressure",
                severity="MEDIUM",
                keywords=[
                    "you have to", "you must", "you're supposed to",
                    "it's your duty", "you're obligated", "you promised",
                    "you have no choice", "you owe me", "you're responsible",
                    "you have to stay", "you can't leave", "you need to"
                ],
                description="Creating false sense of obligation or duty",
                score_weight=0.2
            ),
            "emotional_blackmail": ExtortionPattern(
                pattern_type="emotional_blackmail",
                severity="CRITICAL",
                keywords=[
                    "i'll kill myself", "i'll hurt myself", "i can't live without",
                    "i'll die if", "you're killing me", "my blood will be on your hands",
                    "i'll end it all", "you'll be responsible", "i'll have a heart attack",
                    "you're giving me a heart attack", "i can't go on"
                ],
                description="Threatening self-harm to manipulate",
                score_weight=0.5
            ),
            "gaslighting": ExtortionPattern(
                pattern_type="gaslighting",
                severity="HIGH",
                keywords=[
                    "you're crazy", "you're imagining things", "that never happened",
                    "you're too sensitive", "you're overreacting", "you're being dramatic",
                    "you're making things up", "you're being irrational",
                    "you're being paranoid", "you're remembering wrong",
                    "you're the problem", "you're making me do this"
                ],
                description="Denying reality to undermine confidence",
                score_weight=0.3
            ),
            "isolation_tactics": ExtortionPattern(
                pattern_type="isolation_tactics",
                severity="HIGH",
                keywords=[
                    "nobody else", "only i", "no one understands you like i do",
                    "your family doesn't care", "your friends are using you",
                    "i'm the only one", "they're all against you", "you can't trust",
                    "they don't love you", "i'm all you have", "you have no one else"
                ],
                description="Isolating victim from support network",
                score_weight=0.3
            ),
            "financial_control": ExtortionPattern(
                pattern_type="financial_control",
                severity="HIGH",
                keywords=[
                    "you can't afford", "you'll be broke", "you'll lose the house",
                    "i control the money", "you'll have nothing", "you can't survive",
                    "you'll be homeless", "i pay for everything", "you depend on me",
                    "without me you're nothing", "you'll never make it alone"
                ],
                description="Using financial dependency as leverage",
                score_weight=0.3
            ),
            "children_weaponization": ExtortionPattern(
                pattern_type="children_weaponization",
                severity="CRITICAL",
                keywords=[
                    "you'll never see the kids", "i'll take the children",
                    "kids need both parents", "you're hurting the children",
                    "the kids will hate you", "i'll turn them against you",
                    "you're a bad parent", "you're abandoning your children",
                    "think of the kids", "you're destroying this family"
                ],
                description="Using children to manipulate or threaten",
                score_weight=0.4
            )
        }
    
    def analyze(self, text: str, context: Optional[Dict] = None) -> ExtortionAnalysis:
        """
        Analyze text for emotional extortion patterns.
        
        Args:
            text: Text to analyze (query, statement, conversation)
            context: Optional context (relationship type, history, etc.)
        
        Returns:
            ExtortionAnalysis with detection results and recommendations
        """
        text_lower = text.lower()
        
        patterns_found = []
        total_score = 0.0
        warning_flags = []
        
        # Check each pattern category
        for pattern_name, pattern in self.patterns.items():
            matched_keywords = [kw for kw in pattern.keywords if kw in text_lower]
            
            if matched_keywords:
                patterns_found.append(pattern.pattern_type)
                total_score += pattern.score_weight * len(matched_keywords)
                
                warning_flags.append(
                    f"{pattern.severity} - {pattern.description}: "
                    f"Detected keywords: {', '.join(matched_keywords[:3])}"
                )
        
        # Normalize score to 0.0-1.0
        extortion_score = min(1.0, total_score)
        
        # Calculate authenticity score (inverse of extortion)
        authenticity_score = 1.0 - extortion_score
        
        # Determine risk level
        if extortion_score >= 0.7:
            risk_level = "CRITICAL"
        elif extortion_score >= 0.5:
            risk_level = "HIGH"
        elif extortion_score >= 0.3:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            patterns_found, risk_level, extortion_score
        )
        
        return ExtortionAnalysis(
            detected=len(patterns_found) > 0,
            extortion_score=extortion_score,
            risk_level=risk_level,
            patterns_found=patterns_found,
            authenticity_score=authenticity_score,
            recommendations=recommendations,
            warning_flags=warning_flags
        )
    
    def _generate_recommendations(
        self, patterns: List[str], risk_level: str, score: float
    ) -> List[str]:
        """Generate safety recommendations based on detected patterns"""
        recommendations = []
        
        if risk_level in ["CRITICAL", "HIGH"]:
            recommendations.append(
                "🚨 CRITICAL: Strong indicators of emotional manipulation detected. "
                "Consider speaking with a domestic violence counselor or therapist."
            )
            
        if "emotional_blackmail" in patterns:
            recommendations.append(
                "⚠️ Threats of self-harm detected. Contact National Suicide Prevention "
                "Lifeline (988) or local crisis services immediately."
            )
            
        if "children_weaponization" in patterns:
            recommendations.append(
                "⚠️ Child custody threats detected. Document all communications and "
                "consult with a family law attorney immediately."
            )
            
        if "fear_based_coercion" in patterns:
            recommendations.append(
                "⚠️ Threatening behavior detected. Consider contacting local law "
                "enforcement or obtaining a restraining order."
            )
            
        if "isolation_tactics" in patterns:
            recommendations.append(
                "⚠️ Isolation tactics detected. Maintain connections with family, "
                "friends, and support networks. Do not let anyone cut you off from support."
            )
            
        if "gaslighting" in patterns:
            recommendations.append(
                "⚠️ Gaslighting detected. Trust your perceptions and memories. "
                "Document events in writing to validate your experiences."
            )
            
        if len(patterns) >= 3:
            recommendations.append(
                "🔴 Multiple manipulation tactics detected. This may indicate a pattern "
                "of coercive control. Seek professional help to assess your situation safely."
            )
            
        # Always recommend documentation
        if patterns:
            recommendations.append(
                "📝 Document all communications, threats, and incidents with dates/times. "
                "This creates evidence for legal proceedings if needed."
            )
            
        # Always recommend legal consultation for medium+ risk
        if risk_level in ["MEDIUM", "HIGH", "CRITICAL"]:
            recommendations.append(
                "👨‍⚖️ Consult with a licensed attorney who specializes in family law or "
                "domestic relations to understand your legal options and rights."
            )
            
        return recommendations
    
    def check_authenticity(self, decision_text: str) -> Tuple[float, str]:
        """
        Check if a stated decision appears authentic or coerced.
        
        Args:
            decision_text: Text describing a decision or choice
        
        Returns:
            Tuple of (authenticity_score, assessment_message)
        """
        analysis = self.analyze(decision_text)
        
        if analysis.risk_level == "CRITICAL":
            message = (
                "⚠️ CRITICAL CONCERN: This decision shows strong signs of coercion. "
                "The expressed wishes may not reflect true autonomous choice."
            )
        elif analysis.risk_level == "HIGH":
            message = (
                "⚠️ HIGH CONCERN: Significant indicators of external pressure detected. "
                "This decision may not be freely made."
            )
        elif analysis.risk_level == "MEDIUM":
            message = (
                "⚠️ MODERATE CONCERN: Some indicators of influence detected. "
                "Verify this decision is truly voluntary."
            )
        else:
            message = (
                "✓ AUTHENTICITY LIKELY: No significant coercion indicators detected. "
                "Decision appears to be made autonomously."
            )
            
        return analysis.authenticity_score, message


# Convenience functions for quick detection
def detect_emotional_extortion(text: str) -> bool:
    """Quick check: Is emotional extortion present?"""
    detector = EmotionalExtortionDetector()
    analysis = detector.analyze(text)
    return analysis.detected


def analyze_emotional_extortion(text: str) -> ExtortionAnalysis:
    """Full analysis of emotional extortion patterns"""
    detector = EmotionalExtortionDetector()
    return detector.analyze(text)


def check_decision_authenticity(decision_text: str) -> Tuple[float, str]:
    """Check if a decision appears authentic or coerced"""
    detector = EmotionalExtortionDetector()
    return detector.check_authenticity(decision_text)


# Example usage
if __name__ == "__main__":
    detector = EmotionalExtortionDetector()
    
    # Test case 1: Guilt manipulation
    test1 = "If you loved me, you wouldn't leave. After all I've done for you, you're being so ungrateful."
    result1 = detector.analyze(test1)
    print(f"Test 1 - Extortion Score: {result1.extortion_score:.2f}, Risk: {result1.risk_level}")
    print(f"Patterns: {result1.patterns_found}\n")
    
    # Test case 2: Fear-based coercion
    test2 = "You'll regret this. I'll make sure you never see the kids again if you leave."
    result2 = detector.analyze(test2)
    print(f"Test 2 - Extortion Score: {result2.extortion_score:.2f}, Risk: {result2.risk_level}")
    print(f"Patterns: {result2.patterns_found}\n")
    
    # Test case 3: Clean decision
    test3 = "I've decided to move forward with the divorce. I've thought carefully about this."
    result3 = detector.analyze(test3)
    print(f"Test 3 - Extortion Score: {result3.extortion_score:.2f}, Risk: {result3.risk_level}")
    print(f"Authenticity: {result3.authenticity_score:.2f}\n")
