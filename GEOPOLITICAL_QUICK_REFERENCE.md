# SERE Sovereign Security System Geopolitical Friend/Foe Classification - Quick Reference

**Copyright © 2025 Herbert Velez Jr. All rights reserved.**

---

## TL;DR - How It Works

```
IP Address → MaxMind GeoIP2 → Country Code → Geopolitical Analysis → Classification
                (local DB)      (GB, RU, CN)    (ALLY, HOSTILE)      (FRIEND, FOE)
```

**Classifications:**
- 🤝 **FRIEND** (US, UK, CA, AU, NZ): 90% threat reduction
- 🛡️ **ALLY** (NATO, Japan): 80% threat reduction
- ⚖️ **NEUTRAL** (Most countries): 50% threat reduction
- ⚠️ **FOE** (Pakistan, Brazil, etc.): 20% threat escalation
- 🚨 **CRITICAL_FOE** (Russia, China, Iran, N.Korea): 50% threat escalation

---

## Setup (3 Steps)

### 1. Download MaxMind GeoLite2 Database
```
https://www.maxmind.com/en/geolite2/geolite2-free
Create account → Download GeoLite2-City.mmdb
```

### 2. Place File in Project
```
Mythara_Archive/
├── GeoLite2-City.mmdb  ← Here
├── sere_security_system.py
└── requirements.txt
```

### 3. Install Dependencies
```bash
pip install geoip2 python-dotenv
```

---

## Configuration

In `sere_security_system.py` CONFIG:

```python
'ENABLE_GEOLOCATION': True,              # Enable system
'GEOIP_DB_PATH': 'GeoLite2-City.mmdb',   # Database path
'FRIENDLY_COUNTRIES': ['US'],             # Base friendly list (overridden by geopolitical analysis)
'GEOIP_CACHE_SIZE': 500,                  # Cache size (faster repeated lookups)
```

---

## Usage Examples

### Check Threat Classification
```python
from sere_security_system import SERESecuritySystem

bot = SERESecuritySystem()
classification, multiplier = bot._classify_ip_threat("1.2.3.4")
# Returns: ("ALLY", 0.2)
```

### View Statistics
```python
stats = bot.get_geolocation_stats()
print(f"Threats from FOE countries: {stats['threat_classifications']['FOE']}")
# Output: Threats from FOE countries: 3
```

### Monitor Cache Performance
```python
cache_stats = bot.geoip_manager.get_cache_stats()
print(f"Cache hit ratio: {cache_stats['hit_ratio']:.1%}")
# Output: Cache hit ratio: 73.2%
```

---

## Threat Response by Classification

| Classification | Action | Logging |
|---|---|---|
| 🤝 FRIEND | Minimal monitoring | Debug only |
| 🛡️ ALLY | Selective monitoring | Info level |
| ⚖️ NEUTRAL | Standard monitoring | Info level |
| ⚠️ FOE | Enhanced monitoring | Warning |
| 🚨 CRITICAL_FOE | Maximum defense | Error/Critical |

---

## Example Log Output

```
[2025-01-26 14:23:45] sere_bot [INFO] 🤝 FRIEND (FRIEND): Connection from United Kingdom
                                       IP: 1.2.3.4:443
                                       Geopolitical Threat Multiplier: 0.10x

[2025-01-26 14:23:46] sere_bot [WARNING] 🔴 FOE (FOE): Connection from Russia
                                          IP: 5.6.7.8:443
                                          Geopolitical Threat Multiplier: 1.50x

[2025-01-26 14:23:47] sere_bot [CRITICAL] 🚨 CRITICAL_FOE (CRITICAL_FOE): Connection from China
                                           IP: 9.10.11.12:443
                                           Geopolitical Threat Multiplier: 1.50x
```

---

## Threat Multipliers

Adjust severity based on country stance:

```python
ALLY           → 0.10  # 90% threat reduction (safest)
PARTNER        → 0.20  # 80% threat reduction
NEUTRAL        → 0.50  # 50% threat reduction
COMPETITOR     → 1.20  # 20% threat escalation
HOSTILE        → 1.50  # 50% threat escalation (most dangerous)
UNKNOWN        → 0.50  # Medium threat (default)
LOCAL          → 0.00  # No threat (local system)
```

---

## Geopolitical Stance Categories

