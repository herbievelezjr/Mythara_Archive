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

__all__ = [
    "ActionEnvelope",
    "AuthorizationError",
    "SoulCradleAuthority",
    "action_types",
    "register_handler",
]
