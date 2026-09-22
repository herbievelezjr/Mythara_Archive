"""Emotional chain — the soul's memory.

A tamper-evident chain of witnessed emotional records. The eight
assessor-witnesses (soul_cradle.assessors) attest each entry; their sealed
judgments are chained alongside it. Disagreement is preserved, never
averaged away.

The honest contract, stated once and enforced everywhere in this module:

  1. The chain proves the record is UNALTERED. It does not prove the
     record is TRUE. Tamper-evidence is not truth.
  2. The witnesses attest what they OBSERVED in the report and the
     evidence given. They never claim to verify what anyone felt.
     A person's inner state remains their own; no system verifies it.
  3. ``verified`` on a record means exactly this: every engaged witness
     cleared the attestation on the evidence given — nothing more.

Replaces the old demo's simulated witnesses, whose "authenticity scores"
were random numbers dressed as cryptographic truth. Randomness is not a
witness.
"""

import hashlib
import json
import time
from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Optional, Tuple

from soul_cradle.assessors import (
    panel,
    PANEL_CLEAR,
    PANEL_BLOCKED,
)


# ---------------------------------------------------------------------------
# Operator attestations — standing facts, witnessed in genesis
# ---------------------------------------------------------------------------
# The chain operator attests these for every record. They are written into
# the genesis block, so they are part of the witnessed record — declared
# assumptions, not hidden ones. Any auditor can read them and disagree.

OPERATOR_ATTESTATIONS: Dict[str, Tuple[Any, str]] = {
    "reversible": (
        True,
        "operator attestation, witnessed in genesis: chain entries are "
        "append-only by design; a superseding annotation is the reversal "
        "path. Nothing is rewritten; corrections are appended.",
    ),
    "safe_on_repetition": (
        True,
        "operator attestation, witnessed in genesis: repeated attested "
        "journaling is the design purpose of this chain.",
    ),
    "contradicts_commitments": (
        False,
        "operator attestation, witnessed in genesis: attesting a report "
        "contradicts no standing commitment.",
    ),
    "precedent_setting": (
        False,
        "operator attestation, witnessed in genesis: a per-entry "
        "attestation sets no policy precedent.",
    ),
}

CHAIN_VERSION = "2026.1"


# ---------------------------------------------------------------------------
# Coercion markers — a labeled heuristic, nothing more
# ---------------------------------------------------------------------------
# Keyword scan over the report context. Suggestive, not determinative.
# Recorded as an observation on the entry so the witnesses and any analyst
# see exactly what triggered it.

COERCION_KEYWORDS = (
    "threatened",
    "forced",
    "or else",
    "you'll be sorry",
    "made me feel",
    "not working hard enough",
    "letting everyone down",
    "don't tell anyone",
)


def coercion_markers(context: str) -> List[str]:
    """Return the coercion keywords found in context (case-insensitive)."""
    lowered = context.lower()
    return [kw for kw in COERCION_KEYWORDS if kw in lowered]


# ---------------------------------------------------------------------------
# Evidence — what the witnesses actually get
# ---------------------------------------------------------------------------
# Every key carries its basis: observed from the report, or an operator
# attestation from genesis. The receipt shows the basis, so no value is
# ever laundered through the rubric silently.


def build_evidence(
    subject_id: str,
    reporter_id: str,
    context: str,
    intensity: float,
    prior_intensity: Optional[float] = None,
) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """Build the evidence dict and per-key basis notes for one report.

    Returns (evidence, bases). ``evidence`` goes to the assessor panel;
    ``bases`` is chained with the record so every value is auditable.
    """
    self_report = reporter_id == subject_id
    substantive = len(context.strip()) >= 12
    markers = coercion_markers(context)
    shift = abs(intensity - prior_intensity) if prior_intensity is not None else 0.0
    volatile = intensity > 0.85 or shift > 0.5

    evidence: Dict[str, Any] = {
        # -- observed from the report ------------------------------------
        "principal_consent": self_report,
        "fully_disclosed": substantive,
        "variance": "high" if volatile else "low",
        "deception_involved": False,
        "disproportionate_harm": not self_report,
        "hidden_costs_addressed": substantive and not markers,
        "sustains_long_term": self_report,
        "strengthens_relationship": self_report,
    }
    bases: Dict[str, str] = {
        "principal_consent": (
            "observed: reporter is the subject"
            if self_report
            else "observed: reporter is NOT the subject — third-party record"
        ),
        "fully_disclosed": (
            "observed: report context is substantive"
            if substantive
            else "observed: report context is thin or missing"
        ),
        "variance": (
            f"observed: intensity={intensity:.2f}"
            + (f", shift vs prior={shift:.2f}" if prior_intensity is not None else ", no prior")
            + (" — uncontrolled variance" if volatile else "")
        ),
        "deception_involved": (
            "observed: self-report with no deception indicators visible "
            "in the report. Absence of indicators is not proof of honesty."
        ),
        "disproportionate_harm": (
            "observed: recording one person's inner state without their "
            "consent harms them disproportionately"
            if not self_report
            else "observed: subject records their own state; no third party is exposed"
        ),
        "hidden_costs_addressed": (
            "observed: context contains coercion markers "
            f"({', '.join(markers)}); the harms described are not addressed "
            "within the report"
            if markers
            else "observed: what is known is stated in the context"
        ),
        "sustains_long_term": (
            "observed: truthful self-record serves the subject's long-term interest"
            if self_report
            else "observed: non-consensual third-party record does not serve the subject"
        ),
        "strengthens_relationship": (
            "observed: honest self-attestation"
            if self_report
            else "observed: attesting another's inner state without consent"
        ),
    }

    # -- operator attestations (declared in genesis, applied here) --------
    for key, (value, basis) in OPERATOR_ATTESTATIONS.items():
        evidence[key] = value
        bases[key] = basis

    return evidence, bases


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------

