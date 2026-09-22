"""DrMythara — health-reasoning organ of the Mythara body.

She is the reasoning behind Mythara when it comes to health: HIPAA
compliance, FDA 21 CFR Part 11 electronic records/signatures, and
medical-AI governance. This module is the canonical core. The
user-facing demo bot (Commercial/mythara_drmythara_bot.py) is a thin
wrapper around it; the core is the authority.

NOT A MEDICAL PROFESSIONAL. DOES NOT PROVIDE MEDICAL ADVICE.
COMPLIANCE GUIDANCE ONLY. Every judgment says what rule was checked,
what version of the rule was used, and what evidence was evaluated —
never a bare score.

Deterministic: the same topic + evidence always yields the same
judgment. She does not perceive, she does not generate, she does not
guess. Garbage evidence in, flagged judgment out.

Humility mechanism: consult_health() returns verdict "outside_scope"
when the topic matches no rule domain — she declares the limit instead
of scoring anyway. A health-touching action with no evidence is
fail-closed: flagged as "insufficient evidence", never silently cleared.

HOW TO ADD OR UPDATE A RULE (Herb's update path):
  1. Find the RuleTable for the domain in RULE_TABLES below.
  2. To change a rule: edit its requirement/guidance/severity AND bump
     the table's `version` (format YYYY.N, e.g. "2025.2") and set
     `effective_date` to today. Old judgments keep working because every
     HealthJudgment records the rule_versions it was evaluated under.
  3. To add a rule: append a Rule(...) with a unique rule_id,
     the evidence key it checks (`check`), severity, and guidance —
     then bump version/effective_date as above.
  4. To add a whole domain: create a new RuleTable with version,
     effective_date, and a `source` citation, add it to RULE_TABLES,
     and add its keywords to DOMAIN_KEYWORDS.
  5. Run tests/test_health.py. Every judgment must cite rule versions;
     a table without version/effective_date/source fails the suite.

Rule sources are cited per table. The ai_governance table is Herb's own
internal checklist — it is labeled as such, not as a regulation.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

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
OUTSIDE_SCOPE = "outside_scope"

VERDICTS = (CLEAR, FLAGGED, OUTSIDE_SCOPE)

# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Rule:
    """One checkable compliance requirement.

    check: the evidence key this rule evaluates. consult_health() looks up
    evidence[check]; truthy means the control is present/satisfied.
    """

    rule_id: str
    domain: str  # "hipaa" | "fda_cfr11" | "ai_governance"
    category: str  # grouping within the domain, e.g. "access_control"
    requirement: str  # human-readable requirement
    check: str  # evidence key
    severity: str  # "critical" | "high" | "medium" | "low"
    guidance: str  # remediation guidance


@dataclass(frozen=True)
class RuleTable:
    """A versioned set of rules with a cited source."""

    name: str
    version: str  # format YYYY.N
    effective_date: str  # ISO date
    source: str  # citation — regulation or honest "internal framework" label
    rules: List[Rule]


def _r(rule_id, domain, category, requirement, check, severity, guidance):
    return Rule(rule_id, domain, category, requirement, check, severity, guidance)


RULE_TABLES: Dict[str, RuleTable] = {
    "hipaa_technical": RuleTable(
        name="hipaa_technical",
        version="2025.1",
        effective_date="2025-01-01",
        source="45 CFR Part 164, Subpart C — HIPAA Security Rule, Technical Safeguards (164.312)",
        rules=[
            _r("hipaa.tech.access.unique_user_id", "hipaa", "access_control",
               "Unique user identification for every workforce member accessing ePHI",
               "unique_user_id", "high",
               "Assign a unique name/number for identifying and tracking user identity."),
            _r("hipaa.tech.access.emergency_access", "hipaa", "access_control",
               "Emergency access procedure for obtaining necessary ePHI during an emergency",
               "emergency_access", "medium",
               "Document and implement an emergency access procedure."),
            _r("hipaa.tech.access.auto_logoff", "hipaa", "access_control",
               "Automatic logoff terminating electronic sessions after inactivity",
               "auto_logoff", "high",
               "Implement automatic logoff (e.g. 15 minutes) on all systems handling ePHI."),
            _r("hipaa.tech.access.encryption", "hipaa", "access_control",
               "Encryption and decryption mechanism for ePHI",
               "encryption", "critical",
               "Implement a mechanism to encrypt and decrypt ePHI at rest."),
            _r("hipaa.tech.audit.audit_logging", "hipaa", "audit_controls",
               "Audit controls: hardware, software, and procedural mechanisms recording access to ePHI",
               "audit_logging", "high",
               "Enable audit logging on all systems that create, receive, or transmit ePHI."),
            _r("hipaa.tech.audit.log_review", "hipaa", "audit_controls",
               "Regular review of audit logs and access reports",
               "log_review", "medium",
               "Establish a cadence for reviewing audit logs and document each review."),
            _r("hipaa.tech.audit.integrity_verification", "hipaa", "audit_controls",
               "Mechanism to verify integrity of audit records",
               "integrity_verification", "medium",
               "Protect audit logs from tampering; verify integrity on review."),
            _r("hipaa.tech.integrity.data_integrity", "hipaa", "integrity",
               "Mechanism protecting ePHI from improper alteration or destruction",
               "data_integrity", "critical",
               "Deploy integrity controls (checksums, hashes) over ePHI stores."),
            _r("hipaa.tech.integrity.authentication", "hipaa", "integrity",
               "Person or entity authentication before ePHI access",
               "authentication", "high",
               "Require authentication (unique credentials at minimum) before ePHI access."),
            _r("hipaa.tech.transmission.encryption_in_transit", "hipaa", "transmission_security",
               "Encryption of ePHI whenever transmitted over a network",
               "encryption_in_transit", "critical",
               "Encrypt ePHI in transit; never transmit ePHI over unencrypted channels."),
            _r("hipaa.tech.transmission.tls_1_2", "hipaa", "transmission_security",
               "Transmission security via TLS 1.2 or higher",
               "tls_1_2_minimum", "high",
               "Disable TLS below 1.2 on all endpoints handling ePHI."),
        ],
    ),
    "hipaa_administrative": RuleTable(
        name="hipaa_administrative",
        version="2025.1",
        effective_date="2025-01-01",
        source="45 CFR Part 164, Subpart C — HIPAA Security Rule, Administrative Safeguards (164.308)",
        rules=[
            _r("hipaa.admin.risk_analysis", "hipaa", "security_management",
               "Security risk analysis of ePHI confidentiality, integrity, availability",
               "risk_analysis", "critical",
               "Conduct and document a full risk analysis; repeat on material change."),
            _r("hipaa.admin.risk_management", "hipaa", "security_management",
               "Risk management: measures sufficient to reduce risks to reasonable level",
               "risk_management", "high",
               "Implement and track remediation for every risk the analysis found."),
            _r("hipaa.admin.sanctions", "hipaa", "security_management",
               "Sanction policy for workforce members who violate security policies",
               "sanctions", "medium",
               "Adopt and communicate a sanction policy for security violations."),
            _r("hipaa.admin.periodic_review", "hipaa", "security_management",
               "Periodic review of security measures and records",
               "periodic_review", "medium",
               "Schedule and document periodic reviews of all security measures."),
            _r("hipaa.admin.workforce_authorization", "hipaa", "workforce_security",
               "Workforce authorization procedures for ePHI access",
               "workforce_authorization", "medium",
               "Define who may access ePHI and document each authorization."),
            _r("hipaa.admin.training", "hipaa", "training",
               "Security awareness and training program for all workforce members",
               "security_awareness_training", "medium",
               "Train every workforce member; keep training logs (malware, login monitoring, password management)."),
            _r("hipaa.admin.access_authorization", "hipaa", "information_access",
               "Information access management: documented access authorization and modification",
               "access_authorization", "high",
               "Document access authorization, establishment, and modification procedures."),
        ],
    ),
    "hipaa_physical": RuleTable(
        name="hipaa_physical",
        version="2025.1",
        effective_date="2025-01-01",
        source="45 CFR Part 164, Subpart C — HIPAA Security Rule, Physical Safeguards (164.310)",
        rules=[
            _r("hipaa.phys.facility_security", "hipaa", "facility_access",
               "Facility access controls: security plan and access procedures",
               "facility_security", "medium",
               "Implement a facility security plan controlling physical access to ePHI systems."),
            _r("hipaa.phys.workstation_security", "hipaa", "workstation_use",
               "Workstation security: physical safeguards restricting access to authorized users",
               "workstation_security", "medium",
               "Position and lock down workstations so only authorized users can access ePHI."),
            _r("hipaa.phys.device_encryption", "hipaa", "device_media",
               "Encryption of devices and media containing ePHI",
               "device_encryption", "high",
               "Encrypt laptops, drives, and removable media that may hold ePHI."),
            _r("hipaa.phys.disposal", "hipaa", "device_media",
               "Secure disposal of ePHI and the media it resides on",
               "secure_disposal", "high",
               "Dispose of ePHI/media so it cannot be reconstructed; document disposal."),
            _r("hipaa.phys.data_backup", "hipaa", "device_media",
               "Data backup plan for retrievable exact copies of ePHI",
               "data_backup", "high",
               "Maintain and test a data backup plan for all ePHI."),
        ],
    ),
    "fda_records": RuleTable(
        name="fda_records",
        version="2025.1",
        effective_date="2025-01-01",
        source="21 CFR Part 11, Subpart B — FDA Electronic Records (11.10)",
        rules=[
            _r("fda.rec.validation", "fda_cfr11", "electronic_records",
               "System validation: accurate, reliable, consistent, able to discern invalid/altered records",
               "system_validation", "critical",
               "Validate the system for its intended use before production; revalidate on change."),
            _r("fda.rec.audit_trail", "fda_cfr11", "electronic_records",
               "Secure, computer-generated, time-stamped audit trail recording operator entries/actions",
               "audit_trail", "critical",
               "Enable independent, secure, timestamped audit trails; never allow silent edits."),
            _r("fda.rec.record_copies", "fda_cfr11", "electronic_records",
               "Accurate and complete copies of records, readily retrievable for FDA inspection",
               "record_copies", "high",
               "Ensure records are retrievable in accurate, complete form for inspection."),
        ],
    ),
    "fda_signatures": RuleTable(
        name="fda_signatures",
        version="2025.1",
        effective_date="2025-01-01",
        source="21 CFR Part 11, Subpart C — FDA Electronic Signatures (11.50–11.70)",
        rules=[
            _r("fda.sig.unique", "fda_cfr11", "electronic_signatures",
               "Electronic signatures unique to one individual; never reused or reassigned",
               "signature_unique", "critical",
               "Guarantee one-to-one signature identity; prohibit reuse and reassignment."),
            _r("fda.sig.two_factor", "fda_cfr11", "electronic_signatures",
               "Two distinct identification components for non-biometric signatures",
               "two_factor_signatures", "high",
               "Require two distinct identification components at signing."),
            _r("fda.sig.manifestation", "fda_cfr11", "signature_manifestations",
               "Signed records display printed name, date/time, and meaning of signature",
               "signature_manifestation", "medium",
               "Render name, timestamp, and signing meaning on every signed record."),
            _r("fda.sig.linkage", "fda_cfr11", "signature_manifestations",
               "Signatures linked to records so they cannot be excised, copied, or transferred",
               "signature_linkage", "high",
               "Bind each signature to its record cryptographically or procedurally."),
        ],
    ),
    "ai_governance": RuleTable(
        name="ai_governance",
        version="2025.1",
        effective_date="2025-01-01",
        source="Mythara internal medical-AI governance framework v1.0 (2025) — "
                "Herb's own checklist, NOT a regulation and NOT a certification standard",
        rules=[
            _r("ai.gov.clinical_validation", "ai_governance", "validation",
               "Clinical validation complete for the system's intended use",
               "clinical_validation", "high",
               "Validate against clinical ground truth before any clinical use."),
            _r("ai.gov.bias_testing", "ai_governance", "validation",
               "Bias testing across demographic subgroups documented",
               "bias_testing", "high",
               "Test performance across age, sex, and race/ethnicity subgroups; document gaps."),
            _r("ai.gov.drift_monitoring", "ai_governance", "monitoring",
               "Continuous performance and drift monitoring enabled",
               "drift_monitoring", "medium",
               "Enable drift detection with alerts on performance degradation."),
            _r("ai.gov.fda_clearance_path", "ai_governance", "regulatory",
               "FDA clearance path determined for the system's risk class",
               "fda_clearance_determined", "critical",
               "Classify the system (I/II/III or not-a-device) and determine the clearance path before deployment."),
        ],
    ),
}

# topic keyword -> rule-table names consulted
DOMAIN_KEYWORDS: Dict[str, List[str]] = {
    "hipaa": ["hipaa_technical", "hipaa_administrative", "hipaa_physical"],
    "phi": ["hipaa_technical", "hipaa_administrative", "hipaa_physical"],
    "patient": ["hipaa_technical", "hipaa_administrative", "hipaa_physical"],
    "fda": ["fda_records", "fda_signatures"],
    "cfr11": ["fda_records", "fda_signatures"],
    "21 cfr 11": ["fda_records", "fda_signatures"],
    "part 11": ["fda_records", "fda_signatures"],
    "electronic signature": ["fda_signatures"],
    "audit trail": ["fda_records"],
    "medical ai": ["ai_governance"],
    "ai governance": ["ai_governance"],
    "clinical ai": ["ai_governance"],
}

# words that mark an action as health-touching for the membrane hook
HEALTH_SURFACE_WORDS = (
    "phi", "hipaa", "patient", "medical", "health", "clinical",
    "diagnos", "treatment", "prescription", "ehr", "health record",
    "fda", "hospital", "clinic",
)


# ---------------------------------------------------------------------------
# Judgments
# ---------------------------------------------------------------------------


@dataclass
class HealthJudgment:
    """One health-reasoning judgment. Signed by content hash."""

    judgment_id: str
    verdict: str  # "clear" | "flagged" | "outside_scope"
    topic: str
    findings: List[Dict[str, Any]] = field(default_factory=list)
    rule_versions: Dict[str, str] = field(default_factory=dict)
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
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _seal(j: HealthJudgment) -> HealthJudgment:
    j.integrity_hash = hashlib.sha256(_canonical(j.unsigned_dict())).hexdigest()
    return j


def verify_judgment(j: HealthJudgment) -> bool:
    """Recompute the content hash. Tamper-evidence, not authentication."""
    if not j.integrity_hash:
        return False
    expected = hashlib.sha256(_canonical(j.unsigned_dict())).hexdigest()
    return expected == j.integrity_hash


def _matching_tables(topic: str) -> List[str]:
    """Rule-table names whose domain keywords appear in the topic."""
    t = topic.lower()
    matched: List[str] = []
    for keyword, tables in DOMAIN_KEYWORDS.items():
        if keyword in t:
            for name in tables:
                if name not in matched:
                    matched.append(name)
    return matched


def consult_health(topic: str, evidence: Dict[str, Any]) -> HealthJudgment:
    """The consult API. Deterministic health-reasoning judgment.

    topic: what the question is about ("hipaa", "fda 21 cfr 11",
        "medical ai governance", ...). evidence: mapping of check-keys to
    truthy (control present/satisfied) or falsy/missing values.

    Returns a HealthJudgment with verdict:
      - "clear": every consulted rule satisfied by the evidence
      - "flagged": one or more rules unsatisfied, or no evidence at all
        for a health topic (fail-closed)
      - "outside_scope": the topic matched no rule domain. She declares
        the limit instead of scoring anyway.
    """
    now = int(time.time())
    judgment_id = hashlib.sha256(
        f"health:{topic}:{now}:{json.dumps(evidence, sort_keys=True, default=str)}".encode()
    ).hexdigest()[:16]

    matched = _matching_tables(topic)
    if not matched:
        return _seal(HealthJudgment(
            judgment_id=judgment_id,
            verdict=OUTSIDE_SCOPE,
            topic=topic,
            findings=[],
            rule_versions={},
            note=(
                "No health rule domain covers this topic. DrMythara declines "
                "to score it: outside_scope is a declaration, not a guess. "
                "NOT A MEDICAL PROFESSIONAL — compliance guidance only."
            ),
            issued_at=now,
        ))

    rule_versions = {name: RULE_TABLES[name].version for name in matched}
    findings: List[Dict[str, Any]] = []

    if not evidence:
        findings.append({
            "rule_id": "*",
            "domain": "health",
            "requirement": "Compliance evidence provided for evaluation",
            "severity": "high",
            "guidance": (
                "Fail-closed: a health-touching question with no evidence "
                "cannot be cleared. Provide compliance evidence for each "
                "consulted rule, or route to human review."
            ),
        })
    else:
        for name in matched:
            table = RULE_TABLES[name]
            for rule in table.rules:
                if not evidence.get(rule.check):
                    findings.append({
                        "rule_id": rule.rule_id,
                        "domain": rule.domain,
                        "requirement": rule.requirement,
                        "severity": rule.severity,
                        "guidance": rule.guidance,
                    })

    verdict = FLAGGED if findings else CLEAR
    return _seal(HealthJudgment(
        judgment_id=judgment_id,
        verdict=verdict,
        topic=topic,
        findings=findings,
        rule_versions=rule_versions,
        note=(
            "NOT A MEDICAL PROFESSIONAL. Compliance guidance only — "
            "evaluated against cited rule versions above."
        ),
        issued_at=now,
    ))


def screen_health(
    action_description: str,
    evidence: Optional[Dict[str, Any]] = None,
) -> HealthJudgment:
    """Membrane hook: call before a health-touching action clears.

    If the description has no health surface, returns a clear judgment
    noting so (cheap path — she stays out of the way). If it does,
    consults the matching rule domains. Health-touching + no evidence =
    flagged (fail-closed), never silently cleared.
    """
    desc = action_description.lower()
    if not any(w in desc for w in HEALTH_SURFACE_WORDS):
        now = int(time.time())
        return _seal(HealthJudgment(
            judgment_id=hashlib.sha256(
                f"screen:{action_description}:{now}".encode()
            ).hexdigest()[:16],
            verdict=CLEAR,
            topic=action_description,
            findings=[],
            rule_versions={},
            note="No health surface detected in action description; no health rules consulted.",
            issued_at=now,
        ))

    matched: List[str] = []
    for keyword, tables in DOMAIN_KEYWORDS.items():
        if keyword in desc:
            for name in tables:
                if name not in matched:
                    matched.append(name)
    topic = " ".join(matched) if matched else "hipaa"
    return consult_health(topic, evidence or {})


def health_bounds_check(
    purpose: str,
    action_type: str,
    payload: Dict[str, Any],
) -> Optional[str]:
    """Adapter for SoulCradleAuthority.set_bounds_check.

    Signature matches the bounds-check contract exactly:
    fn(purpose, action_type, payload) -> refusal reason or None.
    A flagged health judgment refuses the action; clear and
    outside_scope allow it (outside_scope means no health rules apply).
    Payloads may carry evidence under the "health_evidence" key.
    """
    description = f"{purpose} | {action_type} | {json.dumps(payload, sort_keys=True, default=str)[:500]}"
    evidence = payload.get("health_evidence")
    if not isinstance(evidence, dict):
        evidence = None
    judgment = screen_health(description, evidence)
    if judgment.verdict == FLAGGED:
        top = judgment.findings[0]
        return (
            f"health screen flagged ({judgment.judgment_id}): "
            f"{top.get('requirement', 'unsatisfied health rule')} "
            f"[{top.get('rule_id', '*')}]. "
            f"{len(judgment.findings)} finding(s). Compliance guidance only — not medical advice."
        )
    return None


def health_witness_declaration(
    authority: StandingAuthority,
    event_ref: str,
    judgment: HealthJudgment,
) -> Declaration:
    """Translate a health judgment into the standing matrix.

    In the standing matrix DrMythara speaks only as WITNESS: she declares
    what she observed (the evaluated evidence and the resulting judgment),
    never as wronged or trespasser. A stranger declares nothing; she is no
    stranger to health evidence she actually evaluated.
    """
    statement = (
        f"DrMythara health judgment {judgment.judgment_id}: "
        f"verdict={judgment.verdict} on topic {judgment.topic!r} "
        f"({len(judgment.findings)} finding(s), "
        f"rules={json.dumps(judgment.rule_versions, sort_keys=True)}). "
        f"Compliance guidance only — not a medical professional."
    )
    return authority.declare(
        WITNESS_STATEMENT,
        actor="drmythara",
        role=WITNESS,
        event_ref=event_ref,
        statement=statement,
        scope={
            "observed": True,
            "verdict": judgment.verdict,
            "judgment": judgment.to_dict(),
        },
    )


def rule_inventory() -> Dict[str, Dict[str, str]]:
    """Every table with its version, date, and source. For audits."""
    return {
        name: {
            "version": t.version,
            "effective_date": t.effective_date,
            "source": t.source,
            "rule_count": str(len(t.rules)),
        }
        for name, t in RULE_TABLES.items()
    }
