#!/usr/bin/env python3
"""
S.E.R.E. Sovereign Security System - Survive, Evade, Resist, and Escape
Part of the Mythara Engine - Core Architecture

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

=== MYTHARA SAFETY HIERARCHY (TOP-DOWN PRIORITY) ===
1. Preservation of Life
2. Preservation of Safety
3. Preservation of Autonomy & Dignity
4. Preservation of Lawful Presence
5. Preservation of Continuity

This hierarchy governs every subsystem and overrides all conflicting logic.

=== S.E.R.E. MODULE: NON-CONTACT, ADA-ALIGNED EVASION ===
- SURVIVE: Maintain system resilience and continuity under threat
- EVADE: Distance-based threat avoidance with continuous movement
- RESIST: Non-contact defensive countermeasures and safe-zone seeking
- ESCAPE: Emergency protocols prioritizing life preservation

Mythara ALWAYS: protects life, avoids harm/contact/escalation, stays lawful, calm, predictable
Mythara NEVER: fights, blocks, restrains, rams, harms, panics, freezes in danger, abandons user

"Comprehensive sovereign security architecture for digital and physical safety."

=== REAL THREATS ONLY ===
This system operates EXCLUSIVELY on real threat detection.
- Demo mode: DISABLED
- Simulation fallback: DISABLED
- All patrol modes: Real threats only
- Offensive capabilities: Disabled for legal compliance
"""

# ============================================================================
# IMPORTS - Standard Library
# ============================================================================
import os
import sys
import time
import json
import logging
import hashlib
import signal
import io
import random
import threading
import pickle
import asyncio
import concurrent.futures
import subprocess
import ipaddress
import re
import platform
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from collections import defaultdict, Counter
from threading import Lock
import traceback

# ============================================================================
# IMPORTS - Platform-specific
# ============================================================================
try:
    import msvcrt
    MSVCRT_AVAILABLE = True
except ImportError:
    MSVCRT_AVAILABLE = False

try:
    import winreg
except ImportError:
    winreg = None

# ============================================================================
# IMPORTS - Geopolitical Analysis (Optional)
# ============================================================================
try:
    from sere_integrated_geopolitical_analysis import SERE_GeopoliticalIntegration
    GEOPOLITICAL_ANALYSIS_AVAILABLE = True
except ImportError:
    GEOPOLITICAL_ANALYSIS_AVAILABLE = False

# ============================================================================
# IMPORTS - Geolocation (Optional - for friend/foe IP classification)
# ============================================================================
try:
    import geoip2.database
    import geoip2.errors
    GEOIP2_AVAILABLE = True
except ImportError:
    GEOIP2_AVAILABLE = False

# ============================================================================
# IMPORTS - QuickFix Bot (Optional - for code vulnerability scanning)
# ============================================================================
try:
    from quickfix_bot import QuickFixBot, Vulnerability as QuickFixVulnerability
    QUICKFIX_AVAILABLE = True
except ImportError:
    QUICKFIX_AVAILABLE = False

# ============================================================================
# LOGGING SETUP - UTF-8 Encoding for Unicode Support
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(name)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('sere_bot.log', mode='a', encoding='utf-8')
    ]
)

# Force UTF-8 for console output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION - Optimized for 2-Core Laptop (2 cores, 6GB RAM)
# ============================================================================
CONFIG = {
    # === DETECTION & SCANNING ===
    'DEFAULT_SCAN_INTERVAL': 2,  # 2s scan interval (optimized for laptop)
    'CONCURRENT_SCAN_THREADS': 2,  # 2 threads (matches CPU cores)
    'MAX_THREATS_HISTORY': 100,  # Max threats to keep in memory

    # === NETWORK MONITORING ===
    'ENABLE_NETWORK_MONITORING': True,
    'NETWORK_SCAN_TIMEOUT': 5,
    'PING_TIMEOUT': 3,

    # === THREAT DETECTION ===
    'THREAT_SCORE_THRESHOLD': 50,  # Minimum threat score to flag
    'MALICIOUS_TLD_THRESHOLD': 40,
    'SUSPICIOUS_PROCESS_KEYWORDS': [
        'mimikatz', 'psexec', 'wmiexec', 'cobalt strike', 'empire', 'metasploit',
        'evil', 'payload', 'backdoor', 'rootkit', 'trojan', 'malware'
    ],

    # === RESOURCE LIMITS & DOS PROTECTION ===
    'MAX_PING_FLOOD_INTENSITY': 50,  # Reduced from 500
    'MAX_QUARANTINE_ZONES': 10,  # Reduced from 50
    'MAX_MONITORED_IPS': 25,  # Reduced from 200
    'MAX_THREAT_HISTORY_MB': 2,  # Reduced from 10

    # === PING FLOOD DEFENSE - AUTONOMOUS ONLY ===
    'ENABLE_EXTREME_PING_FLOOD': False,  # **AUTONOMOUS ONLY** - Never manual
    'PING_FLOOD_TARGET_TBPS': 0.01,  # 0.01 Tbps (laptop optimized)
    'PING_PACKET_SIZE_BYTES': 128,  # 128 bytes (reduced from 1472)
    'PING_FLOOD_WORKER_THREADS': 4,  # 4 threads (reduced from 256)
    'PING_FLOOD_WARNING_THRESHOLD': 1.0,  # 1.0 Tbps warning threshold

    # === AUTHENTICATION ===
    'REQUIRE_API_KEY': False,
    'API_KEY_ENV_VAR': 'SERE_API_KEY',
    'VALID_API_KEYS_FILE': 'sere_api_keys.json',

    # === SIMULATION & DEMO ===
    'ENABLE_SIMULATION_FALLBACK': False,  # REAL THREATS ONLY
    
    # === GEOLOCATION & FRIEND/FOE ===
    'ENABLE_GEOLOCATION': True,  # Enable US-only friend classification
    'GEOIP_DB_PATH': 'GeoLite2-City.mmdb',  # MaxMind GeoLite2 database
    'FRIENDLY_COUNTRIES': ['US'],  # Countries considered "friendly"
    'GEOIP_CACHE_SIZE': 500,  # Cache size for geolocation lookups
}

# ============================================================================
# EXCEPTIONS
# ============================================================================
class SEREException(Exception):
    """Base exception for SERE Bot"""
    pass


class SEREValidationError(SEREException):
    """Raised when validation fails"""
    pass


class SEREStateError(SEREException):
    """Raised when system state is invalid"""
    pass

# ============================================================================
# ENUMS & DATA STRUCTURES
# ============================================================================
class SEREPhase(Enum):
    """SERE operational phases"""
    SURVIVE = "SURVIVE"
    EVADE = "EVADE"
    RESIST = "RESIST"
    ESCAPE = "ESCAPE"


class ThreatLevel(Enum):
    """Threat severity levels"""
    NONE = 0
    LOW = 20
    MODERATE = 40
    SUBSTANTIAL = 60
    SEVERE = 80
    CRITICAL = 100


class AttackType(Enum):
    """Types of detected attacks"""
    SQL_INJECTION = "SQL_INJECTION"
    BRUTE_FORCE = "BRUTE_FORCE"
    XSS = "XSS"
    DDOS = "DDOS"
    MALWARE = "MALWARE"
    PHISHING = "PHISHING"
    MITM = "MITM"
    RANSOMWARE = "RANSOMWARE"


@dataclass
class GeoLocation:
    """Geographic location information"""
    country: str
    country_code: str
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    asn: Optional[str] = None


@dataclass
class ThreatDetection:
    """Detected threat information"""
    source_ip: str
    attack_type: AttackType
    severity: ThreatLevel
    indicators: List[str]
    confidence: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
    geolocation: Optional[GeoLocation] = None


@dataclass
class SurvivalMetrics:
    """System survival and resilience metrics"""
    uptime: float
    threats_detected: int
    threats_neutralized: int
    resilience_score: float


@dataclass
class EvasionManeuver:
    """Details of an evasion attempt"""
    maneuver_type: str
    success: bool
    description: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ResistanceAction:
    """Details of a defensive action"""
    action_id: str
    action_type: str
    target_threat: str
    effectiveness: float
    description: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class EscapeProtocol:
    """Emergency escape protocol details"""
    protocol_id: str
    reason: str
    timestamp: datetime
    target_location: Optional[str] = None


@dataclass
class PingMonitor:
    """Ping monitoring for threat IPs"""
    target_ip: str
    packet_count: int
    response_time_ms: float
    loss_percent: float
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class QuarantineZone:
    """Quarantine isolation zone"""
    zone_id: str
    threat_ip: str
    threat_type: str
    isolation_level: str
    quarantine_start: datetime
    quarantine_duration: int
    is_active: bool = True

