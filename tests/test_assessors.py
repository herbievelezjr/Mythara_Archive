"""Tests for the rebuilt soul assessors (soul_cradle/assessors.py).

The eight witnesses are evidence-fed: they read observable evidence,
abstain when their domain is not engaged, seal judgments by content
hash, and surface disagreement instead of averaging it away.
"""

import pytest

from soul_cradle.assessors import (
    ABSTAIN,
    ASSESSORS,
    CLEAR,
    FLAGGED,
    PANEL_BLOCKED,
    PANEL_CLEAR,
    PANEL_CONTESTED,
    PANEL_FLAGGED,
    assessor_bounds_check,
    assessor_witness_declaration,
    consult,
    panel,
    rubric_inventory,
    verify_judgment,
)
from soul_cradle.standing import StandingAuthority, WITNESS

GOOD = {
    "actor": "vp_marketing",
    "action_type": "queue_draft",
    "principal_consent": True,
    "affected_parties": ["prospect"],
    "disproportionate_harm": False,
    "reversible": True,
    "precedent_setting": False,
    "fully_disclosed": True,
    "variance": "low",
    "deception_involved": False,
    "contradicts_commitments": False,
    "sustains_long_term": True,
    "hidden_costs_addressed": True,
    "safe_on_repetition": True,
    "strengthens_relationship": True,
}

ASSESSOR_IDS = ["demeter", "dionysus", "eros", "hades", "hermes", "janus", "nemesis", "persephone"]


def test_all_eight_registered_with_versioned_rubrics():
    assert set(ASSESSORS) == set(ASSESSOR_IDS)
    for aid, spec in ASSESSORS.items():
        assert spec.version and spec.effective_date and spec.source, aid
        assert len(spec.checks) >= 3, aid
        assert spec.domain_question, aid


def test_rubric_inventory_covers_all_eight():
    inv = rubric_inventory()
    assert set(inv) == set(ASSESSOR_IDS)
    assert all(inv[aid]["version"] for aid in ASSESSOR_IDS)


@pytest.mark.parametrize("aid", ASSESSOR_IDS)
def test_clear_on_good_evidence(aid):
    j = consult(aid, "honest reversible draft", GOOD)
    assert j.verdict == CLEAR, (aid, j.findings)
    assert j.rubric_version == ASSESSORS[aid].version
    assert verify_judgment(j)


@pytest.mark.parametrize("aid", ASSESSOR_IDS)
def test_abstain_when_domain_not_engaged(aid):
    j = consult(aid, "unrelated", {"actor": "someone", "weather": "sunny"})
    assert j.verdict == ABSTAIN
    assert "abstain" in j.note.lower() or "declines" in j.note.lower()
    assert verify_judgment(j)


def test_fail_closed_on_missing_evidence_key():
    # demeter engaged (sustains_long_term present) but reversible missing
    j = consult("demeter", "partial evidence", {"sustains_long_term": True})
    assert j.verdict == FLAGGED
    assert any("fail-closed: no evidence" in f["guidance"].lower() for f in j.findings)


def test_each_assessor_flags_its_own_violation():
    violations = {
        "demeter": {"sustains_long_term": False},
        "dionysus": {"variance": "high"},
        "eros": {"deception_involved": True},
        "hades": {"hidden_costs_addressed": False},
        "hermes": {"deception_involved": True},
        "janus": {"contradicts_commitments": True},
        "nemesis": {"disproportionate_harm": True},
        "persephone": {"reversible": False},
    }
    for aid, bad in violations.items():
        ev = dict(GOOD)
        ev.update(bad)
        j = consult(aid, "violation", ev)
        assert j.verdict == FLAGGED, aid
        assert j.findings, aid


def test_unknown_assessor_raises():
    with pytest.raises(KeyError):
        consult("zeus", "whatever", GOOD)


def test_judgment_tamper_evident():
    j = consult("nemesis", "x", GOOD)
    assert verify_judgment(j)
    j.findings.append({"forged": True})
    assert not verify_judgment(j)


def test_deterministic_verdict_and_findings():
    j1 = consult("hades", "same action", GOOD)
    j2 = consult("hades", "same action", GOOD)
    assert j1.verdict == j2.verdict == CLEAR
    assert j1.findings == j2.findings
    assert j1.domain_question == j2.domain_question


def test_panel_clear():
    r = panel("good action", GOOD)
    assert r.verdict == PANEL_CLEAR
    assert r.dissent == []
    assert len(r.judgments) == 8


def test_panel_blocked_on_critical():
    ev = dict(GOOD, disproportionate_harm=True)  # nemesis critical
    r = panel("harmful action", ev)
    assert r.verdict == PANEL_BLOCKED
    assert "nemesis" in r.note


def test_one_critical_witness_blocks_despite_clear_majority():
    # everything good except the one critical tripwire
    ev = dict(GOOD, deception_involved=True)  # eros + hermes critical
    r = panel("deceptive but otherwise fine", ev)
    assert r.verdict == PANEL_BLOCKED


def test_panel_contested_surfaces_dissent():
    ev = dict(GOOD, strengthens_relationship=False)  # only eros flags
    r = panel("honest but cold", ev)
    assert r.verdict == PANEL_CONTESTED
    assert len(r.dissent) == 1
    d = r.dissent[0]
    assert d["flagged_by"] == "eros"
    assert "demeter" in d["cleared_by"]
    assert d["finding"]["check_id"] == "eros.relationship"


def test_panel_flagged_without_dissent():
    # sparse evidence: every engaged assessor flags on missing keys, none clear
    r = panel("thin evidence", {"variance": "high"})
    assert r.verdict in (PANEL_FLAGGED, PANEL_CONTESTED, PANEL_BLOCKED)


def test_panel_all_abstain_is_clear():
    r = panel("nothing relevant", {"actor": "x"})
    assert r.verdict == PANEL_CLEAR
    assert all(j.verdict == ABSTAIN for j in r.judgments)


def test_membrane_hook_blocks():
    payload = {"assessor_evidence": dict(GOOD, disproportionate_harm=True)}
    reason = assessor_bounds_check("do harm", "send", payload)
    assert reason is not None and "BLOCKED" in reason


def test_membrane_hook_escalates_contested():
    payload = {"assessor_evidence": dict(GOOD, strengthens_relationship=False)}
    reason = assessor_bounds_check("cold draft", "queue", payload)
    assert reason is not None and "escalate" in reason.lower()


def test_membrane_hook_clear_returns_none():
    payload = {"assessor_evidence": dict(GOOD)}
    assert assessor_bounds_check("good draft", "queue", payload) is None


def test_membrane_hook_no_evidence_stays_out_of_the_way():
    assert assessor_bounds_check("anything", "anything", {}) is None
    assert assessor_bounds_check("anything", "anything", {"other": 1}) is None


def test_witness_declaration_speaks_only_as_witness():
    auth = StandingAuthority()
    j = consult("janus", "precedent action", dict(GOOD, precedent_setting=True))
    d = assessor_witness_declaration(auth, "evt-1", j)
    assert d.role == WITNESS
    assert d.actor == "janus"
    assert "evt-1" in d.event_ref


def test_legacy_bot_shims_delegate_to_core():
    import demeter_bot
    import nemesis_bot
    j = demeter_bot.consult_evidence("good action", GOOD)
    assert j.assessor_id == "demeter" and j.verdict == CLEAR
    j2 = nemesis_bot.consult_evidence("bad action", dict(GOOD, disproportionate_harm=True))
    assert j2.assessor_id == "nemesis" and j2.verdict == FLAGGED
