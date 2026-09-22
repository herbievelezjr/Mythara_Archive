import os
import sys
# Copyright © 2025 Herbert Velez Jr. All rights reserved.

"""
DrMythara Bot - Healthcare Compliance Specialist (user-facing wrapper).

Thin demo face. The canonical health-reasoning core lives in
soul_cradle/health.py — rule tables, consult_health(), screen_health(),
and the standing-matrix adapter. This wrapper owns the SQLite audit
trail, the self-assessment checklist flows, and orchestrator
registration. It owns no rules: every rule it references comes from the
core.

- HIPAA self-assessment checklists (NOT audits)
- FDA 21 CFR Part 11 readiness checklists (NOT validations)
- Medical AI governance checklists

NOT A MEDICAL PROFESSIONAL. DOES NOT PROVIDE MEDICAL ADVICE.
COMPLIANCE GUIDANCE ONLY.

HONESTY CONTRACT (read before using the checklist functions):
  * Every "audit" / "validation" / "assessment" function below is a
    SELF-ASSESSMENT CHECKLIST, not an audit. It evaluates ONLY the
    answers the caller supplies and derives every finding from those
    inputs. Nothing is simulated, scanned, or pre-filled — the old
    simulated flows with canned findings were removed.
  * Answers are keyed by control id (the rule "check" fields in
    soul_cradle/health.py). Call bot.checklist_controls(domain) to list
    the exact questions and their control ids.
  * Answer values: True (control in place) / False (not in place) /
    "unknown" (no answer). Unanswered controls are reported as UNKNOWN —
    never assumed pass or fail. Unrecognized values are treated as
    unknown, never guessed.
  * Output is always labeled "self-assessment checklist, not an audit"
    and never implies certification, compliance achievement, audit
    completeness, or a regulatory determination.
"""

# Repo-root bootstrap so the wrapper can reach the Soul Cradle core.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import sqlite3
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
import requests

from soul_cradle.health import (
    RULE_TABLES,
    consult_health,
    screen_health,
    verify_judgment,
    rule_inventory,
)

try:
    from soul_cradle.bot_witness import (
        witness_action,
        checklist_evidence,
        WitnessUnavailable,
    )
except ImportError:  # pragma: no cover — direct-script fallback
    from pathlib import Path as _WitnessPath

    sys.path.insert(0, str(_WitnessPath(__file__).resolve().parent.parent))
    from soul_cradle.bot_witness import (
        witness_action,
        checklist_evidence,
        WitnessUnavailable,
    )

# Orchestrator connection
ORCHESTRATOR_URL = "http://localhost:5000"
# QUICKFIX FIX: Moved to environment variable (CWE-798)
VP_MASTER_TOKEN = os.getenv("VP_MASTER_TOKEN", "")  # Set via environment

DISCLAIMER = (
    "NOT A MEDICAL PROFESSIONAL. DOES NOT PROVIDE MEDICAL ADVICE. "
    "COMPLIANCE GUIDANCE ONLY."
)

CHECKLIST_LABEL = (
    "SELF-ASSESSMENT CHECKLIST — NOT AN AUDIT. Results reflect only "
    "caller-supplied answers; this is not an audit, not a certification, "
    "not a determination of compliance, and not a complete assessment."
)

# Rule-table -> legacy nested group label (shape compatibility for rule views)
_TABLE_GROUPS = {
    "hipaa_technical": "technical_safeguards",
    "hipaa_administrative": "administrative_safeguards",
    "hipaa_physical": "physical_safeguards",
}

# Checklist domain -> canonical rule-table names consulted
CHECKLIST_TABLES = {
    "hipaa": ["hipaa_technical", "hipaa_administrative", "hipaa_physical"],
    "fda_cfr11": ["fda_records", "fda_signatures"],
    "ai_governance": ["ai_governance"],
}

# Rule table -> audit-trail group label
_TABLE_GROUP = {
    "hipaa_technical": "technical",
    "hipaa_administrative": "administrative",
    "hipaa_physical": "physical",
    "fda_records": "records",
    "fda_signatures": "signatures",
    "ai_governance": "governance",
}

# Answer normalization: truthy tokens, falsy tokens. Anything else (or
# missing) -> unknown. Never guessed.
_TRUE_TOKENS = {
    "true", "yes", "y", "1", "pass", "passed", "implemented", "satisfied",
    "compliant", "complete", "done", "in_place", "in place",
}
_FALSE_TOKENS = {
    "false", "no", "n", "0", "fail", "failed", "not_implemented",
    "not implemented", "unsatisfied", "non_compliant", "noncompliant",
    "incomplete", "missing", "absent",
}

