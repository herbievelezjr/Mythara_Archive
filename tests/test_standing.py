"""Tests for moral standing: trespass, forgiveness, repentance.

Every test asserts a property of the standing membrane. If any of these
fail, the judgment layer must not ship.
"""

import os
import sys
import time

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from soul_cradle.standing import (
    DECLARE_FORGIVENESS,
    DECLARE_REPENTANCE,
    DECLARE_TRESPASS,
    WITNESS_STATEMENT,
    STRANGER,
    TRESPASSER,
    WITNESS,
    WRONGED,
    StandingAuthority,
    StandingError,
    evaluate_standing,
)


@pytest.fixture()
def authority(tmp_path, monkeypatch):
    monkeypatch.setenv("STANDING_AUDIT", str(tmp_path / "standing_audit.jsonl"))
    # Fixed key so declarations verify across instances in-test.
    return StandingAuthority(key=b"test-standing-key-32-bytes-long!!")


# --- structural law: the role x declaration matrix --------------------------


def test_wronged_declares_trespass():
    ok, _ = evaluate_standing(WRONGED, DECLARE_TRESPASS, "evt-1")
    assert ok


def test_wronged_forgives():
    ok, _ = evaluate_standing(WRONGED, DECLARE_FORGIVENESS, "evt-1")
    assert ok


def test_wronged_cannot_repent():
    ok, reason = evaluate_standing(WRONGED, DECLARE_REPENTANCE, "evt-1")
    assert not ok
    assert "no standing" in reason


def test_trespasser_repents_own_trespass():
    ok, _ = evaluate_standing(TRESPASSER, DECLARE_REPENTANCE, "evt-1")
    assert ok


def test_trespasser_cannot_declare_trespass():
    ok, _ = evaluate_standing(TRESPASSER, DECLARE_TRESPASS, "evt-1")
    assert not ok


def test_trespasser_cannot_forgive():
    ok, _ = evaluate_standing(TRESPASSER, DECLARE_FORGIVENESS, "evt-1")
    assert not ok


def test_witness_states_only_what_observed():
    ok, _ = evaluate_standing(WITNESS, WITNESS_STATEMENT, "evt-1", {"observed": True})
    assert ok
    ok, reason = evaluate_standing(WITNESS, WITNESS_STATEMENT, "evt-1", {"observed": False})
    assert not ok
    assert "observed" in reason


def test_witness_cannot_declare_trespass():
    ok, _ = evaluate_standing(WITNESS, DECLARE_TRESPASS, "evt-1")
    assert not ok


def test_stranger_declares_nothing():
    for dtype in (DECLARE_TRESPASS, DECLARE_FORGIVENESS, DECLARE_REPENTANCE, WITNESS_STATEMENT):
        ok, _ = evaluate_standing(STRANGER, dtype, "evt-1")
        assert not ok, f"stranger must never declare {dtype}"


def test_standing_requires_event_ref():
    ok, reason = evaluate_standing(WRONGED, DECLARE_TRESPASS, "")
    assert not ok
    assert "event" in reason


def test_unknown_role_and_type_rejected():
    ok, _ = evaluate_standing("king", DECLARE_TRESPASS, "evt-1")
    assert not ok
    ok, _ = evaluate_standing(WRONGED, "declare_war", "evt-1")
    assert not ok


# --- issuance: signed, timestamped, auditable --------------------------------


def test_valid_declaration_issues_and_verifies(authority):
    decl = authority.declare(
        DECLARE_TRESPASS, actor="eros", role=WRONGED,
        event_ref="evt-1", statement="My boundary was crossed.",
    )
    assert decl.signature
    ok, reason = authority.verify(decl)
    assert ok, reason


def test_declaration_without_standing_refused(authority):
    with pytest.raises(StandingError):
        authority.declare(
            DECLARE_FORGIVENESS, actor="hades", role=TRESPASSER,
            event_ref="evt-1", statement="I forgive you.",
        )


def test_stranger_declaration_refused(authority):
    with pytest.raises(StandingError):
        authority.declare(
            DECLARE_TRESPASS, actor="mallory", role=STRANGER,
            event_ref="evt-1", statement="On behalf of someone else.",
        )


def test_tampered_declaration_fails_verify(authority):
    decl = authority.declare(
        DECLARE_REPENTANCE, actor="hades", role=TRESPASSER,
        event_ref="evt-1", statement="I was wrong.",
    )
    decl.statement = "I was right actually."
    ok, reason = authority.verify(decl)
    assert not ok
    assert "mismatch" in reason


def test_expired_declaration_fails_verify(authority):
    decl = authority.declare(
        WITNESS_STATEMENT, actor="janus", role=WITNESS,
        event_ref="evt-1", statement="I saw it happen.",
        scope={"observed": True}, ttl_seconds=-1,
    )
    ok, reason = authority.verify(decl)
    assert not ok
    assert "expired" in reason


def test_wrong_key_fails_verify(authority, tmp_path, monkeypatch):
    decl = authority.declare(
        DECLARE_TRESPASS, actor="eros", role=WRONGED,
        event_ref="evt-1", statement="My boundary was crossed.",
    )
    other = StandingAuthority(key=b"a-different-test-key-32-bytes-ok!")
    ok, _ = other.verify(decl)
    assert not ok


def test_credibility_check_can_refuse_role(authority):
    authority.set_credibility_check(
        lambda actor, role, event_ref, scope: "actor not party to event"
        if actor == "impostor" else None
    )
    with pytest.raises(StandingError) as exc:
        authority.declare(
            DECLARE_TRESPASS, actor="impostor", role=WRONGED,
            event_ref="evt-1", statement="Trust me.",
        )
    assert "credibility" in str(exc.value)


def test_credibility_check_pass_through(authority):
    authority.set_credibility_check(lambda a, r, e, s: None)
    decl = authority.declare(
        DECLARE_TRESPASS, actor="eros", role=WRONGED,
        event_ref="evt-1", statement="My boundary was crossed.",
    )
    ok, _ = authority.verify(decl)
    assert ok


def test_denials_are_audited(authority, tmp_path, monkeypatch):
    audit = tmp_path / "standing_audit.jsonl"
    monkeypatch.setenv("STANDING_AUDIT", str(audit))
    auth2 = StandingAuthority(key=b"test-standing-key-32-bytes-long!!")
    with pytest.raises(StandingError):
        auth2.declare(DECLARE_TRESPASS, actor="x", role=STRANGER,
                      event_ref="e", statement="s")
    lines = audit.read_text().strip().split("\n")
    assert any("declare_denied" in line for line in lines)
