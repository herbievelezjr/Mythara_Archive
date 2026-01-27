#!/usr/bin/env python3
"""
Test script to demonstrate health and volatility dashboard
"""

import sys
sys.path.insert(0, '.')
from sere_security_system import SERESecuritySystem, ThreatDetection, AttackType, ThreatLevel

bot = SERESecuritySystem()

# Simulate threat detection history across multiple cycles
threat_counts = [0, 2, 5, 8, 7, 4, 2, 1, 0, 1]
print("="*70)
print("HEALTH & VOLATILITY DASHBOARD - SIMULATED PATROL CYCLES")
print("="*70)
print()

for cycle, threat_count in enumerate(threat_counts, 1):
    # Create threats
    threats = []
    for i in range(threat_count):
        threat = ThreatDetection(
            attack_type=AttackType.MALWARE if i % 2 == 0 else AttackType.MITM,
            source_ip=f'192.168.1.{100+i}',
            indicators=['test'],
            severity=ThreatLevel.MODERATE,
            confidence=0.8
        )
        threats.append(threat)
    
    # Calculate scores
    health = bot.calculate_system_health(threats)
    integrity = bot.calculate_system_integrity(threats)
    
    # Track history
    bot.health_history.append(health)
    bot.integrity_history.append(integrity)
    
    # Calculate volatility
    volatility = bot.calculate_volatility(bot.integrity_history)
    
    # Get status
    health_status = bot.get_health_status(health)
    integrity_status = bot.get_integrity_status(integrity)
    
    # Volatility level
    if volatility < 5:
        volatility_level = "STABLE 🟢"
    elif volatility < 15:
        volatility_level = "ELEVATED 🟡"
    else:
        volatility_level = "CRITICAL 🔴"
    
    # Display cycle
    print(f"[Cycle {cycle}] Threats: {threat_count}")
    print("   " + "═"*60)
    print("   📊 SYSTEM HEALTH DASHBOARD")
    print("   " + "═"*60)
    print(f"   Health Score:    {health:5.1f}%  [{health_status}]")
    print(f"   Integrity Score: {integrity:5.1f}%  [{integrity_status}]")
    print(f"   Volatility:      {volatility:5.2f}   [{volatility_level}]")
    print(f"   Threat Count:    {threat_count:3d} active")
    print("   " + "═"*60)
    print()
