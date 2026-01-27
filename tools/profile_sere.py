#!/usr/bin/env python3
"""
GitHub Copilot Profiler Harness for S.E.R.E. Bot

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

Profiles sere_bot.py to identify CPU and memory hotspots.
Outputs: tests/output/sere_profile.prof and tests/output/sere_profile.txt
"""

import os
import sys
import time
import tracemalloc
import cProfile
import pstats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / 'tests' / 'output'
OUT_DIR.mkdir(parents=True, exist_ok=True)
PROF_PATH = OUT_DIR / 'sere_profile.prof'
REPORT_PATH = OUT_DIR / 'sere_profile.txt'


def run_demo_profile():
    # Ensure repo root is on sys.path for imports
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    # Import module and run core operations directly (no CLI demo)
    import sere_security_system

    tracemalloc.start()
    t0 = time.perf_counter()

    profile = cProfile.Profile()
    profile.enable()
    try:
        # Run drill directly and a short detection cycle
        bot = sere_bot.SERESecuritySystem()
        bot.full_sere_drill()
        # Minimal extra exercise without sleeping
        threats = bot.detect_threats()
        if threats:
            bot.execute_evasion(threats)
        bot.display_status()
    finally:
        profile.disable()
    elapsed = time.perf_counter() - t0

    # Save .prof
    profile.dump_stats(str(PROF_PATH))

    # Build text report
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    with REPORT_PATH.open('w', encoding='utf-8') as f:
        f.write(f"SERE Profiling Report\n")
        f.write(f"Elapsed: {elapsed:.3f}s\n")
        f.write(f"Profile file: {PROF_PATH}\n\n")

        f.write("Top CPU hotspots (cumtime):\n")
        ps = pstats.Stats(profile)
        ps.sort_stats('cumtime')
        # Capture top 30 lines
        ps.dump_stats(str(PROF_PATH))
        # Print to file
        ps_stream = []
        ps.print_stats(30)
        # Unfortunately print_stats goes to stdout; re-run with a stream
        import io as _io
        _s = _io.StringIO()
        ps = pstats.Stats(profile, stream=_s)
        ps.sort_stats('cumtime').print_stats(30)
        f.write(_s.getvalue())

        f.write("\nTop memory allocations:\n")
        for idx, stat in enumerate(top_stats[:20], start=1):
            f.write(f"{idx:2d}. {stat}\n")

    return elapsed


if __name__ == '__main__':
    try:
        e = run_demo_profile()
        print(f"Profile complete in {e:.3f}s")
        print(f"- Stats: {PROF_PATH}")
        print(f"- Report: {REPORT_PATH}")
    except SystemExit as se:
        # sere_bot.main() returns 0 and calls sys.exit
        print(f"Exited sere_bot with code: {se.code}")
        print(f"- Stats: {PROF_PATH}")
        print(f"- Report: {REPORT_PATH}")
    except Exception as ex:
        print(f"Profiling failed: {ex}")
        raise
