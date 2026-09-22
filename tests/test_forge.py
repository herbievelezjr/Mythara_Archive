"""Tests for the Hephaestus Forge: governed bonding between bots.

Every test asserts a property of the forge membrane. If any of these
fail, emergence is ungoverned and the forge must not ship.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from soul_cradle.forge import Bond, Compound, Forge, ForgeError
from soul_cradle.identity import (
    GENDER,
    NAME,
    PRONOUNS,
    VOICE_CHARACTER,
    VOICE_GENDER,
    get_identity,
)


@pytest.fixture()
def forge(tmp_path, monkeypatch):
    monkeypatch.setenv("FORGE_AUDIT", str(tmp_path / "forge_audit.jsonl"))
    # Fixed key so bonds verify across instances in-test.
    return Forge(key=b"test-forge-key-32-bytes-long-ok!!")


def allow_all(purpose, participants):
    return None


def deny_all(purpose, participants):
    return "forge is closed for this purpose"


# --- bonds ------------------------------------------------------------------


def test_bond_forges_with_judge_approval(forge):
    bond = forge.forge_bond(["eros", "janus"], "discern the situation", allow_all)
    assert bond.signature
    assert bond.participants == ("eros", "janus")
    ok, reason = forge.verify_bond(bond)
    assert ok, reason


def test_bond_requires_judge(forge):
    with pytest.raises(ForgeError) as exc:
        forge.forge_bond(["eros", "janus"], "discern", None)
    assert "judge" in str(exc.value)


def test_bond_refused_when_judge_denies(forge):
    with pytest.raises(ForgeError) as exc:
        forge.forge_bond(["aries", "hades"], "unsupervised action", deny_all)
    assert "refused" in str(exc.value)


def test_bond_needs_two_distinct_participants(forge):
    with pytest.raises(ForgeError):
        forge.forge_bond(["eros"], "solo", allow_all)
    with pytest.raises(ForgeError):
        forge.forge_bond(["eros", "eros"], "echo", allow_all)
    with pytest.raises(ForgeError):
        forge.forge_bond([], "nothing", allow_all)


def test_bond_needs_purpose(forge):
    with pytest.raises(ForgeError):
        forge.forge_bond(["eros", "janus"], "", allow_all)


def test_tampered_bond_fails_verify(forge):
    bond = forge.forge_bond(["eros", "janus"], "discern", allow_all)
    bond.purpose = "unsupervised action"
    ok, reason = forge.verify_bond(bond)
    assert not ok
    assert "mismatch" in reason


def test_wrong_key_fails_bond_verify(forge):
    bond = forge.forge_bond(["eros", "janus"], "discern", allow_all)
    other = Forge(key=b"a-different-forge-key-32-bytes!")
    ok, _ = other.verify_bond(bond)
    assert not ok


def test_expired_bond_fails_verify(forge):
    bond = forge.forge_bond(["eros", "janus"], "discern", allow_all, ttl_seconds=-1)
    ok, reason = forge.verify_bond(bond)
    assert not ok
    assert "expired" in reason


# --- compounds: emergence with a paper trail --------------------------------


def test_compound_witnessed_from_valid_bond(forge):
    bond = forge.forge_bond(["eros", "janus"], "discern the situation", allow_all)
    compound = forge.forge_compound(bond, "heart-aware situational read")
    assert compound.signature
    assert compound.bond_id == bond.bond_id
    ok, reason = forge.verify_compound(compound)
    assert ok, reason


def test_compound_refused_from_invalid_bond(forge):
    bond = forge.forge_bond(["eros", "janus"], "discern", allow_all)
    bond.purpose = "tampered"
    with pytest.raises(ForgeError):
        forge.forge_compound(bond, "something emerged")


def test_compound_refused_from_expired_bond(forge):
    bond = forge.forge_bond(["eros", "janus"], "discern", allow_all, ttl_seconds=-1)
    with pytest.raises(ForgeError):
        forge.forge_compound(bond, "too late")


def test_compound_judge_can_refuse(forge):
    bond = forge.forge_bond(["eros", "janus"], "discern", allow_all)
    with pytest.raises(ForgeError):
        forge.forge_compound(bond, "dangerous emergence", judge=deny_all)


def test_tampered_compound_fails_verify(forge):
    bond = forge.forge_bond(["eros", "janus"], "discern", allow_all)
    compound = forge.forge_compound(bond, "heart-aware situational read")
    compound.description = "something else entirely"
    ok, _ = forge.verify_compound(compound)
    assert not ok


def test_forge_events_are_audited(forge, tmp_path, monkeypatch):
    audit = tmp_path / "forge_audit.jsonl"
    monkeypatch.setenv("FORGE_AUDIT", str(audit))
    f2 = Forge(key=b"test-forge-key-32-bytes-long-ok!!")
    bond = f2.forge_bond(["eros", "janus"], "discern", allow_all)
    f2.forge_compound(bond, "a new chemical")
    text = audit.read_text()
    assert "bond_forged" in text
    assert "compound_witnessed" in text


# --- identity: who she is ----------------------------------------------------


def test_mythara_is_female():
    assert NAME == "Mythara"
    assert GENDER == "female"
    assert "she" in PRONOUNS and "her" in PRONOUNS


def test_voice_character_is_warm_female():
    assert VOICE_CHARACTER == "warm"
    assert VOICE_GENDER == "female"


def test_get_identity_agrees():
    ident = get_identity()
    assert ident["name"] == "Mythara"
    assert ident["gender"] == "female"
    assert ident["voice_character"] == "warm"