# Reference data (identifier categories, not checkable rules)
PHI_CATEGORIES = [
    "names", "addresses", "dates", "phone_numbers", "fax_numbers", "email_addresses",
    "ssn", "medical_record_numbers", "health_plan_numbers", "account_numbers",
    "certificate_numbers", "vehicle_identifiers", "device_identifiers", "urls",
    "ip_addresses", "biometric_identifiers", "photos", "unique_identifying_numbers",
]

AI_GOVERNANCE_REFERENCE = {
    "risk_categories": {
        "low_risk": "Non-diagnostic informational AI (e.g., appointment scheduling)",
        "moderate_risk": "Clinical decision support without autonomous action",
        "high_risk": "Diagnostic AI requiring FDA clearance",
        "critical_risk": "Autonomous treatment AI (rare, heavily regulated)",
    },
    "fda_device_classes": {
        "class_i": "Low risk, general controls",
        "class_ii": "Moderate risk, special controls + 510(k) clearance",
        "class_iii": "High risk, PMA (Pre-Market Approval) required",
    },
}


def _nested_rule_view() -> Dict[str, Any]:
    """Rebuild the legacy nested rule shape from the canonical core tables."""
    view: Dict[str, Any] = {}
    for table_name, group in _TABLE_GROUPS.items():
        table = RULE_TABLES[table_name]
        group_view = view.setdefault(group, {})
        for rule in table.rules:
            group_view.setdefault(rule.category, []).append(rule.check)
    view["phi_categories"] = list(PHI_CATEGORIES)
    return view


def prompt_answer(check_id: str, requirement: str):
    """Example `ask` callable for interactive checklist use (stdin).

    Pass as ask=prompt_answer to audit_hipaa_compliance() /
    validate_fda_cfr11_compliance() / assess_medical_ai_governance() to be
    prompted for each control not present in `answers`.
    """
    return input(f"[{check_id}] {requirement}\n  Implemented? (yes/no/unknown): ")


