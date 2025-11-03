# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
Runner script for Mythara Accounting VP
Execute via Windows Task Scheduler: Daily 11:00 AM
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.source_proprietary.mythara_accounting_vp import MytharaAccountingVP

if __name__ == "__main__":
    print("Starting Mythara Accounting VP...")
    vp = MytharaAccountingVP()
    
    # Generate daily accounting report
    report = vp.generate_accounting_report()
    print(report)
    
    print("\nMythara Accounting VP execution complete.")
