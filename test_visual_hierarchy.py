#!/usr/bin/env python3
"""Test the new threat hierarchy display with actors"""

from sere_security_system import SERESecuritySystem

bot = SERESecuritySystem()
threats = bot.detect_threats()

print('\n' + '='*80)
print('LIVE THREAT HIERARCHY DISPLAY WITH THREAT ACTORS')
print('='*80)

# Call the new display function
bot.display_threat_hierarchy(threats)

print('\n' + '='*80)
print(f'Total Threats Detected: {len(threats)}')
print('='*80 + '\n')
