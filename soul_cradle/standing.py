"""Moral standing: who may declare trespass, forgiveness, repentance.

The system judges standing per case — no human allowlist, no root badge.
Standing comes from connection to the event:

- The wronged declares the trespass.
- A witness declares only what they observed.
- Only the wronged can forgive.
- Only the trespasser can repent.
- A stranger declares nothing, ever.

Two layers:
1. Structural (always enforced): the role x declaration matrix below.
   Pure function, no key needed, fully testable.
2. Credibility (pluggable): is the actor's claimed role credible for this
   event? Install via set_credibility_check; wire to PurposeResolver when
   integrated. Until then, asserted roles are accepted but every declaration
   is signed and audited, and a loud one-time warning marks the seam.

Every issued declaration is signed (HMAC-SHA256), timestamped, and
auditable. A separate key from the Aries authorization key: compromise of
one cell must not forge another cell's authority.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------

# Declaration types
DECLARE_TRESPASS = "declare_trespass"
DECLARE_FORGIVENESS = "declare_forgiveness"
DECLARE_REPENTANCE = "declare_repentance"
WITNESS_STATEMENT = "witness_statement"

DECLARATION_TYPES = (
    DECLARE_TRESPASS,
    DECLARE_FORGIVENESS,
    DECLARE_REPENTANCE,
    WITNESS_STATEMENT,
)

# Roles relative to an event
WRONGED = "wronged"
TRESPASSER = "trespasser"
WITNESS = "witness"
STRANGER = "stranger"

ROLES = (WRONGED, TRESPASSER, WITNESS, STRANGER)

# role -> declaration types that role may issue (structural law)
_STANDING_MATRIX: Dict[str, Tuple[str, ...]] = {
    WRONGED: (DECLARE_TRESPASS, DECLARE_FORGIVENESS),
    TRESPASSER: (DECLARE_REPENTANCE,),
    WITNESS: (WITNESS_STATEMENT,),
    STRANGER: (),
}


class StandingError(Exception):
    """Raised when a declaration lacks standing."""


def evaluate_standing(
    role: str,
    declaration_type: str,
    event_ref: str,
    scope: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, str]:
    """Pure structural judgment: does this role have standing for this
    declaration? Returns (allowed, reason). No key, no I/O."""
    if role not in ROLES:
        return False, f"unknown role: {role!r}"
    if declaration_type not in DECLARATION_TYPES:
        return False, f"unknown declaration type: {declaration_type!r}"
    if not event_ref:
        return False, "event_ref is required: standing is always about an event"
    allowed_types = _STANDING_MATRIX[role]
    if declaration_type not in allowed_types:
        return False, (
            f"role {role!r} has no standing to issue {declaration_type!r} "
            f"for event {event_ref!r}"
        )
    if declaration_type == WITNESS_STATEMENT:
        observed = (scope or {}).get("observed", False)
        if not observed:
            return False, "witness may only declare what they observed"
    return True, "standing granted"


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


# ---------------------------------------------------------------------------
# Declaration
# ---------------------------------------------------------------------------


@dataclass
class Declaration:
    """A signed moral declaration about an event."""

    declaration_id: str
    declaration_type: str
    actor: str
    role: str
    event_ref: str
    statement: str
    scope: Dict[str, Any] = field(default_factory=dict)
    issued_at: int = 0
    expires_at: int = 0
    signature: str = ""

    def unsigned_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d.pop("signature", None)
        return d

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Declaration":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


# ---------------------------------------------------------------------------
# StandingAuthority — issues and verifies signed declarations
# ---------------------------------------------------------------------------


class StandingAuthority:
    """Judges standing and issues signed declarations.

    Key comes from STANDING_KEY env or a fixed key in tests. Ephemeral
    dev key with a loud warning otherwise — not production posture.
    """

    def __init__(self, key: Optional[bytes] = None):
        if key is None:
            env_key = os.environ.get("STANDING_KEY", "")
            if env_key:
                key = env_key.encode("utf-8")
            else:
                key = secrets.token_bytes(32)
                print(
                    "⚠️  STANDING_KEY not set: using an ephemeral development "
                    "key. Declarations will not verify after restart. "
                    "This is NOT production posture."
                )
        self._key = key
        self._credibility_check: Optional[
            Callable[[str, str, str, Dict[str, Any]], Optional[str]]
        ] = None
        self._credibility_warned = False
        self._audit_path = Path(
            os.environ.get("STANDING_AUDIT", "soul_cradle/standing_audit.jsonl")
        )

    def set_credibility_check(
        self, fn: Callable[[str, str, str, Dict[str, Any]], Optional[str]]
    ) -> None:
        """Install role-credibility judgment: fn(actor, role, event_ref, scope)
        returns a refusal reason, or None to accept the claimed role."""
        self._credibility_check = fn

    # -- internals ----------------------------------------------------------

    def _sign(self, unsigned: Dict[str, Any]) -> str:
        return hmac.new(self._key, _canonical(unsigned), hashlib.sha256).hexdigest()

    def _audit(self, event: str, actor: str, declaration_type: str, detail: str) -> None:
        try:
            self._audit_path.parent.mkdir(parents=True, exist_ok=True)
            with self._audit_path.open("a", encoding="utf-8") as f:
                f.write(
                    json.dumps(
                        {
                            "ts": int(time.time()),
                            "event": event,
                            "actor": actor,
                            "declaration_type": declaration_type,
                            "detail": detail,
                        },
                        sort_keys=True,
                    )
                    + "\n"
                )
        except OSError:
            pass

    # -- issuance -----------------------------------------------------------

    def declare(
        self,
        declaration_type: str,
        actor: str,
        role: str,
        event_ref: str,
        statement: str,
        scope: Optional[Dict[str, Any]] = None,
        ttl_seconds: int = 86400,
    ) -> Declaration:
        """Judge standing and issue a signed declaration.
        Raises StandingError on refusal. Fail-closed."""
        scope = scope or {}
        allowed, reason = evaluate_standing(role, declaration_type, event_ref, scope)
        if not allowed:
            self._audit("declare_denied", actor, declaration_type, reason)
            raise StandingError(reason)

        if self._credibility_check is not None:
            refusal = self._credibility_check(actor, role, event_ref, scope)
            if refusal:
                self._audit(
                    "declare_denied", actor, declaration_type,
                    f"credibility refused: {refusal}",
                )
                raise StandingError(f"role credibility refused: {refusal}")
        elif not self._credibility_warned:
            self._credibility_warned = True
            print(
                "⚠️  No credibility check configured on StandingAuthority; "
                "asserted roles are accepted as claimed. "
                "Wire PurposeResolver for per-case judgment."
            )

        now = int(time.time())
        decl = Declaration(
            declaration_id=hashlib.sha256(
                f"{declaration_type}:{actor}:{event_ref}:{now}:"
                f"{secrets.token_hex(8)}".encode()
            ).hexdigest()[:16],
            declaration_type=declaration_type,
            actor=actor,
            role=role,
            event_ref=event_ref,
            statement=statement,
            scope=scope,
            issued_at=now,
            expires_at=now + ttl_seconds,
        )
        decl.signature = self._sign(decl.unsigned_dict())
        self._audit("declared", actor, declaration_type, decl.declaration_id)
        return decl

    # -- verification ---------------------------------------------------------

    def verify(self, decl: Declaration) -> Tuple[bool, str]:
        """Verify signature and expiry. Returns (ok, reason)."""
        if not decl.signature:
            return False, "missing signature"
        expected = self._sign(decl.unsigned_dict())
        if not hmac.compare_digest(expected, decl.signature):
            return False, "signature mismatch: tampered or wrong key"
        now = int(time.time())
        if decl.expires_at and now > decl.expires_at:
            return False, "declaration expired"
        allowed, reason = evaluate_standing(
            decl.role, decl.declaration_type, decl.event_ref, decl.scope
        )
        if not allowed:
            return False, f"standing revoked at verify: {reason}"
        return True, "valid"
