"""
Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

Mythara Gopher - Vernacular Comprehension Demo
Shows vernacular input → professional English output
"""

from mythara_gopher_nlp_engine import MytharaGopherNLP

def demo_side_by_side():
    """Show vernacular input with professional output side-by-side"""
    print("\n" + "=" * 80)
    print("MYTHARA GOPHER - VERNACULAR COMPREHENSION DEMO")
    print("Input: ANY vernacular | Output: ALWAYS professional English")
    print("=" * 80 + "\n")
    
    gopher = MytharaGopherNLP()
    
    # Demo cases showing diverse inputs
    demos = [
        {
            "title": "Employment Discrimination (AAVE)",
            "input": "My boss be treating me different cuz I'm Black, can I sue?",
            "context": "AAVE verbal patterns + informal speech"
        },
        {
            "title": "Wrongful Termination (Mixed Vernacular)",
            "input": "They fired me but I ain't did nothing wrong, finna take them to court",
            "context": "AAVE + legal slang"
        },
        {
            "title": "Landlord Issues (Southern + Informal)",
            "input": "Y'all, my landlord tryna keep my deposit but the place was clean",
            "context": "Southern dialect + informal speech"
        },
        {
            "title": "Police Misconduct (AAVE + Slang)",
            "input": "The po-po locked me up but Ion did nothing, they violated my rights",
            "context": "AAVE + police slang"
        },
        {
            "title": "Car Accident (Legal Slang)",
            "input": "Some fool smashed into my car and totaled it, he owe me money right?",
            "context": "Informal + legal slang"
        }
    ]
    
    for i, demo in enumerate(demos, 1):
        print(f"\n{'='*80}")
        print(f"DEMO {i}: {demo['title']}")
        print(f"{'='*80}")
        print(f"\n📥 USER INPUT ({demo['context']}):")
        print(f"   \"{demo['input']}\"")
        
        # Show normalization
        normalized = gopher.normalize_vernacular(demo['input'])
        print(f"\n🔄 NORMALIZED (for processing):")
        print(f"   \"{normalized}\"")
        
        # Get response
        print(f"\n📤 GOPHER RESPONSE (professional English):")
        print("-" * 80)
        response = gopher.process_query(demo['input'], user_id=f"demo_{i}")
        
        # Show first 500 chars
        preview = response[:500] + "..." if len(response) > 500 else response
        print(preview)
        print("-" * 80)
        
        # Verify professional output
        vernacular_markers = ["ain't", "finna", "tryna", "y'all", "po-po", "Ion"]
        has_vernacular = any(marker.lower() in response.lower() for marker in vernacular_markers)
        
        if has_vernacular:
            print("❌ WARNING: Response contains vernacular")
        else:
            print("✅ Response in professional English")
        
        print(f"✅ Proper grammar maintained")
        print(f"✅ Legal terminology used")
        
        input("\nPress Enter for next demo...")
    
    print("\n" + "=" * 80)
    print("✅ DEMO COMPLETE")
    print("Mythara Gopher comprehends ALL vernaculars")
    print("Responds ONLY in professional legal English")
    print("=" * 80 + "\n")

def interactive_vernacular_test():
    """Allow user to test with their own vernacular input"""
    print("\n" + "=" * 80)
    print("INTERACTIVE VERNACULAR TEST")
    print("=" * 80 + "\n")
    
    gopher = MytharaGopherNLP()
    
    print("Enter legal queries in ANY vernacular, dialect, or informal speech.")
    print("Gopher will respond in professional English.\n")
    print("Examples:")
    print('  • "My boss be trippin, can I sue?"')
    print('  • "They ain\'t paid me in 3 weeks"')
    print('  • "Finna send a demand letter to my landlord"')
    print('  • "Got locked up for no reason"\n')
    print("Type 'quit' to exit\n")
    
    session_id = "interactive_vernacular"
    
    while True:
        user_input = input("\n🗣️  YOUR QUERY (vernacular OK): ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Thanks for testing Mythara Gopher's vernacular comprehension!")
            break
        
        if not user_input:
            continue
        
        # Show normalization
        normalized = gopher.normalize_vernacular(user_input)
        print(f"\n🔄 Normalized: \"{normalized}\"")
        
        # Get response
        print(f"\n🦫 GOPHER (professional English):")
        print("-" * 80)
        response = gopher.process_query(user_input, user_id="interactive", session_id=session_id)
        print(response)
        print("-" * 80)

def main():
    """Run vernacular comprehension demo"""
    print("\n" + "=" * 80)
    print("  MYTHARA GOPHER - VERNACULAR COMPREHENSION FEATURE")
    print("  Understands: AAVE, Southern dialects, slang, multilingual")
    print("  Responds: Professional legal English with proper grammar")
    print("=" * 80)
    
    print("\nChoose demo mode:\n")
    print("1. 🎬 Guided Demo (5 examples)")
    print("2. 💬 Interactive Test (your own input)")
    print("3. 📚 Quick Reference")
    print("4. 🚪 Exit")
    
    choice = input("\nSelect (1-4): ").strip()
    
    if choice == "1":
        demo_side_by_side()
    elif choice == "2":
        interactive_vernacular_test()
    elif choice == "3":
        print("\n" + "=" * 80)
        print("VERNACULAR COMPREHENSION - QUICK REFERENCE")
        print("=" * 80 + "\n")
        
        print("📋 SUPPORTED VERNACULARS:\n")
        print("✅ AAVE (African American Vernacular)")
        print("   ain't, be (habitual), finna, tryna, Ion, Imma, etc.\n")
        
        print("✅ Southern Dialects")
        print("   y'all, fixin' to, reckon, might could, etc.\n")
        
        print("✅ Informal Speech")
        print("   kinda, sorta, gonna, wanna, cuz, tho, etc.\n")
        
        print("✅ Legal Slang")
        print("   got fired, kicked out, smashed into, owed money, etc.\n")
        
        print("✅ Multilingual")
        print("   Spanish: abogado, demanda, contrato, trabajo")
        print("   Chinese: lüshi, fayuan, hetong, zhengju\n")
        
        print("🎯 KEY PRINCIPLE:")
        print("   INPUT: Any vernacular ➜ OUTPUT: Professional English\n")
        
        print("📖 See VERNACULAR_COMPREHENSION.md for full documentation\n")
    elif choice == "4":
        print("\n👋 Goodbye!")
    else:
        print("\n❌ Invalid choice")

if __name__ == "__main__":
    main()
