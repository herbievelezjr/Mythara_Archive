"""
Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

Mythara Gopher - ABC (Always Be Closing) Consultation Framework Demo
Shows how Gopher guides users through complete problem-solving cycle
"""

from mythara_gopher_nlp_engine import MytharaGopherNLP

def demo_abc_consultation():
    """
    Demonstrate ABC consultation framework through a realistic scenario.
    Shows Discovery → Qualification → Solution Design → Implementation → Closing
    """
    print("\n" + "=" * 80)
    print("MYTHARA GOPHER - ABC CONSULTATION FRAMEWORK DEMO")
    print("Always Be Closing: Complete Problem-Solving Cycle")
    print("=" * 80 + "\n")
    
    gopher = MytharaGopherNLP()
    session_id = "abc_demo_session"
    
    # Simulate realistic consultation conversation
    conversation = [
        {
            "user": "My boss fired me yesterday",
            "stage_expected": "discovery",
            "note": "Initial contact - Discovery phase begins"
        },
        {
            "user": "I complained about safety violations last week and then boom, fired for 'performance issues'",
            "stage_expected": "qualification",
            "note": "Pain point identified - Pressing the pain"
        },
        {
            "user": "I got kids to feed and rent due next week. This is urgent.",
            "stage_expected": "qualification",
            "note": "Urgency established - Multiple pain points"
        },
        {
            "user": "I want to take legal action. What can I do?",
            "stage_expected": "solution_design",
            "note": "Readiness to act - Solution design phase"
        },
        {
            "user": "Yes, I want to send a demand letter. What do I need?",
            "stage_expected": "implementation",
            "note": "Commitment to action - Implementation phase"
        }
    ]
    
    print("SCENARIO: Wrongful Termination / Retaliation Case\n")
    print("Watch as Gopher:\n")
    print("  1. 🔍 Discovers the need (what happened?)")
    print("  2. 💥 Presses the pain (urgency? impact?)")
    print("  3. 🤝 Builds rapport (understands preferences)")
    print("  4. 🛠️  Designs solution (custom action plan)")
    print("  5. ✅ Implements (generates docs, creates plan)")
    print("  6. 🎯 Closes loop (ensures next steps)\n")
    print("=" * 80 + "\n")
    
    for turn, conv in enumerate(conversation, 1):
        print(f"\n{'='*80}")
        print(f"TURN {turn}: {conv['stage_expected'].upper()} STAGE")
        print(f"{'='*80}")
        print(f"\n📝 Note: {conv['note']}\n")
        print(f"👤 USER:")
        print(f"   \"{conv['user']}\"\n")
        
        response = gopher.process_query(conv['user'], user_id="abc_demo", session_id=session_id)
        
        # Get context to show ABC tracking
        context = gopher.active_contexts[session_id]
        
        print(f"🦫 GOPHER:")
        print("-" * 80)
        print(response)
        print("-" * 80)
        
        # Show ABC framework tracking
        print(f"\n📊 ABC TRACKING:")
        print(f"   • Consultation Stage: {context.consultation_stage}")
        print(f"   • Urgency Level: {context.urgency_level}")
        print(f"   • Readiness to Act: {context.readiness_to_act:.1%}")
        print(f"   • Pain Points: {len(context.pain_points)}")
        if context.pain_points:
            for pain in context.pain_points[:3]:
                print(f"     - {pain}")
        if context.user_preferences:
            print(f"   • User Preferences: {context.user_preferences}")
        
        input("\n▶️  Press Enter to continue...")
    
    print("\n" + "=" * 80)
    print("✅ ABC CONSULTATION COMPLETE")
    print("=" * 80)
    print("\nKey Outcomes:")
    print("  ✅ Problem fully understood (Discovery)")
    print("  ✅ Urgency and pain points identified (Qualification)")
    print("  ✅ User preferences captured (Rapport)")
    print("  ✅ Custom solution designed (Solution Design)")
    print("  ✅ Concrete action plan created (Implementation)")
    print("  ✅ Next steps clearly defined (Closing)")
    print("\nUser leaves with: Clear plan, specific actions, and sense of urgency!")
    print("=" * 80 + "\n")

def demo_high_urgency_fast_close():
    """
    Show how ABC framework handles critical urgency - fast close
    """
    print("\n" + "=" * 80)
    print("DEMO: HIGH URGENCY SCENARIO (Fast Close)")
    print("=" * 80 + "\n")
    
    gopher = MytharaGopherNLP()
    
    query = "URGENT! I got evicted notice today, says I have 3 days to leave but I paid rent! Help!"
    
    print("👤 USER:")
    print(f"   \"{query}\"\n")
    
    response = gopher.process_query(query, user_id="urgent_demo")
    
    print("🦫 GOPHER:")
    print("-" * 80)
    print(response)
    print("-" * 80)
    
    context = list(gopher.active_contexts.values())[0]
    
    print(f"\n📊 ABC ANALYSIS:")
    print(f"   • Urgency: {context.urgency_level} (triggers immediate close)")
    print(f"   • Pain Points: {context.pain_points}")
    print(f"   • Action Plan: Generated immediately due to urgency")
    print("\n✅ Notice: Gopher skips gradual build-up and closes FAST when urgency is critical\n")

