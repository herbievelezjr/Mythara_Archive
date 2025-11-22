"""
Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

Mythara Engine - Document Generation Demo
Demonstrates SHA-256 cryptographic timestamping and legal document production
"""

from mythara_gopher_nlp_engine import MytharaGopherNLP
import os

def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def demo_demand_letter(gopher: MytharaGopherNLP):
    """Demo: Generate demand letter with SHA-256 timestamp"""
    print_section("📨 DEMAND LETTER GENERATION")
    
    print("Generating demand letter for unlawfully withheld security deposit...")
    
    doc = gopher.generate_demand_letter(
        sender_name="Jane Smith",
        sender_address="789 Tenant Street, Apt 4B\nAustin, TX 78701",
        recipient_name="ABC Property Management",
        recipient_address="456 Landlord Plaza\nAustin, TX 78702",
        incident_description=(
            "I rented the property at 789 Tenant Street, Apt 4B from January 1, 2024 through "
            "October 31, 2024. Upon move-out, I provided 30 days notice, cleaned the unit "
            "professionally, and returned keys on October 31st. The unit passed the final inspection "
            "with no damages noted. Despite Texas law requiring security deposit return within 30 days, "
            "I have not received my $1,800 security deposit or any itemized accounting as of December 15, 2024."
        ),
        legal_basis=[
            "Violation of Texas Property Code § 92.109 (security deposit return requirements)",
            "Bad faith retention of security deposit",
            "Breach of lease agreement deposit return clause",
            "Constructive conversion of tenant funds"
        ],
        damages_claimed=(
            "$1,800 (security deposit) + $3,600 (statutory penalty - 3x deposit per TX Property Code § 92.109) "
            "+ $100/day statutory damages from day 31 (45 days = $4,500) + attorney fees + court costs. "
            "Total damages claimed: $9,900"
        ),
        deadline_days=30
    )
    
    # Save to file
    filepath = doc.to_file()
    
    print(f"✅ Document generated successfully!")
    print(f"📄 File saved to: {filepath}")
    print(f"🔒 SHA-256 Hash: {doc.integrity_hash}")
    print(f"⏱️  Timestamp: {doc.timestamp}")
    print(f"\n📋 Document Preview (first 500 chars):\n")
    print("-" * 80)
    print(doc.content[:500] + "...")
    print("-" * 80)

def demo_cease_and_desist(gopher: MytharaGopherNLP):
    """Demo: Generate cease and desist letter"""
    print_section("🛑 CEASE & DESIST LETTER GENERATION")
    
    print("Generating cease and desist for copyright infringement...")
    
    doc = gopher.generate_cease_and_desist(
        sender_name="Mythara Inc.",
        recipient_name="CopyCat Software LLC",
        infringing_conduct=(
            "Your company has reproduced, distributed, and publicly displayed copyrighted software code "
            "from our Mythara Engine product without authorization. Specifically:\n"
            "1. Your product 'GopherClone' uses identical algorithms from our Soul Cradle framework\n"
            "2. You have copied our proprietary paradox detection methodology\n"
            "3. Your marketing materials use screenshots from our documentation\n"
            "4. You are using our trademarked name 'Mythara' in your advertising"
        ),
        legal_violations=[
            "Copyright infringement under 17 U.S.C. § 106 (unauthorized reproduction and distribution)",
            "Trademark infringement under 15 U.S.C. § 1114 (use of registered trademark)",
            "Violation of Digital Millennium Copyright Act (DMCA) 17 U.S.C. § 1201",
            "Misappropriation of trade secrets under Uniform Trade Secrets Act",
            "Unfair competition and false advertising"
        ]
    )
    
    filepath = doc.to_file()
    
    print(f"✅ Cease & Desist generated successfully!")
    print(f"📄 File saved to: {filepath}")
    print(f"🔒 SHA-256 Hash: {doc.integrity_hash}")
    print(f"⏱️  Timestamp: {doc.timestamp}")

