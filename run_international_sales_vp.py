# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
Runner script for Mythara International Sales VP
Execute via Windows Task Scheduler: Daily 9:00 AM
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.source_proprietary.mythara_international_sales_vp import MytharaInternationalSalesVP

if __name__ == "__main__":
    print("Starting Mythara International Sales VP...")
    vp = MytharaInternationalSalesVP()
    
    # Generate daily international sales report
    report = vp.generate_international_report()
    print(report)
    
    print("\nMythara International Sales VP execution complete.")