def demo_low_readiness_nurture():
    """
    Show how ABC framework handles low readiness - nurturing approach
    """
    print("\n" + "=" * 80)
    print("DEMO: LOW READINESS (Nurturing Approach)")
    print("=" * 80 + "\n")
    
    gopher = MytharaGopherNLP()
    
    query = "I'm thinking maybe I might have a case against my landlord but I'm not sure"
    
    print("👤 USER:")
    print(f"   \"{query}\"\n")
    
    response = gopher.process_query(query, user_id="nurture_demo")
    
    print("🦫 GOPHER:")
    print("-" * 80)
    print(response)
    print("-" * 80)
    
    context = list(gopher.active_contexts.values())[0]
    
    print(f"\n📊 ABC ANALYSIS:")
    print(f"   • Readiness: {context.readiness_to_act:.1%} (low - needs nurturing)")
    print(f"   • Stage: {context.consultation_stage}")
    print("\n✅ Notice: Gopher focuses on discovery and building case, not pushing hard close\n")

def show_abc_framework_overview():
    """Show overview of ABC methodology"""
    print("\n" + "=" * 80)
    print("MYTHARA GOPHER ABC FRAMEWORK OVERVIEW")
    print("=" * 80 + "\n")
    
    print("🎯 **ALWAYS BE CLOSING** - Not shutting down, but CLOSING THE LOOP\n")
    
    print("📋 **THE 6-STAGE CONSULTATION CYCLE:**\n")
    
    print("1. 🔍 DISCOVERY")
    print("   • Find the real need/problem")
    print("   • Open-ended questions")
    print("   • Build initial understanding\n")
    
    print("2. 💥 QUALIFICATION (Press the Pain)")
    print("   • Identify pain points")
    print("   • Assess urgency level")
    print("   • Understand impact/consequences")
    print("   • Ask: What happens if you do nothing?\n")
    
    print("3. 🤝 RAPPORT (Likes/Dislikes)")
    print("   • Learn communication preferences")
    print("   • Understand cost sensitivity")
    print("   • Identify DIY vs representation preference")
    print("   • Build trust through understanding\n")
    
    print("4. 🛠️  SOLUTION DESIGN")
    print("   • Build custom solution based on:")
    print("     - Legal issues identified")
    print("     - User preferences")
    print("     - Urgency level")
    print("     - Readiness to act\n")
    
    print("5. ✅ IMPLEMENTATION")
    print("   • Generate documents (demand letters, C&D)")
    print("   • Create evidence summaries")
    print("   • Timestamp critical statements")
    print("   • Provide concrete deliverables\n")
    
    print("6. 🎯 CLOSING THE LOOP")
    print("   • Clear action plan with numbered steps")
    print("   • Specific deadlines")
    print("   • Follow-up questions")
    print("   • Ensure user knows EXACTLY what to do next\n")
    
    print("=" * 80)
    print("KEY PRINCIPLE: Every conversation ends with ACTION, not information")
    print("=" * 80 + "\n")
    
    print("💡 **ADAPTIVE CLOSING:**\n")
    print("   • High urgency → Fast close with immediate actions")
    print("   • Low readiness → Nurture, educate, build confidence")
    print("   • High readiness → Strong close with document generation")
    print("   • Critical pain → Skip stages, close immediately\n")

def main():
    """Run ABC framework demo"""
    print("\n" + "=" * 80)
    print("  MYTHARA GOPHER - ABC (ALWAYS BE CLOSING) FRAMEWORK")
    print("  Consultation methodology for complete problem solving")
    print("=" * 80)
    
    print("\nChoose demo:\n")
    print("1. 🎬 Full ABC Consultation (5-turn scenario)")
    print("2. ⚠️  High Urgency Fast Close")
    print("3. 🌱 Low Readiness Nurturing")
    print("4. 📚 ABC Framework Overview")
    print("5. 🏃 Run All Demos")
    print("6. 🚪 Exit")
    
    choice = input("\nSelect (1-6): ").strip()
    
    if choice == "1":
        demo_abc_consultation()
    elif choice == "2":
        demo_high_urgency_fast_close()
    elif choice == "3":
        demo_low_readiness_nurture()
    elif choice == "4":
        show_abc_framework_overview()
    elif choice == "5":
        show_abc_framework_overview()
        input("\nPress Enter to continue to demos...")
        demo_abc_consultation()
        input("\nPress Enter for high urgency demo...")
        demo_high_urgency_fast_close()
        input("\nPress Enter for low readiness demo...")
        demo_low_readiness_nurture()
    elif choice == "6":
        print("\n👋 Goodbye!")
    else:
        print("\n❌ Invalid choice")

if __name__ == "__main__":
    main()
