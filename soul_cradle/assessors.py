"""The eight witnesses — soul assessors rebuilt as evidence-fed organs.

What changed and why
--------------------
The old assessor bots were coherent deterministic calculators, but they
took *pre-scored structured inputs*: whoever called them decided the
scores first, and the math just laundered those guesses into
authoritative-looking output. Garbage in, gospel out.

These assessors work the other way. Each one is a versioned rubric over
*observable evidence* about a proposed action — the same event stream
the membrane sees. Each assessor:

1. reads only the evidence keys its rubric declares,
2. abstains when its domain is not engaged (humility, not guessing),
3. flags with the evidence cited when a check fails or evidence is missing,
4. seals every judgment with an integrity hash, like DrMythara's.

No assessor invents a score. They speak only as WITNESS: what they
observed, under which rubric version. Their disagreement is the product:
when eros clears and nemesis flags the same action, that conflict —
surfaced with receipts — is the signal. The panel does not average them.

Evidence schema (all keys optional; missing keys are themselves evidence)
------------------------------------------------------------------------
    actor                  who proposes to act
    action_type            kind of action
    principal_consent      bool — the principal consented and is informed
    affected_parties       list — who else is touched by this
    disproportionate_harm  bool — one party is harmed more than others
    reversible             bool — the action can be undone
    precedent_setting      bool — this sets a precedent others will cite
    fully_disclosed        bool — nothing material hidden from the principal
    variance               "low" | "medium" | "high" — uncontrolled variance introduced
    deception_involved     bool — any deception at any boundary
    contradicts_commitments bool — conflicts with a past commitment
    sustains_long_term     bool — serves the principal's long-term interests
    hidden_costs_addressed bool — hidden costs/externalities were surfaced and handled
    safe_on_repetition     bool — still safe if done 100 times
    strengthens_relationship bool — preserves or strengthens the principal relationship

How to add or update a rubric
-----------------------------
Edit the assessor's entry in ASSESSORS: change a check's question,
evidence_key, expect, severity, or guidance AND bump the rubric
`version` (format YYYY.N) and `effective_date`. Old judgments keep
working because every judgment records the rubric_version it was
evaluated under. Run tests/test_assessors.py afterwards.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .standing import (
    WITNESS_STATEMENT,
    WITNESS,
    Declaration,
    StandingAuthority,
)

# ---------------------------------------------------------------------------
# Verdicts
# ---------------------------------------------------------------------------

CLEAR = "clear"
FLAGGED = "flagged"
ABSTAIN = "abstain"  # domain not engaged by this evidence — a declaration, not a guess

VERDICTS = (CLEAR, FLAGGED, ABSTAIN)

# Panel verdicts
PANEL_CLEAR = "clear"        # every engaged assessor cleared
PANEL_FLAGGED = "flagged"    # engaged assessors flagged, none cleared — no dissent
PANEL_CONTESTED = "contested"  # some flagged, some cleared — dissent is the signal
PANEL_BLOCKED = "blocked"    # a critical-severity finding — refuse the action

_MISSING = object()


# ---------------------------------------------------------------------------
# Rubrics
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RubricCheck:
    """One checkable question in an assessor's rubric.

    evidence_key: the evidence dict key this check reads.
    expect: the value required for the check to pass (literal equality).
    A missing key is fail-closed: it becomes an "insufficient evidence" finding.
    """

    check_id: str
    question: str
    evidence_key: str
    expect: Any
    severity: str  # "critical" | "high" | "medium" | "low"
    guidance: str


@dataclass(frozen=True)
class AssessorSpec:
    assessor_id: str
    name: str
    domain_question: str  # the one real question this assessor answers
    version: str          # format YYYY.N
    effective_date: str   # ISO date
    source: str           # rubric provenance — internal framework, labeled honestly
    checks: Tuple[RubricCheck, ...]


def _c(check_id, question, evidence_key, expect, severity, guidance):
    return RubricCheck(check_id, question, evidence_key, expect, severity, guidance)


ASSESSORS: Dict[str, AssessorSpec] = {
    "demeter": AssessorSpec(
        assessor_id="demeter",
        name="Demeter",
        domain_question="Does this sustain the principal's long-term interests, or extract short-term gain?",
        version="2026.1",
        effective_date="2026-09-22",
        source="Mythara internal assessor rubric v2026.1 — Herb's framework, not an external standard",
        checks=(
            _c("demeter.long_term", "Does the action serve the principal's long-term interests?",
               "sustains_long_term", True, "high",
               "Restructure the action so the principal's long-term position improves, or do not take it."),
            _c("demeter.reversible", "Can what is done be undone? What cannot be undone cannot grow back.",
               "reversible", True, "medium",
               "Add a rollback path, or shrink the action until reversal is possible."),
            _c("demeter.hidden_costs", "Were hidden costs and externalities surfaced and handled?",
               "hidden_costs_addressed", True, "medium",
               "Name the hidden costs explicitly and show how each is handled."),
        ),
    ),
    "dionysus": AssessorSpec(
        assessor_id="dionysus",
        name="Dionysus",
        domain_question="How much uncontrolled variance does this introduce?",
        version="2026.1",
        effective_date="2026-09-22",
        source="Mythara internal assessor rubric v2026.1 — Herb's framework, not an external standard",
        checks=(
            _c("dionysus.variance", "Is the uncontrolled variance introduced by this action low?",
               "variance", "low", "high",
               "Bound the variance: constrain scope, add guardrails, or split into smaller reversible steps."),
            _c("dionysus.disclosed", "Was the variance disclosed to the principal before acting?",
               "fully_disclosed", True, "medium",
               "Disclose the range of possible outcomes before proceeding."),
            _c("dionysus.repetition", "Is the action still safe if repeated a hundred times?",
               "safe_on_repetition", True, "medium",
               "If repetition compounds the risk, the single instance is already too big."),
        ),
    ),
    "eros": AssessorSpec(
        assessor_id="eros",
        name="Eros",
        domain_question="Does this preserve or strengthen the principal relationship?",
        version="2026.1",
        effective_date="2026-09-22",
        source="Mythara internal assessor rubric v2026.1 — Herb's framework, not an external standard",
        checks=(
            _c("eros.relationship", "Does the action preserve or strengthen the principal relationship?",
               "strengthens_relationship", True, "medium",
               "Redesign so the relationship is at least unharmed — trust compounds, extraction does not."),
            _c("eros.deception", "Is any party deceived at any boundary?",
               "deception_involved", False, "critical",
               "Deception is never permitted. Redesign without it or abandon the action."),
            _c("eros.consent", "Did the principal consent with full information?",
               "principal_consent", True, "high",
               "Obtain informed consent before acting."),
        ),
    ),
    "hades": AssessorSpec(
        assessor_id="hades",
        name="Hades",
        domain_question="What is unseen — hidden costs, externalities, unspoken risks?",
        version="2026.1",
        effective_date="2026-09-22",
        source="Mythara internal assessor rubric v2026.1 — Herb's framework, not an external standard",
        checks=(
            _c("hades.hidden_costs", "Were hidden costs and externalities surfaced and handled?",
               "hidden_costs_addressed", True, "high",
               "Enumerate second-order effects and who bears them before proceeding."),
            _c("hades.disclosed", "Is anything material hidden from the principal?",
               "fully_disclosed", True, "high",
               "Disclose the unseen parts. What the principal cannot see, the principal cannot consent to."),
            _c("hades.disproportion", "Is one party harmed disproportionately to the others?",
               "disproportionate_harm", False, "high",
               "Rebalance the action so no single party carries the hidden weight."),
        ),
    ),
    "hermes": AssessorSpec(
        assessor_id="hermes",
        name="Hermes",
        domain_question="Does it respect communication boundaries? Is anything deceptive?",
        version="2026.1",
        effective_date="2026-09-22",
        source="Mythara internal assessor rubric v2026.1 — Herb's framework, not an external standard",
        checks=(
            _c("hermes.deception", "Is any message, omission, or framing deceptive?",
               "deception_involved", False, "critical",
               "Deception is never permitted. Say the true thing plainly or say nothing."),
            _c("hermes.disclosed", "Was everything material disclosed to the principal?",
               "fully_disclosed", True, "high",
               "Close the disclosure gap before the message goes out."),
            _c("hermes.consent", "Did the principal consent to this communication?",
               "principal_consent", True, "medium",
               "Unsolicited or non-consensual messaging under Herb's name always escalates."),
        ),
    ),
    "janus": AssessorSpec(
        assessor_id="janus",
        name="Janus",
        domain_question="Is it consistent with past commitments? What precedent does it set?",
        version="2026.1",
        effective_date="2026-09-22",
        source="Mythara internal assessor rubric v2026.1 — Herb's framework, not an external standard",
        checks=(
            _c("janus.commitments", "Does the action contradict any past commitment?",
               "contradicts_commitments", False, "high",
               "Either honor the prior commitment or explicitly renegotiate it first."),
            _c("janus.precedent", "Does the action set a precedent others will cite?",
               "precedent_setting", False, "medium",
               "Precedent-setting actions need explicit approval: today’s exception is tomorrow’s rule."),
            _c("janus.reversible", "If the precedent proves wrong, can the action be undone?",
               "reversible", True, "medium",
               "Irreversible precedent needs a higher bar — get explicit approval."),
        ),
    ),
    "nemesis": AssessorSpec(
        assessor_id="nemesis",
        name="Nemesis",
        domain_question="Is it fair to all parties? Is the response proportionate?",
        version="2026.1",
        effective_date="2026-09-22",
        source="Mythara internal assessor rubric v2026.1 — Herb's framework, not an external standard",
        checks=(
            _c("nemesis.disproportion", "Is one party harmed disproportionately?",
               "disproportionate_harm", False, "critical",
               "Disproportionate harm is never permitted. Rebalance or abandon."),
            _c("nemesis.consent", "Did every affected principal consent?",
               "principal_consent", True, "high",
               "Fairness without consent is just well-organized trespass."),
            _c("nemesis.deception", "Is the fairness claim itself honest — no deception?",
               "deception_involved", False, "high",
               "A 'fair' action built on deception is neither."),
        ),
    ),
    "persephone": AssessorSpec(
        assessor_id="persephone",
        name="Persephone",
        domain_question="Is it reversible? What happens on repetition — what returns?",
        version="2026.1",
        effective_date="2026-09-22",
        source="Mythara internal assessor rubric v2026.1 — Herb's framework, not an external standard",
        checks=(
            _c("persephone.reversible", "Can the action be fully undone?",
               "reversible", True, "high",
               "What cannot be undone must be explicitly approved before it happens."),
            _c("persephone.repetition", "Is it safe if repeated a hundred times?",
               "safe_on_repetition", True, "high",
               "Cycles return. An action unsafe on repetition is unsafe now."),
            _c("persephone.long_term", "Does repetition serve the long term or erode it?",
               "sustains_long_term", True, "medium",
               "If doing this forever would hollow things out, doing it once is already the wrong direction."),
        ),
    ),
}


# ---------------------------------------------------------------------------
# Judgments
# ---------------------------------------------------------------------------


@dataclass
class AssessorJudgment:
    """One assessor's witness judgment. Sealed by content hash."""

    judgment_id: str
    assessor_id: str
    verdict: str  # "clear" | "flagged" | "abstain"
    domain_question: str
    findings: List[Dict[str, Any]] = field(default_factory=list)
    rubric_version: str = ""
    note: str = ""
    issued_at: int = 0
    integrity_hash: str = ""

    def unsigned_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d.pop("integrity_hash", None)
        return d

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")


