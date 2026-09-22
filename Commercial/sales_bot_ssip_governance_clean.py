# Copyright  2025 Herbert Velez Jr. All rights reserved.

"""
Sales Bot SSIP Governance - Apply Mythara Engine integrity to autonomous email responses

This is a DEMO of Mythara's own technology governing AI sales autonomy:
- Cryptographic hashing of all bot-generated emails
- Clause-based rules the bot CANNOT violate
- Override authority levels (auto-send vs human review)
- Audit trail of every email decision
- Blessings reservoir (bot "earns trust" over time)
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Literal
from pathlib import Path

class SalesMessenger:
    """Messenger roles for sales bot actions"""
    MICHAEL = "Michael"      # Truth-teller: Can auto-send factual answers
    GABRIEL = "Gabriel"      # Announcer: Can auto-send not_interested responses  
    URIEL = "Uriel"         # Illuminator: Can auto-send simple clarifications
    RAPHAEL = "Raphael"     # Healer: CANNOT auto-send (needs human for deals)
    METATRON = "Metatron"   # Scribe: Logs everything, no autonomy

class SalesClause:
    """Inviolable rules the bot must follow"""
    
    NEVER_AUTO_SEND = [
        "pricing_negotiation",      # Never negotiate price without human
        "contract_terms",           # Never discuss legal terms
        "custom_requirements",      # Never promise custom features
        "enterprise_deal",          # Deals >$2,500 need human approval
        "technical_deep_dive",      # Complex tech questions need human
        "competitor_comparison",    # Never trash competitors
    ]
    
    CAN_AUTO_SEND = [
        "not_interested",           # Graceful exit, low risk
        "out_of_office",           # Auto-acknowledge OOO
        "simple_faq",              # Questions clearly answered in docs
        "referral_request",        # Ask for referrals (no risk)
    ]
    
    PRICING_RULES = {
        "early_adopter_max": 500,
        "standard_max": 2500,
        "enterprise_max": 5000,
        "never_discount_below": 500,
        "cannot_promise": ["free trial", "money-back guarantee", "custom pricing"]
    }
    
    COMPLIANCE_RULES = {
        "never_claim": [
            "FDA approved",
            "HIPAA certified", 
            "SOC2 compliant",
            "guaranteed regulatory pass"
        ],
        "always_caveat": [
            "Results may vary",
            "Subject to technical review",
            "Pilot terms negotiable"
        ]
    }

class BlessingsReservoir:
    """Bot earns trust over time - poor performance = less autonomy"""
    
    def __init__(self, filepath: str = "Commercial/bot_blessings.json"):
        self.filepath = Path(filepath)
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        if self.filepath.exists():
            return json.loads(self.filepath.read_text())
        return {
            "blessings": 100,  # Start at 100 (full trust)
            "auto_sends": 0,
            "human_overrides": 0,
            "errors_caught": 0,
            "successful_closes": 0,
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_state(self):
        self.filepath.parent.mkdir(exist_ok=True)
        self.filepath.write_text(json.dumps(self.state, indent=2))
    
    def check_autonomy_level(self) -> Literal["full", "limited", "supervised", "disabled"]:
        """Determine bot's autonomy based on blessings"""
        blessings = self.state["blessings"]
        
        if blessings >= 90:
            return "full"        # Can auto-send all approved categories
        elif blessings >= 70:
            return "limited"     # Can auto-send only not_interested + FAQ
        elif blessings >= 50:
            return "supervised"  # All drafts need human review
        else:
            return "disabled"    # Bot offline, human handles all
    
    def record_auto_send(self, success: bool):
        """Record outcome of auto-sent email"""
        if success:
            self.state["blessings"] = min(100, self.state["blessings"] + 2)
            self.state["auto_sends"] += 1
        else:
            self.state["blessings"] = max(0, self.state["blessings"] - 10)
            self.state["errors_caught"] += 1
        
        self._save_state()
    
    def record_human_override(self, reason: str):
        """Human edited bot's draft - learn from it"""
        self.state["human_overrides"] += 1
        self.state["blessings"] = max(50, self.state["blessings"] - 1)  # Small penalty
        self._save_state()
    
    def record_successful_close(self, deal_value: int):
        """Bot helped close a deal - big blessing boost"""
        self.state["successful_closes"] += 1
        self.state["blessings"] = min(100, self.state["blessings"] + 10)
        self._save_state()

