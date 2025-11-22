"""
Attorney Referral System for Mythara Gopher
To be integrated into mythara_gopher_nlp_engine.py
"""

def _build_attorney_database(self) -> Dict:
    """
    Build attorney referral database with practice areas and locations.
    PUBLIC DATABASE - attorneys can submit their information for inclusion.
    
    Database structure:
    - Attorney profile (name, firm, contact)
    - Practice areas (employment, personal injury, landlord/tenant, etc.)
    - Geographic coverage (state, city, counties)
    - Bar admissions
    - Free consultation info
    - Client reviews/ratings (future)
    
    NOTE: This is a PUBLIC referral service. Gopher does NOT endorse or guarantee
    any attorney. Users must verify credentials and make their own selection.
    """
    return {
        "practice_areas": {
            "employment": {
                "keywords": ["wrongful termination", "discrimination", "harassment", "wage", "retaliation", "fired", "employment"],
                "description": "Employment Law (wrongful termination, discrimination, wage disputes)"
            },
            "personal_injury": {
                "keywords": ["accident", "injury", "car crash", "medical malpractice", "slip and fall", "negligence"],
                "description": "Personal Injury (accidents, medical malpractice, negligence)"
            },
            "landlord_tenant": {
                "keywords": ["eviction", "landlord", "tenant", "rent", "security deposit", "housing"],
                "description": "Landlord/Tenant (evictions, rent disputes, security deposits)"
            },
            "family_law": {
                "keywords": ["divorce", "custody", "child support", "alimony", "family", "domestic"],
                "description": "Family Law (divorce, custody, child support)"
            },
            "criminal": {
                "keywords": ["criminal", "arrest", "charged", "felony", "misdemeanor", "dui", "defense"],
                "description": "Criminal Defense (arrests, charges, DUI)"
            },
            "civil_rights": {
                "keywords": ["civil rights", "police", "constitutional", "discrimination", "first amendment"],
                "description": "Civil Rights (police misconduct, constitutional violations)"
            },
            "immigration": {
                "keywords": ["immigration", "visa", "deportation", "asylum", "green card", "citizenship"],
                "description": "Immigration (visas, deportation, asylum)"
            },
            "business": {
                "keywords": ["business", "contract", "partnership", "llc", "corporation", "commercial"],
                "description": "Business Law (contracts, partnerships, corporate)"
            },
            "estate": {
                "keywords": ["estate", "will", "trust", "probate", "inheritance", "elder"],
                "description": "Estate Planning (wills, trusts, probate)"
            },
            "bankruptcy": {
                "keywords": ["bankruptcy", "debt", "chapter 7", "chapter 13", "creditor"],
                "description": "Bankruptcy & Debt (Chapter 7, Chapter 13, creditors)"
            }
        },
        "attorneys": [
            # CALIFORNIA ATTORNEYS
            {
                "name": "Public Referral - California Employment Law",
                "firm": "[Submit your firm - attorney_referrals@mythara.com]",
                "practice_areas": ["employment"],
                "states": ["CA"],
                "cities": ["Los Angeles", "San Francisco", "San Diego", "Sacramento"],
                "phone": "[To be listed]",
                "email": "attorney_referrals@mythara.com",
                "website": "https://mythara.com/attorney-referrals",
                "free_consultation": True,
                "notes": "Submit your practice info to be listed in public database"
            },
            {
                "name": "Public Referral - California Personal Injury",
                "firm": "[Submit your firm - attorney_referrals@mythara.com]",
                "practice_areas": ["personal_injury"],
                "states": ["CA"],
                "cities": ["Los Angeles", "San Diego", "San Jose"],
                "phone": "[To be listed]",
                "email": "attorney_referrals@mythara.com",
                "website": "https://mythara.com/attorney-referrals",
                "free_consultation": True,
                "notes": "Contingency fee - no upfront costs. Submit your practice to be listed."
            },
            # NEW YORK ATTORNEYS
            {
                "name": "Public Referral - New York Employment Law",
                "firm": "[Submit your firm - attorney_referrals@mythara.com]",
                "practice_areas": ["employment", "civil_rights"],
                "states": ["NY"],
                "cities": ["New York City", "Buffalo", "Rochester", "Albany"],
                "phone": "[To be listed]",
                "email": "attorney_referrals@mythara.com",
                "website": "https://mythara.com/attorney-referrals",
                "free_consultation": True,
                "notes": "Submit your practice info to be listed"
            },
            # TEXAS ATTORNEYS
            {
                "name": "Public Referral - Texas Personal Injury",
                "firm": "[Submit your firm - attorney_referrals@mythara.com]",
                "practice_areas": ["personal_injury"],
                "states": ["TX"],
                "cities": ["Houston", "Dallas", "Austin", "San Antonio"],
                "phone": "[To be listed]",
                "email": "attorney_referrals@mythara.com",
                "website": "https://mythara.com/attorney-referrals",
                "free_consultation": True,
                "notes": "Contingency fee cases. Submit your practice to be listed."
            },
            # FLORIDA ATTORNEYS
            {
                "name": "Public Referral - Florida Criminal Defense",
                "firm": "[Submit your firm - attorney_referrals@mythara.com]",
                "practice_areas": ["criminal"],
                "states": ["FL"],
                "cities": ["Miami", "Tampa", "Orlando", "Jacksonville"],
                "phone": "[To be listed]",
                "email": "attorney_referrals@mythara.com",
                "website": "https://mythara.com/attorney-referrals",
                "free_consultation": True,
                "notes": "24/7 emergency availability. Submit your practice to be listed."
            },
            # ILLINOIS ATTORNEYS
            {
                "name": "Public Referral - Illinois Employment Law",
                "firm": "[Submit your firm - attorney_referrals@mythara.com]",
                "practice_areas": ["employment"],
                "states": ["IL"],
                "cities": ["Chicago", "Naperville", "Aurora"],
                "phone": "[To be listed]",
                "email": "attorney_referrals@mythara.com",
                "website": "https://mythara.com/attorney-referrals",
                "free_consultation": True,
                "notes": "Submit your practice info to be listed"
            }
        ],
        "bar_associations": {
            "CA": {"name": "State Bar of California", "website": "https://www.calbar.ca.gov", "phone": "(866) 442-2529"},
            "NY": {"name": "New York State Bar Association", "website": "https://www.nysba.org", "phone": "(518) 463-3200"},
            "TX": {"name": "State Bar of Texas", "website": "https://www.texasbar.com", "phone": "(800) 204-2222"},
            "FL": {"name": "The Florida Bar", "website": "https://www.floridabar.org", "phone": "(850) 561-5600"},
            "IL": {"name": "Illinois State Bar Association", "website": "https://www.isba.org", "phone": "(217) 525-1760"}
        },
        "legal_aid": {
            "national": {
                "name": "Legal Services Corporation",
                "website": "https://www.lsc.gov/what-legal-aid/find-legal-aid",
                "description": "Find free legal aid in your area"
            },
            "employment": {
                "name": "National Employment Lawyers Association",
                "website": "https://www.nela.org",
                "description": "Find employment law attorneys"
            }
        }
    }

