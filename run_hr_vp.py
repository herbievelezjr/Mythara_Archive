# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
Runner script for Mythara HR VP
Execute via Windows Task Scheduler: Weekly Monday 8:00 AM
"""

import sys
import os

# Add Commercial directory to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
COMMERCIAL_PATH = os.path.join(CURRENT_DIR, "Commercial")
if COMMERCIAL_PATH not in sys.path:
    sys.path.insert(0, COMMERCIAL_PATH)

from mythara_hr_vp import MytharaHRVP

if __name__ == "__main__":
    print("Starting Mythara HR VP...")
    vp = MytharaHRVP()
    
    # Generate weekly HR report
    report = vp.generate_hr_report()
    print(report)
    
    print("\nMythara HR VP execution complete.")