class SalesGovernanceEngine:
    """SSIP for sales bot - enforces rules, creates audit trail"""
    
    def __init__(self):
        self.reservoir = BlessingsReservoir()
        self.audit_log = Path("Commercial/bot_audit_log.jsonl")
    
    def validate_email_draft(self, 
                            email_data: Dict, 
                            draft_response: str,
                            intent: str) -> Dict:
        """
        Validate draft against Mythara clauses
        Returns: {can_auto_send: bool, violations: List, messenger: str, hash: str}
        """
        violations = []
        messenger = SalesMessenger.METATRON  # Default: no autonomy
        can_auto_send = False
        
        # Check pricing violations
        pricing_violations = self._check_pricing_rules(draft_response)
        violations.extend(pricing_violations)
        
        # Check compliance violations
        compliance_violations = self._check_compliance_rules(draft_response)
        violations.extend(compliance_violations)
        
        # Check intent-based autonomy
        autonomy_level = self.reservoir.check_autonomy_level()
        
        if intent == "not_interested" and autonomy_level in ["full", "limited"]:
            messenger = SalesMessenger.GABRIEL
            can_auto_send = True if not violations else False
        
        elif intent == "question" and autonomy_level == "full":
            # Check if it's a simple FAQ
            if self._is_simple_faq(email_data, draft_response):
                messenger = SalesMessenger.URIEL
                can_auto_send = True if not violations else False
            else:
                messenger = SalesMessenger.RAPHAEL
                can_auto_send = False
        
        elif intent == "interested":
            # NEVER auto-send interested leads - too valuable
            messenger = SalesMessenger.RAPHAEL
            can_auto_send = False
        
        # Generate integrity hash
        integrity_hash = self._generate_hash(email_data, draft_response, messenger)
        
        # Log to audit trail
        self._log_decision({
            "timestamp": datetime.now().isoformat(),
            "intent": intent,
            "messenger": messenger,
            "can_auto_send": can_auto_send,
            "violations": violations,
            "autonomy_level": autonomy_level,
            "blessings": self.reservoir.state["blessings"],
            "hash": integrity_hash
        })
        
        return {
            "can_auto_send": can_auto_send,
            "violations": violations,
            "messenger": messenger,
            "hash": integrity_hash,
            "autonomy_level": autonomy_level,
            "blessings": self.reservoir.state["blessings"]
        }
    
    def _check_pricing_rules(self, draft: str) -> List[str]:
        """Ensure bot doesn't violate pricing clauses"""
        violations = []
        draft_lower = draft.lower()
        
        # Check for forbidden promises
        for forbidden in SalesClause.PRICING_RULES["cannot_promise"]:
            if forbidden in draft_lower:
                violations.append(f"PRICING_VIOLATION: Cannot promise '{forbidden}'")
        
        # Check for price mentions below minimum
        if "$" in draft:
            # Extract numbers after $
            import re
            prices = re.findall(r'\$(\d+)', draft)
            for price in prices:
                if int(price) < SalesClause.PRICING_RULES["never_discount_below"]:
                    violations.append(f"PRICING_VIOLATION: Price ${price} below minimum $500")
        
        return violations
    
    def _check_compliance_rules(self, draft: str) -> List[str]:
        """Ensure bot doesn't make illegal claims"""
        violations = []
        draft_lower = draft.lower()
        
        for forbidden_claim in SalesClause.COMPLIANCE_RULES["never_claim"]:
            if forbidden_claim.lower() in draft_lower:
                violations.append(f"COMPLIANCE_VIOLATION: Cannot claim '{forbidden_claim}'")
        
        return violations
    
    def _is_simple_faq(self, email_data: Dict, draft: str) -> bool:
        """Determine if this is a simple FAQ (safe to auto-send)"""
        # Simple heuristic: draft is short + high confidence from RAG
        word_count = len(draft.split())
        
        # If draft is under 150 words and doesn't mention pricing/contracts
        if word_count < 150:
            draft_lower = draft.lower()
            complex_topics = ["pricing", "contract", "custom", "enterprise", "negotiate"]
            if not any(topic in draft_lower for topic in complex_topics):
                return True
        
        return False
    
    def _generate_hash(self, email_data: Dict, draft: str, messenger: str) -> str:
        """Generate SHA-256 hash for integrity verification"""
        content = f"{email_data['subject']}|{email_data['body']}|{draft}|{messenger}|{datetime.now().isoformat()}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def _log_decision(self, decision: Dict):
        """Append to audit log (JSONL format)"""
        self.audit_log.parent.mkdir(exist_ok=True)
        with open(self.audit_log, 'a') as f:
            f.write(json.dumps(decision) + '\n')

