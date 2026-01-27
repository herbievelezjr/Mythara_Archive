#!/usr/bin/env python3
"""
Quick fix script for sere_bot.py to remove remaining SLIME/evolutionary references
"""

import re

# Read the file
with open(r'c:\Users\Mythara\Desktop\Clone Repo Mythara\Mythara_Archive\sere_bot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Remove slime_analysis reference block (lines ~2161-2180)
content = re.sub(
    r'if new_ips:\s+print\(f".*?SLIME RESOURCE ALLOCATION.*?"\).*?slime_allocation = slime_analysis\.get.*?print\(f"\s+\u2022 \{ip\}:.*?priority"\).*?print\(f"\s+\u21d2 Flood intensity:.*?"\).*?print\(f"\s+\u21d2 Quarantine:.*?"\)',
    'if new_ips:',
    content,
    flags=re.DOTALL
)

# Fix 2: Replace slime_analysis.get calls with defaults
content = re.sub(r"slime_allocation = slime_analysis\.get\('allocation', \{\}\)", "# SLIME removed", content)
content = re.sub(r"ip_allocation\.get\('ping_flood_intensity', 0\.8\)", "0.8", content)
content = re.sub(r"ip_allocation\.get\('quarantine_duration', 3600\)", "3600", content)
content = re.sub(r"ip_allocation\.get\('monitoring_priority', 'high'\)", "'high'", content)

# Fix 3: Remove any remaining slime_defense references
content = re.sub(r'self\.slime_defense\.\w+\([^)]*\)', '{}', content)

# Fix 4: Remove any remaining evolutionary_engine references  
content = re.sub(r'self\.evolutionary_engine\.\w+\([^)]*\)', 'None', content)

# Fix 5: Clean up the evolutionary analysis block
content = re.sub(
    r'# Evolutionary analysis removed for streamlined operation.*?if False:.*?adaptations = \[\]',
    '# Evolutionary analysis removed for streamlined operation',
    content,
    flags=re.DOTALL
)

# Write the fixed content
with open(r'c:\Users\Mythara\Desktop\Clone Repo Mythara\Mythara_Archive\sere_bot.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed sere_bot.py - removed SLIME/evolutionary references")
print(f"✓ New file size: {len(content.splitlines())} lines")
