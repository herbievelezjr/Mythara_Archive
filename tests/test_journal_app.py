"""Smoke tests for the journal app server: persistence round-trip."""

import importlib.util
import os


def _load_server():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "journal_app", "server.py")
    spec = importlib.util.spec_from_file_location("journal_server", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_persistence_round_trip(tmp_path):
    srv = _load_server()
    srv.DATA_FILE = str(tmp_path / "chain.json")
    srv.chain.record("zed", "calm", 0.4, "Testing persistence round trip here")
    srv._save()
    assert os.path.exists(srv.DATA_FILE)

    srv2 = _load_server()
    srv2.DATA_FILE = str(tmp_path / "chain.json")
    srv2._load()
    ok, details = srv2.chain.verify()
    assert ok, details["failures"]
    assert len(srv2.chain.chain) == len(srv.chain.chain)
    assert srv2.chain.chain[-1].record_hash == srv.chain.chain[-1].record_hash
    assert srv2.chain._prior_intensity["zed"] == 0.4


def test_handler_routes_exist():
    srv = _load_server()
    assert hasattr(srv.Handler, "do_POST")
    assert hasattr(srv.Handler, "do_GET")
