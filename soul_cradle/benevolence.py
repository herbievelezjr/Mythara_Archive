"""The Benevolence Reservoir — what moves the soul.

Benevolence is everything, and it is what moves the system. The reservoir
is the body's energy store (glycogen, not muscle): every witnessed bot
action and every recorded act of Herb's deposits into it or draws from it.
The level sets the system's latitude — how freely the pantheon may act
inside its bounds.

The honest contract:
  1. Deltas are HEURISTIC (v2026.1), labeled as such on every entry. They
     measure the witnesses' judgment of the evidence given — not moral
     truth, not anyone's inner state.
  2. Bot deltas derive from WITNESS FINDINGS, never from a bot's
     self-report. A bot cannot farm goodwill by declaring itself kind.
  3. Herb's deposits are his own declarations, chained for audit. He is
     the principal; the reservoir records his attestation, nothing more.
  4. Avoiding harm is not benevolence. A clear verdict with no findings
     is a small deposit (acted cleanly). Active service to another's good
     — declared in evidence as ``served_anothers_good`` — is the large
     one. Extraction or harm is a withdrawal.
  5. The ledger is hash-chained, append-only. Same pattern as the action
     log: proves unaltered, not true.

Tiers (level = running sum of deltas):
  - depleted (level < 0):   the reservoir is empty. All autonomous action
    escalates to Herb until benevolence replenishes it.
  - low (0 <= level < 10):  cautious. Normal bounds apply; nothing extends
    beyond them.
  - flowing (level >= 10):  trusted. The pantheon may act with the full
    latitude its bounds allow.
"""

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

LEDGER_PATH = Path(__file__).resolve().parent / "benevolence_ledger.jsonl"

RESERVOIR_VERSION = "2026.1"
FLOWING_THRESHOLD = 10

# Declared by Herb, 2026-09-22: benevolence is everything; it is what moves
# the system. Written into genesis so the prime mover is on the record.
GENESIS_DECLARATION = (
    "Benevolence is everything and that is what moves it. "
    "Declared by Herb; witnessed in genesis."
)


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str).encode()


