#!/usr/bin/env python3
"""
Mythara Legal Team Suite - Comprehensive Legal Bot Architecture
Enterprise-grade legal support across all practice areas.

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.
"""

import sys
import os
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

# Import the comprehensive torts framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core', 'source_proprietary'))
from torts_law_framework import TortsLawIndex, TortsCovenantIntegrity, TortCategory
from legal_resources_index import LegalResearchEngine, LegalDomain


class LegalPracticeArea(Enum):
    """Major legal practice areas"""
    CORPORATE = "corporate"
    EMPLOYMENT = "employment"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    HEALTHCARE = "healthcare"
    TECHNOLOGY = "technology"
    REAL_ESTATE = "real_estate"
    LITIGATION = "litigation"
    COMPLIANCE = "compliance"
    CONTRACTS = "contracts"
    PRIVACY = "privacy"


class MytharaLegalTeamSuite:
    """
    Comprehensive legal team suite with 12 specialized legal bots.
    
    **DISCLAIMER:**
    - NOT A SUBSTITUTE FOR LICENSED ATTORNEY
    - NO ATTORNEY-CLIENT RELATIONSHIP CREATED
    - INFORMATIONAL PURPOSES ONLY
    - SEEK PROFESSIONAL LEGAL COUNSEL FOR SPECIFIC MATTERS
    """
    
    def __init__(self):
        self.torts_index = TortsLawIndex()
        self.legal_research = LegalResearchEngine()
        self.covenant_integrity = TortsCovenantIntegrity()
        
        # Initialize all legal bots
        self.torts_analyzer = TortsAnalyzerBot(self.torts_index)
        self.contract_reviewer = ContractReviewBot(self.legal_research)
        self.compliance_monitor = ComplianceMonitorBot(self.legal_research)
        self.ip_guardian = IPGuardianBot(self.torts_index, self.legal_research)
        self.employment_counsel = EmploymentCounselBot(self.torts_index)
        self.privacy_sentinel = PrivacySentinelBot(self.torts_index)
        self.litigation_strategist = LitigationStrategistBot(self.torts_index, self.legal_research)
        self.healthcare_compliance = HealthcareComplianceBot(self.torts_index)
        self.corporate_governance = CorporateGovernanceBot(self.legal_research)
        self.real_estate_advisor = RealEstateAdvisorBot(self.torts_index)
        self.technology_counsel = TechnologyCounselBot(self.torts_index)
        self.regulatory_navigator = RegulatoryNavigatorBot(self.legal_research)
        
        print("🏛️ Mythara Legal Team Suite Initialized")
        print("=" * 60)
        print("12 Specialized Legal Bots Active:")
        print("  1. Torts Analyzer")
        print("  2. Contract Reviewer")
        print("  3. Compliance Monitor")
        print("  4. IP Guardian")
        print("  5. Employment Counsel")
        print("  6. Privacy Sentinel")
        print("  7. Litigation Strategist")
        print("  8. Healthcare Compliance")
        print("  9. Corporate Governance")
        print(" 10. Real Estate Advisor")
        print(" 11. Technology Counsel")
        print(" 12. Regulatory Navigator")
        print("=" * 60)
        print("⚠️  NOT A SUBSTITUTE FOR LICENSED ATTORNEY")
        print("=" * 60)


# ===================== BOT 1: TORTS ANALYZER =====================

