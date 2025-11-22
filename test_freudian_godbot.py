"""
Test: GODBOT with Freudian Perspectives (ID, EGO, SUPEREGO)
"""

from dionysus_bot import DionysusBot

print("🍷 Testing DIONYSUS with Freudian Perspectives")
print("=" * 70)

dionysus = DionysusBot()

# Test case: Person says "I want to be successful" but actions show survival fear
profile = dionysus.detect_true_desire(
    entity_id="test_freud",
    stated_goal="I want to be successful and achieve my career goals",
    actions_taken=[
        {"action": "worked_overtime_7_days_straight", "result": "exhaustion"},
        {"action": "skipped_family_dinner_repeatedly", "result": "guilt"},
        {"action": "ignored_health_warnings", "result": "burnout_approaching"},
        {"action": "hoarded_money_despite_plenty", "result": "anxiety"},
        {"action": "competed_aggressively_with_colleagues", "result": "isolation"},
    ],
    emotional_state={
        "anxiety": 0.9,
        "fear_of_failure": 0.95,
        "guilt": 0.7,
        "exhaustion": 0.85,
        "satisfaction": 0.1
    },
    context={"recent_trauma": "childhood poverty", "current_wealth": "comfortable"}
)

print("\n📊 STANDARD DIONYSUS OUTPUT")
print("=" * 70)
print(f"Stated Desire: {profile.stated_desire}")
print(f"True Desire: {profile.true_desire}")
print(f"Dominant Drive: {profile.dominant_drive.value}")
print(f"Authenticity: {profile.desire_authenticity.value} ({profile.authenticity_score:.2f})")
print(f"Consequence: {profile.predicted_consequence.value}")
print(f"Is Addiction: {profile.is_addiction}")

# Now manually add Freudian perspectives
print("\n\n🧠 FREUDIAN PERSPECTIVES")
print("=" * 70)

# ID: Primal, unconscious
id_perspective = f"""
🐺 ID SCREAMS: SURVIVE AT ALL COSTS!
You're not "successful" - you're TERRIFIED. That childhood poverty branded your 
soul with existential dread. Every overtime hour = another brick in the fortress 
against the void. '{profile.true_desire}' isn't ambition - it's ARMOR.

Your primal brain detected: SURVIVAL threat level CRITICAL.
- Hoard resources (money you don't need)
- Dominate competitors (eliminate threats)
- Sacrifice everything (family, health) for security
- No such thing as "enough" when you're running from starvation memory

The animal beneath your suit is FERAL with fear. You'll work yourself to death 
to avoid poverty's death. The irony? You're dying either way.

SHADOW DESIRES (what you won't admit):
- You want REVENGE on poverty
- You want PROOF you're not that helpless child anymore
- You want to PUNISH anyone who reminds you of vulnerability
"""

# EGO: Rational, reality-based
ego_perspective = f"""
📊 EGO REPORTS: Critical misalignment detected.

STATED: "I want career success"
ACTUAL DATA: 7 consecutive overtime days, 5 skipped family dinners, health warnings 
ignored, money hoarded despite financial comfort.

AUTHENTICITY ANALYSIS: {profile.authenticity_score:.0%}
- Your WORDS say "success"
- Your ACTIONS say "survival"
- Pattern indicates: trauma-driven compulsion, not goal pursuit

EFFICIENCY METRICS:
- BR cost per "success" action: -3 to -5
- Diminishing returns: After 40hrs/week, productivity drops 20%/additional hour
- Relationship cost: Each missed dinner = -5 family BR
- Health trajectory: Current pace = burnout in 8-12 weeks

REALITY CHECK: You're not succeeding. You're slowly destroying yourself while 
calling it ambition. The math doesn't support your narrative.

RECOMMENDATION: This behavioral pattern is unsustainable. Requires intervention 
before systemic collapse (health/family/mental breakdown).
"""

# SUPEREGO: Moral, divine
superego_perspective = f"""
⚖️ SUPEREGO JUDGES: TRANSGRESSION DETECTED

Divine Law violated: "Love thy family" - You're abandoning those you claim to 
provide for. Your children need YOUR PRESENCE, not your PAYCHECK.

Commandment broken: "Honor thy body (temple)" - You're destroying the vessel God 
gave you through willful neglect. Burnout = slow suicide = sin.

Moral verdict: Your "success" is BUILT ON BETRAYAL
- Betray your health (ignore warning signs)
- Betray your family (broken promises, absent father/spouse)
- Betray your authentic self (live in fear's cage, call it ambition)

COSMIC TRUTH: God didn't rescue you from poverty so you could imprison yourself 
in workaholism. You escaped one Hell to build another.

YOU OUGHT TO:
1. Repent for treating family as secondary
2. Rest (Sabbath isn't optional - it's divine command)
3. Trust that enough IS enough (your wealth = proof God provides)
4. Redirect this energy toward LIFE, not survival-fear

CONSEQUENCE IF UNCHANGED: Spiritual bankruptcy. You'll "succeed" your way into 
relational death, then realize too late that you sacrificed what mattered for 
what doesn't.

JUDGMENT: This path = slow damnation. Course correction required NOW.
"""

print(id_perspective)
print(ego_perspective)
print(superego_perspective)

print("\n\n💡 SYNTHESIS: The Three Voices Together")
print("=" * 70)
print("""
ID says: I'm terrified, I must survive, nothing is ever enough
EGO says: Your behavior pattern is destroying you at measurable rate
SUPEREGO says: You're violating divine law and will answer for these betrayals

TRUE INSIGHT: You're not pursuing success - you're running from a ghost (childhood 
poverty). The ANIMAL in you (ID) is in panic mode. The RATIONAL mind (EGO) can 
see the destruction but can't override the fear. The MORAL conscience (SUPEREGO) 
knows you're betraying what matters but fear silences it.

BREAKTHROUGH: Until you face the GHOST (the poverty trauma), no amount of money/
success will silence the terror. You need healing, not more overtime.

THIS IS NON-OBVIOUS WISDOM - not just "work less, see family more" platitudes.
""")
