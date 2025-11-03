# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
Runner script for Mythara Support Chat Bot
Execute via Windows Task Scheduler: Every 30 minutes
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.source_proprietary.mythara_support_bot import MytharaSupportBot

if __name__ == "__main__":
    print("Starting Mythara Support Bot...")
    bot = MytharaSupportBot()
    
    # Check for new tickets and respond
    report = bot.generate_support_report()
    print(report)
    
    print("\nMythara Support Bot execution complete.")
