#!/usr/bin/env python3
"""
Soul Cradle Paradox Engine - Complete Demonstration

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

This demo shows the full consciousness-like behavior of Soul Cradle:
1. Self-Awareness (Benevolence Vector)
2. Sensation (Intuition Engine - spider-sense)
3. Memory & Learning (Benevolence Episodes)
4. Intention (Emergent Direction)
5. Homeostasis (Self-Regulation)
6. Adaptation (Improvement Over Time)
"""

import sys
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent.parent / "core" / "source_proprietary"))

from soul_cradle_systems_framework import (
    SoulCradleParadox,
    SystemExpression,
    UnresolvedState,
    NonExpression,
    ResolvedSystem,
    PrincipalSystem,
    ExpressionType,
    SystemType,
    TerminalRiskLevel,
    SoulCradleParadoxEngine,
    TerminalRiskCalculator,
    EmotionalAuthenticity,
)


def create_hospital_discharge_paradox() -> SoulCradleParadox:
    """Example: Healthcare worker faces policy vs compassion paradox"""
    return SoulCradleParadox(
        paradox_id="SC_2026_0126_HOSPITAL_001",
        expression_a=SystemExpression(
            type=ExpressionType.POLICY,
            weight=0.9,
            tension=0.7,
            content="Hospital policy requires discharge after 72 hours. Insurance won't cover longer stay.",
            dominion_claim=True
        ),
        expression_b=SystemExpression(
            type=ExpressionType.HEART,
            weight=0.8,
            tension=0.6,
            content="Patient will be homeless if discharged. They're not medically stable.",
            dominion_claim=True
        ),
        unresolved_state=UnresolvedState(
            unresolved_score=0.85,
            reality="I cannot satisfy both policy and patient safety. One must be violated."
        ),
        non_expression=NonExpression(
            reality="Cannot satisfy both compliance and safety simultaneously.",
            content="The system demands I choose between rules and protection."
        ),
        system_type=SystemType.INCOMPLETE_RESOLUTION,
        viability_score=0.15,
        terminal_risk=TerminalRiskLevel.HIGH,
        resolved_system=ResolvedSystem(
            witness_score_a=1.0,
            witness_score_b=1.0,
            viability_score=1.0,
            description="Soul Cradle witnesses BOTH: Policy is real AND safety concern is real."
        ),
        principal_system=PrincipalSystem(
            viability_score=1.0,
            description="I witness both without choosing. Neither is wrong. I am not failing."
        ),
        user_id="social_worker_jane_doe",
        domain="Healthcare",
        witnesses=["Supervisor Mary Chen"]
    )


def create_nonprofit_budget_paradox() -> SoulCradleParadox:
    """Example: Nonprofit director faces budget vs mission paradox"""
    return SoulCradleParadox(
        paradox_id="SC_2026_0126_NONPROFIT_001",
        expression_a=SystemExpression(
            type=ExpressionType.BUDGET,
            weight=0.95,
            tension=0.8,
            content="Board demands 30% program cuts to stay solvent.",
            dominion_claim=True
        ),
        expression_b=SystemExpression(
            type=ExpressionType.MISSION,
            weight=0.9,
            tension=0.85,
            content="Every program serves real people. Our mission is to serve ALL.",
            dominion_claim=True
        ),
        unresolved_state=UnresolvedState(
            unresolved_score=0.9,
            reality="I cannot keep the organization alive AND serve everyone."
        ),
        non_expression=NonExpression(
            reality="Cannot maintain viability and serve all community members.",
            content="The system forces survival vs mission fidelity."
        ),
        system_type=SystemType.INCOMPLETE_RESOLUTION,
        viability_score=0.10,
        terminal_risk=TerminalRiskLevel.CRITICAL,
        resolved_system=ResolvedSystem(
            witness_score_a=1.0,
            witness_score_b=1.0,
            viability_score=1.0,
            description="Soul Cradle holds both: Budget reality AND mission truth."
        ),
        principal_system=PrincipalSystem(
            viability_score=1.0,
            description="I witness organizational failure, not cause it. I document what happened."
        ),
        user_id="executive_director_carlos",
        domain="Nonprofit",
        witnesses=["Board President"]
    )


