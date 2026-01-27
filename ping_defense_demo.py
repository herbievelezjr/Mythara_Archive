#!/usr/bin/env python3
"""
S.E.R.E. Ping Monitoring Defense Demonstration
"""

from sere_security_system import SERESecuritySystem
import time
import argparse

def demonstrate_ping_defense(ip_list=None):
    """Demonstrate the continuous ping monitoring defense.

    Note: This demo no longer uses public DNS IPs.
    Provide authorized test IPs explicitly via CLI.
    """
    print("🛡️ S.E.R.E. PING MONITORING DEFENSE DEMONSTRATION")
    print("="*60)

    # Create S.E.R.E. Sovereign Security System
    print("\n🎖️ Initializing S.E.R.E. Sovereign Security System...")
    bot = SERESecuritySystem()

    # Start ping monitoring
    print("\n📡 Starting continuous ping monitoring defense...")
    if not ip_list:
        print("⚠️  No IPs provided. Skipping demo. Use --ips <ip1,ip2,...>.")
        return

    success = bot.start_ping_monitoring(ip_list)
    if success:
        print("✓ Ping monitoring defense activated successfully!")
        print("📊 Monitoring will continue indefinitely until stopped...")
        print("   Press Ctrl+C to stop the demonstration")

        try:
            # Let it run for a short demonstration
            time.sleep(10)
        except KeyboardInterrupt:
            print("\n\n⏹️  Demonstration interrupted by user")

        # Stop ping monitoring
        print("\n📡 Stopping ping monitoring defense...")
        bot.stop_ping_monitoring()
        print("✓ Ping monitoring defense deactivated")

    else:
        print("✗ Failed to start ping monitoring defense")

    print("\n" + "="*60)
    print("🏆 PING MONITORING DEFENSE DEMONSTRATION COMPLETE")
    print("="*60)
    print("\nKey Features Demonstrated:")
    print("• Continuous IP address monitoring")
    print("• Automatic ping failure detection")
    print("• Real-time status reporting")
    print("• Integration with S.E.R.E. defense system")
    print("• Indefinite monitoring capability")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="S.E.R.E. Ping Defense Demo")
    parser.add_argument("--ips", type=str, help="Comma-separated list of authorized IPs to monitor")
    args = parser.parse_args()

    ip_list = None
    if args.ips:
        ip_list = [ip.strip() for ip in args.ips.split(',') if ip.strip()]

    demonstrate_ping_defense(ip_list)