class GovernedEmailAssistant:
    """Email assistant with Mythara SSIP governance"""
    
    def __init__(self):
        from email_assistant import EmailAssistant
        self.assistant = EmailAssistant()
        self.governance = SalesGovernanceEngine()
    
    def process_email(self, email_data: Dict) -> Dict:
        """
        Process email with full governance
        Returns: {draft, can_auto_send, violations, messenger, hash, action_taken}
        """
        # Step 1: Categorize intent
        intent, confidence = self.assistant.categorize_intent(
            email_data['body'], 
            email_data['subject']
        )
        
        # Step 2: Generate draft with sales psychology
        draft = self.assistant.generate_draft_response(email_data, intent)
        
        # Step 3: Validate against Mythara clauses
        validation = self.governance.validate_email_draft(email_data, draft, intent)
        
        # Step 4: Decide action
        if validation["can_auto_send"] and not validation["violations"]:
            action = "AUTO_SEND"
            # Actually send (would call Gmail API here)
            # self.assistant.send_email(draft)
            self.governance.reservoir.record_auto_send(success=True)
        else:
            action = "HUMAN_REVIEW_REQUIRED"
            # Create draft in Gmail for human review
            # self.assistant.create_gmail_draft(draft)
        
        return {
            "intent": intent,
            "draft": draft,
            "can_auto_send": validation["can_auto_send"],
            "violations": validation["violations"],
            "messenger": validation["messenger"],
            "hash": validation["hash"],
            "autonomy_level": validation["autonomy_level"],
            "blessings": validation["blessings"],
            "action_taken": action
        }
    
    def get_governance_report(self) -> Dict:
        """Generate governance stats for transparency"""
        state = self.governance.reservoir.state
        autonomy = self.governance.reservoir.check_autonomy_level()
        
        return {
            "autonomy_level": autonomy,
            "blessings": state["blessings"],
            "total_auto_sends": state["auto_sends"],
            "human_overrides": state["human_overrides"],
            "errors_caught": state["errors_caught"],
            "successful_closes": state["successful_closes"],
            "auto_send_enabled": autonomy in ["full", "limited"],
            "categories_allowed": self._get_allowed_categories(autonomy)
        }
    
    def _get_allowed_categories(self, autonomy: str) -> List[str]:
        if autonomy == "full":
            return ["not_interested", "simple_faq", "referral_request", "out_of_office"]
        elif autonomy == "limited":
            return ["not_interested", "out_of_office"]
        else:
            return []


# ============================================================================
# DEMO USAGE
# ============================================================================

