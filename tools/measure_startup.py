#!/usr/bin/env python3
"""
Measure SERE startup and execution times
Copyright © 2025 Herbert Velez Jr. All rights reserved.
"""
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

print("Startup Performance Analysis\n")

# Measure import
t0 = time.perf_counter()
import sere_security_system
t_import = time.perf_counter() - t0
print(f"Import: {t_import*1000:.1f}ms")

# Measure init
t0 = time.perf_counter()
bot = sere_bot.SERESecuritySystem()
t_init = time.perf_counter() - t0
print(f"Initialization: {t_init*1000:.1f}ms")

# Measure drill
t0 = time.perf_counter()
bot.full_sere_drill()
t_drill = time.perf_counter() - t0
print(f"Drill: {t_drill*1000:.1f}ms")

total = t_import + t_init + t_drill
print(f"\nTotal: {total*1000:.1f}ms ({total:.2f}s)")