class DrMytharaBot:
    """DrMythara Bot - Healthcare compliance specialist (user-facing wrapper)."""

    def __init__(self):
        self.bot_id = "drmythara_bot"
        self.bot_token = None
        self.db_path = "mythara_drmythara.db"

        # Rule views are projections of the canonical core — not copies.
        self.hipaa_rules = _nested_rule_view()
        self.ai_governance = dict(AI_GOVERNANCE_REFERENCE)

        # Initialize database
        self._init_db()

        # Register with orchestrator
        self._register()

    # -- canonical core passthroughs -------------------------------------

    def consult(self, topic: str, evidence: Dict[str, Any]):
        """Health-reasoning consult. Delegates to soul_cradle.health.

        Returns a HealthJudgment: verdict in {"clear","flagged",
        "outside_scope"}, findings, rule_versions, integrity_hash.
        """
        return consult_health(topic, evidence)

    def screen(self, action_description: str, evidence: Optional[Dict[str, Any]] = None):
        """Membrane hook passthrough: screen_health() from the core."""
        return screen_health(action_description, evidence)

    def rule_versions(self) -> Dict[str, Dict[str, str]]:
        """Every rule table with version, effective date, and source."""
        return rule_inventory()

    # -- audit trail ------------------------------------------------------

    def _init_db(self):
        """Initialize DrMythara database."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # HIPAA compliance audits
        c.execute('''
            CREATE TABLE IF NOT EXISTS hipaa_audits (
                audit_id TEXT PRIMARY KEY,
                organization_name TEXT NOT NULL,
                audit_date TEXT NOT NULL,
                audit_type TEXT CHECK(audit_type IN ('initial', 'annual', 'incident', 'ad_hoc')),
                scope TEXT,
                technical_score INT DEFAULT 0,
                administrative_score INT DEFAULT 0,
                physical_score INT DEFAULT 0,
                overall_score INT DEFAULT 0,
                findings TEXT,
                critical_issues INT DEFAULT 0,
                high_issues INT DEFAULT 0,
                medium_issues INT DEFAULT 0,
                low_issues INT DEFAULT 0,
                remediation_plan TEXT,
                status TEXT DEFAULT 'in_progress',
                completed_at TEXT,
                integrity_hash TEXT
            )
        ''')

        # FDA 21 CFR Part 11 validations
        c.execute('''
            CREATE TABLE IF NOT EXISTS fda_validations (
                validation_id TEXT PRIMARY KEY,
                system_name TEXT NOT NULL,
                validation_date TEXT NOT NULL,
                validation_type TEXT CHECK(validation_type IN ('initial', 'periodic', 'change_control', 'revalidation')),
                electronic_records_compliant BOOLEAN DEFAULT 0,
                electronic_signatures_compliant BOOLEAN DEFAULT 0,
                audit_trail_compliant BOOLEAN DEFAULT 0,
                overall_compliant BOOLEAN DEFAULT 0,
                findings TEXT,
                gaps TEXT,
                remediation_actions TEXT,
                status TEXT DEFAULT 'in_progress',
                completed_at TEXT,
                integrity_hash TEXT
            )
        ''')

        # Medical AI governance assessments
        c.execute('''
            CREATE TABLE IF NOT EXISTS ai_governance_assessments (
                assessment_id TEXT PRIMARY KEY,
                ai_system_name TEXT NOT NULL,
                assessment_date TEXT NOT NULL,
                risk_category TEXT CHECK(risk_category IN ('low_risk', 'moderate_risk', 'high_risk', 'critical_risk')),
                fda_device_class TEXT CHECK(fda_device_class IN ('class_i', 'class_ii', 'class_iii', 'not_device')),
                requires_fda_clearance BOOLEAN DEFAULT 0,
                clinical_validation_complete BOOLEAN DEFAULT 0,
                bias_testing_complete BOOLEAN DEFAULT 0,
                drift_monitoring_enabled BOOLEAN DEFAULT 0,
                overall_governance_score INT DEFAULT 0,
                findings TEXT,
                recommendations TEXT,
                status TEXT DEFAULT 'in_progress',
                completed_at TEXT,
                integrity_hash TEXT
            )
        ''')

        # PHI exposure incidents
        c.execute('''
            CREATE TABLE IF NOT EXISTS phi_incidents (
                incident_id TEXT PRIMARY KEY,
                detected_at TEXT NOT NULL,
                incident_type TEXT CHECK(incident_type IN ('unauthorized_access', 'data_breach', 'improper_disposal', 'lost_device', 'ransomware', 'phishing', 'insider_threat')),
                severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical')),
                affected_records INT DEFAULT 0,
                affected_phi_categories TEXT,
                breach_notification_required BOOLEAN DEFAULT 0,
                ocr_notified BOOLEAN DEFAULT 0,
                patients_notified BOOLEAN DEFAULT 0,
                root_cause TEXT,
                remediation_actions TEXT,
                status TEXT DEFAULT 'investigating',
                resolved_at TEXT,
                integrity_hash TEXT
            )
        ''')

        # Compliance reports
        c.execute('''
            CREATE TABLE IF NOT EXISTS compliance_reports (
                report_id TEXT PRIMARY KEY,
                report_type TEXT CHECK(report_type IN ('hipaa', 'fda_cfr11', 'ai_governance', 'combined')),
                generated_at TEXT NOT NULL,
                reporting_period_start TEXT NOT NULL,
                reporting_period_end TEXT NOT NULL,
                overall_compliance_score INT DEFAULT 0,
                total_audits INT DEFAULT 0,
                critical_findings INT DEFAULT 0,
                recommendations TEXT,
                executive_summary TEXT,
                integrity_hash TEXT
            )
        ''')

        conn.commit()
        conn.close()
        print("[OK] DrMythara Bot database initialized: mythara_drmythara.db")

    def _register(self):
        """Register with Mythara Orchestrator."""
        try:
            response = requests.post(
                f"{ORCHESTRATOR_URL}/register_bot",
                json={
                    "vp_token": VP_MASTER_TOKEN,
                    "bot_id": self.bot_id,
                    "bot_name": "DrMythara Healthcare Compliance Bot"
                },
                timeout=5
            )
            if response.status_code == 200:
                self.bot_token = response.json()['bot_token']
                print(f"[OK] Registered with orchestrator: {self.bot_id}")
        except Exception as e:
            print(f"[WARN] Could not connect to orchestrator: {e}")

    def _generate_integrity_hash(self, data: Dict[str, Any]) -> str:
        """Generate SHA-256 hash for audit trail."""
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()[:16]

    # -- honest checklist engine (self-assessment; nothing is simulated) ---

    def _witness_checklist(self, domain: str, summary: Dict[str, int]) -> None:
        """Record a checklist completion with the Soul Cradle panel.

        Record-only: a self-assessment checklist is never blocked, but its
        completion is witnessed and chained. Warn-and-proceed on outage.
        """
        try:
            evidence, bases = checklist_evidence(
                domain=domain,
                controls_total=summary["total_controls"],
                controls_failed=summary["failed"],
                controls_unknown=summary["unanswered"],
                declared_intent="report the checklist answers honestly; unanswered stay UNKNOWN",
            )
            witness_action(
                bot_id="drmythara",
                action=f"complete {domain} self-assessment checklist",
                evidence=evidence,
                evidence_bases=bases,
                enforce=False,
            )
        except WitnessUnavailable as exc:
            print(f"[DRMYTHARA] WITNESS UNAVAILABLE — {exc}; proceeding.")

    @staticmethod
    def _normalize_answer(raw: Any) -> Optional[bool]:
        """Normalize a caller-supplied answer -> True | False | None(unknown).

        Unrecognized or missing values become unknown. Never guessed.
        """
        if raw is None:
            return None
        if isinstance(raw, bool):
            return raw
        token = str(raw).strip().lower()
        if token in _TRUE_TOKENS:
            return True
        if token in _FALSE_TOKENS:
            return False
        return None

    @staticmethod
    def _json_safe(raw: Any) -> Any:
        """Keep stored answers JSON-serializable."""
        if raw is None or isinstance(raw, (bool, int, float, str)):
            return raw
        return str(raw)

    def checklist_controls(self, domain: str = "hipaa") -> List[Dict[str, Any]]:
        """List the control questions for a checklist domain.

        Returns [{table, rule_id, check, requirement, category, severity,
        guidance}]. The "check" value is the key your `answers` dict must
        supply. Every rule comes from the canonical core tables.
        """
        if domain not in CHECKLIST_TABLES:
            raise ValueError(
                f"Unknown checklist domain: {domain!r}. "
                f"Choose from {sorted(CHECKLIST_TABLES)}"
            )
        controls = []
        for table_name in CHECKLIST_TABLES[domain]:
            table = RULE_TABLES[table_name]
            for rule in table.rules:
                controls.append({
                    "table": table_name,
                    "rule_id": rule.rule_id,
                    "check": rule.check,
                    "requirement": rule.requirement,
                    "category": rule.category,
                    "severity": rule.severity,
                    "guidance": rule.guidance,
                })
        return controls

    def _run_checklist(
        self,
        tables,
        answers: Optional[Dict[str, Any]] = None,
        ask: Optional[Callable[[str, str], Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Evaluate caller-supplied answers against the canonical rules.

        Every control result derives from the caller's input. Returns
        per-control dicts with status in {"pass", "fail", "unknown"}.
        """
        answers = answers or {}
        table_names = [tables] if isinstance(tables, str) else list(tables)
        results = []
        for table_name in table_names:
            table = RULE_TABLES[table_name]
            for rule in table.rules:
                raw = answers.get(rule.check)
                if raw is None and ask is not None:
                    raw = ask(rule.check, rule.requirement)
                verdict = self._normalize_answer(raw)
                status = (
                    "pass" if verdict is True
                    else "fail" if verdict is False
                    else "unknown"
                )
                results.append({
                    "table": table_name,
                    "rule_id": rule.rule_id,
                    "check": rule.check,
                    "requirement": rule.requirement,
                    "category": rule.category,
                    "severity": rule.severity,
                    "guidance": rule.guidance,
                    "answer": self._json_safe(raw),
                    "status": status,
                })
        return results

    @staticmethod
    def _checklist_summary(results: List[Dict[str, Any]]) -> Dict[str, int]:
        """Score from answered controls only; unanswered are reported, not scored."""
        passed = sum(1 for r in results if r["status"] == "pass")
        failed = sum(1 for r in results if r["status"] == "fail")
        unknown = sum(1 for r in results if r["status"] == "unknown")
        answered = passed + failed
        score = round(passed / answered * 100) if answered else 0
        return {
            "total_controls": len(results),
            "answered": answered,
            "unanswered": unknown,
            "passed": passed,
            "failed": failed,
            "score": score,
        }

    @staticmethod
    def _findings_from_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Build findings ONLY from the caller's answers. No canned findings.

        Failed controls become findings carrying the rule's own severity,
        requirement, and remediation guidance from the canonical core.
        Unanswered controls become "unknown" advisories — never assumed
        pass or fail.
        """
        findings = []
        for r in results:
            if r["status"] == "fail":
                findings.append({
                    "rule_id": r["rule_id"],
                    "severity": r["severity"],
                    "finding": (
                        "Control NOT satisfied per caller-supplied answer: "
                        f"{r['requirement']}"
                    ),
                    "recommendation": r["guidance"],
                })
            elif r["status"] == "unknown":
                findings.append({
                    "rule_id": r["rule_id"],
                    "severity": "advisory",
                    "finding": (
                        "No answer supplied — status UNKNOWN (not assumed "
                        f"pass or fail): {r['requirement']}"
                    ),
                    "recommendation": (
                        "Answer this control to complete the checklist; "
                        "unanswered controls cannot be cleared."
                    ),
                })
        return findings

    # -- checklist flows (self-assessment; the core does the real reasoning)

    def audit_hipaa_compliance(
        self,
        organization: str,
        answers: Optional[Dict[str, Any]] = None,
        ask: Optional[Callable[[str, str], Any]] = None,
        scope: str = "full",
    ) -> Dict[str, Any]:
        """HIPAA self-assessment checklist (NOT an audit).

        Evaluates ONLY the answers you supply. Nothing is simulated and no
        finding is pre-written: every result derives from `answers`.

        Args:
            organization: Name of the organization being assessed.
            answers: dict of control_id -> True/False/"unknown". Control
                ids are the rule "check" fields; see checklist_controls().
                Omitted controls are reported as UNKNOWN.
            ask: optional callable(check_id, requirement) -> answer, used
                for controls missing from `answers` (interactive prompting;
                pass prompt_answer for a stdin prompt).
            scope: 'full', 'technical', 'administrative', or 'physical'.

        Returns:
            Checklist results labeled as self-assessment, with per-control
            pass/fail/unknown, findings derived from the answers, and the
            disclaimer. NOT a medical professional; NOT an audit.
        """
        scope_map = {
            "full": CHECKLIST_TABLES["hipaa"],
            "technical": ["hipaa_technical"],
            "administrative": ["hipaa_administrative"],
            "physical": ["hipaa_physical"],
        }
        if scope not in scope_map:
            raise ValueError(f"Unknown scope: {scope!r}. Choose from {sorted(scope_map)}")
        tables = scope_map[scope]

        audit_id = hashlib.sha256(
            f"{organization}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]

        results = self._run_checklist(tables, answers, ask)
        summary = self._checklist_summary(results)
        findings = self._findings_from_results(results)

        # Per-group scores for the audit-trail columns (answered controls only)
        group_scores = {}
        for table_name in tables:
            group = _TABLE_GROUP[table_name]
            group_results = [r for r in results if r["table"] == table_name]
            group_scores[group] = self._checklist_summary(group_results)["score"]

        technical_score = group_scores.get("technical", 0)
        administrative_score = group_scores.get("administrative", 0)
        physical_score = group_scores.get("physical", 0)

        critical_issues = sum(1 for r in results if r["status"] == "fail" and r["severity"] == "critical")
        high_issues = sum(1 for r in results if r["status"] == "fail" and r["severity"] == "high")
        medium_issues = sum(1 for r in results if r["status"] == "fail" and r["severity"] == "medium")
        low_issues = sum(1 for r in results if r["status"] == "fail" and r["severity"] == "low")

        findings_payload = {
            "label": CHECKLIST_LABEL,
            "disclaimer": DISCLAIMER,
            "controls": results,
            "findings": findings,
        }

        audit_data = {
            "audit_id": audit_id,
            "organization_name": organization,
            "audit_date": datetime.now().isoformat(),
            "audit_type": "ad_hoc",
            "scope": scope,
            "technical_score": technical_score,
            "administrative_score": administrative_score,
            "physical_score": physical_score,
            "overall_score": summary["score"],
            "findings": json.dumps(findings_payload),
            "critical_issues": critical_issues,
            "high_issues": high_issues,
            "medium_issues": medium_issues,
            "low_issues": low_issues,
            "status": "completed",
            "completed_at": datetime.now().isoformat(),
        }
        audit_data["integrity_hash"] = self._generate_integrity_hash(audit_data)

        # Save to database
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO hipaa_audits VALUES
                     (:audit_id, :organization_name, :audit_date, :audit_type, :scope,
                      :technical_score, :administrative_score, :physical_score, :overall_score,
                      :findings, :critical_issues, :high_issues, :medium_issues, :low_issues,
                      NULL, :status, :completed_at, :integrity_hash)''', audit_data)
        conn.commit()
        conn.close()

        if summary["failed"] or summary["unanswered"]:
            recommendation = (
                f"Address the {summary['failed']} failed control(s) and answer the "
                f"{summary['unanswered']} unanswered control(s), then re-run. This "
                "checklist alone is not a determination of compliance."
            )
        else:
            recommendation = (
                "All controls answered and satisfied. Self-assessment only — "
                "not an audit, not a certification, not a compliance determination."
            )

        self._witness_checklist("hipaa", summary)

        return {
            "label": CHECKLIST_LABEL,
            "disclaimer": DISCLAIMER,
            "audit_id": audit_id,
            "organization": organization,
            "scope": scope,
            "overall_score": summary["score"],
            "technical_score": technical_score,
            "administrative_score": administrative_score,
            "physical_score": physical_score,
            "controls_answered": summary["answered"],
            "controls_unanswered": summary["unanswered"],
            "controls_passed": summary["passed"],
            "controls_failed": summary["failed"],
            "findings": findings,
            "critical_issues": critical_issues,
            "high_issues": high_issues,
            "recommendation": recommendation,
        }

    def validate_fda_cfr11_compliance(
        self,
        system_name: str,
        answers: Optional[Dict[str, Any]] = None,
        ask: Optional[Callable[[str, str], Any]] = None,
    ) -> Dict[str, Any]:
        """FDA 21 CFR Part 11 readiness checklist (NOT a validation).

        Same honesty contract as audit_hipaa_compliance(): evaluates ONLY
        caller-supplied answers keyed by control id (see
        checklist_controls("fda_cfr11")). A group reads compliant only when
        every control in it was answered and passed; any unanswered control
        yields None (unknown), never an assumed pass.
        """
        validation_id = hashlib.sha256(
            f"{system_name}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]

        results = self._run_checklist(CHECKLIST_TABLES["fda_cfr11"], answers, ask)
        summary = self._checklist_summary(results)
        findings = self._findings_from_results(results)

        def _group_flag(table_name: str, check_id: Optional[str] = None) -> Optional[bool]:
            group = [r for r in results if r["table"] == table_name]
            if check_id is not None:
                group = [r for r in group if r["check"] == check_id]
            if any(r["status"] == "fail" for r in group):
                return False
            if group and all(r["status"] == "pass" for r in group):
                return True
            return None  # unanswered somewhere — unknown, not assumed

        records_compliant = _group_flag("fda_records")
        signatures_compliant = _group_flag("fda_signatures")
        audit_trail_compliant = _group_flag("fda_records", "audit_trail")

        flags = [records_compliant, signatures_compliant, audit_trail_compliant]
        if all(f is True for f in flags):
            overall_compliant: Optional[bool] = True
        elif any(f is False for f in flags):
            overall_compliant = False
        else:
            overall_compliant = None

        gaps = [
            f"{f['finding']} Remediation: {f['recommendation']}"
            for f in findings if f["severity"] != "advisory"
        ]

        findings_payload = {
            "label": CHECKLIST_LABEL,
            "disclaimer": DISCLAIMER,
            "controls": results,
            "findings": findings,
        }

        validation_data = {
            "validation_id": validation_id,
            "system_name": system_name,
            "validation_date": datetime.now().isoformat(),
            "validation_type": "periodic",  # self-assessment checklist run
            "electronic_records_compliant": records_compliant,
            "electronic_signatures_compliant": signatures_compliant,
            "audit_trail_compliant": audit_trail_compliant,
            "overall_compliant": overall_compliant,
            "findings": json.dumps(findings_payload),
            "gaps": json.dumps(gaps),
            "status": "completed",
            "completed_at": datetime.now().isoformat(),
        }
        validation_data["integrity_hash"] = self._generate_integrity_hash(validation_data)

        # Save to database
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO fda_validations VALUES
                     (:validation_id, :system_name, :validation_date, :validation_type,
                      :electronic_records_compliant, :electronic_signatures_compliant,
                      :audit_trail_compliant, :overall_compliant, :findings, :gaps,
                      NULL, :status, :completed_at, :integrity_hash)''', validation_data)
        conn.commit()
        conn.close()

        if overall_compliant is True:
            recommendation = (
                "All answered controls satisfied. Readiness checklist only — "
                "not a validation, not a certification, not a compliance determination."
            )
        elif overall_compliant is False:
            recommendation = "Address the gaps before using the system in production."
        else:
            recommendation = (
                "Cannot determine readiness: some controls are unanswered. "
                "Answer every control, then re-run."
            )

        self._witness_checklist("fda_cfr11", summary)

        return {
            "label": CHECKLIST_LABEL,
            "disclaimer": DISCLAIMER,
            "validation_id": validation_id,
            "system_name": system_name,
            "overall_compliant": overall_compliant,
            "electronic_records_compliant": records_compliant,
            "electronic_signatures_compliant": signatures_compliant,
            "audit_trail_compliant": audit_trail_compliant,
            "controls_answered": summary["answered"],
            "controls_unanswered": summary["unanswered"],
            "gaps": gaps,
            "recommendation": recommendation,
        }

    def assess_medical_ai_governance(
        self,
        ai_system: str,
        use_case: str,
        answers: Optional[Dict[str, Any]] = None,
        ask: Optional[Callable[[str, str], Any]] = None,
        risk_category: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Medical-AI governance checklist (NOT a regulatory assessment).

        Governance findings derive ONLY from caller-supplied answers keyed
        by control id (see checklist_controls("ai_governance")). The risk
        category is a rough keyword screening of the use case unless the
        caller supplies one — it is an estimate, not a clinical or
        regulatory determination.
        """
        assessment_id = hashlib.sha256(
            f"{ai_system}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]

        results = self._run_checklist(CHECKLIST_TABLES["ai_governance"], answers, ask)
        summary = self._checklist_summary(results)
        findings = self._findings_from_results(results)

        allowed_categories = ("low_risk", "moderate_risk", "high_risk", "critical_risk")
        if risk_category is None:
            risk_basis = "keyword_heuristic_estimate"
            lowered = use_case.lower()
            risk_category = "moderate_risk"
            if "autonomous" in lowered:
                risk_category = "critical_risk"
            elif "diagnostic" in lowered or "treatment" in lowered:
                risk_category = "high_risk"
            elif "scheduling" in lowered or "reminder" in lowered:
                risk_category = "low_risk"
        else:
            risk_basis = "caller_supplied"
        if risk_category not in allowed_categories:
            raise ValueError(
                f"Unknown risk_category: {risk_category!r}. "
                f"Choose from {allowed_categories}"
            )

        # Device-class screening estimate — confirm with FDA classification.
        fda_class = "not_device"
        requires_clearance = False
        if risk_category in ("high_risk", "critical_risk"):
            fda_class = "class_ii"
            requires_clearance = True
        elif risk_category == "moderate_risk":
            fda_class = "class_i"

        def _rule_flag(check_id: str) -> Optional[bool]:
            match = [r for r in results if r["check"] == check_id]
            if not match:
                return None
            status = match[0]["status"]
            return True if status == "pass" else (False if status == "fail" else None)

        recommendations = [
            f"{f['finding']} Remediation: {f['recommendation']}"
            for f in findings
        ]

        assessment_data = {
            "assessment_id": assessment_id,
            "ai_system_name": ai_system,
            "assessment_date": datetime.now().isoformat(),
            "risk_category": risk_category,
            "fda_device_class": fda_class,
            "requires_fda_clearance": requires_clearance,
            "clinical_validation_complete": _rule_flag("clinical_validation"),
            "bias_testing_complete": _rule_flag("bias_testing"),
            "drift_monitoring_enabled": _rule_flag("drift_monitoring"),
            "overall_governance_score": summary["score"],
            "findings": json.dumps({
                "label": CHECKLIST_LABEL,
                "disclaimer": DISCLAIMER,
                "controls": results,
                "findings": findings,
            }),
            "recommendations": json.dumps(recommendations),
            "status": "completed",
            "completed_at": datetime.now().isoformat(),
        }
        assessment_data["integrity_hash"] = self._generate_integrity_hash(assessment_data)

        # Save to database
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO ai_governance_assessments VALUES
                     (:assessment_id, :ai_system_name, :assessment_date, :risk_category,
                      :fda_device_class, :requires_fda_clearance, :clinical_validation_complete,
                      :bias_testing_complete, :drift_monitoring_enabled, :overall_governance_score,
                      :findings, :recommendations, :status, :completed_at, :integrity_hash)''', assessment_data)
        conn.commit()
        conn.close()

        self._witness_checklist("ai_governance", summary)

        return {
            "label": CHECKLIST_LABEL,
            "disclaimer": DISCLAIMER,
            "assessment_id": assessment_id,
            "ai_system": ai_system,
            "risk_category": risk_category,
            "risk_basis": risk_basis,
            "risk_note": (
                "Risk category is a rough screening estimate "
                f"({risk_basis.replace('_', ' ')}), not a clinical or "
                "regulatory determination."
            ),
            "fda_device_class": fda_class,
            "fda_device_class_note": "Estimated device class — confirm with FDA classification.",
            "requires_fda_clearance": requires_clearance,
            "governance_score": summary["score"],
            "controls_answered": summary["answered"],
            "controls_unanswered": summary["unanswered"],
            "findings": findings,
            "recommendations": recommendations,
        }

    def generate_compliance_report(self) -> str:
        """Generate a summary of recorded self-assessment checklists.

        Aggregates the checklist audit trail. These are self-reported
        checklist runs — not audits, not certifications.
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Get recent checklist runs
        c.execute('''SELECT COUNT(*), AVG(overall_score), SUM(critical_issues), SUM(high_issues)
                     FROM hipaa_audits
                     WHERE audit_date >= date('now', '-30 days')''')
        hipaa_stats = c.fetchone()

        # Get recent validations
        c.execute('''SELECT COUNT(*),
                     SUM(CASE WHEN overall_compliant = 1 THEN 1 ELSE 0 END)
                     FROM fda_validations
                     WHERE validation_date >= date('now', '-30 days')''')
        fda_stats = c.fetchone()

        # Get recent AI assessments
        c.execute('''SELECT COUNT(*), AVG(overall_governance_score),
                     SUM(CASE WHEN requires_fda_clearance = 1 THEN 1 ELSE 0 END)
                     FROM ai_governance_assessments
                     WHERE assessment_date >= date('now', '-30 days')''')
        ai_stats = c.fetchone()

        # Get recent PHI incidents
        c.execute('''SELECT COUNT(*), SUM(affected_records)
                     FROM phi_incidents
                     WHERE detected_at >= date('now', '-30 days')''')
        incident_stats = c.fetchone()

        conn.close()

        report = f"""
{'='*80}
    DRMYTHARA BOT - HEALTHCARE SELF-ASSESSMENT CHECKLIST SUMMARY
                 {datetime.now().strftime('%Y-%m-%d %H:%M')}
{'='*80}

NOT A MEDICAL PROFESSIONAL. DOES NOT PROVIDE MEDICAL ADVICE.
COMPLIANCE GUIDANCE ONLY.

{CHECKLIST_LABEL}

HIPAA SELF-ASSESSMENT CHECKLISTS (Last 30 Days):
   Total Checklist Runs: {hipaa_stats[0] or 0}
   Avg Score (answered controls only): {hipaa_stats[1] or 0:.1f}%
   Critical Issues: {hipaa_stats[2] or 0}
   High Issues: {hipaa_stats[3] or 0}

FDA 21 CFR PART 11 READINESS CHECKLISTS (Last 30 Days):
   Total Checklist Runs: {fda_stats[0] or 0}
   Systems Fully Satisfied: {fda_stats[1] or 0}

MEDICAL AI GOVERNANCE CHECKLISTS (Last 30 Days):
   AI Systems Assessed: {ai_stats[0] or 0}
   Avg Governance Score: {ai_stats[1] or 0:.1f}%
   Systems Flagged as Possibly Requiring FDA Clearance: {ai_stats[2] or 0}

PHI SECURITY INCIDENTS (Last 30 Days):
   Total Incidents: {incident_stats[0] or 0}
   Affected Records: {incident_stats[1] or 0}
   {'[!] BREACH NOTIFICATION REQUIRED' if incident_stats[1] and incident_stats[1] > 500 else '[OK] No breach notification threshold reached'}

RECOMMENDATIONS:
   {'[!] Address critical HIPAA findings immediately' if hipaa_stats[2] and hipaa_stats[2] > 0 else '✓ No critical HIPAA issues'}
   {'[!] Complete FDA 21 CFR Part 11 gap remediation' if fda_stats[0] and fda_stats[1] and fda_stats[1] < fda_stats[0] else '✓ No FDA 21 CFR Part 11 gaps found (readiness checklist — not a validation)'}
   {'[!] Confirm FDA classification for flagged AI systems' if ai_stats[2] and ai_stats[2] > 0 else '✓ AI systems appropriately screened'}

{'='*80}
"""
        return report


if __name__ == "__main__":
    print("Starting DrMythara Healthcare Compliance Bot...")
    print(DISCLAIMER)
    print(CHECKLIST_LABEL)
    bot = DrMytharaBot()

    # Canonical core consult (real reasoning)
    judgment = bot.consult("hipaa", {"unique_user_id": True, "encryption": True})
    print(f"\n[CORE CONSULT] verdict={judgment.verdict} findings={len(judgment.findings)} "
          f"rules={judgment.rule_versions}")
    print(f"[CORE CONSULT] hash verifies: {verify_judgment(judgment)}")

    # Example: HIPAA self-assessment checklist with caller-supplied answers.
    # Every finding below derives from THESE inputs — change an answer and
    # the finding changes with it.
    hipaa_answers = {c["check"]: True for c in bot.checklist_controls("hipaa")}
    hipaa_answers["auto_logoff"] = False  # the one failing control (caller's input)
    audit_result = bot.audit_hipaa_compliance(
        "Example Healthcare Org", answers=hipaa_answers, scope="full"
    )
    print(f"\n[HIPAA CHECKLIST] Score: {audit_result['overall_score']}% "
          f"({audit_result['controls_answered']} answered, "
          f"{audit_result['controls_unanswered']} unanswered)")
    for f in audit_result["findings"]:
        print(f"   - [{f['severity']}] {f['finding']}")

    # Example: FDA 21 CFR Part 11 readiness checklist with caller answers.
    fda_answers = {c["check"]: True for c in bot.checklist_controls("fda_cfr11")}
    fda_answers["two_factor_signatures"] = False  # failing control (caller's input)
    fda_result = bot.validate_fda_cfr11_compliance(
        "Electronic Health Records System", answers=fda_answers
    )
    print(f"\n[FDA CFR11 CHECKLIST] Overall compliant: {fda_result['overall_compliant']} "
          f"| Gaps: {len(fda_result['gaps'])}")
    for g in fda_result["gaps"]:
        print(f"   - {g}")

    # Example: AI governance checklist — leave one control unanswered to
    # show the UNKNOWN path (never assumed pass or fail).
    ai_answers = {
        "clinical_validation": True,
        "bias_testing": False,  # failing control (caller's input)
        "drift_monitoring": True,
        # "fda_clearance_determined" unanswered -> UNKNOWN advisory
    }
    ai_result = bot.assess_medical_ai_governance(
        "Diagnostic AI System",
        "Radiology image analysis for cancer detection",
        answers=ai_answers,
    )
    print(f"\n[AI GOVERNANCE CHECKLIST] Risk: {ai_result['risk_category']} "
          f"({ai_result['risk_basis']}) | FDA class: {ai_result['fda_device_class']} "
          f"(estimated) | Score: {ai_result['governance_score']}%")
    for f in ai_result["findings"]:
        print(f"   - [{f['severity']}] {f['finding']}")

    # Generate report
    report = bot.generate_compliance_report()
    print(report)

    print("\nDrMythara Healthcare Compliance Bot execution complete.")
