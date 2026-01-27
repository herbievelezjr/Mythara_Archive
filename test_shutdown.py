#!/usr/bin/env python3
"""
Test graceful shutdown behavior:
- Start continuous_auto_defense() in a thread
- Trigger shutdown() programmatically
- Verify loop exits and thread joins
"""
import threading
import time
from sere_security_system import SERESecuritySystem

def run_auto_defense(bot: SERESecuritySystem):
    try:
        bot.continuous_auto_defense()
    except Exception as e:
        print(f"auto_defense exception: {e}")


def main():
    bot = SERESecuritySystem()
    t = threading.Thread(target=run_auto_defense, args=(bot,), daemon=True)
    t.start()

    # Let it run briefly
    time.sleep(2)

    print("\n>>> Requesting shutdown() ...")
    bot.shutdown()

    # Give the worker time to notice shutdown and exit
    t.join(timeout=10)
    print(f"Thread alive after shutdown: {t.is_alive()}")
    print(f"shutdown_requested: {bot.shutdown_requested}")
    print("Done.")

if __name__ == "__main__":
    main()
