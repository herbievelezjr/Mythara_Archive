# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
Runner script for DrMythara Medical Team Suite
Execute via Windows Task Scheduler or manually
Orchestrates all essential and non-essential medical bots
"""

import sys
import os

# Add Commercial directory to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
COMMERCIAL_PATH = os.path.join(CURRENT_DIR, "Commercial")
if COMMERCIAL_PATH not in sys.path:
    sys.path.insert(0, COMMERCIAL_PATH)

from mythara_medical_team_suite import MedicalTeamSuite
import json
from datetime import datetime

def print_banner():
    """Print startup banner"""
    print("\n" + "="*80)
    print("🏥 DrMythara Medical Team Suite - Healthcare Bot Orchestration")
    print("="*80)
    print("\nCRITICAL DISCLAIMER:")
    print("- NO MEDICAL ADVICE PROVIDED")
    print("- NO DIAGNOSTIC CAPABILITIES")
    print("- ADMINISTRATIVE & COMPLIANCE SUPPORT ONLY")
    print("- NOT A SUBSTITUTE FOR MEDICAL PROFESSIONALS")
    print("="*80 + "\n")

def print_section(title):
    """Print section header"""
    print("\n" + "-"*80)
    print(f"📋 {title}")
    print("-"*80)

if __name__ == "__main__":
    print_banner()
    
    print(f"⏰ Execution Time: {datetime.utcnow().isoformat()}")
    print("🚀 Initializing Medical Team Suite...\n")
    
    # Initialize suite
    suite = MedicalTeamSuite()
    
    # Generate comprehensive status report
    print_section("GENERATING SUITE STATUS REPORT")
    report = suite.generate_suite_report()
    
    # Pretty print report
    print("\n📊 Essential Bots Status:")
    for bot_name, bot_status in report["essential_bots"].items():
        status_symbol = "✅" if bot_status.get("operational") else "❌"
        print(f"  {status_symbol} {bot_name.replace('_', ' ').title()}")
        if "active_cases_by_urgency" in bot_status:
            print(f"     Active cases: {bot_status['active_cases_by_urgency']}")
        if "unsigned_notes_pending" in bot_status:
            print(f"     Unsigned notes: {bot_status['unsigned_notes_pending']}")
        if "active_alerts_by_severity" in bot_status:
            print(f"     Active alerts: {bot_status['active_alerts_by_severity']}")
    
    print("\n📊 Support Bots Status:")
    for bot_name, bot_status in report["support_bots"].items():
        status_symbol = "✅" if bot_status.get("operational") else "❌"
        print(f"  {status_symbol} {bot_name.replace('_', ' ').title()}")
        if "todays_appointments" in bot_status:
            print(f"     Today's appointments: {bot_status['todays_appointments']}")
    
    print("\n📊 Overall Suite Health:")
    health = report["overall_health"]
    print(f"  Active triage cases: {health['active_triage_cases']}")
    print(f"  Unresolved compliance alerts: {health['unresolved_compliance_alerts']}")
    print(f"  Today's scheduled appointments: {health['todays_scheduled_appointments']}")
    print(f"  Suite operational: {'✅ YES' if health['suite_operational'] else '❌ NO'}")
    
    print_section("REPORT INTEGRITY")
    print(f"  SHA-256 Hash: {report['integrity_hash'][:32]}...")
    print(f"  Report Time: {report['report_time']}")
    
    # Save report to file
    report_filename = f"medical_team_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Full report saved to: {report_filename}")
    
    print("\n" + "="*80)
    print("✅ DrMythara Medical Team Suite execution complete")
    print("="*80 + "\n")
