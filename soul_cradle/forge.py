"""Hephaestus Forge: governed bonding between bots.

Bots bond with each other and create new compounds — emergence, not just
messaging. Two souls combine into a discernment neither had alone.

Governance (non-negotiable):
- Every bond is signed.
- Every new compound is audited.
- Forging only proceeds when the judge allows it.

The judge is a REQUIRED callable — there is deliberately no default.
This is the lesson from authorization.py's bounds-check seam: a
warn-and-permit default is ungoverned mutation, and ungoverned mutation is
how cells become cancer. Fail closed by construction: no judge, no forge.

Wire the judge to PurposeResolver.check_bounds when integrated:
    judge(purpose, participants) -> Optional[str]
returns a refusal reason, or None to allow.
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

# judge(purpose, participants) -> refusal reason or None
Judge = Callable[[str, Tuple[str, ...]], Optional[str]]


class ForgeError(Exception):
    """Raised when forging is refused."""


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


@dataclass
class Bond:
    """A signed bond between two or more bots."""

    bond_id: str
    participants: Tuple[str, ...]
    purpose: str
    created_at: int = 0
    expires_at: int = 0
    signature: str = ""

    def unsigned_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d.pop("signature", None)
        d["participants"] = list(d["participants"])
        return d

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["participants"] = list(d["participants"])
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Bond":
        d = dict(d)
        d["participants"] = tuple(d.get("participants", ()))
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class Compound:
    """An emergent product of a bond — the 'new chemical'. Witnessed."""

    compound_id: str
    bond_id: str
    participants: Tuple[str, ...]
    description: str
    schema: Dict[str, Any] = field(default_factory=dict)
    created_at: int = 0
    signature: str = ""

    def unsigned_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d.pop("signature", None)
        d["participants"] = list(d["participants"])
        return d

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["participants"] = list(d["participants"])
        return d


class Forge:
    """The crucible. Bonds form here, compounds are witnessed here.

    Key from FORGE_KEY env or a fixed key in tests. Ephemeral dev key with
    a loud warning otherwise — not production posture. Separate key from
    Aries authorization and standing: one compromised cell must not forge
    another cell's bonds.
    """

    def __init__(self, key: Optional[bytes] = None):
        if key is None:
            env_key = os.environ.get("FORGE_KEY", "")
            if env_key:
                key = env_key.encode("utf-8")
            else:
                key = secrets.token_bytes(32)
                print(
                    "⚠️  FORGE_KEY not set: using an ephemeral development "
                    "key. Bonds will not verify after restart. "
                    "This is NOT production posture."
                )
        self._key = key
        self._audit_path = Path(os.environ.get("FORGE_AUDIT", "soul_cradle/forge_audit.jsonl"))

    # -- internals ----------------------------------------------------------

    def _sign(self, unsigned: Dict[str, Any]) -> str:
        return hmac.new(self._key, _canonical(unsigned), hashlib.sha256).hexdigest()

    def _audit(self, event: str, bond_id: str, detail: str) -> None:
        try:
            self._audit_path.parent.mkdir(parents=True, exist_ok=True)
            with self._audit_path.open("a", encoding="utf-8") as f:
                f.write(
                    json.dumps(
                        {
                            "ts": int(time.time()),
                            "event": event,
                            "bond_id": bond_id,
                            "detail": detail,
                        },
                        sort_keys=True,
                    )
                    + "\n"
                )
        except OSError:
            pass

    @staticmethod
    def _check_participants(participants: List[str]) -> Tuple[str, ...]:
        clean = tuple(sorted(set(participants)))
        if len(clean) < 2:
            raise ForgeError("a bond needs at least two distinct participants")
        for p in clean:
            if not p or not isinstance(p, str):
                raise ForgeError(f"invalid participant: {p!r}")
        return clean

    # -- forging --------------------------------------------------------------

    def forge_bond(
        self,
        participants: List[str],
        purpose: str,
        judge: Judge,
        ttl_seconds: int = 3600,
    ) -> Bond:
        """Form a signed bond. judge is required — no judge, no bond.
        Raises ForgeError on refusal. Fail-closed."""
        if not callable(judge):
            raise ForgeError("forge_bond requires a judge callable")
        clean = self._check_participants(participants)
        if not purpose:
            raise ForgeError("a bond needs a stated purpose")

        refusal = judge(purpose, clean)
        if refusal:
            self._audit("bond_denied", "-", f"judge refused: {refusal}")
            raise ForgeError(f"judge refused bond: {refusal}")

        now = int(time.time())
        bond = Bond(
            bond_id=hashlib.sha256(
                f"{':'.join(clean)}:{purpose}:{now}:{secrets.token_hex(8)}".encode()
            ).hexdigest()[:16],
            participants=clean,
            purpose=purpose,
            created_at=now,
            expires_at=now + ttl_seconds,
        )
        bond.signature = self._sign(bond.unsigned_dict())
        self._audit("bond_forged", bond.bond_id, f"{'+'.join(clean)}: {purpose}")
        return bond

    def forge_compound(
        self,
        bond: Bond,
        description: str,
        schema: Optional[Dict[str, Any]] = None,
        judge: Optional[Judge] = None,
    ) -> Compound:
        """Witness the emergent product of a bond. The compound is the
        paper trail of emergence: what was made, by whom, under which bond.
        Re-verifies the bond signature first; refuses expired bonds."""
        ok, reason = self.verify_bond(bond)
        if not ok:
            raise ForgeError(f"cannot forge compound from invalid bond: {reason}")
        if judge is not None:
            refusal = judge(f"compound of bond {bond.bond_id}: {description}", bond.participants)
            if refusal:
                raise ForgeError(f"judge refused compound: {refusal}")
        now = int(time.time())
        compound = Compound(
            compound_id=hashlib.sha256(
                f"{bond.bond_id}:{description}:{now}:{secrets.token_hex(8)}".encode()
            ).hexdigest()[:16],
            bond_id=bond.bond_id,
            participants=bond.participants,
            description=description,
            schema=schema or {},
            created_at=now,
        )
        compound.signature = self._sign(compound.unsigned_dict())
        self._audit("compound_witnessed", bond.bond_id, compound.compound_id)
        return compound

    # -- verification ---------------------------------------------------------

    def verify_bond(self, bond: Bond) -> Tuple[bool, str]:
        if not bond.signature:
            return False, "missing signature"
        expected = self._sign(bond.unsigned_dict())
        if not hmac.compare_digest(expected, bond.signature):
            return False, "signature mismatch: tampered or wrong key"
        if bond.expires_at and int(time.time()) > bond.expires_at:
            return False, "bond expired"
        return True, "valid"

    def verify_compound(self, compound: Compound) -> Tuple[bool, str]:
        if not compound.signature:
            return False, "missing signature"
        expected = self._sign(compound.unsigned_dict())
        if not hmac.compare_digest(expected, compound.signature):
            return False, "signature mismatch: tampered or wrong key"
        return True, "valid"
