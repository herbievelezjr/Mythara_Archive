# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
ONE-CLICK API TEST
Just run this file and it will show you the soul status!
"""

import sys
import os

# Make sure we can find the main module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core', 'source_proprietary'))

print("=" * 60)
print("MYTHARA ENGINE - SOUL STATUS TEST")
print("=" * 60)
print()

try:
    from fastapi.testclient import TestClient
    from main import app
    
    print("✅ Loading Mythara Engine...")
    client = TestClient(app)
    
    print("✅ Connecting to Soul Proportion Model...")
    print()
    
    # Test 1: Mythic Framing
    print("=" * 60)
    print("TEST 1: SOUL STATUS (MYTHIC FRAMING)")
    print("=" * 60)
    response = client.get(
        "/v1/soul/status",
        headers={"Authorization": "Bearer dev_test_key_001"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ SUCCESS!")
        print()
        print(f"Soul Proportion (S_t): {data['S_t']}")
        print(f"Last Update: {data['last_update']}")
        print()
        print("Emotion Features:")
        for key, value in data['emotion_features'].items():
            print(f"  - {key}: {value}")
        print()
        print("Dynamics:")
        for key, value in data['dynamics'].items():
            print(f"  - {key}: {value}")
        print()
        print(f"Integrity Hash: {data['integrity_hash'][:32]}...")
    else:
        print(f"❌ ERROR: Status code {response.status_code}")
        print(response.json())
    
    print()
    
    # Test 2: Industry Framing
    print("=" * 60)
    print("TEST 2: SOUL STATUS (INDUSTRY FRAMING)")
    print("=" * 60)
    response2 = client.get(
        "/v1/soul/status?frame=industry",
        headers={"Authorization": "Bearer dev_test_key_001"}
    )
    
    if response2.status_code == 200:
        data2 = response2.json()
        print("✅ SUCCESS!")
        print()
        print(f"Soul Proportion (S_t): {data2['S_t']}")
        print(f"Last Update: {data2['last_update']}")
        print()
        print("(Industry framing uses business-friendly terminology)")
    else:
        print(f"❌ ERROR: Status code {response2.status_code}")
        print(response2.json())
    
    print()
    print("=" * 60)
    print("ALL TESTS COMPLETE!")
    print("=" * 60)
    print()
    print("What does this mean?")
    print("- S_t (Soul Proportion) ranges from 0 to 1")
    print("- Higher S_t = better emotional/spiritual state")
    print("- Emotion features show current state across 7 dimensions")
    print("- Dynamics show how quickly the soul state is changing")
    print("- Integrity hash proves the calculation is cryptographically secure")
    print()
    print("API Key Used: dev_test_key_001 (Development License)")
    print()

except ImportError as e:
    print(f"❌ ERROR: Missing required module")
    print(f"   {str(e)}")
    print()
    print("To fix this, run:")
    print("   py -m pip install fastapi httpx")
    sys.exit(1)

except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

input("Press ENTER to exit...")