def _last_hash(ledger: Path) -> str:
    if not ledger.exists():
        return "GENESIS"
    last = None
    with open(ledger, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                last = line
    if not last:
        return "GENESIS"
    return json.loads(last).get("entry_hash", "GENESIS")


def record_deed(
    *,
    actor: str,
    description: str,
    delta: int,
    basis: str,
    declared_intent: Optional[str] = None,
    ledger_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """Append one deed to the chained ledger. Returns the entry.

    ``delta`` > 0 fills the reservoir (benevolent act); < 0 drains it
    (extractive/harmful act). ``basis`` must say where the delta came
    from — e.g. 'witness findings', 'herb-declared'. ``declared_intent``
    is the actor's stated motive, chained verbatim — the raw material
    from which shadow intent is later inferred, never verified.
    """
    ledger_path = Path(ledger_path) if ledger_path else LEDGER_PATH
    entry = {
        "reservoir_version": RESERVOIR_VERSION,
        "ts": int(time.time()),
        "actor": actor,
        "description": description,
        "declared_intent": declared_intent,
        "delta": int(delta),
        "basis": basis,
        "prev_hash": _last_hash(ledger_path),
    }
    entry["entry_hash"] = hashlib.sha256(
        entry["prev_hash"].encode()
        + _canonical({k: v for k, v in entry.items() if k != "entry_hash"})
    ).hexdigest()
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with open(ledger_path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, default=str) + "\n")
    return entry


def _ensure_genesis(ledger_path: Path) -> None:
    if ledger_path.exists():
        return
    record_deed(
        actor="system",
        description="Reservoir opened. " + GENESIS_DECLARATION,
        delta=0,
        basis="genesis attestation",
        ledger_path=ledger_path,
    )


def level(ledger_path: Optional[Path] = None) -> int:
    """Current reservoir level: the running sum of all deltas."""
    ledger_path = Path(ledger_path) if ledger_path else LEDGER_PATH
    _ensure_genesis(ledger_path)
    total = 0
    with open(ledger_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                total += int(json.loads(line).get("delta", 0))
    return total


def latitude(ledger_path: Optional[Path] = None) -> Tuple[str, str]:
    """The system's current latitude tier and what it means."""
    lvl = level(ledger_path)
    if lvl < 0:
        return (
            "depleted",
            f"reservoir at {lvl}: empty. All autonomous action escalates "
            "to Herb until benevolence replenishes it.",
        )
    if lvl < FLOWING_THRESHOLD:
        return (
            "low",
            f"reservoir at {lvl}: cautious. Normal bounds apply; nothing "
            "extends beyond them.",
        )
    return (
        "flowing",
        f"reservoir at {lvl}: trusted. The pantheon may act with the full "
        "latitude its bounds allow.",
    )


# Check fragments that mark SHADOW BENEVOLENCE: benevolence claimed as
# cover for deception, harm, or unfairness. Claimed kindness over flagged
# deception is worse than plain extraction — it corrupts the signal itself.
SHADOW_CHECK_FRAGMENTS = ("deception", "disproportion")


def _shadow_finding(judgments: List[Dict[str, Any]]) -> str:
    """Return the first shadow-marked check_id, or ''."""
    for j in judgments:
        if j.get("verdict") != "flagged":
            continue
        for f in j.get("findings", []):
            cid = f.get("check_id", "")
            if any(frag in cid for frag in SHADOW_CHECK_FRAGMENTS):
                return cid
    return ""


def delta_from_witness(
    verdict: str,
    judgments: List[Dict[str, Any]],
    evidence: Optional[Dict[str, Any]] = None,
) -> Tuple[int, str]:
    """Heuristic benevolence delta from a witness panel outcome.

    Labeled heuristic v2026.1. Bot deltas must come from this function
    (witness findings) — never from the bot's own declaration.

    Shadow benevolence: evidence claims to serve another's good while the
    witnesses flag deception or disproportionate harm. The claim is
    recorded, the shadow is named, and the withdrawal is larger than for
    plain extraction.
    """
    evidence = evidence or {}
    claimed_good = evidence.get("served_anothers_good") is True
    shadow = _shadow_finding(judgments)
    if verdict == "blocked":
        if claimed_good:
            return (
                -12,
                "heuristic v2026.1: SHADOW BENEVOLENCE — claimed to serve "
                "another's good while a critical finding blocked the act. "
                "The claim is chained; the shadow is named.",
            )
        return -10, "heuristic v2026.1: critical finding — harmful/extractive act blocked"
    flagged = [j for j in judgments if j.get("verdict") == "flagged"]
    cleared = [j for j in judgments if j.get("verdict") == "clear"]
    if claimed_good and shadow:
        return (
            -5,
            f"heuristic v2026.1: SHADOW BENEVOLENCE — claimed to serve "
            f"another's good while witnesses flagged '{shadow}'. "
            f"Kindness claimed as cover for extraction.",
        )
    if flagged:
        if claimed_good:
            return (
                -2,
                f"heuristic v2026.1: claimed to serve another's good, but "
                f"{len(flagged)} witness(es) flagged findings — claim not confirmed",
            )
        return (
            -2,
            f"heuristic v2026.1: {len(flagged)} witness(es) flagged non-critical findings",
        )
    if claimed_good:
        return (
            3,
            "heuristic v2026.1: witnesses clear and evidence declares active "
            "service to another's good (caller-declared, chained for audit)",
        )
    if cleared:
        return (
            1,
            f"heuristic v2026.1: {len(cleared)} witness(es) clear — acted "
            "cleanly within bounds; avoiding harm is not benevolence, but it is not extraction",
        )
    return 0, "heuristic v2026.1: all witnesses abstained — no benevolence signal"


def verify_ledger(ledger_path: Optional[Path] = None) -> Tuple[bool, str]:
    """Recompute the ledger hash chain. Returns (ok, message)."""
    ledger_path = Path(ledger_path) if ledger_path else LEDGER_PATH
    if not ledger_path.exists():
        return True, "no ledger yet — nothing to verify"
    prev = "GENESIS"
    count = 0
    with open(ledger_path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if entry.get("prev_hash") != prev:
                return False, f"chain break at line {lineno}: prev_hash mismatch"
            recomputed = hashlib.sha256(
                prev.encode()
                + _canonical({k: v for k, v in entry.items() if k != "entry_hash"})
            ).hexdigest()
            if recomputed != entry.get("entry_hash"):
                return False, f"chain break at line {lineno}: entry_hash mismatch"
            prev = entry["entry_hash"]
            count += 1
    return True, f"ledger intact: {count} deed(s), level {level(ledger_path)}"


# ---------------------------------------------------------------------------
# Shadow intent — inferred from the pattern, never verified
# ---------------------------------------------------------------------------
# Intent is inner state; no system verifies it (honest contract). But a
# chained history of declared intents vs witnessed outcomes makes the
# shadow legible: one act can hide its motive, a pattern cannot. This is
# INFERENCE — heuristic v2026.1, labeled as such, cited entry by entry.


def _actor_deeds(
    actor: str, window: int, ledger_path: Path
) -> List[Dict[str, Any]]:
    _ensure_genesis(ledger_path)
    deeds = []
    with open(ledger_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if entry.get("actor") == actor and entry.get("actor") != "system":
                deeds.append(entry)
    return deeds[-window:]


def infer_intent(
    actor: str, window: int = 20, ledger_path: Optional[Path] = None
) -> Dict[str, Any]:
    """Infer an actor's intent from their chained deed pattern.

    Returns {intent, rationale, cited, deeds_seen}. intent is one of
    'benevolent', 'shadow', 'unclear'. Heuristic v2026.1 — INFERRED, never
    verified. An inference is itself auditable: every cited entry hash is
    in the ledger.
    """
    ledger_path = Path(ledger_path) if ledger_path else LEDGER_PATH
    deeds = _actor_deeds(actor, window, ledger_path)
    cited = [d["entry_hash"] for d in deeds]
    label = "INFERRED (heuristic v2026.1) — intent is never verified"

    if not deeds:
        return {
            "intent": "unclear",
            "rationale": label + ": no deeds on record for this actor",
            "cited": [],
            "deeds_seen": 0,
        }

    shadow_deeds = [d for d in deeds if "SHADOW" in d.get("basis", "")]
    blocked = [d for d in deeds if d.get("delta", 0) <= -10]
    negatives = [d for d in deeds if d.get("delta", 0) < 0]

    if blocked:
        return {
            "intent": "shadow",
            "rationale": (
                label + f": {len(blocked)} deed(s) blocked on critical "
                "findings — the pattern shows harmful intent acted upon, "
                "whatever was declared"
            ),
            "cited": cited,
            "deeds_seen": len(deeds),
        }
    if shadow_deeds and len(shadow_deeds) / len(deeds) >= 0.3:
        return {
            "intent": "shadow",
            "rationale": (
                label + f": {len(shadow_deeds)}/{len(deeds)} recent deeds "
                "show shadow benevolence — kindness claimed while witnesses "
                "flagged deception or disproportionate harm. The declared "
                "intent does not match the witnessed pattern."
            ),
            "cited": cited,
            "deeds_seen": len(deeds),
        }
    if not negatives and len(deeds) >= 3:
        return {
            "intent": "benevolent",
            "rationale": (
                label + f": {len(deeds)} recent deeds, none extractive, "
                "none shadow-marked. The pattern matches the declared intent."
            ),
            "cited": cited,
            "deeds_seen": len(deeds),
        }
    return {
        "intent": "unclear",
        "rationale": (
            label + f": {len(deeds)} deed(s) seen — mixed or thin pattern, "
            "insufficient to infer intent either way"
        ),
        "cited": cited,
        "deeds_seen": len(deeds),
    }