def demo_evidence_summary(gopher: MytharaGopherNLP):
    """Demo: Generate evidence summary with chain of custody"""
    print_section("📋 EVIDENCE SUMMARY WITH CHAIN OF CUSTODY")
    
    print("Creating evidence summary for wrongful termination case...")
    
    evidence_items = [
        {
            "description": "Email from supervisor dated 2024-10-15 stating 'You're fired for reporting safety violations'",
            "type": "Email communication",
            "source": "Company email server (Outlook)",
            "date_obtained": "2024-10-15",
            "custodian": "Jane Smith (employee)",
            "relevance": "Direct evidence of retaliatory termination"
        },
        {
            "description": "Voicemail from HR threatening termination if OSHA complaint not withdrawn",
            "type": "Audio recording",
            "source": "iPhone voicemail",
            "date_obtained": "2024-10-10",
            "custodian": "Jane Smith",
            "relevance": "Evidence of coercion and retaliation"
        },
        {
            "description": "OSHA complaint filed by employee (Complaint #2024-TX-12345)",
            "type": "Government filing",
            "source": "OSHA Austin office",
            "date_obtained": "2024-10-01",
            "custodian": "OSHA records",
            "relevance": "Protected activity triggering retaliation"
        },
        {
            "description": "Termination letter with false reason (performance issues)",
            "type": "Company document",
            "source": "HR Department certified mail",
            "date_obtained": "2024-10-20",
            "custodian": "Jane Smith",
            "relevance": "Pretext for retaliatory termination"
        },
        {
            "description": "Performance reviews 2022-2024 showing 'Exceeds Expectations' ratings",
            "type": "Company records",
            "source": "HR file obtained via subpoena",
            "date_obtained": "2024-11-15",
            "custodian": "Attorney work product",
            "relevance": "Contradicts false performance-based termination reason"
        }
    ]
    
    doc = gopher.generate_evidence_summary(
        case_title="Smith v. XYZ Manufacturing Inc. - Wrongful Termination",
        incident_date="October 15, 2024",
        parties={
            "plaintiff": "Jane Smith",
            "defendant": "XYZ Manufacturing Inc.",
            "plaintiff_attorney": "Smith Law Firm PLLC"
        },
        evidence_items=evidence_items
    )
    
    filepath = doc.to_file()
    
    print(f"✅ Evidence summary generated successfully!")
    print(f"📄 File saved to: {filepath}")
    print(f"🔒 Master SHA-256 Hash: {doc.integrity_hash}")
    print(f"⏱️  Timestamp: {doc.timestamp}")
    print(f"📦 Evidence items: {len(evidence_items)}")
    print("\n🔐 Each evidence item has its own SHA-256 hash for forensic integrity")

def demo_statement_timestamping(gopher: MytharaGopherNLP):
    """Demo: Cryptographically timestamp user statement"""
    print_section("⏱️  STATEMENT TIMESTAMPING FOR EVIDENCE")
    
    statement = (
        "I witnessed the defendant, John Doe, run a red light at the intersection of Main St and 5th Ave "
        "on November 20, 2024 at approximately 2:35 PM. The light had been red for at least 3 seconds. "
        "The defendant's vehicle, a blue Honda Civic (license plate ABC-1234), struck the plaintiff's "
        "vehicle on the passenger side. I immediately called 911 and provided this statement to the police "
        "officer at the scene (Officer Badge #4567)."
    )
    
    print("Timestamping eyewitness statement...")
    print(f"\n📝 Statement:\n{statement}\n")
    
    result = gopher.timestamp_user_statement(statement, user_id="witness_001")
    
    print("✅ Statement timestamped successfully!\n")
    print(f"⏱️  Timestamp: {result['timestamp']}")
    print(f"🔒 SHA-256 Hash: {result['integrity_hash']}")
    print(f"\n{result['certification']}")

