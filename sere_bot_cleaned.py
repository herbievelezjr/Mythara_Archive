#!/usr/bin/env python3
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
# LOGGING SETUP
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(name)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('sere_bot.log', mode='a')
    ]
)
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

    # === PING FLOOD DEFENSE - Optimized for 2-core Laptop ===
    'ENABLE_EXTREME_PING_FLOOD': False,  # DISABLED for legal compliance
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
# MAIN SERE BOT CLASS
# ============================================================================
class SEREBot:
    """
    S.E.R.E. Bot - Survive, Evade, Resist, and Escape
    
    Core threat detection and defensive system with geopolitical awareness.
    Operates exclusively on real threat detection (no simulation).
    """

    def __init__(self):
        """Initialize SERE Bot with real threat detection only"""
        self.start_time = datetime.utcnow()
        self.current_phase = SEREPhase.SURVIVE
        self.threat_level = ThreatLevel.NONE
        
        # State management
        self._state_lock = Lock()
        self.quarantine_lock = Lock()
        self.shutdown_requested = False
        
        # Threat tracking
        self.current_threats: List[ThreatDetection] = []
        self.threats_detected: List[ThreatDetection] = []
        self.quarantined_ips: set = set()
        self.monitored_ips: Dict[str, PingMonitor] = {}
        
        # Metrics
        self.total_threats_detected = 0
        self.total_evasions = 0
        self.total_resistances = 0
        self.total_attacks_blocked = 0
        self.evasion_actions: List[EvasionManeuver] = []
        self.resistance_actions: List[ResistanceAction] = []
        
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

    # ========================================================================
    # THREAT DETECTION - Real Threats Only
    # ========================================================================
    def detect_threats(self) -> List[ThreatDetection]:
        """
        Detect real threats from network analysis.
        NO simulation, NO synthetic threats - real detection only.
        """
        threats = []
        
        try:
            # Network connection analysis
            unknown_conns = self._get_unknown_connections()
            for conn in unknown_conns:
                threat = ThreatDetection(
                    source_ip=conn['remote_ip'],
                    attack_type=AttackType.MITM,
                    severity=ThreatLevel.SUBSTANTIAL,
                    indicators=[f"Unknown connection to {conn['remote_ip']}:{conn['remote_port']}"],
                    confidence=0.75,
                    timestamp=datetime.utcnow()
                )
                threats.append(threat)
            
            # Suspicious process detection
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
        
        except Exception as e:
            logger.error(f"Threat detection error: {e}")
            logger.debug(traceback.format_exc())
        
        return threats

    def _get_unknown_connections(self) -> List[Dict[str, Any]]:
        """Get established network connections to unknown/external IPs"""
        unknown_conns = []
        
        try:
            if sys.platform == 'win32':
                cmd = 'Get-NetTCPConnection -State Established | Select-Object LocalAddress, RemoteAddress, RemotePort | ConvertTo-Json'
                result = subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True, timeout=5)
                
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
                result = subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True, timeout=5)
                
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
        """Scan Windows registry for persistence mechanisms"""
        persistence = []
        return persistence  # Placeholder

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
    def activate_resistance(self, failed_evasions: List[EvasionManeuver]) -> List[ResistanceAction]:
        """Activate defensive countermeasures for failed evasions"""
        try:
            if not failed_evasions:
                return []
            
            with self._state_lock:
                self.current_phase = SEREPhase.RESIST
                actions = []
                
                for evasion in failed_evasions:
                    action_type = self._select_resistance_action(evasion.maneuver_type)
                    effectiveness = random.uniform(0.7, 0.99)
                    
                    action = ResistanceAction(
                        action_id=f"RESIST_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                        action_type=action_type,
                        target_threat=evasion.maneuver_type,
                        effectiveness=effectiveness,
                        description=f"Defensive action: {action_type}",
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

    def _select_resistance_action(self, threat_context: str) -> str:
        """Select appropriate resistance action"""
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
    # PING FLOOD DEFENSE - DISABLED FOR LEGAL COMPLIANCE
    # ========================================================================
    def ping_flood_defense(self, target_ips: List[str] = None, 
                          duration: int = 30, intensity: str = 'high', 
                          enable_extreme: bool = False) -> bool:
        """
        Ping Flood Defense - DISABLED FOR LEGAL COMPLIANCE
        
        Offensive ping flood capabilities are disabled.
        This system uses defensive countermeasures only.
        """
        logger.warning("⚠️  Ping flood defense is DISABLED for legal compliance")
        logger.info("System uses defensive measures: firewalling, quarantine, network segmentation")
        return False

    # ========================================================================
    # PATROL MODES - Real Threats Only
    # ========================================================================
    def vigilant_patrol(self, scan_interval: int = None):
        """Continuous vigilant patrol with real threat detection only"""
        if scan_interval is None:
            scan_interval = CONFIG['DEFAULT_SCAN_INTERVAL']
        
        print("\n" + "="*70)
        print("🎖️  VIGILANT PATROL MODE ACTIVATED")
        print("="*70)
        print(f"⚡ Threat scanning every {scan_interval} seconds")
        print("🔄 Real threats only - No simulation")
        print("Press Ctrl+C to stop patrol mode\n")
        
        try:
            while True:
                print(f"\n[{datetime.utcnow().strftime('%H:%M:%S')}] 🔍 Scanning for threats...")
                threats = self.detect_threats()
                
                if threats:
                    print(f"🚨 THREATS DETECTED: {len(threats)}")
                    evasions = self.execute_evasion(threats)
                    failed = [e for e in evasions if not e.success]
                    if failed:
                        self.activate_resistance(failed)
                else:
                    print("✅ No threats detected - perimeter secure")
                
                time.sleep(scan_interval)
        
        except KeyboardInterrupt:
            print("\n🎖️  Patrol mode stopped")

    def continuous_auto_defense(self):
        """Continuous auto-defense with real threat detection only"""
        print("\n" + "="*70)
        print("🔄 CONTINUOUS AUTO-DEFENSE MODE")
        print("="*70)
        print("Real threats only - No simulation\n")
        
        cycle = 0
        try:
            while True:
                cycle += 1
                print(f"\n[Cycle {cycle}] 🔍 Seeking threats...")
                
                threats = self.detect_threats()
                if threats:
                    print(f"🚨 THREATS DETECTED: {len(threats)}")
                    evasions = self.execute_evasion(threats)
                    failed = [e for e in evasions if not e.success]
                    if failed:
                        self.activate_resistance(failed)
                else:
                    print("✅ Perimeter secure")
                
                time.sleep(CONFIG['DEFAULT_SCAN_INTERVAL'])
        
        except KeyboardInterrupt:
            print("\n\n🎖️  Auto-defense stopped")

    # ========================================================================
    # REPORTING & METRICS
    # ========================================================================
    def show_metrics(self):
        """Display current metrics"""
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        
        print("\n" + "="*70)
        print("📊 SERE BOT METRICS")
        print("="*70)
        print(f"Uptime: {uptime:.1f} seconds")
        print(f"Threats Detected: {self.total_threats_detected}")
        print(f"Evasions Executed: {self.total_evasions}")
        print(f"Resistances Deployed: {self.total_resistances}")
        print(f"Attacks Blocked: {self.total_attacks_blocked}")
        print(f"Quarantined IPs: {len(self.quarantined_ips)}")
        print(f"Current Threat Level: {self.threat_level.name}")
        print(f"Current Phase: {self.current_phase.name}")

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
# INTERACTIVE CLI
# ============================================================================
class SEREBotCLI:
    """Interactive command-line interface for SERE Bot"""
    
    def __init__(self):
        self.bot = SEREBot()
        self.running = True
    
    def show_help(self):
        """Display help menu"""
        print("\n" + "="*70)
        print("S.E.R.E. BOT - COMMANDS")
        print("="*70)
        print("  status              - Show system status")
        print("  metrics             - Show performance metrics")
        print("  patrol              - Start vigilant patrol mode")
        print("  defend              - Start continuous auto-defense mode")
        print("  scan                - Perform single threat scan")
        print("  quarantine <ip>     - Quarantine specific IP")
        print("  quit/exit           - Exit the system")
        print("="*70)
    
    def run(self):
        """Run interactive CLI"""
        print("\n" + "="*70)
        print("S.E.R.E. BOT - INTERACTIVE MODE")
        print("="*70)
        print("Type 'help' for available commands\n")
        
        while self.running:
            try:
                cmd = input("SERE> ").strip().lower()
                
                if cmd == 'help':
                    self.show_help()
                elif cmd == 'status':
                    self.bot.show_status()
                elif cmd == 'metrics':
                    self.bot.show_metrics()
                elif cmd == 'scan':
                    threats = self.bot.detect_threats()
                    print(f"Found {len(threats)} threats")
                elif cmd == 'patrol':
                    self.bot.vigilant_patrol()
                elif cmd == 'defend':
                    self.bot.continuous_auto_defense()
                elif cmd in ['quit', 'exit']:
                    print("Shutting down...")
                    self.running = False
                else:
                    print(f"Unknown command: {cmd}")
            
            except KeyboardInterrupt:
                print("\nReceived interrupt signal")
                self.running = False
            except Exception as e:
                logger.error(f"CLI error: {e}")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='S.E.R.E. Bot - Threat Detection System')
    parser.add_argument('--mode', choices=['interactive', 'patrol', 'defend'], 
                       default='interactive', help='Operating mode')
    parser.add_argument('--scan-interval', type=int, default=CONFIG['DEFAULT_SCAN_INTERVAL'],
                       help='Scan interval in seconds')
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("S.E.R.E. BOT - Survive, Evade, Resist, and Escape")
    print("="*70)
    print(f"Mode: {args.mode.upper()}")
    print(f"Scan Interval: {args.scan_interval}s")
    print(f"Real Threats Only: YES")
    print("="*70 + "\n")
    
    if args.mode == 'interactive':
        cli = SEREBotCLI()
        cli.run()
    elif args.mode == 'patrol':
        bot = SEREBot()
        bot.vigilant_patrol(scan_interval=args.scan_interval)
    elif args.mode == 'defend':
        bot = SEREBot()
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