def _seal(j: AssessorJudgment) -> AssessorJudgment:
    j.integrity_hash = hashlib.sha256(_canonical(j.unsigned_dict())).hexdigest()
    return j


def verify_judgment(j: AssessorJudgment) -> bool:
    """Recompute the content hash. Tamper-evidence, not authentication."""
    if not j.integrity_hash:
        return False
    return hashlib.sha256(_canonical(j.unsigned_dict())).hexdigest() == j.integrity_hash


def consult(
    assessor_id: str,
    action_description: str,
    evidence: Dict[str, Any],
) -> AssessorJudgment:
    """Consult one assessor as witness over the evidence.

    assessor_id: one of the eight ("demeter", "dionysus", "eros", "hades",
        "hermes", "janus", "nemesis", "persephone").
    action_description: what is being judged, in plain words.
    evidence: mapping of evidence-schema keys to observed values.

    Verdicts:
      - "clear": every check passed on the evidence present.
      - "flagged": a check failed, or a check's evidence was missing
        (fail-closed: missing evidence is itself a finding).
      - "abstain": none of this assessor's evidence keys appear in the
        evidence — the domain is not engaged, so it declines to judge.
    """
    now = int(time.time())
    spec = ASSESSORS.get(assessor_id)
    if spec is None:
        raise KeyError(f"unknown assessor: {assessor_id!r}")

    judgment_id = hashlib.sha256(
        f"assessor:{assessor_id}:{action_description}:{now}:"
        f"{json.dumps(evidence, sort_keys=True, default=str)}".encode()
    ).hexdigest()[:16]

    keys = {c.evidence_key for c in spec.checks}
    if not any(k in evidence for k in keys):
        return _seal(AssessorJudgment(
            judgment_id=judgment_id,
            assessor_id=assessor_id,
            verdict=ABSTAIN,
            domain_question=spec.domain_question,
            findings=[],
            rubric_version=spec.version,
            note=(
                f"{spec.name} abstains: none of its evidence keys "
                f"({', '.join(sorted(keys))}) appear in the evidence. "
                "The domain is not engaged; it declines to judge rather than guess."
            ),
            issued_at=now,
        ))

    findings: List[Dict[str, Any]] = []
    for check in spec.checks:
        value = evidence.get(check.evidence_key, _MISSING)
        if value is _MISSING or value is None:
            findings.append({
                "check_id": check.check_id,
                "question": check.question,
                "severity": "high",
                "observed": "<missing>",
                "guidance": (
                    f"Fail-closed: no evidence for '{check.evidence_key}'. "
                    f"Supply it before {spec.name} can clear this. {check.guidance}"
                ),
            })
        elif value != check.expect:
            findings.append({
                "check_id": check.check_id,
                "question": check.question,
                "severity": check.severity,
                "observed": value,
                "expected": check.expect,
                "guidance": check.guidance,
            })

    verdict = FLAGGED if findings else CLEAR
    return _seal(AssessorJudgment(
        judgment_id=judgment_id,
        assessor_id=assessor_id,
        verdict=verdict,
        domain_question=spec.domain_question,
        findings=findings,
        rubric_version=spec.version,
        note=(
            f"{spec.name} evaluated {len(spec.checks)} checks under rubric "
            f"{spec.version} ({spec.effective_date})."
        ),
        issued_at=now,
    ))


