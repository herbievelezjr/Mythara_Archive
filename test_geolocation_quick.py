#!/usr/bin/env python3
"""Quick test of GeoIPManager with MaxMind database"""

from sere_security_system import GeoIPManager, CONFIG

print("Testing GeoIPManager with MaxMind GeoLite2-City.mmdb\n")
print(f"Database path: {CONFIG['GEOIP_DB_PATH']}")

# Initialize manager
gm = GeoIPManager()

print(f"✅ GeoIPManager initialized: {gm.is_initialized}")
print(f"Database reader: {gm.reader is not None}\n")

# Test lookups
test_ips = [
    "8.8.8.8",      # Google (US)
    "1.1.1.1",      # Cloudflare (US)
    "91.198.174.192" # Wikimedia (likely non-US)
]

print("Testing IP lookups:\n")
for ip in test_ips:
    country = gm.get_country_code(ip)
    is_friendly = gm.is_friendly_country(country) if country else False
    print(f"  {ip:20s} → Country: {country or 'N/A':5s} | Friendly: {is_friendly}")

print(f"\nCache stats: {gm.get_cache_stats()}")
print("\n✅ GeoIPManager test completed without crashing!")
