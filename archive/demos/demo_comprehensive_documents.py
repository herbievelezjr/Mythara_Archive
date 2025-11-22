"""
Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

Mythara Gopher - Comprehensive Legal Document Generation Demo
Demonstrates: Complaints, Motions, Discovery, Writs, Affidavits, Subpoenas, etc.
"""

from mythara_gopher_nlp_engine import MytharaGopherNLP

def demo_complaint():
    """Demonstrate complaint (lawsuit) generation"""
    print("\n" + "="*80)
    print("📋 DEMO: CIVIL COMPLAINT")
    print("="*80 + "\n")
    
    gopher = MytharaGopherNLP()
    
    doc = gopher.generate_complaint(
        plaintiff_name="Jane Doe",
        defendant_name="XYZ Corporation",
        court_name="Superior Court of California",
        case_number="CV-2025-001234",
        jurisdiction="County of Los Angeles, State of California",
        causes_of_action=[
            "Wrongful Termination in Violation of Public Policy",
            "Retaliation for Reporting Safety Violations",
            "Breach of Implied Contract"
        ],
        facts="""5. On January 15, 2024, Plaintiff was hired by Defendant as a Safety Inspector.

6. Throughout Plaintiff's employment, Plaintiff observed numerous safety violations
   including inadequate fall protection equipment and blocked emergency exits.

7. On March 10, 2025, Plaintiff reported these violations to management and to OSHA.

8. On March 15, 2025, Defendant terminated Plaintiff's employment citing
   "performance issues" despite Plaintiff's exemplary performance record.

9. Plaintiff's termination was in direct retaliation for reporting safety violations.""",
        damages="""Plaintiff has suffered and continues to suffer damages including but not limited to:

A. Lost wages and benefits: approximately $75,000
B. Future lost earning capacity: $200,000+
C. Emotional distress and mental anguish
D. Loss of professional reputation
E. Medical expenses related to stress-induced conditions: $5,000
F. Punitive damages for willful and malicious conduct""",
        prayer_for_relief="""A. Award compensatory damages according to proof;
B. Award punitive damages to punish Defendant's willful conduct;
C. Award back pay, front pay, and benefits;
D. Award costs of suit and reasonable attorney's fees;
E. Order reinstatement or other equitable relief;"""
    )
    
    print(doc.content)
    print("\n" + "="*80)
    print(f"✅ Complaint generated with SHA-256 hash: {doc.integrity_hash[:16]}...")
    print(f"📄 Document ID: {doc.doc_id}")
    print(f"⏰ Timestamp: {doc.timestamp}")
    print("="*80)

def demo_motion():
    """Demonstrate motion generation"""
    print("\n" + "="*80)
    print("⚖️ DEMO: MOTION TO COMPEL DISCOVERY")
    print("="*80 + "\n")
    
    gopher = MytharaGopherNLP()
    
    doc = gopher.generate_motion(
        motion_type="Motion to Compel Discovery Responses",
        case_caption="Jane Doe v. XYZ Corporation",
        case_number="CV-2025-001234",
        court_name="Superior Court of California, County of Los Angeles",
        moving_party="Plaintiff Jane Doe",
        legal_basis="""Under Federal Rule of Civil Procedure 37(a), a party may move for an order
compelling disclosure or discovery when the opposing party has failed to respond to
properly served discovery requests. The Court may order the party to provide answers
and may award expenses including attorney's fees incurred in making the motion.""",
        argument="""I. Defendant Has Failed to Respond to Plaintiff's Discovery Requests

On October 1, 2025, Plaintiff served Defendant with Interrogatories (Set One) and
Request for Production of Documents (Set One). To date, Defendant has not served
responses despite the 30-day deadline having expired on November 1, 2025.

II. Plaintiff Made Good Faith Efforts to Obtain Responses

Counsel for Plaintiff sent meet-and-confer letters on November 5, 2025 and
November 12, 2025 requesting responses. Defendant's counsel did not respond to
either letter and has not provided any justification for the delay.

III. The Discovery Requests Are Relevant and Not Overly Burdensome

The interrogatories seek basic information about Plaintiff's employment, performance
reviews, and the circumstances of her termination - all directly relevant to this
wrongful termination action. The document requests seek employment records,
performance reviews, and internal communications about safety complaints.""",
        relief_sought="""compelling Defendant XYZ Corporation to serve full and complete responses to
Plaintiff's First Set of Interrogatories and First Request for Production of
Documents within 10 days of the Court's order, and awarding Plaintiff reasonable
attorney's fees and costs incurred in bringing this motion"""
    )
    
    print(doc.content[:1500] + "\n[...content truncated for demo...]\n")
    print("="*80)
    print(f"✅ Motion generated with SHA-256 hash: {doc.integrity_hash[:16]}...")
    print("="*80)

