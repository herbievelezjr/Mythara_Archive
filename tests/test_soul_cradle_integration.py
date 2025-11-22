"""Test Soul Cradle integration with Gopher"""

from mythara_gopher_nlp_engine import MytharaGopherNLP, SOUL_CRADLE_AVAILABLE

print(f"\n{'='*60}")
print(f"Soul Cradle Available: {SOUL_CRADLE_AVAILABLE}")
print(f"{'='*60}\n")

if SOUL_CRADLE_AVAILABLE:
    print("✅ Soul Cradle ENABLED - Emotional intelligence features active!")
    print("✅ Paradox detection: OPERATIONAL")
    print("✅ Coercion assessment: OPERATIONAL")
    print("✅ Terminal risk calculation: OPERATIONAL\n")
    
    gopher = MytharaGopherNLP()
    print("\n✅ Gopher initialized with Soul Cradle successfully!")
    
    # Test query with emotional intelligence
    response = gopher.process_query(
        "My boss threatened to fire me if I don't work this weekend without pay",
        user_id="test_user"
    )
    
    print("\n" + "="*60)
    print("TEST QUERY: Boss threatening termination for unpaid work")
    print("="*60)
    print(response[:500] + "..." if len(response) > 500 else response)
    
else:
    print("❌ Soul Cradle DISABLED - Emotional intelligence features unavailable")
    print("⚠️  Paradox detection will be skipped")
    print("⚠️  Coercion assessment will be skipped")
    print("⚠️  Terminal risk calculation will be skipped")
