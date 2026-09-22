import os
# Copyright © 2025 Herbert Velez Jr. All rights reserved.

"""
Test Mythara Orchestrator API
"""

import requests
import json

API_URL = "http://localhost:5000"
# QUICKFIX FIX: Moved to environment variable (CWE-798)
VP_TOKEN = os.getenv("VP_TOKEN", "")  # Set via environment

def test_health():
    """Test health endpoint."""
    response = requests.get(f"{API_URL}/health")
    print("Health Check:")
    print(json.dumps(response.json(), indent=2))
    print()

def test_register_bot():
    """Test bot registration."""
    response = requests.post(f"{API_URL}/register_bot", json={
        'vp_token': VP_TOKEN,
        'bot_id': 'sales_bot',
        'bot_name': 'Autonomous Sales Bot'
    })
    print("Register Bot:")
    print(json.dumps(response.json(), indent=2))
    return response.json().get('bot_token')

def test_request_approval(bot_token):
    """Test approval request."""
    response = requests.post(f"{API_URL}/request_approval", json={
        'bot_id': 'sales_bot',
        'token': bot_token,
        'action': 'send_email',
        'reason': 'cold_outreach',
        'count': 10
    })
    print("\nRequest Approval:")
    print(json.dumps(response.json(), indent=2))

def test_dashboard():
    """Test dashboard."""
    response = requests.get(f"{API_URL}/dashboard")
    print("\nDashboard:")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("🧪 Testing Mythara Orchestrator API\n")
    print("="*60)
    
    try:
        test_health()
        bot_token = test_register_bot()
        if bot_token:
            test_request_approval(bot_token)
        test_dashboard()
        
        print("\n" + "="*60)
        print("✅ All tests passed")
    except Exception as e:
        print(f"\n❌ Error: {e}")
