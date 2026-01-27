#!/usr/bin/env python3
"""
Test script to demonstrate S.E.R.E. outbound monitoring capabilities
Shows how S.E.R.E. watches your back while browsing
"""

from sere_security_system import SERESecuritySystem, CONFIG
import time

print("\n" + "="*70)
print("🔍 S.E.R.E. OUTBOUND MONITORING TEST")
print("    Watching Your Back - Monitoring Your Network Activity")
print("="*70)

# Initialize S.E.R.E.
sere = SERESecuritySystem()

print("\n📡 Initializing outbound monitoring...")
print(f"✓ Monitoring active external connections")
print(f"✓ Tracking Tor usage and dark web access")
print(f"✓ Detecting suspicious outbound behavior")
print(f"✓ Watching for malware callbacks")

print("\n🔎 Running threat detection scan...")
print("   (This will detect any active network connections)")

# Run detection
threats = sere.detect_threats()

if threats:
    print(f"\n⚠️  DETECTED {len(threats)} POTENTIAL THREATS:")
    for i, threat in enumerate(threats, 1):
        print(f"\n  [{i}] {threat.attack_type.value}")
        print(f"      Source: {threat.source_ip}")
        print(f"      Severity: {threat.severity.name}")
        print(f"      Indicators:")
        for indicator in threat.indicators:
            print(f"        • {indicator}")
        print(f"      Recommended: {threat.recommended_action}")
else:
    print("\n✅ No threats detected")
    print("   All your network activity appears normal")

print("\n" + "="*70)
print("OUTBOUND MONITORING FEATURES:")
print("="*70)
print("✓ Tracks all external connections (non-local IPs)")
print("✓ Detects Tor usage (ports 9050, 9051, 9150, 9151)")
print("✓ Flags suspicious connection patterns:")
print("  • High volume to single IP (>50 connections)")
print("  • Port scanning behavior (>10 ports)")
print("  • Known malware ports (4444, 5555, 6666, etc.)")
print("✓ Monitors unencrypted protocols (FTP, Telnet)")
print("✓ Watches for potential data exfiltration")
print("✓ Alerts on malware callback attempts")
print("\n💡 TIP: Run 'python sere_bot.py' in patrol mode")
print("   S.E.R.E. will continuously monitor your activity")
print("   and alert you to incoming attacks from sites you visit")
print("="*70 + "\n")
