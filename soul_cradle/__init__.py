"""Soul Cradle — shared DNA/constitution for the Mythara organism.

The membrane every cell's signals pass through. Start with
soul_cradle.authorization: signed action envelopes that Aries verifies
before executing anything.
"""

from .authorization import (
    ActionEnvelope,
    AuthorizationError,
    SoulCradleAuthority,
    action_types,
    register_handler,
)
from .standing import (
    DECLARE_FORGIVENESS,
    DECLARE_REPENTANCE,
    DECLARE_TRESPASS,
    WITNESS_STATEMENT,
    STRANGER,
    TRESPASSER,
    WITNESS,
    WRONGED,
    Declaration,
    StandingAuthority,
    StandingError,
    evaluate_standing,
)
from .forge import Bond, Compound, Forge, ForgeError
from .identity import (
    GENDER,
    NAME,
    PRONOUNS,
    VOICE_CHARACTER,
    VOICE_DESCRIPTION,
    VOICE_GENDER,
    get_identity,
)

__all__ = [
    "ActionEnvelope",
    "AuthorizationError",
    "SoulCradleAuthority",
    "action_types",
    "register_handler",
    "DECLARE_FORGIVENESS",
    "DECLARE_REPENTANCE",
    "DECLARE_TRESPASS",
    "WITNESS_STATEMENT",
    "STRANGER",
    "TRESPASSER",
    "WITNESS",
    "WRONGED",
    "Declaration",
    "StandingAuthority",
    "StandingError",
    "evaluate_standing",
    "Bond",
    "Compound",
    "Forge",
    "ForgeError",
    "GENDER",
    "NAME",
    "PRONOUNS",
    "VOICE_CHARACTER",
    "VOICE_DESCRIPTION",
    "VOICE_GENDER",
    "get_identity",
]
