#!/usr/bin/env python3
"""Test the full S.E.R.E. operational cycle"""

from sere_security_system import SERESecuritySystem

bot = SERESecuritySystem()
threats = bot.detect_threats()

print('\n' + '='*80)
print('FULL S.E.R.E. OPERATIONAL CYCLE TEST')
print('='*80)
print('\nSurvive → Evade → Resist → Escape')
print('='*80)

# Display the complete S.E.R.E. cycle
bot.display_sere_cycle(threats)

print('\n' + '='*80)
print(f'Total Threats Detected: {len(threats)}')
print('='*80)

# Show threat hierarchy
bot.display_threat_hierarchy(threats)

print('\n' + '='*80 + '\n')
