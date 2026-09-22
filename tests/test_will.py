"""Tests for Herb's will (soul_cradle/will.py), the VP's will-gate,
and the two real leaf executors. All must pass."""

import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "Commercial"))

from soul_cradle import will
from soul_cradle.will import ALLOW, ESCALATE, WillError, check, parse_will_md

import proposal_drafter
from proposal_drafter import FabricatedClaimError, ProposalDrafter, pick_template
from outreach_queue import OutreachQueue
from mythara_vp_bot import MytharaVPBot


def _decision(bot_type="proposal_drafter", **over):
    d = {
        "decision_id": "test123",
        "decision_type": "deploy_bot",
        "bot_type": bot_type,
        "reason": "test",
        "spec": {"name": "Test", "purpose": "Draft proposals", "cost_per_month": 0},
        "budget_allocated": 0,
        "deployment_status": "pending",
    }
    d.update(over)
    return d


# ---------------------------------------------------------------------------
# will.check — allow cases
# ---------------------------------------------------------------------------


def test_will_loads_from_will_md():
    w = will.load_will()
    assert "first 5 freelance clients" in w.purpose
    assert "HONEST_CLAIMS_ONLY" in w.constraints
    assert len(w.forbidden) > 5


def test_allow_proposal_drafter():
    verdict, reason = check(_decision("proposal_drafter"))
    assert verdict == ALLOW, reason


def test_allow_outreach_queue():
    verdict, reason = check(_decision("outreach_queue"))
    assert verdict == ALLOW, reason


# ---------------------------------------------------------------------------
# will.check — escalate cases
# ---------------------------------------------------------------------------


def test_escalate_spend_cost():
    d = _decision()
    d["spec"]["cost_per_month"] = 50
    verdict, reason = check(d)
    assert verdict == ESCALATE
    assert "SPEND" in reason


def test_escalate_spend_budget_allocated():
    d = _decision(budget_allocated=100)
    verdict, reason = check(d)
    assert verdict == ESCALATE
    assert "SPEND" in reason


def test_escalate_publish():
    d = _decision("content_marketing_bot", decision_type="publish")
    verdict, reason = check(d)
    assert verdict == ESCALATE
    assert "CONTACT" in reason


def test_escalate_linkedin_contact():
    d = _decision("linkedin_automation_bot")
    verdict, reason = check(d)
    assert verdict == ESCALATE
    assert "CONTACT" in reason


def test_escalate_email_nurture_contact():
    d = _decision("email_nurture_bot")
    verdict, reason = check(d)
    assert verdict == ESCALATE
    assert "CONTACT" in reason


def test_escalate_fabricated_claim():
    d = _decision()
    d["spec"]["purpose"] = "We helped 3 banks pass audits"
    verdict, reason = check(d)
    assert verdict == ESCALATE
    assert "FABRICATED_CLAIM" in reason


def test_escalate_soc2_certified_claim():
    d = _decision()
    d["spec"]["purpose"] = "SOC 2 certified platform"
    verdict, reason = check(d)
    assert verdict == ESCALATE


def test_escalate_new_api():
    d = _decision()
    d["spec"]["requires_api_key"] = True
    verdict, reason = check(d)
    assert verdict == ESCALATE
    assert "NEW_API" in reason


def test_fail_closed_when_will_missing():
    real = will._WILL
    will._WILL = None
    try:
        verdict, reason = check(_decision())
        assert verdict == ESCALATE
        assert "fail closed" in reason
    finally:
        will._WILL = real


def test_parse_missing_file_raises():
    with pytest.raises(WillError):
        parse_will_md(Path("/nonexistent/WILL.md"))


# ---------------------------------------------------------------------------
# VP will-gate
# ---------------------------------------------------------------------------


def test_vp_decision_carries_will_verdict():
    vp = MytharaVPBot()
    d = vp._decide_deploy_bot("proposal_drafter", "test")
    assert d["will_verdict"]["verdict"] == ALLOW
    assert len(d["will_verdict"]["integrity_hash"]) == 16


def test_vp_executes_allowed_decision():
    vp = MytharaVPBot()
    d = vp._decide_deploy_bot("proposal_drafter", "test")
    result = vp.execute_decision(d["decision_id"])
    assert result["status"] == "deployed"
    assert d["deployment_status"] == "deployed"
    assert vp.escalation_queue == []


