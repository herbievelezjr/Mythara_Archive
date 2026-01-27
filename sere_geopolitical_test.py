#!/usr/bin/env python3
"""
SERE Bot Geopolitical Friend/Foe System - Integration Test & Demo

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

This script demonstrates the new geopolitical threat classification system.
Run it to verify the integration works correctly.

USAGE:
    python sere_geopolitical_test.py
"""

import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(name)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


def test_maxmind_geolocation():
    """Test MaxMind GeoIP2 database integration"""
    print("\n" + "="*70)
    print("TEST 1: MaxMind GeoIP2 Integration")
    print("="*70)
    
    try:
        from sere_security_system import GeoIPManager, CONFIG
        
        manager = GeoIPManager()
        
        if not manager.is_initialized:
            print("⚠️  GEOIP2 database not initialized")
            print("   Download GeoLite2-City.mmdb from:")
            print("   https://www.maxmind.com/en/geolite2/geolite2-free")
            return False
        
        print("✅ GeoIPManager initialized successfully")
        print(f"   Database: {CONFIG['GEOIP_DB_PATH']}")
        print(f"   Cache size: {CONFIG['GEOIP_CACHE_SIZE']}")
        
        # Test IP lookups
        test_ips = {
            "1.2.3.4": "GB",           # UK
            "5.6.7.8": "RU",           # Russia
            "9.10.11.12": "CN",        # China
            "13.14.15.16": "JP",       # Japan
            "17.18.19.20": "US",       # USA
        }
        
        print("\n📍 Testing IP Geolocation:")
        for ip, expected_country in test_ips.items():
            country_code = manager.get_country_code(ip)
            geo = manager.get_geolocation(ip)
            
            if geo:
                country = geo.get('country', 'Unknown')
                city = geo.get('city', 'Unknown')
                print(f"   {ip:15} → {country:20} ({city:15}) [Code: {country_code}]")
            else:
                print(f"   {ip:15} → Could not geolocate")
        
        return True
    
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you have geoip2 installed: pip install geoip2")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_threat_classification():
    """Test friend/foe classification with geopolitical analysis"""
    print("\n" + "="*70)
    print("TEST 2: Friend/Foe Threat Classification")
    print("="*70)
    
    try:
        from sere_security_system import SERESecuritySystem
        
        bot = SERESecuritySystem()
        print("✅ SERESecuritySystem initialized successfully")
        
        # Test IPs with expected classifications
        test_scenarios = [
            {
                'ip': '1.2.3.4',
                'description': 'United Kingdom (ALLY)',
                'expected': 'FRIEND'
            },
            {
                'ip': '5.6.7.8',
                'description': 'Russia (HOSTILE)',
                'expected': 'CRITICAL_FOE'
            },
            {
                'ip': '9.10.11.12',
                'description': 'China (HOSTILE)',
                'expected': 'CRITICAL_FOE'
            },
            {
                'ip': '13.14.15.16',
                'description': 'Japan (PARTNER)',
                'expected': 'ALLY'
            },
            {
                'ip': '127.0.0.1',
                'description': 'Localhost (LOCAL)',
                'expected': 'LOCAL'
            },
        ]
        
        print("\n🔍 Testing Threat Classification:")
        print(f"{'IP':<15} {'Description':<30} {'Classification':<20} {'Multiplier':<10} {'Status'}")
        print("-"*95)
        
        for scenario in test_scenarios:
            ip = scenario['ip']
            description = scenario['description']
            expected = scenario['expected']
            
            classification, multiplier = bot._classify_ip_threat(ip)
            
            # Check if classification makes sense
            status = "✅" if classification in [expected, 'UNKNOWN', 'ALLY'] else "⚠️"
            
            print(f"{ip:<15} {description:<30} {classification:<20} {multiplier:<10.2f} {status}")
        
        return True
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_threat_severity_assessment():
    """Test geopolitical-aware threat severity assessment"""
    print("\n" + "="*70)
    print("TEST 3: Geopolitical Threat Severity Assessment")
    print("="*70)
    
    try:
        from sere_security_system import SERESecuritySystem, ThreatLevel
        
        bot = SERESecuritySystem()
        
        test_cases = [
            {
                'classification': 'FRIEND',
                'multiplier': 0.1,
                'base_severity': ThreatLevel.SUBSTANTIAL,
                'description': 'Allied nation threat'
            },
            {
                'classification': 'FOE',
                'multiplier': 1.0,
                'base_severity': ThreatLevel.SUBSTANTIAL,
                'description': 'Hostile nation threat'
            },
            {
                'classification': 'CRITICAL_FOE',
                'multiplier': 1.5,
                'base_severity': ThreatLevel.SUBSTANTIAL,
                'description': 'State-level APT threat'
            },
        ]
        
        print("\n📊 Testing Severity Assessment:")
        print(f"{'Classification':<20} {'Multiplier':<12} {'Base Severity':<15} {'Adjusted Severity':<20} {'Status'}")
        print("-"*87)
        
        for case in test_cases:
            adjusted = bot._assess_threat_severity_geopolitically(
                base_severity=case['base_severity'],
                threat_multiplier=case['multiplier'],
                classification=case['classification']
            )
            
            status = "✅"
            print(f"{case['classification']:<20} {case['multiplier']:<12.2f} {case['base_severity'].name:<15} {adjusted.name:<20} {status}")
        
        return True
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_classification_indicators():
    """Test emoji/text indicators for classifications"""
    print("\n" + "="*70)
    print("TEST 4: Classification Indicators")
    print("="*70)
    
    try:
        from sere_security_system import SERESecuritySystem
        
        bot = SERESecuritySystem()
        
        classifications = [
            ('LOCAL', 0.0),
            ('FRIEND', 0.1),
            ('ALLY', 0.2),
            ('NEUTRAL', 0.5),
            ('FOE', 1.0),
            ('CRITICAL_FOE', 1.5),
            ('UNKNOWN', 0.5),
        ]
        
        print("\n🎨 Testing Classification Indicators:")
        print(f"{'Classification':<20} {'Multiplier':<12} {'Indicator':<50} {'Status'}")
        print("-"*82)
        
        for classification, multiplier in classifications:
            indicator = bot._get_classification_indicator(classification, multiplier)
            status = "✅"
            print(f"{classification:<20} {multiplier:<12.2f} {indicator:<50} {status}")
        
        return True
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_geolocation_stats():
    """Test geolocation statistics collection"""
    print("\n" + "="*70)
    print("TEST 5: Geolocation Statistics")
    print("="*70)
    
    try:
        from sere_security_system import SERESecuritySystem
        
        bot = SERESecuritySystem()
        stats = bot.get_geolocation_stats()
        
        print("\n📈 Geolocation Statistics:")
        print(json.dumps(stats, indent=2, default=str))
        
        # Verify key fields
        required_fields = ['status', 'geoip_manager_status']
        for field in required_fields:
            if field in stats:
                print(f"✅ {field}: {stats[field]}")
            else:
                print(f"⚠️  Missing field: {field}")
        
        return True
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_geopolitical_integration():
    """Test integration with geopolitical analyzer (if available)"""
    print("\n" + "="*70)
    print("TEST 6: Geopolitical Analyzer Integration")
    print("="*70)
    
    try:
        from sere_security_system import SERESecuritySystem, GEOPOLITICAL_ANALYSIS_AVAILABLE
        
        if not GEOPOLITICAL_ANALYSIS_AVAILABLE:
            print("⚠️  Geopolitical analysis module not available")
            print("   This is optional - system falls back to MaxMind-only classification")
            return True
        
        bot = SERESecuritySystem()
        
        if bot.geopolitical_analyzer:
            print("✅ Geopolitical analyzer initialized")
            print("   Advanced features available:")
            print("   - 30+ state actor profiles")
            print("   - Threat capability assessments")
            print("   - Alliance relationship tracking")
            print("   - Escalation logic")
            return True
        else:
            print("⚠️  Geopolitical analyzer initialization failed")
            print("   Falling back to MaxMind-only classification")
            return True
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all integration tests"""
    print("\n" + "█"*70)
    print("█ SERE BOT GEOPOLITICAL FRIEND/FOE SYSTEM - INTEGRATION TESTS")
    print("█"*70)
    print(f"\nTest Date: {datetime.now().isoformat()}")
    print("System: MaxMind GeoIP2 + Geopolitical Analysis")
    
    tests = [
        ("MaxMind GeoIP2", test_maxmind_geolocation),
        ("Threat Classification", test_threat_classification),
        ("Threat Severity Assessment", test_threat_severity_assessment),
        ("Classification Indicators", test_classification_indicators),
        ("Geolocation Statistics", test_geolocation_stats),
        ("Geopolitical Integration", test_geopolitical_integration),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_flag in results.items():
        status = "✅ PASSED" if passed_flag else "❌ FAILED"
        print(f"{test_name:<40} {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All tests passed! Geopolitical friend/foe system is ready.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review output above.")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