def demo_interrogatories():
    """Demonstrate interrogatories generation"""
    print("\n" + "="*80)
    print("❓ DEMO: INTERROGATORIES (Discovery Questions)")
    print("="*80 + "\n")
    
    gopher = MytharaGopherNLP()
    
    doc = gopher.generate_interrogatories(
        propounding_party="Plaintiff Jane Doe",
        responding_party="Defendant XYZ Corporation",
        case_caption="Jane Doe v. XYZ Corporation",
        case_number="CV-2025-001234",
        interrogatory_questions=[
            "State the name, address, and telephone number of every person who participated in the decision to terminate Plaintiff's employment.",
            "Identify all documents that relate to Plaintiff's job performance during her employment with Defendant.",
            "Describe in detail all reasons for Plaintiff's termination, including the date each reason was identified and the person who identified it.",
            "Identify all complaints or reports made by Plaintiff regarding safety violations, including the date, manner, and content of each complaint.",
            "State whether Defendant conducted an investigation into Plaintiff's safety complaints and if so, describe the scope, findings, and persons involved in such investigation.",
            "Identify all documents related to OSHA complaints, inspections, or citations at the facility where Plaintiff worked from January 2024 to March 2025.",
            "List all employees terminated within 60 days of reporting safety violations to management or regulatory agencies in the past 5 years.",
            "State the amount of any severance pay or benefits offered to Plaintiff.",
            "Identify all witnesses to any events described in the Complaint.",
            "Describe Defendant's policy regarding retaliation against employees who report safety violations."
        ]
    )
    
    print(doc.content[:1200] + "\n[...remaining questions truncated...]\n")
    print("="*80)
    print(f"✅ Interrogatories generated: {doc.metadata['question_count']} questions")
    print(f"📄 SHA-256 hash: {doc.integrity_hash[:16]}...")
    print("="*80)

def demo_request_for_production():
    """Demonstrate request for production"""
    print("\n" + "="*80)
    print("📂 DEMO: REQUEST FOR PRODUCTION OF DOCUMENTS")
    print("="*80 + "\n")
    
    gopher = MytharaGopherNLP()
    
    doc = gopher.generate_request_for_production(
        requesting_party="Plaintiff Jane Doe",
        producing_party="Defendant XYZ Corporation",
        case_caption="Jane Doe v. XYZ Corporation",
        case_number="CV-2025-001234",
        document_requests=[
            "All documents constituting or relating to Plaintiff's personnel file.",
            "All performance evaluations, reviews, or assessments of Plaintiff.",
            "All documents relating to Plaintiff's termination, including emails, memoranda, and notes.",
            "All documents relating to safety complaints or violations at the facility where Plaintiff worked from January 2024 to March 2025.",
            "All communications between Defendant's management and OSHA regarding safety inspections or complaints.",
            "All policies, procedures, or handbooks regarding reporting safety violations.",
            "All documents showing Defendant's policy on retaliation or whistleblower protection.",
            "All communications mentioning Plaintiff by name from March 1, 2025 to March 31, 2025."
        ]
    )
    
    print(doc.content[:1000] + "\n[...remaining requests truncated...]\n")
    print("="*80)
    print(f"✅ RFP generated: {doc.metadata['request_count']} document requests")
    print("="*80)

def demo_affidavit():
    """Demonstrate affidavit generation"""
    print("\n" + "="*80)
    print("✍️ DEMO: AFFIDAVIT (Sworn Statement)")
    print("="*80 + "\n")
    
    gopher = MytharaGopherNLP()
    
    doc = gopher.generate_affidavit(
        affiant_name="Jane Doe",
        case_caption="Jane Doe v. XYZ Corporation",
        case_number="CV-2025-001234",
        statements=[
            "I am the Plaintiff in this action and am over 18 years of age and competent to testify.",
            "I was employed by XYZ Corporation from January 15, 2024 to March 15, 2025 as a Safety Inspector.",
            "During my employment, I consistently received 'Excellent' performance ratings.",
            "On or about March 10, 2025, I submitted a written report to my supervisor detailing multiple safety violations including inadequate fall protection and blocked emergency exits.",
            "I also filed a complaint with OSHA on March 10, 2025 regarding these safety violations.",
            "Five days later, on March 15, 2025, I was called into a meeting and terminated, allegedly for 'performance issues.'",
            "Prior to reporting the safety violations, I had never received any warnings or discipline.",
            "I believe my termination was in direct retaliation for reporting safety violations."
        ],
        purpose="Support Motion for Preliminary Injunction",
        jurisdiction="California"
    )
    
    print(doc.content)
    print("\n" + "="*80)
    print(f"✅ Affidavit generated: {doc.metadata['statement_count']} sworn statements")
    print("="*80)

