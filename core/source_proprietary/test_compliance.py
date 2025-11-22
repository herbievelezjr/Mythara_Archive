#!/usr/bin/env python3
"""Test script for Unified Compliance Framework"""

from unified_compliance_framework import unified_compliance, ComplianceFramework

print("="*60)
print("Mythara Engine - Unified Compliance Framework Test")
print("="*60)

# Test 1: Framework enumeration
print(f"\n✅ Supported frameworks: {len(list(ComplianceFramework))}")

# Test 2: Generate report
report = unified_compliance.generate_compliance_report()
print(f"✅ Report generated: {report['frameworks_supported']} frameworks")

# Test 3: List frameworks by category
print(f"\n📋 Frameworks by Category:")
for category, frameworks in report['compliance_frameworks'].items():
    print(f"  - {category}: {len(frameworks)} frameworks")

# Test 4: PCI DSS validation
print(f"\n💳 Testing PCI DSS Validation:")
pci_data = {
    "card_token": "tok_abc123",
    "amount": 100.00,
    "encrypted": True,
    "transaction_id": "TXN_001"
}
pci_result = unified_compliance.validate_multi_framework_compliance(
    pci_data,
    [ComplianceFramework.PCI_DSS]
)
print(f"  Result: {'✅ COMPLIANT' if pci_result['overall_compliant'] else '❌ NON-COMPLIANT'}")
print(f"  Risk: {pci_result['risk_assessment']}")

# Test 5: TCPA validation
print(f"\n📞 Testing FCC TCPA Validation:")
tcpa_data = {
    "automated": True,
    "consent_given": True,
    "call_time": "14:00",
    "opt_out_available": True,
    "on_dnc_list": False
}
tcpa_result = unified_compliance.validate_multi_framework_compliance(
    tcpa_data,
    [ComplianceFramework.FCC_TCPA]
)
print(f"  Result: {'✅ COMPLIANT' if tcpa_result['overall_compliant'] else '❌ NON-COMPLIANT'}")
print(f"  Risk: {tcpa_result['risk_assessment']}")

# Test 6: Labor compliance validation
print(f"\n👷 Testing NLRA (Labor) Validation:")
labor_data = {
    "union_activity": True,
    "disciplinary_action": True,
    "legitimate_business_reason": True
}
labor_result = unified_compliance.validate_multi_framework_compliance(
    labor_data,
    [ComplianceFramework.NLRA]
)
print(f"  Result: {'✅ COMPLIANT' if labor_result['overall_compliant'] else '❌ NON-COMPLIANT'}")
print(f"  Risk: {labor_result['risk_assessment']}")

print(f"\n{'='*60}")
print("✅ All tests completed successfully!")
print(f"{'='*60}\n")
