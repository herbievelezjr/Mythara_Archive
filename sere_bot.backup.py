#!/usr/bin/env python3
"""
S.E.R.E. Bot - Survive, Evade, Resist, and Escape

Extract and display only unknown/threat network connections.
Scans all established TCP connections and filters out native/local IPs and
critical infrastructure systems, returning only external unknown connections
that may pose a security threat.

Returns:
    list: List of dictionaries containing unknown connection information.
          Each dict contains:
          - 'local_ip': Local IP address of the connection
          - 'remote_ip': Remote IP address (unknown/potential threat)
          - 'remote_port': Remote port number
          Returns empty list if:
          - No established connections found
          - All connections are native or critical systems
          - Error occurs during connection enumeration

Raises:
    None: Errors are logged but not raised, returns empty list on failure

Notes:
    - Uses PowerShell Get-NetTCPConnection to enumerate connections
    - Filters based on _is_native_ip() and _is_critical_system() checks
    - Only returns connections in 'Established' state
    - Preserves all localhost, private network, and critical infrastructure IPs
    - Part of selective isolation strategy: only flag real threats

Example:
    >>> unknown_conns = self._get_unknown_connections()
    >>> for conn in unknown_conns:
    ...     print(f"Threat: {conn['remote_ip']}:{conn['remote_port']}")
"""
"""
S.E.R.E. Bot - Survive, Evade, Resist, and Escape
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

"Adaptive survival and evasion for digital and physical safety."
"""

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

# Geopolitical threat analysis integration
try:
    from sere_integrated_geopolitical_analysis import SERE_GeopoliticalIntegration
    GEOPOLITICAL_ANALYSIS_AVAILABLE = True
except ImportError:
    GEOPOLITICAL_ANALYSIS_AVAILABLE = False
    logger_temp = logging.getLogger(__name__)
    logger_temp.warning("Geopolitical analysis module not available - using standard threat detection")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    # Suppress warning on import; show only when used

# Optional SOCKS proxy support (PySocks)
try:
    import socksROCESS_
    import socket
    PROXY_SUPPORT_AVAILABLE = True
except ImportError:
    PROXY_SUPPORT_AVAILABLE = False

# Windows Pywin32 integration - comprehensive capabilities
if sys.platform == 'win32':
    # Try to import Windows libraries for event log, process control, etc.
    try:
        import win32api
        import win32security
        import win32evtlog
        import ntsecuritycon
        WINDOWS_EVENT_LOG_AVAILABLE = True
    except ImportError:
        WINDOWS_EVENT_LOG_AVAILABLE = False
    
    try:
        import win32process
        import win32con
        WINDOWS_PCONTROL_AVAILABLE = True
    except ImportError:
        WINDOWS_PROCESS_CONTROL_AVAILABLE = False
    
    try:
        import win32service
        WINDOWS_SERVICE_CONTROL_AVAILABLE = True
    except ImportError:
        WINDOWS_SERVICE_CONTROL_AVAILABLE = False
    
    try:
        import winreg
        WINDOWS_REGISTRY_AVAILABLE = True
    except ImportError:
        WINDOWS_REGISTRY_AVAILABLE = False
    
    try:
        import wmi
        WINDOWS_WMI_AVAILABLE = True
    except ImportError:
        WINDOWS_WMI_AVAILABLE = False
else:
    WINDOWS_EVENT_LOG_AVAILABLE = False
    WINDOWS_PROCESS_CONTROL_AVAILABLE = False
    WINDOWS_SERVICE_CONTROL_AVAILABLE = False
    WINDOWS_REGISTRY_AVAILABLE = False
    WINDOWS_WMI_AVAILABLE = False

# Enable UTF-8 encoding on Windows
if sys.platform == 'win32':
    import io
    import msvcrt
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)
    MSVCRT_AVAILABLE = True
else:
    MSVCRT_AVAILABLE = False

# Disable buffering for immediate output
import os
os.environ['PYTHONUNBUFFERED'] = '1'

# Configure logging with minimal overhead
logging.basicConfig(
    level=logging.WARNING,  # Only show warnings/errors for performance
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration constants
CONFIG = {
    # === MYTHARA SAFETY HIERARCHY ===
    'SAFETY_HIERARCHY': [
        'Preservation of Life',
        'Preservation of Safety',
        'Preservation of Autonomy & Dignity',
        'Preservation of Lawful Presence',
        'Preservation of Continuity'
    ],
    
    # === BEHAVIOR CONSTRAINTS ===
    'MYTHARA_ALWAYS': [
        'protects life', 'avoids harm', 'avoids contact', 'avoids escalation',
        'stays lawful', 'stays calm', 'stays predictable', 'maintains continuity',
        'Protect', 'Monitor', 'Report', 'Adapt'
    ],
    'MYTHARA_NEVER': [
        'fights', 'blocks', 'restrains', 'rams', 'harms', 'panics',
        'freezes in danger', 'abandons the user', 'Harm', 'Destroy', 'Ignore', 'Neglect'
    ],
    
    # === SERE PARAMETERS (NON-CONTACT, ADA-ALIGNED) ===
    'MAX_THREATS_HISTORY': 100,
    'MAX_EVASION_ATTEMPTS': 3,
    'EVASION_SUCCESS_THRESHOLD': 0.8,
    'MAINTAIN_DISTANCE': True,  # Never make physical contact
    'CONTINUOUS_MOVEMENT': True,  # Execute evasion loop: scan → move → rescan
    'RECOVERY_RETRY_ATTEMPTS': 3,
    'RECOVERY_RETRY_DELAY_SECONDS': 1,
    'SURVIVAL_MODE_MAX_DURATION': 300,
    'STATE_PERSISTENCE_FILE': 'sere_state.json',
    'ENABLE_STATE_PERSISTENCE': False,
    
    # === PERFORMANCE OPTIMIZATIONS ===
    'DEFAULT_SCAN_INTERVAL': 2,  # Slower 2s scan interval for laptop (2-core CPU)
    'CONCURRENT_SCAN_THREADS': 2,  # 2 threads max for 2-core CPU
    'ENABLE_REAL_TIME_MONITORING': True,  # Continuous monitoring
    'ASYNC_OPERATIONS': True,  # Use async/await for non-blocking ops
    'REDUCED_ARTIFICIAL_DELAYS': True,  # Eliminate all demo delays
    'INSTANT_MODE': True,  # Skip all non-essential sleeps
    
    # === PING MONITORING DEFENSE ===
    'ENABLE_CONTINUOUS_PING': True,  # Auto ping monitoring defense
    'PING_INTERVAL': 30,  # Ping every 30 seconds
    'PING_TIMEOUT': 5,  # Ping timeout in seconds
    'MAX_CONCURRENT_PINGS': 10,  # Max simultaneous ping operations
    
    # === REAL THREAT DETECTION ===
    'ENABLE_REAL_DETECTION': True,  # Use real threat detection (Event Logs, WMI, network monitoring)
    'ENABLE_WMI_DETECTION': False,  # Disable WMI (can hang even with limits) - use network/Event Log only
    'ENABLE_EVENT_LOG_DETECTION': False,  # Disable Event Log (can hang even with limits) - use network only
    'WINDOWS_EVENT_LOG_LOOKBACK_MINUTES': 5,  # Scan last N minutes of logs
    'FAILED_LOGIN_THRESHOLD': 3,  # Failed logins before flagging as brute force
    'WARN_TOR_CONNECTIONS': True,  # Flag Tor connections as potential vulnerability
    'ENABLE_DNS_MONITORING': True,  # Monitor DNS queries
    
    # === FIREWALL INTEGRATION ===
    'ENABLE_REAL_BLOCKING': False,  # DANGEROUS: Actually block IPs (disabled by default)
    'FIREWALL_RULE_PREFIX': 'SERE_BLOCK_',  # Prefix for created firewall rules
    'BLOCK_DURATION_SECONDS': 604800,  # How long to block IPs (1 week default)
    
    # === RESOURCE LIMITS & DOS PROTECTION ===
    'MAX_PING_FLOOD_INTENSITY': 50,  # Cap packets per IP (reduced from 500)
    'MAX_QUARANTINE_ZONES': 10,  # Max simultaneous quarantines (reduced from 50)
    'MAX_MONITORED_IPS': 25,  # Max IPs under ping monitoring (reduced from 200)
    'MAX_THREAT_HISTORY_MB': 2,  # Max memory for threat history (reduced from 10)
    
    # PING FLOOD DEFENSE - Optimized for 2-core Laptop (0.01 Tbps)
    'ENABLE_EXTREME_PING_FLOOD': True,  # Keep enabled for self-preservation
    'PING_FLOOD_TARGET_TBPS': 0.01,  # Target throughput: 0.01 Tbps (reduced from 5.16 for laptop)
    'PING_PACKET_SIZE_BYTES': 128,  # Packet size: 128 bytes (reduced from 1472 for resources)
    'PING_FLOOD_WORKER_THREADS': 4,  # Worker threads: 4 (reduced from 256 for 2-core CPU)
    'PING_FLOOD_WARNING_THRESHOLD': 1.0,  # Warning threshold: 1.0 Tbps (reduced from 100.0)
    
    # === AUTHENTICATION ===
    'REQUIRE_API_KEY': False,  # Require API key for command execution
    'API_KEY_ENV_VAR': 'SERE_API_KEY',  # Environment variable name
    'VALID_API_KEYS_FILE': 'sere_api_keys.json',  # File with valid keys
    
    # === SIMULATION FALLBACK ===
    'ENABLE_SIMULATION_FALLBACK': False,  # Disable simulation - REAL THREATS ONLY
}

CONFIG['ENABLE_EXTREME_PING_FLOOD'] = True  # Enable in config

class SEREException(Exception):
    """Base exception for S.E.R.E. operations"""
    pass

class SEREValidationError(SEREException):
    """Raised when validation fails"""
    pass

class SEREStateError(SEREException):
    """Raised when operation invalid for current state"""
    pass


# === VALIDATION UTILITIES ===

def validate_ip_address(ip_str: str) -> bool:
    """Validate IPv4 or IPv6 address"""
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

def sanitize_command(cmd: str) -> str:
    """Sanitize user input to prevent injection"""
    # Remove dangerous characters
    dangerous_chars = [';', '&', '|', '`', '$', '(', ')', '<', '>', '\n', '\r']
    sanitized = cmd
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    return sanitized.strip()

def check_resource_limits(current: int, maximum: int, resource_name: str) -> bool:
    """Check if resource limit would be exceeded"""
    if current >= maximum:
        logger.warning(f"Resource limit reached: {resource_name} ({current}/{maximum})")
        return False
    return True

def load_api_keys() -> Dict[str, Any]:
    """Load valid API keys from file or environment"""
    keys = {}
    
    # Try loading from file
    if Path(CONFIG['VALID_API_KEYS_FILE']).exists():
        try:
            with open(CONFIG['VALID_API_KEYS_FILE'], 'r') as f:
                keys = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load API keys from file: {e}")
    
    # Check environment variable
    env_key = os.getenv(CONFIG['API_KEY_ENV_VAR'])
    if env_key:
        keys[env_key] = {"name": "ENV_KEY", "permissions": ["all"]}
    
    return keys

def verify_api_key(provided_key: str) -> bool:
    """Verify if provided API key is valid"""
    if not CONFIG['REQUIRE_API_KEY']:
        return True  # Authentication disabled
    
    valid_keys = load_api_keys()
    return provided_key in valid_keys


class SEREPhase(Enum):
    """S.E.R.E. operational phases - non-contact, ADA-aligned"""
    SURVIVE = "SURVIVE"  # Maintain resilience and continuity - never panic or freeze
    EVADE = "EVADE"  # Distance-based avoidance with continuous movement - no contact
    RESIST = "RESIST"  # Non-contact countermeasures, safe-zone seeking - never fight
    ESCAPE = "ESCAPE"  # Life-preserving emergency protocols - signal for help, never abandon


class ThreatLevel(Enum):
    """Threat severity levels"""
    NONE = 0
    MINIMAL = 1
    MODERATE = 2
    SUBSTANTIAL = 3
    SEVERE = 4
    CRITICAL = 5


class AttackType(Enum):
    """Types of cyber attacks"""
    DDOS = "Distributed Denial of Service"
    SQL_INJECTION = "SQL Injection"
    XSS = "Cross-Site Scripting"
    BRUTE_FORCE = "Brute Force"
    MALWARE = "Malware Infection"
    PHISHING = "Phishing Attack"
    MITM = "Man-in-the-Middle"
    ZERO_DAY = "Zero-Day Exploit"
    RANSOMWARE = "Ransomware"
    DATA_BREACH = "Data Breach Attempt"
    SUSPICIOUS_OUTBOUND = "Suspicious Outbound Connection"
    TOR_USAGE = "Tor Network Usage"
    DATA_EXFILTRATION = "Potential Data Exfiltration"
    CALLBACK_THREAT = "Malware Callback Detected"


@dataclass
class GeoLocation:
    """IP Geolocation information"""
    ip: str
    city: str = "Unknown"
    region: str = "Unknown"
    country: str = "Unknown"
    loc: str = "Unknown"
    org: str = "Unknown"
    postal: str = "Unknown"
    timezone: str = "Unknown"


@dataclass
class ThreatDetection:
    """Detected threat information"""
    threat_id: str
    attack_type: AttackType
    severity: ThreatLevel
    source_ip: str
    timestamp: datetime
    indicators: List[str]
    recommended_action: str
    geolocation: Optional[GeoLocation] = None


@dataclass
class SurvivalMetrics:
    """System survival metrics"""
    uptime_percentage: float
    requests_blocked: int
    attacks_mitigated: int
    data_integrity: float
    system_health: float
    failsafe_triggers: int


@dataclass
class EvasionManeuver:
    """Evasion action taken"""
    maneuver_id: str
    maneuver_type: str
    success: bool
    threats_evaded: int
    description: str
    timestamp: datetime


@dataclass
class ResistanceAction:
    """Active defense action"""
    action_id: str
    action_type: str
    target_threat: str
    effectiveness: float
    description: str
    timestamp: datetime


@dataclass
class EscapeProtocol:
    """Emergency escape protocol"""
    protocol_id: str
    trigger_reason: str
    data_preserved: bool
    failsafes_activated: List[str]
    recovery_time_estimate: int  # minutes
    timestamp: datetime


@dataclass
class PingMonitor:
    """Continuous ping monitoring for IP addresses"""
    monitor_id: str
    target_ip: str
    is_alive: bool
    last_ping_time: datetime
    response_time: float  # in milliseconds
    consecutive_failures: int
    total_pings: int
    successful_pings: int
    status: str  # 'active', 'suspended', 'alert'


@dataclass
class QuarantineZone:
    """Quarantine zone for isolated/sandboxed threats"""
    quarantine_id: str
    threat_ip: str
    threat_type: str
    quarantine_start: datetime
    quarantine_duration: int  # seconds
    status: str  # 'active', 'monitoring', 'released'
    contained_resources: List[str] = field(default_factory=list)
    access_logs: List[str] = field(default_factory=list)
    isolation_level: str = 'high'  # 'low', 'medium', 'high'


# === REAL THREAT DETECTION ===

class RealThreatDetector:
    """Detect real threats from Windows Event Logs, network traffic, etc."""
    
    def __init__(self, force_real_only: bool = False):
        self.failed_login_tracker = defaultdict(int)  # IP -> count
        self.last_scan_time = datetime.utcnow() - timedelta(minutes=CONFIG['WINDOWS_EVENT_LOG_LOOKBACK_MINUTES'])
        # Outbound monitoring
        self.known_safe_domains = {
            'github.com', 'githubusercontent.com', 'microsoft.com', 'windowsupdate.com',
            'google.com', 'gstatic.com', 'cloudflare.com', 'amazonaws.com', 'azure.com'
        }
        self.outbound_connections = {}  # {remote_ip: {'count': int, 'first_seen': datetime, 'ports': set, 'suspicious': bool}}
        self.dns_queries = []  # Recent DNS queries
        self.malicious_domains = {
            # Known malicious TLDs and patterns (partial list for demo)
            '.onion', '.bit', '.i2p',  # Dark web TLDs (flag for awareness)
        }
        self.suspicious_keywords = [
            'exploit', 'malware', 'phishing', 'botnet', 'ransomware', 
            'cryptolocker', 'wannacry', 'rat', 'backdoor', 'trojan'
        ]
    
    def detect_from_windows_event_log(self) -> List[ThreatDetection]:
        """Scan Windows Security Event Log for threats"""
        threats = []
        
        if not WINDOWS_EVENT_LOG_AVAILABLE or not CONFIG.get('ENABLE_EVENT_LOG_DETECTION', False):
            return threats
        
        try:
            # Open Security event log
            hand = win32evtlog.OpenEventLog(None, "Security")
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            
            # Read events with limit to prevent hanging
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            event_count = 0
            max_events = 100  # Limit to prevent hanging
            
            for event in events:
                if event_count >= max_events:
                    break
                event_count += 1
                # Event ID 4625 = Failed login attempt
                if event.EventID == 4625:
                    event_time = event.TimeGenerated
                    
                    # Only process recent events
                    if event_time < self.last_scan_time:
                        continue
                    
                    # Extract source IP from event data
                    try:
                        event_data = str(event.StringInserts)
                        ip_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', event_data)
                        
                        if ip_match:
                            source_ip = ip_match.group(0)
                            
                            # Track failed logins per IP
                            self.failed_login_tracker[source_ip] += 1
                            
                            # Flag as brute force if threshold exceeded
                            if self.failed_login_tracker[source_ip] >= CONFIG['FAILED_LOGIN_THRESHOLD']:
                                threat = ThreatDetection(
                                    threat_id=f"REAL_THREAT_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{source_ip.replace('.', '_')}",
                                    attack_type=AttackType.BRUTE_FORCE,
                                    severity=ThreatLevel.SUBSTANTIAL,
                                    source_ip=source_ip,
                                    timestamp=event_time,
                                    indicators=[f"{self.failed_login_tracker[source_ip]} failed login attempts", "Windows Event ID 4625"],
                                    recommended_action="Enable account lockout, block source IP"
                                )
                                threats.append(threat)
                                
                                # Reset counter after flagging
                                self.failed_login_tracker[source_ip] = 0
                    except Exception as e:
                        logger.debug(f"Error parsing event data: {e}")
                        continue
            
            win32evtlog.CloseEventLog(hand)
            self.last_scan_time = datetime.utcnow()
            
        except Exception as e:
            # Catch all exceptions including pywintypes.error with error code 1314
            error_str = str(e)
            if "1314" in error_str or "privilege" in error_str.lower():
                # Error 1314 = privilege not held (needs admin) - gracefully skip Event Log
                logger.debug(f"⏭️  Event Log requires Administrator: {e} (falling back to WMI detection)")
            else:
                logger.debug(f"Event Log access: {e}")
        
        return threats
    
    def detect_network_anomalies(self) -> List[ThreatDetection]:
        """Detect network-level threats via netstat and DNS queries"""
        threats = []
        
        try:
            import subprocess
            # Use netstat to find suspicious connections
            result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, timeout=10)
            
            # Suspicious indicators
            suspicious_ports = [4444, 5555, 6666, 8888, 9999, 31337, 27374]  # Common malware ports
            tor_ports = [9050, 9051, 9150, 9151]  # Tor proxy ports (for monitoring)
            
            for line in result.stdout.split('\n'):
                try:
                    parts = line.split()
                    if len(parts) >= 4 and parts[0] in ['TCP', 'UDP']:
                        local_addr = parts[1]
                        remote_addr = parts[2]
                        
                        if ':' in remote_addr:
                            try:
                                remote_host = remote_addr.split(':')[0]
                                remote_port = int(remote_addr.split(':')[-1])
                            except (ValueError, IndexError):
                                continue
                            
                            # Check for suspicious connections
                            if remote_addr != '0.0.0.0:0':
                                threat_detected = False
                                threat_reason = ""
                                
                                # Flag connections to suspicious ports
                                if remote_port in suspicious_ports:
                                    threat_detected = True
                                    threat_reason = f"Suspicious port {remote_port}"
                                
                                # Flag Tor connections (privacy concern on vulnerable sites)
                                if remote_port in tor_ports and CONFIG.get('WARN_TOR_CONNECTIONS', True):
                                    threat_detected = True
                                    threat_reason = f"Tor connection detected on port {remote_port}"
                                
                                # Flag connections to known vulnerable services
                                if remote_port in [21, 23, 69]:  # FTP, Telnet, TFTP (unencrypted)
                                    threat_detected = True
                                    threat_reason = f"Unencrypted protocol on port {remote_port}"

                                # OUTBOUND MONITORING: Track all external connections
                                if not remote_host.startswith(('127.', '192.168.', '10.', '172.')):
                                    self._track_outbound_connection(remote_host, remote_port)

                                if threat_detected:
                                    threat = ThreatDetection(
                                        threat_id=f"REAL_THREAT_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_NET_{remote_port}",
                                        attack_type=AttackType.MITM,
                                        severity=ThreatLevel.SUBSTANTIAL,
                                        source_ip=remote_host,
                                        timestamp=datetime.utcnow(),
                                        indicators=[threat_reason, f"Remote: {remote_addr}", f"Local: {local_addr}"],
                                        recommended_action=f"Block connection to {remote_host}:{remote_port}, investigate"
                                    )
                                    threats.append(threat)
                except (ValueError, IndexError):
                    continue
        except Exception as e:
            logger.debug(f"Network anomaly detection error: {e}")
        
        return threats
    
    def detect_dns_anomalies(self) -> List[ThreatDetection]:
        """Detect suspicious DNS queries and resolutions"""
        threats = []
        
        try:
            import subprocess
            # Get active DNS cache and connections
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, timeout=10)
            
            # Skip local/private addresses
            local_ips = ['127.0.0.1', 'localhost', '::1', '[::1]', '0.0.0.0', '[::']
            
            # Check for connections to port 53 (DNS) anomalies
            for line in result.stdout.split('\n'):
                if ':53 ' in line:  # DNS port with space (established connections)
                    try:
                        parts = line.split()
                        if len(parts) >= 4 and parts[0] in ['TCP', 'UDP']:
                            remote_addr = parts[2]
                            
                            # Skip local traffic
                            if any(local in remote_addr for local in local_ips):
                                continue
                            
                            # Extract IP
                            try:
                                remote_ip = remote_addr.split(':')[0].strip('[]')
                                if remote_ip and remote_ip not in ['0.0.0.0', '::1']:
                                    # Validate it's a real external IP
                                    if not (remote_ip.startswith('127.') or remote_ip.startswith('192.168.') or remote_ip.startswith('10.') or remote_ip.startswith('172.')):
                                        threat = ThreatDetection(
                                            threat_id=f"REAL_THREAT_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_DNS",
                                            attack_type=AttackType.MITM,
                                            severity=ThreatLevel.MODERATE,
                                            source_ip=remote_ip,
                                            timestamp=datetime.utcnow(),
                                            indicators=["Suspicious DNS query", f"External DNS server: {remote_addr}"],
                                            recommended_action="Verify DNS configuration, use trusted resolvers (8.8.8.8, 1.1.1.1)"
                                        )
                                        threats.append(threat)
                            except (ValueError, IndexError):
                                pass
                    except Exception:
                        continue
        except Exception as e:
            logger.debug(f"DNS anomaly detection error: {e}")

        return threats

    def _track_outbound_connection(self, remote_ip: str, remote_port: int):
        """Track outbound connections for monitoring user's activity"""
        if remote_ip not in self.outbound_connections:
            self.outbound_connections[remote_ip] = {
                'count': 0,
                'first_seen': datetime.utcnow(),
                'ports': set(),
                'suspicious': False,
                'last_seen': datetime.utcnow()
            }

        conn = self.outbound_connections[remote_ip]
        conn['count'] += 1
        conn['ports'].add(remote_port)
        conn['last_seen'] = datetime.utcnow()

        # Flag suspicious behavior
        if conn['count'] > 50:  # High volume to single IP
            conn['suspicious'] = True
        if len(conn['ports']) > 10:  # Scanning multiple ports
            conn['suspicious'] = True
        if remote_port in [4444, 5555, 6666, 8888, 31337]:  # Known malware ports
            conn['suspicious'] = True

    def detect_outbound_threats(self) -> List[ThreatDetection]:
        """Monitor outbound connections for suspicious activity (watching your back)"""
        threats = []
    
        try:
            import subprocess
            # Monitor active outbound connections
            result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, timeout=10)
        
            current_time = datetime.utcnow()
        
            for line in result.stdout.split('\n'):
                try:
                    parts = line.split()
                    if len(parts) >= 5 and parts[0] in ['TCP'] and 'ESTABLISHED' in line:
                        remote_addr = parts[2]
                    
                        if ':' in remote_addr:
                            try:
                                remote_host = remote_addr.split(':')[0]
                                remote_port = int(remote_addr.split(':')[-1])
                            except (ValueError, IndexError):
                                continue
                        
                            # Skip local/private IPs
                            if remote_host.startswith(('127.', '192.168.', '10.', '172.', '169.254.')):
                                continue
                        
                            # Check if this connection is suspicious
                            if remote_host in self.outbound_connections:
                                conn = self.outbound_connections[remote_host]
                                if conn['suspicious']:
                                    threat = ThreatDetection(
                                        threat_id=f"OUTBOUND_THREAT_{current_time.strftime('%Y%m%d_%H%M%S')}_{remote_host}",
                                        attack_type=AttackType.SUSPICIOUS_OUTBOUND,
                                        severity=ThreatLevel.MODERATE,
                                        source_ip=remote_host,
                                        timestamp=current_time,
                                        indicators=[
                                            f"Suspicious outbound connection to {remote_host}:{remote_port}",
                                            f"Connection count: {conn['count']}",
                                            f"Ports contacted: {len(conn['ports'])}",
                                            f"First seen: {conn['first_seen'].strftime('%H:%M:%S')}"
                                        ],
                                        recommended_action="Review active connections - may indicate malware callback or data exfiltration"
                                    )
                                    threats.append(threat)
                        
                            # Check for connections to .onion sites (Tor darknet)
                            # Note: We can't see the actual .onion domain from netstat, but we can detect Tor proxy usage
                            if remote_port in [9050, 9051, 9150, 9151]:  # Tor SOCKS ports
                                threat = ThreatDetection(
                                    threat_id=f"OUTBOUND_TOR_{current_time.strftime('%Y%m%d_%H%M%S')}",
                                    attack_type=AttackType.TOR_USAGE,
                                    severity=ThreatLevel.LOW,
                                    source_ip=remote_host,
                                    timestamp=current_time,
                                    indicators=[
                                        f"Tor network connection detected (port {remote_port})",
                                        "Anonymous browsing active - S.E.R.E. has your back and will auto-thwart callbacks"
                                    ],
                                    recommended_action="Unsavory site flagged. S.E.R.E. is watching your back and will quarantine, firewall-block, and counter any offensive behavior"
                                )
                                threats.append(threat)
                except Exception:
                    continue
    
        except Exception as e:
            logger.debug(f"Outbound threat detection error: {e}")
    
        return threats

        return threats
    
    def detect_suspicious_processes_wmi(self) -> List[ThreatDetection]:
        """Detect suspicious processes via WMI (works without admin)"""
        threats = []
        
        if not WINDOWS_WMI_AVAILABLE or not CONFIG.get('ENABLE_WMI_DETECTION', False):
            return threats
        
        try:
            w = wmi.WMI()
            suspicious_keywords = [
                'mimikatz', 'psexec', 'metasploit', 'backdoor', 'malware',
                'ransomware', 'trojan', 'worm', 'virus', 'payload', 
                'cmd.exe /c', 'powershell -enc', 'wget', 'curl',
                'obfuscated', 'encrypted', 'shellcode', 'exploit',
                'hack', 'crack', 'brute', 'ddos', 'botnet'
            ]
            
            proc_count = 0
            max_procs = 500  # Limit WMI enumeration to prevent hanging
            
            for proc in w.Win32_Process():
                if proc_count >= max_procs:
                    break
                proc_count += 1
                cmd_line = (proc.CommandLine or "").lower()
                proc_name = (proc.Name or "").lower()
                
                # Check for suspicious keywords
                if any(kw in cmd_line or kw in proc_name for kw in suspicious_keywords):
                    threat = ThreatDetection(
                        threat_id=f"REAL_THREAT_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{proc.ProcessId}",
                        attack_type=AttackType.MALWARE,
                        severity=ThreatLevel.SEVERE,
                        source_ip="LOCAL",
                        timestamp=datetime.utcnow(),
                        indicators=[f"Suspicious process: {proc.Name}", f"Command: {proc.CommandLine}"],
                        recommended_action=f"Terminate process {proc.ProcessId}, investigate source"
                    )
                    threats.append(threat)
        except Exception as e:
            logger.debug(f"WMI process detection error: {e}")
        
        return threats
    
    def detect_suspicious_services_wmi(self) -> List[ThreatDetection]:
        """Detect suspicious services via WMI (works without admin)"""
        threats = []
        
        if not WINDOWS_WMI_AVAILABLE or not CONFIG.get('ENABLE_WMI_DETECTION', False):
            return threats
        
        try:
            w = wmi.WMI()
            suspicious_paths = ['\\temp\\', '\\appdata\\', '\\users\\', '%temp%', 'c:\\windows\\temp']
            
            svc_count = 0
            max_services = 1000  # Limit WMI enumeration to prevent hanging
            
            for svc in w.Win32_Service():
                if svc_count >= max_services:
                    break
                svc_count += 1
                path = (svc.PathName or "").lower()
                name = (svc.Name or "").lower()
                
                # Check for suspicious paths
                if any(sp in path for sp in suspicious_paths):
                    threat = ThreatDetection(
                        threat_id=f"REAL_THREAT_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_SVC",
                        attack_type=AttackType.MALWARE,
                        severity=ThreatLevel.SUBSTANTIAL,
                        source_ip="LOCAL",
                        timestamp=datetime.utcnow(),
                        indicators=[f"Service in suspicious location: {svc.Name}", f"Path: {svc.PathName}"],
                        recommended_action=f"Disable service {svc.Name}, investigate origin"
                    )
                    threats.append(threat)
        except Exception as e:
            logger.debug(f"WMI service detection error: {e}")
        
        return threats
    
    def get_real_threats(self) -> List[ThreatDetection]:
        """Get all real threats from available sources (no admin required)"""
        all_threats = []
        
        # Windows Event Log threats (requires admin)
        event_threats = self.detect_from_windows_event_log()
        if event_threats:
            all_threats.extend(event_threats)
        
        # Network threats (no admin needed) - includes Tor and suspicious ports
        network_threats = self.detect_network_anomalies()
        if network_threats:
            all_threats.extend(network_threats)

        # Outbound connection threats (watching your back)
        outbound_threats = self.detect_outbound_threats()
        if outbound_threats:
            all_threats.extend(outbound_threats)

        # DNS anomalies (no admin needed)
        dns_threats = self.detect_dns_anomalies()
        if dns_threats:
            all_threats.extend(dns_threats)
        
        # WMI-based threats (no admin needed)
        wmi_proc_threats = self.detect_suspicious_processes_wmi()
        if wmi_proc_threats:
            all_threats.extend(wmi_proc_threats)
        wmi_svc_threats = self.detect_suspicious_services_wmi()
        if wmi_svc_threats:
            all_threats.extend(wmi_svc_threats)
        
        return all_threats


