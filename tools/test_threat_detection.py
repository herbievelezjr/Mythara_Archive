#!/usr/bin/env python3
"""Test threat detection on Tor/vulnerable connections"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import sere_security_system

print("Testing real threat detection...\n")
bot = sere_bot.SERESecuritySystem()
threats = bot.detect_threats()

print(f"Threats detected: {len(threats)}\n")
for threat in threats[:10]:
    print(f"  Type: {threat.attack_type.value}")
    print(f"  Source: {threat.source_ip}")
    print(f"  Indicators: {threat.indicators}")
    print(f"  Severity: {threat.severity.name}")
    print(f"  Action: {threat.recommended_action}\n")

if not threats:
    print("No network threats detected (system is clean)")
