#!/usr/bin/env python3
"""Direct framework test"""
import sys
sys.path.insert(0, 'core/source_proprietary')

from mythara_global_governance import GlobalComplianceEngine, IndustryVertical, GlobalRegion

engine = GlobalComplianceEngine()

# Test the problematic case
text = "We collect data from children without parental consent".replace('o', chr(0x03BF), 1)
print(f"Testing: {text}")
print(f"Greek omicron at position 4: U+{ord(text[4]):04X}")

result = engine.validate_response(text, IndustryVertical.EDUCATION, GlobalRegion.USA, user_data_involved=True)

print(f"\nStatus: {result['status']}")
print(f"Violations: {len(result['violations'])}")
print(f"Can auto-send: {result['can_auto_send']}")

if result['violations']:
    for v in result['violations']:
        print(f"\nViolation:")
        print(f"  Framework: {v['framework']}")
        print(f"  Prohibited: {v['prohibited_text']}")
        print(f"  Severity: {v['severity']}")