def demo_subpoena():
    """Demonstrate subpoena generation"""
    print("\n" + "="*80)
    print("📬 DEMO: SUBPOENA DUCES TECUM")
    print("="*80 + "\n")
    
    gopher = MytharaGopherNLP()
    
    doc = gopher.generate_subpoena(
        issuing_party="Plaintiff Jane Doe",
        recipient_name="OSHA Regional Office - Los Angeles",
        case_caption="Jane Doe v. XYZ Corporation",
        case_number="CV-2025-001234",
        court_name="Superior Court of California, County of Los Angeles",
        subpoena_type="duces_tecum",
        appearance_date="January 15, 2026",
        appearance_location="Superior Court of California, 111 N. Hill St, Los Angeles, CA 90012",
        documents_requested=[
            "All complaints filed against XYZ Corporation between January 1, 2024 and December 31, 2025.",
            "All inspection reports for XYZ Corporation's facility located at [address].",
            "All citations issued to XYZ Corporation for safety violations from 2024 to 2025.",
            "All correspondence between OSHA and XYZ Corporation regarding the complaint filed on March 10, 2025."
        ]
    )
    
    print(doc.content)
    print("\n" + "="*80)
    print(f"✅ Subpoena generated for: {doc.metadata['recipient']}")
    print("="*80)

def demo_answer():
    """Demonstrate answer to complaint"""
    print("\n" + "="*80)
    print("📝 DEMO: ANSWER TO COMPLAINT")
    print("="*80 + "\n")
    
    gopher = MytharaGopherNLP()
    
    doc = gopher.generate_answer(
        defendant_name="XYZ Corporation",
        plaintiff_name="Jane Doe",
        case_caption="Jane Doe v. XYZ Corporation",
        case_number="CV-2025-001234",
        court_name="Superior Court of California, County of Los Angeles",
        admissions=["1", "2", "5"],  # Admits paragraphs 1, 2, and 5
        denials=["6", "7", "8", "9", "10", "11", "12"],  # Denies most allegations
        affirmative_defenses=[
            "Statute of Limitations",
            "Failure to State a Claim",
            "At-Will Employment",
            "Legitimate Business Reason",
            "Waiver and Estoppel",
            "Comparative Fault"
        ]
    )
    
    print(doc.content[:1500] + "\n[...content truncated...]\n")
    print("="*80)
    print(f"✅ Answer generated with {doc.metadata['affirmative_defenses_count']} affirmative defenses")
    print("="*80)

def show_menu():
    """Show demo menu"""
    print("\n" + "="*80)
    print("  MYTHARA GOPHER - COMPREHENSIVE LEGAL DOCUMENT GENERATION")
    print("="*80 + "\n")
    
    print("Available Demos:\n")
    print("1. 📋 Civil Complaint (Start a Lawsuit)")
    print("2. ⚖️  Motion to Compel Discovery")
    print("3. ❓ Interrogatories (Discovery Questions)")
    print("4. 📂 Request for Production (RFP)")
    print("5. ✍️  Affidavit (Sworn Statement)")
    print("6. 📬 Subpoena Duces Tecum")
    print("7. 📝 Answer to Complaint")
    print("8. 🎬 Run All Demos")
    print("9. 🚪 Exit\n")
    
    return input("Select (1-9): ").strip()

def main():
    """Run comprehensive document generation demo"""
    while True:
        choice = show_menu()
        
        if choice == "1":
            demo_complaint()
        elif choice == "2":
            demo_motion()
        elif choice == "3":
            demo_interrogatories()
        elif choice == "4":
            demo_request_for_production()
        elif choice == "5":
            demo_affidavit()
        elif choice == "6":
            demo_subpoena()
        elif choice == "7":
            demo_answer()
        elif choice == "8":
            print("\n🎬 Running all demos...\n")
            demo_complaint()
            input("\nPress Enter to continue...")
            demo_motion()
            input("\nPress Enter to continue...")
            demo_interrogatories()
            input("\nPress Enter to continue...")
            demo_request_for_production()
            input("\nPress Enter to continue...")
            demo_affidavit()
            input("\nPress Enter to continue...")
            demo_subpoena()
            input("\nPress Enter to continue...")
            demo_answer()
        elif choice == "9":
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please select 1-9.")
        
        if choice in ["1", "2", "3", "4", "5", "6", "7"]:
            input("\n▶️  Press Enter to return to menu...")

if __name__ == "__main__":
    main()