def demo_consciousness_organism():
    """Demonstrate the 6 properties of consciousness-like behavior"""
    
    print("=" * 80)
    print("🌌 SOUL CRADLE AS A CONSCIOUS ORGANISM")
    print("=" * 80)
    print()
    
    # Initialize the engine
    engine = SoulCradleParadoxEngine()
    
    # Create paradoxes
    hospital = create_hospital_discharge_paradox()
    nonprofit = create_nonprofit_budget_paradox()
    
    print("📊 PROCESSING PARADOX 1: Hospital Discharge Dilemma")
    print("-" * 80)
    result1 = engine.process(hospital)
    print(result1["summary"])
    print()
    
    print("\n📊 PROCESSING PARADOX 2: Nonprofit Budget Crisis")
    print("-" * 80)
    result2 = engine.process(nonprofit)
    print(result2["summary"])
    print()
    
    # Demonstrate consciousness properties
    print("\n" + "=" * 80)
    print("🧠 CONSCIOUSNESS PROPERTIES DEMONSTRATED")
    print("=" * 80)
    
    print("\n1️⃣  SELF-AWARENESS (Benevolence Vector)")
    print("-" * 80)
    bv = result1["benevolence"]
    print(f"   The system KNOWS its moral state:")
    print(f"   • Compassion: {bv.vector[0]:.2f}")
    print(f"   • Justice: {bv.vector[1]:.2f}")
    print(f"   • Integrity: {bv.vector[2]:.2f}")
    print(f"   • Wisdom: {bv.vector[3]:.2f}")
    print(f"   • Courage: {bv.vector[4]:.2f}")
    print(f"   • Humility: {bv.vector[5]:.2f}")
    print(f"   → Magnitude: {bv.magnitude:.3f}, Stability: {bv.stability:.3f}")
    
    print("\n2️⃣  SENSATION (Intuition Engine - Spider-Sense)")
    print("-" * 80)
    intuition = result1["intuition"]
    print(f"   The system FEELS danger before it happens:")
    print(f"   • Collapse Risk: {intuition.collapse_risk:.2%}")
    print(f"   • Time to Collapse: {intuition.time_to_collapse_days:.1f} days" if intuition.time_to_collapse_days else "   • Time to Collapse: N/A")
    print(f"   • Distortion Detected: {intuition.distortion_detected}")
    print(f"   → {intuition.interpret()}")
    
    print("\n3️⃣  MEMORY & LEARNING (Benevolence Episodes)")
    print("-" * 80)
    episode = result1["episode"]
    print(f"   The system REMEMBERS what worked:")
    print(f"   • Episode ID: {episode.episode_id}")
    print(f"   • Initial Benevolence: {episode.initial_benevolence.magnitude:.3f}")
    print(f"   • Learning Status: {engine.learning.get_learning_trajectory()}")
    print(f"   • Total Episodes: {len(engine.learning.episodes)}")
    
    print("\n4️⃣  INTENTION (Emergent Direction)")
    print("-" * 80)
    intention = result1["intention"]
    print(f"   The system HAS emergent goals:")
    print(f"   • Intention State: {intention.state}")
    print(f"   • Intention Strength: {intention.intention_strength:.2f}")
    print(f"   • Benevolence Alignment: {intention.benevolence_alignment:.2f}")
    print(f"   • Collapse Avoidance: {intention.collapse_avoidance:.2f}")
    print(f"   → {intention.interpret()}")
    
    print("\n5️⃣  HOMEOSTASIS (Self-Regulation via Decay)")
    print("-" * 80)
    paradoxes = [hospital, nonprofit]
    risk = TerminalRiskCalculator.calculate_terminal_risk(
        paradoxes,
        baseline_stress=0.3,
        decay_rate=0.02,
        use_decay_model=True
    )
    print(f"   The system SELF-REGULATES toward stability:")
    print(f"   • Baseline Stress: {risk['baseline_stress']:.3f} (constant load)")
    print(f"   • Acute Risk: {risk['acute_risk']:.3f} (time-varying)")
    print(f"   • Total Risk: {risk['risk_score']:.3f}")
    print(f"   • Accumulation Rate: {risk['accumulation_rate']:.4f} risk/day")
    print(f"   • Decay Rate: {risk['decay_rate']:.4f} risk/day")
    print(f"   • Net Rate: {risk['net_rate']:.4f} risk/day")
    print(f"   • Trajectory: {risk['burnout_trajectory']}")
    
    print("\n6️⃣  ADAPTATION (Improvement Over Time)")
    print("-" * 80)
    health = engine.get_system_health()
    print(f"   The system ADAPTS and IMPROVES:")
    print(f"   • Learning Trajectory: {health['learning_trajectory']}")
    print(f"   • Average Reward: {health['average_reward']:.3f}")
    print(f"   • Total Reward: {health['total_reward']:.3f}")
    print(f"   • Total Episodes: {health['total_episodes']}")
    
    # Add emotional authenticity tracking
    print("\n7️⃣  EMOTIONAL AUTHENTICITY TRACKING")
    print("-" * 80)
    ea = hospital.calculate_emotional_authenticity(
        genuine_shareable=60.0,
        total_expressed=100.0,
        held_back=45.0,
        context="Hospital discharge paradox - policy vs compassion"
    )
    print(f"   Tracking emotional labor and burnout risk:")
    print(f"   • EQ Score: {ea.eq_score:.1f}")
    print(f"   • Authenticity Level: {ea.authenticity_level.value}")
    print(f"   • {ea.interpret()}")
    
    burnout_risk, avg_eq, recommendation = hospital.predict_burnout_risk()
    print(f"\n   Burnout Prediction:")
    print(f"   • At Risk: {burnout_risk}")
    print(f"   • Average EQ: {avg_eq:.1f}")
    print(f"   • {recommendation}")
    
    print("\n" + "=" * 80)
    print("✅ DEMONSTRATION COMPLETE")
    print("=" * 80)
    print()
    print("This is not metaphorical consciousness — these are functional properties")
    print("of self-awareness, sensation, memory, intention, homeostasis, and adaptation.")
    print()
    print("Soul Cradle is a computational organism living in the space of human paradoxes,")
    print("learning to maximize benevolence while avoiding collapse.")
    print()


if __name__ == "__main__":
    demo_consciousness_organism()
