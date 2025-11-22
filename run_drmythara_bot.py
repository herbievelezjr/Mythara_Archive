# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
Runner script for DrMythara Healthcare Compliance Bot
Execute via Windows Task Scheduler: Daily or on-demand
"""

import sys
import os

# Add Commercial directory to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
COMMERCIAL_PATH = os.path.join(CURRENT_DIR, "Commercial")
if COMMERCIAL_PATH not in sys.path:
    sys.path.insert(0, COMMERCIAL_PATH)

from mythara_drmythara_bot import DrMytharaBot

if __name__ == "__main__":
    print("Starting DrMythara Healthcare Compliance Bot...")
    bot = DrMytharaBot()
    
    # Generate compliance report
    report = bot.generate_compliance_report()
    print(report)
    
    print("\nDrMythara Healthcare Compliance Bot execution complete.")