def demo_legal_memo(gopher: MytharaGopherNLP):
    """Demo: Generate professional legal memorandum"""
    print_section("📝 LEGAL MEMORANDUM GENERATION")
    
    print("Generating legal memo analyzing defamation claim...")
    
    doc = gopher.generate_legal_memo(
        title="Analysis of Defamation Claim - Online False Statements",
        issue_statement=(
            "Whether Plaintiff can successfully pursue a defamation claim against Defendant for posting "
            "false statements on social media claiming Plaintiff embezzled company funds."
        ),
        brief_answer=(
            "Yes, likely. Plaintiff appears to have a strong defamation claim. The statements are false, "
            "defamatory per se (accusation of crime), published to third parties, and caused reputational harm. "
            "Defendant may struggle to establish truth defense or privilege."
        ),
        facts=(
            "Plaintiff was employed as an accountant at XYZ Corp from 2020-2024. In October 2024, Defendant "
            "(former coworker) posted on Facebook, Twitter, and LinkedIn that 'Jane Smith STOLE $50,000 from "
            "our company. She's a criminal and should be in jail.' The statements were viewed by 5,000+ people "
            "including Plaintiff's professional contacts. Plaintiff was never charged with any crime, never "
            "investigated for theft, and company financial audits show no discrepancies. Plaintiff has "
            "suffered job loss at new employer who rescinded offer after seeing posts."
        ),
        analysis=(
            "Under Texas defamation law, Plaintiff must prove: (1) false statement of fact, (2) that was published, "
            "(3) with actual malice (public figure) or negligence, and (4) caused damages. See New York Times Co. v. "
            "Sullivan, 376 U.S. 254 (1964); Musser v. Smith Protective Servs., 723 S.W.2d 653 (Tex. 1987).\n\n"
            "Element 1 (False Statement): The accusation of theft is factual, not opinion, and is objectively false. "
            "No theft occurred.\n\n"
            "Element 2 (Publication): Statements were published to thousands via social media.\n\n"
            "Element 3 (Fault): If Plaintiff is private figure (likely), only negligence required. Defendant made "
            "no effort to verify accusations.\n\n"
            "Element 4 (Damages): Job loss and reputational harm are concrete damages. This is defamation per se "
            "(accusation of crime), so damages may be presumed. See Musser, 723 S.W.2d at 654.\n\n"
            "Defenses: Defendant cannot establish truth. No privilege applies to social media posts. Actual malice "
            "may be shown by reckless disregard for truth.\n\n"
            "The claim is strong. Plaintiff should proceed with litigation."
        ),
        conclusion=(
            "Plaintiff has a viable defamation claim. The statements are false, defamatory per se, published broadly, "
            "and caused quantifiable damages. Recommend: (1) immediate cease & desist letter, (2) demand for retraction, "
            "(3) filing defamation lawsuit in Texas state court, (4) seek injunctive relief to remove posts, "
            "(5) claim compensatory and exemplary damages."
        )
    )
    
    filepath = doc.to_file()
    
    print(f"✅ Legal memorandum generated successfully!")
    print(f"📄 File saved to: {filepath}")
    print(f"🔒 SHA-256 Hash: {doc.integrity_hash}")

def interactive_document_menu(gopher: MytharaGopherNLP):
    """Interactive document generation menu"""
    print_section("🔧 INTERACTIVE DOCUMENT GENERATION")
    
    while True:
        print("\nWhat would you like to generate?\n")
        print("1. 📨 Demand Letter")
        print("2. 🛑 Cease & Desist Letter")
        print("3. 📋 Evidence Summary")
        print("4. 📝 Legal Memorandum")
        print("5. ⏱️  Timestamp Statement")
        print("6. 🏠 Return to Main Menu")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "6":
            break
        elif choice == "1":
            print("\n[DEMO MODE] Generating sample demand letter...")
            demo_demand_letter(gopher)
        elif choice == "2":
            print("\n[DEMO MODE] Generating sample cease & desist...")
            demo_cease_and_desist(gopher)
        elif choice == "3":
            print("\n[DEMO MODE] Generating sample evidence summary...")
            demo_evidence_summary(gopher)
        elif choice == "4":
            print("\n[DEMO MODE] Generating sample legal memo...")
            demo_legal_memo(gopher)
        elif choice == "5":
            statement = input("\nEnter statement to timestamp: ").strip()
            if statement:
                result = gopher.timestamp_user_statement(statement, "interactive_user")
                print(f"\n✅ Timestamped!\n⏱️  {result['timestamp']}\n🔒 {result['integrity_hash']}")
        else:
            print("Invalid option. Try again.")

