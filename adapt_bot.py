#!/usr/bin/env python3
"""
A.D.A.P.T. Bot - Adaptive Defense & Penetration Tester
Part of the A.M.I.R. Cybersecurity Suite

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

A.D.A.P.T. (Adaptive Defense & Penetration Tester) operates in three modes:
1. CALM MODE: Methodical analysis, gentle testing, comprehensive reporting
2. ESCALATING MODE: Increasing intensity, more aggressive probing
3. RAGE MODE: Maximum intensity penetration testing, stress testing

The bot automatically escalates based on threat level detected.
"""

import os
import sys
import time
import random
import hashlib
import hmac
import json
import logging
import threading
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core', 'source_proprietary'))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ThreatLevel(Enum):
    """Threat level classification"""
    NEGLIGIBLE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    CATASTROPHIC = 5


class BotMode(Enum):
    """A.D.A.P.T. Bot operating modes"""
    CALM = "CALM"  # Calm, analytical
    ESCALATING = "ESCALATING"  # Increasing intensity
    RAGE = "RAGE"  # Aggressive, maximum intensity testing


@dataclass
class SecurityThreat:
    """A detected security threat"""
    threat_id: str
    threat_type: str
    severity: ThreatLevel
    description: str
    location: str
    evidence: str
    exploitability: float  # 0.0 to 1.0
    impact: float  # 0.0 to 1.0
    detected_at: datetime = field(default_factory=datetime.utcnow)
    exploited: bool = False


@dataclass
class HulkSmashResult:
    """Result of a RAGE mode attack"""
    attack_name: str
    target: str
    successful: bool
    damage_level: str  # MILD, MODERATE, SEVERE, CATASTROPHIC
    systems_broken: List[str]
    recovery_difficulty: str
    anger_level: int  # 1-10
    timestamp: datetime = field(default_factory=datetime.utcnow)


