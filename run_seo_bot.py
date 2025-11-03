# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
Runner script for Mythara SEO Master Bot
Execute via Windows Task Scheduler: Weekly Sunday 12:00 AM
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.source_proprietary.mythara_seo_bot import MytharaSEOBot

if __name__ == "__main__":
    print("Starting Mythara SEO Master Bot...")
    bot = MytharaSEOBot()
    
    # Generate weekly SEO report
    report = bot.generate_seo_report()
    print(report)
    
    print("\nMythara SEO Master Bot execution complete.")
