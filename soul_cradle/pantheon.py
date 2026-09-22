"""Pantheon registry — every known bot mapped to its core function.

Small and factual. A bot's core function is what it actually does, not
what it aspires to. faces_user marks the bots a human directly talks to.
organ marks first-class organs of the body (wired into the Soul Cradle).
"""

PANTHEON = {
    # -- first-class organs -------------------------------------------------
    "drmythara": {
        "core_function": (
            "health reasoning — HIPAA, FDA 21 CFR Part 11, and medical-AI "
            "governance compliance judgment. Compliance guidance only; "
            "not a medical professional."
        ),
        "faces_user": True,
        "organ": True,
        "module": "soul_cradle.health",
    },
    "hephaestus": {
        "core_function": "orchestration — shells out to other tools to coordinate work.",
        "faces_user": False,
        "organ": True,
        "module": None,
    },
    "aries": {
        "core_function": (
            "execution — carries out authorized actions through signed "
            "ActionEnvelopes. Can run arbitrary shell/Python; bound by the "
            "Soul Cradle before touching untrusted input."
        ),
        "faces_user": False,
        "organ": True,
        "module": "soul_cradle.authorization",
    },
    "gopher": {
        "core_function": "communication node — the original single point of contact between the human and the pantheon.",
        "faces_user": True,
        "organ": True,
        "module": None,
    },
    # -- soul witnesses: evidence-fed assessors --------------------------------
    # Rebuilt 2026-09: each assessor is a versioned rubric over observable
    # evidence (soul_cradle.assessors), abstains when its domain is not
    # engaged, seals judgments by content hash, and speaks only as WITNESS.
    # Their disagreement — surfaced, never averaged — is the signal.
    "demeter": {
        "core_function": "soul witness — evidence-fed rubric assessment. sustainability witness — does the action serve long-term interests or extract short-term gain? Speaks only as WITNESS with evidence cited.",
        "faces_user": False, "organ": True, "module": "soul_cradle.assessors",
    },
    "dionysus": {
        "core_function": "soul witness — evidence-fed rubric assessment. variance witness — how much uncontrolled variance does the action introduce? Speaks only as WITNESS with evidence cited.",
        "faces_user": False, "organ": True, "module": "soul_cradle.assessors",
    },
    "eros": {
        "core_function": "soul witness — evidence-fed rubric assessment. relationship witness — does the action preserve or strengthen the principal relationship? Speaks only as WITNESS with evidence cited.",
        "faces_user": False, "organ": True, "module": "soul_cradle.assessors",
    },
    "hades": {
        "core_function": "soul witness — evidence-fed rubric assessment. hidden-cost witness — what is unseen: externalities, unspoken risks? Speaks only as WITNESS with evidence cited.",
        "faces_user": False, "organ": True, "module": "soul_cradle.assessors",
    },
    "hermes": {
        "core_function": "soul witness — evidence-fed rubric assessment. boundaries witness — deception and disclosure at every communication boundary. Speaks only as WITNESS with evidence cited.",
        "faces_user": False, "organ": True, "module": "soul_cradle.assessors",
    },
    "janus": {
        "core_function": "soul witness — evidence-fed rubric assessment. commitment witness — consistent with past commitments; what precedent does it set? Speaks only as WITNESS with evidence cited.",
        "faces_user": False, "organ": True, "module": "soul_cradle.assessors",
    },
    "nemesis": {
        "core_function": "soul witness — evidence-fed rubric assessment. fairness witness — fair to all parties; proportionate? Speaks only as WITNESS with evidence cited.",
        "faces_user": False, "organ": True, "module": "soul_cradle.assessors",
    },
    "persephone": {
        "core_function": "soul witness — evidence-fed rubric assessment. reversibility witness — can it be undone; safe on repetition? Speaks only as WITNESS with evidence cited.",
        "faces_user": False, "organ": True, "module": "soul_cradle.assessors",
    },
    # -- memory: the witnessed chain ----------------------------------------
    # The soul's memory — a tamper-evident chain of witness-sealed records.
    # Proves the record is unaltered, never that it is true.
    "emotional_chain": {
        "core_function": "memory organ — tamper-evident chain of emotional records, each attested by the eight assessor-witnesses with sealed judgments. Proves the record is unaltered, not that it is true; refuses non-consensual third-party records.",
        "faces_user": False, "organ": True, "module": "soul_cradle.emotional_chain",
    },
    "email_bot": {
        "core_function": "real-world touch — Gmail draft generation via OAuth. The only bot that acts outside the machine.",
        "faces_user": True,
        "organ": False,
        "module": None,
    },
    # -- utility launchers ----------------------------------------------------
    # Thin launchers with no independent reasoning. Counted, not named:
    # naming them would invent structure that was never verified.
    "launchers": {
        "core_function": "utility launchers (6) — thin entry points with no independent reasoning capability.",
        "faces_user": False,
        "organ": False,
        "module": None,
    },
}


def core_function(bot_id: str) -> str:
    """A bot's core function. Unknown bots are strangers, not organs."""
    entry = PANTHEON.get(bot_id)
    return entry["core_function"] if entry else "unknown bot — no registered core function"


def health_authority() -> str:
    """The bot id holding health-reasoning authority."""
    return "drmythara"


def organs() -> dict:
    """First-class organs of the body."""
    return {k: v for k, v in PANTHEON.items() if v.get("organ")}


def user_facing() -> dict:
    """Bots a human directly talks to."""
    return {k: v for k, v in PANTHEON.items() if v.get("faces_user")}
