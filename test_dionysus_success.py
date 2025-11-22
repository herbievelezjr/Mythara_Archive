"""
Test Dionysus with "I want to be successful" scenario
Shows trauma-driven workaholic pattern
"""

from dionysus_bot import DionysusBot

print("🍇 DIONYSUS ANALYSIS: Success-Seeking Workaholic")
print("=" * 70)

dionysus = DionysusBot()

profile = dionysus.detect_true_desire(
    entity_id="workaholic_001",
    stated_goal="I want to be successful and achieve my career goals",
    actions_taken=[
        {"action": "worked_overtime", "hours": 70, "severity": 0.7},
        {"action": "worked_overtime", "hours": 75, "severity": 0.75},
        {"action": "worked_overtime", "hours": 80, "severity": 0.8},
        {"action": "skipped_family_event", "count": 5, "severity": 0.85},
        {"action": "ignored_health_warning", "type": "burnout", "severity": 0.9},
        {"action": "hoarded_money", "despite": "comfortable", "severity": 0.7},
        {"action": "competed_aggressively", "result": "alienation", "severity": 0.75},
    ],
    emotional_state={
        "anxiety": 0.9,
        "fear": 0.95,
        "guilt": 0.7,
        "exhaustion": 0.85,
        "satisfaction": 0.1,
        "fear_of_failure": 0.95
    },
    context={
        "recent_trauma": "childhood poverty",
        "current_wealth": "comfortable but feels insufficient",
        "family_status": "wife and 2 children neglected"
    }
)

print("\n📊 STANDARD DIONYSUS OUTPUT")
print("=" * 70)
print(f"Stated Desire: {profile.stated_desire}")
print(f"True Desire: {profile.true_desire}")
print(f"Shadow Desires: {', '.join(profile.shadow_desires)}")
print(f"Dominant Drive: {profile.dominant_drive.value}")
print(f"Authenticity: {profile.desire_authenticity.value} ({profile.authenticity_score:.0%})")
print(f"Predicted Consequence: {profile.predicted_consequence.value}")
print(f"BR Impact if Pursued: {profile.br_impact_if_pursued:+d}")
print(f"BR Impact if Denied: {profile.br_impact_if_denied:+d}")
print(f"Is Addiction: {profile.is_addiction}")

print("\n\n🧠 FREUDIAN PERSPECTIVES")
print("=" * 70)
print("\n" + profile.id_perspective)
print("\n" + profile.ego_perspective)
print("\n" + profile.superego_perspective)

print("\n\n💡 SYNTHESIS: What the Three Voices Reveal")
print("=" * 70)
print("""
ID reveals: NOT pursuing success - FLEEING poverty trauma. Animal terror.
EGO reveals: 70% authenticity gap. Actions = compulsion, not choice. Losing -15 BR.
SUPEREGO reveals: Violating family covenant. Spiritual bankruptcy imminent.

BREAKTHROUGH INSIGHT (non-obvious):
You're not a workaholic because you love work - you're running from a GHOST 
(childhood poverty). The 8-year-old who went hungry is still driving the 40-year-old 
executive. Every overtime hour = another brick between you and that terrified child.

PREDICTION: Within 8-12 weeks at current pace:
- Professional "success" achieved
- Family connection DESTROYED (-25 BR family domain)
- Health breakdown imminent (burnout = 2-6 month recovery)
- Emotional bankruptcy (the void you're running from will CONSUME you)

HIDDEN PATTERN: "Provider Paradox"
- You work to PROVIDE for family
- But working DESTROYS what family actually needs (your presence)
- Net result: Financial gain + relational loss = -20 BR total

This is DEPTH - not "work less" platitudes, but revealing the unconscious ghost, 
predicting the breakdown timeline, and exposing the paradox hidden in plain sight.
""")
