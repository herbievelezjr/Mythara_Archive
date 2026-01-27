#!/usr/bin/env python3
"""Profile imports"""
import sys
import time

# Measure stdlib loads
t0 = time.perf_counter()
import asyncio
import concurrent.futures
import subprocess
import re
import platform
import argparse
t_stdlib = time.perf_counter() - t0
print(f"Standard library imports: {t_stdlib*1000:.1f}ms")

# Now measure sere_bot
t0 = time.perf_counter()
sys.path.insert(0, '.')
import sere_security_system
t_sere = time.perf_counter() - t0
print(f"SERE Bot import: {t_sere*1000:.1f}ms")
print(f"Total: {(t_stdlib + t_sere)*1000:.1f}ms")
