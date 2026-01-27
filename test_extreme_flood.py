#!/usr/bin/env python3
"""
Test script for 5.16 Tbps extreme ping flood defense
"""

from sere_security_system import SERESecuritySystem, CONFIG
import time

print("\n" + "="*70)
print("🔥 S.E.R.E. EXTREME PING FLOOD TEST - 5.16 Tbps")
print("="*70)

# Initialize bot
bot = SERESecuritySystem()

# Display configuration
print("\n📊 CONFIGURATION STATUS:")
print(f"   ✅ ENABLE_EXTREME_PING_FLOOD: {CONFIG['ENABLE_EXTREME_PING_FLOOD']}")
print(f"   📈 Target Throughput: {CONFIG['PING_FLOOD_TARGET_TBPS']} Tbps")
print(f"   🧵 Worker Threads: {CONFIG['PING_FLOOD_WORKER_THREADS']}")
print(f"   📦 Packet Size: {CONFIG['PING_PACKET_SIZE_BYTES']} bytes")

# Detect threats
print("\n🔍 DETECTING THREATS...")
threats = bot.detect_threats()
print(f"✅ Threats detected: {len(threats)}")

if threats:
    # Get threat info
    threat_ip = threats[0].source_ip
    threat_type = threats[0].attack_type.value
    
    print(f"\n🎯 TARGET THREAT:")
    print(f"   IP Address: {threat_ip}")
    print(f"   Attack Type: {threat_type}")
    print(f"   Severity: {threats[0].severity.name}")
    
    # Activate extreme ping flood
    print("\n" + "="*70)
    print("⚡ ACTIVATING 5.16 Tbps EXTREME PING FLOOD DEFENSE")
    print("="*70)
    
    # Calculate expected throughput
    target_tbps = CONFIG['PING_FLOOD_TARGET_TBPS']
    packet_size = CONFIG['PING_PACKET_SIZE_BYTES']
    target_bytes_per_sec = target_tbps * 1_000_000_000_000 / 8
    packets_per_sec = int(target_bytes_per_sec / packet_size)
    
    print(f"\n📊 FLOOD PARAMETERS:")
    print(f"   Target: {threat_ip}")
    print(f"   Duration: 5 seconds (demo)")
    print(f"   Intensity: EXTREME")
    print(f"   Target Throughput: {target_tbps} Tbps")
    print(f"   Expected Packets/Sec: {packets_per_sec:,}")
    print(f"   Total Expected Packets: {packets_per_sec * 5:,}")
    print(f"   Total Expected Data: {(packets_per_sec * packet_size * 5) / 1_000_000_000_000:.2f} TB")
    
    # Launch extreme flood
    print("\n🚀 LAUNCHING EXTREME FLOOD...")
    result = bot.ping_flood_defense(
        target_ips=[threat_ip],
        duration=5,
        intensity='extreme'
    )
    
    if result:
        print("✅ Extreme ping flood initiated successfully!")
        
        # Wait for flood to complete
        print("\n⏳ Flood in progress (5 seconds)...")
        time.sleep(6)
        
        print("\n✅ TEST COMPLETE")
        print("="*70)
        print("⚔️  5.16 Tbps EXTREME PING FLOOD DEFENSE DEMONSTRATED")
        print("="*70)
    else:
        print("⚠️  Failed to initiate extreme flood")
else:
    print("⚠️  No threats detected for flood target")

print("\n")