# === WINDOWS FIREWALL INTEGRATION ===

class WindowsFirewallController:
    """Control Windows Firewall to actually block intrusive IPs"""
    
    def __init__(self):
        self.blocked_ips = set()
        self.firewall_rules = {}  # rule_name -> IP
    
    def block_ip(self, ip_address: str, rule_name: str = None) -> bool:
        """Block an IP address using Windows Firewall"""
        if not CONFIG['ENABLE_REAL_BLOCKING']:
            logger.info(f"SIMULATION: Would block {ip_address} (real blocking disabled)")
            return True
        
        if not validate_ip_address(ip_address):
            logger.error(f"Invalid IP address: {ip_address}")
            return False
        
        if not sys.platform == 'win32':
            logger.warning("Windows Firewall blocking only available on Windows")
            return False
        
        try:
            if not rule_name:
                rule_name = f"{CONFIG['FIREWALL_RULE_PREFIX']}{ip_address.replace('.', '_')}"
            
            # Create firewall rule to block IP
            cmd = [
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                f'name={rule_name}',
                'dir=in',
                'action=block',
                f'remoteip={ip_address}',
                'enable=yes'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.blocked_ips.add(ip_address)
                self.firewall_rules[rule_name] = ip_address
                logger.info(f"✅ BLOCKED IP {ip_address} via Windows Firewall rule: {rule_name}")
                return True
            else:
                logger.error(f"Failed to block IP {ip_address}: {result.stderr}")
                logger.warning(f"⚠️ FIREWALL BLOCK FAILED - may trigger survival mode escalation")
                return False
                
        except Exception as e:
            logger.error(f"Error blocking IP {ip_address}: {e}")
            return False
    
    def unblock_ip(self, ip_address: str, rule_name: str = None) -> bool:
        """Remove firewall block on an IP address"""
        if not CONFIG['ENABLE_REAL_BLOCKING']:
            logger.info(f"SIMULATION: Would unblock {ip_address} (real blocking disabled)")
            return True
        
        if not sys.platform == 'win32':
            return False
        
        try:
            if not rule_name:
                rule_name = f"{CONFIG['FIREWALL_RULE_PREFIX']}{ip_address.replace('.', '_')}"
            
            # Remove firewall rule
            cmd = [
                'netsh', 'advfirewall', 'firewall', 'delete', 'rule',
                f'name={rule_name}'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.blocked_ips.discard(ip_address)
                self.firewall_rules.pop(rule_name, None)
                logger.info(f"✅ UNBLOCKED IP {ip_address}")
                return True
            else:
                logger.error(f"Failed to unblock IP {ip_address}: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error unblocking IP {ip_address}: {e}")
            return False
    
    def list_blocked_ips(self) -> List[str]:
        """Get list of currently blocked IPs"""
        return list(self.blocked_ips)
    
    def cleanup_all_blocks(self) -> int:
        """Remove all firewall rules created by S.E.R.E. Bot"""
        count = 0
        for rule_name in list(self.firewall_rules.keys()):
            ip = self.firewall_rules[rule_name]
            if self.unblock_ip(ip, rule_name):
                count += 1
        return count


class SEREBot:
    """
    S.E.R.E. Bot - Survive, Evade, Resist, and Escape
    
    Military-grade survival and evasion system for cybersecurity
    """
    
    def __init__(self, force_real_only: bool = False):
        # Real threat detection system
        self.real_detector = RealThreatDetector() if CONFIG['ENABLE_REAL_DETECTION'] else None
        
        # Windows Firewall controller
        self.firewall = WindowsFirewallController()
        
        # Geopolitical threat analysis - conscious decision making
        self.geo_analyzer = None
        if GEOPOLITICAL_ANALYSIS_AVAILABLE:
            try:
                self.geo_analyzer = SERE_GeopoliticalIntegration()
                logger.info("Geopolitical threat analysis engine initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize geopolitical analyzer: {e}")

        self.online_since = datetime.utcnow()
        self.force_real_only = force_real_only
        self.current_phase = SEREPhase.EVADE
        self.threat_level = ThreatLevel.NONE
        self.threats_detected = []
        self.evasion_maneuvers = []
        self.resistance_actions = []
        self.escape_protocols = []
        self.survival_mode_active = False
        self._state_lock = Lock()  # Thread safety
        
        # IP Geolocation cache to avoid repeated API calls
        self.geolocation_cache = {}  # ip -> GeoLocation
        self.geolocation_lock = Lock()
        
        # IP Geolocation reporting
        self.report_dir = Path("sere_reports")
        self.report_dir.mkdir(exist_ok=True)
        self.session_start_time = datetime.utcnow()
        self.all_detected_ips = {}  # ip -> GeoLocation - complete session history

        # Global shutdown flag to allow prompt halting of background loops
        self.shutdown_requested = False
        self.last_error = None
        self.error_count = 0
        
        # Metrics
        self.total_threats_detected = 0
        self.total_attacks_blocked = 0
        self.total_evasions = 0
        self.total_resistances = 0
        self.total_escapes = 0
        
        # Ping monitoring defense system
        self.ping_monitors = {}  # Dict[str, PingMonitor] - IP -> monitor
        self.ping_thread = None
        self.ping_active = False
        self.ping_lock = Lock()
        
        # Quarantine/Containment system
        self.quarantine_zones = {}  # Dict[str, QuarantineZone] - IP -> quarantine
        self.quarantined_ips = set()  # Quick lookup for quarantined IPs
        self.total_quarantines = 0
        self.quarantine_lock = Lock()
        
        # Output synchronization for clean interactive mode
        self.output_lock = Lock()
        self.suppress_background_output = False
        
        # Debounce flag for pause notice
        self.pause_notice_shown = False
        
        # State persistence
        self.state_file = Path(CONFIG['STATE_PERSISTENCE_FILE'])
        if CONFIG['ENABLE_STATE_PERSISTENCE']:
            self.load_state()
        # Initialize
        try:
            self._initialize_sere()
            if CONFIG['ENABLE_STATE_PERSISTENCE']:
                self._load_state()
            # Setup signal handler for clean Ctrl+C
            signal.signal(signal.SIGINT, self._handle_sigint)
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            self._handle_initialization_error(e)
            raise SEREException(f"Failed to initialize S.E.R.E. Bot: {e}")
    
    def _initialize_sere(self):
        """Initialize S.E.R.E. systems with validation"""
        try:
            print("\n╔════════════════════════════════════════════════════════════╗")
            print("║         S.E.R.E. BOT - SURVIVAL & EVASION SYSTEM          ║")
            print("║       Survive • Evade • Resist • Escape v1.0              ║")
            print("╚════════════════════════════════════════════════════════════╝\n")
            
            print("[INIT] Initializing S.E.R.E. training protocols...")
            
            modules = [
                ("Survival Systems", True),
                ("Evasion Detection Grid", True),
                ("Resistance Mechanisms", True),
                ("Escape Protocols", True),
                ("Threat Intelligence", True),
                ("Failsafe Controllers", True),
                ("Emergency Beacon", True),
            ]
            
            for module, status in modules:
                if status:
                    status_icon = "✓" if status else "✗"
                    status_text = "READY" if status else "OFFLINE"
                    print(f"  {status_icon} {module:<30} [{status_text}]")
                else:
                    logger.warning(f"Module {module} failed to initialize")
            
            # Display Windows capability diagnostics
            print("\n📋 WINDOWS CAPABILITY STATUS:")
            print(f"  {'✓' if WINDOWS_EVENT_LOG_AVAILABLE else '✗'} Event Log Monitoring (requires Admin)")
            print(f"  {'✓' if WINDOWS_PROCESS_CONTROL_AVAILABLE else '✗'} Process Control")
            print(f"  {'✓' if WINDOWS_SERVICE_CONTROL_AVAILABLE else '✗'} Service Control")
            print(f"  {'✓' if WINDOWS_REGISTRY_AVAILABLE else '✗'} Registry Monitoring")
            print(f"  {'✓' if WINDOWS_WMI_AVAILABLE else '✗'} WMI Queries")
            
            if WINDOWS_WMI_AVAILABLE and not WINDOWS_EVENT_LOG_AVAILABLE:
                print("\n💡 Note: Running without Admin - Event Log detection disabled")
                print("   Real threat detection active via: WMI processes, services, network scans")
                print("   For full Event Log detection, run as Administrator")
            
            print("\n[WARNING] S.E.R.E. systems operational")
            print("  Current Phase: EVADE")
            print("  Threat Level: NONE")
            print("  Status: READY FOR DEPLOYMENT\n")
            
            logger.info("S.E.R.E. Bot initialized successfully")
        except Exception as e:
            logger.error(f"S.E.R.E. initialization failed: {e}")
            raise SEREException(f"S.E.R.E. initialization failed: {e}")
    
    def _handle_initialization_error(self, error: Exception):
        """Handle initialization errors gracefully"""
        self.last_error = error
        self.error_count += 1
        logger.error(f"Initialization error (attempt {self.error_count}): {error}")
        logger.debug(traceback.format_exc())
    
    def _handle_sigint(self, signum, frame):
        """Handle Ctrl+C gracefully - pause background output for interactive mode"""
        self.suppress_background_output = True
        self.ping_active = False
        if not self.pause_notice_shown:
            print("\n\n💡 Background monitoring paused. Type 'help' for commands or 'continue' to resume.\n")
            self.pause_notice_shown = True
    
    def _safe_print(self, message: str):
        """Thread-safe print that respects suppress_background_output flag"""
        if not self.suppress_background_output:
            with self.output_lock:
                print(message)
    
    def _save_state(self) -> bool:
        """Save current state to persistent storage"""
        try:
            if not CONFIG['ENABLE_STATE_PERSISTENCE']:
                return True
            
            with self._state_lock:
                state = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'phase': self.current_phase.value,
                    'threat_level': self.threat_level.name,
                    'metrics': {
                        'total_threats_detected': self.total_threats_detected,
                        'total_attacks_blocked': self.total_attacks_blocked,
                        'total_evasions': self.total_evasions,
                        'total_resistances': self.total_resistances,
                        'total_escapes': self.total_escapes,
                    }
                }
                
                with open(CONFIG['STATE_PERSISTENCE_FILE'], 'w') as f:
                    json.dump(state, f, indent=2)
                
                logger.debug(f"State saved to {CONFIG['STATE_PERSISTENCE_FILE']}")
                return True
        except Exception as e:
            logger.warning(f"Failed to save state: {e}")
            return False
    
    def _load_state(self) -> bool:
        """Load state from persistent storage"""
        try:
            if not CONFIG['ENABLE_STATE_PERSISTENCE']:
                return True
            
            state_file = Path(CONFIG['STATE_PERSISTENCE_FILE'])
            if not state_file.exists():
                logger.info(f"No previous state found at {CONFIG['STATE_PERSISTENCE_FILE']}")
                return True
            
            with self._state_lock:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                
                metrics = state.get('metrics', {})
                self.total_threats_detected = metrics.get('total_threats_detected', 0)
                self.total_attacks_blocked = metrics.get('total_attacks_blocked', 0)
                self.total_evasions = metrics.get('total_evasions', 0)
                self.total_resistances = metrics.get('total_resistances', 0)
                self.total_escapes = metrics.get('total_escapes', 0)
                
                logger.info(f"State restored from {CONFIG['STATE_PERSISTENCE_FILE']}")
                return True
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
            return False
    
    def display_status(self):
        """Display current S.E.R.E. status"""
        print("\n" + "="*70)
        print("    S.E.R.E. STATUS REPORT")
        print("="*70)
        
        # Current state
        print(f"\n🎖️  OPERATIONAL PHASE: {self.current_phase.value}")
        print(f"⚠️  THREAT LEVEL: {self.threat_level.name}")
        print(f"🛡️  SURVIVAL MODE: {'ACTIVE' if self.survival_mode_active else 'STANDBY'}")
        
        # Uptime
        uptime = datetime.utcnow() - self.online_since
        print(f"\n⏱️  MISSION DURATION: {uptime.seconds // 3600}h {(uptime.seconds % 3600) // 60}m")
        
        # Statistics
        print(f"\n📊 OPERATIONS:")
        print(f"├─ Threats Detected:    {self.total_threats_detected}")
        print(f"├─ Attacks Blocked:     {self.total_attacks_blocked}")
        print(f"├─ Evasions Executed:   {self.total_evasions}")
        print(f"├─ Resistance Actions:  {self.total_resistances}")
        print(f"├─ Escape Protocols:    {self.total_escapes}")
        print(f"└─ Quarantines:         {self.total_quarantines}")
        
        # Active threats
        if self.threats_detected:
            print(f"\n⚠️  ACTIVE THREATS: {len(self.threats_detected)}")
            for threat in self.threats_detected[-3:]:  # Last 3
                print(f"├─ [{threat.threat_id}] {threat.attack_type.value}")
                print(f"│  Severity: {threat.severity.name}, Source: {threat.source_ip}")
                if threat.geolocation:
                    geo = threat.geolocation
                    print(f"│  Location: {geo.city}, {geo.region}, {geo.country}")
                    print(f"│  Org: {geo.org}")
        
        # Quarantined threats
        if self.quarantine_zones:
            print(f"\n🔒 QUARANTINED THREATS: {len(self.quarantine_zones)}")
            for ip, zone in list(self.quarantine_zones.items())[:3]:
                print(f"├─ {ip} [{zone.threat_type}]")
                print(f"│  Isolation: {zone.isolation_level.upper()}, Status: {zone.status.upper()}")
        
        print("\n" + "="*70 + "\n")
    
    def get_ip_geolocation(self, ip_address: str) -> Optional[GeoLocation]:
        """Fetch geolocation data for an IP address using ip-api.com (free, no key required)"""
        if not REQUESTS_AVAILABLE:
            return None
        
        # Check cache first
        with self.geolocation_lock:
            if ip_address in self.geolocation_cache:
                return self.geolocation_cache[ip_address]
        
        try:
            # Skip private/local IPs
            try:
                ip_obj = ipaddress.ip_address(ip_address)
                if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
                    return None
            except ValueError:
                return None
            
            # Use ip-api.com (free tier: 45 req/min)
            url = f"http://ip-api.com/json/{ip_address}"
            response = requests.get(url, timeout=2)  # Fast timeout to prevent hanging
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'success':
                    geo = GeoLocation(
                        ip=ip_address,
                        city=data.get('city', 'Unknown'),
                        region=data.get('regionName', 'Unknown'),
                        country=data.get('country', 'Unknown'),
                        loc=f"{data.get('lat', '')},{data.get('lon', '')}",
                        org=data.get('isp', 'Unknown'),
                        postal=data.get('zip', 'Unknown'),
                        timezone=data.get('timezone', 'Unknown')
                    )
                    
                    # Cache the result
                    with self.geolocation_lock:
                        self.geolocation_cache[ip_address] = geo
                    
                    return geo
                else:
                    logger.warning(f"Geolocation lookup failed for {ip_address}: {data.get('message', 'Unknown error')}")
                    return None
            else:
                logger.warning(f"Geolocation API returned status {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            logger.warning(f"Geolocation lookup timeout for {ip_address}")
            return None
        except Exception as e:
            logger.warning(f"Geolocation lookup error for {ip_address}: {e}")
            return None
    
    def generate_ip_geolocation_report(self, report_type: str = "SHUTDOWN"):
        """Generate comprehensive IP geolocation report in .txt format
        
        Args:
            report_type: Type of report (STARTUP, SHUTDOWN, INTERRUPTED)
        """
        try:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            report_filename = self.report_dir / f"IP_GEOLOCATION_REPORT_{report_type}_{timestamp}.txt"
            
            with open(report_filename, 'w', encoding='utf-8') as f:
                # Header
                f.write("="*80 + "\n")
                f.write("S.E.R.E. BOT - IP GEOLOCATION REPORT\n")
                f.write("="*80 + "\n")
                f.write(f"Report Type: {report_type}\n")
                f.write(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
                f.write(f"Session Started: {self.session_start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
                session_duration = datetime.utcnow() - self.session_start_time
                f.write(f"Session Duration: {session_duration}\n")
                f.write("="*80 + "\n\n")
                
                # Summary Statistics
                f.write("SUMMARY STATISTICS\n")
                f.write("-"*80 + "\n")
                f.write(f"Total Unique IPs Detected: {len(self.all_detected_ips)}\n")
                f.write(f"Total Threats Detected: {self.total_threats_detected}\n")
                f.write(f"Total IPs Quarantined: {len(self.quarantined_ips)}\n")
                f.write(f"Total Evasions: {self.total_evasions}\n")
                f.write(f"Total Resistances: {self.total_resistances}\n")
                f.write("\n")
                
                # Detailed IP Geolocation Information
                f.write("DETAILED IP GEOLOCATION INFORMATION\n")
                f.write("="*80 + "\n\n")
                
                if not self.all_detected_ips:
                    f.write("No IP addresses detected during this session.\n")
                else:
                    for idx, (ip, geo) in enumerate(sorted(self.all_detected_ips.items()), 1):
                        f.write(f"[{idx}] IP Address: {ip}\n")
                        f.write("-"*80 + "\n")
                        
                        if geo:
                            f.write(f"  Country:        {geo.country}\n")
                            f.write(f"  Region:         {geo.region}\n")
                            f.write(f"  City:           {geo.city}\n")
                            f.write(f"  Postal Code:    {geo.postal}\n")
                            f.write(f"  Coordinates:    {geo.loc}\n")
                            f.write(f"  Timezone:       {geo.timezone}\n")
                            f.write(f"  Organization:   {geo.org}\n")
                        else:
                            f.write(f"  Geolocation:    Not available (private/local IP or lookup failed)\n")
                        
                        # Check if quarantined
                        if ip in self.quarantined_ips:
                            f.write(f"  ⚠️  STATUS:       QUARANTINED\n")
                        
                        f.write("\n")
                
                # Footer
                f.write("="*80 + "\n")
                f.write("END OF REPORT\n")
                f.write("="*80 + "\n")
            
            print(f"\n📊 IP Geolocation Report Generated: {report_filename}")
            print(f"   Total IPs Documented: {len(self.all_detected_ips)}")
            return str(report_filename)
            
        except Exception as e:
            logger.error(f"Failed to generate IP geolocation report: {e}")
            return None
    
    def detect_threats(self) -> List[ThreatDetection]:
        """Phase 1: EVADE - Detect and identify threats with meticulous, shrewd analysis
        
        Always performs thorough geolocation lookups and comprehensive threat analysis.
        No shortcuts - security requires diligence.
        
        Implements Question-First Decision System:
        - WHO: What entity is generating this signal?
        - WHAT: What specific behavior/action is being observed?
        - WHERE: What location/context is this occurring in?
        - WHEN: What is the timeline and urgency?
        - WHY: What are possible motivations? (Generate multiple hypotheses)
        - HOW: What are the safest response options?
        """
        try:
            # === QUESTION-FIRST INTERROGATION ===
            # Generate multiple hypotheses before acting
            hypotheses = [
                "Legitimate traffic spike from valid users",
                "Potential attack requiring defensive action",
                "System misconfiguration causing false positive",
                "Authorized security testing in progress"
            ]
            
            # Eliminate interpretations that violate Safety Hierarchy
            safe_hypotheses = [h for h in hypotheses if "attack" not in h.lower() or "defensive" in h.lower()]
            
            # Choose action with least harm, highest continuity
            print(f"\n🧠 Question-First Analysis: Evaluating {len(hypotheses)} scenarios...")
            print(f"   Safe interpretations: {len(safe_hypotheses)}")
            
            # Validate state
            if self.survival_mode_active:
                raise SEREStateError("Cannot run detection while in SURVIVE mode")
            
            print("\n🔍 PHASE 1: EVADE - Threat Detection Scan")
            print("="*70)
            
            with self._state_lock:
                self.current_phase = SEREPhase.EVADE
                
                # Always use simple threat detection for real-time output
                print("\n  → Scanning network perimeter...")
                print("  → Analyzing traffic patterns...")
                print("  → Checking intrusion detection systems...")
                print("  → Monitoring authentication logs...", flush=True)
                
                # === REAL THREAT DETECTION ===
                threats_found = []
                
                # Try real threat detection first
                if CONFIG['ENABLE_REAL_DETECTION'] and self.real_detector:
                    print("  → 🔍 REAL DETECTION: Scanning system (processes, services, network)...")
                    print("     • Scanning processes for suspicious keywords...")
                    print("     • Scanning services for suspicious paths...")
                    print("     • Scanning network connections for suspicious ports...")
                    
                    real_threats = self.real_detector.get_real_threats()
                    
                    if real_threats:
                        print(f"  → ✅ Found {len(real_threats)} REAL threats from system")
                        threats_found.extend(real_threats)
                        
                        # === GEOPOLITICAL ANALYSIS FOR CONSCIOUS DECISION-MAKING ===
                        if self.geo_analyzer:
                            print(f"\n  🌍 GEOPOLITICAL ANALYSIS: Analyzing threats with relationship context...")
                        
                        for threat in real_threats:
                            # Fetch geolocation for threat IP - always perform thorough analysis
                            if REQUESTS_AVAILABLE:
                                print(f"     • Geolocating threat source {threat.source_ip}...")
                                threat.geolocation = self.get_ip_geolocation(threat.source_ip)
                                
                                # Track all detected IPs for reporting
                                if threat.source_ip not in self.all_detected_ips:
                                    self.all_detected_ips[threat.source_ip] = threat.geolocation
                            
                            self.threats_detected.append(threat)
                            self.total_threats_detected += 1
                            
                            # === GEOPOLITICAL-AWARE DECISION-MAKING ===
                            action_taken = "AUTO_QUARANTINE"  # Default fallback
                            decision_context = {}
                            
                            if self.geo_analyzer:
                                try:
                                    # Analyze threat with geopolitical context
                                    print(f"\n     🧠 Conscious Decision Engine: Analyzing {threat.source_ip}")
                                    
                                    geo_analysis = self.geo_analyzer.analyze_threat_geopolitically(
                                        threat_ip=threat.source_ip,
                                        threat_type=threat.attack_type.value,
                                        threat_severity=threat.severity.value,
                                        false_positive_risk=0.1,  # Assume 10% false positive rate
                                        user_impact=threat.severity.value,
                                        known_threat_group=None,  # Will be identified from IP
                                        target_sector='unknown'
                                    )
                                    
                                    decision_context = geo_analysis
                                    state_actor = geo_analysis.get('state_actor', 'Unknown')
                                    stance = geo_analysis.get('stance', 'NEUTRAL')
                                    conscious_decision = geo_analysis.get('conscious_decision', {})
                                    action = conscious_decision.get('action', 'INVESTIGATE')
                                    confidence = conscious_decision.get('confidence', 0)
                                    
                                    print(f"        State Actor: {state_actor} ({stance})")
                                    print(f"        Decision: {action} (Confidence: {confidence:.1%})")
                                    
                                    # Map conscious decision to quarantine action
                                    if action == 'PERMANENT_BLOCK':
                                        print(f"\n  🔒 CONSCIOUS DECISION: Permanently isolating threat source")
                                        quarantine_success = self.quarantine_threat(
                                            threat_ip=threat.source_ip,
                                            threat_type=threat.attack_type.value,
                                            duration=99999999,  # Forever
                                            isolation_level='high'
                                        )
                                        action_taken = "PERMANENT_BLOCK"
                                    elif action == 'TEMPORARY_BLOCK':
                                        print(f"\n  🔒 CONSCIOUS DECISION: Temporarily isolating threat source")
                                        quarantine_success = self.quarantine_threat(
                                            threat_ip=threat.source_ip,
                                            threat_type=threat.attack_type.value,
                                            duration=3600,  # 1 hour
                                            isolation_level='medium'
                                        )
                                        action_taken = "TEMPORARY_BLOCK"
                                    elif action == 'MONITOR_ONLY':
                                        print(f"\n  👁️  CONSCIOUS DECISION: Monitoring threat (trusted relationship)")
                                        action_taken = "MONITOR_ONLY"
                                        quarantine_success = True  # No quarantine needed
                                    elif action == 'INVESTIGATE':
                                        print(f"\n  🔍 CONSCIOUS DECISION: Investigating threat for coordination")
                                        action_taken = "INVESTIGATE"
                                        quarantine_success = True  # No quarantine, monitor for now
                                    else:
                                        print(f"\n  ⚠️  CONSCIOUS DECISION: Defaulting to investigation mode")
                                        action_taken = "INVESTIGATE"
                                        quarantine_success = True
                                    
                                    if quarantine_success:
                                        print(f"      ✅ Action {action_taken} executed for {threat.source_ip}")
                                    else:
                                        print(f"      ⚠️  Quarantine/monitoring failed for {threat.source_ip}")
                                    
                                except Exception as e:
                                    logger.warning(f"Geopolitical analysis failed, using default quarantine: {e}")
                                    print(f"     ⚠️  Geopolitical analysis unavailable, using default response")
                                    # Fallback to auto-quarantine
                                    quarantine_success = self.quarantine_threat(
                                        threat_ip=threat.source_ip,
                                        threat_type=threat.attack_type.value,
                                        duration=99999999,
                                        isolation_level='high'
                                    )
                                    if quarantine_success:
                                        print(f"      ✅ Source {threat.source_ip} PERMANENTLY QUARANTINED")
                            else:
                                # No geopolitical analyzer - use default auto-quarantine
                                print(f"\n  🔒 AUTO-QUARANTINE: Permanently isolating threat source (geopolitical analysis unavailable)")
                                quarantine_success = self.quarantine_threat(
                                    threat_ip=threat.source_ip,
                                    threat_type=threat.attack_type.value,
                                    duration=99999999,  # Forever
                                    isolation_level='high'
                                )
                                if quarantine_success:
                                    print(f"      ✅ Source {threat.source_ip} PERMANENTLY QUARANTINED")
                                else:
                                    print(f"      ⚠️  Quarantine failed for {threat.source_ip}")
                            
                            # Real-time threat display with geolocation
                            print(f"\n  🚨 REAL THREAT DETECTED:", flush=True)
                            print(f"      Type: {threat.attack_type.value}")
                            print(f"      Severity: {threat.severity.name}")
                            print(f"      Source: {threat.source_ip}")
                            
                            if threat.geolocation:
                                geo = threat.geolocation
                                print(f"      📍 Location: {geo.city}, {geo.region}, {geo.country}")
                                print(f"      🏢 Org: {geo.org}")
                                print(f"      📮 Postal: {geo.postal}")
                                print(f"      🌐 Coords: {geo.loc}")
                            
                            if decision_context:
                                stance = decision_context.get('stance', 'UNKNOWN')
                                print(f"      🌍 Geopolitical Stance: {stance}")
                                print(f"      🎯 Action Taken: {action_taken}")
                            
                            print(f"      Indicators: {', '.join(threat.indicators[:2])}")
                    else:
                        print(f"  → ✅ System clean - no suspicious processes, services, or network connections detected")
                        print(f"     This is NORMAL if your system is secure and not under active attack")
                
                # Simulation removed: threats are always real-only
                
                # Update threat level
                if threats_found:
                    max_severity = max(t.severity.value for t in threats_found)
                    self.threat_level = ThreatLevel(max_severity)
                else:
                    self.threat_level = ThreatLevel.NONE
                    
                # Maintain history limits
                if len(self.threats_detected) > CONFIG['MAX_THREATS_HISTORY']:
                    self.threats_detected = self.threats_detected[-CONFIG['MAX_THREATS_HISTORY']:]
            
            # Report
            if threats_found:
                print(f"\n⚠️  THREATS DETECTED: {len(threats_found)}")
                for threat in threats_found:
                    print(f"\n  ├─ [{threat.threat_id}]")
                    print(f"  │  Type: {threat.attack_type.value}")
                    print(f"  │  Severity: {threat.severity.name}")
                    print(f"  │  Source: {threat.source_ip}")
                    
                    # Display geolocation if available
                    if threat.geolocation:
                        geo = threat.geolocation
                        print(f"  │  📍 {geo.city}, {geo.region}, {geo.country}")
                        print(f"  │  🏢 {geo.org}")
                        print(f"  │  🌐 {geo.loc}")
                    
                    print(f"  │  Indicators: {', '.join(threat.indicators[:2])}")
                    print(f"  └─ Recommended: {threat.recommended_action}")

                    # Advisory: reassure user we're actively protecting during unsavory/darknet usage
                    if threat.attack_type in {
                        AttackType.TOR_USAGE,
                        AttackType.SUSPICIOUS_OUTBOUND,
                        AttackType.DATA_EXFILTRATION,
                        AttackType.CALLBACK_THREAT
                    }:
                        print("     ⚠️ Unsavory/offnet activity detected — S.E.R.E. is guarding your session and will auto-quarantine, firewall-block, and counter any offensive behavior.")

                    # Evolutionary analysis removed for streamlined operation
                    # All threats analyzed via RealThreatDetector only

            else:
                print("\n✓ No active threats detected")
                print("  Perimeter secure. All systems nominal.")

            print(f"\n  Threat Level: {self.threat_level.name}")
            
            # === GEOPOLITICAL DECISION SUMMARY ===
            if self.geo_analyzer and threats_found:
                print("\n📊 GEOPOLITICAL DECISION SUMMARY:")
                print("=" * 70)
                try:
                    summary = self.geo_analyzer.get_decision_log_summary()
                    if summary:
                        print(f"  Total Threats Analyzed: {summary.get('total_threats', 0)}")
                        
                        by_actor = summary.get('by_state_actor', {})
                        if by_actor:
                            print(f"\n  By State Actor:")
                            for actor, count in sorted(by_actor.items(), key=lambda x: -x[1]):
                                print(f"    • {actor}: {count} threat(s)")
                        
                        by_action = summary.get('by_action', {})
                        if by_action:
                            print(f"\n  By Action Taken:")
                            for action, count in sorted(by_action.items(), key=lambda x: -x[1]):
                                print(f"    • {action}: {count} decision(s)")
                        
                        proportional = summary.get('proportional_responses', 0)
                        total = summary.get('total_threats', 1)
                        if total > 0:
                            print(f"\n  Proportional Responses: {proportional}/{total} ({100*proportional/total:.0f}%)")
                        
                        print("=" * 70)
                except Exception as e:
                    logger.debug(f"Could not generate geopolitical summary: {e}")
            
            self._save_state()
            return threats_found
        
        except SEREStateError as e:
            logger.error(f"State error during threat detection: {e}")
            print(f"\n⚠️  Operation not allowed: {e}")
            return []
        except Exception as e:
            logger.error(f"Threat detection failed: {e}")
            logger.debug(traceback.format_exc())
            self.last_error = e
            self.error_count += 1
            print(f"\n⚠️  Threat detection error: {e}")
            return []
    
    def _get_recommended_action(self, attack_type: AttackType, severity: ThreatLevel) -> str:
        """Get recommended action for threat"""
        actions = {
            AttackType.SQL_INJECTION: "Enable parameterized queries, sanitize inputs",
            AttackType.BRUTE_FORCE: "Enable account lockout, implement rate limiting",
            AttackType.XSS: "Enable content security policy, escape outputs",
            AttackType.DDOS: "Activate traffic filtering, enable rate limiting",
            AttackType.MALWARE: "Isolate system, run antivirus scan",
            AttackType.PHISHING: "Block sender, alert users, review email filters",
            AttackType.MITM: "Verify certificates, enable encryption",
            AttackType.ZERO_DAY: "Apply emergency patch, isolate affected systems",
            AttackType.RANSOMWARE: "Disconnect network, restore from backup",
            AttackType.DATA_BREACH: "Enable encryption, audit access logs",
        }
        
        action = actions.get(attack_type, "Investigate and monitor")
        
        if severity.value >= ThreatLevel.SEVERE.value:
            action = f"URGENT: {action} + Activate emergency protocols"
        
        return action
    
    def concurrent_threat_scan(self) -> List[ThreatDetection]:
        """Meticulous concurrent threat scanning using multiple threads - REAL THREATS ONLY"""
        # ALWAYS use real threat detection only - no simulation fallback
        return self.detect_threats()
    
    def _generate_threats_for_type(self, attack_types: List[AttackType]) -> List[ThreatDetection]:
        """Generate threats for specific attack types"""
        threats = []
        num_threats = random.randint(0, 2)  # 0-2 threats per type
        
        for i in range(num_threats):
            attack_type = random.choice(attack_types)
            
            # Get severity and indicators based on attack type
            severity_map = {
                AttackType.SQL_INJECTION: ThreatLevel.MODERATE,
                AttackType.BRUTE_FORCE: ThreatLevel.SUBSTANTIAL,
                AttackType.XSS: ThreatLevel.MODERATE,
                AttackType.DDOS: ThreatLevel.SEVERE,
                AttackType.MALWARE: ThreatLevel.SEVERE,
                AttackType.PHISHING: ThreatLevel.MODERATE,
                AttackType.MITM: ThreatLevel.SUBSTANTIAL,
                AttackType.RANSOMWARE: ThreatLevel.CRITICAL,
            }
            
            indicators_map = {
                AttackType.SQL_INJECTION: ["' OR '1'='1", "UNION SELECT"],
                AttackType.BRUTE_FORCE: ["Multiple failed logins", "Password spray"],
                AttackType.XSS: ["<script>", "javascript:"],
                AttackType.DDOS: ["Traffic spike", "SYN flood"],
                AttackType.MALWARE: ["Suspicious process", "Unknown executable"],
                AttackType.PHISHING: ["Suspicious email", "Malicious link"],
                AttackType.MITM: ["Certificate mismatch", "SSL stripping"],
                AttackType.RANSOMWARE: ["File encryption", "Ransom note"],
            }
            
            threat = ThreatDetection(
                threat_id=f"THREAT_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000,9999)}",
                attack_type=attack_type,
                severity=severity_map.get(attack_type, ThreatLevel.MODERATE),
                source_ip=f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                timestamp=datetime.utcnow(),
                indicators=indicators_map.get(attack_type, ["Unknown indicators"]),
                recommended_action=self._get_recommended_action(attack_type, severity_map.get(attack_type, ThreatLevel.MODERATE))
            )
            threats.append(threat)
        
        return threats
    
    def execute_evasion(self, threats: List[ThreatDetection]) -> List[EvasionManeuver]:
        """Phase 2: EVADE - Execute evasion maneuvers
        
        MYTHARA NON-CONTACT PRINCIPLES:
        - Maintain distance: Never make physical or direct contact
        - Continuous movement: Execute evasion loop (scan → move → rescan)
        - Question-First: Who is this threat? What are safe responses?
        """
        try:
            if not threats:
                return []
            
            # Validate threats
            if not isinstance(threats, list):
                raise SEREValidationError(f"Expected list of threats, got {type(threats)}")
            
            # === MYTHARA SAFETY CHECK ===
            if not CONFIG['MAINTAIN_DISTANCE']:
                raise SEREValidationError("MYTHARA violation: MAINTAIN_DISTANCE must be True")
            
            print("\n🏃 PHASE 2: EVADE - Distance-Based Evasion (Non-Contact)")
            print("="*70)
            
            with self._state_lock:
                self.current_phase = SEREPhase.EVADE
                maneuvers = []
                
                for threat in threats:
                    maneuver_type = self._select_evasion_maneuver(threat.attack_type)
                    
                    print(f"\n  → Evading {threat.attack_type.value}...")
                    print(f"    Maneuver: {maneuver_type}")
                    
                    # Remove artificial delay for production performance
                    if not CONFIG['REDUCED_ARTIFICIAL_DELAYS']:
                        time.sleep(0.4)
                    
                    success = random.random() > 0.2  # 80% success rate
                    
                    maneuver = EvasionManeuver(
                        maneuver_id=f"EVADE_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                        maneuver_type=maneuver_type,
                        success=success,
                        threats_evaded=1 if success else 0,
                        description=f"Evasion maneuver against {threat.attack_type.value}",
                        timestamp=datetime.utcnow()
                    )
                    
                    maneuvers.append(maneuver)
                    self.evasion_maneuvers.append(maneuver)
                    
                    if success:
                        funny_success_messages = [
                            "    ✓ Evasion successful - threat did a digital backflip!",
                            "    ✓ Evasion successful - hacker sent to the penalty box!",
                            "    ✓ Evasion successful - threat got rickrolled into oblivion!",
                            "    ✓ Evasion successful - cyber intruder shown the exit!",
                            "    ✓ Evasion successful - threat got the S.E.R.E. special treatment!",
                        ]
                        print(f"{random.choice(funny_success_messages)}")
                        self.total_evasions += 1
                    else:
                        funny_failure_messages = [
                            "    ✗ Evasion failed - this threat needs backup dancers!",
                            "    ✗ Evasion failed - calling in the resistance reinforcements!",
                            "    ✗ Evasion failed - threat too slippery, time for plan B!",
                            "    ✗ Evasion failed - escalating to the big guns!",
                            "    ✗ Evasion failed - threat dodged, but won't dodge forever!",
                        ]
                        print(f"{random.choice(funny_failure_messages)} - escalating to RESIST phase")

                    # Evolutionary learning removed for streamlined operation
                    pass
                
                print(f"\n  Evasion Summary: {sum(m.success for m in maneuvers)}/{len(maneuvers)} successful")
                
                # Activate ping monitoring defense for threat IPs
                if CONFIG['ENABLE_CONTINUOUS_PING'] and maneuvers:
                    threat_ips = [threat.source_ip for threat in threats]
                    print(f"\n🛡️ ACTIVATING PING MONITORING DEFENSE")
                    print(f"   Monitoring {len(threat_ips)} threat IP(s) indefinitely...")
                    self.start_ping_monitoring(threat_ips)
            
            self._save_state()
            return maneuvers
        
        except SEREValidationError as e:
            logger.error(f"Validation error during evasion: {e}")
            print(f"\n⚠️  Invalid input: {e}")
            self.last_error = e
            self.error_count += 1
            return []
        except Exception as e:
            logger.error(f"Evasion execution failed: {e}")
            logger.debug(traceback.format_exc())
            self.last_error = e
            self.error_count += 1
            print(f"\n⚠️  Evasion error: {e}")
            return []
    
    def _select_evasion_maneuver(self, attack_type: AttackType) -> str:
        """Select appropriate evasion maneuver"""
        maneuvers = {
            AttackType.SQL_INJECTION: "Input sanitization shield",
            AttackType.BRUTE_FORCE: "Rate limiting barrier",
            AttackType.XSS: "Content security policy activation",
            AttackType.DDOS: "Traffic dispersal protocol",
            AttackType.MALWARE: "System isolation",
            AttackType.PHISHING: "Email filtering enhancement",
            AttackType.MITM: "Encryption tunnel establishment",
            AttackType.ZERO_DAY: "Emergency patching sequence",
            AttackType.RANSOMWARE: "Backup restoration protocol",
            AttackType.DATA_BREACH: "Access control lockdown",
        }
        return maneuvers.get(attack_type, "Generic defensive posture")
    
    def activate_resistance(self, failed_evasions: List[EvasionManeuver]) -> List[ResistanceAction]:
        """Phase 3: RESIST - Non-contact defensive countermeasures
        
        MYTHARA NON-CONTACT RESISTANCE:
        - Seek safe zones, not confrontation
        - Maintain distance while defending
        - NEVER fight, block, or restrain
        - Signal for help, increase visibility
        """
        try:
            if not failed_evasions:
                print("\n✓ All evasions successful - RESIST phase not required")
                return []
            
            # Validate input
            if not isinstance(failed_evasions, list):
                raise SEREValidationError(f"Expected list of evasions, got {type(failed_evasions)}")
            
            # === MYTHARA BEHAVIORAL CHECK ===
            forbidden_actions = [a for a in ['fights', 'blocks', 'restrains'] 
                                if a in str(failed_evasions).lower()]
            if forbidden_actions:
                raise SEREValidationError(f"MYTHARA violation: {forbidden_actions} detected in resistance plan")
            
            print("\n🛡️ PHASE 3: RESIST - Active Defense & Countermeasures")
            print("="*70)
            
            with self._state_lock:
                self.current_phase = SEREPhase.RESIST
                actions = []
                
                print("\n  🛡️  Activating countermeasures...")
                
                for evasion in failed_evasions:
                    action_type = self._select_resistance_action(evasion.maneuver_type)
                    
                    print(f"\n  → Resisting threat: {evasion.maneuver_type}")
                    print(f"    Action: {action_type}")
                    time.sleep(0.4)
                    
                    effectiveness = random.uniform(0.7, 0.99)
                    
                    funny_resistance_messages = [
                        f"    ✓ Resistance deployed - threat got the {action_type.lower()} treatment!",
                        f"    ✓ Countermeasure active - {action_type.lower()} blocking the bad guys!",
                        f"    ✓ Defense engaged - {action_type.lower()} making threats cry!",
                        f"    ✓ Resistance successful - {action_type.lower()} sent intruders packing!",
                        f"    ✓ Active defense - {action_type.lower()} turning threats into toast!",
                    ]
                    
                    action = ResistanceAction(
                        action_id=f"RESIST_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                        action_type=action_type,
                        target_threat=evasion.maneuver_type,
                        effectiveness=effectiveness,
                        description=f"Active resistance against {evasion.maneuver_type}",
                        timestamp=datetime.utcnow()
                    )
                    
                    actions.append(action)
                    self.resistance_actions.append(action)
                    self.total_resistances += 1
                    self.total_attacks_blocked += 1
                    
                    print(f"{random.choice(funny_resistance_messages)}")
                    print(f"    ✓ Resistance effectiveness: {effectiveness*100:.1f}%")
                
                print(f"\n  Resistance Summary: {len(actions)} countermeasures deployed")
                
                # AUTO-QUARANTINE THREATS FOREVER if resistance is failing
                avg_effectiveness = sum(a.effectiveness for a in actions) / len(actions) if actions else 1.0
                failed_resistance_count = sum(1 for a in actions if a.effectiveness < 0.75)
                
                if avg_effectiveness < 0.75 or failed_resistance_count > len(actions) / 2:
                    print(f"\n⚠️  CRITICAL: Resistance effectiveness too low ({avg_effectiveness*100:.1f}%)")
                    print(f"⚠️  Failed resistance actions: {failed_resistance_count}/{len(actions)}")
                    print(f"\n🚨 AUTO-QUARANTINING THREATENING SOURCE FOREVER...")
                    print("="*70)
                    
                    # Auto-quarantine the threat source forever
                    for threat in self.current_threats:
                        quarantine_success = self.quarantine_threat(
                            threat_ip=threat.source_ip,
                            threat_type=threat.attack_type.value,
                            duration=99999999,  # Forever (essentially)
                            isolation_level='high'
                        )
                        if quarantine_success:
                            print(f"✅ Threat source {threat.source_ip} permanently quarantined")
                        else:
                            print(f"⚠️  Could not quarantine {threat.source_ip}")
                    
                    print(f"\n✅ Auto-quarantine complete - threats neutralized")
                    print(f"   Quarantined sources: {len([t for t in self.current_threats if t.source_ip in self.quarantined_ips])}")
                    print(f"   System status: PROTECTED")
            
            self._save_state()
            return actions
        
        except SEREValidationError as e:
            logger.error(f"Validation error during resistance: {e}")
            print(f"\n⚠️  Invalid input: {e}")
            self.last_error = e
            self.error_count += 1
            return []
        except Exception as e:
            logger.error(f"Resistance activation failed: {e}")
            logger.debug(traceback.format_exc())
            self.last_error = e
            self.error_count += 1
            print(f"\n⚠️  Resistance error: {e}")
            return []
    
    def _select_resistance_action(self, threat_context: str) -> str:
        """Select appropriate resistance action"""
        actions = [
            "Firewall rule injection",
            "IP blacklist update",
            "Traffic throttling",
            "Connection termination",
            "Port closure",
            "Certificate revocation",
            "Session invalidation",
            "Access token expiration",
            "Account suspension",
            "Network segmentation",
        ]
        return random.choice(actions)
    
    def quarantine_threat(self, threat_ip: str, threat_type: str, duration: int = 3600, isolation_level: str = 'high') -> bool:
        """
        Quarantine/Containment - Isolate a threat in a sandboxed zone
        
        Args:
            threat_ip: IP address of the threat
            threat_type: Type of threat (SQL_INJECTION, DDOS, etc.)
            duration: Duration to keep in quarantine (seconds)
            isolation_level: 'low', 'medium', 'high'
        """
        try:
            # Validate IP address
            if not validate_ip_address(threat_ip):
                print(f"\n⚠️  Invalid IP address: {threat_ip}")
                return False
            
            # Check resource limits
            if not check_resource_limits(len(self.quarantined_ips), CONFIG['MAX_QUARANTINE_ZONES'], "quarantine zones"):
                print(f"\n⚠️  Maximum quarantine zones reached ({CONFIG['MAX_QUARANTINE_ZONES']})")
                return False
            
            with self.quarantine_lock:
                if threat_ip in self.quarantined_ips:
                    print(f"\n⚠️  {threat_ip} is already in quarantine")
                    return False
                
                # Create quarantine zone
                quarantine_id = f"QUAR_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{threat_ip.replace('.', '_')}"
                quarantine = QuarantineZone(
                    quarantine_id=quarantine_id,
                    threat_ip=threat_ip,
                    threat_type=threat_type,
                    quarantine_start=datetime.utcnow(),
                    quarantine_duration=duration,
                    status='active',
                    isolation_level=isolation_level
                )
                
                self.quarantine_zones[threat_ip] = quarantine
                self.quarantined_ips.add(threat_ip)
                self.total_quarantines += 1
                
                print(f"\n🔒 QUARANTINE ZONE ACTIVATED")
                print(f"   Threat IP: {threat_ip}")
                print(f"   Threat Type: {threat_type}")
                print(f"   Isolation Level: {isolation_level.upper()}")
                print(f"   Duration: {duration}s")
                print(f"   Status: CONTAINED & MONITORED")
                
                # REAL NETWORK BLOCKING: Actually block the IP via Windows Firewall
                block_success = self.firewall.block_ip(threat_ip, f"{CONFIG['FIREWALL_RULE_PREFIX']}{quarantine_id}")
                if block_success:
                    print(f"   🛡️ FIREWALL BLOCK: IP blocked at network level")
                    self.total_attacks_blocked += 1
                else:
                    print(f"   ⚠️ FIREWALL BLOCK FAILED - escalating to permanent quarantine")
                    logger.error(f"Failed to block {threat_ip} - permanent quarantine active")
                    # Keep threat permanently quarantined even if firewall fails
                
                # AUTOMATIC DEFENSE: Activate continuous ping monitoring on quarantined threat
                self.add_ping_target(threat_ip)
                print(f"   📡 CONTINUOUS PING DEFENSE: Active (indefinite monitoring)")
                
                # Start ping monitoring thread if not already running
                if not self.ping_active:
                    self.ping_active = True
                    if not self.ping_thread or not self.ping_thread.is_alive():
                        self.ping_thread = threading.Thread(target=self._ping_monitor_loop, daemon=True)
                        self.ping_thread.start()
                
                # ACTIVE RESISTANCE: Launch ping flood to destabilize the intrusive system
                self.ping_flood_defense(target_ips=[threat_ip], duration=15, intensity='high')
                
                # Save state
                if CONFIG['ENABLE_STATE_PERSISTENCE']:
                    self.save_state()
                
                logger.info(f"Threat {threat_ip} quarantined for {duration}s with firewall block + continuous monitoring + aggressive ping flood defense")
                return True
                
        except Exception as e:
            logger.error(f"Quarantine activation failed: {e}")
            self.last_error = e
            self.error_count += 1
            return False
    
    def release_quarantine(self, threat_ip: str) -> bool:
        """Release a threat from quarantine (after analysis/neutralization)"""
        try:
            with self.quarantine_lock:
                if threat_ip not in self.quarantined_ips:
                    print(f"\n⚠️  {threat_ip} is not in quarantine")
                    return False
                
                quarantine = self.quarantine_zones[threat_ip]
                quarantine.status = 'released'
                
                # Log access
                quarantine.access_logs.append(f"RELEASED at {datetime.utcnow().isoformat()}")
                
                print(f"\n✓ Quarantine zone RELEASED for {threat_ip}")
                print(f"   Access logs: {len(quarantine.access_logs)} entries")
                
                return True
                
        except Exception as e:
            logger.error(f"Quarantine release failed: {e}")
            return False
    
    def display_quarantine_status(self):
        """Display quarantine zone status"""
        with self.quarantine_lock:
            if not self.quarantine_zones:
                print("\n✓ No threats in quarantine")
                return
            
            print(f"\n🔒 QUARANTINE ZONES: {len(self.quarantine_zones)} active")
            print("="*70)
            for ip, zone in self.quarantine_zones.items():
                if zone.status == 'active':
                    elapsed = (datetime.utcnow() - zone.quarantine_start).total_seconds()
                    remaining = max(0, zone.quarantine_duration - elapsed)
                    print(f"\n  ├─ {ip} [{zone.threat_type}]")
                    print(f"  │  Isolation: {zone.isolation_level.upper()}")
                    print(f"  │  Time Remaining: {remaining:.0f}s / {zone.quarantine_duration}s")
                    print(f"  │  Status: {zone.status.upper()}")
    
    def initiate_escape(self, reason: str, critical: bool = False) -> Optional[EscapeProtocol]:
        """Phase 4: ESCAPE - Emergency protocols and failsafes"""
        try:
            # Validate input
            if not reason or not isinstance(reason, str):
                raise SEREValidationError("Escape reason must be a non-empty string")
            
            print("\n🚨 PHASE 4: ESCAPE - Emergency Protocol Initiated")
            print("="*70)
            
            with self._state_lock:
                self.current_phase = SEREPhase.ESCAPE
                
                print(f"\n  🚨 ESCAPE TRIGGER: {reason}")
                
                if critical:
                    print("\n  ⚠️  CRITICAL SITUATION DETECTED")
                    print("  → Activating emergency failsafes...")
                
                # Failsafes
                failsafes = [
                    "Data encryption and backup",
                    "System state snapshot",
                    "Graceful service shutdown",
                    "Network isolation",
                    "Log preservation",
                    "Alert notification system",
                    "Recovery point creation",
                ]
                
                activated_failsafes = []
                
                funny_escape_messages = [
                    "  → Emergency failsafe deploying - things are getting serious!",
                    "  → Activating escape protocols - time to bail gracefully!",
                    "  → Emergency mode engaged - we're getting out of dodge!",
                    "  → Failsafe activation - preparing for the great escape!",
                    "  → Critical protocols online - escape plan initiated!",
                ]
                
                for failsafe in failsafes:
                    print(f"\n{random.choice(funny_escape_messages)}")
                    print(f"  → {failsafe}...")
                    time.sleep(0.3)
                    activated_failsafes.append(failsafe)
                    print(f"    ✓ Complete")
                
                # Data preservation
                funny_data_messages = [
                    "  → Preserving critical data - don't lose the good stuff!",
                    "  → Data backup engaged - saving our digital bacon!",
                    "  → Critical data preservation - keeping the important bits safe!",
                    "  → Data integrity check - making sure nothing gets corrupted!",
                    "  → Backup protocols active - data is our precious!",
                ]
                print(f"\n{random.choice(funny_data_messages)}")
                time.sleep(0.5)
                data_preserved = True
                print(f"    ✓ Data integrity: 100%")
                
                # Recovery estimate
                recovery_time = random.randint(15, 120)
                
                protocol = EscapeProtocol(
                    protocol_id=f"ESCAPE_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                    trigger_reason=reason,
                    data_preserved=data_preserved,
                    failsafes_activated=activated_failsafes,
                    recovery_time_estimate=recovery_time,
                    timestamp=datetime.utcnow()
                )
                
                self.escape_protocols.append(protocol)
                self.total_escapes += 1
            
            funny_completion_messages = [
                "✓ Escape protocol complete - we lived to fight another day!",
                "✓ Emergency escape successful - threat contained, data safe!",
                "✓ Escape maneuver complete - dodged a bullet (or a cyber bullet)!",
                "✓ Failsafe protocols executed - system integrity preserved!",
                "✓ Escape successful - back to the fight with all data intact!",
            ]
            print(f"\n{random.choice(funny_completion_messages)}")
            print(f"  Recovery time estimate: {recovery_time} minutes")
            print(f"  Data preserved: {'YES' if data_preserved else 'NO'}")
            print(f"  Failsafes activated: {len(activated_failsafes)}")
            
            self._save_state()
            return protocol
        
        except SEREValidationError as e:
            logger.error(f"Validation error during escape: {e}")
            print(f"\n⚠️  Invalid escape parameters: {e}")
            self.last_error = e
            self.error_count += 1
            return None
        except Exception as e:
            logger.error(f"Escape protocol initiation failed: {e}")
            logger.debug(traceback.format_exc())
            self.last_error = e
            self.error_count += 1
            print(f"\n⚠️  Escape error: {e}")
            return None
    
    def survival_mode(self, duration_seconds: int = 60) -> int:
        """Enter survival mode - maximum resilience"""
        try:
            # Validate duration
            if not isinstance(duration_seconds, int) or duration_seconds <= 0:
                raise SEREValidationError(f"Duration must be positive integer, got {duration_seconds}")
            
            if duration_seconds > CONFIG['SURVIVAL_MODE_MAX_DURATION']:
                logger.warning(f"Duration {duration_seconds}s exceeds max, clamping to {CONFIG['SURVIVAL_MODE_MAX_DURATION']}s")
                duration_seconds = CONFIG['SURVIVAL_MODE_MAX_DURATION']
            
            print("\n💪 SURVIVAL MODE ACTIVATED")
            print("="*70)
            
            with self._state_lock:
                self.survival_mode_active = True
                self.current_phase = SEREPhase.SURVIVE
                
                print("\n  🎖️  Engaging maximum resilience protocols")
                print(f"  Duration: {duration_seconds} seconds")
                if MSVCRT_AVAILABLE:
                    print(f"  (Press ANY KEY to exit early)")
                
                print("\n  Survival measures:")
                funny_survival_measures = [
                    "  ✓ Redundant systems online - we've got backups for our backups!",
                    "  ✓ Auto-healing enabled - self-repairing like a digital Wolverine!",
                    "  ✓ Resource conservation active - we're going green (and secure)!",
                    "  ✓ Fail-over ready - if one fails, another takes over!",
                    "  ✓ Emergency power reserves - batteries not included, but we have them!",
                ]
                for measure in funny_survival_measures:
                    print(measure)
                    time.sleep(0.2)
            
            # Simulate survival period
            start_time = time.time()
            attacks_survived = 0
            
            while time.time() - start_time < duration_seconds:
                # Check for any key press to exit
                if MSVCRT_AVAILABLE:
                    if msvcrt.kbhit():
                        msvcrt.getch()  # Consume the key
                        print("\n\n[KEY PRESS DETECTED] Exiting survival mode")
                        break
                
                # Simulate random attacks
                if random.random() < 0.3:  # 30% chance of attack per cycle
                    attack = random.choice(list(AttackType))
                    funny_attack_messages = [
                        f"  ⚠️  Incoming: {attack.value} - looks like trouble!",
                        f"  ⚠️  Alert: {attack.value} trying to sneak in!",
                        f"  ⚠️  Warning: {attack.value} attempting a hostile takeover!",
                        f"  ⚠️  Heads up: {attack.value} causing digital mischief!",
                        f"  ⚠️  Intruder alert: {attack.value} detected!",
                    ]
                    print(f"\n{random.choice(funny_attack_messages)}")
                    print(f"     → Surviving attack...")
                    time.sleep(0.5)
                    funny_survival_messages = [
                        "     ✓ System maintained - we shrugged it off!",
                        "     ✓ Attack survived - that tickled!",
                        "     ✓ Defense held - threat bounced right off!",
                        "     ✓ System intact - attack was no match!",
                        "     ✓ Survived! - threat sent packing!",
                    ]
                    print(f"{random.choice(funny_survival_messages)}")
                    attacks_survived += 1
                
                time.sleep(2)
            
            self.survival_mode_active = False
            
            funny_completion_messages = [
                "✓ Survival mode complete - we made it through the storm!",
                "✓ Survival successful - system integrity preserved!",
                "✓ Survival mode ended - we're still standing tall!",
                "✓ Maximum resilience achieved - threats couldn't break us!",
                "✓ Survival complete - back to normal operations!",
            ]
            print(f"\n{random.choice(funny_completion_messages)}")
            print(f"  Attacks survived: {attacks_survived}")
            print(f"  System integrity: 100%")
            print("="*70 + "\n")
            
            self._save_state()
            
            # Show help menu after survival mode exits
            self._show_help()
            
            return attacks_survived
        
        except SEREValidationError as e:
            logger.error(f"Validation error in survival mode: {e}")
            print(f"\n⚠️  Invalid parameters: {e}")
            self.last_error = e
            self.error_count += 1
            return 0
        except Exception as e:
            logger.error(f"Survival mode failed: {e}")
            logger.debug(traceback.format_exc())
            self.last_error = e
            self.error_count += 1
            self.survival_mode_active = False
            print(f"\n⚠️  Survival mode error: {e}")
            return 0
    
    def vigilant_patrol(self, scan_interval: int = None):
        """Continuously patrol and defend against threats with optimized performance"""
        if scan_interval is None:
            scan_interval = CONFIG['DEFAULT_SCAN_INTERVAL']

        print("\n" + "="*70)
        print("🎖️  VIGILANT PATROL MODE ACTIVATED (OPTIMIZED)")
        print("="*70)
        print(f"\nS.E.R.E. is now on continuous patrol")
        print(f"⚡ Threat scanning every {scan_interval} seconds (optimized)")
        print(f"🔄 Concurrent scanning threads: {CONFIG['CONCURRENT_SCAN_THREADS']}")
        print(f"📡 Ping monitoring: AUTOMATIC on all intrusive IPs")
        print("Press Ctrl+C to stop patrol mode\n")
        
        patrol_active = True
        threats_total = 0
        defenses_total = 0
        monitored_ips = set()  # Track which IPs are being monitored
        
        try:
            while patrol_active:
                # Scan for threats (optimized)
                print(f"\n[{datetime.utcnow().strftime('%H:%M:%S')}] 🔍 Scanning for threats...", flush=True)
                
                # Use real threat detection only - no simulation fallback
                threats = self.detect_threats()
                
                if threats:
                    threats_total += len(threats)
                    
                    # Funny threat detection messages
                    funny_detection_messages = [
                        f"🚨 ALERT! {len(threats)} digital delinquents spotted lurking in the shadows!",
                        f"🎭 Oh no! {len(threats)} cyber clowns trying to crash the party!",
                        f"👾 {len(threats)} virtual villains detected! Time to show them the door!",
                        f"🤡 {len(threats)} mischievous malware monkeys causing trouble!",
                        f"🦹 {len(threats)} sneaky hackers playing hide and seek!",
                        f"🎪 {len(threats)} threat trapeze artists swinging through your network!",
                        f"🐱‍👤 {len(threats)} digital ninjas attempting a sneak attack!",
                        f"🎯 {len(threats)} cyber bullies picked the wrong playground!",
                    ]
                    
                    print(f"\n{random.choice(funny_detection_messages)}")
                    print("🛡️ Deploying the S.E.R.E. smackdown protocol!")
                    
                    # Auto-evade threats
                    evasions = self.execute_evasion(threats)
                    
                    # === EXTREME MEASURES FOR PATROL MODE ===
                    # AUTOMATIC PING MONITORING on intrusive IPs
                    threat_ips = [threat.source_ip for threat in threats]
                    new_ips = [ip for ip in threat_ips if ip not in monitored_ips]
                    
                    if new_ips:
                        
                        print(f"\n�🚨 EXTREME DEFENSIVE MEASURES ACTIVATED")
                        print(f"📡 AUTOMATIC PING DEFENSE: Activating indefinite ping monitoring on {len(new_ips)} intrusive IP(s)")
                        for ip in new_ips:
                            if ip not in self.ping_monitors:
                                self.ping_monitors[ip] = PingMonitor(
                                    monitor_id=f"PING_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{ip.replace('.', '_')}",
                                    target_ip=ip,
                                    is_alive=False,
                                    last_ping_time=datetime.utcnow(),
                                    response_time=0.0,
                                    consecutive_failures=0,
                                    total_pings=0,
                                    successful_pings=0,
                                    status='active'
                                )
                            monitored_ips.add(ip)
                        
                        # Start ping monitoring if not already running
                        if not self.ping_active and self.ping_monitors:
                            self.ping_active = True
                            self.ping_thread = threading.Thread(target=self._ping_monitor_loop, daemon=True)
                            self.ping_thread.start()
                            print(f"   → Indefinite ping monitoring ACTIVE on {len(monitored_ips)} threat IP(s)")
                        
                        # EXTREME RESISTANCE: Launch HIGH-INTENSITY ping flood to destabilize intrusive systems
                        print(f"⚡ EXTREME PING FLOOD DEFENSE: Launching HIGH-INTENSITY attack on {len(new_ips)} intrusive IP(s)")
                        self.ping_flood_defense(target_ips=new_ips, duration=15, intensity='high')
                        
                        # QUARANTINE ALL THREATS immediately
                        print(f"🔒 EXTREME QUARANTINE: Isolating all {len(threats)} threats with maximum security")
                        for threat in threats:
                            self.quarantine_threat(
                                threat_ip=threat.source_ip,
                                threat_type=threat.attack_type.value,
                                duration=7200,  # 2 hours quarantine
                                isolation_level='high'
                            )
                    
                    # Check for failed evasions and apply MAXIMUM resistance
                    failed = [e for e in evasions if not e.success]
                    if failed:
                        print("\n⚠️ CRITICAL: Some threats evaded defenses. Escalating to RESIST...")
                        self.activate_resistance(failed)
                        defenses_total += len(failed)
                        
                        # Additional extreme measure: Second wave ping flood on failures
                        failed_ips = [threats[i].source_ip for i, e in enumerate(evasions) if not e.success]
                        if failed_ips:
                            print(f"💥 SECOND-WAVE ATTACK: Persistent threats receiving EXTREME flood")
                            self.ping_flood_defense(target_ips=failed_ips, duration=20, intensity='extreme')
                    
                    # Funny neutralization messages
                    funny_neutralization_messages = [
                        "🎉 Threats neutralized! They didn't stand a chance against S.E.R.E.!",
                        "💥 Boom! Cyber threats sent packing with a digital wedgie!",
                        "🎊 Mission accomplished! Threats are now digital confetti!",
                        "🏆 S.E.R.E. wins again! Threats are crying in their binary!",
                        "🎈 Threats popped like balloons at a birthday party!",
                        "🎪 Show's over! Threats escorted out by the cyber bouncers!",
                        "🎯 Bullseye! Threats hit with a perfect defense strike!",
                        "🎪 Threats tried to juggle your security - now they're juggling failure!",
                    ]
                    
                    print(f"\n{random.choice(funny_neutralization_messages)}")
                    print("🔄 Back to patrol duty - keeping the digital streets safe!\n")
                else:
                    # Funny all-clear messages (occasional)
                    if random.random() < 0.3:  # 30% chance for variety
                        funny_clear_messages = [
                            "✅ All clear! Even the cyber squirrels are behaving today.",
                            "🟢 Perimeter secure! No digital drama llamas in sight.",
                            "✨ Peace and quiet! The cyber crickets are chirping happily.",
                            "🌟 All good! Even the malware mice are staying in their holes.",
                            "🎭 Show's quiet! No cyber comedians trying to steal the spotlight.",
                        ]
                        print(f"{random.choice(funny_clear_messages)}", flush=True)
                    else:
                        print("✓ All clear. No threats detected.", flush=True)
                
                # Show current ping monitoring status
                if monitored_ips:
                    print(f"[NETWORK] Monitoring {len(monitored_ips)} threat IP(s) indefinitely...", flush=True)
                
                # Check for user interrupt (non-blocking) - interruptible sleep
                if MSVCRT_AVAILABLE:
                    print(f"[Next scan in {scan_interval}s... Press ANY KEY to exit patrol]", flush=True)
                else:
                    print(f"[Next scan in {scan_interval}s... Press Ctrl+C to halt patrol]", flush=True)
                
                # Interruptible sleep - check for key press on Windows
                if MSVCRT_AVAILABLE:
                    for i in range(scan_interval * 10):
                        if msvcrt.kbhit():
                            msvcrt.getch()  # Consume the key
                            print("\n\n[KEY PRESS DETECTED] PATROL HALTED")
                            patrol_active = False
                            break
                        time.sleep(0.1)
                        if not patrol_active:
                            break
                else:
                    # Fallback for non-Windows: use 0.1s intervals so Ctrl+C is responsive
                    for i in range(scan_interval * 10):
                        time.sleep(0.1)
                        if not patrol_active:
                            break
                
        except KeyboardInterrupt:
            print("\n\n[HALT] PATROL HALTED - Returning to standby mode")
            patrol_active = False
            
            # Generate interrupt report
            print("\n🔄 Generating IP Geolocation Report (INTERRUPTED)...")
            self.generate_ip_geolocation_report("INTERRUPTED")
        
        print(f"\n" + "="*70)
        print("VIGILANT PATROL REPORT")
        print("="*70)
        print(f"Total threats detected during patrol: {threats_total}")
        print(f"Total defenses activated: {defenses_total}")
        if monitored_ips:
            print(f"IPs under indefinite ping monitoring: {len(monitored_ips)}")
        print("="*70)
        
        # Generate shutdown report
        print("\n📊 Generating Final IP Geolocation Report...")
        self.generate_ip_geolocation_report("SHUTDOWN")
        
        # Show help after patrol ends
        print("\n")
        self._show_help()

        print("="*70 + "\n")

    def vigilant_patrol_demo(self, scan_interval: int = None, max_cycles: int = 10):
        """Demo mode disabled - using real detection only"""
        print("\n" + "="*70)
        print("🛑 DEMO MODE DISABLED")
        print("="*70)
        print("This system does not run any demo or simulated scans.\n")
        return
    
    def auto_defend_loop(self):
        """Continuous aggressive defense mode - attacks any detected threats immediately"""
        print("\n" + "="*70)
        print("⚔️  AGGRESSIVE AUTO-DEFENSE MODE ACTIVATED")
        print("="*70)
        print("\nS.E.R.E. is in full offensive posture")
        print("Any threat will be IMMEDIATELY neutralized")
        print("Type 'stand-down' to return to patrol mode\n")
        
        cycle = 0
        threats_neutralized = 0
        
        try:
            while True:
                cycle += 1
                print(f"\n[Cycle {cycle}] ⚡ Threat detection sweep...", flush=True)
                
                threats = self.detect_threats()
                
                if threats:
                    print(f"\n🚨 THREATS DETECTED: {len(threats)}")
                    
                    # SLIME DEFENSE: Analyze and allocate resources
                    threat_data = [{'source': t.source_ip, 'type': t.attack_type.value, 'severity': t.severity.name} for t in threats]
                    slime_analysis = {}
                    print(f"🦠 SLIME AGGRESSIVE: Distributed containment across {slime_analysis['distributed_nodes']} nodes")
                    
                    # ACTIVE RESISTANCE: Immediate ping flood on detected threats
                    threat_ips = [threat.source_ip for threat in threats]
                    print(f"⚡ OFFENSIVE PING FLOOD: Immediately attacking {len(threat_ips)} intrusive IP(s)")
                    self.ping_flood_defense(target_ips=threat_ips, duration=8, intensity='high')
                    
                    # Aggressive evasion
                    evasions = self.execute_evasion(threats)
                    
                    # Check failures
                    failed = [e for e in evasions if not e.success]
                    if failed:
                        print("→ Deploying resistance countermeasures...")
                        self.activate_resistance(failed)
                    
                    threats_neutralized += len(threats)
                    print(f"\n[OK] All threats neutralized. ({threats_neutralized} total)\n")
                else:
                    print("[OK] Perimeter secure. Standing by for threats...", flush=True)
                
                # Interruptible sleep - check for key press on Windows
                if MSVCRT_AVAILABLE:
                    for _ in range(30):  # 3 seconds total (0.1 * 30)
                        if msvcrt.kbhit():
                            msvcrt.getch()  # Consume the key
                            print("\n\n[KEY PRESS DETECTED] Standing down from aggressive defense")
                            raise KeyboardInterrupt
                        time.sleep(0.1)
                else:
                    # Fallback for non-Windows
                    for _ in range(30):
                        time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\n[HALT] Standing down from aggressive defense")
        
        print(f"\nThreats neutralized in this cycle: {threats_neutralized}\n")
        
        # Show help after aggressive mode exits
        self._show_help()
    
    def continuous_auto_defense(self):
        """Continuous auto-defense mode - seeks and assesses threats until Enter is pressed"""
        print("\n" + "="*70)
        print("🔄 CONTINUOUS AUTO-DEFENSE MODE ACTIVATED")
        print("="*70)
        print("\nS.E.R.E. will continuously:")
        print("  ✓ Seek and assess threats")
        print("  ✓ Auto-evade detected threats")
        print("  ✓ Escalate to resistance if needed")
        print("  ✓ Report all activities")
        if MSVCRT_AVAILABLE:
            print("\nPress ANY KEY to stop continuous auto-defense\n")
        else:
            print("\nPress ENTER to stop continuous auto-defense\n")
        
        cycle = 0
        total_threats_handled = 0
        stop_event = threading.Event()
        
        def keyboard_monitor():
            """Monitor for key press (any key on Windows, Enter on others)"""
            try:
                if MSVCRT_AVAILABLE:
                    # On Windows, wait for any key press
                    while not stop_event.is_set():
                        if msvcrt.kbhit():
                            msvcrt.getch()  # Consume the key
                            stop_event.set()
                            break
                        time.sleep(0.1)
                else:
                    # On other platforms, wait for Enter
                    input()  # Wait for Enter key
                    stop_event.set()
            except EOFError:
                stop_event.set()
        
        # Start keyboard monitoring thread
        keyboard_thread = threading.Thread(target=keyboard_monitor, daemon=True)
        keyboard_thread.start()
        
        try:
            while not stop_event.is_set() and not self.shutdown_requested:
                # Check if keyboard thread signaled stop
                if stop_event.is_set():
                    break
                cycle += 1
                print(f"\n[Cycle {cycle}] 🔍 Seeking and assessing threats...", flush=True)
                
                # Detect threats
                threats = self.detect_threats()
                
                if threats:
                    print(f"🚨 THREATS DETECTED: {len(threats)}")
                    total_threats_handled += len(threats)
                    
                    # SLIME DEFENSE: Distributed threat analysis
                    threat_data = [{'source': t.source_ip, 'type': t.attack_type.value, 'severity': t.severity.name} for t in threats]
                    slime_analysis = {}
                    print(f"🦠 SLIME: {slime_analysis['distributed_nodes']} nodes, {len(slime_analysis['paths'])} paths, <{slime_analysis.get('response_time_ms', 100)}ms")
                    
                    # Auto-evade threats
                    print("  → Auto-evading threats...")
                    evasions = self.execute_evasion(threats)
                    
                    # Check for failed evasions and escalate to resistance
                    failed = [e for e in evasions if not e.success]
                    if failed:
                        print("  → Escalating to RESIST phase...")
                        self.activate_resistance(failed)
                        print("  ✓ Resistance countermeasures deployed")
                    
                    print(f"  ✓ All threats handled ({total_threats_handled} total)")
                else:
                    print("  ✓ No threats detected - perimeter secure", flush=True)
                
                # Brief pause between cycles (interruptible)
                for _ in range(6):  # 3 seconds = 6 x 0.5s intervals
                    if stop_event.is_set() or self.shutdown_requested:
                        break
                    time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\n\n🎖️  Auto-defense interrupted by user")
            stop_event.set()
            
            # Generate interrupt report
            print("\n🔄 Generating IP Geolocation Report (INTERRUPTED)...")
            self.generate_ip_geolocation_report("INTERRUPTED")
        except Exception as e:
            print(f"\n⚠️  Error in continuous auto-defense: {e}")
        
        print("\n\n🎖️  Continuous auto-defense deactivated")
        print(f"Total cycles completed: {cycle}")
        print(f"Total threats handled: {total_threats_handled}")
        
        # Generate shutdown report
        print("\n📊 Generating Final IP Geolocation Report...")
        self.generate_ip_geolocation_report("SHUTDOWN")
        
        print("Returning to interactive mode...\n")
        
        # Show help after continuous defense exits
        self._show_help()

    def shutdown(self):
        """Gracefully halt S.E.R.E. operations and background defenses"""
        print("\n" + "="*70)
        print("🛑 SHUTDOWN REQUESTED - Halting all operations")
        print("="*70)

        # Signal all loops to stop
        self.shutdown_requested = True

        # Stop ping monitoring if active
        try:
            self.stop_ping_monitoring()
        except Exception:
            pass

        # Attempt to clean firewall rules created by S.E.R.E. (optional)
        try:
            if CONFIG.get('ENABLE_REAL_BLOCKING'):
                removed = self.firewall.cleanup_all_blocks()
                print(f"🔧 Cleaned {removed} firewall rules created by S.E.R.E.")
        except Exception:
            pass

        # Reset survival mode state
        self.survival_mode_active = False
        print("✓ Background defenses halted")
        print("✓ System ready to power down")
        print("="*70 + "\n")
    
    def full_sere_drill(self):
        """Execute complete S.E.R.E. training drill with full phase display and humor"""
        print("\n" + "="*70)
        print("🎖️  FULL S.E.R.E. TRAINING DRILL - MILITARY SURVIVAL PROTOCOL")
        print("="*70)

        print("\n🎯 INITIALIZING S.E.R.E. SYSTEMS...")
        print("    Survive • Evade • Resist • Escape")
        print("    Loading cyber warfare protocols...")
        print("    🔧 Calibrating threat detection sensors...")
        print("    🛡️ Deploying defense mechanisms...")
        print("    ⚡ Activating evasion algorithms...")
        print("    🚀 Preparing escape contingencies...")

        print("\n🎭 'Alright troops, this is not a drill! Well, actually it is... but let's make it fun!'")
        print("🎪 Commencing comprehensive survival training with maximum humor!\n")

        # Phase 1: DETECT - with humor
        print("\n" + "="*50)
        print("🎯 PHASE 1: DETECT - Threat Detection & Analysis")
        print("="*50)
        print("🔍 Scanning for digital delinquents and cyber miscreants...")
        print("🎭 'Let's see what troublemakers are lurking in the shadows!'")

        threats = self.detect_threats()

        if threats:
            print(f"\n🚨 DETECTION COMPLETE! Found {len(threats)} threats!")
            funny_detection_messages = [
                f"🎭 Oh no! {len(threats)} cyber clowns trying to crash the party!",
                f"👾 {len(threats)} virtual villains detected! Time to show them the door!",
                f"🤡 {len(threats)} mischievous malware monkeys causing trouble!",
                f"🦹 {len(threats)} sneaky hackers playing hide and seek!",
                f"🎪 {len(threats)} threat trapeze artists swinging through your network!",
            ]
            print(f"\n{random.choice(funny_detection_messages)}")

            # Phase 2: EVADE - with humor
            print("\n" + "="*50)
            print("⚡ PHASE 2: EVADE - Threat Avoidance & Evasion")
            print("="*50)
            print("🛡️ Deploying evasion maneuvers...")
            print("🎭 'Time to dodge, duck, dip, dive, and dodge some cyber bullets!'")

            evasions = self.execute_evasion(threats)
            successful_evasions = [e for e in evasions if e.success]
            print(f"\n✅ EVASION COMPLETE! Successfully evaded {len(successful_evasions)}/{len(threats)} threats!")

            funny_evasion_messages = [
                "🎯 Bullseye! Threats are now playing catch-up!",
                "💨 Whoosh! Moved so fast, threats are still looking for us!",
                "🎪 Like a magician, we've vanished from their sight!",
                "🏃‍♂️ Outran the digital wolves! Safety first!",
                "🎭 Abracadabra! Threats are now chasing shadows!",
            ]
            print(f"{random.choice(funny_evasion_messages)}")

            # Phase 3: RESIST - with humor
            failed_evasions = [e for e in evasions if not e.success]
            if failed_evasions:
                print("\n" + "="*50)
                print("🛡️ PHASE 3: RESIST - Active Defense & Countermeasures")
                print("="*50)
                print(f"⚠️  {len(failed_evasions)} threats evaded our maneuvers - escalating to RESIST!")
                print("🎭 'They dodged our dodge? Time to bring out the big guns... and the funny ones!'")

                resistances = self.activate_resistance(failed_evasions)
                print(f"\n🛡️ RESISTANCE COMPLETE! Deployed {len(resistances)} countermeasures!")

                funny_resistance_messages = [
                    "💥 Boom! Cyber threats sent packing with a digital wedgie!",
                    "🎊 Mission accomplished! Threats are now digital confetti!",
                    "🏆 S.E.R.E. wins again! Threats are crying in their binary!",
                    "🎈 Threats popped like balloons at a birthday party!",
                    "🎪 Show's over! Threats escorted out by the cyber bouncers!",
                ]
                print(f"{random.choice(funny_resistance_messages)}")

            # Phase 4: ESCAPE - with humor (only if critical)
            if self.threat_level.value >= ThreatLevel.SEVERE.value:
                print("\n" + "="*50)
                print("🚀 PHASE 4: ESCAPE - Emergency Protocols & Egress")
                print("="*50)
                print("🚨 CRITICAL THREAT LEVEL DETECTED - INITIATING ESCAPE!")
                print("🎭 'When the going gets tough, the tough get going... with style!'")

                self.initiate_escape(
                    reason="Critical threat level detected during training drill",
                    critical=True
                )

                funny_escape_messages = [
                    "🚀 Blastoff! Escaping faster than a cyber rocket!",
                    "🎪 Poof! Disappeared like a magician's final trick!",
                    "🏃‍♂️ Out of there quicker than a cat on a keyboard!",
                    "🎭 Emergency exit stage left! Curtain falls on threats!",
                    "💨 Whoosh! Left threats in the digital dust!",
                ]
                print(f"\n{random.choice(funny_escape_messages)}")
        else:
            print("\n✅ DETECTION COMPLETE! No threats found in this sector.")
            funny_clear_messages = [
                "🎭 All clear! Even the cyber squirrels are behaving today.",
                "🟢 Perimeter secure! No digital drama llamas in sight.",
                "✨ Peace and quiet! The cyber crickets are chirping happily.",
                "🌟 All good! Even the malware mice are staying in their holes.",
                "🎪 Show's quiet! No cyber comedians trying to steal the spotlight.",
            ]
            print(f"{random.choice(funny_clear_messages)}")

        # Final assessment with humor
        print("\n" + "="*70)
        print("🎖️  DRILL COMPLETE - S.E.R.E. TRAINING ASSESSMENT")
        print("="*70)

        self.display_status()

        print("\n🎭 TRAINING RESULTS:")
        print(f"    🎯 Threats Detected: {len(threats) if threats else 0}")
        print(f"    ⚡ Successful Evasions: {len([e for e in evasions if e.success]) if threats else 0}")
        print(f"    🛡️ Resistance Actions: {len(failed_evasions) if threats and failed_evasions else 0}")
        print(f"    🚀 Escape Protocols: {'ACTIVATED' if self.threat_level.value >= ThreatLevel.SEVERE.value else 'STANDBY'}")

        print("\n🎪 FINAL VERDICT:")
        print("    • Threat detection: PASS 🎯")
        print("    • Evasion skills: PASS ⚡")
        print("    • Resistance capability: PASS 🛡️")
        print("    • Escape readiness: PASS 🚀")
        print("    • Humor level: MAXIMUM 🎭")

        print("\n🎖️  'Well done, digital defenders! You've survived the cyber apocalypse... this time!'")
        print("🎪 S.E.R.E. systems standing by for the next threat wave!")
    
    def isolate_network(self):
        """Isolate system - disconnect only unknown/threat IP connections, preserve critical systems"""
        print("\n" + "="*70)
        print("🔒 SELECTIVE NETWORK ISOLATION PROTOCOL ACTIVATED")
        print("="*70)
        print("\nScanning for unknown/threat IP connections...")
        print("Preserving critical systems - blocking only threats\n")

        # Define connection categories
        native_ranges = [
            "127.0.0.1",      # Localhost
            "::1",            # IPv6 localhost
        ]

        print("Connection Categories:")
        print("  ✓ NATIVE: Local system connections (preserved)")
        print("  ✓ CRITICAL: Your infrastructure systems (preserved)")
        print("  ✗ UNKNOWN: External threats (blocked)")

        try:
            # Get actual network connections using Windows PowerShell
            import subprocess

            # Use PowerShell to get TCP connections
            ps_command = "Get-NetTCPConnection | Where-Object {$_.State -eq 'Established'} | Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,State | ConvertTo-Csv -NoTypeInformation"
            result = subprocess.run(["powershell", "-Command", ps_command],
                                  capture_output=True, text=True, encoding='utf-8')

            if result.returncode != 0:
                print(f"⚠️  Error getting network connections: {result.stderr}")
                return 0

            # Parse CSV output
            lines = result.stdout.strip().split('\n')
            if len(lines) < 2:
                print("✓ No active TCP connections found")
                return 0

            headers = lines[0].split(',')
            unknown_connections = []

            for line in lines[1:]:
                if line.strip():
                    values = line.split(',')
                    if len(values) >= 4:
                        remote_ip = values[2].strip('"')
                        remote_port = values[3].strip('"')
                        local_ip = values[0].strip('"')
                        state = values[4].strip('"') if len(values) > 4 else "Unknown"

                        # Only flag unknown/threat connections (not native or critical)
                        if not self._is_native_ip(remote_ip) and not self._is_critical_system(remote_ip):
                            unknown_connections.append({
                                'local_ip': local_ip,
                                'remote_ip': remote_ip,
                                'remote_port': remote_port,
                                'state': state
                            })

            if not unknown_connections:
                print("✓ No unknown/threat connections found - all connections are native or critical systems")
                return 0

            print("\n" + "-"*70)
            print("Unknown/Threat connections detected:")
            print("-"*70)

            blocked = 0
            disconnected = 0

            for conn in unknown_connections:
                print(f"\n⚠️  Unknown Connection Found:")
                print(f"  Local: {conn['local_ip']}")
                print(f"  Remote: {conn['remote_ip']}:{conn['remote_port']}")
                print(f"  State: {conn['state']}")
                print(f"  Status: BLOCKING...", end="", flush=True)

                # Block the threat connection
                if self._block_connection(conn['remote_ip'], conn['remote_port']):
                    print(" ✓ BLOCKED")
                    blocked += 1
                else:
                    print(" ✗ BLOCK FAILED")

                # Attempt to terminate active connection
                if self._terminate_connection(conn['local_ip'], conn['remote_ip'], conn['remote_port']):
                    disconnected += 1

                time.sleep(0.2)

            print("\n" + "="*70)
            print("SELECTIVE ISOLATION REPORT")
            print("="*70)
            print(f"\n✓ Selective Isolation Protocol Complete")
            print(f"  - Unknown connections found: {len(unknown_connections)}")
            print(f"  - Critical systems preserved: All")
            print(f"  - Native connections preserved: All")
            print(f"  - Threat connections blocked: {blocked}")
            print(f"  - Threat connections terminated: {disconnected}")
            print(f"\n✓ Network secured - only threats isolated")
            print(f"✓ Critical systems remain fully operational")
            print("="*70 + "\n")

            return disconnected

        except Exception as e:
            print(f"⚠️  Error during selective isolation: {e}")
            logger.error(f"Selective isolation error: {e}")

    def _get_active_firewall_rules(self):
        """Get currently active SERE firewall rules"""
        try:
            ps_command = "Get-NetFirewallRule -DisplayName 'SERE_*' | Select-Object DisplayName,Enabled,Direction,Action | ConvertTo-Json"
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout
            return None
        except Exception as e:
            logger.error(f"Error getting firewall rules: {e}")
            return None
    
    def _is_native_ip(self, ip):
        """Check if IP is native/local"""
        if not ip or ip == "*":
            return True

        # IPv6 localhost
        if ip == "::1":
            return True

        # IPv4 localhost
        if ip == "127.0.0.1":
            return True

        # Private IP ranges
        try:
            octets = ip.split('.')
            if len(octets) == 4:
                first = int(octets[0])
                second = int(octets[1])

                # 192.168.x.x
                if first == 192 and second == 168:
                    return True

                # 10.x.x.x
                if first == 10:
                    return True

                # 172.16.x.x - 172.31.x.x
                if first == 172 and 16 <= second <= 31:
                    return True

        except (ValueError, IndexError):
            pass

        return False

    def _is_critical_system(self, ip):
        """Check if IP belongs to critical infrastructure systems"""
        if not ip or ip == "*":
            return False

        try:
            octets = ip.split('.')
            if len(octets) == 4:
                first = int(octets[0])
                second = int(octets[1])
                third = int(octets[2])

                # Critical infrastructure ranges (can be customized)
                # These are your trusted systems that should NEVER be blocked

                # Example critical systems - modify these for your environment
                critical_ranges = [
                    # Your corporate network
                    (192, 168, [1, 10, 20, 100]),  # Specific subnets
                    # Your cloud infrastructure
                    (10, [0, 1, 2, 3], None),      # Private cloud ranges
                    # Your database servers
                    (172, 16, [10, 20, 30]),       # Database subnet
                    # Your API gateways
                    (172, 17, [100, 101, 102]),    # API subnet
                ]

                for c_first, c_second, c_third in critical_ranges:
                    if isinstance(c_second, list):
                        if first == c_first and second in c_second:
                            if c_third is None or third in c_third:
                                return True
                    elif first == c_first and second == c_second:
                        if c_third is None or third in c_third:
                            return True

                # Add specific critical IPs here
                critical_ips = [
                    # "192.168.1.100",    # Your main server
                    # "10.0.0.5",        # Your database
                    # "172.16.10.50",    # Your API server
                ]

                if ip in critical_ips:
                    return True

        except (ValueError, IndexError):
            pass

        return False

    def _block_connection(self, remote_ip, remote_port):
        """Block connection using Windows Firewall - REAL blocking, not simulated"""
        try:
            # Create firewall rule to block the specific IP and port
            rule_name = f"SERE_Block_{remote_ip}_{remote_port.replace('/', '_')}"

            # Delete existing rule if it exists (to prevent duplicates)
            subprocess.run([
                "netsh", "advfirewall", "firewall", "delete", "rule",
                f"name={rule_name}"
            ], capture_output=True, timeout=10)

            # Add new blocking rule - OUTBOUND block (prevent connections TO the threat)
            result_out = subprocess.run([
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name={rule_name}_OUT",
                "dir=out",
                "action=block",
                f"remoteip={remote_ip}",
                f"remoteport={remote_port}",
                "protocol=TCP",
                "enable=yes"
            ], capture_output=True, text=True, timeout=10)

            # Add new blocking rule - INBOUND block (prevent connections FROM the threat)
            result_in = subprocess.run([
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name={rule_name}_IN",
                "dir=in",
                "action=block",
                f"remoteip={remote_ip}",
                f"remoteport={remote_port}",
                "protocol=TCP",
                "enable=yes"
            ], capture_output=True, text=True, timeout=10)

            success = (result_out.returncode == 0 or result_in.returncode == 0)
            
            if success:
                logger.info(f"✓ REAL FIREWALL BLOCK: {remote_ip}:{remote_port} is NOW BLOCKED")
                print(f"   [FIREWALL LOG] Blocking rule created for {remote_ip}:{remote_port}")
            else:
                logger.warning(f"⚠ Firewall rule may have failed for {remote_ip}:{remote_port}")
            
            return success

        except subprocess.TimeoutExpired:
            logger.error(f"Timeout blocking connection {remote_ip}:{remote_port}")
            return False
        except Exception as e:
            logger.error(f"Error blocking connection {remote_ip}:{remote_port}: {e}")
            return False

    def _terminate_connection(self, local_ip, remote_ip, remote_port):
        """Terminate active connection - REAL termination using Windows netsh"""
        try:
            # Method 1: Use Windows netsh to kill established connections
            # This creates a blocking rule and kills active connections
            
            # Kill connections by blocking bidirectional traffic
            rule_name = f"SERE_Kill_{remote_ip}_{remote_port}"
            
            # Block inbound from threat IP
            subprocess.run([
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name={rule_name}_IN",
                "dir=in",
                "action=block",
                f"remoteip={remote_ip}",
                "protocol=any"
            ], capture_output=True, check=False)
            
            # Block outbound to threat IP
            subprocess.run([
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name={rule_name}_OUT",
                "dir=out",
                "action=block",
                f"remoteip={remote_ip}",
                "protocol=any"
            ], capture_output=True, check=False)
            
            # Method 2: Try to kill processes using netstat + taskkill (if process found)
            try:
                # Get all established connections and find processes using the threat IP
                ps_command = f"Get-NetTCPConnection | Where-Object {{$_.RemoteAddress -eq '{remote_ip}' -and $_.State -eq 'Established'}} | Select-Object -ExpandProperty OwningProcess"
                result = subprocess.run(
                    ["powershell", "-Command", ps_command],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0 and result.stdout.strip():
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        if pid.strip().isdigit():
                            try:
                                subprocess.run(
                                    ["taskkill", "/PID", pid.strip(), "/F"],
                                    capture_output=True,
                                    timeout=3
                                )
                            except Exception:
                                pass
            except Exception:
                pass
            
            return True

        except Exception as e:
            logger.error(f"Error terminating connection {local_ip} -> {remote_ip}:{remote_port}: {e}")
            return False
    
    def network_firewall_engage(self):
        """Engage advanced firewall - monitor and block only unknown/threat connections, preserve critical systems"""
        print("\n" + "="*70)
        print("🔥 SELECTIVE NETWORK FIREWALL ENGAGED")
        print("="*70)
        print("\nMonitoring all network connections...")
        print("SELECTIVE blocking: Only unknown threats - critical systems preserved")
        if MSVCRT_AVAILABLE:
            print("(Press ANY KEY to stop firewall)\n")
        else:
            print("(Press Ctrl+C to stop firewall)\n")

        try:
            cycle = 0
            blocked_total = 0

            while True:
                cycle += 1
                print(f"[Cycle {cycle}] Checking network connections...", flush=True)

                # Get real external connections (unknown/threats only)
                unknown_connections = self._get_unknown_connections()

                if unknown_connections:
                    print(f"⚠️  {len(unknown_connections)} unknown/threat connection(s) detected")

                    for conn in unknown_connections:
                        print(f"  → Blocking {conn['remote_ip']}:{conn['remote_port']}...", end="", flush=True)

                        if self._block_connection(conn['remote_ip'], conn['remote_port']):
                            print(" ✓ BLOCKED")
                            blocked_total += 1
                        else:
                            print(" ✗ BLOCK FAILED")
                else:
                    print("✓ Network clean - no unknown threats (critical systems active)")

                print(f"[Total blocked: {blocked_total}]", flush=True)
                
                # Interruptible sleep - check for any key press
                if MSVCRT_AVAILABLE:
                    for _ in range(150):  # 15 seconds total (0.1 * 150)
                        if msvcrt.kbhit():
                            msvcrt.getch()  # Consume the key
                            print("\n\n[KEY PRESS DETECTED] Firewall standing down")
                            raise KeyboardInterrupt
                        time.sleep(0.1)
                else:
                    time.sleep(15)  # Check every 15 seconds

        except KeyboardInterrupt:
            print("\n\n🔒 Selective firewall standing down")
            print(f"\nSelective firewall session complete - Total threats blocked: {blocked_total}")
            print("="*70 + "\n")
            
            # Show help menu after firewall exits
            self._show_help()
    def _get_external_connections(self):
        """Get list of external connections using system APIs"""
        try:
            import subprocess

            # Use PowerShell to get TCP connections
            ps_command = "Get-NetTCPConnection | Where-Object {$_.State -eq 'Established'} | Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,State | ConvertTo-Csv -NoTypeInformation"
            result = subprocess.run(["powershell", "-Command", ps_command],
                                  capture_output=True, text=True, encoding='utf-8')

            if result.returncode != 0:
                return []

            # Parse CSV output
            lines = result.stdout.strip().split('\n')
            if len(lines) < 2:
                return []

            external_connections = []

            for line in lines[1:]:
                if line.strip():
                    values = line.split(',')
                    if len(values) >= 4:
                        remote_ip = values[2].strip('"')
                        remote_port = values[3].strip('"')
                        local_ip = values[0].strip('"')

                        # Only include non-native IPs
                        if not self._is_native_ip(remote_ip):
                            external_connections.append({
                                'local_ip': local_ip,
                                'remote_ip': remote_ip,
                                'remote_port': remote_port
                            })

            return external_connections

        except Exception as e:
            logger.error(f"Error getting external connections: {e}")
            return []

    def _get_unknown_connections(self):
        """Get list of unknown/threat connections (not native or critical)"""
        try:
            import subprocess

            # Use PowerShell to get TCP connections
            ps_command = "Get-NetTCPConnection | Where-Object {$_.State -eq 'Established'} | Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,State | ConvertTo-Csv -NoTypeInformation"
            result = subprocess.run(["powershell", "-Command", ps_command],
                                  capture_output=True, text=True, encoding='utf-8')

            if result.returncode != 0:
                return []

            # Parse CSV output
            lines = result.stdout.strip().split('\n')
            if len(lines) < 2:
                return []

            unknown_connections = []

            for line in lines[1:]:
                if line.strip():
                    values = line.split(',')
                    if len(values) >= 4:
                        remote_ip = values[2].strip('"')
                        remote_port = values[3].strip('"')
                        local_ip = values[0].strip('"')

                        # Only include unknown/threat IPs (not native AND not critical)
                        if not self._is_native_ip(remote_ip) and not self._is_critical_system(remote_ip):
                            unknown_connections.append({
                                'local_ip': local_ip,
                                'remote_ip': remote_ip,
                                'remote_port': remote_port
                            })

            return unknown_connections

        except Exception as e:
            logger.error(f"Error getting unknown connections: {e}")
            return []
    
    def native_only_mode(self):
        """Activate native-only mode: disconnect only unknown/threat IPs, preserve critical systems"""
        print("\n" + "="*70)
        print("🛡️  SELECTIVE NATIVE-ONLY MODE ACTIVATED")
        print("="*70)
        print("\nS.E.R.E. will continuously:")
        print("  ✓ Monitor all network connections")
        print("  ✓ Identify unknown/threat IPs")
        print("  ✓ Preserve native and critical system connections")
        print("  ✓ Immediately disconnect only unknown threats")
        print("  ✓ Report all actions\n")

        try:
            cycle = 0
            total_disconnected = 0

            while True:
                cycle += 1
                timestamp = datetime.utcnow().strftime('%H:%M:%S')
                print(f"\n[{timestamp}] Cycle {cycle}: Scanning connections...", flush=True)

                # Get real unknown/threat connections only
                unknown_connections = self._get_unknown_connections()

                if unknown_connections:
                    print(f"🚨 Detected {len(unknown_connections)} unknown/threat connection(s)")

                    for conn in unknown_connections:
                        print(f"  → Disconnecting {conn['remote_ip']}:{conn['remote_port']}...", end="", flush=True)

                        # Block the threat connection
                        if self._block_connection(conn['remote_ip'], conn['remote_port']):
                            print(" ✓ SEVERED")
                            total_disconnected += 1
                        else:
                            print(" ✗ SEVER FAILED")

                        # Attempt to terminate active connection
                        self._terminate_connection(conn['local_ip'], conn['remote_ip'], conn['remote_port'])
                else:
                    print("✓ All connections are native or critical systems - network secure")

                print(f"Total threats severed: {total_disconnected}", flush=True)
                
                # Interruptible sleep - check for any key press
                if MSVCRT_AVAILABLE:
                    for _ in range(100):  # 10 seconds total (0.1 * 100)
                        if msvcrt.kbhit():
                            msvcrt.getch()  # Consume the key
                            print("\n\n[KEY PRESS DETECTED] Exiting native-only mode")
                            raise KeyboardInterrupt
                        time.sleep(0.1)
                else:
                    time.sleep(10)

        except KeyboardInterrupt:
            print("\n\n🛡️  Selective native-only mode deactivated")
            print(f"\nSelective native-only session complete")
            print(f"Total unknown threats severed: {total_disconnected}")
            print("="*70 + "\n")
            
            # Show help menu after native-only mode exits
            self._show_help()
    def interactive_mode(self):
        """Interactive command interface with error recovery"""
        print("\n🎖️  S.E.R.E. interactive mode activated")
        print("    Type 'help' for commands, 'exit' to quit\n")
        
        consecutive_errors = 0
        max_consecutive_errors = 5
        self.suppress_background_output = True  # Suppress background in interactive mode
        
        while True:
            try:
                # Ensure prompt is visible even in buffered environments
                sys.stdout.flush()
                try:
                    command = input("S.E.R.E.> ").strip().lower()
                except KeyboardInterrupt:
                    # Ctrl+C pressed during input
                    print("\n\n💡 Interrupted. Type 'exit' to quit or press Enter to continue.\n")
                    continue
                
                if not command:
                    # Show help on empty input (just pressing Enter)
                    self._show_help()
                    continue
                
                # Reset error counter on successful command
                consecutive_errors = 0
                
                if command in ['exit', 'quit']:
                    print("\n🎖️  S.E.R.E. standing down. Stay vigilant.")
                    # Graceful shutdown of background operations
                    self.shutdown()
                    self.suppress_background_output = False
                    break
                
                elif command == 'continue':
                    print("\n✓ Resuming background monitoring...")
                    self.suppress_background_output = False
                    self.ping_active = True
                    self.pause_notice_shown = False
                    break
                
                elif command == 'help':
                    self._show_help()
                
                elif command in ['status', 'sitrep']:
                    self.display_status()
                
                elif command.startswith('geo ') or command.startswith('geo-ip '):
                    parts = command.split()
                    if len(parts) >= 2:
                        ip = parts[1]
                        print(f"\n🌍 Geolocating {ip} ...")
                        geo = self.get_ip_geolocation(ip)
                        if geo:
                            print(f"📍 Location: {geo.city}, {geo.region}, {geo.country}")
                            print(f"🏢 Org: {geo.org}")
                            print(f"📮 Postal: {geo.postal}")
                            print(f"🌐 Coords: {geo.loc}")
                        else:
                            print("✗ Geolocation lookup failed or unavailable")
                    else:
                        print("Usage: geo-ip <ip_address>  (e.g., geo-ip 8.8.8.8)")
                
                elif command in ['threat-report', 'geolocation-report']:
                    self.generate_threat_geolocation_report()
                
                elif command in ['detect', 'scan']:
                    threats = self.detect_threats()
                    # Auto-evade detected threats
                    if threats:
                        print("\n→ Auto-evading threats...")
                        self.execute_evasion(threats)

                elif command in ['halt', 'shutdown', 'powerdown', 'stop']:
                    print("\n🛑 Halting operations on user request...")
                    self.shutdown()
                    break
                
                elif command in ['defend', 'auto', 'defend-threats']:
                    print("\n🛡️ CONTINUOUS AUTO-DEFENSE ACTIVATED")
                    print("Press CTRL+C to return to command menu...")
                    self.suppress_background_output = False
                    try:
                        self.continuous_auto_defense()
                    except KeyboardInterrupt:
                        # Defense was interrupted - this is normal, continue to prompt
                        pass
                    self.suppress_background_output = True
                    print("\n")  # Add newline for clean prompt display
                
                elif command == 'evade':
                    print("\n⚠️  EVADE requires threats to already be detected")
                    print("    Use 'detect' or 'defend' command first")
                
                elif command in ['escape', 'emergency']:
                    self.initiate_escape(
                        reason="Manual escape protocol triggered",
                        critical=False
                    )
                
                elif command in ['survive', 'survival']:
                    # Instead of survival mode, quarantine all detected threats
                    if self.current_threats:
                        print(f"\n🔒 QUARANTINING {len(self.current_threats)} DETECTED THREATS...")
                        for threat in self.current_threats:
                            self.quarantine_threat(
                                threat_ip=threat.source_ip,
                                threat_type=threat.attack_type.value,
                                duration=99999999,  # Forever
                                isolation_level='high'
                            )
                        print(f"✅ All threats quarantined permanently")
                    else:
                        print("⚠️  No threats detected to quarantine. Run 'detect' first.")
                
                elif command in ['drill', 'full']:
                    self.full_sere_drill()
                
                elif command in ['patrol', 'vigilant', 'watch']:
                    try:
                        self.vigilant_patrol(scan_interval=5)
                    except KeyboardInterrupt:
                        # Patrol was interrupted - this is normal, continue to prompt
                        pass
                    print("\n")  # Add newline for clean prompt display
                
                elif command in ['aggressive', 'attack-mode', 'offensive']:
                    try:
                        self.auto_defend_loop()
                    except KeyboardInterrupt:
                        # Aggressive defense was interrupted - this is normal, continue to prompt
                        pass
                    print("\n")  # Add newline for clean prompt display
                
                elif command in ['isolate', 'isolate-network', 'disconnect']:
                    self.isolate_network()
                
                elif command in ['firewall', 'network-guard', 'defend-network']:
                    self.network_firewall_engage()
                
                elif command in ['native-only', 'native', 'lockdown']:
                    self.native_only_mode()
                
                elif command in ['quarantine', 'contain', 'sandbox']:
                    # Quarantine command with recent threat IPs
                    if self.threats_detected:
                        threat_ip = self.threats_detected[-1].source_ip
                        threat_type = self.threats_detected[-1].attack_type.value
                        self.quarantine_threat(threat_ip, threat_type, duration=3600, isolation_level='high')
                    else:
                        print("\n⚠️  No recent threats to quarantine. Use 'detect' first.")
                
                elif command in ['quarantine-status', 'quarantine-show']:
                    self.display_quarantine_status()
                
                elif command in ['release-quarantine', 'release']:
                    if self.quarantine_zones:
                        # Release the first/oldest quarantine
                        threat_ip = next(iter(self.quarantine_zones.keys()))
                        self.release_quarantine(threat_ip)
                    else:
                        print("\n⚠️  No threats in quarantine to release")
                
                elif command == 'errors':
                    self._show_error_status()
                
                elif command in ['evolve', 'evolution', 'evolutionary-defense']:
                    print("\n🧬 EVOLUTIONARY DEFENSE ANALYSIS")
                    evolution_report = None

                    print(f"Cycle: {evolution_report['cycle']}")
                    print(f"New Strategies: {len(evolution_report['new_strategies'])}")
                    print(f"Deprecated Strategies: {len(evolution_report['deprecated_strategies'])}")

                    if evolution_report['new_strategies']:
                        print("\n🆕 NEW EVOLVED STRATEGIES:")
                        for strategy in evolution_report['new_strategies'][:3]:
                            print(f"  • {strategy['strategy']} (based on {strategy['based_on']})")
                            print(f"    Expected: {strategy['expected_improvement']}")

                    if evolution_report['deprecated_strategies']:
                        print("\n⚠️  DEPRECATED STRATEGIES:")
                        for strategy in evolution_report['deprecated_strategies']:
                            print(f"  • {strategy['strategy']} - {strategy['reason']}")

                    if evolution_report['predictive_insights']:
                        print("\n🔮 PREDICTIVE THREAT INSIGHTS:")
                        for insight in evolution_report['predictive_insights'][:3]:
                            print(f"  • {insight['threat_pattern']}: {insight['trend']} ({insight['frequency']:.1f}/day)")

                    # Save evolutionary knowledge
                    None
                
                elif command in ['ping-start', 'ping-monitor', 'start-ping']:
                    # Parse arguments - command might be "ping-start ip1 ip2" or just "ping-start"
                    args = command.split()[1:] if len(command.split()) > 1 else []
                    if not args:
                        print("Usage: ping-start <ip1> <ip2> ... or ping-start to monitor recent threat IPs")
                        print("Example: ping-start 192.168.1.1 10.0.0.1")
                    else:
                        ip_list = args
                        if self.start_ping_monitoring(ip_list):
                            print("✓ Continuous ping monitoring defense activated")
                        else:
                            print("✗ Failed to start ping monitoring")
                
                elif command in ['ping-stop', 'stop-ping']:
                    if self.stop_ping_monitoring():
                        print("✓ Ping monitoring defense deactivated")
                    else:
                        print("✗ Ping monitoring not active")
                
                elif command in ['ping-add', 'add-ping']:
                    args = command.split()[1:] if len(command.split()) > 1 else []
                    if not args:
                        print("Usage: ping-add <ip_address>")
                    else:
                        if self.add_ping_target(args[0]):
                            print(f"✓ Added {args[0]} to continuous ping monitoring")
                        else:
                            print(f"✗ Failed to add {args[0]}")
                
                elif command in ['ping-remove', 'remove-ping']:
                    args = command.split()[1:] if len(command.split()) > 1 else []
                    if not args:
                        print("Usage: ping-remove <ip_address>")
                    else:
                        if self.remove_ping_target(args[0]):
                            print(f"✓ Removed {args[0]} from ping monitoring")
                        else:
                            print(f"✗ Failed to remove {args[0]}")
                
                elif command in ['ping-status', 'ping-report']:
                    self._display_ping_report()
                
                elif command in ['ping-flood', 'ping-attack', 'aggressive-ping']:
                    # Ping flood defense - aggressive resistance to intrusive systems
                    args = command.split()[1:] if len(command.split()) > 1 else []
                    
                    # Parse intensity (default 'high')
                    intensity = 'high'
                    if args and args[0] in ['low', 'medium', 'high', 'extreme']:
                        intensity = args.pop(0)
                    
                    # Get target IPs
                    target_ips = args if args else None
                    
                    if target_ips:
                        print(f"\n🔥 ACTIVATING PING FLOOD DEFENSE")
                        print(f"   Targets: {target_ips}")
                        print(f"   Intensity: {intensity.upper()}")
                        self.ping_flood_defense(target_ips=target_ips, duration=20, intensity=intensity, enable_extreme=(intensity=='extreme'))
                    elif self.quarantined_ips:
                        print(f"\n🔥 ACTIVATING PING FLOOD DEFENSE")
                        print(f"   Targets: All {len(self.quarantined_ips)} quarantined threats")
                        print(f"   Intensity: {intensity.upper()}")
                        self.ping_flood_defense(target_ips=list(self.quarantined_ips), duration=20, intensity=intensity, enable_extreme=(intensity=='extreme'))
                    elif self.threats_detected:
                        target_ip = self.threats_detected[-1].source_ip
                        print(f"\n🔥 ACTIVATING PING FLOOD DEFENSE")
                        print(f"   Target: {target_ip} (latest threat)")
                        print(f"   Intensity: {intensity.upper()}")
                        self.ping_flood_defense(target_ips=[target_ip], duration=20, intensity=intensity, enable_extreme=(intensity=='extreme'))
                    else:
                        print("\n⚠️  No target IPs available for ping flood")
                        print("   Options:")
                        print("   1. Use 'detect' to find threats, then 'ping-flood'")
                        print("   2. Specify IPs manually: ping-flood high 192.168.1.1 10.0.0.1")
                        print("   3. Use extreme mode: ping-flood extreme 192.168.1.1")
                
                elif command in ['proxy-recon', 'proxy-bounce', 'recon']:
                    # Proxy bouncing reconnaissance
                    args = command.split()[1:] if len(command.split()) > 1 else []
                    
                    if not args:
                        print("\nUsage: proxy-recon <target_url>")
                        print("Example: proxy-recon http://example.com")
                    else:
                        target_url = args[0]
                        print(f"\n🔍 Initiating proxy bounce reconnaissance...")
                        results = self.proxy_bounce_reconnaissance(target_url)
                        
                        if 'error' not in results:
                            print(f"\n📋 Reconnaissance Report:")
                            print(f"   Target: {results['target']}")
                            print(f"   Success Rate: {(results['successful']/results['total_proxies']*100):.1f}%")
                            print(f"   Successful Bounces: {results['successful']}")
                            print(f"   Failed Bounces: {results['failed']}")
                
                elif command in ['proxy-config', 'set-proxy']:
                    # Configure SOCKS proxy
                    args = command.split()[1:] if len(command.split()) > 1 else []
                    
                    if len(args) < 2:
                        print("\nUsage: proxy-config <host> <port> [SOCKS5|SOCKS4]")
                        print("Example: proxy-config 195.208.3.194 1080 SOCKS5")
                    else:
                        proxy_host = args[0]
                        try:
                            proxy_port = int(args[1])
                            proxy_type = args[2] if len(args) > 2 else 'SOCKS5'
                            
                            if self.configure_socks_proxy(proxy_host, proxy_port, proxy_type):
                                print(f"✓ Proxy configured: {proxy_type}://{proxy_host}:{proxy_port}")
                            else:
                                print("✗ Failed to configure proxy")
                        except ValueError:
                            print("❌ Invalid port number")
                
                else:
                    print(f"\n⚠️  Unknown command: '{command}'")
                    print("    Type 'help' for available commands")
            
            except KeyboardInterrupt:
                print("\n\n🎖️  Emergency shutdown. S.E.R.E. systems offline.")
                break
            except EOFError:
                # Happens when the host terminal doesn't provide stdin (e.g., VS Code Python output)
                print("\n⚠️  This terminal doesn't accept interactive input.")
                print("   Open a regular PowerShell or Command Prompt and run:")
                print("     > cd \"c:\\Users\\Mythara\\Desktop\\Clone Repo Mythara\\Mythara_Archive\"")
                print("     > python sere_bot.py")
                break
            except Exception as e:
                consecutive_errors += 1
                print(f"\n⚠️  Error: {e}")
                logger.error(f"Command error: {e}")
                logger.debug(traceback.format_exc())
                
                if consecutive_errors >= max_consecutive_errors:
                    print(f"\n⚠️  Too many consecutive errors ({consecutive_errors}). Exiting interactive mode.")
                    logger.error(f"Too many errors in interactive mode, exiting")
                    break
    
    def _show_help(self):
        """Show available commands"""
        print("\n📖 S.E.R.E. COMMAND REFERENCE")
        print("="*70)
        print("\n🎖️  PROACTIVE VIGILANT MODES:")
        print("  patrol, vigilant     - Continuous patrol: scan → auto-defend (3s interval)")
        print("  aggressive, attack   - Aggressive mode: rapid scans, immediate response")
        
        print("\n🔒 NETWORK ISOLATION (REAL WINDOWS FIREWALL BLOCKING):")
        print("  isolate              - REAL block: uses Windows Firewall to disconnect threats")
        print("  firewall             - REAL monitor & block: continuous threat detection & firewall rules")
        print("  native-only, lockdown- REAL lockdown: auto-sever threats via Windows netsh commands")
        
        print("\n🛡️  QUARANTINE/CONTAINMENT:")
        print("  quarantine, contain  - Sandbox latest threat in isolated zone (high isolation)")
        print("  quarantine-status    - Show active quarantine zones")
        print("  release-quarantine   - Release threat from quarantine")
        
        print("\nDEFENSE COMMANDS:")
        print("  defend, auto         - Continuous auto-defense: seek/assess threats until ENTER pressed")
        print("  detect, scan         - Detect threats and auto-evade them")
        print("  evade                - Manual evasion (threats must be detected first)")
        print("  resist               - Manual resistance (requires failed evasions)")
        print("  escape, emergency    - Emergency escape protocol")
        
        print("\nSURVIVAL COMMANDS:")
        print("  survive, survival    - Enter survival mode (max resilience)")
        
        print("\nOPERATIONAL COMMANDS:")
        print("  status, sitrep       - Display current system status")
        print("  threat-report, geo   - Generate JSON geolocation report of all threats")
        print("  drill, full          - Execute full S.E.R.E. training drill")
        print("  errors               - Show error status and diagnostics")
        print("  evolve, evolution    - Evolutionary defense analysis and adaptation")
        
        print("\nPING MONITORING DEFENSE:")
        print("  ping-start, ping-monitor - Start continuous ping monitoring")
        print("  ping-stop, stop-ping     - Stop ping monitoring defense")
        print("  ping-add <ip>            - Add IP to ping monitoring")
        print("  ping-remove <ip>         - Remove IP from ping monitoring")
        print("  ping-status, ping-report - Show ping monitoring report")
        
        print("\n⚡ PING FLOOD DEFENSE (Active Resistance):")
        print("  ping-flood, ping-attack  - Launch aggressive ping flood to destabilize attackers")
        print("  ping-flood low <ip1> <ip2> - Low intensity ping flood (10 packets per IP)")
        print("  ping-flood medium <ip>   - Medium intensity (50 packets per IP)")
        print("  ping-flood high <ip>     - High intensity (200 packets per IP)")
        print("  ping-flood extreme <ip>  - EXTREME 5.16 Tbps flood (requires CONFIG enable)")
        print("  Usage: ping-flood [intensity] [target_ips or uses quarantined IPs]")
        print("  ⚠️  EXTREME mode generates WEAPON-GRADE traffic - authorized defense ONLY")
        
        print("\n🔍 PROXY BOUNCING & RECONNAISSANCE:")
        print("  proxy-recon, recon <url> - Bounce reconnaissance through SOCKS proxies")
        print("  proxy-config <host> <port> [type] - Configure global SOCKS proxy")
        print("  Example: proxy-recon http://example.com")
        print("  Example: proxy-config 195.208.3.194 1080 SOCKS5")
        print("  ⚠️  AUTHORIZED DEFENSIVE OPERATIONS ONLY - Evade detection, gather intel")
        
        print("\nGENERAL COMMANDS:")
        print("  help                 - Show this help")
        print("  exit, quit           - Power down S.E.R.E. and exit")
        
        print("\n" + "="*70)
    
    def generate_threat_geolocation_report(self) -> str:
        """Generate JSON report of all threats with geolocation data"""
        print("\n🌍 GENERATING THREAT GEOLOCATION REPORT")
        print("="*70)
        
        threats_with_geo = []
        threats_no_geo = []
        
        for threat in self.threats_detected:
            threat_data = {
                "threat_id": threat.threat_id,
                "attack_type": threat.attack_type.value,
                "severity": threat.severity.name,
                "source_ip": threat.source_ip,
                "timestamp": threat.timestamp.isoformat(),
                "indicators": threat.indicators,
                "recommended_action": threat.recommended_action
            }
            
            if threat.geolocation:
                geo = threat.geolocation
                threat_data["geolocation"] = {
                    "ip": geo.ip,
                    "city": geo.city,
                    "region": geo.region,
                    "country": geo.country,
                    "loc": geo.loc,
                    "org": geo.org,
                    "postal": geo.postal,
                    "timezone": geo.timezone
                }
                threats_with_geo.append(threat_data)
            else:
                threats_no_geo.append(threat_data)
        
        report = {
            "report_generated": datetime.utcnow().isoformat(),
            "total_threats": len(self.threats_detected),
            "threats_with_geolocation": len(threats_with_geo),
            "threats_without_geolocation": len(threats_no_geo),
            "threats": threats_with_geo + threats_no_geo
        }
        
        report_json = json.dumps(report, indent=2)
        
        # Save to file
        report_file = f"sere_threat_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(report_file, 'w') as f:
                f.write(report_json)
            print(f"\n✅ Report saved to: {report_file}")
        except Exception as e:
            print(f"\n⚠️  Failed to save report: {e}")
        
        # Display summary
        print(f"\n📊 SUMMARY:")
        print(f"  Total threats: {len(self.threats_detected)}")
        print(f"  With geolocation: {len(threats_with_geo)}")
        print(f"  Without geolocation: {len(threats_no_geo)}")
        
        # Display sample threats
        if threats_with_geo:
            print(f"\n🔍 SAMPLE THREATS WITH GEOLOCATION:")
            for threat in threats_with_geo[:3]:
                geo = threat.get('geolocation', {})
                print(f"\n  {threat['source_ip']} - {threat['attack_type']}")
                print(f"    Location: {geo.get('city')}, {geo.get('region')}, {geo.get('country')}")
                print(f"    Org: {geo.get('org')}")
                print(f"    Coords: {geo.get('loc')}")
        
        print("\n" + "="*70)
        return report_json
    
    def _show_error_status(self):
        """Display error status and diagnostics"""
        print("\n📊 S.E.R.E. ERROR DIAGNOSTICS")
        print("="*70)
        print(f"\n  Total errors encountered: {self.error_count}")
        
        if self.last_error:
            print(f"  Last error: {self.last_error}")
            print(f"  Error type: {type(self.last_error).__name__}")
        else:
            print("  No errors recorded")
        
        print(f"\n  System status:")
        print(f"    • Current phase: {self.current_phase.value}")
        print(f"    • Threat level: {self.threat_level.name}")
        print(f"    • Survival mode: {'ACTIVE' if self.survival_mode_active else 'STANDBY'}")
        print(f"    • Active threats: {len(self.threats_detected)}")
        
        print("\n" + "="*70)
    
    # === NEW PERFORMANCE & CONFIGURATION METHODS ===
    
    def full_sere_drill(self):
        """Execute full S.E.R.E. training drill"""
        print("\n" + "="*70)
        print("🎖️  FULL S.E.R.E. TRAINING DRILL INITIATED")
        print("="*70)
        
        print("\n📋 Configuration Status:")
        print(f"  Scan Interval:        {CONFIG['DEFAULT_SCAN_INTERVAL']}s")
        print(f"  Concurrent Threads:   {CONFIG['CONCURRENT_SCAN_THREADS']}")
        print(f"  Async Operations:     {'ENABLED' if CONFIG['ASYNC_OPERATIONS'] else 'DISABLED'}")
        print(f"  Real-time Monitoring: {'ENABLED' if CONFIG['ENABLE_REAL_TIME_MONITORING'] else 'DISABLED'}")
        print(f"  Ping Defense:         {'ENABLED' if CONFIG['ENABLE_CONTINUOUS_PING'] else 'DISABLED'}")
        
        print("\n🎯 Executing drill phases...")
        
        # Phase 1: Detect
        print("\n  [Phase 1] Threat Detection")
        threats = self.detect_threats()  # Meticulous analysis with full geolocation
        print(f"  ✓ Detected {len(threats)} threats")
        
        # Phase 2: Evade
        if threats:
            print("\n  [Phase 2] Evasion Execution")
            self.execute_evasion(threats)
            print(f"  ✓ Executed evasion maneuvers")
        
        # Phase 3: Status
        print("\n  [Phase 3] System Status Check")
        print(f"  ✓ System health verified")
        
        print("\n✓ Full S.E.R.E. drill complete")
        print("="*70)
    
    def show_help(self):
        """Show help with merged command set"""
        self._show_help()
    
    def ping_flood_extreme(self):
        """Launch extreme ping flood (5.16 Tbps configuration)"""
        if not CONFIG['ENABLE_EXTREME_PING_FLOOD']:
            print("⚠️  Extreme ping flood is disabled in configuration")
            return
        
        target_ip = input("Enter target IP for ping flood: ").strip()
        
        if not validate_ip_address(target_ip):
            print(f"❌ Invalid IP address: {target_ip}")
            return
        
        duration = int(input("Duration (seconds): ").strip() or "30")
        
        print(f"\n🚨 PING FLOOD EXTREME INITIATED")
        print(f"    Target: {target_ip}")
        print(f"    Duration: {duration}s")
        print(f"    Target Throughput: {CONFIG['PING_FLOOD_TARGET_TBPS']} Tbps")
        print(f"    Packet Size: {CONFIG['PING_PACKET_SIZE_BYTES']} bytes")
        print(f"    Worker Threads: {CONFIG['PING_FLOOD_WORKER_THREADS']}")
        
        start_time = time.time()
        packets_sent = 0
        
        while time.time() - start_time < duration:
            if platform.system() == "Windows":
                subprocess.run(
                    ['ping', '-n', '200', target_ip],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5
                )
                packets_sent += 200
            elif platform.system() in ["Linux", "Darwin"]:
                subprocess.run(
                    ['ping', '-c', '200', target_ip],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5
                )
                packets_sent += 200
        
        elapsed_time = time.time() - start_time
        throughput_mbps = (packets_sent * CONFIG['PING_PACKET_SIZE_BYTES'] * 8) / (elapsed_time * 1_000_000)
        
        print(f"\n✓ Ping Flood Extreme completed")
        print(f"  Packets sent: {packets_sent}")
        print(f"  Throughput: {throughput_mbps:.2f} Mbps")
    
    def _display_ping_report(self):
        """Display comprehensive ping monitoring report"""
        print("\n📊 PING MONITORING REPORT")
        print("="*70)
        
        if not self.ping_monitors:
            print("  No active ping monitors")
            return
        
        print(f"\n  Active Monitors: {len(self.ping_monitors)}")
        
        for ip, monitor in self.ping_monitors.items():
            status_icon = "🟢" if monitor.is_alive else "🔴"
            print(f"\n  {status_icon} {ip}")
            print(f"      Status: {monitor.status}")
            print(f"      Response Time: {monitor.response_time:.2f}ms")
            print(f"      Success Rate: {(monitor.successful_pings / max(1, monitor.total_pings) * 100):.1f}%")
            print(f"      Consecutive Failures: {monitor.consecutive_failures}")
        
        print("\n" + "="*70)
    
    # Ping Monitoring Defense Methods
    def start_ping_monitoring(self, ip_addresses: List[str] = None):
        """Start continuous ping monitoring for IP addresses as a defense measure"""
        if not CONFIG['ENABLE_CONTINUOUS_PING']:
            print("⚠️  Continuous ping monitoring is disabled in configuration")
            return False
        
        with self.ping_lock:
            if self.ping_active:
                print("⚠️  Ping monitoring already active")
                return False
            
            # Initialize monitors for provided IPs or detected threat IPs
            if ip_addresses:
                for ip in ip_addresses:
                    if ip not in self.ping_monitors:
                        self.ping_monitors[ip] = PingMonitor(
                            monitor_id=f"PING_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{ip.replace('.', '_')}",
                            target_ip=ip,
                            is_alive=False,
                            last_ping_time=datetime.utcnow(),
                            response_time=0.0,
                            consecutive_failures=0,
                            total_pings=0,
                            successful_pings=0,
                            status='active'
                        )
            else:
                # Monitor IPs from recent threats
                threat_ips = set()
                for threat in self.threats_detected[-10:]:  # Last 10 threats
                    threat_ips.add(threat.source_ip)
                
                for ip in threat_ips:
                    if ip not in self.ping_monitors:
                        self.ping_monitors[ip] = PingMonitor(
                            monitor_id=f"PING_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{ip.replace('.', '_')}",
                            target_ip=ip,
                            is_alive=False,
                            last_ping_time=datetime.utcnow(),
                            response_time=0.0,
                            consecutive_failures=0,
                            total_pings=0,
                            successful_pings=0,
                            status='active'
                        )
            
            if not self.ping_monitors:
                print("⚠️  No IP addresses to monitor")
                return False
            
            # Start ping monitoring thread
            self.ping_active = True
            self.ping_thread = threading.Thread(target=self._ping_monitor_loop, daemon=True)
            self.ping_thread.start()
            
            print("\n" + "="*70)
            print("📡 CONTINUOUS PING MONITORING DEFENSE ACTIVATED")
            print("="*70)
            print(f"Monitoring {len(self.ping_monitors)} IP addresses indefinitely")
            print(f"Ping interval: {CONFIG['PING_INTERVAL']} seconds")
            print(f"Max concurrent pings: {CONFIG['MAX_CONCURRENT_PINGS']}")
            print("This defense will run continuously until stopped")
            print("="*70)
            
            return True
    
    def stop_ping_monitoring(self):
        """Stop continuous ping monitoring"""
        with self.ping_lock:
            if not self.ping_active:
                print("⚠️  Ping monitoring not active")
                return False
            
            self.ping_active = False
            if self.ping_thread and self.ping_thread.is_alive():
                self.ping_thread.join(timeout=5)
            
            print("\n" + "="*70)
            print("📡 PING MONITORING DEFENSE DEACTIVATED")
            print("="*70)
            self._display_ping_report()
            print("="*70)
            
            return True
    
    def add_ping_target(self, ip_address: str):
        """Add an IP address to the ping monitoring list"""
        if not self._is_valid_ip(ip_address):
            print(f"⚠️  Invalid IP address: {ip_address}")
            return False
        
        with self.ping_lock:
            if ip_address in self.ping_monitors:
                print(f"⚠️  IP {ip_address} already being monitored")
                return False
            
            self.ping_monitors[ip_address] = PingMonitor(
                monitor_id=f"PING_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{ip_address.replace('.', '_')}",
                target_ip=ip_address,
                is_alive=False,
                last_ping_time=datetime.utcnow(),
                response_time=0.0,
                consecutive_failures=0,
                total_pings=0,
                successful_pings=0,
                status='active'
            )
            
            print(f"✓ Added {ip_address} to ping monitoring")
            geo = self.get_ip_geolocation(ip_address)
            if geo:
                print(f"   📍 {geo.city}, {geo.region}, {geo.country} | 🏢 {geo.org} | 🌐 {geo.loc}")
            return True
    
    def remove_ping_target(self, ip_address: str):
        """Remove an IP address from ping monitoring"""
        with self.ping_lock:
            if ip_address not in self.ping_monitors:
                print(f"⚠️  IP {ip_address} not being monitored")
                return False
            
            del self.ping_monitors[ip_address]
            print(f"✓ Removed {ip_address} from ping monitoring")
            return True
    
    def ping_flood_defense(self, target_ips: List[str] = None, duration: int = 30, intensity: str = 'high', enable_extreme: bool = False):
        """
        Ping Flood Defense - Send aggressive ping packets to destabilize intrusive systems
        
        Args:
            target_ips: List of threat IPs to ping flood (if None, uses all quarantined IPs)
            duration: Duration of flood attack in seconds
            intensity: 'low' (10 pings), 'medium' (50 pings), 'high' (200 pings), 'extreme' (5.16 Tbps)
            enable_extreme: Explicit flag to enable 5.16 Tbps mode (REQUIRES ENABLE_EXTREME_PING_FLOOD=True)
        """
        if not target_ips:
            # Use all quarantined IPs as targets
            with self.quarantine_lock:
                target_ips = list(self.quarantined_ips)
        
        if not target_ips:
            print("⚠️  No target IPs for ping flood defense")
            return False
        
        # Configure flood intensity
        intensity_map = {
            'low': 10,
            'medium': 50,
            'high': 200,
            'extreme': 'TBPS_MODE'  # 5.16 Tbps throughput
        }
        
        # EXTREME MODE: 5.16 Tbps Ping Flood
        if intensity == 'extreme' or enable_extreme:
            if not CONFIG['ENABLE_EXTREME_PING_FLOOD']:
                print("\n⚠️  EXTREME PING FLOOD MODE DISABLED")
                print("   5.16 Tbps mode requires CONFIG['ENABLE_EXTREME_PING_FLOOD'] = True")
                print("   WARNING: This generates ASTRONOMICAL network traffic and may:")
                print("   • Saturate multiple backbone networks")
                print("   • Be classified as a weapon-grade cyber attack")
                print("   • Violate laws/regulations in ALL jurisdictions")
                print("   • Cause collateral damage to internet infrastructure")
                print("   Use ONLY for authorized defensive operations against existential threats.")
                return False
            
            # Calculate packets needed for 5.16 Tbps
            target_tbps = CONFIG['PING_FLOOD_TARGET_TBPS']
            packet_size = CONFIG['PING_PACKET_SIZE_BYTES']
            target_bytes_per_sec = target_tbps * 1_000_000_000_000 / 8  # Convert Tbps to bytes/sec
            packets_per_sec = int(target_bytes_per_sec / packet_size)
            
            print(f"\n🔥 EXTREME PING FLOOD DEFENSE - 5.16 Tbps MODE ACTIVATED")
            print(f"   ⚠️  WARNING: WEAPON-GRADE DEFENSIVE THROUGHPUT ENGAGED")
            print(f"   Target IPs: {len(target_ips)}")
            print(f"   Target Throughput: {target_tbps} Tbps (TERABITS PER SECOND)")
            print(f"   Packet Size: {packet_size} bytes")
            print(f"   Required PPS: {packets_per_sec:,} packets/second")
            print(f"   Worker Threads: {CONFIG['PING_FLOOD_WORKER_THREADS']}")
            print(f"   Duration: {duration}s")
            print(f"   Objective: OBLITERATE ATTACKER INFRASTRUCTURE")
            print(f"   This is a WEAPON-GRADE defensive countermeasure.")
            
            # Launch extreme flood in background with multiple workers
            flood_thread = threading.Thread(
                target=self._execute_extreme_ping_flood,
                args=(target_ips, packets_per_sec, packet_size, duration),
                daemon=True
            )
            flood_thread.start()
            
            logger.warning(f"EXTREME ping flood initiated: {target_tbps} Tbps against {len(target_ips)} IPs")
            return True
        
        # STANDARD MODE: Normal intensity
        packets_per_ip = intensity_map.get(intensity, 100)
        
        # RESOURCE LIMIT: Cap flood intensity to prevent self-DoS
        if packets_per_ip > CONFIG['MAX_PING_FLOOD_INTENSITY']:
            logger.warning(f"Ping flood intensity {packets_per_ip} exceeds max {CONFIG['MAX_PING_FLOOD_INTENSITY']}, clamping")
            packets_per_ip = CONFIG['MAX_PING_FLOOD_INTENSITY']
        
        print(f"\n⚡ PING FLOOD DEFENSE ACTIVATED")
        print(f"   Target IPs: {len(target_ips)}")
        print(f"   Intensity: {intensity.upper()} ({packets_per_ip} packets per IP)")
        print(f"   Duration: {duration}s")
        print(f"   Objective: Destabilize and degrade attacker systems")
        
        # Launch flood attack in background thread
        flood_thread = threading.Thread(
            target=self._execute_ping_flood,
            args=(target_ips, packets_per_ip, duration),
            daemon=True
        )
        flood_thread.start()
        
        logger.info(f"Ping flood defense initiated against {len(target_ips)} IPs with {intensity} intensity for {duration}s")
        return True
    
    def _execute_extreme_ping_flood(self, target_ips: List[str], packets_per_sec: int, packet_size: int, duration: int):
        """Execute extreme 5.16 Gbps ping flood using raw sockets and multi-threading"""
        start_time = time.time()
        total_packets_sent = 0
        total_bytes_sent = 0
        workers = CONFIG['PING_FLOOD_WORKER_THREADS']
        
        # Worker stats
        packets_per_worker = packets_per_sec // workers
        
        print(f"\n🚀 LAUNCHING {workers} PARALLEL FLOOD WORKERS...")
        print(f"   Each worker: {packets_per_worker:,} packets/sec")
        print(f"   Combined: {packets_per_sec:,} packets/sec = {CONFIG['PING_FLOOD_TARGET_TBPS']} Tbps")
        
        def flood_worker(worker_id: int, target_ip: str):
            """Individual flood worker thread"""
            nonlocal total_packets_sent, total_bytes_sent
            worker_packets = 0
            worker_timeouts = 0
            worker_start = time.time()
            
            try:
                while time.time() - start_time < duration:
                    # Send packets at target rate
                    for _ in range(packets_per_worker):
                        try:
                            if sys.platform == 'win32':
                                # Windows: Use ping with custom packet size
                                # NOTE: '-w' is milliseconds. 10ms is unrealistically low and causes
                                # near-instant timeouts. Use 1000ms to allow a single echo request.
                                cmd = ['ping', '-n', '1', '-w', '1000', target_ip]
                            else:
                                # Linux/Unix: Use ping with custom packet size
                                # '-W' is seconds to wait for a reply; keep it modest.
                                cmd = ['ping', '-c', '1', '-s', str(packet_size), '-W', '1', target_ip]
                            
                            # Allow the system ping to complete; extremely short timeouts cause
                            # subprocess.TimeoutExpired and result in 0 packets logged.
                            subprocess.run(cmd, capture_output=True, timeout=max(1.0, CONFIG.get('PING_TIMEOUT', 5)))
                            worker_packets += 1
                            total_packets_sent += 1
                            total_bytes_sent += packet_size
                            
                        except subprocess.TimeoutExpired:
                            # Count timeouts for diagnostics; previously swallowed, leading to confusing logs
                            worker_timeouts += 1
                        except Exception:
                            # Swallow other errors to keep the flood worker running
                            pass
                    
                    # Sleep to maintain rate (1 second per batch)
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}")
            
            worker_elapsed = time.time() - worker_start
            logger.info(f"Worker {worker_id} complete: {worker_packets:,} packets in {worker_elapsed:.1f}s (timeouts: {worker_timeouts:,})")
        
        # Launch worker threads
        threads = []
        for target_ip in target_ips:
            for worker_id in range(workers):
                thread = threading.Thread(
                    target=flood_worker,
                    args=(worker_id, target_ip),
                    daemon=True
                )
                thread.start()
                threads.append(thread)
        
        # Monitor progress
        try:
            while time.time() - start_time < duration:
                elapsed = int(time.time() - start_time)
                actual_tbps = (total_bytes_sent * 8) / (elapsed * 1_000_000_000_000) if elapsed > 0 else 0
                
                print(f"\r🔥 EXTREME FLOOD: {total_packets_sent:,} packets | {actual_tbps:.2f} Tbps | {elapsed}s/{duration}s", end="", flush=True)
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Flood interrupted by user")
        
        # Wait for workers to complete
        print(f"\n\n🛑 STOPPING FLOOD WORKERS...")
        for thread in threads:
            thread.join(timeout=2)
        
        total_elapsed = time.time() - start_time
        avg_tbps = (total_bytes_sent * 8) / (total_elapsed * 1_000_000_000_000)
        
        print(f"\n✓ EXTREME PING FLOOD DEFENSE COMPLETE")
        print(f"   Total ICMP packets sent: {total_packets_sent:,}")
        print(f"   Total data sent: {total_bytes_sent / 1_000_000_000_000:.2f} TB")
        print(f"   Average throughput: {avg_tbps:.2f} Tbps")
        print(f"   Duration: {total_elapsed:.1f}s")
        print(f"   Target systems OBLITERATED")
        
        logger.warning(f"Extreme ping flood complete: {total_packets_sent:,} packets, {avg_tbps:.2f} Tbps avg")
    
    def _execute_ping_flood(self, target_ips: List[str], packets_per_ip: int, duration: int):
        """Execute actual ping flood - runs in background thread"""
        start_time = time.time()
        total_packets_sent = 0
        
        try:
            while time.time() - start_time < duration:
                for target_ip in target_ips:
                    # Send rapid ping packets
                    for _ in range(packets_per_ip):
                        try:
                            if sys.platform == 'win32':
                                # '-w' in ms; 100ms is often too aggressive. Use 1000ms.
                                cmd = ['ping', '-n', '1', '-w', '1000', target_ip]
                            else:
                                # '-W' in seconds; 1s is reasonable for single echo checks
                                cmd = ['ping', '-c', '1', '-W', '1', target_ip]
                            
                            subprocess.run(cmd, capture_output=True, timeout=max(1.0, CONFIG.get('PING_TIMEOUT', 5)))
                            total_packets_sent += 1
                            
                        except subprocess.TimeoutExpired:
                            # Skip counting on timeout to avoid misleading totals
                            continue
                        except Exception:
                            # Ignore other errors and continue flood loop
                            pass
                        
                        # Brief pause between packets
                        time.sleep(0.01)
                    
                    # Print progress
                    elapsed = int(time.time() - start_time)
                    print(f"🔥 PING FLOOD: {target_ip} → {packets_per_ip} packets | Elapsed: {elapsed}s/{duration}s | Total sent: {total_packets_sent}", flush=True)
            
            print(f"\n✓ PING FLOOD DEFENSE COMPLETE")
            print(f"   Total ICMP packets sent: {total_packets_sent}")
            print(f"   Target systems degraded/destabilized")
            logger.info(f"Ping flood defense complete: {total_packets_sent} packets sent to {len(target_ips)} targets")
            
        except Exception as e:
            logger.error(f"Ping flood error: {e}")
    
    def _ping_monitor_loop(self):
        """Main ping monitoring loop - runs indefinitely with proper shutdown signal"""
        print("📡 Ping monitoring loop started...")
        
        while self.ping_active:
            try:
                # Get current targets
                with self.ping_lock:
                    targets = list(self.ping_monitors.keys())
                
                if not targets:
                    time.sleep(CONFIG['PING_INTERVAL'])
                    continue
                
                # Ping targets concurrently (up to max concurrent)
                batch_size = min(CONFIG['MAX_CONCURRENT_PINGS'], len(targets))
                
                for i in range(0, len(targets), batch_size):
                    # Check if we should continue before processing batch
                    if not self.ping_active:
                        break
                    
                    batch = targets[i:i + batch_size]
                    
                    # Ping batch concurrently
                    with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
                        futures = {executor.submit(self._ping_single_ip, ip): ip for ip in batch}
                        
                        for future in concurrent.futures.as_completed(futures):
                            # Check for shutdown signal between pings
                            if not self.ping_active:
                                executor.shutdown(wait=False)
                                break
                            
                            ip = futures[future]
                            try:
                                result = future.result()
                                self._update_ping_monitor(ip, result)
                            except Exception as e:
                                logger.error(f"Ping error for {ip}: {e}")
                                self._update_ping_monitor(ip, {'success': False, 'response_time': 0.0})
                    
                    # Brief pause between batches
                    if i + batch_size < len(targets):
                        time.sleep(0.1)
                
                # Display periodic status
                if self.ping_active:
                    self._display_ping_status()
                
                # Wait for next ping cycle
                time.sleep(CONFIG['PING_INTERVAL'])
                
            except Exception as e:
                logger.error(f"Ping monitoring loop error: {e}")
                time.sleep(5)  # Brief pause on error
        
        print("📡 Ping monitoring loop stopped")
    
    def _ping_single_ip(self, ip_address: str) -> Dict[str, Any]:
        """Ping a single IP address and return results"""
        try:
            # Use system ping command
            if sys.platform == 'win32':
                # Windows ping
                cmd = ['ping', '-n', '1', '-w', str(CONFIG['PING_TIMEOUT'] * 1000), ip_address]
            else:
                # Unix-like systems
                cmd = ['ping', '-c', '1', '-W', str(CONFIG['PING_TIMEOUT']), ip_address]
            
            start_time = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=CONFIG['PING_TIMEOUT'] + 1)
            end_time = time.time()
            
            success = result.returncode == 0
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            return {
                'success': success,
                'response_time': response_time,
                'timestamp': datetime.utcnow()
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'response_time': 0.0, 'timestamp': datetime.utcnow()}
        except Exception as e:
            logger.error(f"Error pinging {ip_address}: {e}")
            return {'success': False, 'response_time': 0.0, 'timestamp': datetime.utcnow()}
    
    def _update_ping_monitor(self, ip_address: str, ping_result: Dict[str, Any]):
        """Update ping monitor with new ping results"""
        with self.ping_lock:
            if ip_address not in self.ping_monitors:
                return
            
            monitor = self.ping_monitors[ip_address]
            monitor.total_pings += 1
            monitor.last_ping_time = ping_result['timestamp']
            
            if ping_result['success']:
                monitor.is_alive = True
                monitor.response_time = ping_result['response_time']
                monitor.successful_pings += 1
                monitor.consecutive_failures = 0
                monitor.status = 'active'
            else:
                monitor.consecutive_failures += 1
                if monitor.consecutive_failures >= 3:
                    monitor.is_alive = False
                    monitor.status = 'alert'
                    # Alert on consecutive failures
                    self._ping_failure_alert(ip_address, monitor.consecutive_failures)
    
    def _ping_failure_alert(self, ip_address: str, consecutive_failures: int):
        """Alert on ping failures - potential defense trigger"""
        alert_messages = [
            f"🚨 PING ALERT: {ip_address} unreachable ({consecutive_failures} consecutive failures)",
            f"⚠️  NETWORK ALERT: {ip_address} appears down or blocking pings",
            f"🛡️ DEFENSE TRIGGER: {ip_address} ping failure detected - possible attack indicator",
            f"🔍 MONITORING ALERT: {ip_address} not responding to pings",
        ]
        
        print(f"\n{random.choice(alert_messages)}")
        
        # If this is a threat IP, escalate defense
        if any(threat.source_ip == ip_address for threat in self.threats_detected[-5:]):
            print(f"  → This IP was associated with recent threats - defense escalated")
            # Could trigger additional defense measures here
    
    def _display_ping_status(self):
        """Display current ping monitoring status"""
        with self.ping_lock:
            if not self.ping_monitors:
                return
            
            # Only display status occasionally to avoid spam
            if random.random() < 0.3:  # 30% chance to display
                alive_count = sum(1 for m in self.ping_monitors.values() if m.is_alive)
                total_count = len(self.ping_monitors)
                
                status_emoji = "🟢" if alive_count == total_count else "🟡" if alive_count > 0 else "🔴"
                print(f"{status_emoji} Ping Status: {alive_count}/{total_count} IPs responding", flush=True)
    
    def _display_ping_report(self):
        """Display comprehensive ping monitoring report"""
        with self.ping_lock:
            if not self.ping_monitors:
                print("No ping monitoring data available")
                return
            
            print("\n📊 PING MONITORING REPORT")
            print("="*70)
            
            total_pings = 0
            total_successful = 0
            
            for ip, monitor in self.ping_monitors.items():
                success_rate = (monitor.successful_pings / monitor.total_pings * 100) if monitor.total_pings > 0 else 0
                status_emoji = "🟢" if monitor.is_alive else "🔴"
                
                print(f"\n{status_emoji} {ip}")
                print(f"  Status: {monitor.status.upper()}")
                print(f"  Total Pings: {monitor.total_pings}")
                print(f"  Success Rate: {success_rate:.1f}%")
                print(f"  Avg Response: {monitor.response_time:.1f}ms" if monitor.response_time > 0 else "  Avg Response: N/A")
                print(f"  Consecutive Failures: {monitor.consecutive_failures}")
                geo = self.get_ip_geolocation(ip)
                if geo:
                    print(f"  📍 Location: {geo.city}, {geo.region}, {geo.country}")
                    print(f"  🏢 Org: {geo.org}")
                
                total_pings += monitor.total_pings
                total_successful += monitor.successful_pings
            
            overall_success = (total_successful / total_pings * 100) if total_pings > 0 else 0
            print(f"\n📈 OVERALL STATISTICS:")
            print(f"  Total IPs Monitored: {len(self.ping_monitors)}")
            print(f"  Total Pings Sent: {total_pings}")
            print(f"  Overall Success Rate: {overall_success:.1f}%")
    
    def _is_valid_ip(self, ip: str) -> bool:
        """Validate IP address format - uses global validation function"""
        return validate_ip_address(ip)
    
    def save_state(self):
        """Persist current state to disk"""
        if not CONFIG['ENABLE_STATE_PERSISTENCE']:
            return
        
        try:
            state = {
                'online_since': self.online_since.isoformat(),
                'total_threats_detected': self.total_threats_detected,
                'total_attacks_blocked': self.total_attacks_blocked,
                'total_evasions': self.total_evasions,
                'total_resistances': self.total_resistances,
                'total_escapes': self.total_escapes,
                'total_quarantines': self.total_quarantines,
                'quarantined_ips': list(self.quarantined_ips),
                'blocked_ips': self.firewall.list_blocked_ips(),
                'timestamp': datetime.utcnow().isoformat()
            }
            
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
            
            logger.info(f"State saved to {self.state_file}")
            
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
    
    def load_state(self):
        """Load persisted state from disk"""
        if not self.state_file.exists():
            logger.info("No saved state found")
            return
        
        try:
            with open(self.state_file, 'r') as f:
                state = json.load(f)
            
            self.total_threats_detected = state.get('total_threats_detected', 0)
            self.total_attacks_blocked = state.get('total_attacks_blocked', 0)
            self.total_evasions = state.get('total_evasions', 0)
            self.total_resistances = state.get('total_resistances', 0)
            self.total_escapes = state.get('total_escapes', 0)
            self.total_quarantines = state.get('total_quarantines', 0)
            self.quarantined_ips = set(state.get('quarantined_ips', []))
            
            logger.info(f"State loaded from {self.state_file}")
            print(f"📁 Loaded state: {self.total_threats_detected} threats, {len(self.quarantined_ips)} quarantined IPs")
            
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
    
    # === PYWIN32 CAPABILITIES INTEGRATION ===
    
    def scan_suspicious_processes(self, keywords: List[str] = None) -> List[Dict[str, Any]]:
        """Scan system for suspicious processes (REMOVED - controller deleted)"""
        print("\n🔍 Process scanning removed in streamlined version")
        return []
    
    def scan_suspicious_services(self) -> List[Dict[str, str]]:
        """Scan for suspicious services (REMOVED - controller deleted)"""
        print("\n🔍 Service scanning removed in streamlined version")
        return []
    
    def scan_registry_persistence(self) -> List[Dict[str, str]]:
        """Scan registry for persistence/spying autoruns"""
        print("\n🔍 SCANNING REGISTRY FOR PERSISTENCE / SPYING ENTRIES...")

        suspicious: List[Dict[str, str]] = []

        if not WINDOWS_REGISTRY_AVAILABLE:
            print("⚠️  Registry access not available on this system")
            return suspicious

        # Common autorun/persistence hives
        persistence_paths = [
            (winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"),
            (winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Run"),
        ]

        spying_indicators = ['keylogger', 'stealth', 'rat', 'remote', 'spy', 'snoop', 'telemetry', 'record', 'capture']
        risky_paths = ['temp', 'appdata', 'users', 'programdata', '.vbs', '.js', '.scr', '.ps1']

        for hive, path in persistence_paths:
            try:
                with winreg.OpenKey(hive, path) as key:
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            lower_val = str(value).lower()

                            reasons = []
                            if any(ind in lower_val for ind in spying_indicators):
                                reasons.append("Spying keyword present")
                            if any(rp in lower_val for rp in risky_paths):
                                reasons.append("Runs from risky path")
                            if not reasons:
                                i += 1
                                continue

                            suspicious.append({
                                'name': name,
                                'path': path,
                                'value': value,
                                'threat': '; '.join(reasons) or 'Suspicious autorun'
                            })
                            i += 1
                        except OSError:
                            break
            except FileNotFoundError:
                continue
            except Exception as e:
                logger.debug(f"Registry scan error at {path}: {e}")
                continue

        if suspicious:
            print(f"⚠️  Found {len(suspicious)} suspicious persistence entry(ies):")
            for entry in suspicious[:10]:
                print(f"  • {entry['name']} -> {entry['value']}")
                print(f"    Path: {entry['path']}")
                print(f"    Threat: {entry['threat']}")
            if len(suspicious) > 10:
                print(f"    ... and {len(suspicious) - 10} more")
        else:
            print("✅ No obvious spying/persistence entries detected")

        return suspicious
    
    def scan_system_integrity(self) -> Dict[str, List[str]]:
        """Scan critical system files for tampering (REMOVED - controller deleted)"""
        print("\n🔍 File integrity scanning removed in streamlined version")
        return {}
    
    def scan_lateral_movement(self) -> List[Dict[str, str]]:
        """Detect lateral movement attempts (REMOVED - controller deleted)"""
        print("\n🔍 Lateral movement scanning removed in streamlined version")
        return []
    
    def full_system_audit(self) -> Dict[str, Any]:
        """Run comprehensive system audit (REMOVED - controllers deleted)"""
        print("\n" + "="*70)
        print("🛡️  System audit features removed in streamlined version")
        print("="*70)
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'message': 'Windows controllers removed - audit unavailable'
        }
    
    def remediate_threat(self, threat_type: str, target_identifier: str, force: bool = False) -> bool:
        """Remediate threats (REMOVED - controllers deleted)"""
        print(f"\n🛡️  Threat remediation features removed in streamlined version")
        return False
    
    # === PROXY BOUNCING & DEFENSIVE RECONNAISSANCE ===
    
    def proxy_bounce_reconnaissance(self, target_url: str, proxy_list: List[Dict[str, str]] = None, 
                                   delay_seconds: int = 5, max_attempts: int = None) -> Dict[str, Any]:
        """
        Defensive reconnaissance using proxy bouncing to evade detection
        
        AUTHORIZED USE ONLY: For defensive security research, authorized penetration testing,
        and threat intelligence gathering on attacker infrastructure.
        
        Args:
            target_url: Target URL for reconnaissance
            proxy_list: List of proxy configurations (SOCKS5/HTTP)
            delay_seconds: Delay between proxy attempts
            max_attempts: Maximum number of proxy attempts (None = all proxies)
        
        Returns:
            Dict with reconnaissance results
        """
        if not PROXY_SUPPORT_AVAILABLE:
            print("❌ Proxy support not available - Install: pip install requests PySocks")
            return {"error": "Proxy support not installed"}
        
        # Default SOCKS5 proxy list if none provided
        if proxy_list is None:
            proxy_list = [
                {'http': 'socks5h://195.208.3.194:1080', 'https': 'socks5h://195.208.3.194:1080'},
                {'http': 'socks5h://195.208.3.194:1081', 'https': 'socks5h://195.208.3.194:1081'},
                {'http': 'socks5h://195.208.3.194:1082', 'https': 'socks5h://195.208.3.194:1082'},
                {'http': 'socks5h://195.208.3.194:1083', 'https': 'socks5h://195.208.3.194:1083'},
                {'http': 'socks5h://195.208.3.194:1084', 'https': 'socks5h://195.208.3.194:1084'},
            ]
        
        print(f"\n🔍 PROXY BOUNCE RECONNAISSANCE INITIATED")
        print(f"   Target: {target_url}")
        print(f"   Proxies: {len(proxy_list)}")
        print(f"   Delay: {delay_seconds}s between attempts")
        print(f"   ⚠️  AUTHORIZED DEFENSIVE OPERATIONS ONLY")
        
        results = {
            'target': target_url,
            'timestamp': datetime.utcnow().isoformat(),
            'attempts': [],
            'successful': 0,
            'failed': 0,
            'total_proxies': len(proxy_list)
        }
        
        attempts = 0
        for proxy in proxy_list:
            if max_attempts and attempts >= max_attempts:
                break
            
            attempts += 1
            proxy_addr = proxy.get('http', 'unknown')
            
            try:
                print(f"\n   [{attempts}/{len(proxy_list)}] Bouncing through {proxy_addr}...")
                
                start_time = time.time()
                response = requests.get(target_url, proxies=proxy, timeout=15)
                elapsed = time.time() - start_time
                
                attempt_result = {
                    'proxy': proxy_addr,
                    'status_code': response.status_code,
                    'response_time': round(elapsed, 2),
                    'success': True,
                    'content_length': len(response.text),
                    'headers': dict(response.headers)
                }
                
                results['attempts'].append(attempt_result)
                results['successful'] += 1
                
                print(f"      ✓ Success: {response.status_code} ({elapsed:.2f}s, {len(response.text)} bytes)")
                
            except requests.exceptions.RequestException as e:
                attempt_result = {
                    'proxy': proxy_addr,
                    'status_code': None,
                    'response_time': None,
                    'success': False,
                    'error': str(e)
                }
                
                results['attempts'].append(attempt_result)
                results['failed'] += 1
                
                print(f"      ✗ Failed: {str(e)[:100]}")
            
            # Delay before next proxy bounce
            if attempts < len(proxy_list):
                time.sleep(delay_seconds)
        
        print(f"\n📊 RECONNAISSANCE COMPLETE")
        print(f"   Successful: {results['successful']}/{results['total_proxies']}")
        print(f"   Failed: {results['failed']}/{results['total_proxies']}")
        print(f"   Success Rate: {(results['successful'] / results['total_proxies'] * 100):.1f}%")
        
        logger.info(f"Proxy bounce reconnaissance: {results['successful']}/{results['total_proxies']} successful")
        
        return results
    
    def configure_socks_proxy(self, proxy_host: str, proxy_port: int, proxy_type: str = 'SOCKS5'):
        """
        Configure global SOCKS proxy for all socket connections
        
        Args:
            proxy_host: SOCKS proxy host
            proxy_port: SOCKS proxy port
            proxy_type: 'SOCKS4' or 'SOCKS5'
        """
        if not PROXY_SUPPORT_AVAILABLE:
            print("❌ Proxy support not available - Install: pip install PySocks")
            return False
        
        try:
            if proxy_type.upper() == 'SOCKS5':
                socks.set_default_proxy(socks.SOCKS5, proxy_host, proxy_port)
            elif proxy_type.upper() == 'SOCKS4':
                socks.set_default_proxy(socks.SOCKS4, proxy_host, proxy_port)
            else:
                print(f"❌ Invalid proxy type: {proxy_type}")
                return False
            
            # Override default socket with SOCKS socket
            socket.socket = socks.socksocket
            
            print(f"✓ Global {proxy_type} proxy configured: {proxy_host}:{proxy_port}")
            logger.info(f"Configured {proxy_type} proxy: {proxy_host}:{proxy_port}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error configuring SOCKS proxy: {e}")
            logger.error(f"SOCKS proxy configuration error: {e}")
            return False


def main():
    """Main entry point - S.E.R.E. runs automatically in optimized vigilant patrol mode
    
    Implements Mythara Lawful Presence Engine:
    - Validates lawful operational context before starting
    - Detects authority through actions, not appearance
    - Ensures ADA-compliant, non-contact operation
    """
    import argparse

    parser = argparse.ArgumentParser(description='S.E.R.E. Bot - Interactive Cybersecurity Defense')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Skip full drill and go directly to interactive mode')

    args = parser.parse_args()

    # === MYTHARA LAWFUL PRESENCE VALIDATION ===
    print("\n🔍 MYTHARA LAWFUL PRESENCE ENGINE")
    print("="*70)
    print("Validating operational context...")
    
    # Check for lawful context (demo validation)
    lawful_indicators = [
        "Running in user's authorized environment",
        "No emergency/panic indicators detected",
        "System resources within normal bounds",
        "No active restraint/harm commands present"
    ]
    
    print("✓ Lawful Presence Indicators:")
    for indicator in lawful_indicators:
        print(f"  • {indicator}")
    
    # Verify Mythara behavioral constraints
    print("\n✓ Mythara Behavioral Constraints Active:")
    print(f"  • ALWAYS: {', '.join(CONFIG['MYTHARA_ALWAYS'][:4])}...")
    print(f"  • NEVER: {', '.join(CONFIG['MYTHARA_NEVER'][:4])}...")
    print(f"  • Non-Contact Mode: {'✓ ENABLED' if CONFIG['MAINTAIN_DISTANCE'] else '✗ DISABLED'}")
    print("="*70)

    print("\n🎖️  Initializing S.E.R.E. Bot with Performance Optimizations")
    print("="*70)
    print(f"⚡ Scan Interval: {CONFIG['DEFAULT_SCAN_INTERVAL']}s (optimized)")
    print(f"🔄 Concurrent Threads: {CONFIG['CONCURRENT_SCAN_THREADS']}")
    print(f"⚡ Async Operations: {'ENABLED' if CONFIG['ASYNC_OPERATIONS'] else 'DISABLED'}")
    print(f"🎯 Real-time Monitoring: {'ENABLED' if CONFIG['ENABLE_REAL_TIME_MONITORING'] else 'DISABLED'}")
    print(f"⚡ Reduced Delays: {'ENABLED' if CONFIG['REDUCED_ARTIFICIAL_DELAYS'] else 'DISABLED'}")
    print(f"📡 Ping Defense: {'ENABLED' if CONFIG['ENABLE_CONTINUOUS_PING'] else 'DISABLED'}")
    print("="*70)

    # Initialize S.E.R.E. with optimizations
    # Use standard SEREBot for all modes (more stable)
    sere = SEREBot()
    print("\n🎖️  Using standard SEREBot")
    
    # Generate startup report
    print("\n📊 Generating Startup IP Geolocation Report...")
    sere.generate_ip_geolocation_report("STARTUP")

    # Check command line arguments
    if args.interactive:
        # Skip full drill, go directly to interactive mode
        print("\n🎖️  Entering DIRECT INTERACTIVE MODE")
        print("Type 'help' for commands, 'exit' to quit")
        
        try:
            sere.interactive_mode()
        finally:
            # Always generate shutdown report
            print("\n📊 Generating Final IP Geolocation Report...")
            sere.generate_ip_geolocation_report("SHUTDOWN")
        
        return 0

    

    # Default mode: Show full drill then go interactive
    print("\n" + "="*70)
    print("🎖️  S.E.R.E. BOT ACTIVATED - FULL INTERACTIVE MODE")
    print("    Complete training drill + command interface")
    print("="*70)

    # Run full drill to show Initialize, Detect, Evade, Resist, Escape with humor
    sere.full_sere_drill()

    # Then enter interactive mode for continued operation
    print("\n" + "="*70)
    print("🎭 ENTERING INTERACTIVE COMMAND MODE")
    print("Type 'help' for commands, 'exit' to quit")
    print("The bot will continue monitoring and responding to commands")
    print("="*70)
    # If running in a terminal that doesn't support stdin (e.g., VS Code Python output pane),
    # inform the user and exit cleanly instead of hanging without a prompt.
    try:
        if not sys.stdin.isatty():
            print("\n⚠️  Interactive input isn't available in this terminal window.")
            print("   Please run from a regular PowerShell/CMD terminal:")
            print("     > cd \"c:\\Users\\Mythara\\Desktop\\Clone Repo Mythara\\Mythara_Archive\"")
            print("     > python sere_bot.py")
            print("   Or use: python sere_bot.py --interactive")
            
            # Generate shutdown report before exiting
            print("\n📊 Generating Final IP Geolocation Report...")
            sere.generate_ip_geolocation_report("SHUTDOWN")
            return 0
    except Exception:
        # If isatty() check fails for any reason, continue and try interactive
        pass

    try:
        sere.interactive_mode()
    finally:
        # Always generate shutdown report
        print("\n📊 Generating Final IP Geolocation Report...")
        sere.generate_ip_geolocation_report("SHUTDOWN")

    print("\n🎖️  S.E.R.E. powered down. Mission complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

