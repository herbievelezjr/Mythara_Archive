#!/usr/bin/env python3
"""
Quick test: real-time geolocation display
Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import sere_security_system

bot = sere_bot.SERESecuritySystem()

ip = '8.8.8.8'
print(f"\n[TEST] Adding ping target {ip}...")
bot.add_ping_target(ip)
print("[TEST] Displaying ping report (should include geolocation)...")
bot._display_ping_report()

print("\n[TEST] Direct geolocation lookup...")
geo = bot.get_ip_geolocation(ip)
if geo:
    print(f"📍 {geo.city}, {geo.region}, {geo.country} | 🏢 {geo.org} | 🌐 {geo.loc}")
else:
    print("✗ Geolocation lookup unavailable")
