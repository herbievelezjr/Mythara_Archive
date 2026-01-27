#!/usr/bin/env python3
"""
Test proxy bouncing functionality in SERE

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.
"""

import sys
sys.path.insert(0, '.')

from sere_security_system import SERESecuritySystem

def test_proxy_bounce():
    """Test the proxy bounce reconnaissance feature"""
    print("\n" + "="*70)
    print("🧪 TESTING SERE PROXY BOUNCE RECONNAISSANCE")
    print("="*70)
    
    bot = SERESecuritySystem()
    
    # Test 1: Check if proxy support is available
    print("\n[Test 1] Checking proxy support availability...")
    try:
        import requests
        import socks
        print("✓ Proxy support available (requests + PySocks installed)")
    except ImportError as e:
        print(f"✗ Proxy support NOT available: {e}")
        print("   Install: pip install requests PySocks")
        return
    
    # Test 2: Configure SOCKS proxy
    print("\n[Test 2] Configuring SOCKS5 proxy...")
    result = bot.configure_socks_proxy("195.208.3.194", 1080, "SOCKS5")
    if result:
        print("✓ SOCKS proxy configured successfully")
    else:
        print("✗ Failed to configure SOCKS proxy")
    
    # Test 3: Execute proxy bounce reconnaissance (using a safe test target)
    print("\n[Test 3] Testing proxy bounce reconnaissance...")
    print("   Target: http://example.com (safe test target)")
    
    # Use a smaller proxy list for testing
    test_proxies = [
        {'http': 'socks5h://195.208.3.194:1080', 'https': 'socks5h://195.208.3.194:1080'},
        {'http': 'socks5h://195.208.3.194:1081', 'https': 'socks5h://195.208.3.194:1081'},
    ]
    
    results = bot.proxy_bounce_reconnaissance(
        target_url="http://example.com",
        proxy_list=test_proxies,
        delay_seconds=2,
        max_attempts=2
    )
    
    if 'error' in results:
        print(f"✗ Reconnaissance failed: {results['error']}")
    else:
        print("\n✓ Reconnaissance completed")
        print(f"   Successful: {results['successful']}/{results['total_proxies']}")
        print(f"   Failed: {results['failed']}/{results['total_proxies']}")
        
        if results['attempts']:
            print("\n   Detailed Results:")
            for i, attempt in enumerate(results['attempts'], 1):
                status = "✓" if attempt['success'] else "✗"
                proxy = attempt['proxy']
                if attempt['success']:
                    print(f"   [{i}] {status} {proxy}: HTTP {attempt['status_code']} ({attempt['response_time']}s)")
                else:
                    print(f"   [{i}] {status} {proxy}: {attempt.get('error', 'Unknown error')[:60]}")
    
    print("\n" + "="*70)
    print("🧪 PROXY BOUNCE TEST COMPLETE")
    print("="*70)

if __name__ == "__main__":
    test_proxy_bounce()
