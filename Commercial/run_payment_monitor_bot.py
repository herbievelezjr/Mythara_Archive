# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
Runner script for Payment Monitor Bot.
Checks Loyverse for new payments and alerts on transactions.
"""

import sys
import os

# Add parent directory to path to import mythara_ai_team_free
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mythara_ai_team_free import MytharaAITeam

def main():
    team = MytharaAITeam()
    
    # Run payment monitoring
    print("💰 Running Payment Monitor Bot...")
    result = team.run_payment_monitor()
    
    print("\n" + "="*60)
    print("PAYMENT MONITOR REPORT")
    print("="*60)
    print(result)
    print("="*60)

if __name__ == "__main__":
    main()
