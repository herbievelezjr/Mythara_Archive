#!/usr/bin/env python3
"""
Demonstrate S.E.R.E. proactive vigilant modes
"""

import sys
import os

sys.path.insert(0, str(os.path.dirname(__file__)))

from sere_security_system import SERESecuritySystem

print("\n" + "="*70)
print("S.E.R.E. PROACTIVE VIGILANT MODES DEMONSTRATION")
print("="*70)

print("""
S.E.R.E. now has THREE proactive modes:

1. 🎖️  PATROL MODE ('patrol' or 'vigilant')
   - Continuously scans for threats every 10 seconds
   - Automatically evades/defends against threats
   - Reports status in real-time
   - Type 'halt-patrol' or Ctrl+C to stop

2. ⚔️  AGGRESSIVE MODE ('aggressive' or 'attack-mode')
   - Rapid threat scanning (every 5 seconds)
   - Immediate offensive response to threats
   - Full aggressive defensive posture
   - Type 'stand-down' or Ctrl+C to stop

3. 🛡️  MANUAL DEFENSE (existing commands)
   - 'defend' - Execute single defense cycle
   - 'detect' - Scan and auto-evade once
   - Still available alongside proactive modes

USAGE IN INTERACTIVE MODE:
""")

print("""
S.E.R.E.> help                    # Show all commands
S.E.R.E.> patrol                  # Start continuous vigilant patrol
S.E.R.E.> aggressive              # Start aggressive auto-defense mode
S.E.R.E.> defend                  # Single defense cycle
S.E.R.E.> detect                  # Scan for threats once
S.E.R.E.> status                  # Check current status
S.E.R.E.> exit                    # Power down

FEATURES:
✓ Ever vigilant - continuous scanning
✓ Proactive defense - threats neutralized automatically
✓ Real-time alerts - immediate notification of threats
✓ Aggressive response - full offensive posture available
✓ Graceful shutdown - can be stopped anytime with Ctrl+C
""")

print("\n" + "="*70)
print("To test, run: python sere_bot.py")
print("Then try: patrol")
print("="*70 + "\n")
