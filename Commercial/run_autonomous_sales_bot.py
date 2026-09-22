# Copyright © 2025 Herbert Velez Jr. All rights reserved.

"""
Runner script for Autonomous Sales Bot.
Fully automated sales - zero human contact.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mythara_ai_team_free import MytharaAITeam

def main():
    team = MytharaAITeam()
    
    # Example prospect list (replace with real data)
    prospects = [
        {
            'email': 'cro@bank.com',
            'name': 'Chief Risk Officer',
            'company': 'Regional Bank',
            'industry': 'Banking'
        },
        {
            'email': 'cto@healthtech.com',
            'name': 'CTO',
            'company': 'HealthTech Inc',
            'industry': 'Healthcare'
        },
        {
            'email': 'ai-lead@saas.com',
            'name': 'Head of AI',
            'company': 'SaaS Company',
            'industry': 'Technology'
        }
    ]
    
    # Run autonomous sales
    print("🤖 Running Autonomous Sales Bot...")
    result = team.run_autonomous_sales(prospects)
    
    print("\n" + "="*60)
    print("AUTONOMOUS SALES REPORT")
    print("="*60)
    print(result)
    print("="*60)
    
    print("\n💡 Bot sends emails automatically")
    print("💡 Tracks engagement via Mythara Blessings Reservoir")
    print("💡 Auto-sends invoices when prospects qualified")
    print("💡 Zero human contact required")

if __name__ == "__main__":
    main()