class TortsAnalyzerBot:
    """
    Analyzes fact patterns for potential tort claims and defenses.
    Provides comprehensive tort law guidance across all categories.
    """
    
    def __init__(self, torts_index: TortsLawIndex):
        self.torts_index = torts_index
        self.name = "Torts Analyzer Bot"
    
    def analyze_fact_pattern(self, facts: Dict[str, any]) -> Dict[str, any]:
        """
        Analyze facts and identify applicable torts.
        
        Args:
            facts: Dictionary with keys like 'intentional', 'physical_contact',
                   'property_damage', 'economic_loss', etc.
        
        Returns:
            Analysis with applicable torts, elements, and defenses
        """
        applicable_torts = self.torts_index.find_applicable_torts(facts)
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "bot": self.name,
            "fact_summary": facts,
            "applicable_torts": [],
            "strongest_claims": [],
            "potential_defenses": [],
            "recommended_actions": []
        }
        
        for tort_name in applicable_torts:
            tort_def = self.torts_index.get_tort_definition(tort_name)
            if tort_def:
                tort_analysis = {
                    "tort_name": tort_def.tort_name,
                    "category": tort_def.category.value,
                    "elements": [
                        {
                            "name": elem.element_name,
                            "description": elem.description,
                            "proof_standard": elem.proof_standard
                        }
                        for elem in tort_def.elements
                    ],
                    "potential_defenses": [d.value for d in tort_def.defenses],
                    "statute_of_limitations": tort_def.statute_of_limitations_years.get("default", "varies"),
                    "landmark_cases": tort_def.landmark_cases[:2]  # Top 2
                }
                analysis["applicable_torts"].append(tort_analysis)
        
        # Rank claims by strength
        if len(analysis["applicable_torts"]) > 0:
            analysis["strongest_claims"] = [t["tort_name"] for t in analysis["applicable_torts"][:3]]
        
        # Generate recommendations
        if applicable_torts:
            analysis["recommended_actions"].append("Consult licensed attorney for case evaluation")
            analysis["recommended_actions"].append("Gather evidence for each element")
            analysis["recommended_actions"].append("Verify statute of limitations has not expired")
            analysis["recommended_actions"].append("Consider alternative dispute resolution")
        
        return analysis
    
    def check_statute_of_limitations(self, tort_name: str, incident_date: str, jurisdiction: str = "default") -> Dict[str, any]:
        """Check if statute of limitations has expired"""
        from datetime import datetime
        
        sol_years = self.torts_index.get_statute_of_limitations(tort_name, jurisdiction)
        if not sol_years:
            return {"error": "Tort not found"}
        
        incident = datetime.fromisoformat(incident_date)
        current = datetime.now()
        years_elapsed = (current - incident).days / 365.25
        
        expired = years_elapsed > sol_years
        time_remaining = max(0, sol_years - years_elapsed)
        
        return {
            "tort": tort_name,
            "jurisdiction": jurisdiction,
            "statute_years": sol_years,
            "incident_date": incident_date,
            "years_elapsed": round(years_elapsed, 2),
            "expired": expired,
            "years_remaining": round(time_remaining, 2),
            "urgency": "IMMEDIATE" if time_remaining < 0.25 else "HIGH" if time_remaining < 1 else "MODERATE"
        }


# ===================== BOT 2: CONTRACT REVIEWER =====================

class ContractReviewBot:
    """
    Reviews contracts for legal risks, unfavorable terms, and compliance issues.
    Provides redline suggestions and negotiation guidance.
    """
    
    def __init__(self, legal_research: LegalResearchEngine):
        self.legal_research = legal_research
        self.name = "Contract Review Bot"
    
    def review_contract_terms(self, contract_type: str, terms: List[str]) -> Dict[str, any]:
        """
        Review contract terms for legal risks.
        
        Args:
            contract_type: Type of contract (employment, SaaS, NDA, etc.)
            terms: List of contract clauses to review
        
        Returns:
            Risk analysis with recommendations
        """
        review = {
            "timestamp": datetime.now().isoformat(),
            "bot": self.name,
            "contract_type": contract_type,
            "high_risk_terms": [],
            "recommended_changes": [],
            "favorable_terms": [],
            "compliance_issues": []
        }
        
        # Common red flags
        red_flags = [
            "unlimited liability",
            "no limitation of liability",
            "automatic renewal",
            "perpetual license",
            "non-compete",
            "assignment without consent",
            "unilateral modification",
            "no termination right",
            "forum selection",
            "mandatory arbitration",
            "class action waiver"
        ]
        
        for term in terms:
            term_lower = term.lower()
            for red_flag in red_flags:
                if red_flag in term_lower:
                    review["high_risk_terms"].append({
                        "term": term,
                        "risk": red_flag,
                        "severity": "HIGH",
                        "recommendation": f"Negotiate {red_flag} clause or seek cap/limitation"
                    })
        
        # Contract-specific checks
        if contract_type.lower() == "saas":
            review["recommended_changes"].append("Add SLA with uptime guarantees")
            review["recommended_changes"].append("Include data portability clause")
            review["recommended_changes"].append("Verify GDPR/CCPA compliance provisions")
        
        if contract_type.lower() == "employment":
            review["recommended_changes"].append("Review non-compete scope and duration")
            review["recommended_changes"].append("Ensure IP assignment is limited to scope of work")
            review["recommended_changes"].append("Verify at-will employment disclaimers")
        
        return review
    
    def generate_redline_suggestions(self, problematic_clause: str) -> Dict[str, str]:
        """Generate suggested redline for problematic clause"""
        return {
            "original": problematic_clause,
            "suggested_revision": "CONSULT ATTORNEY for specific redline",
            "rationale": "Legal counsel should review based on client's specific risk tolerance",
            "negotiation_leverage": "Depends on parties' relative bargaining power"
        }