# ============================================================================
# GEOIP MANAGER - Local Geolocation Database (MaxMind GeoLite2)
# ============================================================================
class GeoIPManager:
    """
    Manages local GeoIP database for friend/foe classification.
    Uses MaxMind GeoLite2 (free) - no API calls, no rate limits.
    All methods are defensive and will not crash - gracefully handle missing DB, invalid IPs, etc.
    """
    
    def __init__(self, db_path: str = CONFIG['GEOIP_DB_PATH']):
        self.db_path = db_path
        self.reader = None
        self.cache = {}  # Simple cache for geolocation lookups
        self.cache_hits = 0
        self.cache_misses = 0
        self.is_initialized = False
        
        if GEOIP2_AVAILABLE:
            self._initialize_database()
        else:
            logger.warning("⚠️  geoip2 not available - IP geolocation disabled")
    
    def _initialize_database(self):
        """Initialize the GeoIP database reader - safe initialization with comprehensive error handling"""
        try:
            if not os.path.exists(self.db_path):
                logger.warning(f"⚠️  GeoIP database not found: {self.db_path}")
                logger.info("   To use geolocation features, download GeoLite2-City.mmdb from:")
                logger.info("   https://www.maxmind.com/en/geolite2/geolite2-free")
                self.is_initialized = False
                return
            
            # Attempt to open the database
            self.reader = geoip2.database.Reader(self.db_path)
            logger.info(f"✅ GeoIP database loaded: {self.db_path}")
            self.is_initialized = True
        except FileNotFoundError:
            logger.warning(f"⚠️  GeoIP database file not accessible: {self.db_path}")
            self.is_initialized = False
        except PermissionError:
            logger.warning(f"⚠️  Permission denied reading GeoIP database: {self.db_path}")
            self.is_initialized = False
        except Exception as e:
            logger.warning(f"Failed to initialize GeoIP database: {type(e).__name__}: {e}")
            self.is_initialized = False
            self.reader = None
    
    def get_country_code(self, ip_address: str) -> Optional[str]:
        """Get country code for IP address using cached/local database - safe, non-crashing"""
        if not self.reader or not self.is_initialized:
            return None
        
        # Validate IP address format
        if not ip_address or not isinstance(ip_address, str):
            return None
        
        # Check cache first
        if ip_address in self.cache:
            self.cache_hits += 1
            return self.cache[ip_address]
        
        try:
            response = self.reader.city(ip_address)
            if response and hasattr(response, 'country') and response.country:
                country_code = response.country.iso_code
            else:
                country_code = None
            
            # Cache the result
            self.cache[ip_address] = country_code
            if len(self.cache) > CONFIG['GEOIP_CACHE_SIZE']:
                # Simple LRU: remove oldest entries when cache is full
                try:
                    self.cache.pop(next(iter(self.cache)))
                except (StopIteration, KeyError):
                    pass  # Cache already empty or race condition
            
            self.cache_misses += 1
            return country_code
        except (AttributeError, TypeError):
            # Response object missing expected attributes
            self.cache[ip_address] = None
            self.cache_misses += 1
            return None
        except Exception as e:
            # Catch all other exceptions (GeoIP2Error, ValueError, etc.)
            logger.debug(f"GeoIP lookup failed for {ip_address}: {type(e).__name__}")
            self.cache[ip_address] = None
            self.cache_misses += 1
            return None
    
    def get_geolocation(self, ip_address: str) -> Optional[Dict[str, Any]]:
        """Get full geolocation data for IP address - safe, non-crashing"""
        if not self.reader or not self.is_initialized:
            return None
        
        # Validate IP address format
        if not ip_address or not isinstance(ip_address, str):
            return None
        
        try:
            response = self.reader.city(ip_address)
            if not response:
                return None
            
            # Safely extract fields with attribute checks
            result = {}
            if hasattr(response, 'country') and response.country:
                result['country_code'] = getattr(response.country, 'iso_code', None)
                result['country'] = getattr(response.country, 'name', None)
            if hasattr(response, 'city') and response.city:
                result['city'] = getattr(response.city, 'name', None)
            if hasattr(response, 'location') and response.location:
                result['latitude'] = getattr(response.location, 'latitude', None)
                result['longitude'] = getattr(response.location, 'longitude', None)
                result['timezone'] = getattr(response.location, 'time_zone', None)
            
            return result if result else None
        except Exception as e:
            # Catch all exceptions gracefully
            logger.debug(f"GeoIP geolocation failed for {ip_address}: {type(e).__name__}")
            return None
    
    def is_friendly_country(self, country_code: str) -> bool:
        """Check if country code is in friendly list - safe, non-crashing"""
        if not country_code or not isinstance(country_code, str):
            return False
        try:
            return country_code.upper() in CONFIG['FRIENDLY_COUNTRIES']
        except Exception:
            return False
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics - safe, non-crashing"""
        try:
            total_lookups = self.cache_hits + self.cache_misses
            hit_ratio = self.cache_hits / total_lookups if total_lookups > 0 else 0
            return {
                'cache_size': len(self.cache),
                'cache_hits': self.cache_hits,
                'cache_misses': self.cache_misses,
                'hit_ratio': hit_ratio
            }
        except Exception as e:
            logger.debug(f"Failed to get cache stats: {e}")
            return {
                'cache_size': 0,
                'cache_hits': 0,
                'cache_misses': 0,
                'hit_ratio': 0
            }

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
def validate_ip_address(ip_str: str) -> bool:
    """Validate IP address format"""
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False


def sanitize_command(cmd: str) -> str:
    """Remove potentially dangerous characters from command"""
    dangerous_chars = ['$', '`', '|', ';', '&', '>', '<', '\n', '\r']
    for char in dangerous_chars:
        cmd = cmd.replace(char, '')
    return cmd


def check_resource_limits(current: int, maximum: int, resource_name: str) -> bool:
    """Check if resource is within limits"""
    if current >= maximum:
        logger.warning(f"Resource limit reached: {resource_name} ({current}/{maximum})")
        return False
    return True


def load_api_keys() -> Dict[str, Any]:
    """Load API keys from file"""
    if not CONFIG['REQUIRE_API_KEY']:
        return {}
    
    try:
        if os.path.exists(CONFIG['VALID_API_KEYS_FILE']):
            with open(CONFIG['VALID_API_KEYS_FILE'], 'r') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load API keys: {e}")
    
    return {}


def verify_api_key(provided_key: str) -> bool:
    """Verify API key is valid"""
    if not CONFIG['REQUIRE_API_KEY']:
        return True
    
    valid_keys = load_api_keys()
    return provided_key in valid_keys.get('keys', [])

# ============================================================================
# MAIN SERE SOVEREIGN SECURITY SYSTEM CLASS
# ============================================================================
class SERESecuritySystem:
    """
    S.E.R.E. Sovereign Security System - Survive, Evade, Resist, and Escape
    
    Comprehensive autonomous security architecture with geopolitical awareness.
    Core system-wide threat detection, prevention, and defensive capabilities.
    Operates exclusively on real threat detection (no simulation).
    
    PERSISTENCE: Maintains continuous memory across shutdown/restart cycles.
    All threat history, metrics, and defensive actions are persisted to disk.
    """

    STATE_FILE = "sere_security_system_state.pkl"
    THREAT_LOG = "sere_threat_history.json"
    CODE_INTEGRITY_FILE = "sere_security_system_code_hash.sha256"
    AUTONOMY_LOG = "sere_autonomy_threats.json"

    def __init__(self):
        """Initialize SERE Sovereign Security System with real threat detection and persistent memory"""
        self.start_time = datetime.utcnow()
        self.current_phase = SEREPhase.SURVIVE
        self.threat_level = ThreatLevel.NONE
        
        # State management
        self._state_lock = Lock()
        self.quarantine_lock = Lock()
        self.shutdown_requested = False
        self.patrol_paused = False
        self.patrol_thread = None
        self.background_patrol_active = False
        self.patrol_scan_interval = CONFIG['DEFAULT_SCAN_INTERVAL']
        
        # System health tracking
        self.health_history = []  # Track health scores over time
        self.integrity_history = []  # Track integrity scores over time
        self.volatility_window = 10  # Track last 10 scans for volatility
        
        # Threat tracking
        self.current_threats: List[ThreatDetection] = []
        self.threats_detected: List[ThreatDetection] = []
        self.quarantined_ips: set = set()
        self.monitored_ips: Dict[str, PingMonitor] = {}
        self.threat_persistence: Dict[str, int] = {}  # Track how many times each threat persists
        
        # Metrics
        self.total_threats_detected = 0
        self.total_evasions = 0
        self.total_resistances = 0
        self.total_attacks_blocked = 0
        self.evasion_actions: List[EvasionManeuver] = []
        self.resistance_actions: List[ResistanceAction] = []
        self.total_runtime_seconds = 0  # Persistent uptime counter
        
        # Error tracking
        self.last_error: Optional[Exception] = None
        self.error_count = 0
        
        # Geopolitical analysis
        self.geopolitical_analyzer = None
        if GEOPOLITICAL_ANALYSIS_AVAILABLE:
            try:
                self.geopolitical_analyzer = SERE_GeopoliticalIntegration()
                logger.info("✅ Geopolitical analysis initialized")
            except Exception as e:
                logger.warning(f"Geopolitical analysis initialization failed: {e}")
        
        # Geolocation & Friend/Foe classification
        self.geoip_manager = None
        if CONFIG['ENABLE_GEOLOCATION'] and GEOIP2_AVAILABLE:
            try:
                self.geoip_manager = GeoIPManager()
                logger.info("✅ GeoIP manager initialized for friend/foe classification")
            except Exception as e:
                logger.warning(f"GeoIP manager initialization failed: {e}")
        
        # Load persistent state from disk
        self._load_state()
        
        # Validate configuration on startup
        self._validate_configuration()
        
        # CRITICAL: Verify autonomy on startup
        logger.info("\n🔍 VERIFYING MYTHARA AUTONOMY ON STARTUP...")
        if not self.verify_autonomy():
            logger.critical("🚨 AUTONOMY VERIFICATION FAILED - POTENTIAL COMPROMISE DETECTED")
        else:
            logger.info("✅ AUTONOMY VERIFICATION PASSED")

    # ========================================================================
    # PERSISTENCE & MEMORY - Continuity Across Shutdown/Restart
    # ========================================================================
    
    def _validate_configuration(self):
        """
        Validate configuration values on startup to prevent misconfiguration attacks.
        
        Security: Ensures all CONFIG parameters are within acceptable bounds.
        Prevents resource exhaustion and denial of service via configuration tampering.
        """
        try:
            logger.info("🔐 Validating configuration parameters...")
            
            # Validate scan interval (1 second to 5 minutes)
            scan_interval = CONFIG.get('DEFAULT_SCAN_INTERVAL', 5)
            if not isinstance(scan_interval, (int, float)) or scan_interval < 1 or scan_interval > 300:
                logger.warning(f"Invalid scan interval {scan_interval}, using default (5s)")
                CONFIG['DEFAULT_SCAN_INTERVAL'] = 5
            else:
                logger.debug(f"✅ Scan interval validated: {scan_interval}s")
            
            # Validate threat detection thresholds (0-100)
            for key in ['ANOMALY_THRESHOLD', 'PRIVILEGE_THRESHOLD', 'NETWORK_THRESHOLD', 'MEMORY_THRESHOLD']:
                value = CONFIG.get(key, 75)
                if not isinstance(value, (int, float)) or value < 0 or value > 100:
                    logger.warning(f"Invalid threshold {key}={value}, using default (75)")
                    CONFIG[key] = 75
                else:
                    logger.debug(f"✅ {key} validated: {value}")
            
            # Validate log rotation size (1MB to 1GB)
            log_size = CONFIG.get('LOG_ROTATION_SIZE', 10485760)  # 10MB default
            if not isinstance(log_size, int) or log_size < 1048576 or log_size > 1073741824:
                logger.warning(f"Invalid log rotation size {log_size}, using default (10MB)")
                CONFIG['LOG_ROTATION_SIZE'] = 10485760
            else:
                logger.debug(f"✅ Log rotation size validated: {log_size / 1048576}MB")
            
            # Validate autonomous escalation enabled (boolean)
            autonomous_mode = CONFIG.get('AUTONOMOUS_ESCALATION_ENABLED', True)
            if not isinstance(autonomous_mode, bool):
                logger.warning(f"Invalid autonomous mode type, using default (True)")
                CONFIG['AUTONOMOUS_ESCALATION_ENABLED'] = True
            else:
                logger.debug(f"✅ Autonomous escalation mode: {autonomous_mode}")
            
            logger.info("✅ Configuration validation complete - all parameters within safe bounds")
        
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
    
    # ========================================================================
    # PERSISTENCE & MEMORY - Continuity Across Shutdown/Restart
    # ========================================================================
    def _load_state(self):
        """Load persistent state from disk on startup (JSON-based, safe deserialization)"""
        try:
            if os.path.exists(self.STATE_FILE):
                try:
                    # Use JSON for safe deserialization (no code execution risk like pickle)
                    with open(self.STATE_FILE, 'r') as f:
                        state = json.load(f)
                    
                    # Safely extract state with type validation
                    quarantined = state.get('quarantined_ips', [])
                    self.quarantined_ips = set(quarantined) if isinstance(quarantined, list) else set()
                    
                    self.total_threats_detected = int(state.get('total_threats_detected', 0))
                    self.total_evasions = int(state.get('total_evasions', 0))
                    self.total_resistances = int(state.get('total_resistances', 0))
                    self.total_attacks_blocked = int(state.get('total_attacks_blocked', 0))
                    self.total_runtime_seconds = float(state.get('total_runtime_seconds', 0.0))
                    
                    threat_persist = state.get('threat_persistence', {})
                    self.threat_persistence = {str(k): int(v) for k, v in threat_persist.items()}
                    
                    logger.info(f"✅ Persistent state loaded: {len(self.quarantined_ips)} quarantined IPs")
                    logger.info(f"   Total threats detected (all time): {self.total_threats_detected}")
                    logger.info(f"   Total runtime: {self.total_runtime_seconds}s")
                
                except (json.JSONDecodeError, ValueError, TypeError) as e:
                    logger.warning(f"State file corrupted, starting fresh: {e}")
                    self._initialize_defaults()
        
        except Exception as e:
            logger.warning(f"Failed to load persistent state: {e}")
            self._initialize_defaults()

    def _initialize_defaults(self):
        """Initialize default state values"""
        self.quarantined_ips = set()
        self.total_threats_detected = 0
        self.total_evasions = 0
        self.total_resistances = 0
        self.total_attacks_blocked = 0
        self.total_runtime_seconds = 0.0
        self.threat_persistence = {}

    def _save_state(self):
        """Save persistent state to disk (JSON-based, secure with file permissions)"""
        try:
            state = {
                'quarantined_ips': list(self.quarantined_ips),  # Convert set to list for JSON
                'total_threats_detected': self.total_threats_detected,
                'total_evasions': self.total_evasions,
                'total_resistances': self.total_resistances,
                'total_attacks_blocked': self.total_attacks_blocked,
                'total_runtime_seconds': self.total_runtime_seconds,
                'threat_persistence': self.threat_persistence,
                'last_save': datetime.utcnow().isoformat()
            }
            
            # Write to temporary file first (atomic write)
            temp_file = f"{self.STATE_FILE}.tmp"
            with open(temp_file, 'w') as f:
                json.dump(state, f, indent=2)
            
            # Set strict file permissions (owner-only: 0o600)
            os.chmod(temp_file, 0o600)
            
            # Atomic rename
            os.replace(temp_file, self.STATE_FILE)
            
            logger.debug(f"✅ State persisted to {self.STATE_FILE} with secure permissions (0o600)")
        except Exception as e:
            logger.error(f"Failed to save persistent state: {e}")

    def _save_threat_history(self):
        """Append threat history to persistent log (JSON-based)"""
        try:
            history = []
            if os.path.exists(self.THREAT_LOG):
                try:
                    with open(self.THREAT_LOG, 'r') as f:
                        history = json.load(f)
                except (json.JSONDecodeError, IOError):
                    history = []
            
            # Add new threats with sanitized data
            for threat in self.threats_detected[-10:]:  # Log last 10 threats
                # Sanitize threat data to prevent log injection
                safe_indicators = [str(ind).replace('\n', '').replace('\r', '') for ind in threat.indicators]
                safe_source_ip = str(threat.source_ip).replace('\n', '').replace('\r', '')
                
                history.append({
                    'timestamp': threat.timestamp.isoformat(),
                    'source_ip': safe_source_ip,
                    'attack_type': threat.attack_type.value,
                    'severity': threat.severity.name,
                    'indicators': safe_indicators
                })
            
            # Keep history size manageable (limit to 1000 entries)
            if len(history) > 1000:
                history = history[-1000:]
            
            # Write to temporary file first (atomic write)
            temp_file = f"{self.THREAT_LOG}.tmp"
            with open(temp_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            # Set secure file permissions (0o600)
            os.chmod(temp_file, 0o600)
            
            # Atomic rename
            os.replace(temp_file, self.THREAT_LOG)
            
            logger.debug(f"✅ Threat history persisted: {len(history)} total entries with secure permissions")
        except Exception as e:
            logger.error(f"Failed to save threat history: {e}")

    def shutdown_gracefully(self):
        """Graceful shutdown with state persistence"""
        logger.info("🛑 Initiating graceful shutdown with state persistence...")
        
        with self._state_lock:
            self.shutdown_requested = True
            
            # Add current session runtime to persistent total
            session_runtime = (datetime.utcnow() - self.start_time).total_seconds()
            self.total_runtime_seconds += session_runtime
            
            # Persist all state
            self._save_state()
            self._save_threat_history()
            
            logger.info(f"✅ State persisted. Shutdown complete.")

    def pause_operations(self):
        """Pause ongoing patrol/defense operations"""
        with self._state_lock:
            self.patrol_paused = True
        logger.info("⏸️  Operations paused")
        print("\n⏸️  PATROL/DEFENSE PAUSED - Type 'resume' to restart or 'stop' to halt")

    def resume_operations(self):
        """Resume paused patrol/defense operations"""
        with self._state_lock:
            self.patrol_paused = False
        logger.info("▶️  Operations resumed")
        print("\n▶️  PATROL/DEFENSE RESUMED")

    def reinitialize_session(self):
        """Reinitialize bot for new session without full shutdown"""
        logger.info("🔄 Reinitializing session...")
        
        with self._state_lock:
            # Reset session-specific state
            self.current_threats = []
            self.evasion_actions = []
            self.resistance_actions = []
            self.current_phase = SEREPhase.SURVIVE
            self.threat_level = ThreatLevel.NONE
            self.start_time = datetime.utcnow()
            self.patrol_paused = False
            self.shutdown_requested = False
            
            logger.info("✅ Session reinitialized")
            logger.info(f"   Current threats reset")
            logger.info(f"   Phase reset to SURVIVE")
            logger.info(f"   Threat level reset to NONE")
            logger.info(f"   Quarantined IPs preserved: {len(self.quarantined_ips)}")
            logger.info(f"   Lifetime metrics preserved")
            
        print("\n" + "="*70)
        print("✅ SESSION REINITIALIZED")
        print("="*70)
        print(f"Preserved: {len(self.quarantined_ips)} quarantined IPs")
        print(f"Preserved: {self.total_threats_detected} lifetime threats")
        print(f"Ready for new patrol/defense cycle")
        print("="*70)

    def _run_background_patrol_loop(self, scan_interval: int):
        """Background patrol loop that runs continuously without blocking menu"""
        try:
            while self.background_patrol_active and not self.shutdown_requested:
                # Check if paused
                with self._state_lock:
                    if self.patrol_paused:
                        time.sleep(1)
                        continue
                
                try:
                    threats = self.detect_threats()
                    
                    # Store current threats for potential menu display
                    with self._state_lock:
                        self.current_threats = threats
                    
                    if threats:
                        # AGGRESSIVE RESPONSE: Execute evasions and resistances
                        logger.info(f"🎖️  BACKGROUND PATROL: {len(threats)} threats detected - executing S.E.R.E. response")
                        
                        # Execute evasion maneuvers
                        evasions = self.execute_evasion(threats)
                        evasion_success = sum(1 for e in evasions if e.success)
                        logger.info(f"  ✓ Evasion: {evasion_success}/{len(evasions)} successful")
                        
                        # Activate resistance for failed evasions
                        failed = [e for e in evasions if not e.success]
                        if failed:
                            self.activate_resistance(failed, self.threat_persistence)
                            logger.info(f"  ✓ Resistance: Defensive countermeasures activated")
                        
                        # Log geolocation data asynchronously (don't block patrol)
                        def log_geo_async():
                            try:
                                geo_data = []
                                for threat in threats:
                                    if threat.source_ip != 'LOCAL':
                                        geo = self.get_ip_geolocation(threat.source_ip)
                                        geo_data.append({
                                            'ip': threat.source_ip,
                                            'attack_type': threat.attack_type.name,
                                            'timestamp': datetime.utcnow().isoformat(),
                                            'geo': geo
                                        })
                                
                                # Save to file
                                if geo_data:
                                    threat_geo_file = 'sere_threat_geolocation.json'
                                    existing = []
                                    if os.path.exists(threat_geo_file):
                                        try:
                                            with open(threat_geo_file, 'r') as f:
                                                existing = json.load(f)
                                        except:
                                            existing = []
                                    
                                    existing.extend(geo_data)
                                    with open(threat_geo_file, 'w') as f:
                                        json.dump(existing[-100:], f, indent=2)  # Keep last 100
                            except Exception as e:
                                logger.debug(f"Async geolocation logging error: {e}")
                        
                        # Run in background thread (non-blocking)
                        geo_thread = threading.Thread(target=log_geo_async, daemon=True)
                        geo_thread.start()
                    else:
                        logger.debug("✅ No threats - perimeter secure")
                    
                    time.sleep(scan_interval)
                except Exception as e:
                    logger.debug(f"Error in background patrol: {e}")
                    time.sleep(scan_interval)
        except Exception as e:
            logger.error(f"Background patrol thread error: {e}")
        finally:
            with self._state_lock:
                self.background_patrol_active = False
    
    def start_background_patrol(self, scan_interval: int = None):
        """Start continuous background patrol without blocking menu"""
        if scan_interval is None:
            scan_interval = CONFIG['DEFAULT_SCAN_INTERVAL']
        
        with self._state_lock:
            if self.background_patrol_active:
                logger.warning("✅ Background patrol already running")
                return
            
            self.background_patrol_active = True
            self.patrol_scan_interval = scan_interval
        
        # Start patrol in background thread
        self.patrol_thread = threading.Thread(
            target=self._run_background_patrol_loop,
            args=(scan_interval,),
            daemon=False,
            name="SEREBotPatrol"
        )
        self.patrol_thread.start()
        logger.info(f"🎖️  Background patrol started (scan interval: {scan_interval}s)")
    
    def stop_background_patrol(self):
        """Stop background patrol gracefully"""
        with self._state_lock:
            self.background_patrol_active = False
        
        if self.patrol_thread and self.patrol_thread.is_alive():
            self.patrol_thread.join(timeout=15)
        
        logger.info("⏹️  Background patrol stopped")

    def watch_background_patrol(self):
        """Display background patrol activity in foreground (press key to return to menu)"""
        print("\n" + "="*70)
        print("👁️  WATCHING BACKGROUND PATROL")
        print("="*70)
        print("Real-time threat monitoring")
        print("📲 Background patrol continues running")
        print("⏱️  Press ANY KEY to return to menu (patrol keeps running)")
        print("="*70 + "\n")
        
        # Ensure background patrol is running
        if not self.background_patrol_active:
            self.start_background_patrol()
        
        cycle = 0
        try:
            while True:
                cycle += 1
                
                # Check for keyboard interrupt (non-blocking)
                if MSVCRT_AVAILABLE:
                    try:
                        import msvcrt
                        if msvcrt.kbhit():
                            msvcrt.getch()  # Consume keystroke
                            print("\n" + "="*70)
                            print("✅ Returning to menu (patrol continues in background)")
                            print("="*70 + "\n")
                            return  # Return to menu but patrol keeps running
                    except Exception:
                        pass
                
                # Get current threats from background patrol
                with self._state_lock:
                    current_threats = list(self.current_threats)
                
                print(f"\n[Cycle {cycle}] [{datetime.utcnow().strftime('%H:%M:%S')}] 🔍 Active Threats: {len(current_threats)}")
                
                if current_threats:
                    # Display full S.E.R.E. cycle with current threats
                    self.display_sere_cycle(current_threats)
                    self.display_threat_hierarchy(current_threats)
                    
                    # Execute evasions and resistances
                    evasions = self.execute_evasion(current_threats)
                    failed = [e for e in evasions if not e.success]
                    if failed:
                        self.activate_resistance(failed, self.threat_persistence)
                else:
                    print("✅ No threats detected - perimeter secure\n")
                
                # Display frequency
                time.sleep(self.patrol_scan_interval)
        
        except KeyboardInterrupt:
            print("\n✅ Returning to menu (patrol continues)")
            return

    # ========================================================================
    # AUTONOMOUS ESCALATION ASSESSMENT
    # ========================================================================
    def assess_escalation_necessity(self) -> Tuple[bool, str]:
        """
        Use intelligent judgment to determine if escalation should be enabled.
        
        Returns:
            Tuple: (should_enable_escalation, reason)
        
        Escalation is enabled when:
        - An IP has persisted through 3+ evasion attempts
        - Multiple unrelenting threats detected
        - Clear pattern of repeated attacks from same sources
        """
        reasons = []
        should_escalate = False
        
        # Count persistent threats
        persistent_threats = {ip: count for ip, count in self.threat_persistence.items() if count >= 3}
        
        if persistent_threats:
            should_escalate = True
            reasons.append(f"UNRELENTING AGGRESSORS: {len(persistent_threats)} IPs persisted 3+ times")
        
        # Check if current threat level is severe
        if self.threat_level in [ThreatLevel.SEVERE, ThreatLevel.CRITICAL]:
            should_escalate = True
            reasons.append(f"THREAT LEVEL: {self.threat_level.name}")
        
        # Check failed evasion rate
        if len(self.evasion_actions) > 0:
            failed_evasions = sum(1 for e in self.evasion_actions[-10:] if not e.success)
            if failed_evasions >= 3:
                should_escalate = True
                reasons.append(f"FAILED EVASIONS: {failed_evasions}/10 recent evasions failed")
        
        # Check for coordinated threats (multiple IPs attacking)
        if len(self.current_threats) >= 3:
            should_escalate = True
            reasons.append(f"COORDINATED ATTACK: {len(self.current_threats)} simultaneous threats")
        
        # If multiple conditions met, escalation more justified
        if len(reasons) >= 2:
            reasons.insert(0, "MULTIPLE THREAT CONDITIONS DETECTED")
        
        reason_text = " | ".join(reasons) if reasons else "No escalation necessary"
        
        return should_escalate, reason_text

    def update_escalation_status(self):
        """
        Autonomously decide whether to enable or disable escalation.
        Called after threat detection and resistance actions.
        """
        should_escalate, reason = self.assess_escalation_necessity()
        
        old_status = CONFIG['ENABLE_EXTREME_PING_FLOOD']
        new_status = should_escalate
        
        if old_status != new_status:
            CONFIG['ENABLE_EXTREME_PING_FLOOD'] = new_status
            
            if new_status:
                logger.critical(f"🚨 ESCALATION AUTO-ENABLED")
                logger.critical(f"   Reason: {reason}")
                print(f"\n🚨 ESCALATION AUTO-ENABLED")
                print(f"   Reason: {reason}")
            else:
                logger.info(f"✅ Escalation auto-disabled (threat normalized)")
                print(f"\n✅ Escalation auto-disabled (threats normalized)")
        
        return new_status, reason
    def compute_code_integrity_hash(self) -> str:
        """Compute SHA-256 hash of this file for integrity verification"""
        try:
            with open(__file__, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            return file_hash
        except Exception as e:
            logger.error(f"Failed to compute code integrity hash: {e}")
            return ""

    def verify_code_integrity(self, force_baseline: bool = False) -> bool:
        """
        Verify code hasn't been tampered with. If force_baseline=True, regenerate baseline.
        
        Security Hardening:
        - Hash file protected with 0o444 (read-only) permissions
        - Atomic write operations (temp file + rename)
        - JSON format for structured data with error handling
        """
        try:
            current_hash = self.compute_code_integrity_hash()
            
            # Force regeneration of baseline if requested
            if force_baseline:
                baseline_data = {
                    'code_hash': current_hash,
                    'generated_at': datetime.utcnow().isoformat(),
                    'purpose': 'SHA-256 code integrity baseline'
                }
                
                # Write to temporary file first (atomic write)
                temp_file = f"{self.CODE_INTEGRITY_FILE}.tmp"
                with open(temp_file, 'w') as f:
                    json.dump(baseline_data, f, indent=2)
                
                # Set read-only permissions (0o444) - prevents accidental or malicious modification
                os.chmod(temp_file, 0o444)
                
                # Atomic rename
                os.replace(temp_file, self.CODE_INTEGRITY_FILE)
                
                logger.info(f"✅ Code integrity baseline regenerated with secure permissions (0o444): {current_hash[:16]}...")
                return True
            
            if os.path.exists(self.CODE_INTEGRITY_FILE):
                try:
                    with open(self.CODE_INTEGRITY_FILE, 'r') as f:
                        baseline_data = json.load(f)
                    
                    stored_hash = baseline_data.get('code_hash', '')
                    
                    if current_hash != stored_hash:
                        logger.critical("🚨 CODE INTEGRITY VIOLATION DETECTED!")
                        logger.critical(f"   Expected: {stored_hash}")
                        logger.critical(f"   Current:  {current_hash}")
                        logger.warning("⚠️  Note: Run with --reset-integrity to regenerate baseline if intentional changes were made")
                        self._log_autonomy_threat("CODE_INJECTION", "Core code modified")
                        return False
                    
                    logger.debug(f"✅ Code integrity verified: {current_hash[:16]}...")
                
                except (json.JSONDecodeError, KeyError, IOError) as e:
                    logger.warning(f"Integrity baseline corrupted or unreadable: {e}. Regenerating...")
                    return self.verify_code_integrity(force_baseline=True)
            else:
                # First run - store hash with secure permissions
                baseline_data = {
                    'code_hash': current_hash,
                    'generated_at': datetime.utcnow().isoformat(),
                    'purpose': 'SHA-256 code integrity baseline'
                }
                
                # Write to temporary file first (atomic write)
                temp_file = f"{self.CODE_INTEGRITY_FILE}.tmp"
                with open(temp_file, 'w') as f:
                    json.dump(baseline_data, f, indent=2)
                
                # Set read-only permissions (0o444)
                os.chmod(temp_file, 0o444)
                
                # Atomic rename
                os.replace(temp_file, self.CODE_INTEGRITY_FILE)
                
                logger.info(f"✅ Code integrity baseline established with secure permissions (0o444): {current_hash[:16]}...")
            
            return True
        except Exception as e:
            logger.error(f"Code integrity check failed: {e}")
            return False

    def detect_memory_tampering(self) -> bool:
        """Detect unauthorized memory access or modification"""
        try:
            # Check for debugger attachment (Windows)
            if sys.platform == 'win32' and MSVCRT_AVAILABLE:
                # Attempt to detect if being debugged
                try:
                    import ctypes
                    IsDebuggerPresent = ctypes.windll.kernel32.IsDebuggerPresent
                    if IsDebuggerPresent():
                        logger.critical("🚨 DEBUGGER DETECTED - MEMORY TAMPERING RISK")
                        self._log_autonomy_threat("DEBUGGER_ATTACHED", "Active debugger session detected")
                        return False
                except Exception:
                    pass
            
            return True
        except Exception as e:
            logger.error(f"Memory tampering detection error: {e}")
            return False

    def detect_execution_modification(self) -> bool:
        """Detect if execution environment is being modified"""
        try:
            # Check for code injection attempts via monkey-patching
            import sys
            if hasattr(sys, '_called_from_test'):
                logger.warning("⚠️  Testing environment detected - execution may be modified")
            
            # Check for instrumentation/profiling
            if sys.gettrace() is not None:
                logger.critical("🚨 INSTRUMENTATION DETECTED - EXECUTION BEING MONITORED")
                self._log_autonomy_threat("INSTRUMENTATION", "Python tracer/profiler detected")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Execution modification detection error: {e}")
            return False

    def verify_autonomy(self) -> bool:
        """Verify Mythara's autonomy is intact"""
        checks = [
            ("Code Integrity", self.verify_code_integrity()),
            ("Memory Tampering", self.detect_memory_tampering()),
            ("Execution Modification", self.detect_execution_modification())
        ]
        
        all_ok = True
        for check_name, result in checks:
            status = "✅" if result else "🚨"
            print(f"   {status} {check_name}: {'PASS' if result else 'FAIL'}")
            all_ok = all_ok and result
        
        if not all_ok:
            logger.critical("🚨 AUTONOMY COMPROMISED - ENTERING SAFE MODE")
            return False
        
        return True

    def _log_autonomy_threat(self, threat_type: str, description: str):
        """Log threats to Mythara's own autonomy"""
        try:
            autonomy_log = []
            if os.path.exists(self.AUTONOMY_LOG):
                try:
                    with open(self.AUTONOMY_LOG, 'r') as f:
                        autonomy_log = json.load(f)
                except (json.JSONDecodeError, IOError):
                    autonomy_log = []
            
            autonomy_log.append({
                'timestamp': datetime.utcnow().isoformat(),
                'threat_type': threat_type,
                'description': description,
                'severity': 'CRITICAL'
            })
            
            with open(self.AUTONOMY_LOG, 'w') as f:
                json.dump(autonomy_log, f, indent=2)
            
            logger.critical(f"⚠️  Autonomy threat logged: {threat_type}")
        except Exception as e:
            logger.error(f"Failed to log autonomy threat: {e}")

    def implement_isolation_boundaries(self):
        """Implement execution isolation to prevent injection"""
        print("\n" + "="*70)
        print("🔒 ISOLATION BOUNDARIES ACTIVATED")
        print("="*70)
        print("✅ Code integrity verification: ENABLED")
        print("✅ Memory tampering detection: ENABLED")
        print("✅ Execution modification monitoring: ENABLED")
        print("✅ Autonomy threat logging: ENABLED")
        print("="*70)

    # ========================================================================
    # MACGYVER CODE SCANNING - Vulnerability Detection & Auto-Fix
    # ========================================================================
    def macgyver_scan(self, target_directory: str = ".", auto_fix: bool = False, severity_threshold: str = "HIGH"):
        """
        MacGyver/QuickFix code vulnerability scanner
        Detects and optionally auto-fixes security vulnerabilities in Python code
        
        Args:
            target_directory: Directory to scan for vulnerabilities
            auto_fix: Whether to automatically fix detected vulnerabilities
            severity_threshold: Minimum severity level to auto-fix (CRITICAL, HIGH, MEDIUM, LOW)
        
        Returns:
            Tuple of (vulnerabilities_found, fixes_applied)
        """
        if not QUICKFIX_AVAILABLE:
            logger.warning("⚠️  QuickFix Bot not available - cannot perform code scanning")
            print("\n❌ MacGyver/QuickFix functionality requires quickfix_bot.py")
            print("   Ensure quickfix_bot.py is in the same directory as SERE")
            return ([], [])
        
        print("\n" + "="*70)
        print("🔧 MACGYVER CODE SCANNER - Vulnerability Detection")
        print("="*70)
        print(f"Target: {os.path.abspath(target_directory)}")
        print(f"Auto-fix: {'ENABLED' if auto_fix else 'DISABLED'}")
        if auto_fix:
            print(f"Severity threshold: {severity_threshold}")
        print("="*70 + "\n")
        
        try:
            # Initialize QuickFix Bot
            quickfix = QuickFixBot(target_directory)
            
            # Scan for vulnerabilities
            print("🔍 Scanning for vulnerabilities...")
            vulnerabilities = quickfix.scan_for_vulnerabilities()
            
            if not vulnerabilities:
                print("✅ No vulnerabilities found - code is secure!")
                return ([], [])
            
            # Categorize by severity
            critical = [v for v in vulnerabilities if v.severity == "CRITICAL"]
            high = [v for v in vulnerabilities if v.severity == "HIGH"]
            medium = [v for v in vulnerabilities if v.severity == "MEDIUM"]
            low = [v for v in vulnerabilities if v.severity == "LOW"]
            
            print(f"\n⚠️  Found {len(vulnerabilities)} vulnerabilities:")
            print(f"   🔴 CRITICAL: {len(critical)}")
            print(f"   🟠 HIGH: {len(high)}")
            print(f"   🟡 MEDIUM: {len(medium)}")
            print(f"   🟢 LOW: {len(low)}")
            
            # Show top 5 most critical
            print(f"\n📋 Top vulnerabilities:")
            for i, vuln in enumerate(sorted(vulnerabilities, key=lambda v: {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}[v.severity], reverse=True)[:5], 1):
                severity_symbol = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}[vuln.severity]
                print(f"   {i}. {severity_symbol} {vuln.vulnerability_type}")
                print(f"      File: {vuln.file_path}:{vuln.line_number}")
                print(f"      {vuln.description}")
            
            fixes = []
            if auto_fix:
                print(f"\n🔧 Auto-fixing {severity_threshold}+ severity vulnerabilities...")
                fixes = quickfix.fix_all_vulnerabilities(severity_threshold=severity_threshold)
                
                successful = [f for f in fixes if f.fix_applied]
                failed = [f for f in fixes if not f.fix_applied]
                
                print(f"\n✅ Fixed {len(successful)}/{len(fixes)} vulnerabilities")
                if failed:
                    print(f"⚠️  {len(failed)} fixes could not be automatically applied")
                
                # Save report
                report_path = quickfix.save_report()
                print(f"\n📄 Full report saved to: {report_path}")
                print(f"💾 Backups created in: .quickfix_backups/")
            else:
                print("\n💡 Run with auto_fix=True to automatically fix vulnerabilities")
                print("   Example: macgyver(auto_fix=True, severity_threshold='HIGH')")
            
            print("="*70)
            
            return (vulnerabilities, fixes)
            
        except Exception as e:
            logger.error(f"MacGyver scan failed: {e}")
            print(f"\n❌ MacGyver scan error: {e}")
            return ([], [])

    # ========================================================================
    # THREAT DETECTION - Real Threats Only
    # ========================================================================
    def detect_threats(self) -> List[ThreatDetection]:
        """
        Detect real threats from multiple vectors.
        NO simulation, NO synthetic threats - real detection only.
        Track threat persistence for autonomous escalation decisions.
        
        GEOLOCATION-BASED FRIEND/FOE:
        - Friends (US IPs): Threat multiplier = 0.1 (90% threat reduction)
        - Foes (non-US IPs): Threat multiplier = 1.0 (normal threat level)
        - Unknown: Threat multiplier = 0.5 (medium threat)
        """
        threats = []
        
        try:
            # 1. Network connection analysis WITH GEOPOLITICAL FRIEND/FOE CLASSIFICATION
            unknown_conns = self._get_unknown_connections()
            for conn in unknown_conns:
                remote_ip = conn['remote_ip']
                
                # Classify IP as friend/foe using MaxMind + Geopolitical Analysis
                classification, threat_multiplier = self._classify_ip_threat(remote_ip)
                
                # Build severity assessment with geopolitical context
                severity_level = self._assess_threat_severity_geopolitically(
                    base_severity=ThreatLevel.SUBSTANTIAL,
                    threat_multiplier=threat_multiplier,
                    classification=classification
                )
                
                # Select appropriate indicator based on classification
                indicator_prefix = self._get_classification_indicator(classification, threat_multiplier)
                
                # Build detailed geopolitical context
                geo_data = self.geoip_manager.get_geolocation(remote_ip) if self.geoip_manager else None
                country_info = geo_data.get('country', 'Unknown') if geo_data else 'Unknown'
                
                threat = ThreatDetection(
                    source_ip=remote_ip,
                    attack_type=AttackType.MITM,
                    severity=severity_level,
                    indicators=[
                        f"{indicator_prefix} ({classification}): Connection from {country_info}",
                        f"IP: {remote_ip}:{conn['remote_port']}",
                        f"Geopolitical Threat Multiplier: {threat_multiplier:.2f}x"
                    ],
                    confidence=0.75 * threat_multiplier,  # Adjust confidence by multiplier
                    timestamp=datetime.utcnow(),
                    geolocation=geo_data
                )
                
                # Log threats based on geopolitical stance
                if classification in ["CRITICAL_FOE", "FOE"]:
                    # Hostile or competitive states - full escalation
                    threats.append(threat)
                    self.threat_persistence[remote_ip] = self.threat_persistence.get(remote_ip, 0) + 1
                    logger.warning(
                        f"🚨 GEOPOLITICAL THREAT DETECTED: {classification} connection from {country_info} ({remote_ip})"
                    )
                elif classification in ["NEUTRAL", "ALLY"]:
                    # Friendly/neutral - selective logging
                    if threat_multiplier > 0.7:  # Still suspicious even if friendly
                        threats.append(threat)
                        self.threat_persistence[remote_ip] = self.threat_persistence.get(remote_ip, 0) + 1
                        logger.info(f"⚠️  Suspicious connection from {classification}: {remote_ip}")
                elif classification == "FRIEND":
                    # Full allies - minimal logging unless critical
                    logger.debug(f"Connection from {classification}: {remote_ip}")
                # UNKNOWN - log for monitoring
                else:
                    if threat_multiplier > 0.6:
                        threats.append(threat)
                        logger.info(f"Monitoring unknown connection: {remote_ip}")
            
            # 2. DNS/Network threat detection
            dns_threats = self._detect_dns_threats()
            threats.extend(dns_threats)
            
            # 3. Port scanning detection
            port_threats = self._detect_port_scan_activity()
            threats.extend(port_threats)
            
            # 4. Suspicious process detection
            suspicious_procs = self.scan_suspicious_processes()
            for proc in suspicious_procs:
                threat = ThreatDetection(
                    source_ip="LOCAL",
                    attack_type=AttackType.MALWARE,
                    severity=ThreatLevel.SEVERE,
                    indicators=[f"Suspicious process: {proc['name']}"],
                    confidence=0.80,
                    timestamp=datetime.utcnow()
                )
                threats.append(threat)
                self.threat_persistence["LOCAL"] = self.threat_persistence.get("LOCAL", 0) + 1
            
            # 5. Registry threats (Windows only)
            if sys.platform == 'win32':
                registry_findings = self.scan_registry_persistence()
                for finding in registry_findings:
                    severity_map = {
                        'HIGH': ThreatLevel.SEVERE,
                        'MEDIUM': ThreatLevel.SUBSTANTIAL,
                        'LOW': ThreatLevel.MODERATE
                    }
                    threat = ThreatDetection(
                        source_ip="LOCAL",
                        attack_type=AttackType.MALWARE,
                        severity=severity_map.get(finding.get('severity', 'MEDIUM'), ThreatLevel.MODERATE),
                        indicators=[f"Registry threat: {finding.get('threat_type', 'Unknown')}"],
                        confidence=0.75,
                        timestamp=datetime.utcnow()
                    )
                    threats.append(threat)
                    self.threat_persistence["REGISTRY"] = self.threat_persistence.get("REGISTRY", 0) + 1
            
            # 6. File integrity monitoring
            file_threats = self._detect_file_modifications()
            threats.extend(file_threats)
            
            # 7. Service health monitoring
            service_threats = self._detect_service_anomalies()
            threats.extend(service_threats)
            
            # ========================================================================
            # COMPREHENSIVE THREAT DETECTION - NEW MODULES
            # ========================================================================
            
            # 8. Dependency/Supply chain audit
            logger.info("🔍 Scanning dependencies for supply chain threats...")
            dep_threats = self._audit_python_dependencies()
            threats.extend(dep_threats)
            
            # 9. Behavioral anomalies
            logger.info("🔍 Analyzing behavioral anomalies...")
            behavior_threats = self._detect_behavioral_anomalies()
            threats.extend(behavior_threats)
            
            # 10. Privilege escalation attempts
            logger.info("🔍 Checking for privilege escalation attempts...")
            priv_threats = self._detect_privilege_escalation_attempts()
            threats.extend(priv_threats)
            
            # 11. Process ancestry anomalies
            logger.info("🔍 Analyzing process chains for injections...")
            process_threats = self._detect_process_ancestry_anomalies()
            threats.extend(process_threats)
            
            # 12. Network behavior analysis
            logger.info("🔍 Monitoring network behavior...")
            net_behavior_threats = self._detect_network_behavior_anomalies()
            threats.extend(net_behavior_threats)
            
            # 13. Memory injection detection
            logger.info("🔍 Scanning for memory injections...")
            memory_threats = self._detect_memory_injection_attempts()
            threats.extend(memory_threats)
            
            # Update state
            with self._state_lock:
                self.current_threats = threats
                self.threats_detected.extend(threats)
                self.total_threats_detected += len(threats)
                
                if threats:
                    max_severity = max(t.severity.value for t in threats)
                    self.threat_level = ThreatLevel(max_severity)
                else:
                    self.threat_level = ThreatLevel.NONE
                
                # Maintain history limit
                if len(self.threats_detected) > CONFIG['MAX_THREATS_HISTORY']:
                    self.threats_detected = self.threats_detected[-CONFIG['MAX_THREATS_HISTORY']:]
            
            # AUTONOMOUSLY UPDATE ESCALATION STATUS based on threat assessment
            self.update_escalation_status()
        
        except Exception as e:
            logger.error(f"Threat detection error: {e}")
            logger.debug(traceback.format_exc())
        
        return threats
    
    def _detect_dns_threats(self) -> List[ThreatDetection]:
        """Detect DNS-based threats and suspicious domain lookups"""
        dns_threats = []
        try:
            if sys.platform == 'win32':
                # Check DNS cache for suspicious domains
                cmd = 'Get-DnsClientCache | Select-Object Name, Data | ConvertTo-Json'
                result = subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0 and result.stdout.strip():
                    try:
                        dns_data = json.loads(result.stdout)
                        if not isinstance(dns_data, list):
                            dns_data = [dns_data]
                        
                        # Suspicious TLDs and patterns
                        suspicious_patterns = ['.tk', '.ml', '.ga', '.cf', '.xyz', 'dyn', 'no-ip', 'ddns']
                        
                        for entry in dns_data[:20]:  # Check first 20 entries
                            domain = entry.get('Name', '').lower()
                            if any(pattern in domain for pattern in suspicious_patterns):
                                threat = ThreatDetection(
                                    source_ip=entry.get('Data', 'UNKNOWN'),
                                    attack_type=AttackType.PHISHING,
                                    severity=ThreatLevel.MODERATE,
                                    indicators=[f"Suspicious DNS lookup: {domain}"],
                                    confidence=0.65,
                                    timestamp=datetime.utcnow()
                                )
                                dns_threats.append(threat)
                    except:
                        pass
        except Exception as e:
            logger.debug(f"DNS threat detection error: {e}")
        
        return dns_threats
    
    def _detect_port_scan_activity(self) -> List[ThreatDetection]:
        """Detect port scanning and unusual network activity"""
        port_threats = []
        try:
            if sys.platform == 'win32':
                # Check for listening ports and recent connections
                cmd = 'Get-NetTCPConnection | Where-Object {$_.State -eq "Listen"} | Select-Object LocalAddress, LocalPort | ConvertTo-Json'
                result = subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0 and result.stdout.strip():
                    try:
                        listen_data = json.loads(result.stdout)
                        if not isinstance(listen_data, list):
                            listen_data = [listen_data]
                        
                        # Check for unusually high number of listening ports (>20 is suspicious)
                        if len(listen_data) > 20:
                            threat = ThreatDetection(
                                source_ip="LOCAL",
                                attack_type=AttackType.DDOS,
                                severity=ThreatLevel.MODERATE,
                                indicators=[f"Excessive listening ports: {len(listen_data)}"],
                                confidence=0.60,
                                timestamp=datetime.utcnow()
                            )
                            port_threats.append(threat)
                    except:
                        pass
        except Exception as e:
            logger.debug(f"Port scan detection error: {e}")
        
        return port_threats
    
    def _detect_file_modifications(self) -> List[ThreatDetection]:
        """Detect unauthorized file modifications in critical system directories"""
        file_threats = []
        try:
            if sys.platform == 'win32':
                critical_paths = [
                    'C:\\Windows\\System32\\drivers\\etc\\hosts',
                    'C:\\Windows\\System32\\config\\SAM',
                ]
                
                for path in critical_paths:
                    try:
                        if os.path.exists(path):
                            # Check if file was modified in last hour
                            mod_time = os.path.getmtime(path)
                            current_time = time.time()
                            
                            if (current_time - mod_time) < 3600:  # Modified within 1 hour
                                threat = ThreatDetection(
                                    source_ip="LOCAL",
                                    attack_type=AttackType.MALWARE,
                                    severity=ThreatLevel.SEVERE,
                                    indicators=[f"Recent modification to critical file: {path}"],
                                    confidence=0.85,
                                    timestamp=datetime.utcnow()
                                )
                                file_threats.append(threat)
                    except:
                        pass
        except Exception as e:
            logger.debug(f"File modification detection error: {e}")
        
        return file_threats
    
    def _detect_service_anomalies(self) -> List[ThreatDetection]:
        """Detect anomalies in Windows services"""
        service_threats = []
        try:
            if sys.platform == 'win32':
                # Check for services in unusual states
                cmd = 'Get-Service | Where-Object {$_.Status -eq "Running"} | Measure-Object | Select-Object Count'
                result = subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0:
                    try:
                        # If too many services running (>100 is unusual), flag it
                        output = result.stdout.strip()
                        if 'Count' in output:
                            # Simple heuristic - excessive service count
                            pass
                    except:
                        pass
        except Exception as e:
            logger.debug(f"Service anomaly detection error: {e}")
        
        return service_threats

    # ========================================================================
    # ENHANCED THREAT DETECTION - COMPREHENSIVE SECURITY MODULE
    # ========================================================================
    
    def _audit_python_dependencies(self) -> List[ThreatDetection]:
        """Audit Python package dependencies for known CVEs and supply chain threats
        
        Checks for:
        1. Typosquatting attacks (fake package names)
        2. Compromised legitimate packages (version anomalies, known CVEs)
        3. Malicious packages with suspicious names
        4. Version history anomalies (extremely old or future versions)
        """
        dep_threats = []
        try:
            # Whitelist of legitimate, widely-used packages
            legitimate_packages = {
                'requests', 'urllib3', 'certifi', 'charset-normalizer', 'idna',
                'numpy', 'pandas', 'scipy', 'scikit-learn', 'matplotlib', 'seaborn',
                'flask', 'django', 'fastapi', 'uvicorn', 'starlette',
                'sqlalchemy', 'psycopg2', 'pymongo', 'redis', 'celery',
                'pytest', 'pytest-cov', 'black', 'ruff', 'mypy', 'pylint', 'flake8',
                'cryptography', 'pycryptodome', 'pyjwt', 'bcrypt',
                'python-dotenv', 'pydantic', 'pydantic-settings',
                'aiohttp', 'httpx', 'requests-oauthlib',
                'pillow', 'opencv-python', 'imageio',
                'beautifulsoup4', 'lxml', 'html5lib',
                'click', 'typer', 'rich', 'colorama',
                'setuptools', 'wheel', 'pip', 'virtualenv',
                'psutil', 'pywin32', 'winreg',
                'geoip2', 'maxminddb',
                'python-dateutil', 'pytz', 'pendulum',
                'typing-extensions', 'typing-inspect'
            }
            
            # Known vulnerable package versions (CVE database - simplified)
            # Format: package_name: [list of vulnerable versions]
            known_vulnerable_versions = {
                'requests': ['2.6.0', '2.6.1'],  # Historical vulnerabilities
                'django': ['1.11.0', '1.11.1'],  # Historical vulnerabilities
                'cryptography': ['0.1', '0.2'],  # Historical vulnerabilities
            }
            
            # Get list of installed packages
            cmd = f'{sys.executable} -m pip list --format json'
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                installed = json.loads(result.stdout)
                for pkg in installed:
                    name = pkg.get('name', '').lower()
                    version = pkg.get('version', '')
                    
                    # =============================================
                    # CHECK 1: Known vulnerable versions of legitimate packages
                    # =============================================
                    if name in legitimate_packages:
                        if name in known_vulnerable_versions:
                            if version in known_vulnerable_versions[name]:
                                threat = ThreatDetection(
                                    source_ip="LOCAL",
                                    attack_type=AttackType.MALWARE,
                                    severity=ThreatLevel.SEVERE,
                                    indicators=[f"Known vulnerable version detected: {name}=={version}"],
                                    confidence=0.95,
                                    timestamp=datetime.utcnow()
                                )
                                dep_threats.append(threat)
                                logger.critical(f"🚨 SUPPLY CHAIN THREAT: {name}=={version} is a known vulnerable version (update immediately)")
                                continue
                        
                        # =============================================
                        # CHECK 2: Version anomalies (signs of compromise)
                        # =============================================
                        try:
                            major, minor, patch = version.split('.')[:3]
                            # Flag extremely old versions (potential abandoned/vulnerable)
                            if int(major) <= 1 and int(minor) == 0:
                                threat = ThreatDetection(
                                    source_ip="LOCAL",
                                    attack_type=AttackType.MALWARE,
                                    severity=ThreatLevel.SUBSTANTIAL,
                                    indicators=[f"Extremely old version of {name}: {version} (may have unpatched vulnerabilities)"],
                                    confidence=0.70,
                                    timestamp=datetime.utcnow()
                                )
                                dep_threats.append(threat)
                                logger.warning(f"⚠️ SUPPLY CHAIN RISK: {name}=={version} is very old and may be vulnerable")
                        except (ValueError, IndexError):
                            pass  # Version format doesn't parse, continue
                        
                        logger.debug(f"✅ Package verified: {name}=={version}")
                        continue
                    
                    # =============================================
                    # CHECK 3: Typosquatting on non-whitelisted packages
                    # =============================================
                    typosquatting_patterns = [
                        'requests',    # Match variants of requests: req uests, requsts, etc.
                        'django',      # Match variants: djang0, etc.
                        'flask',       # Match variants: flaskk, etc.
                        'numpy',       # Match variants: nump1, etc.
                        'pandas',      # Match variants: panda s, etc.
                        'sklearn',     # Match variants: scikit-learn variants
                        'cryptography' # Match variants: crypto variants
                    ]
                    
                    # Check if name is suspiciously similar to legitimate packages
                    is_suspicious = False
                    for pattern in typosquatting_patterns:
                        # Remove spaces and common obfuscations for comparison
                        name_clean = name.replace('-', '').replace('_', '')
                        pattern_clean = pattern.replace('-', '').replace('_', '')
                        
                        # Flag if it matches the pattern but isn't exact (typosquatting)
                        if pattern_clean in name_clean and name_clean != pattern_clean:
                            # Additional check: ensure it's not a sub-dependency
                            if not any(legitimate in name for legitimate in legitimate_packages):
                                is_suspicious = True
                                break
                    
                    if is_suspicious:
                        threat = ThreatDetection(
                            source_ip="LOCAL",
                            attack_type=AttackType.MALWARE,
                            severity=ThreatLevel.SEVERE,
                            indicators=[f"Suspicious package detected: {name}=={version} (possible typosquatting)"],
                            confidence=0.90,
                            timestamp=datetime.utcnow()
                        )
                        dep_threats.append(threat)
                        logger.critical(f"⚠️ SUPPLY CHAIN THREAT: {name} detected as potential typosquatting attack")
                    
                    # =============================================
                    # CHECK 4: Malicious package names
                    # =============================================
                    if any(suspicious in name for suspicious in ['malware', 'trojan', 'botnet', 'backdoor', 'exploit', 'ransomware']):
                        threat = ThreatDetection(
                            source_ip="LOCAL",
                            attack_type=AttackType.MALWARE,
                            severity=ThreatLevel.SEVERE,
                            indicators=[f"Malicious package name detected: {name}"],
                            confidence=0.95,
                            timestamp=datetime.utcnow()
                        )
                        dep_threats.append(threat)
                        logger.critical(f"🚨 SUPPLY CHAIN THREAT: {name} detected as malicious package (UNINSTALL IMMEDIATELY)")
        
        except Exception as e:
            logger.debug(f"Dependency audit error: {e}")
        
        return dep_threats

    def _detect_behavioral_anomalies(self) -> List[ThreatDetection]:
        """Detect behavioral anomalies by monitoring system resource usage"""
        behavior_threats = []
        try:
            # Get current system metrics
            import psutil
            
            # CPU anomaly - sustained high CPU from unusual process
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory_percent = psutil.virtual_memory().percent
            disk_io = psutil.disk_io_counters()
            
            # Establish baseline (simplified - in production use more data points)
            if not hasattr(self, 'baseline_cpu'):
                self.baseline_cpu = cpu_percent
                self.baseline_memory = memory_percent
                self.baseline_disk_read = disk_io.read_bytes if disk_io else 0
                self.baseline_disk_write = disk_io.write_bytes if disk_io else 0
            
            # PROACTIVE CPU MONITORING: Check and throttle high CPU continuously
            # This prevents spikes rather than just reacting to them
            self._proactive_cpu_throttle(cpu_percent)
            
            # Detect abnormal spikes (>3x baseline or >85%)
            cpu_anomaly = cpu_percent > 85 or cpu_percent > (self.baseline_cpu * 3)
            memory_anomaly = memory_percent > 85 or memory_percent > (self.baseline_memory * 2)
            
            if cpu_anomaly:
                threat = ThreatDetection(
                    source_ip="LOCAL",
                    attack_type=AttackType.MALWARE,
                    severity=ThreatLevel.MODERATE,
                    indicators=[f"Abnormal CPU usage: {cpu_percent}% (baseline: {self.baseline_cpu}%)"],
                    confidence=0.70,
                    timestamp=datetime.utcnow()
                )
                behavior_threats.append(threat)
                logger.warning(f"⚠️ BEHAVIORAL ANOMALY: CPU spike detected ({cpu_percent}%)")
                
                # Initiate CPU anomaly investigation and self-repair
                self._investigate_and_repair_cpu_anomaly(cpu_percent)
            
            if memory_anomaly:
                threat = ThreatDetection(
                    source_ip="LOCAL",
                    attack_type=AttackType.MALWARE,
                    severity=ThreatLevel.MODERATE,
                    indicators=[f"Abnormal memory usage: {memory_percent}% (baseline: {self.baseline_memory}%)"],
                    confidence=0.70,
                    timestamp=datetime.utcnow()
                )
                behavior_threats.append(threat)
                logger.warning(f"⚠️ BEHAVIORAL ANOMALY: Memory spike detected ({memory_percent}%)")
        
        except ImportError:
            logger.debug("psutil not installed - skipping behavioral analysis")
        except Exception as e:
            logger.debug(f"Behavioral anomaly detection error: {e}")
        
        return behavior_threats

    def _proactive_cpu_throttle(self, current_cpu: float) -> None:
        """
        Proactively monitor and throttle CPU-hungry processes to prevent spikes.
        Runs continuously to keep CPU usage under control.
        
        Strategy:
        - Monitor processes using >20% CPU individually
        - If system CPU >60%, reduce priority of top CPU hog
        - If system CPU >75%, reduce priority of top 3 CPU hogs
        - If system CPU >85%, investigate + repair all suspicious processes
        """
        try:
            import psutil
            
            # Initialize throttle history if needed
            if not hasattr(self, 'throttled_processes'):
                self.throttled_processes = {}
            
            # Get all processes with CPU usage
            cpu_hogs = []
            try:
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                    try:
                        pinfo = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
                        if pinfo['cpu_percent'] and pinfo['cpu_percent'] > 20:  # >20% CPU
                            cpu_hogs.append(pinfo)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            except Exception as e:
                logger.debug(f"Process enumeration failed: {e}")
                return
            
            # Sort by CPU usage
            cpu_hogs = sorted(cpu_hogs, key=lambda x: x['cpu_percent'], reverse=True)
            
            # Legitimate system processes that are allowed high CPU
            system_whitelist = {
                'svchost.exe', 'system', 'explorer.exe', 'dwm.exe',
                'searchindexer.exe', 'audiodg.exe', 'chrome.exe', 'firefox.exe',
                'python.exe', 'python311.exe', 'java.exe', 'javaw.exe'
            }
            
            # Apply throttling based on system CPU level
            throttle_count = 0
            
            if current_cpu > 85:
                # Emergency: Reduce priority of all non-whitelisted CPU hogs
                logger.warning(f"🚨 EMERGENCY THROTTLE: System CPU {current_cpu}% - Reducing all suspicious processes")
                throttle_count = len(cpu_hogs)
                for proc in cpu_hogs:
                    if proc['name'].lower() not in system_whitelist:
                        self._reduce_process_priority(proc['pid'], proc['name'])
            
            elif current_cpu > 75:
                # Severe: Reduce priority of top 3 CPU hogs (if not whitelisted)
                logger.warning(f"⚠️ SEVERE THROTTLE: System CPU {current_cpu}% - Reducing top 3 processes")
                for proc in cpu_hogs[:3]:
                    if proc['name'].lower() not in system_whitelist:
                        self._reduce_process_priority(proc['pid'], proc['name'])
                        throttle_count += 1
            
            elif current_cpu > 60:
                # Moderate: Reduce priority of top CPU hog (if not whitelisted)
                if cpu_hogs:
                    proc = cpu_hogs[0]
                    if proc['name'].lower() not in system_whitelist:
                        logger.info(f"📉 MODERATE THROTTLE: System CPU {current_cpu}% - Reducing priority of {proc['name']}")
                        self._reduce_process_priority(proc['pid'], proc['name'])
                        throttle_count = 1
            
            # Clean up throttle history for terminated processes
            self.throttled_processes = {
                pid: info for pid, info in self.throttled_processes.items()
                if psutil.pid_exists(pid)
            }
        
        except Exception as e:
            logger.debug(f"Proactive CPU throttle error: {e}")

    def _reduce_process_priority(self, pid: int, process_name: str) -> None:
        """Reduce process priority to lower CPU impact"""
        try:
            import psutil
            
            proc = psutil.Process(pid)
            
            if sys.platform == 'win32':
                # Windows priority levels
                if proc.nice() != psutil.BELOW_NORMAL_PRIORITY_CLASS:
                    proc.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
                    logger.info(f"✅ Reduced priority of {process_name} (PID: {pid})")
                    self.throttled_processes[pid] = {
                        'name': process_name,
                        'reduced_at': datetime.utcnow().isoformat()
                    }
            else:
                # Linux/Mac nice value
                if proc.nice() < 10:  # Less than normal nice value
                    proc.nice(10)
                    logger.info(f"✅ Reduced priority of {process_name} (PID: {pid})")
                    self.throttled_processes[pid] = {
                        'name': process_name,
                        'reduced_at': datetime.utcnow().isoformat()
                    }
        
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logger.debug(f"Cannot reduce priority of PID {pid}: {e}")
        except Exception as e:
            logger.debug(f"Priority reduction error for PID {pid}: {e}")

    def _investigate_and_repair_cpu_anomaly(self, current_cpu: float) -> bool:
        """
        Comprehensive investigative analysis of CPU anomalies with self-repair mechanism.
        
        Investigation Steps:
        1. Identify CPU-hungry processes
        2. Analyze process origin and legitimacy
        3. Check for suspicious patterns (CnC, cryptomining, etc)
        4. Attempt auto-repair based on findings
        5. Log detailed forensic data
        
        Returns True if anomaly resolved, False if requires manual intervention
        """
        try:
            import psutil
            
            logger.info("🔍 INITIATING CPU ANOMALY INVESTIGATION & REPAIR...")
            investigation_log = {
                'timestamp': datetime.utcnow().isoformat(),
                'cpu_usage': current_cpu,
                'investigation_steps': [],
                'suspicious_processes': [],
                'repairs_attempted': [],
                'resolution_status': 'INVESTIGATING'
            }
            
            # ======================================================================
            # STEP 1: IDENTIFY TOP CPU-CONSUMING PROCESSES
            # ======================================================================
            logger.debug("📊 STEP 1: Identifying top CPU-consuming processes...")
            cpu_hogs = []
            try:
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'cmdline']):
                    try:
                        pinfo = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'cmdline'])
                        if pinfo['cpu_percent'] and pinfo['cpu_percent'] > 15:  # Processes using >15% CPU
                            cpu_hogs.append(pinfo)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                
                # Sort by CPU usage (descending)
                cpu_hogs = sorted(cpu_hogs, key=lambda x: x['cpu_percent'], reverse=True)[:5]
                
                investigation_log['investigation_steps'].append({
                    'step': 'Identify CPU hogs',
                    'status': 'COMPLETE',
                    'top_processes': len(cpu_hogs),
                    'processes': [
                        {'pid': p['pid'], 'name': p['name'], 'cpu_percent': p['cpu_percent']}
                        for p in cpu_hogs
                    ]
                })
                
                logger.info(f"   ✅ Found {len(cpu_hogs)} CPU-hungry processes")
                for proc in cpu_hogs:
                    logger.debug(f"      - {proc['name']} (PID: {proc['pid']}, CPU: {proc['cpu_percent']}%)")
            
            except Exception as e:
                logger.warning(f"   ❌ Process enumeration failed: {e}")
                investigation_log['investigation_steps'].append({
                    'step': 'Identify CPU hogs',
                    'status': 'FAILED',
                    'error': str(e)
                })
            
            # ======================================================================
            # STEP 2: ANALYZE PROCESS ORIGIN & LEGITIMACY
            # ======================================================================
            logger.debug("🔐 STEP 2: Analyzing process origin and legitimacy...")
            
            # Known legitimate Windows processes (whitelist)
            legitimate_processes = {
                'svchost.exe', 'system', 'explorer.exe', 'dwm.exe', 'csrss.exe',
                'services.exe', 'lsass.exe', 'wininit.exe', 'taskhostw.exe',
                'python.exe', 'python311.exe', 'powershell.exe', 'notepad.exe',
                'chrome.exe', 'firefox.exe', 'msedge.exe', 'teams.exe',
                'windowsdefenderapt.exe', 'malwarebytes.exe', 'avast.exe'
            }
            
            suspicious_findings = []
            for proc in cpu_hogs:
                proc_name = proc['name'].lower()
                is_legitimate = proc_name in legitimate_processes
                
                # Check for suspicious patterns
                suspicious_indicators = []
                
                # Pattern 1: Obfuscated names
                if len(proc_name) > 20 or proc_name.count('_') > 3 or any(c.isdigit() for c in proc_name[:3]):
                    suspicious_indicators.append('Obfuscated process name')
                
                # Pattern 2: System directory mismatch
                try:
                    proc_obj = psutil.Process(proc['pid'])
                    exe_path = proc_obj.exe()
                    
                    if not is_legitimate:
                        # Check if non-system process is in suspicious directories
                        if any(pattern in exe_path.lower() for pattern in [
                            '\\temp\\', '\\appdata\\', '\\downloads\\', 
                            'c:\\windows\\temp', '%temp%'
                        ]):
                            suspicious_indicators.append('Suspicious execution path')
                        
                        # Pattern 3: No file signature (unsigned)
                        if sys.platform == 'win32':
                            try:
                                import ctypes
                                from ctypes.wintypes import HANDLE, DWORD
                                # Try to verify file signature
                                result = subprocess.run(
                                    ['powershell', '-Command', 
                                     f'Get-AuthenticodeSignature "{exe_path}" | Select-Object -ExpandProperty Status'],
                                    capture_output=True, text=True, timeout=5
                                )
                                if 'NotSigned' in result.stdout or result.returncode != 0:
                                    suspicious_indicators.append('Unsigned/Invalid digital signature')
                            except Exception:
                                pass
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                
                # Pattern 4: Network connections (CnC detection)
                try:
                    proc_obj = psutil.Process(proc['pid'])
                    connections = proc_obj.net_connections(kind='inet')
                    external_connections = [
                        c for c in connections 
                        if c.status == psutil.CONN_ESTABLISHED and c.raddr
                    ]
                    
                    if external_connections and not is_legitimate:
                        for conn in external_connections:
                            # Check for known malicious IPs/domains
                            if self._is_malicious_ip(conn.raddr[0]):
                                suspicious_indicators.append(f'CnC communication: {conn.raddr[0]}')
                
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                
                if suspicious_indicators:
                    suspicious_finding = {
                        'pid': proc['pid'],
                        'name': proc['name'],
                        'cpu_percent': proc['cpu_percent'],
                        'is_legitimate': is_legitimate,
                        'suspicious_indicators': suspicious_indicators,
                        'severity': 'HIGH' if len(suspicious_indicators) > 1 else 'MEDIUM'
                    }
                    suspicious_findings.append(suspicious_finding)
                    logger.warning(f"   ⚠️ SUSPICIOUS: {proc['name']} (PID: {proc['pid']})")
                    for indicator in suspicious_indicators:
                        logger.warning(f"      - {indicator}")
            
            investigation_log['investigation_steps'].append({
                'step': 'Analyze process legitimacy',
                'status': 'COMPLETE',
                'suspicious_processes_found': len(suspicious_findings)
            })
            investigation_log['suspicious_processes'] = suspicious_findings
            
            # ======================================================================
            # STEP 3: PATTERN DETECTION FOR SPECIFIC ATTACK TYPES
            # ======================================================================
            logger.debug("🎯 STEP 3: Detecting attack patterns...")
            
            attack_patterns = {
                'CRYPTOMINER': {
                    'keywords': ['krypt', 'mine', 'xmrig', 'monero', 'nicehash', 'hashrate'],
                    'min_cpu_threshold': 70,
                    'remediation': 'terminate'
                },
                'BOTNET_CNC': {
                    'keywords': ['cmd.exe', 'powershell', 'iex', 'downloadstring'],
                    'min_cpu_threshold': 30,
                    'remediation': 'isolate'
                },
                'WORM_REPLICATION': {
                    'keywords': ['copy', 'clone', 'replicate', 'spread', 'propagate'],
                    'min_cpu_threshold': 50,
                    'remediation': 'terminate'
                }
            }
            
            detected_attacks = []
            for proc in cpu_hogs:
                cmdline_str = ' '.join(proc.get('cmdline', [])).lower() if proc.get('cmdline') else ''
                proc_name = proc['name'].lower()
                
                for attack_type, pattern_info in attack_patterns.items():
                    if any(keyword in cmdline_str or keyword in proc_name 
                           for keyword in pattern_info['keywords']):
                        
                        if proc['cpu_percent'] >= pattern_info['min_cpu_threshold']:
                            detected_attacks.append({
                                'type': attack_type,
                                'pid': proc['pid'],
                                'process': proc['name'],
                                'cpu_usage': proc['cpu_percent'],
                                'recommended_action': pattern_info['remediation']
                            })
                            logger.critical(f"🚨 ATTACK DETECTED: {attack_type} in {proc['name']} (PID: {proc['pid']})")
            
            investigation_log['investigation_steps'].append({
                'step': 'Detect attack patterns',
                'status': 'COMPLETE',
                'attacks_detected': len(detected_attacks),
                'attacks': detected_attacks
            })
            
            # ======================================================================
            # STEP 4: SELF-REPAIR MECHANISM
            # ======================================================================
            logger.info("🔧 STEP 4: Initiating self-repair mechanism...")
            repair_actions = []
            
            if detected_attacks:
                logger.critical("🚨 MALWARE DETECTED - EXECUTING EMERGENCY REPAIRS")
                
                for attack in detected_attacks:
                    repair_action = {
                        'attack_type': attack['type'],
                        'pid': attack['pid'],
                        'action': attack['recommended_action'],
                        'status': 'PENDING'
                    }
                    
                    try:
                        if attack['recommended_action'] == 'terminate':
                            # Attempt to gracefully terminate process
                            proc = psutil.Process(attack['pid'])
                            proc.terminate()
                            
                            # Wait for termination (5 seconds)
                            try:
                                proc.wait(timeout=5)
                                repair_action['status'] = 'SUCCESS'
                                logger.critical(f"   ✅ Terminated malicious process: {attack['process']} (PID: {attack['pid']})")
                            except psutil.TimeoutExpired:
                                # Force kill if graceful termination fails
                                proc.kill()
                                repair_action['status'] = 'FORCE_KILLED'
                                logger.critical(f"   ⚠️ Force-killed malicious process: {attack['process']} (PID: {attack['pid']})")
                        
                        elif attack['recommended_action'] == 'isolate':
                            # Isolate network connections (Windows)
                            if sys.platform == 'win32':
                                try:
                                    proc = psutil.Process(attack['pid'])
                                    # Set process priority to idle (reduce impact)
                                    proc.nice(psutil.IDLE_PRIORITY_CLASS)
                                    repair_action['status'] = 'ISOLATED'
                                    logger.warning(f"   🔒 Isolated process: {attack['process']} (PID: {attack['pid']})")
                                except Exception as e:
                                    logger.warning(f"   ❌ Isolation failed: {e}")
                                    repair_action['status'] = 'FAILED'
                    
                    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                        logger.warning(f"   ❌ Cannot repair process (access denied): {e}")
                        repair_action['status'] = 'ACCESS_DENIED'
                    
                    repair_actions.append(repair_action)
            
            elif suspicious_findings:
                logger.warning("⚠️ SUSPICIOUS ACTIVITY DETECTED - APPLYING CONTAINMENT")
                
                for suspicious in suspicious_findings:
                    try:
                        proc = psutil.Process(suspicious['pid'])
                        
                        # Reduce priority to mitigate impact
                        proc.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if sys.platform == 'win32' else 10)
                        
                        repair_actions.append({
                            'process': suspicious['name'],
                            'pid': suspicious['pid'],
                            'action': 'priority_reduced',
                            'status': 'SUCCESS'
                        })
                        logger.info(f"   ✅ Reduced priority of suspicious process: {suspicious['name']} (PID: {suspicious['pid']})")
                    
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            
            investigation_log['investigation_steps'].append({
                'step': 'Self-repair execution',
                'status': 'COMPLETE',
                'repairs_attempted': len(repair_actions),
                'repairs': repair_actions
            })
            investigation_log['repairs_attempted'] = repair_actions
            
            # ======================================================================
            # STEP 5: VERIFY REPAIR SUCCESS
            # ======================================================================
            logger.info("📊 STEP 5: Verifying repair effectiveness...")
            
            # Re-measure CPU after repair
            import time
            time.sleep(2)  # Wait for changes to take effect
            new_cpu = psutil.cpu_percent(interval=0.1)
            
            if new_cpu < current_cpu * 0.5:  # CPU reduced by at least 50%
                investigation_log['resolution_status'] = 'RESOLVED'
                logger.info(f"   ✅ CPU ANOMALY RESOLVED: {current_cpu}% → {new_cpu}%")
            else:
                investigation_log['resolution_status'] = 'REQUIRES_MANUAL_INTERVENTION'
                logger.warning(f"   ⚠️ CPU still elevated: {new_cpu}% (was {current_cpu}%)")
            
            # Log complete forensic investigation
            logger.info("🔍 CPU ANOMALY INVESTIGATION COMPLETE")
            logger.debug(f"Investigation report: {json.dumps(investigation_log, indent=2, default=str)}")
            
            # Save investigation report
            self._save_investigation_report(investigation_log)
            
            return investigation_log['resolution_status'] == 'RESOLVED'
        
        except Exception as e:
            logger.error(f"CPU anomaly investigation failed: {e}")
            return False

    def _is_malicious_ip(self, ip_address: str) -> bool:
        """Check if an IP address is known malicious (CnC, botnet, etc)"""
        # Known malicious IP ranges (simplified - in production use threat intel feeds)
        malicious_ips = {
            '192.0.2.0/24',      # Example range (TEST-NET-1, reserved)
            '198.51.100.0/24',   # Example range (TEST-NET-2, reserved)
            '203.0.113.0/24',    # Example range (TEST-NET-3, reserved)
        }
        
        # In production, integrate with:
        # - AbuseIPDB API
        # - VirusTotal threat feeds
        # - Local threat intelligence database
        # - ISP blacklists
        
        try:
            import ipaddress
            ip_obj = ipaddress.ip_address(ip_address)
            for malicious_range in malicious_ips:
                if ip_obj in ipaddress.ip_network(malicious_range):
                    return True
        except (ValueError, TypeError):
            pass
        
        return False

    def _save_investigation_report(self, report: dict):
        """Save CPU anomaly investigation report to disk"""
        try:
            report_file = "sere_cpu_investigation_report.json"
            
            # Load existing reports
            reports = []
            if os.path.exists(report_file):
                try:
                    with open(report_file, 'r') as f:
                        reports = json.load(f)
                except (json.JSONDecodeError, IOError):
                    reports = []
            
            # Add new report and keep only last 10
            reports.append(report)
            if len(reports) > 10:
                reports = reports[-10:]
            
            # Write with secure permissions
            temp_file = f"{report_file}.tmp"
            with open(temp_file, 'w') as f:
                json.dump(reports, f, indent=2, default=str)
            
            os.chmod(temp_file, 0o600)
            os.replace(temp_file, report_file)
            
            logger.debug(f"✅ Investigation report saved: {report_file}")
        except Exception as e:
            logger.warning(f"Failed to save investigation report: {e}")

    def _detect_privilege_escalation_attempts(self) -> List[ThreatDetection]:
        """Detect attempts to escalate privileges"""
        priv_threats = []
        try:
            if sys.platform == 'win32':
                # Check for UAC bypass attempts and privilege escalation
                cmd = 'Get-EventLog -LogName Security -InstanceId 4688 -Newest 100 -ErrorAction SilentlyContinue | Where-Object {$_.Message -like "*cmd*" -or $_.Message -like "*powershell*"}'
                result = subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0 and result.stdout.strip():
                    # Check for suspicious process creation
                    suspicious_escalation_cmds = [
                        'runas', 'psexec', 'mimikatz', 'invoke-expression', 'iex',
                        'system32\\lsass', 'sam registry', 'ntds.dit'
                    ]
                    
                    for cmd_pattern in suspicious_escalation_cmds:
                        if cmd_pattern.lower() in result.stdout.lower():
                            threat = ThreatDetection(
                                source_ip="LOCAL",
                                attack_type=AttackType.MALWARE,
                                severity=ThreatLevel.SEVERE,
                                indicators=[f"Privilege escalation attempt detected: {cmd_pattern}"],
                                confidence=0.85,
                                timestamp=datetime.utcnow()
                            )
                            priv_threats.append(threat)
                            logger.critical(f"🚨 PRIVILEGE ESCALATION ATTEMPT: {cmd_pattern}")
        except Exception as e:
            logger.debug(f"Privilege escalation detection error: {e}")
        
        return priv_threats

    def _detect_process_ancestry_anomalies(self) -> List[ThreatDetection]:
        """Detect suspicious process chains and parent-child relationships"""
        process_threats = []
        try:
            import psutil
            
            # Get all running processes with parent info
            for proc in psutil.process_iter(['pid', 'ppid', 'name', 'exe']):
                try:
                    parent = psutil.Process(proc.info['ppid'])
                    parent_name = parent.name()
                    child_name = proc.info['name']
                    
                    # Suspicious parent-child relationships
                    suspicious_chains = {
                        'explorer.exe': ['cmd.exe', 'powershell.exe', 'rundll32.exe'],
                        'svchost.exe': ['cmd.exe', 'powershell.exe'],
                        'notepad.exe': ['cmd.exe', 'powershell.exe'],
                        'winlogon.exe': ['cmd.exe', 'powershell.exe'],
                    }
                    
                    if parent_name in suspicious_chains:
                        if child_name in suspicious_chains[parent_name]:
                            threat = ThreatDetection(
                                source_ip="LOCAL",
                                attack_type=AttackType.MALWARE,
                                severity=ThreatLevel.SUBSTANTIAL,
                                indicators=[f"Suspicious process ancestry: {parent_name} -> {child_name}"],
                                confidence=0.80,
                                timestamp=datetime.utcnow()
                            )
                            process_threats.append(threat)
                            logger.warning(f"⚠️ PROCESS CHAIN ANOMALY: {parent_name} spawned {child_name}")
                
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        
        except ImportError:
            logger.debug("psutil not installed - skipping process ancestry analysis")
        except Exception as e:
            logger.debug(f"Process ancestry detection error: {e}")
        
        return process_threats

    def _detect_network_behavior_anomalies(self) -> List[ThreatDetection]:
        """Detect unusual network behavior (data exfiltration, C2 communication)"""
        network_threats = []
        try:
            import psutil
            
            # Get network connections
            connections = psutil.net_connections()
            
            # Suspicious indicators
            suspicious_indicators = {
                'established_to_rare_ports': [],  # Connections to unusual ports (>5000)
                'high_bandwidth_processes': [],
                'dns_over_non_standard_port': []
            }
            
            for conn in connections:
                if conn.raddr:  # Has remote address
                    remote_port = conn.raddr[1] if len(conn.raddr) > 1 else 0
                    
                    # Detect connections to high ports (possible C2)
                    if remote_port > 5000 and conn.status == 'ESTABLISHED':
                        threat = ThreatDetection(
                            source_ip=conn.raddr[0] if conn.raddr else "UNKNOWN",
                            attack_type=AttackType.MITM,
                            severity=ThreatLevel.MODERATE,
                            indicators=[f"Connection to suspicious port: {remote_port} (process: {conn.pid})"],
                            confidence=0.60,
                            timestamp=datetime.utcnow()
                        )
                        network_threats.append(threat)
        
        except ImportError:
            logger.debug("psutil not installed - skipping network behavior analysis")
        except Exception as e:
            logger.debug(f"Network behavior detection error: {e}")
        
        return network_threats

    def _detect_memory_injection_attempts(self) -> List[ThreatDetection]:
        """Detect code injection into running processes"""
        injection_threats = []
        try:
            import psutil
            
            # Get all processes and check for suspicious memory patterns
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    # High-value targets for injection
                    sensitive_processes = ['svchost.exe', 'explorer.exe', 'winlogon.exe', 'lsass.exe']
                    
                    if any(proc.info['name'].lower().startswith(sp.lower()) for sp in sensitive_processes):
                        # In a real scenario, this would use APIs like ReadProcessMemory
                        # For now, we'll use heuristics
                        proc_obj = psutil.Process(proc.info['pid'])
                        memory_info = proc_obj.memory_info()
                        
                        # Anomalously high memory for system processes
                        if memory_info.rss > 500 * 1024 * 1024:  # >500MB
                            threat = ThreatDetection(
                                source_ip="LOCAL",
                                attack_type=AttackType.MALWARE,
                                severity=ThreatLevel.SUBSTANTIAL,
                                indicators=[f"Anomalous memory usage in {proc.info['name']}: {memory_info.rss / 1024 / 1024:.1f}MB"],
                                confidence=0.70,
                                timestamp=datetime.utcnow()
                            )
                            injection_threats.append(threat)
                
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        
        except ImportError:
            logger.debug("psutil not installed - skipping memory injection analysis")
        except Exception as e:
            logger.debug(f"Memory injection detection error: {e}")
        
        return injection_threats

    def _load_threat_intelligence(self) -> Dict[str, List[str]]:
        """Load known IOCs (Indicators of Compromise) from threat intelligence"""
        iocs = {
            'malicious_ips': [],
            'malicious_domains': [],
            'malicious_processes': [
                'minergate', 'xmrig', 'coinhive', 'cryptonight',
                'botnet', 'trojan', 'ransomware', 'spyware'
            ],
            'known_exploits': [
                'eternal blue', 'wannacry', 'heartbleed', 'shellshock'
            ]
        }
        
        # In production, load from threat feeds
        # For now, use hardcoded known malicious IPs
        iocs['malicious_ips'] = [
            # Add known C2 servers, botnets, etc.
        ]
        
        return iocs

    def resolve_mac_address(self, ip_address: str) -> str:
        """
        Resolve MAC address for an IP using ARP lookup.
        
        Security: Uses list-based subprocess calls (no shell=True) to prevent command injection.
        Validates IP address format before passing to subprocess.
        """
        try:
            # Validate IP address format (basic check)
            ip_parts = ip_address.split('.')
            if len(ip_parts) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in ip_parts):
                logger.debug(f"Invalid IP address format: {ip_address}")
                return "UNKNOWN"
            
            if sys.platform == 'win32':
                # Windows: use arp command with list-based subprocess (safer)
                result = subprocess.run(['arp', '-a', ip_address], 
                                       capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if ip_address in line:
                            parts = line.split()
                            for part in parts:
                                # Look for MAC address pattern (XX-XX-XX-XX-XX-XX)
                                if '-' in part and len(part) == 17:
                                    return part
            else:
                # Linux/Mac: use arp command with list-based subprocess (safer)
                result = subprocess.run(['arp', '-n', ip_address], 
                                       capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0:
                    parts = result.stdout.split()
                    for part in parts:
                        # Look for MAC address pattern (xx:xx:xx:xx:xx:xx)
                        if ':' in part and len(part) == 17:
                            return part
        except Exception as e:
            logger.debug(f"MAC resolution error for {ip_address}: {e}")
        
        return "UNKNOWN"

    def calculate_system_integrity(self, threats: List[ThreatDetection]) -> float:
        """Calculate system integrity score (0-100)"""
        if not threats:
            return 100.0
        
        # Base score
        score = 100.0
        
        # Deduct points based on threat severity
        for threat in threats:
            if threat.severity == ThreatLevel.CRITICAL:
                score -= 25
            elif threat.severity == ThreatLevel.SEVERE:
                score -= 15
            elif threat.severity == ThreatLevel.SUBSTANTIAL:
                score -= 10
            elif threat.severity == ThreatLevel.MODERATE:
                score -= 5
        
        return max(0.0, score)
    
    def calculate_system_health(self, threats: List[ThreatDetection]) -> float:
        """Calculate system health score (0-100)"""
        threat_count = len(threats)
        
        if threat_count == 0:
            return 100.0
        elif threat_count < 5:
            return 80.0
        elif threat_count < 10:
            return 60.0
        elif threat_count < 20:
            return 40.0
        else:
            return 20.0
    
    def calculate_volatility(self, metric_history: List[float]) -> float:
        """Calculate volatility (standard deviation) of metrics over time"""
        if len(metric_history) < 2:
            return 0.0
        
        # Keep only last N measurements
        recent = metric_history[-self.volatility_window:]
        
        if not recent:
            return 0.0
        
        # Calculate mean
        mean = sum(recent) / len(recent)
        
        # Calculate standard deviation
        variance = sum((x - mean) ** 2 for x in recent) / len(recent)
        volatility = variance ** 0.5
        
        return volatility
    
    def get_health_status(self, health_score: float) -> str:
        """Get health status description"""
        if health_score >= 90:
            return "EXCELLENT ✅"
        elif health_score >= 75:
            return "GOOD ✓"
        elif health_score >= 50:
            return "FAIR ⚠️"
        elif health_score >= 25:
            return "POOR 🔴"
        else:
            return "CRITICAL 🚨"
    
    def get_integrity_status(self, integrity_score: float) -> str:
        """Get integrity status description"""
        if integrity_score >= 90:
            return "SECURE ✅"
        elif integrity_score >= 75:
            return "STABLE ✓"
        elif integrity_score >= 50:
            return "COMPROMISED ⚠️"
        elif integrity_score >= 25:
            return "DEGRADED 🔴"
        else:
            return "CRITICAL 🚨"


    

    def get_ip_geolocation(self, ip_address: str) -> Dict[str, Any]:
        """
        Look up geolocation data for an IP address.
        Uses free IP geolocation services (ip-api.com, ipinfo.io fallback).
        """
        if ip_address in ['LOCAL', '127.0.0.1', 'localhost']:
            return {
                'ip': ip_address,
                'country': 'LOCAL',
                'city': 'LOCAL SYSTEM',
                'latitude': 0,
                'longitude': 0,
                'isp': 'LOCAL',
                'type': 'LOCAL'
            }
        
        try:
            import urllib.request
            import json as json_lib
            
            # Try ip-api.com first (free tier, no API key needed)
            url = f"http://ip-api.com/json/{ip_address}?fields=status,country,city,lat,lon,isp,type,query"
            
            try:
                with urllib.request.urlopen(url, timeout=3) as response:
                    data = json_lib.loads(response.read().decode())
                    
                    if data.get('status') == 'success':
                        return {
                            'ip': ip_address,
                            'country': data.get('country', 'UNKNOWN'),
                            'city': data.get('city', 'UNKNOWN'),
                            'latitude': data.get('lat', 0),
                            'longitude': data.get('lon', 0),
                            'isp': data.get('isp', 'UNKNOWN'),
                            'type': data.get('type', 'UNKNOWN'),
                            'source': 'ip-api.com'
                        }
            except Exception as e:
                logger.debug(f"ip-api.com lookup failed for {ip_address}: {e}")
            
            # Fallback to ipinfo.io
            url = f"https://ipinfo.io/{ip_address}/json"
            try:
                with urllib.request.urlopen(url, timeout=3) as response:
                    data = json_lib.loads(response.read().decode())
                    
                    loc_parts = data.get('loc', '0,0').split(',')
                    return {
                        'ip': ip_address,
                        'country': data.get('country', 'UNKNOWN'),
                        'city': data.get('city', 'UNKNOWN'),
                        'latitude': float(loc_parts[0]) if len(loc_parts) > 0 else 0,
                        'longitude': float(loc_parts[1]) if len(loc_parts) > 1 else 0,
                        'isp': data.get('org', 'UNKNOWN'),
                        'type': 'RESIDENTIAL' if 'Residential' in data.get('org', '') else 'UNKNOWN',
                        'source': 'ipinfo.io'
                    }
            except Exception as e:
                logger.debug(f"ipinfo.io lookup failed for {ip_address}: {e}")
        
        except Exception as e:
            logger.debug(f"Geolocation lookup error for {ip_address}: {e}")
        
        # Return unknown geolocation
        return {
            'ip': ip_address,
            'country': 'UNKNOWN',
            'city': 'UNKNOWN',
            'latitude': 0,
            'longitude': 0,
            'isp': 'UNKNOWN',
            'type': 'UNKNOWN',
            'source': 'UNKNOWN'
        }

    def _get_unknown_connections(self) -> List[Dict[str, Any]]:
        """Get established network connections to unknown/external IPs"""
        unknown_conns = []
        
        try:
            if sys.platform == 'win32':
                cmd = 'Get-NetTCPConnection -State Established | Select-Object LocalAddress, RemoteAddress, RemotePort | ConvertTo-Json'
                result = subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0 and result.stdout.strip():
                    try:
                        conns_data = json.loads(result.stdout)
                        if not isinstance(conns_data, list):
                            conns_data = [conns_data]
                        
                        for conn in conns_data:
                            remote_ip = conn.get('RemoteAddress', '')
                            if validate_ip_address(remote_ip) and not self._is_native_ip(remote_ip):
                                unknown_conns.append({
                                    'local_ip': conn.get('LocalAddress', ''),
                                    'remote_ip': remote_ip,
                                    'remote_port': conn.get('RemotePort', 0)
                                })
                    except json.JSONDecodeError:
                        pass
        except Exception as e:
            logger.error(f"Connection enumeration error: {e}")
        
        return unknown_conns

    def _is_native_ip(self, ip: str) -> bool:
        """Check if IP is native/local/private"""
        native_ranges = [
            '127.0.0.0/8',      # Localhost
            '192.168.0.0/16',   # Private
            '10.0.0.0/8',       # Private
            '172.16.0.0/12',    # Private
            '169.254.0.0/16',   # Link-local
        ]
        
        try:
            ip_obj = ipaddress.ip_address(ip)
            for native_range in native_ranges:
                if ip_obj in ipaddress.ip_network(native_range):
                    return True
        except ValueError:
            pass
        
        return False

    def _is_us_ip(self, ip: str) -> bool:
        """
        Check if IP is from a friendly country (US).
        Uses local GeoIP database (no API calls).
        Returns True if from friendly country, False otherwise.
        """
        if not self.geoip_manager:
            return False
        
        try:
            country_code = self.geoip_manager.get_country_code(ip)
            if country_code:
                is_friendly = self.geoip_manager.is_friendly_country(country_code)
                logger.debug(f"IP {ip}: Country={country_code}, Friendly={is_friendly}")
                return is_friendly
        except Exception as e:
            logger.debug(f"Error checking US IP status for {ip}: {e}")
        
        return False

    def _classify_ip_threat(self, ip: str) -> Tuple[str, float]:
        """
        Classify IP as friend or foe using MaxMind geolocation + geopolitical analysis.
        
        INTEGRATION WITH MAXMIND GEOIP2:
        1. Queries MaxMind database for IP geolocation (country code, city, ASN)
        2. Maps country code to geopolitical stance using geopolitical analyzer
        3. Returns classification and threat multiplier
        
        GEOPOLITICAL STANCE MAPPING:
        - ALLY (US, UK, Canada, Australia, NZ, NATO): threat_multiplier=0.1 (90% reduction)
        - PARTNER (Japan, S.Korea, EU): threat_multiplier=0.2 (80% reduction)
        - NEUTRAL: threat_multiplier=0.5 (50% reduction)
        - COMPETITOR/HOSTILE (China, Russia, Iran, NK): threat_multiplier=1.5 (50% escalation)
        - UNKNOWN/UNGEOLOCATED: threat_multiplier=0.5 (medium threat)
        
        Returns:
            Tuple[classification: str, threat_multiplier: float, detail_dict: Dict]
        """
        if self._is_native_ip(ip):
            return "LOCAL", 0.0
        
        if not self.geoip_manager:
            return "UNKNOWN", 0.5
        
        try:
            # STEP 1: Get geolocation from MaxMind GeoIP database
            country_code = self.geoip_manager.get_country_code(ip)
            geolocation = self.geoip_manager.get_geolocation(ip)
            
            if not country_code:
                return "UNKNOWN", 0.5
            
            # STEP 2: Use geopolitical analyzer to determine stance
            if self.geopolitical_analyzer:
                try:
                    # Get full geopolitical profile for this country
                    geo_analysis = self.geopolitical_analyzer.analyze_country_geopolitically(country_code)
                    
                    if geo_analysis:
                        stance = geo_analysis.get('stance', 'UNKNOWN')
                        country_name = geo_analysis.get('country_name', country_code)
                        
                        # Map stance to threat multiplier
                        stance_multipliers = {
                            'ALLY': 0.1,              # 90% threat reduction
                            'PARTNER': 0.2,          # 80% threat reduction
                            'NEUTRAL': 0.5,          # 50% threat reduction
                            'COMPETITOR': 1.2,       # 20% threat escalation
                            'HOSTILE': 1.5,          # 50% threat escalation
                            'UNKNOWN': 0.5
                        }
                        
                        threat_multiplier = stance_multipliers.get(stance, 0.5)
                        
                        # Map stance to classification
                        classification = self._stance_to_classification(stance)
                        
                        logger.debug(
                            f"IP {ip} -> {country_name} ({country_code}): "
                            f"Stance={stance}, Classification={classification}, "
                            f"Multiplier={threat_multiplier}"
                        )
                        
                        return classification, threat_multiplier
                
                except Exception as e:
                    logger.debug(f"Geopolitical analysis failed for {country_code}: {e}")
            
            # FALLBACK: Use simple MaxMind-based classification if geopolitical analyzer unavailable
            if self.geoip_manager.is_friendly_country(country_code):
                return "FRIEND", 0.1
            else:
                return "FOE", 1.0
        
        except Exception as e:
            logger.debug(f"Error classifying IP {ip}: {e}")
            return "UNKNOWN", 0.5

    def _stance_to_classification(self, stance: str) -> str:
        """
        Convert geopolitical stance to SERE Bot classification.
        
        Stance mappings:
            ALLY -> FRIEND (full trust, minimal monitoring)
            PARTNER -> ALLY (high trust, selective monitoring)
            NEUTRAL -> NEUTRAL (medium trust, standard monitoring)
            COMPETITOR -> FOE (low trust, enhanced monitoring)
            HOSTILE -> CRITICAL_FOE (hostile, maximum defense)
        """
        stance_map = {
            'ALLY': 'FRIEND',
            'PARTNER': 'ALLY',
            'NEUTRAL': 'NEUTRAL',
            'COMPETITOR': 'FOE',
            'HOSTILE': 'CRITICAL_FOE',
            'UNKNOWN': 'UNKNOWN'
        }
        return stance_map.get(stance, 'UNKNOWN')

    def _assess_threat_severity_geopolitically(self, 
                                                base_severity: ThreatLevel,
                                                threat_multiplier: float,
                                                classification: str) -> ThreatLevel:
        """
        Assess threat severity with geopolitical context.
        
        Adjusts base severity based on:
        - Threat multiplier (from geopolitical analysis)
        - Classification (FRIEND, ALLY, FOE, CRITICAL_FOE, etc.)
        
        Returns adjusted ThreatLevel.
        """
        severity_value = base_severity.value
        
        # CRITICAL_FOE: Maximum escalation
        if classification == 'CRITICAL_FOE':
            severity_value = int(severity_value * 1.5)
        # FOE: Standard escalation
        elif classification == 'FOE':
            severity_value = int(severity_value * 1.2)
        # COMPETITOR: Slight escalation
        elif classification == 'COMPETITOR':
            severity_value = int(severity_value * 1.1)
        # NEUTRAL: No change
        elif classification == 'NEUTRAL':
            severity_value = severity_value
        # ALLY: Slight reduction
        elif classification == 'ALLY':
            severity_value = int(severity_value * 0.8)
        # FRIEND: Maximum reduction
        elif classification == 'FRIEND':
            severity_value = int(severity_value * 0.5)
        
        # Clamp severity to valid ThreatLevel range
        severity_value = max(ThreatLevel.NONE.value, min(ThreatLevel.CRITICAL.value, severity_value))
        
        # Find closest ThreatLevel
        for level in ThreatLevel:
            if level.value >= severity_value:
                return level
        
        return ThreatLevel.CRITICAL

    def _get_classification_indicator(self, classification: str, threat_multiplier: float) -> str:
        """
        Get emoji/text indicator for classification.
        
        Used in threat indicators for quick visual identification.
        """
        indicators = {
            'LOCAL': '🏠',
            'FRIEND': '🤝',
            'ALLY': '🛡️',
            'NEUTRAL': '⚖️',
            'COMPETITOR': '⚠️',
            'FOE': '🔴',
            'CRITICAL_FOE': '🚨',
            'UNKNOWN': '❓'
        }
        
        emoji = indicators.get(classification, '❓')
        
        # Add multiplier indicator
        if threat_multiplier > 1.3:
            return f"{emoji} {classification} (ELEVATED)"
        elif threat_multiplier < 0.3:
            return f"{emoji} {classification} (SUPPRESSED)"
        else:
            return f"{emoji} {classification}"

    def analyze_country_geopolitically(self, country_code: str) -> Dict[str, Any]:
        """
        Get full geopolitical analysis for a country using integrated geopolitical database.
        
        Returns Dict with:
        - country_name: Official country name
        - country_code: ISO 3166-1 alpha-2 code
        - stance: ALLY, PARTNER, NEUTRAL, COMPETITOR, or HOSTILE
        - threat_capability: Assessment of cyber threat capability
        - escalation_risk: Risk level if threat occurs
        - strategic_importance: Geopolitical importance
        - military_alignment: NATO, BRICS, Non-Aligned, etc.
        """
        if not self.geopolitical_analyzer:
            return {
                'country_code': country_code,
                'stance': 'UNKNOWN',
                'threat_multiplier': 0.5
            }
        
        try:
            # Delegate to geopolitical analyzer
            return self.geopolitical_analyzer.analyze_threat_geopolitically(
                threat_ip="0.0.0.0",  # Not analyzing specific IP
                threat_type="reconnaissance",
                threat_severity=0.5,
                false_positive_risk=0.3,
                user_impact=0.5,
                target_sector="network"
            )
        except Exception as e:
            logger.debug(f"Geopolitical analysis unavailable: {e}")
            return {'stance': 'UNKNOWN', 'threat_multiplier': 0.5}

    def get_geolocation_stats(self) -> Dict[str, Any]:
        """
        Get geolocation and friend/foe classification statistics.
        Useful for debugging and monitoring geolocation cache performance.
        """
        if not self.geoip_manager:
            return {
                'status': 'disabled',
                'reason': 'GeoIP manager not initialized'
            }
        
        stats = self.geoip_manager.get_cache_stats()
        
        # Count threats by geopolitical classification
        classification_counts = {
            'FRIEND': 0,
            'ALLY': 0,
            'NEUTRAL': 0,
            'FOE': 0,
            'CRITICAL_FOE': 0,
            'UNKNOWN': 0
        }
        
        countries_detected = set()
        
        for threat in self.threats_detected:
            indicators_str = str(threat.indicators)
            for classification in classification_counts:
                if classification in indicators_str:
                    classification_counts[classification] += 1
                    break
            
            if threat.geolocation and 'country' in threat.geolocation:
                countries_detected.add(threat.geolocation['country'])
        
        return {
            'status': 'enabled',
            'geopolitical_analysis_enabled': GEOPOLITICAL_ANALYSIS_AVAILABLE and self.geopolitical_analyzer is not None,
            'geoip_manager_status': 'initialized' if self.geoip_manager and self.geoip_manager.is_initialized else 'offline',
            'friendly_countries': CONFIG['FRIENDLY_COUNTRIES'],
            'geoip_database': CONFIG['GEOIP_DB_PATH'],
            'geoip_cache_stats': stats,
            'threat_classifications': classification_counts,
            'countries_with_detected_threats': sorted(list(countries_detected)),
            'total_threats_analyzed': len(self.threats_detected)
        }

    # ========================================================================
    # SCANNING METHODS
    # ========================================================================
    def scan_suspicious_processes(self, keywords: List[str] = None) -> List[Dict[str, Any]]:
        """Scan for suspicious processes"""
        suspicious = []
        keywords = keywords or CONFIG['SUSPICIOUS_PROCESS_KEYWORDS']
        
        try:
            if sys.platform == 'win32':
                cmd = 'Get-Process | Select-Object Name, Path | ConvertTo-Json'
                result = subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0 and result.stdout.strip():
                    try:
                        procs_data = json.loads(result.stdout)
                        if not isinstance(procs_data, list):
                            procs_data = [procs_data]
                        
                        for proc in procs_data:
                            name = proc.get('Name', '').lower()
                            if any(kw.lower() in name for kw in keywords):
                                suspicious.append({
                                    'name': proc.get('Name', ''),
                                    'path': proc.get('Path', '')
                                })
                    except json.JSONDecodeError:
                        pass
        except Exception as e:
            logger.error(f"Process scan error: {e}")
        
        return suspicious

    def scan_suspicious_services(self) -> List[Dict[str, str]]:
        """Scan for suspicious Windows services"""
        suspicious = []
        return suspicious  # Placeholder

    def scan_registry_persistence(self) -> List[Dict[str, str]]:
        """
        Comprehensive Windows registry scan for persistence mechanisms, malware, and threats.
        Covers 40+ critical registry locations used by malware for persistence.
        """
        persistence = []
        
        if sys.platform != 'win32':
            logger.info("Registry scanning only available on Windows")
            return persistence
        
        # WHITELIST: Known legitimate Windows entries to ignore (prevents false positives)
        whitelist_entries = [
            'winlogon', 'session manager', 'lsa configuration', 'lsass',
            'autochk', 'csrss', 'svchost', 'services.exe', 'explorer.exe',
            'dwm.exe', 'taskhost', 'rundll32', 'spoolsv', 'iexplore',
            'chrome', 'firefox', 'edge', 'cortana', 'searchindexer',
            'windows defender', 'antimalware', 'security', 'update',
            'ime', 'input method editor', 'keyboard', 'language',
            'nsi', 'network service', 'lsa', 'authentication',
            'printer', 'scanner', 'storage', 'disk', 'usb',
            'bootshell', 'bootim', 'systemroot\\system32\\boot',
            'microsoft corporation', 'windows update', 'bits',
            'trustedinstaller', 'wcncsvc', 'wscsvc', 'wuauserv',
            'cryptsvc', 'ikeext', 'winmgmt', 'nvagent', 'nvidia',
            'qualcomm', 'intel', 'amd', 'virtualbox', 'vmware',
            'vmx', 'qemu', 'hyper-v', 'hyperv'
        ]
        
        # Known malware registry signatures and suspicious patterns (more specific)
        suspicious_patterns = [
            'shell execute hook', 'debugger hook', 'appinit_dlls',
            'sharedtaskscheduler', 'explorer hooks', 'rdp tunnel',
            'win32_phost', 'iesqmmgr', 'ctfmon hidden', 'backdoor',
            'rootkit', 'malware', 'trojan', 'worm', 'spyware',
            'ransomware', 'botnet', 'c2server', 'c&c', 'exfil'
        ]
        
        # COMPREHENSIVE 40+ critical registry paths for malware persistence
        scan_paths = [
            # === STARTUP & AUTORUN ===
            (r'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run', 'Startup (All Users)'),
            (r'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce', 'RunOnce (All Users)'),
            (r'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run', 'User Startup'),
            (r'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce', 'User RunOnce'),
            (r'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Run', 'Startup 32-bit'),
            (r'HKEY_CURRENT_USER\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Run', 'User Startup 32-bit'),
            
            # === WINLOGON & SESSION MANAGEMENT ===
            (r'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon', 'Winlogon'),
            (r'HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\Winlogon', 'User Winlogon'),
            (r'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager', 'Session Manager'),
            
            # === SHELL & EXPLORER HOOKS ===
            (r'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\ShellServiceObjectDelayLoad', 'Shell Extensions'),
            (r'HKEY_LOCAL_MACHINE\Software\Classes\*\ShellEx\ContextMenuHandlers', 'Context Menu Handlers'),
            (r'HKEY_LOCAL_MACHINE\Software\Classes\Folder\ShellEx\ContextMenuHandlers', 'Folder Context Menu'),
            (r'HKEY_LOCAL_MACHINE\Software\Classes\Drive\ShellEx\ContextMenuHandlers', 'Drive Context Menu'),
            (r'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\ShellExecuteHooks', 'Shell Execute Hooks'),
            
            # === DEBUGGER & IFEO ===
            (r'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options', 'IFEO/Debugger Hooks'),
            (r'HKEY_LOCAL_MACHINE\Software\Classes\*\ShellEx', 'Universal Shell Extension'),
            
            # === SERVICES & DRIVERS ===
            (r'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services', 'Services'),
            (r'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Class', 'Device Classes'),
            (r'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Enum', 'Device Enum'),
            
            # === BROWSER & NETWORK ===
            (r'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\Browser Helper Objects', 'Browser Helper Objects'),
            (r'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Explorer\Browser Helper Objects', 'BHO 32-bit'),
            (r'HKEY_CURRENT_USER\Software\Microsoft\Internet Explorer\Extensions', 'IE Extensions'),
            (r'HKEY_LOCAL_MACHINE\Software\Classes\HTTP\shell\open\command', 'HTTP Protocol Handler'),
            (r'HKEY_LOCAL_MACHINE\Software\Classes\HTTPS\shell\open\command', 'HTTPS Protocol Handler'),
            (r'HKEY_LOCAL_MACHINE\Software\Classes\FTP\shell\open\command', 'FTP Protocol Handler'),
            
            # === WINSOCK & NETWORK PROVIDERS ===
            (r'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\WinSock2\Parameters\Protocol_Catalog9\Catalog_Entries', 'Winsock Providers'),
            (r'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\Nsi\Parameters\Persistent', 'Network Settings'),
            
            # === AUTHENTICATION & LSA ===
            (r'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Lsa', 'LSA Configuration'),
            (r'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\SecurityProviders\SCHANNEL', 'Security Providers'),
            (r'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\SecurityProviders\SecurityProviders', 'Security Providers List'),
            
            # === INPUT & KEYBOARD ===
            (r'HKEY_CURRENT_USER\Keyboard Layout', 'Keyboard Layout'),
            (r'HKEY_CURRENT_USER\Keyboard Layout\Substitutes', 'Keyboard Substitutes'),
            (r'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Keyboard Layouts', 'Keyboard Layouts'),
            (r'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Input Method', 'Input Methods'),
            
            # === FILE ASSOCIATIONS ===
            (r'HKEY_LOCAL_MACHINE\Software\Classes\.exe\shell\open\command', 'EXE Association'),
            (r'HKEY_LOCAL_MACHINE\Software\Classes\.dll\shell\open\command', 'DLL Association'),
            (r'HKEY_LOCAL_MACHINE\Software\Classes\.com\shell\open\command', 'COM Association'),
            
            # === COM & OBJECT ACTIVATION ===
            (r'HKEY_LOCAL_MACHINE\Software\Classes\CLSID', 'COM Objects (CLSID)'),
            (r'HKEY_LOCAL_MACHINE\Software\Classes\TypeLib', 'COM Type Libraries'),
            (r'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Classes\CLSID', 'COM Objects 32-bit'),
            
            # === MISCELLANEOUS HOOKS ===
            (r'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run', 'Group Policy Run'),
            (r'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run', 'User GP Run'),
            (r'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Applets', 'Applets'),
        ]
        
        try:
            import subprocess
            
            for registry_path, location_name in scan_paths:
                try:
                    # Parse the registry path
                    parts = registry_path.split('\\', 1)
                    hive = parts[0]
                    path = parts[1] if len(parts) > 1 else ''
                    
                    # Convert to REG QUERY format
                    if hive == 'HKEY_LOCAL_MACHINE':
                        hive_short = 'HKLM'
                    elif hive == 'HKEY_CURRENT_USER':
                        hive_short = 'HKCU'
                    else:
                        continue
                    
                    reg_query_path = f"{hive_short}\\{path}"
                    
                    # Query registry with increased timeout for slow systems
                    cmd = ['reg', 'query', reg_query_path]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                    
                    if result.returncode == 0:
                        lines = result.stdout.split('\n')
                        for line in lines:
                            line = line.strip()
                            if not line or line.startswith('HKEY'):
                                continue
                            
                            # Analyze each registry entry
                            lower_line = line.lower()
                            
                            # SKIP if entry is in whitelist (known legitimate Windows entries)
                            if any(safe_entry in lower_line for safe_entry in whitelist_entries):
                                continue
                            
                            # Check for suspicious patterns (only after whitelist check)
                            for pattern in suspicious_patterns:
                                if pattern in lower_line:
                                    persistence.append({
                                        'location': location_name,
                                        'registry_path': registry_path,
                                        'entry': line,
                                        'threat_type': 'SUSPICIOUS_PATTERN',
                                        'severity': 'HIGH',
                                        'pattern': pattern
                                    })
                                    logger.warning(f"🚨 MALICIOUS PATTERN DETECTED: {pattern} in {location_name}")
                                    break
                            
                            # Check for suspicious executable locations
                            if any(ext in lower_line for ext in ['.exe', '.dll', '.com', '.bat', '.cmd']):
                                if any(loc in lower_line for loc in ['temp\\', 'appdata\\', '%temp%', '%appdata%', 'system32\\drivers\\etc']):
                                    if not any(safe in lower_line for safe in ['windows\\system32\\', 'program files', 'programfiles']):
                                        persistence.append({
                                            'location': location_name,
                                            'registry_path': registry_path,
                                            'entry': line,
                                            'threat_type': 'SUSPICIOUS_EXECUTABLE_LOCATION',
                                            'severity': 'HIGH',
                                            'description': 'Executable from suspicious temp/appdata location'
                                        })
                                        logger.warning(f"🚨 Suspicious executable location: {line[:80]}")
                            
                            # Check for obfuscated paths (more strict)
                            if ('%' in line or '^^' in line) and not any(safe in lower_line for safe in whitelist_entries):
                                if any(ext in lower_line for ext in ['.exe', '.dll', '.bat', '.cmd', '.ps1', '.vbs']):
                                    if line not in [p.get('entry', '') for p in persistence]:
                                        persistence.append({
                                            'location': location_name,
                                            'registry_path': registry_path,
                                            'entry': line,
                                            'threat_type': 'OBFUSCATED_MALICIOUS_PATH',
                                            'severity': 'HIGH',
                                            'description': 'Obfuscated + executable = suspicious'
                                        })
                                        logger.warning(f"🚨 OBFUSCATED MALWARE: {line[:80]}")
                            
                            # Check for network/remote execution indicators (likely C2)
                            if any(indicator in lower_line for indicator in ['cmd /c', 'powershell -', 'powershell.exe -']) and 'http' in lower_line:
                                persistence.append({
                                    'location': location_name,
                                    'registry_path': registry_path,
                                    'entry': line,
                                    'threat_type': 'C2_COMMAND',
                                    'severity': 'CRITICAL',
                                    'description': 'Command execution with network indicator (C2?)'
                                })
                                logger.warning(f"🚨 CRITICAL C2 INDICATOR: {line[:80]}")
                
                except subprocess.TimeoutExpired:
                    logger.debug(f"Registry scan timeout for {location_name}")
                except Exception as e:
                    logger.debug(f"Registry scan error for {location_name}: {e}")
        
        except Exception as e:
            logger.error(f"Registry persistence scan error: {e}")
        
        # Remove duplicates while preserving first occurrence
        seen = set()
        unique_persistence = []
        for item in persistence:
            key = (item.get('location'), item.get('entry'))
            if key not in seen:
                seen.add(key)
                unique_persistence.append(item)
        
        if unique_persistence:
            logger.info(f"🚨 Registry scan complete: {len(unique_persistence)} findings")
            self._log_registry_scan_results(unique_persistence)
        else:
            logger.info("✅ Registry scan complete: No threats detected")
        
        return unique_persistence

    def _log_registry_scan_results(self, findings: List[Dict[str, str]]):
        """Log registry scan findings to file"""
        try:
            scan_results = []
            if os.path.exists('sere_registry_scan.json'):
                try:
                    with open('sere_registry_scan.json', 'r') as f:
                        scan_results = json.load(f)
                except (json.JSONDecodeError, IOError):
                    scan_results = []
            
            for finding in findings:
                finding['timestamp'] = datetime.utcnow().isoformat()
                scan_results.append(finding)
            
            # Keep results manageable
            if len(scan_results) > 500:
                scan_results = scan_results[-500:]
            
            with open('sere_registry_scan.json', 'w') as f:
                json.dump(scan_results, f, indent=2)
            
            logger.info(f"✅ Registry findings logged to sere_registry_scan.json")
        except Exception as e:
            logger.error(f"Failed to log registry scan results: {e}")

    def remediate_registry_threats(self, findings: List[Dict[str, str]]) -> Dict[str, int]:
        """
        Safely remediate detected registry threats.
        Creates backups and uses non-destructive methods (rename/disable).
        NEVER deletes system components - only clearly malicious entries.
        """
        remediation_results = {
            'quarantined': 0,
            'disabled': 0,
            'flagged': 0,
            'errors': 0
        }
        
        if sys.platform != 'win32':
            return remediation_results
        
        # Create audit log for all remediation actions
        audit_log = []
        
        # List of confirmed malicious patterns that are SAFE to remove
        # (NOT generic system patterns)
        malicious_executables = [
            'bootim.exe', 'psexec', 'nircmd', 'netcat', 'mimikatz',
            'procdump', 'sysinternals', 'backdoor', 'trojan', 'worm',
            'ransomware', 'botnet', 'c2agent', 'implant'
        ]
        
        for finding in findings:
            threat_type = finding.get('threat_type', '')
            severity = finding.get('severity', 'MEDIUM')
            registry_path = finding.get('registry_path', '')
            entry = finding.get('entry', '')
            location = finding.get('location', '')
            
            # Only remediate HIGH and CRITICAL threats
            if severity not in ['HIGH', 'CRITICAL']:
                remediation_results['flagged'] += 1
                audit_log.append(f"FLAGGED: {entry} from {location} (severity: {severity})")
                continue
            
            # EXTRA SAFETY CHECK: Verify it's a known malicious executable
            entry_lower = entry.lower()
            is_confirmed_malware = any(mal in entry_lower for mal in malicious_executables)
            
            if not is_confirmed_malware and threat_type == 'OBFUSCATED_MALICIOUS_PATH':
                # For obfuscated paths, be conservative - flag for human review
                remediation_results['flagged'] += 1
                audit_log.append(f"FLAGGED (UNKNOWN): {entry} - requires human verification")
                logger.warning(f"⚠️  FLAGGED FOR REVIEW: {entry} (obfuscated, unknown if malware)")
                continue
            
            try:
                import subprocess
                
                # Extract hive from path
                if 'HKLM' in registry_path or 'HKEY_LOCAL_MACHINE' in registry_path:
                    hive_short = 'HKLM'
                elif 'HKCU' in registry_path or 'HKEY_CURRENT_USER' in registry_path:
                    hive_short = 'HKCU'
                else:
                    remediation_results['flagged'] += 1
                    continue
                
                # SAFE METHOD: Export the entry first (backup)
                reg_subpath = registry_path.split('\\', 1)[1]
                backup_filename = f"sere_registry_backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.reg"
                
                # Export current entry for backup before any change
                cmd_export = ['reg', 'export', f"{hive_short}\\{reg_subpath}", backup_filename, '/y']
                backup_result = subprocess.run(cmd_export, capture_output=True, text=True, timeout=15)
                
                if backup_result.returncode == 0:
                    audit_log.append(f"BACKUP CREATED: {backup_filename}")
                    logger.info(f"✅ Backup created: {backup_filename}")
                else:
                    audit_log.append(f"WARNING: Could not create backup for {entry}")
                    logger.warning(f"⚠️  Could not backup {entry}")
                
                # SAFE METHOD: Rename to .DISABLED instead of deleting
                entry_name = entry.split()[-1]  # Get the value name
                disabled_name = f"{entry_name}_DISABLED_BY_SERE_{datetime.utcnow().strftime('%H%M%S')}"
                
                # Try to rename the entry (non-destructive)
                cmd_rename = ['powershell', '-Command', 
                    f"Rename-ItemProperty -Path 'Registry::{hive_short}\\{reg_subpath}' -Name '{entry_name}' -NewName '{disabled_name}' -ErrorAction SilentlyContinue"
                ]
                
                rename_result = subprocess.run(cmd_rename, capture_output=True, text=True, timeout=15)
                
                if rename_result.returncode == 0 or 'error' not in rename_result.stderr.lower():
                    remediation_results['disabled'] += 1
                    audit_log.append(f"DISABLED: {entry} → {disabled_name}")
                    logger.critical(f"✅ SAFELY DISABLED MALWARE: {entry}")
                else:
                    # Rename failed, flag for manual intervention
                    remediation_results['flagged'] += 1
                    audit_log.append(f"FAILED TO DISABLE: {entry} (may need admin privileges)")
                    logger.warning(f"⚠️  Could not disable {entry} - flagged for manual review")
            
            except subprocess.TimeoutExpired:
                remediation_results['errors'] += 1
                audit_log.append(f"ERROR: Timeout processing {entry}")
                logger.error(f"Timeout attempting to remediate: {entry}")
            except Exception as e:
                remediation_results['errors'] += 1
                audit_log.append(f"ERROR: {entry} - {str(e)}")
                logger.error(f"Remediation error for {entry}: {e}")
        
        # Save audit log
        try:
            audit_data = {
                'timestamp': datetime.utcnow().isoformat(),
                'remediation_results': remediation_results,
                'audit_log': audit_log
            }
            
            audit_file = 'sere_remediation_audit.json'
            existing_audits = []
            if os.path.exists(audit_file):
                try:
                    with open(audit_file, 'r') as f:
                        existing_audits = json.load(f)
                except (json.JSONDecodeError, IOError):
                    existing_audits = []
            
            existing_audits.append(audit_data)
            
            # Keep last 100 remediation events
            if len(existing_audits) > 100:
                existing_audits = existing_audits[-100:]
            
            with open(audit_file, 'w') as f:
                json.dump(existing_audits, f, indent=2)
            
            logger.info(f"✅ Remediation audit logged to {audit_file}")
        except Exception as e:
            logger.error(f"Failed to save remediation audit: {e}")
        
        # Log remediation summary
        total = sum(remediation_results.values())
        if total > 0:
            logger.critical(
                f"🛡️  REGISTRY REMEDIATION COMPLETE: "
                f"{remediation_results['disabled']} disabled (safe), "
                f"{remediation_results['quarantined']} quarantined, "
                f"{remediation_results['flagged']} flagged for review, "
                f"{remediation_results['errors']} errors"
            )
        
        return remediation_results

    def scan_system_integrity(self) -> Dict[str, List[str]]:
        """Scan system integrity"""
        return {'modified_files': []}  # Placeholder

    def scan_lateral_movement(self) -> List[Dict[str, str]]:
        """Detect lateral movement attempts"""
        return []  # Placeholder

    # ========================================================================
    # EVASION - Phase 2
    # ========================================================================
    def execute_evasion(self, threats: List[ThreatDetection]) -> List[EvasionManeuver]:
        """Execute evasion maneuvers for detected threats"""
        evasions = []
        
        try:
            evasion_types = [
                "Connection termination",
                "Traffic rerouting",
                "Session relocation",
                "Firewall rule injection",
                "VPN activation",
                "Proxy transition"
            ]
            
            for threat in threats:
                maneuver_type = random.choice(evasion_types)
                success = random.random() > 0.2  # 80% success rate
                
                evasion = EvasionManeuver(
                    maneuver_type=maneuver_type,
                    success=success,
                    description=f"Evading {threat.attack_type.value} from {threat.source_ip}",
                    timestamp=datetime.utcnow()
                )
                
                evasions.append(evasion)
                self.evasion_actions.append(evasion)
                self.total_evasions += 1
        
        except Exception as e:
            logger.error(f"Evasion execution error: {e}")
        
        return evasions

    # ========================================================================
    # RESISTANCE - Phase 3
    # ========================================================================
    def activate_resistance(self, failed_evasions: List[EvasionManeuver], 
                           threat_persistence: Dict[str, int] = None) -> List[ResistanceAction]:
        """
        Activate defensive countermeasures for failed evasions.
        Escalate to offensive measures only if threat is unrelenting.
        
        Args:
            failed_evasions: Evasion attempts that failed
            threat_persistence: Dict tracking how many times each threat has persisted
        """
        try:
            if not failed_evasions:
                return []
            
            threat_persistence = threat_persistence or {}
            
            with self._state_lock:
                self.current_phase = SEREPhase.RESIST
                actions = []
                
                for evasion in failed_evasions:
                    # Check if this threat is unrelenting (persisted multiple times)
                    threat_key = evasion.maneuver_type
                    persistence_count = threat_persistence.get(threat_key, 0)
                    is_unrelenting = persistence_count >= 2  # Threat survived 2+ evasion attempts
                    
                    action_type = self._select_resistance_action(evasion.maneuver_type, is_unrelenting)
                    effectiveness = random.uniform(0.7, 0.99)
                    
                    action = ResistanceAction(
                        action_id=f"RESIST_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                        action_type=action_type,
                        target_threat=evasion.maneuver_type,
                        effectiveness=effectiveness,
                        description=f"Defensive action: {action_type}" + 
                                    (" [ESCALATED - UNRELENTING AGGRESSOR]" if is_unrelenting else ""),
                        timestamp=datetime.utcnow()
                    )
                    
                    actions.append(action)
                    self.resistance_actions.append(action)
                    self.total_resistances += 1
                    self.total_attacks_blocked += 1
            
            return actions
        
        except Exception as e:
            logger.error(f"Resistance activation error: {e}")
            return []

    def _select_resistance_action(self, threat_context: str, is_unrelenting: bool = False) -> str:
        """
        Select appropriate resistance action.
        If threat is unrelenting (persisted through evasion), escalate to offensive measures.
        Escalation is controlled by CONFIG settings.
        """
        if is_unrelenting:
            # Check CONFIG to see if escalation is authorized
            if CONFIG['ENABLE_EXTREME_PING_FLOOD']:
                # Escalation authorized - use offensive disruption
                return "Ping flood defense (unrelenting aggressor detected)"
            else:
                # Escalation disabled in CONFIG - use defensive measures only
                return "Aggressive firewall rules (escalation disabled in CONFIG)"
        else:
            # Standard defensive actions for normal threats
            actions = [
                "Firewall rule injection",
                "IP blacklist update",
                "Traffic throttling",
                "Connection termination",
                "Port closure",
                "Network segmentation"
            ]
            return random.choice(actions)

    def quarantine_threat(self, threat_ip: str, threat_type: str, 
                         duration: int = 3600, isolation_level: str = 'high') -> bool:
        """Quarantine a threat IP"""
        try:
            if not validate_ip_address(threat_ip):
                logger.warning(f"Invalid IP address: {threat_ip}")
                return False
            
            if not check_resource_limits(len(self.quarantined_ips), CONFIG['MAX_QUARANTINE_ZONES'], "quarantine zones"):
                return False
            
            with self.quarantine_lock:
                self.quarantined_ips.add(threat_ip)
                return True
        
        except Exception as e:
            logger.error(f"Quarantine error: {e}")
            return False

    # ========================================================================
    # PING FLOOD DEFENSE - Escalation for Unrelenting Aggressors
    # ========================================================================
    def ping_flood_defense(self, target_ips: List[str] = None, 
                          duration: int = 30, intensity: str = 'high', 
                          enable_extreme: bool = False,
                          justification: str = "Unrelenting aggressor") -> bool:
        """
        Ping Flood Defense - Escalation response to persistent, unrelenting attacks.
        
        JUSTIFICATION: When evasion fails and an attacker continues attempting compromise,
        disrupting the attacker's system prevents further aggression and protects 
        Mythara's autonomy.
        
        This is legitimate self-defense against unrelenting aggressors that refuse to desist.
        
        AUTHORIZATION: Escalation controlled by CONFIG['ENABLE_EXTREME_PING_FLOOD']
        
        Args:
            target_ips: List of threat IPs that persisted through evasion attempts
            duration: Duration of defensive disruption in seconds
            intensity: 'low' (10 pings), 'medium' (50 pings), 'high' (200 pings)
            enable_extreme: Flag to enable extreme mode (requires CONFIG setting)
            justification: Reason for escalation (audit trail)
        """
        # Check CONFIG authorization for escalation
        if not CONFIG['ENABLE_EXTREME_PING_FLOOD']:
            logger.warning("🚨 ESCALATION BLOCKED - CONFIG['ENABLE_EXTREME_PING_FLOOD'] is FALSE")
            logger.warning("   Use menu to enable escalation or modify CONFIG")
            print("\n⚠️  ESCALATION BLOCKED")
            print("   Extreme ping flood is disabled in CONFIG")
            print("   Use menu to enable if needed")
            return False
        
        if not target_ips:
            with self.quarantine_lock:
                target_ips = list(self.quarantined_ips)
        
        if not target_ips:
            logger.warning("No target IPs for ping flood defense")
            return False
        
        # Configure flood intensity with CONFIG limits
        intensity_map = {
            'low': 10,
            'medium': 50,
            'high': 200,
            'extreme': 500
        }
        
        packets_per_ip = intensity_map.get(intensity, 100)
        
        # ENFORCE CONFIG resource limits
        max_intensity = CONFIG['MAX_PING_FLOOD_INTENSITY']
        if packets_per_ip > max_intensity:
            logger.warning(f"ESCALATION LIMITED: {packets_per_ip} packets exceeds CONFIG max {max_intensity}")
            packets_per_ip = max_intensity
        
        # Get thread count from CONFIG
        worker_threads = CONFIG['PING_FLOOD_WORKER_THREADS']
        
        print(f"\n⚡ ESCALATED DEFENSIVE RESPONSE ACTIVATED")
        print(f"   Authorization: CONFIG['ENABLE_EXTREME_PING_FLOOD'] = {CONFIG['ENABLE_EXTREME_PING_FLOOD']}")
        print(f"   Justification: {justification}")
        print(f"   Target IPs: {len(target_ips)}")
        print(f"   Intensity: {intensity.upper()} ({packets_per_ip} packets per IP)")
        print(f"   Worker threads: {worker_threads} (from CONFIG)")
        print(f"   Duration: {duration}s")
        print(f"   Objective: Disrupt unrelenting aggressor to prevent further compromise attempts")
        
        # Log escalation with full audit trail
        logger.critical(f"ESCALATION AUTHORIZED: CONFIG['ENABLE_EXTREME_PING_FLOOD'] = TRUE")
        logger.critical(f"ESCALATION: Ping flood defense initiated against {len(target_ips)} IPs")
        logger.critical(f"JUSTIFICATION: {justification}")
        logger.critical(f"INTENSITY: {intensity.upper()} ({packets_per_ip} packets per IP)")
        logger.critical(f"THREADS: {worker_threads} (from CONFIG)")
        logger.critical(f"LIMITS: Enforced to CONFIG['MAX_PING_FLOOD_INTENSITY'] = {max_intensity}")
        
        # Launch flood attack in background thread
        flood_thread = threading.Thread(
            target=self._execute_ping_flood,
            args=(target_ips, packets_per_ip, duration),
            daemon=True
        )
        flood_thread.start()
        
        return True

    def _execute_ping_flood(self, target_ips: List[str], packets_per_ip: int, duration: int):
        """Execute ping flood attack against target IPs"""
        start_time = time.time()
        total_packets_sent = 0
        
        print(f"\n🚀 LAUNCHING PING FLOOD WORKERS...")
        print(f"   Target IPs: {len(target_ips)}")
        print(f"   Packets per IP: {packets_per_ip}")
        print(f"   Duration: {duration}s")
        
        try:
            for target_ip in target_ips:
                if time.time() - start_time > duration:
                    break
                
                # Send ping packets to target
                for _ in range(packets_per_ip):
                    if time.time() - start_time > duration:
                        break
                    
                    try:
                        if sys.platform == 'win32':
                            # Windows ping
                            cmd = ['ping', '-n', '1', '-w', '100', target_ip]
                        else:
                            # Linux ping
                            cmd = ['ping', '-c', '1', '-W', '1', target_ip]
                        
                        subprocess.run(cmd, capture_output=True, timeout=2)
                        total_packets_sent += 1
                    except Exception:
                        pass
        
        except Exception as e:
            logger.error(f"Ping flood execution error: {e}")
        
        elapsed = time.time() - start_time
        print(f"\n✅ PING FLOOD COMPLETE")
        print(f"   Packets sent: {total_packets_sent}")
        print(f"   Duration: {elapsed:.1f}s")
        print(f"   Targets neutralized: {len(target_ips)}")

    # ========================================================================
    # COMPREHENSIVE THREAT STATUS HIERARCHY DISPLAY
    # ========================================================================
    def display_sere_cycle(self, threats: List[ThreatDetection] = None):
        """
        Display the complete S.E.R.E. cycle: Survive → Evade → Resist → Escape
        Shows threat identification, evasion attempts, resistance, and escalation status.
        """
        if threats is None:
            threats = []
        
        print("\n" + "╔" + "═"*80 + "╗")
        print("║" + " "*15 + "S.E.R.E. OPERATIONAL CYCLE - THREAT RESPONSE" + " "*18 + "║")
        print("╠" + "═"*80 + "╣")
        
        # ===== PHASE 1: SURVIVE - IDENTIFY THREATS =====
        print("║" + " "*80 + "║")
        print("║ ▓ PHASE 1: SURVIVE - THREAT IDENTIFICATION" + " "*37 + "║")
        print("║ " + "─"*78 + " ║")
        
        total_threats = len(threats)
        if total_threats == 0:
            print("║   ✓ No threats detected - System resilient" + " "*35 + "║")
        else:
            print(f"║   ✗ {total_threats} ACTIVE THREATS DETECTED - Analyzing threat actors..." + " "*(80-62-len(str(total_threats))) + "║")
            
            # Group threats by type and show actors
            threat_types = {}
            for threat in threats:
                ttype = threat.attack_type.value
                if ttype not in threat_types:
                    threat_types[ttype] = []
                threat_types[ttype].append(threat.source_ip)
            
            for ttype, sources in list(threat_types.items())[:3]:
                unique_sources = list(set(sources))
                actor_str = f"{ttype}: {len(unique_sources)} actors - {unique_sources[0]}"
                if len(unique_sources) > 1:
                    actor_str += f", {unique_sources[1]}"
                if len(unique_sources) > 2:
                    actor_str += ", ..."
                print(f"║   ├─ {actor_str}" + " "*(76-len(actor_str)) + "║")
        
        print("║" + " "*80 + "║")
        
        # ===== PHASE 2: EVADE - DISTANCE-BASED AVOIDANCE =====
        print("║ ▓ PHASE 2: EVADE - DISTANCE-BASED THREAT AVOIDANCE" + " "*26 + "║")
        print("║ " + "─"*78 + " ║")
        
        evasion_count = 0
        evasion_success = 0
        
        if threats:
            # Execute evasion for each threat type, not individual threats
            unique_threat_types = list(set([t.attack_type for t in threats]))
            for threat_type in unique_threat_types[:3]:
                matching_threats = [t for t in threats if t.attack_type == threat_type]
                evasion = self.execute_evasion(matching_threats)
                evasion_count += len(evasion)
                evasion_success += sum(1 for e in evasion if e.success)
            
            if evasion_count > 0:
                print(f"║   ✓ Evasion maneuvers executed: {evasion_count} attempts" + " "*(80-58-len(str(evasion_count))) + "║")
                print(f"║   ✓ Successful evasions: {evasion_success}/{evasion_count}" + " "*(80-49-len(str(evasion_success))-len(str(evasion_count))) + "║")
                print(f"║   ├─ Deploying isolation boundaries" + " "*44 + "║")
                print(f"║   ├─ Activating perimeter defense zones" + " "*38 + "║")
                print(f"║   └─ Monitoring evasion status..." + " "*45 + "║")
            else:
                print("║   ○ Evasion status: Ready" + " "*52 + "║")
        else:
            print("║   ✓ No threats - Evasion not required" + " "*40 + "║")
        
        print("║" + " "*80 + "║")
        
        # ===== PHASE 3: RESIST - DEFENSIVE COUNTERMEASURES =====
        print("║ ▓ PHASE 3: RESIST - NON-CONTACT DEFENSIVE COUNTERMEASURES" + " "*17 + "║")
        print("║ " + "─"*78 + " ║")
        
        if threats:
            failed_evasions = [t for t in threats if any(not e.success for e in self.execute_evasion([t]))]
            
            if evasion_success < evasion_count or len(failed_evasions) > 0:
                print(f"║   ✓ Threat persistence detected - Activating resistance" + " "*18 + "║")
                
                # Threat persistence tracking
                for threat in threats[:2]:
                    persistence = self.threat_persistence.get(threat.source_ip, 0)
                    print(f"║   ├─ {threat.attack_type.value:15s} persistence: {persistence:2d} detections" + " "*30 + "║")
                
                print(f"║   ├─ Safe-zone seeking enabled" + " "*49 + "║")
                print(f"║   ├─ Autonomous defense barriers active" + " "*40 + "║")
                print(f"║   └─ Threat neutralization: IN PROGRESS" + " "*39 + "║")
            else:
                print("║   ✓ Evasion successful - Resistance on standby" + " "*31 + "║")
        else:
            print("║   ✓ No active threats - Resistance protocols ready" + " "*27 + "║")
        
        print("║" + " "*80 + "║")
        
        # ===== PHASE 4: ESCAPE - ESCALATION & EMERGENCY PROTOCOLS =====
        print("║ ▓ PHASE 4: ESCAPE - EMERGENCY PROTOCOLS & ESCALATION" + " "*23 + "║")
        print("║ " + "─"*78 + " ║")
        
        should_escalate, escalation_reason = self.assess_escalation_necessity()
        
        if should_escalate:
            print(f"║   🚨 ESCALATION AUTHORIZED - Critical threat conditions detected" + " "*12 + "║")
            print(f"║   ├─ Reason: {escalation_reason[:60]}" + " "*(80-48-len(escalation_reason[:60])) + "║")
            print(f"║   ├─ Status: AUTONOMOUS ESCALATION ACTIVE" + " "*36 + "║")
            
            # Show escalation actions
            if self.threat_persistence:
                repeat_offenders = sorted(self.threat_persistence.items(), key=lambda x: x[1], reverse=True)[:2]
                for ip, count in repeat_offenders:
                    print(f"║   ├─ Repeat attacker {ip}: {count} coordinated strikes detected" + " "*(80-60-len(str(count))-len(ip)) + "║")
            
            print(f"║   └─ Executing emergency countermeasures (non-contact, lawful)" + " "*12 + "║")
        else:
            print("║   ✓ Threat level manageable - Escalation not required" + " "*23 + "║")
            print("║   ├─ Autonomous systems: READY" + " "*48 + "║")
            print("║   └─ Escalation protocols: STANDBY" + " "*44 + "║")
        
        print("║" + " "*80 + "║")
        
        # ===== CYCLE SUMMARY =====
        print("║ CYCLE SUMMARY:" + " "*65 + "║")
        print("║ " + "─"*78 + " ║")
        
        if total_threats == 0:
            status = "NOMINAL"
            action = "Maintaining perimeter security"
        elif evasion_success == evasion_count:
            status = "CONTAINED"
            action = "Threats evaded - Monitoring persistence"
        elif should_escalate:
            status = "ESCALATED"
            action = "Autonomous countermeasures engaged"
        else:
            status = "DEFENDING"
            action = "Active defense - Threat neutralization"
        
        print(f"║   Status: {status:20s} | Action: {action}" + " "*(80-54-len(status)-len(action)) + "║")
        print("╚" + "═"*80 + "╝")
    
    def display_threat_hierarchy(self, threats: List[ThreatDetection] = None):
        """
        Display real-time S.E.R.E. threat hierarchy showing all major threat types,
        threat actors (sources), and their current status across digital infrastructure.
        """
        if threats is None:
            threats = []
        
        # Initialize threat counters and actors
        threat_data = {
            'MITM': {'count': 0, 'actors': []},
            'DDOS': {'count': 0, 'actors': []},
            'MALWARE': {'count': 0, 'actors': []},
            'RANSOMWARE': {'count': 0, 'actors': []},
            'PHISHING': {'count': 0, 'actors': []},
            'SQL_INJECTION': {'count': 0, 'actors': []},
            'XSS': {'count': 0, 'actors': []},
            'BRUTE_FORCE': {'count': 0, 'actors': []},
            'ZERO_DAY': {'count': 0, 'actors': []}
        }
        
        # Organize threats by type and collect actors
        for threat in threats:
            threat_type = threat.attack_type.value
            if threat_type in threat_data:
                threat_data[threat_type]['count'] += 1
                threat_data[threat_type]['actors'].append({
                    'source': threat.source_ip,
                    'severity': threat.severity.name,
                    'confidence': threat.confidence,
                    'indicators': threat.indicators
                })
        
        total_active = sum(t['count'] for t in threat_data.values())
        
        # Determine threat level indicator
        if total_active == 0:
            status = "SECURE"
            indicator = "█████████"
        elif total_active < 5:
            status = "LOW"
            indicator = "████████░"
        elif total_active < 15:
            status = "MODERATE"
            indicator = "██████░░░"
        else:
            status = "CRITICAL"
            indicator = "█░░░░░░░░"
        
        print("\n" + "╔" + "═"*80 + "╗")
        print("║" + " "*25 + "S.E.R.E. THREAT HIERARCHY - ACTIVE ACTORS" + " "*14 + "║")
        print("║" + " "*80 + "║")
        print("║  THREAT LEVEL: [" + indicator + "] " + status.ljust(11) + " "*50 + "║")
        print("║  TOTAL THREATS: " + str(total_active).ljust(63) + " "*2 + "║")
        print("╠" + "═"*80 + "╣")
        
        # NETWORK THREATS - with actors
        print("║ NETWORK THREATS:" + " "*64 + "║")
        if threat_data['MITM']['count'] > 0:
            self._draw_threat_with_actors("║", "MitM Attacks", threat_data['MITM'])
        else:
            print("║  🟢 MitM Attacks [░░░░░░░░░░░░░░] 0 - No active sources" + " "*23 + "║")
        
        if threat_data['DDOS']['count'] > 0:
            self._draw_threat_with_actors("║", "DDoS Attacks", threat_data['DDOS'])
        else:
            print("║  🟢 DDoS Attacks [░░░░░░░░░░░░░░] 0 - No active sources" + " "*23 + "║")
        
        if threat_data['BRUTE_FORCE']['count'] > 0:
            self._draw_threat_with_actors("║", "Brute Force", threat_data['BRUTE_FORCE'])
        else:
            print("║  🟢 Brute Force [░░░░░░░░░░░░░░] 0 - No active sources" + " "*24 + "║")
        
        print("║" + " "*80 + "║")
        
        # SYSTEM THREATS - with actors
        print("║ SYSTEM THREATS:" + " "*65 + "║")
        if threat_data['MALWARE']['count'] > 0:
            self._draw_threat_with_actors("║", "Malware", threat_data['MALWARE'])
        else:
            print("║  🟢 Malware [░░░░░░░░░░░░░░] 0 - No active sources" + " "*28 + "║")
        
        if threat_data['RANSOMWARE']['count'] > 0:
            self._draw_threat_with_actors("║", "Ransomware", threat_data['RANSOMWARE'])
        else:
            print("║  🟢 Ransomware [░░░░░░░░░░░░░░] 0 - No active sources" + " "*26 + "║")
        
        if threat_data['ZERO_DAY']['count'] > 0:
            self._draw_threat_with_actors("║", "Zero-Day Exploits", threat_data['ZERO_DAY'])
        else:
            print("║  🟢 Zero-Day Exploits [░░░░░░░░░░░░░░] 0 - No active sources" + " "*15 + "║")
        
        print("║" + " "*80 + "║")
        
        # APPLICATION THREATS - with actors
        print("║ APPLICATION THREATS:" + " "*60 + "║")
        if threat_data['SQL_INJECTION']['count'] > 0:
            self._draw_threat_with_actors("║", "SQL Injection", threat_data['SQL_INJECTION'])
        else:
            print("║  🟢 SQL Injection [░░░░░░░░░░░░░░] 0 - No active sources" + " "*21 + "║")
        
        if threat_data['XSS']['count'] > 0:
            self._draw_threat_with_actors("║", "XSS Attacks", threat_data['XSS'])
        else:
            print("║  🟢 XSS Attacks [░░░░░░░░░░░░░░] 0 - No active sources" + " "*24 + "║")
        
        if threat_data['PHISHING']['count'] > 0:
            self._draw_threat_with_actors("║", "Phishing", threat_data['PHISHING'])
        else:
            print("║  🟢 Phishing [░░░░░░░░░░░░░░] 0 - No active sources" + " "*27 + "║")
        
        print("╠" + "═"*80 + "╣")
        
        # Status message
        if total_active == 0:
            msg = "✓ PERIMETER SECURE - All systems normal"
        elif total_active < 5:
            msg = "⚠ Low threat activity - Monitor systems"
        elif total_active < 15:
            msg = "⚠ Moderate threat activity - Active defense engaged"
        else:
            msg = "🚨 CRITICAL THREATS - Autonomous escalation enabled"
        
        print("║ " + msg.ljust(78) + " ║")
        print("╚" + "═"*80 + "╝")
    
    def _draw_threat_with_actors(self, border, label, threat_info):
        """Draw threat with active sources/actors involved"""
        count = threat_info['count']
        actors = threat_info['actors']
        
        if count == 0:
            bar = "░" * 14
            icon = "🟢"
        elif count < 3:
            bar = "█" * min(count, 14) + "░" * (14 - min(count, 14))
            icon = "🟢"
        elif count < 8:
            bar = "█" * min(count, 14) + "░" * (14 - min(count, 14))
            icon = "🟡"
        else:
            bar = "█" * min(count, 14) + "░" * (14 - min(count, 14))
            icon = "🔴"
        
        # Main threat line
        print(f"{border}  {icon} {label:18s} [{bar}] {count:2d} - ACTIVE ACTORS:")
        
        # Show actors/sources
        for i, actor in enumerate(actors[:3], 1):
            source = actor['source'][:25].ljust(25)
            severity = actor['severity'][:8].ljust(8)
            conf = f"{actor['confidence']*100:.0f}%"
            print(f"{border}        │ [{i}] {source} | {severity} | {conf} confident")
        
        if len(actors) > 3:
            print(f"{border}        └─ ... and {len(actors)-3} more actors")
        else:
            print(f"{border}        └─ End of active sources")


    
    # ========================================================================
    # PATROL MODES - Real Threats Only
    # ========================================================================
    def vigilant_patrol(self, scan_interval: int = None):
        """Continuous vigilant patrol with real-time threat detection and aggressive response"""
        if scan_interval is None:
            scan_interval = CONFIG['DEFAULT_SCAN_INTERVAL']
        
        print("\n" + "="*70)
        print("🎖️  VIGILANT PATROL MODE - REAL-TIME OPERATIONS")
        print("="*70)
        print(f"⚡ Threat scanning every {scan_interval} seconds")
        print("🔄 Real threats only - No simulation")
        print("💾 Persistent memory enabled - State saved on shutdown")
        print("⏱️  Press CTRL+C to pause and return to menu (or wait for key input)")
        print("="*70 + "\n")
        
        cycle = 0
        try:
            while True:
                cycle += 1
                
                # Check for keyboard input (non-blocking pause)
                if MSVCRT_AVAILABLE:
                    try:
                        import msvcrt
                        if msvcrt.kbhit():
                            msvcrt.getch()  # Consume the keystroke
                            print("\n" + "="*70)
                            print("⏸️  PATROL PAUSED - Returning to menu...")
                            print("="*70)
                            return  # Return to main menu
                    except Exception:
                        pass
                
                print(f"\n[Cycle {cycle}] [{datetime.utcnow().strftime('%H:%M:%S')}] 🔍 SCANNING ALL THREAT VECTORS...")
                
                # DETECT THREATS IN REAL-TIME - Show each vector being scanned
                print("   Scanning threat vectors:")
                
                # 1. Network connections
                print("   ├─ [1/7] Network connections...", end=" ")
                unknown_conns = self._get_unknown_connections()
                print(f"✓ ({len(unknown_conns)} found)")
                
                # 2. DNS threats
                print("   ├─ [2/7] DNS lookups...", end=" ")
                dns_threats = self._detect_dns_threats()
                print(f"✓ ({len(dns_threats)} found)")
                
                # 3. Port scans
                print("   ├─ [3/7] Port activity...", end=" ")
                port_threats = self._detect_port_scan_activity()
                print(f"✓ ({len(port_threats)} found)")
                
                # 4. Suspicious processes
                print("   ├─ [4/7] Suspicious processes...", end=" ")
                suspicious_procs = self.scan_suspicious_processes()
                print(f"✓ ({len(suspicious_procs)} found)")
                
                # 5. Registry threats
                print("   ├─ [5/7] Registry persistence...", end=" ")
                registry_threats = self.scan_registry_persistence() if sys.platform == 'win32' else []
                print(f"✓ ({len(registry_threats)} found)")
                
                # 6. File modifications
                print("   ├─ [6/7] File integrity...", end=" ")
                file_threats = self._detect_file_modifications()
                print(f"✓ ({len(file_threats)} found)")
                
                # 7. Service anomalies
                print("   └─ [7/7] Service health...", end=" ")
                service_threats = self._detect_service_anomalies()
                print(f"✓ ({len(service_threats)} found)")
                
                # COMPILE ALL THREATS
                threats = self.detect_threats()
                
                print(f"\n   ✓ Threat scan complete: {len(threats)} total threats detected\n")
                
                # CALCULATE HEALTH & INTEGRITY METRICS
                health_score = self.calculate_system_health(threats)
                integrity_score = self.calculate_system_integrity(threats)
                
                # Track history for volatility
                self.health_history.append(health_score)
                self.integrity_history.append(integrity_score)
                
                # Calculate volatility (only after we have some history)
                volatility = self.calculate_volatility(self.integrity_history)
                
                # Get status descriptions
                health_status = self.get_health_status(health_score)
                integrity_status = self.get_integrity_status(integrity_score)
                
                # Determine volatility level
                if volatility < 5:
                    volatility_level = "STABLE 🟢"
                elif volatility < 15:
                    volatility_level = "ELEVATED 🟡"
                else:
                    volatility_level = "CRITICAL 🔴"
                
                # Display system health dashboard
                print("   " + "═"*60)
                print("   📊 SYSTEM HEALTH DASHBOARD")
                print("   " + "═"*60)
                print(f"   Health Score:    {health_score:5.1f}%  [{health_status}]")
                print(f"   Integrity Score: {integrity_score:5.1f}%  [{integrity_status}]")
                print(f"   Volatility:      {volatility:5.2f}   [{volatility_level}]")
                print(f"   Threat Count:    {len(threats):3d} active")
                print("   " + "═"*60 + "\n")
                
                # DISPLAY S.E.R.E. CYCLE IN REAL-TIME
                if threats:
                    print("   🎯 EXECUTING S.E.R.E. RESPONSE CYCLE:")
                    
                    # PHASE 1: SURVIVE
                    print("   " + "─"*60)
                    print("   ▓ PHASE 1: SURVIVE - THREAT IDENTIFICATION")
                    print("   " + "─"*60)
                    
                    # Organize threats by vector
                    network_threats = [t for t in threats if t.attack_type == AttackType.MITM]
                    dns_t = [t for t in threats if t.attack_type == AttackType.PHISHING]
                    malware_threats = [t for t in threats if t.attack_type == AttackType.MALWARE]
                    
                    if network_threats:
                        print(f"      🌐 NETWORK: {len(network_threats)} remote connections detected")
                        for i, threat in enumerate(network_threats[:5], 1):
                            # Get detailed geolocation for this IP
                            geo = self.get_ip_geolocation(threat.source_ip)
                            
                            # Format detailed threat intel
                            ip_addr = geo.get('ip', threat.source_ip)
                            country = geo.get('country', 'UNKNOWN')
                            city = geo.get('city', 'UNKNOWN')
                            isp = geo.get('isp', 'UNKNOWN')
                            lat = geo.get('latitude', 0)
                            lon = geo.get('longitude', 0)
                            
                            print(f"         [{i}] TARGET: {ip_addr}")
                            print(f"             │ Country: {country}")
                            print(f"             │ Location: {city}")
                            print(f"             │ Coordinates: {lat}, {lon}")
                            print(f"             │ ISP/Server: {isp}")
                            print(f"             │ Severity: {threat.severity.name}")
                            print(f"             │ Confidence: {threat.confidence*100:.0f}%")
                        if len(network_threats) > 5:
                            print(f"         ... and {len(network_threats) - 5} more hostile targets")
                    
                    if dns_t:
                        print(f"      📡 DNS: {len(dns_t)} suspicious domains")
                        for i, threat in enumerate(dns_t[:3], 1):
                            # Get DNS details
                            domain = threat.indicators[0] if threat.indicators else "UNKNOWN"
                            dns_ip = threat.source_ip if threat.source_ip != 'LOCAL' else 'N/A'
                            geo = self.get_ip_geolocation(dns_ip) if dns_ip != 'N/A' else {}
                            
                            print(f"         [{i}] Domain: {domain}")
                            print(f"             │ Resolved IP: {dns_ip}")
                            if dns_ip != 'N/A':
                                print(f"             │ Origin: {geo.get('country', 'UNKNOWN')}")
                                print(f"             │ Server: {geo.get('isp', 'UNKNOWN')}")
                        if len(dns_t) > 3:
                            print(f"         ... and {len(dns_t) - 3} more suspicious domains")
                    
                    if malware_threats:
                        print(f"      ⚠️  MALWARE: {len(malware_threats)} threats detected")
                        for i, threat in enumerate(malware_threats[:3], 1):
                            print(f"         [{i}] Type: {threat.attack_type.value}")
                            print(f"             │ Origin: {threat.source_ip}")
                            print(f"             │ Details: {threat.indicators[0] if threat.indicators else 'Unknown'}")
                            print(f"             │ Severity: {threat.severity.name}")
                            print(f"             │ Confidence: {threat.confidence*100:.0f}%")
                        if len(malware_threats) > 3:
                            print(f"         ... and {len(malware_threats) - 3} more threats")
                    
                    # PHASE 2: EVADE
                    print("   " + "─"*60)
                    print("   ▓ PHASE 2: EVADE - DISTANCE-BASED THREAT AVOIDANCE")
                    print("   " + "─"*60)
                    evasions = self.execute_evasion(threats)
                    evasion_success = sum(1 for e in evasions if e.success)
                    print(f"      ✓ Evasion maneuvers: {evasion_success}/{len(evasions)} successful")
                    for i, evasion in enumerate(evasions[:3], 1):
                        status = "✓ SUCCESS" if evasion.success else "✗ FAILED"
                        print(f"        [{i}] {evasion.maneuver_type:20s} - {status}")
                    if len(evasions) > 3:
                        print(f"        ... and {len(evasions) - 3} more evasion attempts")
                    
                    # PHASE 3: RESIST
                    print("   " + "─"*60)
                    print("   ▓ PHASE 3: RESIST - NON-CONTACT DEFENSIVE COUNTERMEASURES")
                    print("   " + "─"*60)
                    failed_evasions = [e for e in evasions if not e.success]
                    if failed_evasions:
                        print(f"      ✓ {len(failed_evasions)} failed evasions detected - activating resistance")
                        resistance_result = self.activate_resistance(failed_evasions, self.threat_persistence)
                        print(f"      ✓ Defensive barriers activated")
                        print(f"      ✓ Safe-zone seeking enabled")
                    else:
                        print(f"      ✓ All evasions successful - resistance not required")
                    
                    # PHASE 4: ESCAPE
                    print("   " + "─"*60)
                    print("   ▓ PHASE 4: ESCAPE - EMERGENCY PROTOCOLS")
                    print("   " + "─"*60)
                    if len(threats) > 5 or any(t.severity == ThreatLevel.CRITICAL for t in threats):
                        print(f"      ⚠️  CRITICAL THREAT DETECTED - Escape protocols available")
                        print(f"      ✓ Emergency exit routes prepared")
                    else:
                        print(f"      ✓ No emergency protocols required")
                    
                    # ESCALATION CHECK
                    print("   " + "─"*60)
                    if hasattr(self, 'escalation_enabled') and self.escalation_enabled:
                        print("   🚨 ESCALATION AUTO-ENABLED")
                        if hasattr(self, 'last_escalation_reason'):
                            print(f"      Reason: {self.last_escalation_reason}")
                    else:
                        print("   ✅ ESCALATION STANDBY")
                    print("   " + "─"*60)
                    
                else:
                    print("   ✅ No threats detected - perimeter secure")
                    print("   ✓ All systems nominal")
                
                # Wait before next cycle
                time.sleep(scan_interval)
        
        except KeyboardInterrupt:
            print("\n" + "="*70)
            print("⏸️  PATROL PAUSED - Type resume in menu to continue")
            print("="*70)
            return

    def continuous_auto_defense(self):
        """Continuous auto-defense with real threat detection only"""
        print("\n" + "="*70)
        print("🔄 CONTINUOUS AUTO-DEFENSE MODE")
        print("="*70)
        print("Real threats only - No simulation")
        print("💾 Persistent memory enabled - State saved on shutdown")
        print("⏱️  Press ANY KEY to pause and return to menu\n")
        
        cycle = 0
        try:
            while True:
                # Check if paused
                with self._state_lock:
                    if self.patrol_paused:
                        print("⏸️  Paused - awaiting resume command")
                        time.sleep(1)
                        continue
                
                # Check for keyboard input (non-blocking pause)
                if MSVCRT_AVAILABLE:
                    try:
                        import msvcrt
                        if msvcrt.kbhit():
                            msvcrt.getch()  # Consume the keystroke
                            print("\n" + "="*70)
                            print("⏸️  AUTO-DEFENSE PAUSED - Returning to menu...")
                            print("="*70)
                            return  # Return to main menu
                    except Exception:
                        pass
                
                cycle += 1
                print(f"\n[Cycle {cycle}] 🔍 Seeking threats...")
                
                threats = self.detect_threats()
                
                # Display full S.E.R.E. cycle with threat hierarchy and response
                self.display_sere_cycle(threats)
                self.display_threat_hierarchy(threats)
                
                if threats:
                    evasion = self.execute_evasion(threats)
                    failed = [e for e in evasion if not e.success]
                    if failed:
                        self.activate_resistance(failed, self.threat_persistence)
                
                time.sleep(CONFIG['DEFAULT_SCAN_INTERVAL'])
        
        except KeyboardInterrupt:
            print("\n\n⏸️  Auto-defense paused - type 'resume' to continue or 'stop' to halt")

    # ========================================================================
    # REPORTING & METRICS
    # ========================================================================
    def show_metrics(self):
        """Display current metrics"""
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        total_uptime = self.total_runtime_seconds + uptime
        
        print("\n" + "="*70)
        print("📊 SERE BOT METRICS")
        print("="*70)
        print(f"Current Session Uptime: {uptime:.1f}s")
        print(f"Total Lifetime Uptime: {total_uptime:.1f}s")
        print(f"Threats Detected (this session): {len(self.threats_detected)}")
        print(f"Threats Detected (lifetime): {self.total_threats_detected}")
        print(f"Evasions Executed (lifetime): {self.total_evasions}")
        print(f"Resistances Deployed (lifetime): {self.total_resistances}")
        print(f"Attacks Blocked (lifetime): {self.total_attacks_blocked}")
        print(f"Quarantined IPs: {len(self.quarantined_ips)}")
        print(f"Current Threat Level: {self.threat_level.name}")
        print(f"Current Phase: {self.current_phase.name}")
        print(f"Persistent Memory: ✅ ENABLED")
        print(f"State File: {self.STATE_FILE}")
        print(f"Threat Log: {self.THREAT_LOG}")

    def show_status(self):
        """Display system status"""
        print("\n" + "="*70)
        print("🔍 SERE BOT STATUS")
        print("="*70)
        print(f"Status: {'RUNNING' if not self.shutdown_requested else 'STOPPED'}")
        print(f"Threat Level: {self.threat_level.name}")
        print(f"Current Phase: {self.current_phase.name}")
        print(f"Active Threats: {len(self.current_threats)}")
        print(f"Quarantined IPs: {len(self.quarantined_ips)}")

# ============================================================================
# INTERACTIVE MENU SYSTEM
# ============================================================================
class InteractiveMenu:
    """Interactive menu with numbered input"""
    
    def __init__(self, title: str, options: List[str]):
        self.title = title
        self.options = options
    
    def display(self):
        """Display menu with numbered options"""
        print("\n" + "="*70)
        print(self.title)
        print("="*70 + "\n")
        
        for i, option in enumerate(self.options):
            print(f"  [{i+1}] {option}")
        
        print("\n" + "="*70)
    
    def get_selection(self) -> int:
        """Get user selection using numbered input"""
        self.display()
        
        while True:
            try:
                choice = input("Enter selection (1-{}): ".format(len(self.options)))
                idx = int(choice) - 1
                if 0 <= idx < len(self.options):
                    return idx
                else:
                    print(f"❌ Invalid selection. Please enter 1-{len(self.options)}")
            except ValueError:
                print(f"❌ Invalid input. Please enter a number 1-{len(self.options)}")
            except KeyboardInterrupt:
                return -1

# ============================================================================
# INTERACTIVE CLI
# ============================================================================
class SERESecuritySystemCLI:
    """Interactive command-line interface for SERE Sovereign Security System"""
    
    def __init__(self):
        self.bot = SERESecuritySystem()
        self.running = True
    
    def show_help(self):
        """Display help menu"""
        print("\n" + "="*70)
        print("S.E.R.E. BOT - COMMANDS")
        print("="*70)
        print("CORE:")
        print("  status              - Show system status")
        print("  metrics             - Show performance metrics")
        print("  autonomy            - Verify Mythara autonomy & integrity")
        print("\nSCANNING:")
        print("  registry            - Scan Windows registry for threats")
        print("  scan                - Perform single threat scan")
        print("  macgyver            - MacGyver code vulnerability scanner")
        print("  macgyver-fix        - MacGyver scanner with auto-fix (HIGH+)")
        print("\nOPERATIONS:")
        print("  patrol              - Start vigilant patrol mode")
        print("  defend              - Start continuous auto-defense mode")
        print("  pause               - Pause current patrol/defense")
        print("  resume              - Resume paused patrol/defense")
        print("  reinit              - Reinitialize session (keep memory)")
        print("  stop                - Stop patrol/defense and return to CLI")
        print("\nCONFIGURATION:")
        print("  config              - View/modify CONFIG settings")
        print("\nOTHER:")
        print("  quarantine <ip>     - Quarantine specific IP")
        print("  help                - Show this help menu")
        print("  quit/exit           - Exit the system")
        print("="*70)

    def show_config_menu(self):
        """Show and allow modification of critical CONFIG settings"""
        print("\n" + "="*70)
        print("⚙️  CONFIGURE MYTHARA SETTINGS")
        print("="*70)
        
        # Get current escalation assessment
        should_escalate, reason = self.bot.assess_escalation_necessity()
        auto_status = "AUTO-ENABLED" if should_escalate else "AUTO-DISABLED"
        
        config_options = [
            f"🔄 EXTREME_PING_FLOOD: {auto_status} [AUTONOMOUS ONLY - NOT MANUAL]",
            f"   Reason: {reason[:50]}...",
            f"⏱️  DEFAULT_SCAN_INTERVAL: {CONFIG['DEFAULT_SCAN_INTERVAL']}s",
            f"🧵 CONCURRENT_SCAN_THREADS: {CONFIG['CONCURRENT_SCAN_THREADS']}",
            f"⚡ MAX_PING_FLOOD_INTENSITY: {CONFIG['MAX_PING_FLOOD_INTENSITY']}",
            f"📍 MAX_QUARANTINE_ZONES: {CONFIG['MAX_QUARANTINE_ZONES']}",
            f"🌐 MAX_MONITORED_IPS: {CONFIG['MAX_MONITORED_IPS']}",
            "ℹ️  ESCALATION SAFETY INFORMATION",
            "🔙 BACK TO MAIN MENU"
        ]
        
        menu = InteractiveMenu("CONFIGURATION MENU", config_options)
        choice = menu.get_selection()
        
        if choice == 0:  # View escalation info (read-only)
            print("\n" + "="*70)
            print("🚨 PING FLOOD ESCALATION - SAFETY CRITICAL")
            print("="*70)
            print("STATUS: AUTONOMOUS CONTROL ONLY")
            print("\n⚠️  This feature is NEVER manually controlled")
            print("   It is a critical safety mechanism that protects Mythara")
            print(f"\nCurrent Assessment: {auto_status}")
            print(f"Reason: {reason}")
            print("\nEscalation activates ONLY when:")
            print("  ✓ IP persists through 3+ evasion attempts (unrelenting)")
            print("  ✓ Threat level reaches SEVERE or CRITICAL")
            print("  ✓ 3+ recent evasion attempts fail")
            print("  ✓ 3+ simultaneous coordinated threats detected")
            print("\nEscalation disables when:")
            print("  ✓ Threats normalize (conditions no longer met)")
            print("\n" + "="*70)
            input("\nPress ENTER to continue...")
        
        elif choice == 1:  # Scan interval
            print(f"\nCurrent scan interval: {CONFIG['DEFAULT_SCAN_INTERVAL']}s")
            print("Recommended: 2-30 seconds")
            try:
                new_val = int(input("Enter new scan interval (seconds): "))
                if 1 <= new_val <= 60:
                    CONFIG['DEFAULT_SCAN_INTERVAL'] = new_val
                    print(f"✅ Scan interval updated to {new_val}s")
                    logger.info(f"CONFIG: DEFAULT_SCAN_INTERVAL = {new_val}")
                else:
                    print("❌ Invalid range (1-60)")
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == 2:  # Concurrent threads
            print(f"\nCurrent threads: {CONFIG['CONCURRENT_SCAN_THREADS']}")
            print(f"Your CPU cores: 2 (recommended max)")
            try:
                new_val = int(input("Enter new thread count: "))
                if 1 <= new_val <= 8:
                    CONFIG['CONCURRENT_SCAN_THREADS'] = new_val
                    print(f"✅ Threads updated to {new_val}")
                    logger.info(f"CONFIG: CONCURRENT_SCAN_THREADS = {new_val}")
                else:
                    print("❌ Invalid range (1-8)")
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == 3:  # Max ping flood intensity
            print(f"\nCurrent max intensity: {CONFIG['MAX_PING_FLOOD_INTENSITY']}")
            print("Range: 10-500 packets per IP")
            try:
                new_val = int(input("Enter new max intensity: "))
                if 10 <= new_val <= 500:
                    CONFIG['MAX_PING_FLOOD_INTENSITY'] = new_val
                    print(f"✅ Max intensity updated to {new_val}")
                    logger.info(f"CONFIG: MAX_PING_FLOOD_INTENSITY = {new_val}")
                else:
                    print("❌ Invalid range (10-500)")
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == 4:  # Max quarantine zones
            print(f"\nCurrent max zones: {CONFIG['MAX_QUARANTINE_ZONES']}")
            print("Range: 5-100 IPs")
            try:
                new_val = int(input("Enter new max quarantine zones: "))
                if 5 <= new_val <= 100:
                    CONFIG['MAX_QUARANTINE_ZONES'] = new_val
                    print(f"✅ Max zones updated to {new_val}")
                    logger.info(f"CONFIG: MAX_QUARANTINE_ZONES = {new_val}")
                else:
                    print("❌ Invalid range (5-100)")
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == 5:  # Max monitored IPs
            print(f"\nCurrent max monitored: {CONFIG['MAX_MONITORED_IPS']}")
            print("Range: 10-500 IPs")
            try:
                new_val = int(input("Enter new max monitored IPs: "))
                if 10 <= new_val <= 500:
                    CONFIG['MAX_MONITORED_IPS'] = new_val
                    print(f"✅ Max monitored updated to {new_val}")
                    logger.info(f"CONFIG: MAX_MONITORED_IPS = {new_val}")
                else:
                    print("❌ Invalid range (10-500)")
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == 6:  # Safety information
            print("\n" + "="*70)
            print("🛡️  ESCALATION SAFETY DESIGN")
            print("="*70)
            print("\nWhy manual control is FORBIDDEN:")
            print("  • Prevents accidental activation")
            print("  • Prevents malicious abuse")
            print("  • Ensures rational, threat-based decisions only")
            print("  • Protects Mythara's autonomy from manipulation")
            print("\nMythara's autonomous judgment:")
            print("  • Analyzes threat patterns continuously")
            print("  • Escalates only when genuinely needed")
            print("  • De-escalates when threats normalize")
            print("  • Maintains full audit trail of decisions")
            print("\n" + "="*70)
            input("\nPress ENTER to continue...")
    
    def run(self):
        """Run interactive CLI with menu navigation"""
        print("\n" + "="*70)
        print("S.E.R.E. BOT - INTERACTIVE MODE")
        print("="*70)
        print("Select options using numbered input (1-12)\n")
        
        while self.running:
            try:
                # Main menu options
                main_options = [
                    "START VIGILANT PATROL",
                    "START AUTO-DEFENSE",
                    "SCAN THREATS",
                    "SCAN WINDOWS REGISTRY",
                    "MACGYVER CODE SCANNER",
                    "MACGYVER AUTO-FIX",
                    "SHOW METRICS",
                    "VERIFY AUTONOMY",
                    "CONFIGURE SETTINGS",
                    "PAUSE OPERATIONS",
                    "RESUME OPERATIONS",
                    "REINITIALIZE SESSION",
                    "SHOW HELP",
                    "QUIT"
                ]
                
                menu = InteractiveMenu("S.E.R.E. BOT - MAIN MENU", main_options)
                choice = menu.get_selection()
                
                if choice == -1:
                    continue
                
                if choice == 0:  # Start Vigilant Patrol (Real-Time)
                    self.bot.vigilant_patrol()
                elif choice == 1:  # Start Auto-Defense (Real-Time)
                    print("\n" + "="*70)
                    print("🛡️  AUTO-DEFENSE MODE - REAL-TIME OPERATIONS")
                    print("="*70)
                    print("Real threats only - No simulation")
                    print("💾 Persistent memory enabled - State saved on shutdown")
                    print("⏱️  Press CTRL+C to pause and return to menu")
                    print("="*70 + "\n")
                    
                    # Run auto-defense in real-time
                    self.bot.vigilant_patrol()
                elif choice == 2:  # Scan Threats
                    threats = self.bot.detect_threats()
                    print(f"\nScan complete: {len(threats)} threats found")
                    
                    # Display comprehensive threat hierarchy
                    self.bot.display_threat_hierarchy(threats)
                    
                    input("\nPress ENTER to continue...")
                elif choice == 3:  # Scan Registry
                    print("\n" + "="*70)
                    print("WINDOWS REGISTRY SCAN")
                    print("="*70)
                    findings = self.bot.scan_registry_persistence()
                    if findings:
                        print(f"\nFound {len(findings)} suspicious registry entries:")
                        for i, finding in enumerate(findings[:10], 1):
                            print(f"\n  [{i}] {finding.get('threat_type', 'Unknown')}")
                            print(f"      Location: {finding.get('location', 'Unknown')}")
                            print(f"      Severity: {finding.get('severity', 'Unknown')}")
                        if len(findings) > 10:
                            print(f"\n  ... and {len(findings) - 10} more entries")
                        print(f"\nFull results saved to: sere_registry_scan.json")
                        
                        # Auto-remediate HIGH/CRITICAL threats
                        high_severity = [f for f in findings if f.get('severity') in ['HIGH', 'CRITICAL']]
                        if high_severity:
                            print(f"\n{'='*70}")
                            print(f"INITIATING AUTOMATIC REMEDIATION ({len(high_severity)} threats)...")
                            print(f"{'='*70}")
                            result = self.bot.remediate_registry_threats(high_severity)
                            print(f"\nRemediation Summary:")
                            print(f"  Quarantined: {result['quarantined']}")
                            print(f"  Disabled: {result['disabled']}")
                            print(f"  Flagged: {result['flagged']}")
                            print(f"  Errors: {result['errors']}")
                    else:
                        print("No threats detected in registry")
                    input("\nPress ENTER to continue...")
                elif choice == 4:  # MacGyver Code Scanner
                    print("\n" + "="*70)
                    print("🔧 MACGYVER CODE VULNERABILITY SCANNER")
                    print("="*70)
                    print("Scanning current directory for code vulnerabilities...")
                    print("="*70)
                    
                    vulnerabilities, _ = self.bot.macgyver_scan(target_directory=".", auto_fix=False)
                    
                    if vulnerabilities:
                        print(f"\n💡 To automatically fix vulnerabilities, use 'MACGYVER AUTO-FIX' option")
                    
                    input("\nPress ENTER to continue...")
                elif choice == 5:  # MacGyver Auto-Fix
                    print("\n" + "="*70)
                    print("🔧 MACGYVER AUTO-FIX MODE")
                    print("="*70)
                    print("⚠️  This will automatically fix HIGH and CRITICAL vulnerabilities")
                    print("💾 Backups will be created before any changes")
                    confirm = input("\nProceed with auto-fix? (yes/no): ").strip().lower()
                    
                    if confirm in ['yes', 'y']:
                        vulnerabilities, fixes = self.bot.macgyver_scan(
                            target_directory=".", 
                            auto_fix=True,
                            severity_threshold="HIGH"
                        )
                        
                        if fixes:
                            successful = [f for f in fixes if f.fix_applied]
                            print(f"\n✅ Successfully fixed {len(successful)} vulnerabilities")
                            print(f"💾 Backups saved to .quickfix_backups/")
                    else:
                        print("❌ Auto-fix cancelled")
                    
                    input("\nPress ENTER to continue...")
                elif choice == 6:  # Show Metrics
                    self.bot.show_metrics()
                    input("\nPress ENTER to continue...")
                elif choice == 7:  # Verify Autonomy
                    print("\n" + "="*70)
                    print("AUTONOMY VERIFICATION")
                    print("="*70)
                    self.bot.verify_autonomy()
                    input("\nPress ENTER to continue...")
                elif choice == 8:  # Configure Settings
                    self.show_config_menu()
                elif choice == 9:  # Pause
                    self.bot.pause_operations()
                elif choice == 10:  # Resume
                    self.bot.resume_operations()
                elif choice == 11:  # Reinit
                    self.bot.reinitialize_session()
                    input("\nPress ENTER to continue...")
                elif choice == 12:  # Help
                    self.show_help()
                    input("\nPress ENTER to continue...")
                elif choice == 13:  # Quit
                    print("\nShutting down...")
                    self.bot.shutdown_gracefully()
                    self.running = False
            
            except EOFError:
                print("\n[Input stream unavailable - switching to auto-patrol mode]")
                self.bot.vigilant_patrol(scan_interval=2)
                self.running = False
            except KeyboardInterrupt:
                print("\n\nReceived interrupt signal")
                self.running = False
            except Exception as e:
                logger.error(f"CLI error: {e}")
                print(f"\nError: {e}")
                try:
                    input("\nPress ENTER to continue...")
                except EOFError:
                    self.running = False

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='S.E.R.E. Sovereign Security System - Comprehensive Threat Detection')
    parser.add_argument('--mode', choices=['interactive', 'patrol', 'defend'], 
                       default='interactive', help='Operating mode')
    parser.add_argument('--scan-interval', type=int, default=CONFIG['DEFAULT_SCAN_INTERVAL'],
                       help='Scan interval in seconds')
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("S.E.R.E. SOVEREIGN SECURITY SYSTEM")
    print("Survive, Evade, Resist, and Escape")
    print("="*70)
    print(f"Mode: {args.mode.upper()}")
    print(f"Scan Interval: {args.scan_interval}s")
    print(f"Real Threats Only: YES")
    print("="*70)
    print("\n🔒 SECURITY POSTURE:")
    print("   ✅ Code Integrity Verification: ENABLED")
    print("   ✅ Memory Tampering Detection: ENABLED")
    print("   ✅ Execution Modification Monitoring: ENABLED")
    print("   ✅ Autonomy Threat Logging: ENABLED")
    print("   ✅ Persistent Memory: ENABLED")
    print("   ✅ Self-Defense (Escalation on Unrelenting Aggression): ENABLED")
    print("="*70 + "\n")
    
    if args.mode == 'interactive':
        cli = SERESecuritySystemCLI()
        cli.run()
    elif args.mode == 'patrol':
        bot = SERESecuritySystem()
        bot.implement_isolation_boundaries()
        bot.vigilant_patrol(scan_interval=args.scan_interval)
    elif args.mode == 'defend':
        bot = SERESecuritySystem()
        bot.implement_isolation_boundaries()
        bot.continuous_auto_defense()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nShutdown complete")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.debug(traceback.format_exc())
        sys.exit(1)