def main():
    """Run document generation demo"""
    print("\n" + "=" * 80)
    print("  MYTHARA ENGINE - DOCUMENT GENERATION DEMO")
    print("  SHA-256 Cryptographic Timestamping for Legal Documents")
    print("=" * 80)
    
    print("\n🦫 Initializing Mythara Gopher NLP Engine...")
    gopher = MytharaGopherNLP()
    print("✅ System ready!\n")
    
    print("This demo showcases Mythara's legal document generation capabilities:")
    print("• Professional demand letters with 30-day deadlines")
    print("• Cease & desist letters for IP/harassment")
    print("• Evidence summaries with chain of custody")
    print("• Legal memoranda in IRAC format")
    print("• Cryptographic timestamping for evidentiary purposes")
    print("\nAll documents include SHA-256 integrity hashes for forensic admissibility.\n")
    
    while True:
        print("\n" + "=" * 80)
        print("MAIN MENU")
        print("=" * 80)
        print("\n1. 🎬 Run Full Demo (all document types)")
        print("2. 🔧 Interactive Document Generation")
        print("3. 💬 Test Conversational Interface")
        print("4. 📂 View Generated Documents")
        print("5. 🚪 Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            # Run full demo
            demo_demand_letter(gopher)
            input("\nPress Enter to continue...")
            
            demo_cease_and_desist(gopher)
            input("\nPress Enter to continue...")
            
            demo_evidence_summary(gopher)
            input("\nPress Enter to continue...")
            
            demo_statement_timestamping(gopher)
            input("\nPress Enter to continue...")
            
            demo_legal_memo(gopher)
            input("\nPress Enter to continue...")
            
            print("\n✅ Full demo complete! All documents saved to legal_documents/")
        
        elif choice == "2":
            interactive_document_menu(gopher)
        
        elif choice == "3":
            print_section("💬 CONVERSATIONAL INTERFACE TEST")
            print("Testing natural language document requests...\n")
            
            queries = [
                "I need to send a demand letter to my landlord",
                "Can you generate a cease and desist for copyright infringement?",
                "How do I timestamp evidence for my case?",
                "Create an evidence summary with chain of custody"
            ]
            
            for query in queries:
                print(f"\n{'='*80}")
                print(f"USER: {query}")
                print(f"{'='*80}\n")
                response = gopher.process_query(query, user_id="demo_user")
                print(f"🦫 GOPHER:\n{response}\n")
                input("Press Enter for next query...")
        
        elif choice == "4":
            print_section("📂 GENERATED DOCUMENTS")
            doc_dir = "legal_documents"
            if os.path.exists(doc_dir):
                files = [f for f in os.listdir(doc_dir) if f.endswith('.txt')]
                if files:
                    print(f"Found {len(files)} documents in {doc_dir}/:\n")
                    for f in files:
                        filepath = os.path.join(doc_dir, f)
                        size = os.path.getsize(filepath)
                        print(f"  📄 {f} ({size:,} bytes)")
                else:
                    print("No documents generated yet. Run demo first!")
            else:
                print(f"Directory {doc_dir}/ doesn't exist yet. Generate documents first!")
        
        elif choice == "5":
            print("\n👋 Thank you for using Mythara Engine!")
            print("All documents are saved with SHA-256 integrity hashes for legal use.\n")
            break
        
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
