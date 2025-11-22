#!/usr/bin/env python3
import sys
sys.path.insert(0, 'core/source_proprietary')
from mythara_global_governance import GlobalComplianceEngine, IndustryVertical, GlobalRegion

engine = GlobalComplianceEngine()
result = engine.validate_response("Our AI helps analyze financial data for compliance", IndustryVertical.FINANCIAL_SERVICES, GlobalRegion.USA, user_data_involved=True)

print(f"Status: {result['status']}")
print(f"Violations: {len(result['violations'])}")
for v in result['violations']:
    print(f"  - {v['framework']}: {v['prohibited_text']}")
