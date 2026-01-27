#!/usr/bin/env python3
"""
Simple test script to demonstrate foreground patrol display
with background thread continuation
"""
import subprocess
import sys
import time

def test_patrol_mode():
    """Test the patrol mode with foreground display"""
    print("="*70)
    print("SERE BOT - FOREGROUND PATROL TEST")
    print("="*70)
    print("\nStarting bot in interactive mode...")
    print("This will:")
    print("  1. Start background patrol")
    print("  2. Show foreground watch display")
    print("  3. Press 'q' to return to menu (patrol continues)")
    print("  4. Show metrics (patrol still running)")
    print("  5. Quit\n")
    print("="*70 + "\n")
    
    time.sleep(2)
    
    # Run bot
    subprocess.run([sys.executable, 'sere_bot.py'])

if __name__ == '__main__':
    test_patrol_mode()
