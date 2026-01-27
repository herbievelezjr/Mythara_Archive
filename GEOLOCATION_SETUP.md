# SERE Sovereign Security System Geolocation Friend/Foe Classification Setup Guide

**Copyright © 2025 Herbert Velez Jr. All rights reserved.**
**Proprietary and Confidential.**

---

## Overview

SERE Sovereign Security System now includes **geolocation-based friend/foe IP classification** using the **MaxMind GeoLite2 database** (free, offline, no API calls).

### Friend/Foe Logic
- **🤝 Friends**: US IP addresses → 90% threat reduction (0.1x multiplier)
- **⚠️ Foes**: Non-US IP addresses → Normal threat level (1.0x multiplier)  
- **❓ Unknown**: Ungeolocated IPs → 50% threat reduction (0.5x multiplier)
- **🔒 Local**: Private IP ranges → Always safe

---

## Installation Steps

### STEP 1: Download MaxMind GeoLite2-City Database (Free)

1. Visit: **https://www.maxmind.com/en/geolite2/geolite2-free**
2. Create a free MaxMind account (sign up is instant)
3. Download **GeoLite2 City** (as `.tar.gz` or `.zip`)
4. Extract the archive to find `GeoLite2-City.mmdb`
5. Place `GeoLite2-City.mmdb` in the **Mythara_Archive root directory**

**Database size**: ~40MB  
**Update frequency**: Weekly (automatic if manually re-downloaded)  
**Cost**: FREE

### STEP 2: Install geoip2 Package

The `geoip2` package has already been added to `requirements.txt`. Install it:

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install geoip2 only
pip install geoip2
```

### STEP 3: Verify Installation

Run the test script:

```bash
python test_geolocation.py
```

Expected output:
```
✅ geoip2 module is installed
✅ GeoLite2 database found: GeoLite2-City.mmdb (40.5 MB)
✅ All dependencies ready! SERE Sovereign Security System geolocation is ready to use.
```

---

## How It Works

### Threat Detection Integration

When SERE Sovereign Security System detects a network connection, it:

1. **Gets the remote IP address** from the network connection
2. **Classifies the IP** using local GeoIP database:
   - Checks if IP is from a friendly country (US)
   - Returns classification: FRIEND, FOE, or UNKNOWN
3. **Adjusts threat severity** based on classification:
   - FRIEND → MODERATE severity (instead of SUBSTANTIAL)
   - FOE → SEVERE severity (instead of SUBSTANTIAL)
   - UNKNOWN → SUBSTANTIAL (unchanged)
4. **Multiplies threat confidence** by threat multiplier:
   - FRIEND: 0.75 × 0.1 = 0.075 confidence
   - FOE: 0.75 × 1.0 = 0.75 confidence
   - UNKNOWN: 0.75 × 0.5 = 0.375 confidence
5. **Logs geolocation data** (country, city, timezone, coordinates)

### Example Output

```
[2026-01-26 10:15:32] sere_bot [INFO] 🤝 FRIEND (FRIEND): Unknown connection to 8.8.8.8:443
  - Severity: MODERATE (reduced)
  - Confidence: 0.075 (90% reduced)
  - Country: United States
  - City: Mountain View, CA

[2026-01-26 10:15:35] sere_bot [INFO] ⚠️  FOE (FOE): Unknown connection to 200.100.50.25:443
  - Severity: SEVERE (escalated)
  - Confidence: 0.75 (normal)
  - Country: Mexico
  - City: Mexico City