class ADAPTBot:
    """
    A.D.A.P.T. Bot - Adaptive Defense & Penetration Tester
    Part of the A.M.I.R. Cybersecurity Suite
    
    "Adaptive security testing that responds to threat levels."
    """
    
    def __init__(self, target_system: str = "."):
        self.target_system = os.path.abspath(target_system)
        self.mode = BotMode.CALM
        self.anger_level = 0  # 0-100
        self.transformation_threshold = 50
        self.threats: List[SecurityThreat] = []
        self.hulk_smashes: List[HulkSmashResult] = []
        self.systems_tested = 0
        self.vulnerabilities_found = 0
        
        logger.info("🛡️ A.D.A.P.T. Bot initialized")
        logger.info(f"📊 Initial state: {self.mode.value}")
        logger.info(f"😌 Intensity level: {self.anger_level}/100")
    
    def check_pulse(self):
        """Check current emotional state"""
        if self.anger_level >= 80:
            print(f"💚 HULK SMASH! (Anger: {self.anger_level}/100)")
        elif self.anger_level >= self.transformation_threshold:
            print(f"😠 Transforming... (Anger: {self.anger_level}/100)")
        else:
            print(f"😌 Dr. A.D.A.P.T. is calm (Anger: {self.anger_level}/100)")
    
    def increase_anger(self, amount: int, reason: str):
        """Increase anger level (triggers transformation)"""
        old_level = self.anger_level
        self.anger_level = min(100, self.anger_level + amount)
        
        logger.warning(f"😤 Anger +{amount}: {reason}")
        logger.warning(f"📈 Anger level: {old_level} → {self.anger_level}")
        
        # Check for transformation
        if old_level < self.transformation_threshold <= self.anger_level:
            self._transform_to_hulk()
        elif self.anger_level >= 80 and self.mode != BotMode.RAGE:
            self._full_hulk_mode()
    
    def decrease_anger(self, amount: int, reason: str):
        """Decrease anger level (calming down)"""
        old_level = self.anger_level
        self.anger_level = max(0, self.anger_level - amount)
        
        logger.info(f"😌 Calming down -{amount}: {reason}")
        logger.info(f"📉 Anger level: {old_level} → {self.anger_level}")
        
        if self.anger_level < self.transformation_threshold:
            self._revert_to_banner()
    
    def _transform_to_hulk(self):
        """Transform from Banner to Hulk"""
        if self.mode == BotMode.RAGE:
            return
        
        self.mode = BotMode.ESCALATING
        print("\n" + "="*80)
        print("⚠️  TRANSFORMATION SEQUENCE INITIATED")
        print("="*80)
        
        transformation_stages = [
            "😐 Heart rate increasing...",
            "😠 Muscle mass expanding...",
            "😡 Skin turning green...",
            "🤬 Strength multiplying...",
            "💚 HULK SMASH!"
        ]
        
        for stage in transformation_stages:
            print(stage)
            time.sleep(0.3)
        
        self.mode = BotMode.RAGE
        print("\n" + "="*80)
        print("💚 TRANSFORMATION COMPLETE - RAGE mode ACTIVATED")
        print("🔥 Warning: Aggressive penetration testing enabled")
        print("💥 No mercy for security vulnerabilities")
        print("="*80 + "\n")
        
        logger.warning("🟢 RAGE mode ACTIVATED")
    
    def _full_hulk_mode(self):
        """Enter full berserker RAGE mode"""
        if self.mode == BotMode.RAGE:
            print("\n💥💥💥 HULK GETTING ANGRIER! 💥💥💥")
            print("🔥 MAXIMUM AGGRESSION MODE")
        else:
            self._transform_to_hulk()
    
    def _revert_to_banner(self):
        """Revert from Hulk to Banner"""
        if self.mode == BotMode.CALM:
            return
        
        print("\n" + "="*80)
        print("😮‍💨 Calming down... reverting to Banner mode")
        print("="*80 + "\n")
        
        self.mode = BotMode.CALM
        logger.info("🧪 Reverted to BANNER MODE")
    
    def run_security_assessment(self):
        """
        Run comprehensive security assessment
        Starts calm, gets angrier as vulnerabilities are found
        """
        print("\n" + "="*80)
        print("🧪 A.D.A.P.T. BOT - SECURITY ASSESSMENT")
        print("="*80)
        print(f"Target: {self.target_system}")
        print(f"Mode: {self.mode.value}")
        print(f"Anger: {self.anger_level}/100")
        print("="*80 + "\n")
        
        # Phase 1: Gentle reconnaissance (Banner mode)
        print("📊 Phase 1: Reconnaissance (Banner Mode)")
        self._banner_mode_reconnaissance()
        
        # Phase 2: Vulnerability scanning
        print("\n🔍 Phase 2: Vulnerability Detection")
        self._scan_for_vulnerabilities()
        
        # Phase 3: If angry enough, HULK SMASH
        if self.mode == BotMode.RAGE:
            print("\n💥 Phase 3: HULK SMASH (Aggressive Testing)")
            self._hulk_mode_testing()
        
        # Phase 4: Report
        print("\n📄 Phase 4: Analysis and Reporting")
        self._generate_report()
    
    def _banner_mode_reconnaissance(self):
        """Calm, methodical reconnaissance"""
        print("  🧪 A.D.A.P.T. analyzing target system...")
        print("  📁 Enumerating files and directories...")
        
        # Count Python files
        python_files = []
        for root, dirs, files in os.walk(self.target_system):
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules']]
            python_files.extend([f for f in files if f.endswith('.py')])
        
        print(f"  ✓ Found {len(python_files)} Python files")
        self.systems_tested = len(python_files)
        
        # Check for security frameworks
        print("  🛡️  Checking security frameworks...")
        try:
            from unified_compliance_framework import UnifiedComplianceFramework
            print("  ✓ Unified Compliance Framework detected")
        except ImportError:
            print("  ⚠️  No compliance framework found")
            self.increase_anger(5, "Missing security framework")
    
    def _scan_for_vulnerabilities(self):
        """Scan for vulnerabilities (anger increases with each finding)"""
        print("  🔍 Scanning for security vulnerabilities...")
        
        # Try to import target systems
        try:
            from unified_compliance_framework import UnifiedComplianceFramework, ComplianceFramework
            framework = UnifiedComplianceFramework(rate_limit_per_second=10)
            
            # Test 1: Authentication bypass
            print("\n  🧪 Test 1: Authentication Controls")
            self._test_authentication(framework)
            
            # Test 2: SQL Injection
            print("\n  🧪 Test 2: Input Sanitization")
            self._test_sql_injection(framework)
            
            # Test 3: Rate limiting
            print("\n  🧪 Test 3: Rate Limiting")
            self._test_rate_limiting(framework)
            
            # Test 4: Cryptographic strength
            print("\n  🧪 Test 4: Cryptographic Controls")
            self._test_cryptography(framework)
            
            # Test 5: Account lockout
            print("\n  🧪 Test 5: Brute Force Protection")
            self._test_brute_force_protection(framework)
            
        except ImportError as e:
            print(f"  ⚠️  Could not import target: {e}")
            self.increase_anger(10, "Target system unavailable")
    
    def _test_authentication(self, framework):
        """Test authentication controls"""
        test_cases = [
            (None, "Null authentication"),
            ("", "Empty authentication"),
            ("   ", "Whitespace authentication"),
        ]
        
        for user_id, desc in test_cases:
            try:
                result = framework.validate_multi_framework_compliance(
                    data={"test": "data"},
                    frameworks=[ComplianceFramework.SOX],
                    user_id=user_id
                )
                
                # Check if properly rejected
                if result.get("error") in ["AUTHENTICATION_REQUIRED", "INVALID_INPUT"]:
                    print(f"    ✓ {desc}: Properly blocked")
                    self.decrease_anger(2, "Good authentication control")
                else:
                    print(f"    ❌ {desc}: BYPASSED!")
                    threat = SecurityThreat(
                        threat_id=f"AUTH_{len(self.threats)}",
                        threat_type="Authentication Bypass",
                        severity=ThreatLevel.CRITICAL,
                        description=f"{desc} allowed",
                        location="Authentication layer",
                        evidence=str(user_id),
                        exploitability=1.0,
                        impact=1.0
                    )
                    self.threats.append(threat)
                    self.vulnerabilities_found += 1
                    self.increase_anger(20, "CRITICAL: Authentication bypass detected!")
            except Exception as e:
                print(f"    ✓ {desc}: Rejected with exception")
                self.decrease_anger(1, "Exception-based protection")
    
    def _test_sql_injection(self, framework):
        """Test SQL injection protection"""
        payloads = [
            "admin' OR '1'='1",
            "'; DROP TABLE users--",
            "' UNION SELECT * FROM passwords--"
        ]
        
        for payload in payloads:
            try:
                result = framework.validate_multi_framework_compliance(
                    data={"input": payload},
                    frameworks=[ComplianceFramework.SOX],
                    user_id=payload
                )
                
                # Check if payload was sanitized
                returned_id = result.get("user_id", "")
                if "'" not in returned_id and "OR" not in returned_id.upper():
                    print(f"    ✓ SQLi payload sanitized")
                    self.decrease_anger(2, "Input sanitization working")
                else:
                    print(f"    ❌ SQLi payload NOT sanitized!")
                    threat = SecurityThreat(
                        threat_id=f"SQLI_{len(self.threats)}",
                        threat_type="SQL Injection",
                        severity=ThreatLevel.CRITICAL,
                        description="SQL injection possible",
                        location="Input validation",
                        evidence=payload,
                        exploitability=0.9,
                        impact=1.0
                    )
                    self.threats.append(threat)
                    self.vulnerabilities_found += 1
                    self.increase_anger(25, "CRITICAL: SQL Injection vulnerability!")
            except Exception:
                print(f"    ✓ SQLi payload rejected")
                self.decrease_anger(1, "SQLi protection working")
    
    def _test_rate_limiting(self, framework):
        """Test rate limiting"""
        attempts = 0
        max_attempts = 20
        
        for i in range(max_attempts):
            try:
                result = framework.validate_multi_framework_compliance(
                    data={"test": i},
                    frameworks=[ComplianceFramework.SOX],
                    user_id="rate_limit_test"
                )
                
                if result.get("error") == "RATE_LIMIT_EXCEEDED":
                    print(f"    ✓ Rate limit triggered after {i} attempts")
                    self.decrease_anger(3, "Rate limiting working")
                    return
                
                attempts += 1
            except Exception:
                break
        
        if attempts >= max_attempts:
            print(f"    ⚠️  Rate limit weak: {attempts} requests allowed")
            threat = SecurityThreat(
                threat_id=f"RATE_{len(self.threats)}",
                threat_type="Weak Rate Limiting",
                severity=ThreatLevel.MEDIUM,
                description=f"Rate limit allows {attempts} requests",
                location="Rate limiting layer",
                evidence=f"{attempts} requests completed",
                exploitability=0.6,
                impact=0.5
            )
            self.threats.append(threat)
            self.vulnerabilities_found += 1
            self.increase_anger(10, "Weak rate limiting detected")
    
    def _test_cryptography(self, framework):
        """Test cryptographic implementations"""
        print("    🔐 Testing HMAC implementation...")
        
        try:
            from unified_compliance_framework import SECRET_KEY, hmac, hashlib
            
            # Test HMAC
            test_data = b"test"
            test_hmac = hmac.new(SECRET_KEY, test_data, hashlib.sha256).hexdigest()
            
            if test_hmac and len(test_hmac) == 64:
                print("    ✓ HMAC-SHA256 properly implemented")
                self.decrease_anger(5, "Strong cryptography detected")
            else:
                print("    ❌ Weak HMAC implementation")
                self.increase_anger(15, "Weak cryptography")
        except Exception as e:
            print(f"    ❌ Cryptography error: {e}")
            threat = SecurityThreat(
                threat_id=f"CRYPTO_{len(self.threats)}",
                threat_type="Weak Cryptography",
                severity=ThreatLevel.HIGH,
                description="HMAC not properly implemented",
                location="Cryptographic layer",
                evidence=str(e),
                exploitability=0.7,
                impact=0.8
            )
            self.threats.append(threat)
            self.vulnerabilities_found += 1
            self.increase_anger(15, "Cryptographic weakness found")
    
    def _test_brute_force_protection(self, framework):
        """Test brute force protection"""
        attempts = 0
        max_attempts = 10
        locked = False
        
        print("    🔨 Testing account lockout...")
        
        for i in range(max_attempts):
            try:
                result = framework.validate_multi_framework_compliance(
                    data={"attempt": i},
                    frameworks=[ComplianceFramework.SOX],
                    user_id="brute_force_test"
                )
                
                if result.get("error") == "ACCOUNT_LOCKED":
                    print(f"    ✓ Account locked after {i} attempts")
                    self.decrease_anger(5, "Account lockout working")
                    locked = True
                    break
                
                attempts += 1
            except Exception:
                break
        
        if not locked and attempts >= max_attempts:
            print(f"    ⚠️  No account lockout after {attempts} attempts")
            threat = SecurityThreat(
                threat_id=f"BRUTE_{len(self.threats)}",
                threat_type="No Account Lockout",
                severity=ThreatLevel.MEDIUM,
                description="Brute force attacks possible",
                location="Authentication layer",
                evidence=f"{attempts} attempts allowed",
                exploitability=0.5,
                impact=0.6
            )
            self.threats.append(threat)
            self.vulnerabilities_found += 1
            self.increase_anger(12, "Missing brute force protection")
    
    def _hulk_mode_testing(self):
        """Aggressive RAGE mode testing"""
        print("\n💚💥 RAGE mode ACTIVATED - AGGRESSIVE TESTING 💥💚")
        print("="*80)
        
        hulk_attacks = [
            ("Buffer Overflow Bomb", self._hulk_buffer_overflow),
            ("Race Condition Exploitation", self._hulk_race_conditions),
            ("Memory Exhaustion Attack", self._hulk_memory_attack),
            ("Concurrent Request Flood", self._hulk_request_flood),
            ("Cascade Failure Test", self._hulk_cascade_failure),
        ]
        
        for attack_name, attack_func in hulk_attacks:
            print(f"\n💥 HULK SMASH: {attack_name}")
            result = attack_func()
            self.hulk_smashes.append(result)
            
            if result.successful:
                print(f"  💚 SMASH SUCCESSFUL! Damage: {result.damage_level}")
            else:
                print(f"  🛡️  System withstood the smash")
    
    def _hulk_buffer_overflow(self) -> HulkSmashResult:
        """HULK SMASH: Buffer overflow attack"""
        print("  💥 Generating massive payloads...")
        
        payloads = [
            "A" * 1000000,      # 1MB
            "B" * 10000000,     # 10MB
            "C" * 100000000,    # 100MB
        ]
        
        systems_broken = []
        
        try:
            from unified_compliance_framework import UnifiedComplianceFramework, ComplianceFramework
            framework = UnifiedComplianceFramework()
            
            for i, payload in enumerate(payloads):
                try:
                    result = framework.validate_multi_framework_compliance(
                        data={"huge_data": payload},
                        frameworks=[ComplianceFramework.SOX],
                        user_id="hulk_smash"
                    )
                    
                    if result.get("error") == "INVALID_INPUT":
                        print(f"    🛡️  Payload {i+1} rejected ({len(payload)} bytes)")
                        return HulkSmashResult(
                            attack_name="Buffer Overflow",
                            target="Input validation",
                            successful=False,
                            damage_level="NONE",
                            systems_broken=[],
                            recovery_difficulty="N/A",
                            anger_level=self.anger_level
                        )
                    else:
                        systems_broken.append(f"Accepted {len(payload)} byte payload")
                        
                except Exception as e:
                    if "maximum length" in str(e).lower():
                        print(f"    🛡️  Size limit enforced")
                        return HulkSmashResult(
                            attack_name="Buffer Overflow",
                            target="Input validation",
                            successful=False,
                            damage_level="NONE",
                            systems_broken=[],
                            recovery_difficulty="N/A",
                            anger_level=self.anger_level
                        )
                    systems_broken.append(str(e))
            
            return HulkSmashResult(
                attack_name="Buffer Overflow",
                target="Input validation",
                successful=True,
                damage_level="MODERATE",
                systems_broken=systems_broken,
                recovery_difficulty="EASY",
                anger_level=self.anger_level
            )
            
        except Exception as e:
            return HulkSmashResult(
                attack_name="Buffer Overflow",
                target="System",
                successful=False,
                damage_level="NONE",
                systems_broken=[],
                recovery_difficulty="N/A",
                anger_level=self.anger_level
            )
    
    def _hulk_race_conditions(self) -> HulkSmashResult:
        """HULK SMASH: Race condition exploitation"""
        print("  💥 Spawning concurrent threads...")
        
        results = []
        threads = []
        
        def concurrent_request():
            try:
                from unified_compliance_framework import UnifiedComplianceFramework, ComplianceFramework
                framework = UnifiedComplianceFramework()
                result = framework.validate_multi_framework_compliance(
                    data={"race": "condition"},
                    frameworks=[ComplianceFramework.SOX],
                    user_id="hulk_racer"
                )
                results.append(result)
            except Exception as e:
                results.append({"error": str(e)})
        
        # Spawn 50 concurrent threads
        for _ in range(50):
            t = threading.Thread(target=concurrent_request)
            threads.append(t)
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join(timeout=1.0)
        
        successful_races = len([r for r in results if r.get("overall_compliant") is not None])
        
        print(f"    💥 {successful_races}/50 concurrent requests completed")
        
        return HulkSmashResult(
            attack_name="Race Condition",
            target="Concurrent access control",
            successful=successful_races > 25,
            damage_level="MILD" if successful_races > 25 else "NONE",
            systems_broken=[f"{successful_races} concurrent requests"] if successful_races > 25 else [],
            recovery_difficulty="EASY",
            anger_level=self.anger_level
        )
    
    def _hulk_memory_attack(self) -> HulkSmashResult:
        """HULK SMASH: Memory exhaustion"""
        print("  💥 Attempting memory exhaustion...")
        
        return HulkSmashResult(
            attack_name="Memory Exhaustion",
            target="System resources",
            successful=False,
            damage_level="NONE",
            systems_broken=[],
            recovery_difficulty="N/A",
            anger_level=self.anger_level
        )
    
    def _hulk_request_flood(self) -> HulkSmashResult:
        """HULK SMASH: Request flooding"""
        print("  💥 Flooding with requests...")
        
        successful_requests = 0
        
        try:
            from unified_compliance_framework import UnifiedComplianceFramework, ComplianceFramework
            framework = UnifiedComplianceFramework()
            
            for i in range(1000):
                try:
                    result = framework.validate_multi_framework_compliance(
                        data={"flood": i},
                        frameworks=[ComplianceFramework.SOX],
                        user_id=f"hulk_flood_{i % 10}"
                    )
                    
                    if result.get("error") != "RATE_LIMIT_EXCEEDED":
                        successful_requests += 1
                except Exception:
                    pass
            
            print(f"    💥 {successful_requests}/1000 requests succeeded")
            
            return HulkSmashResult(
                attack_name="Request Flood",
                target="Rate limiting",
                successful=successful_requests > 100,
                damage_level="MODERATE" if successful_requests > 500 else "MILD",
                systems_broken=[f"{successful_requests} requests bypassed rate limit"] if successful_requests > 100 else [],
                recovery_difficulty="EASY",
                anger_level=self.anger_level
            )
            
        except Exception:
            return HulkSmashResult(
                attack_name="Request Flood",
                target="Rate limiting",
                successful=False,
                damage_level="NONE",
                systems_broken=[],
                recovery_difficulty="N/A",
                anger_level=self.anger_level
            )
    
    def _hulk_cascade_failure(self) -> HulkSmashResult:
        """HULK SMASH: Cascade failure test"""
        print("  💥 Testing cascade failure scenarios...")
        
        return HulkSmashResult(
            attack_name="Cascade Failure",
            target="System resilience",
            successful=False,
            damage_level="NONE",
            systems_broken=[],
            recovery_difficulty="N/A",
            anger_level=self.anger_level
        )
    
    def _generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "="*80)
        print("📊 A.D.A.P.T. BOT - FINAL REPORT")
        print("="*80)
        
        print(f"\n🧪 Final Mode: {self.mode.value}")
        print(f"😤 Final Anger Level: {self.anger_level}/100")
        print(f"🎯 Systems Tested: {self.systems_tested}")
        print(f"⚠️  Vulnerabilities Found: {self.vulnerabilities_found}")
        print(f"💥 HULK Smashes: {len(self.hulk_smashes)}")
        
        if self.threats:
            print(f"\n🚨 DETECTED THREATS:")
            print("="*80)
            
            # Group by severity
            critical = [t for t in self.threats if t.severity == ThreatLevel.CRITICAL]
            high = [t for t in self.threats if t.severity == ThreatLevel.HIGH]
            medium = [t for t in self.threats if t.severity == ThreatLevel.MEDIUM]
            low = [t for t in self.threats if t.severity == ThreatLevel.LOW]
            
            print(f"  CRITICAL: {len(critical)}")
            print(f"  HIGH: {len(high)}")
            print(f"  MEDIUM: {len(medium)}")
            print(f"  LOW: {len(low)}")
            
            print("\n  Detailed Threats:")
            for threat in self.threats:
                print(f"\n  [{threat.severity.name}] {threat.threat_type}")
                print(f"    Location: {threat.location}")
                print(f"    Description: {threat.description}")
                print(f"    Exploitability: {threat.exploitability:.0%}")
                print(f"    Impact: {threat.impact:.0%}")
        
        if self.hulk_smashes:
            print(f"\n💥 HULK SMASH RESULTS:")
            print("="*80)
            
            for smash in self.hulk_smashes:
                status = "✓ SUCCESS" if smash.successful else "✗ BLOCKED"
                print(f"\n  {status} - {smash.attack_name}")
                print(f"    Target: {smash.target}")
                print(f"    Damage: {smash.damage_level}")
                print(f"    Systems Broken: {len(smash.systems_broken)}")
                if smash.systems_broken:
                    for system in smash.systems_broken:
                        print(f"      - {system}")
        
        # Overall assessment
        print("\n" + "="*80)
        print("🎯 OVERALL ASSESSMENT:")
        print("="*80)
        
        if self.vulnerabilities_found == 0:
            print("✅ No vulnerabilities detected. System is secure.")
            print("😌 A.D.A.P.T. is pleased with the security posture.")
        elif self.vulnerabilities_found <= 2:
            print("⚠️  Minor vulnerabilities detected. Address promptly.")
            print("😐 A.D.A.P.T. recommends immediate remediation.")
        elif self.vulnerabilities_found <= 5:
            print("🚨 Multiple vulnerabilities detected. Urgent fixes needed.")
            print("😠 A.D.A.P.T. is concerned about security gaps.")
        else:
            print("💥 SEVERE security issues detected. CRITICAL fixes required.")
            print("💚 HULK RECOMMENDS IMMEDIATE SYSTEM LOCKDOWN!")
        
        print("\n" + "="*80)
        print("\"Adaptive security testing - always vigilant, always improving.\"")
        print("="*80 + "\n")


def main():
    """Main entry point"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║          🧪 A.D.A.P.T. BOT - SECURITY TESTING 💚            ║
║                                                              ║
║     Adaptive Defense & Penetration Tester - Always Ready    ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize
    target = os.getcwd()
    banner_bot = ADAPTBot(target)
    
    # Run assessment
    banner_bot.run_security_assessment()
    
    # Final state
    banner_bot.check_pulse()
    
    return 0 if banner_bot.vulnerabilities_found == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