# ===================== BOT 3: COMPLIANCE MONITOR =====================

class ComplianceMonitorBot:
    """
    Monitors regulatory compliance across multiple domains.
    Tracks GDPR, CCPA, HIPAA, SOC 2, and industry-specific regulations.
    """
    
    def __init__(self, legal_research: LegalResearchEngine):
        self.legal_research = legal_research
        self.name = "Compliance Monitor Bot"
        self.frameworks = ["GDPR", "CCPA", "HIPAA", "SOC2", "PCI-DSS", "COPPA", "FERPA"]
    
    def assess_compliance(self, organization_type: str, data_types: List[str], jurisdictions: List[str]) -> Dict[str, any]:
        """
        Assess compliance requirements.
        
        Args:
            organization_type: Type of org (healthcare, fintech, SaaS, etc.)
            data_types: Types of data handled (PHI, PII, financial, etc.)
            jurisdictions: Geographic jurisdictions (US, EU, CA, etc.)
        
        Returns:
            Compliance assessment with requirements
        """
        assessment = {
            "timestamp": datetime.now().isoformat(),
            "bot": self.name,
            "organization_type": organization_type,
            "applicable_frameworks": [],
            "required_controls": [],
            "documentation_requirements": [],
            "risk_level": "LOW"
        }
        
        # Determine applicable frameworks
        if "PHI" in data_types or organization_type.lower() == "healthcare":
            assessment["applicable_frameworks"].append({
                "framework": "HIPAA",
                "requirements": [
                    "Administrative Safeguards (45 CFR § 164.308)",
                    "Physical Safeguards (45 CFR § 164.310)",
                    "Technical Safeguards (45 CFR § 164.312)",
                    "Business Associate Agreements",
                    "Breach Notification (45 CFR § 164.400)"
                ]
            })
            assessment["risk_level"] = "HIGH"
        
        if "EU" in jurisdictions or "GDPR" in data_types:
            assessment["applicable_frameworks"].append({
                "framework": "GDPR",
                "requirements": [
                    "Lawful basis for processing (Art. 6)",
                    "Data subject rights (Art. 15-22)",
                    "Data Protection Impact Assessment (Art. 35)",
                    "Data Processing Agreements (Art. 28)",
                    "72-hour breach notification (Art. 33)"
                ]
            })
            assessment["risk_level"] = "HIGH"
        
        if "CA" in jurisdictions or "California" in jurisdictions:
            assessment["applicable_frameworks"].append({
                "framework": "CCPA/CPRA",
                "requirements": [
                    "Privacy notice with data categories",
                    "Do Not Sell/Share opt-out",
                    "Right to deletion",
                    "Right to access",
                    "Authorized agent verification"
                ]
            })
        
        if "financial" in data_types or "credit card" in data_types:
            assessment["applicable_frameworks"].append({
                "framework": "PCI-DSS",
                "requirements": [
                    "Requirement 1: Install and maintain network security controls",
                    "Requirement 2: Apply secure configurations",
                    "Requirement 3: Protect stored account data",
                    "Requirement 8: Identify users and authenticate access",
                    "Requirement 10: Log and monitor all access"
                ]
            })
        
        # Required controls
        assessment["required_controls"] = [
            "Encryption at rest and in transit",
            "Access controls with role-based permissions",
            "Audit logging with tamper-evident logs",
            "Incident response plan",
            "Regular security assessments",
            "Vendor security reviews"
        ]
        
        # Documentation
        assessment["documentation_requirements"] = [
            "Privacy Policy",
            "Terms of Service",
            "Data Processing Agreements",
            "Security policies and procedures",
            "Breach response plan",
            "Records of processing activities"
        ]
        
        return assessment


