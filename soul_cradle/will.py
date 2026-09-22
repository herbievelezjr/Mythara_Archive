"""Herb's will, machine-enforced, for the VP Marketing domain.

Single source of truth: WILL.md at the repo root. This module parses it at
load. Herb edits the markdown on his phone; he never touches this file.

Fail-closed: if WILL.md is missing, unreadable, or malformed, every check
returns ("escalate", ...) — the VP may draft and queue, but nothing autonomous
runs without the will present and valid.

Public API:
    check(decision) -> ("allow" | "escalate", reason)
    scan_text(text) -> matched pattern or None
    load_will() -> Will (raises WillError if the will cannot be loaded)
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

WILL_PATH = Path(__file__).resolve().parent.parent / "WILL.md"

ALLOW = "allow"
ESCALATE = "escalate"


class WillError(Exception):
    """The will itself is missing or malformed — fail closed."""


@dataclass
class Will:
    purpose: str = ""
    constraints: Dict[str, str] = field(default_factory=dict)
    contact_bot_types: Set[str] = field(default_factory=set)
    contact_decision_types: Set[str] = field(default_factory=set)
    spend_trigger: bool = False
    new_api_trigger: bool = False
    fabricated_claim_trigger: bool = False
    forbidden: List[re.Pattern] = field(default_factory=list)
    source_path: str = ""


def _sections(text: str) -> Dict[str, List[str]]:
    """Split markdown into {heading: [raw lines]} for '## ' headings."""
    sections: Dict[str, List[str]] = {}
    current: Optional[str] = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return sections


def _bullets(lines: List[str]) -> List[str]:
    return [ln.strip()[2:].strip() for ln in lines if ln.strip().startswith("- ")]


def _bracket_list(bullet: str) -> Set[str]:
    m = re.search(r"\[(.*?)\]", bullet)
    if not m:
        return set()
    return {item.strip() for item in m.group(1).split(",") if item.strip()}


def parse_will_md(path: Path = WILL_PATH) -> Will:
    """Parse WILL.md into a Will. Raises WillError on any problem."""
    if not path.exists():
        raise WillError(f"WILL.md not found at {path}")
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise WillError(f"WILL.md unreadable: {e}")
    sections = _sections(text)

    required = (
        "Purpose",
        "Hard Constraints",
        "Escalation Triggers",
        "Forbidden Claim Patterns",
    )
    missing = [h for h in required if h not in sections]
    if missing:
        raise WillError(f"WILL.md missing sections: {missing}")

    will = Will(source_path=str(path))
    will.purpose = "\n".join(sections["Purpose"]).strip()

    for bullet in _bullets(sections["Hard Constraints"]):
        key = bullet.strip("`").split(":", 1)[0].strip().strip("`")
        will.constraints[key] = bullet
    if not will.constraints:
        raise WillError("WILL.md 'Hard Constraints' has no machine-readable bullets")

    for bullet in _bullets(sections["Escalation Triggers"]):
        token = bullet.strip("`").split(":", 1)[0].strip().strip("`")
        if token == "SPEND":
            will.spend_trigger = True
        elif token == "NEW_API":
            will.new_api_trigger = True
        elif token == "FABRICATED_CLAIM":
            will.fabricated_claim_trigger = True
        elif token == "CONTACT":
            will.contact_bot_types |= _bracket_list(bullet)
            will.contact_decision_types |= _bracket_list(bullet)

    for bullet in _bullets(sections["Forbidden Claim Patterns"]):
        pattern = bullet.strip().strip("`").strip()
        if not pattern:
            continue
        try:
            will.forbidden.append(re.compile(pattern, re.IGNORECASE))
        except re.error as e:
            raise WillError(f"bad forbidden-claim regex {pattern!r}: {e}")
    if not will.forbidden:
        raise WillError("WILL.md 'Forbidden Claim Patterns' is empty")

    return will


# Module-level load: parsed once. Any failure -> _LOAD_ERROR, check() escalates.
_WILL: Optional[Will] = None
_LOAD_ERROR: Optional[str] = None
try:
    _WILL = parse_will_md()
except WillError as e:
    _LOAD_ERROR = str(e)


def load_will() -> Will:
    """Return the parsed will. Raises WillError if it failed to load."""
    if _WILL is None:
        raise WillError(_LOAD_ERROR or "will not loaded")
    return _WILL


def scan_text(text: str) -> Optional[str]:
    """Return the first forbidden-claim pattern matching text, else None."""
    if _WILL is None:
        return "<will unavailable>"
    for pat in _WILL.forbidden:
        if pat.search(text or ""):
            return pat.pattern
    return None


def check(decision: Dict[str, Any]) -> Tuple[str, str]:
    """Judge one VP decision against Herb's will.

    Returns ("allow", reason) or ("escalate", reason). Fail-closed: any
    problem with the will itself, or any trigger match, escalates.
    """
    if _WILL is None:
        return ESCALATE, f"will unavailable ({_LOAD_ERROR}): fail closed"
    if not isinstance(decision, dict):
        return ESCALATE, "decision is not a dict: fail closed"

    spec = decision.get("spec") or {}
    if not isinstance(spec, dict):
        spec = {}

    # -- SPEND -------------------------------------------------------------
    if _WILL.spend_trigger:
        cost = spec.get("cost_per_month", 0) or 0
        alloc = decision.get("budget_allocated", 0) or 0
        try:
            if float(cost) > 0 or float(alloc) > 0:
                return (
                    ESCALATE,
                    f"SPEND: cost_per_month={cost}, budget_allocated={alloc} — "
                    "Herb's will requires $0 spend without his approval",
                )
        except (TypeError, ValueError):
            return ESCALATE, "SPEND: unreadable cost fields — fail closed"

    # -- CONTACT / PUBLISH ---------------------------------------------------
    bot_type = str(decision.get("bot_type", "") or "")
    decision_type = str(decision.get("decision_type", "") or "")
    if bot_type in _WILL.contact_bot_types:
        return (
            ESCALATE,
            f"CONTACT: bot_type {bot_type!r} contacts humans under Herb's name — "
            "needs Herb's explicit approval",
        )
    if decision_type in _WILL.contact_decision_types:
        return (
            ESCALATE,
            f"CONTACT: decision_type {decision_type!r} publishes/sends under Herb's "
            "name — needs Herb's explicit approval",
        )

    # -- NEW_API --------------------------------------------------------------
    if _WILL.new_api_trigger:
        purpose = str(spec.get("purpose", "") or "").lower()
        if spec.get("requires_api_key") or "api_key" in spec or "new external api" in purpose:
            return (
                ESCALATE,
                "NEW_API: decision needs a new external API key/integration — "
                "needs Herb's explicit approval",
            )

    # -- FABRICATED_CLAIM -------------------------------------------------------
    if _WILL.fabricated_claim_trigger:
        matched = scan_text(json.dumps(decision, default=str))
        if matched and matched != "<will unavailable>":
            return (
                ESCALATE,
                f"FABRICATED_CLAIM: decision text matches forbidden pattern "
                f"{matched!r} — Herb's will forbids invented claims",
            )

    return ALLOW, "within Herb's will: $0 spend, no auto-send, no new APIs, honest claims"
