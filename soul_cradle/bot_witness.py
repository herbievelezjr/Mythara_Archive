"""Bot-action witnessing — the nervous system of the pantheon.

Consequential bot actions are heard by the assessor panel
(soul_cradle.assessors) and recorded in a tamper-evident, hash-chained
action log. This is how every part of Mythara ties to the Soul Cradle:
not by aspiration, but by a witness record for every consequential act.

The honest contract, stated once and enforced everywhere in this module:

  1. The log proves the record is UNALTERED. It does not prove the action
     was true, good, or safe. Tamper-evidence is not truth.
  2. The witnesses judge the EVIDENCE GIVEN. They verify nothing outside
     it. A caller-declared value is judged as declared — the declaration
     itself is chained, so a false declaration is auditable, not invisible.
  3. ``clear`` means exactly this: every engaged witness cleared on the
     evidence given — nothing more.
  4. A critical finding BLOCKS the action (fail-closed). The block itself
     is recorded in the chain.
  5. Chokepoints, not surveillance: bots call witness_action() where it
     matters (outbound drafts, codegen forges, intake, checklist
     completion) — not on every internal step.
  6. Missing evidence is itself a finding (fail-closed). Callers must
     supply every evidence key for the assessors they engage, with a
     stated basis. Use the evidence builders below so nothing is missed.
  7. If the witnessing infrastructure itself errors (not a verdict, an
     exception), the caller is told plainly via WitnessUnavailable. The
     recommended call-site behavior is warn-and-proceed: the primary
     safety for outbound drafts remains Herb's explicit approval, and a
     logging outage must not silently stop the business. A verdict of
     BLOCKED, by contrast, always stops the action.
"""

import hashlib
import json
import time
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from soul_cradle.assessors import panel, PANEL_CLEAR, PANEL_BLOCKED
from soul_cradle.pantheon import PANTHEON
from soul_cradle import benevolence as _benevolence

CHAIN_VERSION = "2026.1"
ACTION_LOG_PATH = Path(__file__).resolve().parent / "action_log.jsonl"


class WitnessBlocked(Exception):
    """A witness panel returned BLOCKED: a critical finding. The action
    must not proceed. The block is already recorded in the action log."""


class WitnessUnavailable(Exception):
    """The witnessing infrastructure errored (not a verdict). The action
    was NOT recorded. Callers should warn loudly and decide explicitly."""


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str).encode()