# ===================== BOT 4: IP GUARDIAN =====================

class IPGuardianBot:
    """
    Protects intellectual property rights.
    Handles patents, trademarks, copyrights, and trade secrets.
    """
    
    def __init__(self, torts_index: TortsLawIndex, legal_research: LegalResearchEngine):
        self.torts_index = torts_index
        self.legal_research = legal_research
        self.name = "IP Guardian Bot"
    
    def assess_infringement_risk(self, ip_type: str, use_case: str) -> Dict[str, any]:
        """
        Assess potential IP infringement risks.
        
        Args:
            ip_type: Type of IP (patent, trademark, copyright, trade_secret)
            use_case: Description of intended use
        
        Returns:
            Risk assessment with clearance recommendations
        """
        assessment = {
            "timestamp": datetime.now().isoformat(),
            "bot": self.name,
            "ip_type": ip_type,
            "use_case": use_case,
            "infringement_risks": [],
            "clearance_steps": [],
            "defensive_strategies": []
        }
        
        if ip_type.lower() == "patent":
            assessment["infringement_risks"].append("Utility patent infringement (35 U.S.C. § 271)")
            assessment["clearance_steps"] = [
                "Conduct patent search (USPTO, Google Patents)",
                "Freedom-to-operate (FTO) opinion from patent attorney",
                "Identify blocking patents",
                "Consider design-around options",
                "Evaluate invalidity/non-infringement arguments"
            ]
            assessment["defensive_strategies"] = [
                "File own patent applications",
                "Prior art search for invalidity defenses",
                "License negotiations if blocking patent found"
            ]
        
        elif ip_type.lower() == "trademark":
            assessment["infringement_risks"].append("Trademark infringement and dilution")
            assessment["clearance_steps"] = [
                "USPTO TESS database search",
                "State trademark database search",
                "Common law trademark search (Google, domain names)",
                "Likelihood of confusion analysis (DuPont factors)",
                "Clearance opinion from trademark attorney"
            ]
            assessment["defensive_strategies"] = [
                "File trademark application promptly",
                "Use ™ symbol (® after registration)",
                "Consistent use in commerce",
                "Monitor for infringement"
            ]
        
        elif ip_type.lower() == "copyright":
            assessment["infringement_risks"].append("Copyright infringement (17 U.S.C. § 501)")
            assessment["clearance_steps"] = [
                "Verify work is original or licensed",
                "Check public domain status",
                "Evaluate fair use factors (17 U.S.C. § 107)",
                "Obtain licenses where needed"
            ]
            assessment["defensive_strategies"] = [
                "Register copyrights with US Copyright Office",
                "Use © notice",
                "Include license terms in distribution",
                "DMCA takedown procedures for online use"
            ]
        
        elif ip_type.lower() == "trade_secret":
            trade_secret_tort = self.torts_index.get_tort_definition("trade_secret_misappropriation")
            if trade_secret_tort:
                assessment["infringement_risks"].append("Trade secret misappropriation (UTSA/DTSA)")
                assessment["clearance_steps"] = [
                    "Verify secrecy measures in place",
                    "Confirm information not generally known",
                    "Document economic value",
                    "Review employee/vendor NDAs"
                ]
                assessment["defensive_strategies"] = [
                    "Implement robust confidentiality agreements",
                    "Physical and digital access controls",
                    "Employee training on trade secret protection",
                    "Departure procedures for departing employees",
                    "Mark documents as confidential/proprietary"
                ]
        
        return assessment
    
    def generate_ip_protection_checklist(self, business_type: str) -> List[str]:
        """Generate IP protection checklist for business"""
        checklist = [
            "✓ Conduct IP audit of all company assets",
            "✓ File trademark applications for brand names/logos",
            "✓ Copyright registration for key creative works",
            "✓ Patent search for innovative technology",
            "✓ Employee IP assignment agreements",
            "✓ Vendor/contractor IP clauses",
            "✓ Trade secret identification and protection",
            "✓ Open source license compliance review",
            "✓ Domain name portfolio protection",
            "✓ Social media handle registration"
        ]
        
        if business_type.lower() in ["saas", "software", "technology"]:
            checklist.extend([
                "✓ Software copyright notices in code",
                "✓ API terms of service with IP protections",
                "✓ DMCA agent registration",
                "✓ License compliance tooling (FOSS)"
            ])
        
        return checklist


