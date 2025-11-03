# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
Runner for Autonomous Affiliate Marketing Bot.
Processes weekly payouts automatically.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mythara_affiliate_bot import AutonomousAffiliateBot

# Global bot instance (persists across runs)
bot = AutonomousAffiliateBot()

def main():
    print("🤖 Mythara Affiliate Bot - Weekly Payout Run")
    print("="*60)
    
    # Process all pending payouts
    print("\n💰 Processing weekly payouts...")
    payouts = bot.process_weekly_payouts()
    
    if payouts:
        print(f"\n✅ Processed {len(payouts)} payouts:")
        for payout_data in payouts:
            payout = payout_data['payout']
            print(f"\n   Affiliate: {payout['affiliate_email']}")
            print(f"   Amount: ${payout['amount']:.2f}")
            print(f"   Commissions: {len(payout['commissions_included'])}")
            print(f"   Status: {payout['status']}")
    else:
        print("\n✅ No payouts ready (minimum $50 required)")
    
    # Get program stats
    print("\n📊 Affiliate Program Stats:")
    report = bot.get_affiliate_report()
    print(f"   Total Affiliates: {report['total_affiliates']}")
    print(f"   Active Affiliates: {report['active_affiliates']}")
    print(f"   Total Sales Generated: ${report['total_sales_generated']:,.2f}")
    print(f"   Total Commissions Earned: ${report['total_commissions_earned']:,.2f}")
    print(f"   Pending Payouts: ${report['pending_payouts']:,.2f}")
    
    if report['top_affiliates']:
        print("\n🏆 Top Affiliates:")
        for i, aff in enumerate(report['top_affiliates'][:3], 1):
            print(f"   {i}. {aff['name']}: ${aff['earnings']:,.2f}")
    
    print("\n" + "="*60)
    print("✅ Affiliate bot run complete")
    print("💡 Next run: Friday at 5pm")

if __name__ == "__main__":
    main()
