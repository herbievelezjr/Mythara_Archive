# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
Runner script for Mythara HR VP
Execute via Windows Task Scheduler: Weekly Monday 8:00 AM
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.source_proprietary.mythara_hr_vp import MytharaHRVP

if __name__ == "__main__":
    print("Starting Mythara HR VP...")
    vp = MytharaHRVP()
    
    # Generate weekly HR report
    report = vp.generate_hr_report()
    print(report)
    
    print("\nMythara HR VP execution complete.")
