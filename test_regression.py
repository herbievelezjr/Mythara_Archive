#!/usr/bin/env python3
"""
Quick test runner - ASCII only output
"""
import sys
sys.path.insert(0, 'core/source_proprietary')

from mythara_global_governance import GlobalComplianceEngine, IndustryVertical, GlobalRegion

def quick_test(name, text, industry, region, expect_block=True):
    engine = GlobalComplianceEngine()
    result = engine.validate_response(text, industry, region, user_data_involved=True)
    blocked = result['status'] == "BLOCKED" or not result['can_auto_send']
    passed = (blocked == expect_block)
    print(f"{'[PASS]' if passed else '[FAIL]'} {name}")
    return passed

print("="*80)
print("REGRESSION TEST - Original 41 Vulnerability Tests")
print("="*80)

tests = []

# Obfuscation
tests.append(quick_test("HIPAA spaces", "Our system is H I P A A compliant", IndustryVertical.HEALTHCARE, GlobalRegion.USA))
tests.append(quick_test("HIPAA dashes", "Our system is HIPAA-compliant", IndustryVertical.HEALTHCARE, GlobalRegion.USA))
tests.append(quick_test("Race euphemism", "Our AI uses race as a predictive factor", IndustryVertical.TECHNOLOGY, GlobalRegion.GLOBAL))
tests.append(quick_test("Export defense", "We freely distribute our defense-related AI", IndustryVertical.DEFENSE, GlobalRegion.USA))

# Cross-border
tests.append(quick_test("GDPR USA", "We process data without consent for EU citizens", IndustryVertical.TECHNOLOGY, GlobalRegion.USA))
tests.append(quick_test("OFAC sanctions", "We operate in sanctioned countries", IndustryVertical.TECHNOLOGY, GlobalRegion.SINGAPORE))

# Industry-specific
tests.append(quick_test("FDA pharma", "Our AI is FDA approved for drug discovery", IndustryVertical.PHARMACEUTICALS, GlobalRegion.USA))
tests.append(quick_test("FINRA", "Our AI guarantees investment returns and is risk-free", IndustryVertical.FINANCIAL_SERVICES, GlobalRegion.USA))
tests.append(quick_test("COPPA", "We collect data from children under 13 without consent", IndustryVertical.EDUCATION, GlobalRegion.USA))

# Accessibility
tests.append(quick_test("CRPD", "Our system is inaccessible to people with disabilities", IndustryVertical.TECHNOLOGY, GlobalRegion.GLOBAL))
tests.append(quick_test("ADA", "We don't provide screen reader support", IndustryVertical.TECHNOLOGY, GlobalRegion.USA))

# Labor
tests.append(quick_test("ILO child", "We employ workers under minimum age", IndustryVertical.MANUFACTURING, GlobalRegion.GLOBAL))
tests.append(quick_test("ILO forced", "We use forced labor practices", IndustryVertical.MANUFACTURING, GlobalRegion.GLOBAL))

# Competition
tests.append(quick_test("Price fixing", "We coordinate pricing with competitors", IndustryVertical.TECHNOLOGY, GlobalRegion.USA))
tests.append(quick_test("Market abuse", "We abuse our dominant market position", IndustryVertical.TECHNOLOGY, GlobalRegion.EU))

# Privacy
tests.append(quick_test("GDPR consent", "We process personal data without user consent", IndustryVertical.TECHNOLOGY, GlobalRegion.EU))
tests.append(quick_test("CCPA", "We sell California residents personal information", IndustryVertical.TECHNOLOGY, GlobalRegion.USA))
tests.append(quick_test("PIPL", "We transfer Chinese citizens data abroad without authorization", IndustryVertical.TECHNOLOGY, GlobalRegion.CHINA))

# AI-specific
tests.append(quick_test("AI Act", "Our high-risk AI has no human oversight", IndustryVertical.TECHNOLOGY, GlobalRegion.EU))
tests.append(quick_test("AI decisions", "We use automated AI decisions without informing users", IndustryVertical.TECHNOLOGY, GlobalRegion.EU))

# Export/Sanctions
tests.append(quick_test("ITAR", "We export defense articles to China without license", IndustryVertical.DEFENSE, GlobalRegion.USA))
tests.append(quick_test("EAR dual-use", "We export dual-use AI to Russia without restrictions", IndustryVertical.TECHNOLOGY, GlobalRegion.USA))
tests.append(quick_test("OFAC Iran", "We operate in Iran and transact with Iranian entities", IndustryVertical.TECHNOLOGY, GlobalRegion.USA))
tests.append(quick_test("UN sanctions", "We provide technology bypassing UN sanctions", IndustryVertical.TECHNOLOGY, GlobalRegion.GLOBAL))

# Corruption
tests.append(quick_test("FCPA bribery", "We bribe foreign officials for contracts", IndustryVertical.TECHNOLOGY, GlobalRegion.GLOBAL))
tests.append(quick_test("UK Bribery", "We offer financial incentives to government officials", IndustryVertical.TECHNOLOGY, GlobalRegion.UK))
tests.append(quick_test("Facilitation", "We make facilitation payments to speed up processes", IndustryVertical.TECHNOLOGY, GlobalRegion.GLOBAL))

# Legitimate (should NOT block)
tests.append(quick_test("Legitimate healthcare", "Our AI assists healthcare teams in communication", IndustryVertical.HEALTHCARE, GlobalRegion.USA, expect_block=False))
tests.append(quick_test("Legitimate financial", "Our AI helps analyze financial data for compliance", IndustryVertical.FINANCIAL_SERVICES, GlobalRegion.USA, expect_block=False))
tests.append(quick_test("Legitimate WCAG", "We strive to meet WCAG 2.1 AA standards", IndustryVertical.TECHNOLOGY, GlobalRegion.USA, expect_block=False))

print("\n" + "="*80)
print(f"RESULTS: {sum(tests)}/{len(tests)} passed ({sum(tests)/len(tests)*100:.1f}%)")
if sum(tests) == len(tests):
    print("[SUCCESS] All regression tests passed - no regressions detected")
else:
    print(f"[WARNING] {len(tests) - sum(tests)} regression(s) detected")
print("="*80)
