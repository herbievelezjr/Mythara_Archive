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
    # -- soul assessors: deterministic scoring calculators -------------------
    # Each takes pre-scored structured inputs and computes a soul-dimension
    # score. They perceive nothing real on their own.
    "demeter": {
        "core_function": "soul assessor — deterministic scoring calculator on pre-scored structured inputs.",
        "faces_user": False, "organ": False, "module": None,
    },
    "dionysus": {
        "core_function": "soul assessor — deterministic scoring calculator on pre-scored structured inputs.",
        "faces_user": False, "organ": False, "module": None,
    },
    "eros": {
        "core_function": "soul assessor — deterministic scoring calculator on pre-scored structured inputs.",
        "faces_user": False, "organ": False, "module": None,
    },
    "hades": {
        "core_function": "soul assessor — deterministic scoring calculator on pre-scored structured inputs.",
        "faces_user": False, "organ": False, "module": None,
    },
    "hermes": {
        "core_function": "soul assessor — deterministic scoring calculator on pre-scored structured inputs.",
        "faces_user": False, "organ": False, "module": None,
    },
    "janus": {
        "core_function": "soul assessor — deterministic scoring calculator on pre-scored structured inputs.",
        "faces_user": False, "organ": False, "module": None,
    },
    "nemesis": {
        "core_function": "soul assessor — deterministic scoring calculator on pre-scored structured inputs.",
        "faces_user": False, "organ": False, "module": None,
    },
    "persephone": {
        "core_function": "soul assessor — deterministic scoring calculator on pre-scored structured inputs.",
        "faces_user": False, "organ": False, "module": None,
    },
    # -- real-world touch ----------------------------------------------------
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