def test_vp_blocks_escalated_decision():
    vp = MytharaVPBot()
    d = vp._decide_deploy_bot("linkedin_automation_bot", "test")
    assert d["will_verdict"]["verdict"] == ESCALATE
    # snapshot any pre-existing codegen artifact: the will must not rewrite it
    artifact = REPO / "Commercial" / "mythara_linkedin_automation_bot.py"
    before = artifact.read_bytes() if artifact.exists() else None
    result = vp.execute_decision(d["decision_id"])
    assert result["status"] == "escalated"
    assert d["deployment_status"] == "escalated"
    assert len(vp.escalation_queue) == 1
    assert vp.escalation_queue[0]["bot_type"] == "linkedin_automation_bot"
    # never deployed: no codegen written by this decision
    after = artifact.read_bytes() if artifact.exists() else None
    assert before == after
    assert vp.deployed_bots == []


def test_vp_analyze_produces_will_clean_decisions():
    vp = MytharaVPBot()
    analysis = vp.analyze_team_performance()
    assert len(analysis["decisions"]) == 2
    for d in analysis["decisions"]:
        assert d["will_verdict"]["verdict"] == ALLOW, d["will_verdict"]["reason"]


def test_vp_report_renders():
    vp = MytharaVPBot()
    d = vp._decide_deploy_bot("email_nurture_bot", "test")
    vp.execute_decision(d["decision_id"])
    report = vp.generate_vp_report()
    assert "ESCALATED TO HERB" in report
    assert "email_nurture_bot" in report
    assert "Proposals/Month Target" in report


# ---------------------------------------------------------------------------
# Proposal drafter
# ---------------------------------------------------------------------------


def test_pick_template_email():
    assert pick_template("Tame my Gmail inbox", "need email triage") == "email"


def test_pick_template_chatbot():
    assert pick_template("Chatbot for site", "FAQ bot for customers") == "chatbot"


def test_pick_template_compliance():
    assert pick_template("HIPAA review", "health data audit readiness") == "compliance"


def test_pick_template_default_audit():
    assert pick_template("Random gig", "something vague") == "audit"


def test_draft_clean_and_honest():
    d = ProposalDrafter()
    out = d.draft(
        "Need help taming my Gmail inbox",
        "Looking for someone to automate email triage and draft replies.",
        budget="$400",
    )
    assert out["template"] == "email"
    assert "github.com/herbievelezjr/Mythara_Archive" in out["proposal"]
    # no fabricated claims anywhere in the output
    assert will.scan_text(out["proposal"]) is None
    # no invented client names, no metrics
    assert "Western Union" not in out["proposal"]


def test_draft_compliance_keeps_disclaimer():
    d = ProposalDrafter()
    out = d.draft("HIPAA readiness review needed", "small clinic, health data")
    assert out["template"] == "compliance"
    assert "not a lawyer or a certified auditor" in out["proposal"]
    assert "isn't certification" in out["proposal"]


def test_draft_refuses_fabricated_input():
    d = ProposalDrafter()
    with pytest.raises(FabricatedClaimError):
        d.draft(
            "Bank compliance gig",
            "We need someone who helped 3 banks pass audits.",
        )


# ---------------------------------------------------------------------------
# Outreach queue
# ---------------------------------------------------------------------------


def test_queue_writes_pending_draft(tmp_path):
    q = OutreachQueue(queue_dir=tmp_path)
    path = q.queue("proposal", "Test gig", "Draft body here.", meta={"budget": "$400"})
    p = Path(path)
    assert p.exists()
    text = p.read_text()
    assert "PENDING HERB'S APPROVAL" in text
    assert "status: pending_approval" in text
    assert "DO NOT SEND" in text
    pending = q.list_pending()
    assert len(pending) == 1
    assert pending[0]["kind"] == "proposal"


def test_queue_has_no_send_capability():
    q = OutreachQueue(queue_dir=Path("/tmp/will_test_empty"))
    assert not hasattr(q, "send")
    assert not hasattr(q, "publish")
    assert not hasattr(q, "post")
    src = Path(proposal_drafter.__file__).read_text()  # sanity: drafter too
    assert "smtplib" not in src.lower()


def test_queue_rejects_bad_kind(tmp_path):
    q = OutreachQueue(queue_dir=tmp_path)
    with pytest.raises(ValueError):
        q.queue("blast", "x", "y")