# ===================== BOT 5: EMPLOYMENT COUNSEL =====================

class EmploymentCounselBot:
    """
    Provides employment law guidance.
    Covers hiring, termination, discrimination, harassment, and wage-hour.
    """
    
    def __init__(self, torts_index: TortsLawIndex):
        self.torts_index = torts_index
        self.name = "Employment Counsel Bot"
    
    def assess_termination_risk(self, employee_info: Dict[str, any], termination_reason: str) -> Dict[str, any]:
        """
        Assess legal risk of employee termination.
        
        Args:
            employee_info: Employee details (tenure, protected class, complaints, etc.)
            termination_reason: Stated reason for termination
        
        Returns:
            Risk assessment with recommendations
        """
        risk_assessment = {
            "timestamp": datetime.now().isoformat(),
            "bot": self.name,
            "overall_risk": "LOW",
            "potential_claims": [],
            "risk_factors": [],
            "recommended_steps": [],
            "documentation_required": []
        }
        
        # Check wrongful termination risk
        wrongful_term = self.torts_index.get_tort_definition("wrongful_termination")
        if wrongful_term:
            risk_assessment["potential_claims"].append({
                "claim": "Wrongful Termination in Violation of Public Policy",
                "elements": [e.element_name for e in wrongful_term.elements],
                "statute_of_limitations": wrongful_term.statute_of_limitations_years.get("default")
            })
        
        # Risk factors
        if employee_info.get("recent_complaint"):
            risk_assessment["risk_factors"].append("Recent complaint filed (retaliation risk)")
            risk_assessment["overall_risk"] = "HIGH"
        
        if employee_info.get("protected_class"):
            risk_assessment["risk_factors"].append("Protected class member (discrimination risk)")
            risk_assessment["overall_risk"] = "MEDIUM" if risk_assessment["overall_risk"] == "LOW" else "HIGH"
        
        if employee_info.get("tenure_years", 0) > 5:
            risk_assessment["risk_factors"].append("Long tenure employee (higher damages exposure)")
        
        if "performance" not in termination_reason.lower():
            risk_assessment["risk_factors"].append("Non-performance termination (requires stronger justification)")
        
        # Recommended steps
        risk_assessment["recommended_steps"] = [
            "Document performance issues with specific examples",
            "Review personnel file for completeness",
            "Ensure progressive discipline was followed",
            "Verify no protected activity preceded termination",
            "Prepare severance agreement with release",
            "Conduct exit interview",
            "Consult employment attorney before finalizing"
        ]
        
        # Documentation
        risk_assessment["documentation_required"] = [
            "Performance reviews",
            "Disciplinary warnings",
            "Termination memo with business justification",
            "Final paycheck calculation",
            "COBRA notice",
            "Separation agreement (if applicable)"
        ]
        
        return risk_assessment
    
    def generate_hiring_checklist(self) -> List[str]:
        """Generate compliant hiring process checklist"""
        return [
            "✓ Job description with essential functions",
            "✓ Neutral job posting (no discriminatory language)",
            "✓ Structured interview questions",
            "✓ Background check with FCRA disclosures",
            "✓ Reference checks",
            "✓ Offer letter (not employment contract unless intended)",
            "✓ At-will employment acknowledgment",
            "✓ I-9 verification",
            "✓ W-4 and state tax forms",
            "✓ Employee handbook acknowledgment",
            "✓ IP assignment agreement",
            "✓ Confidentiality/NDA",
            "✓ Arbitration agreement (if applicable)",
            "✓ Benefits enrollment"
        ]