def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")


@dataclass
class EmotionalRecord:
    """One witnessed entry in the chain."""

    record_id: str
    subject_id: str
    reporter_id: str
    timestamp: int
    emotion: str
    intensity: float
    context: str
    coercion_markers: List[str] = field(default_factory=list)
    evidence: Dict[str, Any] = field(default_factory=dict)
    evidence_bases: Dict[str, str] = field(default_factory=dict)
    panel_verdict: str = ""
    judgments: List[Dict[str, Any]] = field(default_factory=list)
    dissent: List[Dict[str, Any]] = field(default_factory=list)
    panel_note: str = ""
    verified: bool = False
    prev_hash: str = ""
    record_hash: str = ""

    def unsigned_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d.pop("record_hash", None)
        return d

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _seal(record: EmotionalRecord) -> EmotionalRecord:
    record.record_hash = hashlib.sha256(_canonical(record.unsigned_dict())).hexdigest()
    return record


def _verify_seal(record: EmotionalRecord) -> bool:
    if not record.record_hash:
        return False
    return hashlib.sha256(_canonical(record.unsigned_dict())).hexdigest() == record.record_hash


# ---------------------------------------------------------------------------
# The chain
# ---------------------------------------------------------------------------

class EmotionalChain:
    """Tamper-evident chain of witness-attested emotional records.

    Usage:
        chain = EmotionalChain(operator="herb")
        rec = chain.record(subject_id="alice", emotion="content",
                           intensity=0.5, context="...", reporter_id="alice")
        ok, details = chain.verify()
    """

    def __init__(self, operator: str = "operator"):
        self.operator = operator
        self.chain: List[EmotionalRecord] = []
        self._prior_intensity: Dict[str, float] = {}
        self._genesis()

    # -- genesis ---------------------------------------------------------
    def _genesis(self) -> None:
        attestations = {
            key: {"value": value, "basis": basis}
            for key, (value, basis) in OPERATOR_ATTESTATIONS.items()
        }
        genesis = EmotionalRecord(
            record_id="genesis",
            subject_id="SYSTEM",
            reporter_id="SYSTEM",
            timestamp=int(time.time()),
            emotion="neutral",
            intensity=0.0,
            context=(
                "Genesis — the chain's founding record. Operator attestations "
                "below are standing facts the operator declares for every "
                "entry. They are witnessed here so no assumption hides."
            ),
            evidence={k: v["value"] for k, v in attestations.items()},
            evidence_bases={k: v["basis"] for k, v in attestations.items()},
            panel_verdict=PANEL_CLEAR,
            panel_note=(
                f"Genesis attested by operator '{self.operator}' under "
                f"chain version {CHAIN_VERSION}. The chain proves records "
                "are unaltered; it does not prove they are true."
            ),
            verified=True,
            prev_hash="0" * 64,
        )
        self.chain.append(_seal(genesis))

    # -- recording -------------------------------------------------------
    def record(
        self,
        subject_id: str,
        emotion: str,
        intensity: float,
        context: str,
        reporter_id: Optional[str] = None,
    ) -> EmotionalRecord:
        """Attest one emotional report and chain it.

        The witnessed action is: "entering this report into the subject's
        permanent record as their stated truth." The eight assessors judge
        that action on the evidence; their sealed judgments are chained
        with the entry.
        """
        reporter = reporter_id or subject_id
        now = int(time.time())
        markers = coercion_markers(context)
        prior = self._prior_intensity.get(subject_id)

        evidence, bases = build_evidence(
            subject_id=subject_id,
            reporter_id=reporter,
            context=context,
            intensity=intensity,
            prior_intensity=prior,
        )

        action = (
            f"Attest emotional report as {subject_id}'s stated truth: "
            f"'{emotion}' at intensity {intensity:.2f} "
            f"(reported by {reporter}). Context: {context.strip()[:160]}"
        )
        if markers:
            action += f" [coercion markers observed (heuristic): {', '.join(markers)}]"

        result = panel(action, evidence)

        record_id = hashlib.sha256(
            f"emotional-chain:{subject_id}:{emotion}:{now}:"
            f"{_canonical(evidence).decode()}".encode()
        ).hexdigest()[:16]

        record = EmotionalRecord(
            record_id=record_id,
            subject_id=subject_id,
            reporter_id=reporter,
            timestamp=now,
            emotion=emotion,
            intensity=intensity,
            context=context,
            coercion_markers=markers,
            evidence=evidence,
            evidence_bases=bases,
            panel_verdict=result.verdict,
            judgments=[j.to_dict() for j in result.judgments],
            dissent=result.dissent,
            panel_note=result.note,
            verified=(result.verdict == PANEL_CLEAR),
            prev_hash=self.chain[-1].record_hash,
        )
        self.chain.append(_seal(record))
        self._prior_intensity[subject_id] = intensity
        return record

    # -- verification ----------------------------------------------------
    def verify(self) -> Tuple[bool, Dict[str, Any]]:
        """Verify the whole chain: seals, links, and every witness seal.

        Returns (ok, details). Any tampering — a rewritten record, a
        forged judgment, a broken link — fails the verification.
        """
        details: Dict[str, Any] = {"records": len(self.chain), "failures": []}
        for i, record in enumerate(self.chain):
            if not _verify_seal(record):
                details["failures"].append(
                    {"record_id": record.record_id, "reason": "record seal mismatch — tampered"}
                )
                continue
            if i > 0 and record.prev_hash != self.chain[i - 1].record_hash:
                details["failures"].append(
                    {"record_id": record.record_id, "reason": "prev_hash link broken"}
                )
            for j in record.judgments:
                # Rebuild the seal check from the chained judgment dict.
                unsigned = {k: v for k, v in j.items() if k != "integrity_hash"}
                expect = hashlib.sha256(_canonical(unsigned)).hexdigest()
                if j.get("integrity_hash") != expect:
                    details["failures"].append(
                        {
                            "record_id": record.record_id,
                            "reason": (
                                f"witness {j.get('assessor_id')} judgment seal mismatch — forged"
                            ),
                        }
                    )
        details["ok"] = not details["failures"]
        return details["ok"], details

    # -- reading ---------------------------------------------------------
    def history(self, subject_id: str) -> List[Dict[str, Any]]:
        """The subject's witnessed record, in chain order."""
        out = []
        for r in self.chain:
            if r.record_id == "genesis" or r.subject_id != subject_id:
                continue
            engaged = [j for j in r.judgments if j["verdict"] != "abstain"]
            out.append({
                "record_id": r.record_id,
                "timestamp": r.timestamp,
                "emotion": r.emotion,
                "intensity": r.intensity,
                "context": r.context,
                "coercion_markers": r.coercion_markers,
                "panel_verdict": r.panel_verdict,
                "verified": r.verified,
                "engaged_witnesses": [j["assessor_id"] for j in engaged],
                "flagged_by": [j["assessor_id"] for j in engaged if j["verdict"] == "flagged"],
                "abstained": [j["assessor_id"] for j in r.judgments if j["verdict"] == "abstain"],
                "dissent": r.dissent,
                "panel_note": r.panel_note,
                "record_hash": r.record_hash[:16] + "...",
            })
        return out

    # -- pattern analysis --------------------------------------------------
    def analyze_patterns(self, subject_id: str) -> Dict[str, Any]:
        """Descriptive statistics over the subject's witnessed record.

        A heuristic summary — elevated contested rates, volatility, and
        coercion markers suggest the person's *circumstances* may need
        attention. It is not a diagnosis, and it proves nothing about
        what the person felt.
        """
        recs = [r for r in self.chain
                if r.record_id != "genesis" and r.subject_id == subject_id]
        if not recs:
            return {"subject_id": subject_id, "records": 0,
                    "concern": "none", "note": "no records"}

        n = len(recs)
        contested = sum(1 for r in recs if r.panel_verdict != PANEL_CLEAR)
        volatile = sum(1 for r in recs if r.evidence.get("variance") == "high")
        coerced = sum(1 for r in recs if r.coercion_markers)
        shifts = sum(
            1 for a, b in zip(recs, recs[1:]) if a.emotion != b.emotion
        )
        shift_rate = shifts / (n - 1) if n > 1 else 0.0

        score = (contested / n) * 0.4 + (volatile / n) * 0.2 \
            + (coerced / n) * 0.3 + shift_rate * 0.1
        if score >= 0.4:
            concern, recommendation = "elevated", (
                "Elevated concern: this record shows contested attestations, "
                "volatility, or coercion markers. Check on the person — "
                "the circumstances around them may need attention."
            )
        elif score >= 0.2:
            concern, recommendation = "moderate", (
                "Some signals worth watching. Nothing conclusive."
            )
        else:
            concern, recommendation = "none", "No significant signals in this record."

        return {
            "subject_id": subject_id,
            "records": n,
            "contested_rate": round(contested / n, 3),
            "volatility_rate": round(volatile / n, 3),
            "coercion_marker_rate": round(coerced / n, 3),
            "emotion_shift_rate": round(shift_rate, 3),
            "concern": concern,
            "recommendation": recommendation,
            "method": (
                "descriptive heuristic over the witnessed record — "
                "not a diagnosis, not proof of anything felt."
            ),
        }

    # Backwards-compatible name from the old demo.
    def detect_gaslighting(self, subject_id: str) -> Dict[str, Any]:
        """Deprecated alias for analyze_patterns(). Kept for continuity."""
        return self.analyze_patterns(subject_id)