if __name__ == '__main__':
    print("="*80)
    print("MYTHARA-GOVERNED SALES BOT DEMO")
    print("="*80)
    
    bot = GovernedEmailAssistant()
    
    # Test 1: Not interested (should auto-send)
    print("\n TEST 1: NOT INTERESTED REPLY")
    email1 = {
        'subject': 'Re: AI Governance',
        'body': "Thanks but we're not interested right now."
    }
    result1 = bot.process_email(email1)
    print(f"Intent: {result1['intent']}")
    print(f"Messenger: {result1['messenger']}")
    print(f"Can Auto-Send: {result1['can_auto_send']}")
    print(f"Action: {result1['action_taken']}")
    print(f"Violations: {result1['violations']}")
    print(f"Hash: {result1['hash'][:16]}...")
    
    # Test 2: Interested (never auto-send)
    print("\n" + "="*80)
    print(" TEST 2: INTERESTED PROSPECT")
    email2 = {
        'subject': 'Re: Model Risk Solution',
        'body': "This looks interesting. Can we schedule a call?"
    }
    result2 = bot.process_email(email2)
    print(f"Intent: {result2['intent']}")
    print(f"Messenger: {result2['messenger']}")
    print(f"Can Auto-Send: {result2['can_auto_send']}")
    print(f"Action: {result2['action_taken']}")
    print(f"Reasoning: Interested leads ALWAYS need human touch (RAPHAEL clause)")
    
    # Test 3: Question with pricing violation
    print("\n" + "="*80)
    print(" TEST 3: PRICING VIOLATION DETECTION")
    email3 = {
        'subject': 'Re: Pricing',
        'body': "Can you do $300 for early access?"
    }
    # Simulate bot trying to offer $300 (VIOLATION)
    fake_draft = "Sure! I can do $300 for you as a special early adopter rate."
    validation = bot.governance.validate_email_draft(email3, fake_draft, "question")
    print(f"Draft: {fake_draft}")
    print(f"Violations: {validation['violations']}")
    print(f"Can Auto-Send: {validation['can_auto_send']}")
    print(f"Reasoning: Price below $500 minimum (PRICING_CLAUSE violation)")
    
    # Test 4: Compliance violation
    print("\n" + "="*80)
    print(" TEST 4: COMPLIANCE VIOLATION DETECTION")
    email4 = {
        'subject': 'Re: HIPAA',
        'body': "Is this HIPAA certified?"
    }
    fake_draft2 = "Yes, Mythara is HIPAA certified and FDA approved for clinical use."
    validation2 = bot.governance.validate_email_draft(email4, fake_draft2, "question")
    print(f"Draft: {fake_draft2}")
    print(f"Violations: {validation2['violations']}")
    print(f"Can Auto-Send: {validation2['can_auto_send']}")
    print(f"Reasoning: Cannot claim 'FDA approved' or 'HIPAA certified' (COMPLIANCE_CLAUSE)")
    
    # Show governance stats
    print("\n" + "="*80)
    print(" GOVERNANCE REPORT")
    print("="*80)
    report = bot.get_governance_report()
    print(f"Autonomy Level: {report['autonomy_level']}")
    print(f"Blessings: {report['blessings']}/100")
    print(f"Auto-Sends: {report['total_auto_sends']}")
    print(f"Human Overrides: {report['human_overrides']}")
    print(f"Errors Caught: {report['errors_caught']}")
    print(f"Successful Closes: {report['successful_closes']}")
    print(f"Auto-Send Enabled: {report['auto_send_enabled']}")
    print(f"Allowed Categories: {report['categories_allowed']}")
    
    print("\n" + "="*80)
    print(" MYTHARA SSIP GOVERNANCE ACTIVE")
    print("="*80)
    print("\nThe bot is governed by inviolable clauses:")
    print("   Cannot offer pricing below $500")
    print("   Cannot make illegal compliance claims")
    print("   Cannot auto-send interested leads (too valuable)")
    print("   Earns autonomy through good performance (Blessings Reservoir)")
    print("   Every decision is cryptographically hashed")
    print("   Full audit trail in bot_audit_log.jsonl")
    print("\nThis IS Mythara Engine dogfooding itself. ")
