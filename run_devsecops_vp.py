# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
Runner script for Mythara DevSecOps VP
Execute via Windows Task Scheduler: Hourly
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.source_proprietary.mythara_devsecops_vp import MytharaDevSecOpsVP

if __name__ == "__main__":
    print("Starting Mythara DevSecOps VP...")
    vp = MytharaDevSecOpsVP()
    
    # Generate security report
    report = vp.generate_devsecops_report()
    print(report)
    
    print("\nMythara DevSecOps VP execution complete.")