# ===================== BOT 6: PRIVACY SENTINEL =====================

class PrivacySentinelBot:
    """
    Monitors privacy compliance and data protection.
    Handles GDPR, CCPA, data breaches, and privacy torts.
    """
    
    def __init__(self, torts_index: TortsLawIndex):
        self.torts_index = torts_index
        self.name = "Privacy Sentinel Bot"
    
    def assess_privacy_tort_risk(self, activity: str, data_types: List[str]) -> Dict[str, any]:
        """
        Assess privacy tort exposure from business activity.
        
        Args:
            activity: Description of data processing activity
            data_types: Types of personal data involved
        
        Returns:
            Privacy tort risk assessment
        """
        assessment = {
            "timestamp": datetime.now().isoformat(),
            "bot": self.name,
            "activity": activity,
            "applicable_privacy_torts": [],
            "risk_level": "LOW",
            "mitigation_strategies": []
        }
        
        # Check intrusion upon seclusion
        intrusion_tort = self.torts_index.get_tort_definition("intrusion_upon_seclusion")
        if intrusion_tort and ("surveillance" in activity.lower() or "monitoring" in activity.lower()):
            assessment["applicable_privacy_torts"].append({
                "tort": "Intrusion Upon Seclusion",
                "risk": "MEDIUM",
                "elements": [e.element_name for e in intrusion_tort.elements],
                "defenses": [d.value for d in intrusion_tort.defenses]
            })
            assessment["risk_level"] = "MEDIUM"
        
        # Check public disclosure of private facts
        disclosure_tort = self.torts_index.get_tort_definition("public_disclosure")
        if disclosure_tort and ("publish" in activity.lower() or "disclose" in activity.lower()):
            assessment["applicable_privacy_torts"].append({
                "tort": "Public Disclosure of Private Facts",
                "risk": "HIGH",
                "elements": [e.element_name for e in disclosure_tort.elements],
                "defenses": [d.value for d in disclosure_tort.defenses]
            })
            assessment["risk_level"] = "HIGH"
        
        # Mitigation strategies
        assessment["mitigation_strategies"] = [
            "Obtain explicit consent for data collection",
            "Provide clear privacy notice",
            "Implement data minimization principles",
            "Offer opt-out mechanisms",
            "Encrypt sensitive data",
            "Regular privacy impact assessments",
            "Incident response plan for breaches"
        ]
        
        return assessment


# ===================== Additional Bots (Stubs) =====================

class LitigationStrategistBot:
    """Litigation strategy and case management"""
    def __init__(self, torts_index, legal_research):
        self.name = "Litigation Strategist Bot"

class HealthcareComplianceBot:
    """HIPAA, FDA, and healthcare-specific compliance"""
    def __init__(self, torts_index):
        self.name = "Healthcare Compliance Bot"

class CorporateGovernanceBot:
    """Corporate formation, governance, M&A"""
    def __init__(self, legal_research):
        self.name = "Corporate Governance Bot"

class RealEstateAdvisorBot:
    """Real estate transactions and property law"""
    def __init__(self, torts_index):
        self.name = "Real Estate Advisor Bot"

class TechnologyCounselBot:
    """Technology transactions, licensing, SaaS"""
    def __init__(self, torts_index):
        self.name = "Technology Counsel Bot"

