# SERE Sovereign Security System Friend/Foe Classification - Quick Reference

**Copyright © 2025 Herbert Velez Jr. All rights reserved.**

---

## TL;DR - What Changed

SERE Sovereign Security System now **recognizes US IPs as friends and all others as foes**, using a local offline geolocation database.

### Friend/Foe Classification
| IP Type | Classification | Threat Multiplier | Severity | Confidence |
|---------|-----------------|------------------|----------|-----------|
| 🔒 Local (192.168.x.x, 10.x.x.x) | LOCAL | 0.0x | NONE | 0.0 |
| 🤝 US IP (8.8.8.8, 1.1.1.1) | FRIEND | 0.1x | MODERATE | 0.075 |
| ⚠️  Non-US IP (200.x.x.x) | FOE | 1.0x | SEVERE | 0.75 |
| ❓ Unknown/Ungeolocated | UNKNOWN | 0.5x | SUBSTANTIAL | 0.375 |

---

## Setup (3 Steps)

### Step 1: Download Database (2 minutes)
1. Go to: https://www.maxmind.com/en/geolite2/geolite2-free
2. Click "Download GeoLite2 City"
3. Extract `GeoLite2-City.mmdb`
4. Place in: `Mythara_Archive/` directory

### Step 2: Install Package (1 minute)
```bash
pip install -r requirements.txt
```

### Step 3: Run SERE Sovereign Security System
```bash
python sere_security_system.py
```

**That's it!** Geolocation is automatically enabled.

---

## How It Works

**Threat detected** → Check IP origin → Classify (FRIEND/FOE/UNKNOWN) → Adjust severity & confidence

```
Network Connection to 8.8.8.8:443
├─ Query: Is this US?
├─ Answer: Yes (Google DNS - US-based)
├─ Classification: FRIEND 🤝
├─ Threat Reduced: 90%
└─ Log: "🤝 FRIEND: Unknown connection to 8.8.8.8:443"

Network Connection to 200.100.50.25:443
├─ Query: Is this US?
├─ Answer: No (Mexico-based)
├─ Classification: FOE ⚠️
├─ Threat Normal: 100%
└─ Log: "⚠️  FOE: Unknown connection to 200.100.50.25:443"
```

---

## Configuration

**Default** (in sere_security_system.py):
```python
CONFIG['FRIENDLY_COUNTRIES'] = ['US']  # Only US is friendly
```

**Add more friendly countries** (example):
```python
CONFIG['FRIENDLY_COUNTRIES'] = ['US', 'CA', 'UK', 'AU']  # US + Canada + UK + Australia
```

**Country Codes**: Use ISO 3166-1 alpha-2
- `US` = United States
- `CA` = Canada
- `UK` = United Kingdom
- `DE` = Germany
- `FR` = France
- `JP` = Japan
- (etc. for all countries)

---

## Key Features

✅ **No API Calls** - Uses offline database (~40MB)
✅ **Fast** - < 1ms per IP lookup with caching
✅ **Free** - MaxMind GeoLite2 is free & open
✅ **Private** - No data sent anywhere
✅ **Easy** - Just drop the database file in root directory

---

## Logging Output

Look for these indicators in logs:

```
[2026-01-26 10:15:32] sere_bot [INFO] 🤝 FRIEND (FRIEND): Unknown connection to 8.8.8.8:443
[2026-01-26 10:15:35] sere_bot [INFO] ⚠️  FOE (FOE): Unknown connection to 200.100.50.25:443
[2026-01-26 10:15:38] sere_bot [INFO] ❓ UNKNOWN (UNKNOWN): Unknown connection to 103.45.67.89:443
```

---

## Check Stats

```python
# In Python (if accessing bot directly)
stats = bot.get_geolocation_stats()
print(stats)

# Output:
# {
#   'status': 'enabled',
#   'friendly_countries': ['US'],
#   'cache_stats': {'cache_size': 47, 'cache_hits': 238, 'cache_misses': 52, 'hit_ratio': 0.82},
#   'threat_classifications': {'friends': 12, 'foes': 34, 'unknown': 5}
# }
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "GeoIP database not found" | Download `GeoLite2-City.mmdb` from MaxMind, place in root |
| "geoip2 not available" | Run `pip install geoip2` |
| Geolocation not working | Check logs, run `test_geolocation.py` |
| Slow IP lookups | Increase `CONFIG['GEOIP_CACHE_SIZE']` |

---

## What Was Added

| File | Changes |
|------|---------|
| `requirements.txt` | Added `geoip2>=4.7.0` |
| `sere_security_system.py` | Added GeoIPManager class, threat classification methods, integration with detect_threats() |
| `GEOLOCATION_SETUP.md` | Complete setup & config guide |
| `GEOLOCATION_IMPLEMENTATION.md` | Technical implementation details |

---

## Summary

**Before**: All non-local IPs = threat  
**After**: Non-local IPs = FRIEND (if US), FOE (if non-US), or UNKNOWN

**Threat reduction for US IPs**: 90%  
**No external APIs**: Uses offline MaxMind database  
**Easy setup**: Download 1 file, install 1 package, run bot

---

For detailed setup: See **GEOLOCATION_SETUP.md**  
For technical details: See **GEOLOCATION_IMPLEMENTATION.md**
