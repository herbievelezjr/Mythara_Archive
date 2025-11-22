#!/usr/bin/env python3
"""
Run QuickFix Bot in auto-fix mode
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from quickfix_bot import QuickFixBot

print("""
╔═══════════════════════════════════════════════════════════╗
║              🔧 QUICKFIX BOT - AUTO-FIX MODE 🔧           ║
╚═══════════════════════════════════════════════════════════╝
""")

# Initialize and run
quickfix = QuickFixBot(os.getcwd())

# Scan
print("🔍 Scanning for vulnerabilities...")
vulnerabilities = quickfix.scan_for_vulnerabilities()

if not vulnerabilities:
    print("✅ No vulnerabilities found!")
    sys.exit(0)

print(f"\n⚠️  Found {len(vulnerabilities)} vulnerabilities")

# Group by severity
critical = [v for v in vulnerabilities if v.severity == "CRITICAL"]
high = [v for v in vulnerabilities if v.severity == "HIGH"]
medium = [v for v in vulnerabilities if v.severity == "MEDIUM"]
low = [v for v in vulnerabilities if v.severity == "LOW"]

print(f"  CRITICAL: {len(critical)}")
print(f"  HIGH: {len(high)}")
print(f"  MEDIUM: {len(medium)}")
print(f"  LOW: {len(low)}")

# Auto-fix CRITICAL and HIGH
print("\n🔧 Auto-fixing CRITICAL and HIGH severity issues...")
fixes = quickfix.fix_all_vulnerabilities(severity_threshold="HIGH")

successful = [f for f in fixes if f.fix_applied]
print(f"✅ Successfully fixed {len(successful)}/{len(fixes)} vulnerabilities")

# Save report
print("\n📄 Generating report...")
report_path = quickfix.save_report()

# Display report
print("\n" + quickfix.generate_report())

print("\n🎯 QuickFix Mission Complete!")
print(f"📄 Full report: {report_path}")
print(f"💾 Backups stored in: .quickfix_backups/")