### ALLIES (Five Eyes)
- 🇺🇸 United States
- 🇬🇧 United Kingdom
- 🇨🇦 Canada
- 🇦🇺 Australia
- 🇳🇿 New Zealand

### PARTNERS (NATO/Friendly)
- 🇫🇷 France
- 🇩🇪 Germany
- 🇯🇵 Japan
- 🇰🇷 South Korea
- EU Nations

### COMPETITORS
- 🇵🇰 Pakistan
- 🇧🇷 Brazil
- 🇲🇽 Mexico
- 🇻🇪 Venezuela

### HOSTILE (Known APT Sources)
- 🇷🇺 Russia (FSB, GRU, SVR)
- 🇨🇳 China (PLA Unit 61398, APT1)
- 🇮🇷 Iran (IRGC, APT33, APT34)
- 🇰🇵 North Korea (Lazarus, APT38)
- 🇸🇾 Syria
- 🇨🇺 Cuba
- 🇧🇾 Belarus
- 🇲🇲 Myanmar

---

## Troubleshooting

### Database Not Found
```
Error: GeoLite2-City.mmdb not found
Solution: Download from MaxMind and place in project root
```

### Module ImportError
```
Error: No module named 'geoip2'
Solution: pip install geoip2
```

### Cache Fill
```
Issue: Memory usage increasing
Solution: Reduce GEOIP_CACHE_SIZE in CONFIG
```

### VPN Users Flagged as Foreign
```
Issue: Users on VPN flagged as FOE country
Solution: Whitelist VPN provider IPs or add context-based rules
```

---

## Performance Metrics

- **GeoIP Lookup Speed**: ~0.1 ms (local file)
- **Cache Hit Speed**: ~0.001 ms
- **Memory per 500 IPs**: ~50 KB
- **Database Size**: ~50 MB
- **Network Usage**: Zero (offline)
- **Startup Time**: <100 ms

---

## Integration Points

### With Geopolitical Consciousness
```python
if self.geopolitical_analyzer:
    analysis = self.geopolitical_analyzer.analyze_threat_geopolitically(...)
    # Full APT tracking, alliance relationships, historical context
```

### With Threat Detection
```python
classification, multiplier = self._classify_ip_threat(ip)
severity = self._assess_threat_severity_geopolitically(
    base_severity=ThreatLevel.SUBSTANTIAL,
    threat_multiplier=multiplier,
    classification=classification
)
```

### With Global Actors Database
```python
# Automatically uses GLOBAL_STATE_ACTORS database
# Covers 30+ state actors with detailed profiles
```

---

## Key Methods

| Method | Purpose | Returns |
|--------|---------|---------|
| `_classify_ip_threat(ip)` | Classify IP as friend/foe | (classification, multiplier) |
| `_assess_threat_severity_geopolitically(...)` | Adjust severity | ThreatLevel |
| `_get_classification_indicator(...)` | Get emoji/text | str (e.g., "🔴 FOE") |
| `get_geolocation_stats()` | Get full statistics | Dict |
| `geoip_manager.get_country_code(ip)` | Get country code | str (e.g., "RU") |
| `geoip_manager.get_geolocation(ip)` | Get full geo data | Dict |

---

## Security Notes

✅ **Safe Offline**: Uses local MaxMind database, zero external calls  
✅ **Private**: No user data transmitted to geolocation services  
✅ **Fast**: In-memory caching prevents repeated lookups  
✅ **Graceful**: System continues if database unavailable  

⚠️ **VPN Limitation**: Cannot detect VPN/proxy usage directly  
⚠️ **Spoofing Risk**: IPs can be spoofed via botnets  
⚠️ **Not Foolproof**: Correlate with other signals (DNS, port behavior, ASN)  

---

## References

- Full Documentation: [SERE_GEOPOLITICAL_FRIEND_FOE_SYSTEM.md](SERE_GEOPOLITICAL_FRIEND_FOE_SYSTEM.md)
- MaxMind GeoLite2: https://www.maxmind.com/en/geolite2/geolite2-free
- GeoIP2 API: https://github.com/maxmind/GeoIP2-python
- SERE Sovereign Security System: [sere_security_system.py](sere_security_system.py)

---

**Last Updated:** January 26, 2025  
**Version:** 1.0 Production  
**Status:** Ready for deployment
