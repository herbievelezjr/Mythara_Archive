"""Tests for the Aries plating: signed Soul Cradle authorization.

Every test asserts a security property of the membrane. If any of these
fail, Aries must not ship.
"""

import os
import sys
import time

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from soul_cradle.authorization import (
    ActionEnvelope,
    AuthorizationError,
    SoulCradleAuthority,
    action_types,
    register_handler,
)
from aries_bot import AriesBot, Action, ActionPriority, ActionStatus, ExecutionMode


@pytest.fixture()
def authority():
    # Fixed key so envelopes verify across instances in-test.
    return SoulCradleAuthority(key=b"test-key-32-bytes-long-for-tests!!")


@pytest.fixture()
def bot(authority):
    return AriesBot(authority=authority)


def make_action(
    bot,
    authority,
    action_type="emit_text",
    payload=None,
    issuer="olympus_council",
    purpose="test",
    **kw
):
    payload = {"text": "hello"} if payload is None else payload
    env = authority.authorize(action_type, payload, issuer=issuer, purpose=purpose)
    return bot.create_action("test action", env, payload, **kw)


# --- the membrane ----------------------------------------------------------


def test_valid_envelope_executes(bot, authority):
    action = make_action(bot, authority)
    assert bot.execute_action(action) is True
    assert action.status == ActionStatus.COMPLETED
    assert action.result == "hello"


def test_missing_envelope_blocked_not_executed(bot):
    action = Action(
        action_id="x",
        description="naked",
        envelope=None,
        payload={},
        priority=ActionPriority.CRITICAL,
    )
    assert bot.execute_action(action) is False
    assert action.status == ActionStatus.BLOCKED
    assert action.attempts == 0  # never attempted, let alone retried


def test_forged_signature_blocked(bot, authority):
    action = make_action(bot, authority)
    action.envelope.signature = "0" * 64
    assert bot.execute_action(action) is False
    assert action.status == ActionStatus.BLOCKED


def test_tampered_payload_blocked(bot, authority):
    action = make_action(bot, authority, payload={"text": "original"})
    action.payload = {"text": "EVIL - payload swapped after signing"}
    assert bot.execute_action(action) is False
    assert action.status == ActionStatus.BLOCKED


def test_expired_envelope_blocked(bot, authority):
    env = authority.authorize(
        "emit_text",
        {"text": "stale"},
        issuer="olympus_council",
        purpose="test",
        ttl_seconds=-1,
    )
    action = bot.create_action("stale", env, {"text": "stale"})
    assert bot.execute_action(action) is False
    assert action.status == ActionStatus.BLOCKED


def test_unauthorized_issuer_blocked_at_authorize(authority):
    with pytest.raises(AuthorizationError):
        authority.authorize(
            "write_report",
            {"filename": "x", "content": "y"},
            issuer="untrusted_bot",
            purpose="test",
        )


def test_issuer_permitted_for_one_type_not_another(authority, bot):
    # self_test may emit_text but not write_report
    env = authority.authorize(
        "emit_text", {"text": "ok"}, issuer="self_test", purpose="test"
    )
    action = bot.create_action("ok", env, {"text": "ok"})
    assert bot.execute_action(action) is True

    with pytest.raises(AuthorizationError):
        authority.authorize(
            "write_report",
            {"filename": "x", "content": "y"},
            issuer="self_test",
            purpose="test",
        )


def test_unknown_action_type_refused(authority):
    with pytest.raises(AuthorizationError):
        authority.authorize(
            "delete_everything", {}, issuer="soul_cradle", purpose="test"
        )


def test_raw_string_command_refused_at_creation(bot):
    with pytest.raises(AuthorizationError):
        bot.create_action("old style", "shell:rm -rf /", {})  # type: ignore


def test_aggressive_mode_still_requires_authorization(bot):
    naked = Action(
        action_id="y",
        description="naked aggressive",
        envelope=None,
        payload={},
        priority=ActionPriority.CRITICAL,
    )
    plan = bot.execute_plan("aggressive test", [naked], ExecutionMode.AGGRESSIVE)
    assert plan.completed_actions == 0
    assert naked.status == ActionStatus.BLOCKED


def test_bounds_check_refusal_blocks_issuance(authority):
    authority.set_bounds_check(
        lambda purpose, action_type, payload: (
            "test refusal" if "forbidden" in purpose else None
        )
    )
    with pytest.raises(AuthorizationError):
        authority.authorize(
            "emit_text",
            {"text": "x"},
            issuer="olympus_council",
            purpose="this is forbidden",
        )


# --- handler sandbox -------------------------------------------------------


def test_write_report_path_traversal_refused(bot, authority, tmp_path, monkeypatch):
    monkeypatch.setenv("ARIES_OUT_DIR", str(tmp_path))
    env = authority.authorize(
        "write_report",
        {"filename": "../escape.txt", "content": "evil"},
        issuer="olympus_council",
        purpose="test",
    )
    action = bot.create_action(
        "traversal", env, {"filename": "../escape.txt", "content": "evil"}
    )
    assert bot.execute_action(action) is False
    assert not (tmp_path.parent / "escape.txt").exists()


def test_write_report_absolute_path_refused(bot, authority, tmp_path, monkeypatch):
    monkeypatch.setenv("ARIES_OUT_DIR", str(tmp_path))
    payload = {"filename": "/tmp/aries_escape.txt", "content": "evil"}
    env = authority.authorize(
        "write_report", payload, issuer="olympus_council", purpose="test"
    )
    action = bot.create_action("abs", env, payload)
    assert bot.execute_action(action) is False
    assert not os.path.exists("/tmp/aries_escape.txt")


def test_write_report_happy_path(bot, authority, tmp_path, monkeypatch):
    monkeypatch.setenv("ARIES_OUT_DIR", str(tmp_path))
    payload = {"filename": "reports/r1.txt", "content": "report body"}
    env = authority.authorize(
        "write_report", payload, issuer="olympus_council", purpose="test"
    )
    action = bot.create_action("write", env, payload)
    assert bot.execute_action(action) is True
    assert (tmp_path / "reports" / "r1.txt").read_text() == "report body"


# --- cross-instance verification (key sharing) ------------------------------


def test_envelope_verifies_across_instances():
    key = b"shared-key-32-bytes-long-shared-key!"
    issuer = SoulCradleAuthority(key=key)
    verifier = SoulCradleAuthority(key=key)
    bot = AriesBot(authority=verifier)
    env = issuer.authorize(
        "emit_text", {"text": "cross"}, issuer="olympus_council", purpose="test"
    )
    action = bot.create_action("cross", env, {"text": "cross"})
    assert bot.execute_action(action) is True


def test_wrong_key_does_not_verify():
    issuer = SoulCradleAuthority(key=b"key-one-32-bytes-long-key-one!!!!!")
    verifier = SoulCradleAuthority(key=b"key-two-32-bytes-long-key-two!!!!!")
    bot = AriesBot(authority=verifier)
    env = issuer.authorize(
        "emit_text", {"text": "cross"}, issuer="olympus_council", purpose="test"
    )
    action = bot.create_action("cross", env, {"text": "cross"})
    assert bot.execute_action(action) is False
    assert action.status == ActionStatus.BLOCKED


def test_registered_action_types_are_safe_only():
    # The only things Aries can ever run. If this set grows, it grows
    # through code review, and this test documents the current set.
    assert set(action_types()) == {"emit_text", "write_report"}