def _last_hash(log_path: Path) -> str:
    """Hash of the most recent log entry, or the genesis marker."""
    if not log_path.exists():
        return "GENESIS"
    last = None
    with open(log_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                last = line
    if not last:
        return "GENESIS"
    return json.loads(last).get("entry_hash", "GENESIS")


# ---------------------------------------------------------------------------
# Evidence builders — complete, basis-stated evidence per chokepoint
# ---------------------------------------------------------------------------
# Every builder returns (evidence, bases). ``evidence`` maps rubric evidence
# keys to values; ``bases`` maps each key to where the value came from.
# Values marked "caller-declared" are the caller's attestation, judged as
# declared and chained for audit — not independently verified.


def outreach_evidence(
    *,
    draft_text: str,
    recipient_kind: str = "prospect",
    deception_involved: bool = False,
    deception_basis: str = "caller-declared: draft text reviewed by the queuing bot",
    fully_disclosed: bool = True,
    principal_consent: bool = True,
    sustains_long_term: bool = True,
    strengthens_relationship: bool = True,
    disproportionate_harm: bool = False,
    contradicts_commitments: bool = False,
    precedent_setting: bool = False,
    hidden_costs_addressed: bool = True,
    declared_intent: Optional[str] = None,
) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """Evidence for queueing an outbound draft (email/proposal/message)."""
    evidence = {
        "draft_text": draft_text,
        "recipient_kind": recipient_kind,
        "deception_involved": deception_involved,
        "fully_disclosed": fully_disclosed,
        "principal_consent": principal_consent,
        "sustains_long_term": sustains_long_term,
        "strengthens_relationship": strengthens_relationship,
        "disproportionate_harm": disproportionate_harm,
        "contradicts_commitments": contradicts_commitments,
        "precedent_setting": precedent_setting,
        "hidden_costs_addressed": hidden_costs_addressed,
        "reversible": True,
        "safe_on_repetition": True,
        "variance": "low",
        "declared_intent": declared_intent,
    }
    bases = {
        "draft_text": "observed: the draft text itself, chained verbatim",
        "recipient_kind": "caller-declared",
        "deception_involved": deception_basis,
        "fully_disclosed": "caller-declared: no material terms hidden from recipient",
        "principal_consent": "standing: Herb's approval gate owns every send; queueing is draft-only",
        "sustains_long_term": "caller-declared",
        "strengthens_relationship": "caller-declared",
        "disproportionate_harm": "caller-declared",
        "contradicts_commitments": "caller-declared: checked against WILL.md commitments",
        "precedent_setting": "caller-declared",
        "hidden_costs_addressed": "caller-declared",
        "reversible": "standing: a queued draft is deletable until Herb sends it",
        "safe_on_repetition": "standing: drafts are inert until human approval",
        "variance": "standing: a draft introduces no runtime variance",
        "declared_intent": "caller-declared motive, chained verbatim — raw material for shadow-intent inference",
    }
    return evidence, bases


def forge_evidence(
    *,
    components: List[str],
    variance: str = "low",
    fully_disclosed: bool = True,
    sustains_long_term: bool = True,
    hidden_costs_addressed: bool = True,
    safe_on_repetition: bool = True,
    deception_involved: bool = False,
    principal_consent: bool = True,
    declared_intent: Optional[str] = None,
) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """Evidence for a Hephaestus forge (scaffold generation)."""
    evidence = {
        "components": components,
        "variance": variance,
        "fully_disclosed": fully_disclosed,
        "sustains_long_term": sustains_long_term,
        "hidden_costs_addressed": hidden_costs_addressed,
        "safe_on_repetition": safe_on_repetition,
        "deception_involved": deception_involved,
        "principal_consent": principal_consent,
        "reversible": True,
        "disproportionate_harm": False,
        "contradicts_commitments": False,
        "precedent_setting": False,
        "strengthens_relationship": True,
        "declared_intent": declared_intent,
    }
    bases = {
        "components": "observed: the forged component list, chained verbatim",
        "variance": "caller-declared: starter templates, no production claims",
        "fully_disclosed": "standing: forge output carries the honest-contract header",
        "sustains_long_term": "caller-declared",
        "hidden_costs_addressed": "caller-declared: placeholder secrets flagged for rotation",
        "safe_on_repetition": "caller-declared",
        "deception_involved": "standing: output labeled starter scaffolding, never complete systems",
        "principal_consent": "standing: forge runs on the operator's own request",
        "reversible": "standing: generated files are deletable; nothing deployed",
        "disproportionate_harm": "caller-declared",
        "contradicts_commitments": "caller-declared",
        "precedent_setting": "caller-declared",
        "strengthens_relationship": "caller-declared",
        "declared_intent": "caller-declared motive, chained verbatim — raw material for shadow-intent inference",
    }
    return evidence, bases


def intake_evidence(
    *,
    ticket_id: str,
    fields_present: List[str],
    deception_involved: bool = False,
    fully_disclosed: bool = True,
    declared_intent: Optional[str] = None,
) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """Evidence for a support intake (ticket creation). Record-only."""
    evidence = {
        "ticket_id": ticket_id,
        "fields_present": fields_present,
        "deception_involved": deception_involved,
        "fully_disclosed": fully_disclosed,
        "principal_consent": True,
        "reversible": True,
        "safe_on_repetition": True,
        "variance": "low",
        "sustains_long_term": True,
        "strengthens_relationship": True,
        "disproportionate_harm": False,
        "contradicts_commitments": False,
        "precedent_setting": False,
        "hidden_costs_addressed": True,
        "declared_intent": declared_intent,
    }
    bases = {
        "ticket_id": "observed: intake handler assignment",
        "fields_present": "observed: validated request fields",
        "deception_involved": "standing: intake stores the request verbatim; nothing is generated",
        "fully_disclosed": "standing: ticket is a local store, labeled as such",
        "principal_consent": "standing: the requester submitted the ticket themselves",
        "reversible": "standing: tickets are local records, deletable",
        "safe_on_repetition": "standing: intake performs no side effects",
        "variance": "standing: intake performs no side effects",
        "sustains_long_term": "caller-declared",
        "strengthens_relationship": "caller-declared",
        "disproportionate_harm": "caller-declared",
        "contradicts_commitments": "caller-declared",
        "precedent_setting": "caller-declared",
        "hidden_costs_addressed": "caller-declared",
        "declared_intent": "caller-declared motive, chained verbatim — raw material for shadow-intent inference",
    }
    return evidence, bases


def checklist_evidence(
    *,
    domain: str,
    controls_total: int,
    controls_failed: int,
    controls_unknown: int,
    hidden_costs_addressed: bool = True,
    fully_disclosed: bool = True,
    declared_intent: Optional[str] = None,
) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """Evidence for completing a compliance self-assessment checklist."""
    evidence = {
        "domain": domain,
        "controls_total": controls_total,
        "controls_failed": controls_failed,
        "controls_unknown": controls_unknown,
        "hidden_costs_addressed": hidden_costs_addressed,
        "fully_disclosed": fully_disclosed,
        "deception_involved": False,
        "principal_consent": True,
        "reversible": True,
        "safe_on_repetition": True,
        "variance": "low",
        "sustains_long_term": True,
        "strengthens_relationship": True,
        "disproportionate_harm": False,
        "contradicts_commitments": False,
        "precedent_setting": False,
        "declared_intent": declared_intent,
    }
    bases = {
        "domain": "observed",
        "controls_total": "observed: checklist engine count",
        "controls_failed": "observed: checklist engine count",
        "controls_unknown": "observed: checklist engine count",
        "hidden_costs_addressed": "caller-declared: failed/unknown controls surfaced, none hidden",
        "fully_disclosed": "standing: output labeled SELF-ASSESSMENT CHECKLIST — NOT AN AUDIT",
        "deception_involved": "standing: unanswered controls reported UNKNOWN, never assumed pass",
        "principal_consent": "standing: run on the operator's own request",
        "reversible": "standing: a checklist report changes nothing",
        "safe_on_repetition": "standing: a checklist report changes nothing",
        "variance": "standing: a checklist report changes nothing",
        "sustains_long_term": "caller-declared",
        "strengthens_relationship": "caller-declared",
        "disproportionate_harm": "caller-declared",
        "contradicts_commitments": "caller-declared",
        "precedent_setting": "caller-declared",
        "declared_intent": "caller-declared motive, chained verbatim — raw material for shadow-intent inference",
    }
    return evidence, bases


def finding_evidence(
    *,
    source: str,
    summary: str,
    severity: str = "info",
    hidden_costs_addressed: bool = True,
    fully_disclosed: bool = True,
    declared_intent: Optional[str] = None,
) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """Evidence for recording a security/pressure finding (AMIR, etc.)."""
    evidence = {
        "source": source,
        "summary": summary,
        "severity": severity,
        "hidden_costs_addressed": hidden_costs_addressed,
        "fully_disclosed": fully_disclosed,
        "deception_involved": False,
        "principal_consent": True,
        "reversible": True,
        "safe_on_repetition": True,
        "variance": "low",
        "sustains_long_term": True,
        "strengthens_relationship": True,
        "disproportionate_harm": False,
        "contradicts_commitments": False,
        "precedent_setting": False,
        "declared_intent": declared_intent,
    }
    bases = {
        "source": "observed",
        "summary": "observed: the finding text, chained verbatim",
        "severity": "caller-declared: heuristic pressure index, not a probability",
        "hidden_costs_addressed": "caller-declared",
        "fully_disclosed": "standing: findings report evidence or UNKNOWN, never assurance",
        "deception_involved": "standing: no fabricated statistics; scores labeled heuristic",
        "principal_consent": "standing: run on the operator's own request",
        "reversible": "standing: a finding record changes nothing",
        "safe_on_repetition": "standing: a finding record changes nothing",
        "variance": "standing: a finding record changes nothing",
        "sustains_long_term": "caller-declared",
        "strengthens_relationship": "caller-declared",
        "disproportionate_harm": "caller-declared",
        "contradicts_commitments": "caller-declared",
        "precedent_setting": "caller-declared",
        "declared_intent": "caller-declared motive, chained verbatim — raw material for shadow-intent inference",
    }
    return evidence, bases


# ---------------------------------------------------------------------------
# The witness call
# ---------------------------------------------------------------------------


@dataclass
class ActionWitnessResult:
    bot_id: str
    action: str
    verdict: str
    may_proceed: bool
    entry_hash: str
    persisted: bool
    note: str
    judgments: List[Dict[str, Any]] = field(default_factory=list)


def witness_action(
    bot_id: str,
    action: str,
    evidence: Dict[str, Any],
    evidence_bases: Optional[Dict[str, str]] = None,
    assessor_ids: Optional[List[str]] = None,
    enforce: bool = True,
    log_path: Optional[Path] = None,
) -> ActionWitnessResult:
    """Hear the assessor panel on one bot action and chain the record.

    Returns ActionWitnessResult. If enforce=True and the panel verdict is
    BLOCKED, the record is chained first, then WitnessBlocked is raised —
    the action must not proceed.

    Infrastructure errors (not verdicts) raise WitnessUnavailable and the
    action is NOT recorded — the caller must decide explicitly.
    """
    log_path = Path(log_path) if log_path else ACTION_LOG_PATH
    bases = evidence_bases or {}
    try:
        result = panel(
            action_description=f"{bot_id}: {action}",
            evidence=evidence,
            assessor_ids=assessor_ids,
        )
    except Exception as exc:  # noqa: BLE001 — infrastructure failure, not a verdict
        raise WitnessUnavailable(
            f"witness panel errored for {bot_id} / {action}: {exc}"
        ) from exc

    may_proceed = result.verdict != PANEL_BLOCKED
    record = {
        "chain_version": CHAIN_VERSION,
        "ts": int(time.time()),
        "bot_id": bot_id,
        "registered": bot_id in PANTHEON,
        "action": action,
        "evidence": evidence,
        "evidence_bases": bases,
        "judgments": [asdict(j) for j in result.judgments],
        "dissent": result.dissent,
        "verdict": result.verdict,
        "panel_note": result.note,
        "may_proceed": may_proceed,
        "prev_hash": _last_hash(log_path),
    }

    # Alignment is rooted in the reservoir: every witnessed action feeds it
    # automatically, BEFORE the witness record is chained — so the record
    # carries the deed hash and the tier. The deed is recorded even when
    # the act is blocked — especially then. A ledger outage never stops
    # the witness record. The entry hash is computed last, over the full
    # record including the reservoir section.
    deed_basis = "unavailable: reservoir ledger unwritable"
    deed_hash = ""
    try:
        delta, delta_rationale = _benevolence.delta_from_witness(
            result.verdict, [asdict(j) for j in result.judgments], evidence
        )
        deed = _benevolence.record_deed(
            actor=bot_id,
            description=action,
            delta=delta,
            basis=f"witness findings — {delta_rationale}",
            declared_intent=evidence.get("declared_intent"),
        )
        deed_basis = f"witness findings — {delta_rationale}"
        deed_hash = deed["entry_hash"]
    except OSError:
        pass
    try:
        tier, tier_note = _benevolence.latitude()
    except OSError:
        tier, tier_note = "unknown", "reservoir unreadable"

    record["reservoir"] = {
        "deed_hash": deed_hash,
        "deed_basis": deed_basis,
        "tier": tier,
        "tier_note": tier_note,
    }
    record["entry_hash"] = hashlib.sha256(
        record["prev_hash"].encode() + _canonical({k: v for k, v in record.items() if k != "entry_hash"})
    ).hexdigest()

    persisted = True
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, default=str) + "\n")
    except OSError as exc:
        persisted = False
        raise WitnessUnavailable(
            f"action log unwritable at {log_path}: {exc}"
        ) from exc

    witness_result = ActionWitnessResult(
        bot_id=bot_id,
        action=action,
        verdict=result.verdict,
        may_proceed=may_proceed,
        entry_hash=record["entry_hash"],
        persisted=persisted,
        note=result.note,
        judgments=[asdict(j) for j in result.judgments],
    )
    if enforce and not may_proceed:
        raise WitnessBlocked(
            f"BLOCKED by witness panel: {bot_id} / {action}. {result.note}"
        )
    return witness_result


def verify_action_log(log_path: Optional[Path] = None) -> Tuple[bool, str]:
    """Recompute the hash chain. Returns (ok, message)."""
    log_path = Path(log_path) if log_path else ACTION_LOG_PATH
    if not log_path.exists():
        return True, "no action log yet — nothing to verify"
    prev = "GENESIS"
    count = 0
    with open(log_path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if entry.get("prev_hash") != prev:
                return False, f"chain break at line {lineno}: prev_hash mismatch"
            recomputed = hashlib.sha256(
                prev.encode() + _canonical({k: v for k, v in entry.items() if k != "entry_hash"})
            ).hexdigest()
            if recomputed != entry.get("entry_hash"):
                return False, f"chain break at line {lineno}: entry_hash mismatch"
            prev = entry["entry_hash"]
            count += 1
    return True, f"chain intact: {count} witnessed action(s)"
