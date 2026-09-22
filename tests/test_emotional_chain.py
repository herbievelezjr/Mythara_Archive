"""Tests for soul_cradle.emotional_chain — the witnessed emotional record."""

import pytest

from soul_cradle.emotional_chain import (
    EmotionalChain,
    build_evidence,
    coercion_markers,
    OPERATOR_ATTESTATIONS,
)


@pytest.fixture
def chain():
    return EmotionalChain(operator="test")


def test_genesis_verifies(chain):
    ok, details = chain.verify()
    assert ok, details["failures"]
    assert details["records"] == 1


def test_genesis_carries_operator_attestations(chain):
    genesis = chain.chain[0]
    for key in OPERATOR_ATTESTATIONS:
        assert key in genesis.evidence
        assert key in genesis.evidence_bases


def test_clean_self_report_verifies(chain):
    rec = chain.record("alice", "content", 0.5, "Enjoying a quiet evening at home")
    assert rec.panel_verdict == "clear"
    assert rec.verified is True
    # every judgment seal intact
    ok, details = chain.verify()
    assert ok, details["failures"]


def test_every_judgment_has_basis_and_seal(chain):
    rec = chain.record("alice", "happy", 0.7, "Had a great meeting with the team")
    assert len(rec.judgments) == 8
    for j in rec.judgments:
        assert j["integrity_hash"], j["assessor_id"]
        assert j["rubric_version"]
    # every evidence key used by the panel has a stated basis
    for key in rec.evidence:
        assert key in rec.evidence_bases, f"no basis for {key}"


def test_volatile_report_gets_flagged_not_averaged(chain):
    rec = chain.record("bob", "fearful", 0.95, "Threatened with job loss if I don't work weekends")
    assert rec.panel_verdict in ("contested", "flagged")
    assert rec.verified is False
    assert rec.coercion_markers  # heuristic fired and is on the record
    flagged_by = [j["assessor_id"] for j in rec.judgments if j["verdict"] == "flagged"]
    assert "dionysus" in flagged_by  # high variance witnessed
    assert "hades" in flagged_by     # unaddressed harms witnessed
    # dissent preserved, not averaged
    assert rec.dissent


def test_third_party_record_blocked(chain):
    rec = chain.record(
        subject_id="dave", emotion="angry", intensity=0.8,
        context="He seemed furious in the meeting", reporter_id="carol",
    )
    assert rec.panel_verdict == "blocked"
    assert rec.verified is False
    # the entry is kept AND the refusal — the chain journals the block
    ok, _ = chain.verify()
    assert ok
    assert "nemesis" in rec.panel_note


def test_tampered_record_fails_verification(chain):
    chain.record("alice", "happy", 0.7, "Had a great meeting with the team")
    chain.chain[1].emotion = "ecstatic"
    ok, details = chain.verify()
    assert not ok
    assert any("tampered" in f["reason"] for f in details["failures"])


def test_forged_judgment_fails_verification(chain):
    import hashlib, json
    rec = chain.record("alice", "happy", 0.7, "Had a great meeting with the team")
    # Stronger attack: forge a witness judgment, then reseal the record
    # to hide it. The witness's own seal must still catch the forgery.
    rec.judgments[0]["verdict"] = "flagged"
    rec.judgments[0]["integrity_hash"] = "0" * 64
    d = rec.unsigned_dict()
    rec.record_hash = hashlib.sha256(
        json.dumps(d, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()
    ok, details = chain.verify()
    assert not ok
    assert any("forged" in f["reason"] for f in details["failures"])


def test_broken_link_fails_verification(chain):
    chain.record("alice", "happy", 0.7, "Had a great meeting with the team")
    r = chain.chain[1]
    r.prev_hash = "f" * 64
    # reseal so only the link check fires
    import hashlib, json
    d = r.unsigned_dict()
    r.record_hash = hashlib.sha256(
        json.dumps(d, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()
    ok, details = chain.verify()
    assert not ok
    assert any("link broken" in f["reason"] for f in details["failures"])


def test_history_is_per_subject_in_order(chain):
    chain.record("alice", "happy", 0.7, "Had a great meeting with the team")
    chain.record("bob", "sad", 0.4, "Rainy day, nothing major")
    chain.record("alice", "proud", 0.6, "Finished the report early")
    h = chain.history("alice")
    assert [e["emotion"] for e in h] == ["happy", "proud"]
    assert all("record_hash" in e for e in h)


def test_pattern_analysis_labels_itself_heuristic(chain):
    for emo, inten, ctx in [
        ("anxious", 0.95, "Boss said I'm not working hard enough"),
        ("fearful", 0.95, "Threatened with job loss if I don't work weekends"),
    ]:
        chain.record("bob", emo, inten, ctx)
    a = chain.analyze_patterns("bob")
    assert a["concern"] in ("elevated", "moderate")
    assert "not a diagnosis" in a["method"]
    calm = chain.analyze_patterns("alice")
    assert calm["concern"] == "none"


def test_coercion_heuristic_is_labeled():
    assert coercion_markers("Threatened with job loss") == ["threatened"]
    assert coercion_markers("Had a lovely lunch") == []


def test_build_evidence_documents_bases():
    ev, bases = build_evidence("a", "a", "Some substantive context here", 0.5)
    assert ev["principal_consent"] is True
    assert ev["variance"] == "low"
    assert set(ev) == set(bases)
    ev2, _ = build_evidence("a", "b", "He seemed upset today", 0.5)
    assert ev2["principal_consent"] is False
    assert ev2["disproportionate_harm"] is True