```

---

## Configuration

### Default Settings (sere_security_system.py)

```python
CONFIG = {
    # === GEOLOCATION & FRIEND/FOE ===
    'ENABLE_GEOLOCATION': True,                    # Enable US-only friend classification
    'GEOIP_DB_PATH': 'GeoLite2-City.mmdb',         # MaxMind GeoLite2 database file
    'FRIENDLY_COUNTRIES': ['US'],                  # Countries considered "friendly"
    'GEOIP_CACHE_SIZE': 500,                       # Cache size for geolocation lookups
}
```

### Customize Friendly Countries

To add more friendly countries, edit `sere_security_system.py`:

```python
# Example: US, Canada, UK, Australia as friends
CONFIG['FRIENDLY_COUNTRIES'] = ['US', 'CA', 'UK', 'AU']
```

**Common Country Codes** (ISO 3166-1 alpha-2):
| Code | Country | Code | Country |
|------|---------|------|---------|
| US | United States | CA | Canada |
| UK | United Kingdom | DE | Germany |
| FR | France | JP | Japan |
| AU | Australia | SG | Singapore |

---

## Implementation Details

### New Classes

#### `GeoIPManager`
Manages local geolocation database and caching.

Methods:
- `get_country_code(ip)` → Returns country code (e.g., 'US')
- `get_geolocation(ip)` → Returns full geolocation data (country, city, timezone)
- `is_friendly_country(code)` → Checks if country is in friendly list
- `get_cache_stats()` → Returns cache performance metrics

### New SERE Sovereign Security System Methods

- `_is_us_ip(ip)` → Checks if IP is from friendly country
- `_classify_ip_threat(ip)` → Classifies IP as FRIEND/FOE/UNKNOWN, returns threat multiplier
- `get_geolocation_stats()` → Returns detailed geolocation statistics

### Performance

- **Database load time**: < 1 second
- **IP lookup time**: < 1ms (with caching, even faster)
- **Cache size**: Configurable (default 500 entries)
- **Hit ratio**: Typical 80-90% after warmup

---

## Troubleshooting

### Issue: "GeoIP database not found"
**Solution**: Download `GeoLite2-City.mmdb` and place it in the Mythara_Archive root directory.

### Issue: "geoip2 not available"
**Solution**: Run `pip install geoip2`

### Issue: Geolocation appears disabled in logs
**Verify**:
1. `GeoLite2-City.mmdb` exists in the project root
2. `geoip2` package is installed
3. `CONFIG['ENABLE_GEOLOCATION'] = True` in sere_security_system.py

### Issue: Slow IP lookups
**Cause**: Cache miss for many unique IPs  
**Solution**: Increase `GEOIP_CACHE_SIZE` in CONFIG

---

## No API Calls - Completely Offline

Unlike cloud-based geolocation services:
- ✅ **No API calls** - Uses local database
- ✅ **No rate limits** - Unlimited lookups per second
- ✅ **No API keys** - Nothing to configure or manage
- ✅ **No latency** - < 1ms per lookup
- ✅ **Offline capable** - Works without internet
- ✅ **Privacy** - No external data sharing

---

## Monitoring & Statistics

Check geolocation performance:

```python
# In SERE Sovereign Security System instance
stats = bot.get_geolocation_stats()
print(stats)
```

Returns:
```json
{
  "status": "enabled",
  "friendly_countries": ["US"],
  "geoip_database": "GeoLite2-City.mmdb",
  "cache_stats": {
    "cache_size": 47,
    "cache_hits": 238,
    "cache_misses": 52,
    "hit_ratio": 0.82
  },
  "threat_classifications": {
    "friends": 12,
    "foes": 34,
    "unknown": 5
  }
}
```

---

## Technical Architecture

```
Threat Detection Flow
├── Get Network Connection
│   └── Remote IP: 200.100.50.25
├── Is Native/Private IP?
│   ├── YES → LOCAL (safe)
│   └── NO → Continue to geolocation
├── GeoIPManager.get_country_code()
│   ├── Check cache first
│   │   ├── HIT → Return from cache
│   │   └── MISS → Query database
│   ├── Database lookup: GeoLite2-City.mmdb
│   └── Return country code (e.g., 'MX')
├── Classify IP (FRIEND/FOE/UNKNOWN)
│   ├── Is in FRIENDLY_COUNTRIES?
│   │   ├── YES → FRIEND, multiplier=0.1
│   │   └── NO → FOE, multiplier=1.0
│   └── If ungeolocated → UNKNOWN, multiplier=0.5
├── Create ThreatDetection with:
│   ├── Adjusted severity
│   ├── Adjusted confidence
│   └── Geolocation data
└── Log threat with emoji indicator
    ├── 🤝 FRIEND
    ├── ⚠️  FOE
    └── ❓ UNKNOWN
```

---

## Next Steps

1. ✅ Download `GeoLite2-City.mmdb` from MaxMind
2. ✅ Run `pip install -r requirements.txt`
3. ✅ Start SERE Sovereign Security System: `python sere_security_system.py`
4. ✅ Monitor logs for geolocation classifications
5. ✅ Adjust `FRIENDLY_COUNTRIES` as needed

---

**Questions?** Check the inline code comments in:
- `sere_security_system.py` → `GeoIPManager` class
- `sere_security_system.py` → `detect_threats()` method
- `sere_security_system.py` → Friend/foe classification methods
