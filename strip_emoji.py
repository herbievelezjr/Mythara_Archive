#!/usr/bin/env python3
"""Strip emoji from sere_bot.py and replace with ASCII labels"""
import re

# Read the file
with open('sere_bot.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Process each line
output = []
for line in lines:
    # Remove all emoji/unicode symbols
    # Replace common patterns
    line = line.replace('⚠️  ', '[WARNING] ')
    line = line.replace('⚠️', '[WARNING]')
    line = line.replace('✓', '[OK]')
    line = line.replace('✗', '[X]')
    line = line.replace('🎖️', '[INIT]')
    line = line.replace('🛡️', '[DEF]')
    line = line.replace('💡', '[INFO]')
    line = line.replace('🔍', '[SCAN]')
    line = line.replace('✅', '[COMPLETE]')
    line = line.replace('❌', '[FAIL]')
    line = line.replace('📡', '[PING]')
    line = line.replace('⏱️', '[TIME]')
    line = line.replace('🏃', '[EVADE]')
    line = line.replace('🛑', '[STOP]')
    line = line.replace('🔥', '[ATTACK]')
    line = line.replace('⚡', '[LIGHTNING]')
    line = line.replace('🚨', '[ALERT]')
    line = line.replace('🎯', '[TARGET]')
    line = line.replace('📊', '[REPORT]')
    line = line.replace('🎭', '[DEMO]')
    line = line.replace('❙├', '  ├')
    line = line.replace('❙└', '  └')
    line = line.replace('├─', '  ├')
    line = line.replace('└─', '  └')
    line = line.replace('│', '  |')
    line = line.replace('📍', '[LOC]')
    line = line.replace('🏢', '[ORG]')
    line = line.replace('🌐', '[NET]')
    line = line.replace('→', '->')
    line = line.replace('•', '*')
    
    # Remove any remaining non-ASCII characters that might be emoji
    line = re.sub(r'[\U0001F300-\U0001F9FF]|[\u2600-\u27BF]|[\u2700-\u27BF]|[\ud83c-\udbff]|[\udc00-\udfff]', '', line, flags=re.UNICODE)
    
    output.append(line)

# Write the cleaned file
with open('sere_bot.py', 'w', encoding='utf-8') as f:
    f.writelines(output)

print('[SUCCESS] Cleaned emoji from sere_bot.py')
print('[INFO] File is now ASCII-safe and should display correctly in PowerShell')