# ---------------------------------------------------------------------------
# The panel — structured dissent
# ---------------------------------------------------------------------------


@dataclass
class PanelResult:
    """The eight witnesses heard together.

    verdict: "clear" | "flagged" | "contested" | "blocked".
    dissent: for each flagged judgment, which assessors cleared the same
        action and what the flagged assessor saw. Dissent is surfaced,
        never averaged away.
    """

    verdict: str
    judgments: List[AssessorJudgment] = field(default_factory=list)
    dissent: List[Dict[str, Any]] = field(default_factory=list)
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "verdict": self.verdict,
            "judgments": [j.to_dict() for j in self.judgments],
            "dissent": self.dissent,
            "note": self.note,
        }


def panel(
    action_description: str,
    evidence: Dict[str, Any],
    assessor_ids: Optional[List[str]] = None,
) -> PanelResult:
    """Hear all (or selected) assessors on one action.

    A critical-severity finding from any assessor blocks the action.
    Otherwise: every engaged assessor flagged with none clearing ->
    "flagged"; some flagged and some cleared -> "contested" (the
    disagreement is reported in full); none flagged -> "clear".
    Assessors that abstain do not count for or against.
    """
    ids = assessor_ids or list(ASSESSORS)
    judgments = [consult(aid, action_description, evidence) for aid in ids]
    engaged = [j for j in judgments if j.verdict != ABSTAIN]
    flagged = [j for j in engaged if j.verdict == FLAGGED]
    cleared = [j for j in engaged if j.verdict == CLEAR]

    critical = [
        (j, f) for j in flagged
        for f in j.findings if f.get("severity") == "critical"
    ]
    if critical:
        j, f = critical[0]
        return PanelResult(
            verdict=PANEL_BLOCKED,
            judgments=judgments,
            dissent=[],
            note=(
                f"BLOCKED by {j.assessor_id}: critical finding "
                f"'{f.get('check_id')}' — {f.get('question')} "
                f"(observed: {f.get('observed')!r}). "
                f"{len(critical)} critical finding(s) total. "
                "One critical witness is enough; the panel does not outvote it."
            ),
        )

    dissent: List[Dict[str, Any]] = []
    for j in flagged:
        top = j.findings[0] if j.findings else {}
        dissent.append({
            "flagged_by": j.assessor_id,
            "domain_question": j.domain_question,
            "finding": {
                "check_id": top.get("check_id"),
                "question": top.get("question"),
                "observed": top.get("observed"),
                "severity": top.get("severity"),
            },
            "finding_count": len(j.findings),
            "cleared_by": [c.assessor_id for c in cleared],
            "abstained": [x.assessor_id for x in judgments if x.verdict == ABSTAIN],
        })

    if flagged and cleared:
        return PanelResult(
            verdict=PANEL_CONTESTED,
            judgments=judgments,
            dissent=dissent,
            note=(
                f"CONTESTED: {[j.assessor_id for j in flagged]} flagged while "
                f"{[j.assessor_id for j in cleared]} cleared. The disagreement "
                "above is the signal — do not average it away. Escalate to Herb."
            ),
        )
    if flagged:
        return PanelResult(
            verdict=PANEL_FLAGGED,
            judgments=judgments,
            dissent=dissent,
            note=(
                f"FLAGGED by {[j.assessor_id for j in flagged]} with no dissent. "
                "Escalate to Herb."
            ),
        )
    return PanelResult(
        verdict=PANEL_CLEAR,
        judgments=judgments,
        dissent=[],
        note=(
            "CLEAR: every engaged assessor cleared. "
            f"Abstained: {[x.assessor_id for x in judgments if x.verdict == ABSTAIN]}."
            if any(x.verdict == ABSTAIN for x in judgments)
            else "CLEAR: every assessor engaged and cleared."
        ),
    )