def _handle_attorney_referral(self, query: str, entities: Dict, context: ConversationContext) -> str:
    """Handle attorney referral requests with practice area and location filtering"""
    response = "👨‍⚖️ **Attorney Referral Service**\n\n"
    
    query_lower = query.lower()
    
    # Extract jurisdiction from entities or query
    jurisdictions = entities.get("jurisdiction", [])
    if not jurisdictions:
        # Try to extract state abbreviations
        import re
        state_pattern = r"\b(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)\b"
        state_matches = re.findall(state_pattern, query.upper())
        if state_matches:
            jurisdictions = state_matches
    
    # Identify practice area from query keywords
    matched_areas = []
    for area_key, area_data in self.attorney_database["practice_areas"].items():
        for keyword in area_data["keywords"]:
            if keyword in query_lower:
                matched_areas.append((area_key, area_data["description"]))
                break
    
    if matched_areas:
        response += f"**Case Type Detected:** {', '.join([desc for _, desc in matched_areas])}\n\n"
    
    if jurisdictions:
        response += f"**Location:** {', '.join(jurisdictions)}\n\n"
    
    # Search attorney database
    matching_attorneys = []
    for attorney in self.attorney_database["attorneys"]:
        # Match by jurisdiction
        jurisdiction_match = not jurisdictions or any(j in attorney["states"] for j in jurisdictions)
        
        # Match by practice area
        area_match = not matched_areas or any(
            area_key in attorney["practice_areas"] for area_key, _ in matched_areas
        )
        
        if jurisdiction_match and area_match:
            matching_attorneys.append(attorney)
    
    if matching_attorneys:
        response += f"**✅ {len(matching_attorneys)} Referral(s) Available:**\n\n"
        for i, atty in enumerate(matching_attorneys[:5], 1):  # Show top 5
            response += f"{i}. **{atty['name']}**\n"
            response += f"   Firm: {atty['firm']}\n"
            response += f"   Practice Areas: {', '.join([self.attorney_database['practice_areas'][area]['description'] for area in atty['practice_areas']])}\n"
            response += f"   Location: {', '.join(atty['cities'])}\n"
            if atty.get('free_consultation'):
                response += f"   💡 Free Consultation Available\n"
            response += f"   📞 {atty['phone']}\n"
            response += f"   📧 {atty['email']}\n"
            response += f"   🌐 {atty['website']}\n"
            if atty.get('notes'):
                response += f"   ℹ️ {atty['notes']}\n"
            response += f"\n"
    else:
        response += "**No direct referrals found in database for your specific criteria.**\n\n"
    
    # Add bar association referral info
    if jurisdictions:
        response += "**📋 State Bar Referral Services:**\n\n"
        for juris in jurisdictions:
            if juris in self.attorney_database["bar_associations"]:
                bar = self.attorney_database["bar_associations"][juris]
                response += f"**{bar['name']}**\n"
                response += f"   🌐 {bar['website']}\n"
                response += f"   📞 {bar['phone']}\n"
                response += f"   ℹ️ Free lawyer referral service\n\n"
    
    # Add legal aid resources
    response += "**💰 Free/Low-Cost Legal Help:**\n\n"
    response += f"**{self.attorney_database['legal_aid']['national']['name']}**\n"
    response += f"   🌐 {self.attorney_database['legal_aid']['national']['website']}\n"
    response += f"   ℹ️ {self.attorney_database['legal_aid']['national']['description']}\n\n"
    
    # Add how to verify credentials
    response += "**⚠️ VERIFY ATTORNEY CREDENTIALS:**\n"
    response += "Before hiring any attorney:\n"
    response += "1. ✅ Verify bar license (check state bar website)\n"
    response += "2. ✅ Check disciplinary history\n"
    response += "3. ✅ Read client reviews\n"
    response += "4. ✅ Get fee agreement in writing\n"
    response += "5. ✅ Meet for consultation (many offer free consults)\n\n"
    
    # Add attorney submission info
    response += "**📢 Attorneys: Join Our Public Database**\n"
    response += "Submit your practice information for inclusion:\n"
    response += "📧 attorney_referrals@mythara.com\n"
    response += "🌐 https://mythara.com/attorney-referrals\n\n"
    
    # Add disclaimer
    response += "**⚖️ REFERRAL DISCLAIMER:**\n"
    response += "Mythara Gopher provides this public attorney database as a SERVICE ONLY.\n"
    response += "We do NOT endorse, guarantee, or warrant any attorney's services.\n"
    response += "You are responsible for verifying credentials and selecting counsel.\n"
    response += "Inclusion in this database is NOT a recommendation or endorsement.\n\n"
    
    return response