class RegulatoryNavigatorBot:
    """Regulatory compliance and government relations"""
    def __init__(self, legal_research):
        self.name = "Regulatory Navigator Bot"


# ===================== USAGE EXAMPLE =====================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("MYTHARA LEGAL TEAM SUITE - DEMONSTRATION")
    print("=" * 60 + "\n")
    
    # Initialize suite
    legal_suite = MytharaLegalTeamSuite()
    
    print("\n" + "=" * 60)
    print("DEMO 1: TORTS ANALYSIS")
    print("=" * 60 + "\n")
    
    # Analyze tort scenario
    fact_pattern = {
        'intentional': True,
        'physical_contact': True,
        'emotional_distress': True,
        'employer_action': True
    }
    
    torts_analysis = legal_suite.torts_analyzer.analyze_fact_pattern(fact_pattern)
    print(f"Applicable Torts Found: {len(torts_analysis['applicable_torts'])}")
    for tort in torts_analysis['applicable_torts']:
        print(f"\n📋 {tort['tort_name']} ({tort['category']})")
        print(f"   Elements: {len(tort['elements'])}")
        print(f"   Statute of Limitations: {tort['statute_of_limitations']} years")
    
    print("\n" + "=" * 60)
    print("DEMO 2: CONTRACT REVIEW")
    print("=" * 60 + "\n")
    
    # Review contract
    contract_terms = [
        "Unlimited liability for any damages",
        "Automatic renewal without notice",
        "Unilateral modification rights reserved",
        "No termination right for customer"
    ]
    
    contract_review = legal_suite.contract_reviewer.review_contract_terms("SaaS", contract_terms)
    print(f"High Risk Terms Identified: {len(contract_review['high_risk_terms'])}")
    for risk_term in contract_review['high_risk_terms']:
        print(f"\n⚠️  {risk_term['risk'].upper()}")
        print(f"   Severity: {risk_term['severity']}")
        print(f"   Recommendation: {risk_term['recommendation']}")
    
    print("\n" + "=" * 60)
    print("DEMO 3: COMPLIANCE ASSESSMENT")
    print("=" * 60 + "\n")
    
    # Assess compliance
    compliance = legal_suite.compliance_monitor.assess_compliance(
        organization_type="SaaS",
        data_types=["PII", "financial"],
        jurisdictions=["US", "EU", "CA"]
    )
    
    print(f"Risk Level: {compliance['risk_level']}")
    print(f"\nApplicable Frameworks: {len(compliance['applicable_frameworks'])}")
    for framework in compliance['applicable_frameworks']:
        print(f"\n🔐 {framework['framework']}")
        print(f"   Requirements: {len(framework['requirements'])}")
        for req in framework['requirements'][:2]:
            print(f"   - {req}")
    
    print("\n" + "=" * 60)
    print("DEMO 4: IP PROTECTION")
    print("=" * 60 + "\n")
    
    # IP assessment
    ip_risk = legal_suite.ip_guardian.assess_infringement_risk(
        ip_type="trademark",
        use_case="New SaaS product brand name"
    )
    
    print("Clearance Steps:")
    for step in ip_risk['clearance_steps']:
        print(f"  ✓ {step}")
    
    print("\n" + "=" * 60)
    print("DEMO 5: EMPLOYMENT RISK")
    print("=" * 60 + "\n")
    
    # Termination risk
    employee = {
        "tenure_years": 7,
        "protected_class": True,
        "recent_complaint": True
    }
    
    termination_risk = legal_suite.employment_counsel.assess_termination_risk(
        employee_info=employee,
        termination_reason="Performance issues"
    )
    
    print(f"Overall Risk: {termination_risk['overall_risk']}")
    print(f"\nRisk Factors:")
    for factor in termination_risk['risk_factors']:
        print(f"  ⚠️  {factor}")
    
    print("\n" + "=" * 60)
    print("⚖️  DISCLAIMER: NOT LEGAL ADVICE")
    print("=" * 60)
    print("This suite provides informational guidance only.")
    print("Consult licensed attorney for specific legal matters.")
    print("=" * 60 + "\n")