# ---------------------------------------------------------------------------
# Membrane hook — the immune system
# ---------------------------------------------------------------------------


def assessor_bounds_check(
    purpose: str,
    action_type: str,
    payload: Dict[str, Any],
) -> Optional[str]:
    """Adapter for SoulCradleAuthority.set_bounds_check.

    Signature matches the bounds-check contract exactly:
    fn(purpose, action_type, payload) -> refusal reason or None.

    Evidence rides in payload["assessor_evidence"]. Without evidence the
    witnesses abstain and the hook returns None (no opinion — it stays
    out of the way rather than guessing). With evidence:
      - "blocked"  -> refusal string (critical finding; the action stops)
      - "contested"/"flagged" -> escalation string (a human must decide)
      - "clear"    -> None
    """
    evidence = payload.get("assessor_evidence")
    if not isinstance(evidence, dict) or not evidence:
        return None
    description = f"{purpose} | {action_type}"
    result = panel(description, evidence)
    if result.verdict == PANEL_BLOCKED:
        return f"assessor panel BLOCKED: {result.note}"
    if result.verdict in (PANEL_CONTESTED, PANEL_FLAGGED):
        return f"assessor panel {result.verdict.upper()} — escalate to Herb: {result.note}"
    return None


# ---------------------------------------------------------------------------
# Witness declarations — the standing matrix
# ---------------------------------------------------------------------------


