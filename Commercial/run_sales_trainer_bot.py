import os
# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
Sales Trainer Bot Runner - Runs every 6 hours
Analyzes conversations, updates Sales Bot tactics

UPDATED: Now uses Google Gemini (FREE) instead of OpenAI
Get your free API key: https://ai.google.dev/
# QUICKFIX FIX: Moved to environment variable (CWE-798)
GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY", "")  # Set via environment
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Use FREE version (no API needed)
from mythara_ai_team_free import SalesTrainerBot
from datetime import datetime

# Check for Google AI API key
GOOGLE_AI_API_KEY = os.getenv('GOOGLE_AI_API_KEY')
if not GOOGLE_AI_API_KEY:
    print("⚠️  Warning: GOOGLE_AI_API_KEY not set. Bot will run in rule-based mode.")
    print("   Get free API key: https://ai.google.dev/")
    # QUICKFIX FIX: Moved to environment variable (CWE-798)
    GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY", "")  # Set via environment
    print("")

def run_sales_trainer_bot():
    """Execute Sales Trainer Bot tasks."""
    print(f"🎓 SALES TRAINER BOT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    bot = SalesTrainerBot()
    
    # Simulate conversation analysis (in production, reads from database)
    print("\n📊 Analyzing last 30 days of conversations...")
    
    sample_conversations = [
        {
            "id": "conv_001",
            "outcome": "closed",
            "messages": ["We can help you save 6 weeks", "That sounds great!", "$2,500", "Let's do it"],
            "tactics_used": ["urgency", "competitive_pressure"]
        },
        {
            "id": "conv_002",
            "outcome": "lost",
            "messages": ["Only $500", "Too cheap, seems sketchy", "We have great ROI", "No thanks"],
            "tactics_used": ["discount_language"]
        },
        {
            "id": "conv_003",
            "outcome": "closed",
            "messages": ["Your competitors are using this", "Really? Who?", "Western Union", "I'm interested"],
            "tactics_used": ["competitive_pressure", "social_proof"]
        }
    ]
    
    print(f"\n🔍 Conversations analyzed: {len(sample_conversations)}")
    
    for conv in sample_conversations:
        analysis = bot.analyze_conversation(conv)
        if analysis.get("lessons"):
            print(f"\n   Conversation {conv['id']} ({conv['outcome']}):")
            for lesson in analysis["lessons"]:
                print(f"      ✓ {lesson['pattern']}: {lesson['recommendation']}")
    
    # Generate training update
    print("\n🚀 Generating training update...")
    training_update = bot.generate_training_update(sample_conversations)
    
    if training_update["tactics_to_amplify"]:
        print(f"\n   ✅ Tactics to AMPLIFY:")
        for tactic in training_update["tactics_to_amplify"]:
            print(f"      • {tactic['tactic']}: {tactic['reason']}")
    
    if training_update["tactics_to_retire"]:
        print(f"\n   ❌ Tactics to RETIRE:")
        for tactic in training_update["tactics_to_retire"]:
            print(f"      • {tactic['tactic']}: {tactic['reason']}")
    
    if training_update["new_tactics_to_test"]:
        print(f"\n   🧪 New A/B Tests:")
        for tactic in training_update["new_tactics_to_test"]:
            print(f"      • {tactic['tactic']}: {tactic['hypothesis']}")
    
    # Update Sales Bot
    print("\n📝 Pushing updates to Sales Bot with Soul...")
    bot.update_sales_bot_tactics(training_update)
    
    print("\n✅ Sales Trainer Bot run complete")
    print(f"   Next run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} + 6 hours")

if __name__ == "__main__":
    run_sales_trainer_bot()