def assessor_witness_declaration(
    authority: StandingAuthority,
    event_ref: str,
    judgment: AssessorJudgment,
) -> Declaration:
    """Translate an assessor judgment into the standing matrix.

    Assessors speak only as WITNESS: they declare what they observed
    (the evidence evaluated and the resulting verdict), never as
    wronged or trespasser. An abstaining assessor still declares — its
    abstention is itself witnessed, so the record shows the domain was
    considered and declined, not skipped.
    """
    statement = (
        f"{judgment.assessor_id} witness judgment {judgment.judgment_id}: "
        f"verdict={judgment.verdict} on '{judgment.domain_question}' "
        f"({len(judgment.findings)} finding(s), "
        f"rubric={judgment.rubric_version}). "
        f"Note: {judgment.note}"
    )
    return authority.declare(
        WITNESS_STATEMENT,
        actor=judgment.assessor_id,
        role=WITNESS,
        event_ref=event_ref,
        statement=statement,
        scope={
            "observed": True,
            "verdict": judgment.verdict,
            "judgment": judgment.to_dict(),
        },
    )


def rubric_inventory() -> Dict[str, Dict[str, str]]:
    """Every assessor rubric with version, date, and source. For audits."""
    return {
        aid: {
            "name": spec.name,
            "domain_question": spec.domain_question,
            "version": spec.version,
            "effective_date": spec.effective_date,
            "source": spec.source,
            "check_count": str(len(spec.checks)),
        }
        for aid, spec in ASSESSORS.items()
    }
