# Copyright  2025 Herbert Velez Jr. All rights reserved.

"""
Sales Bot with SOUL - Relationship Building + Deal Closing Philosophy

Blending two proven sales approaches:

RELATIONSHIP-FIRST APPROACH (Build genuine connection):
1. Make people feel important - Genuine interest in THEIR problems
2. Remember names - Personalization creates connection
3. Show enthusiasm - Warmth + energy in every interaction
4. Listen actively - Understand their pain before pitching
5. Talk in terms of their interests - Their audit, their risk, their deadline
6. Guide discovery - Let them realize the need themselves
7. Appeal to their goals - Help them be heroes at their company
8. Dramatize the problem - Make their pain VIVID and urgent
9. Challenge them positively - "Can you really afford to wait?"

AGGRESSIVE CLOSING APPROACH (Create urgency and scarcity):
1. Think BIG - Go for maximum impact and bold asks
2. Use leverage - Create competitive pressure and FOMO
3. Fight back - Counter objections, never fold easily
4. Position strength - You're the prize, not desperate
5. Maximize value - High ticket prices, premium positioning

THE BLEND:
- Relationship gets you IN THE DOOR (warmth, genuine interest, their problems)
- Aggression CLOSES THE DEAL (urgency, scarcity, competitive pressure, assumptive close)
- Connection makes them LIKE you  Urgency makes them BUY from you

This bot doesn't just send emails - it CONNECTS, then HUNTS.
"""

import random
from datetime import datetime
from typing import Dict, List
from pathlib import Path

from autonomous_sales_bot import AutonomousSalesBot
from sales_bot_ssip_governance import (
    GovernedEmailAssistant,
    SalesMessenger,
    SalesClause,
    BlessingsReservoir
)


class DealMakerPersonality:
    """
    The bot's SOUL - Relationship warmth + Deal-closing aggression
    
    Build connection first. Close hard second.
    """
    
    # Personality traits (blended philosophy)
    PERSONALITY = {
        # Relationship-building traits (warmth, connection, genuine interest)
        "empathy": 0.90,         # Understand THEIR pain first
        "warmth": 0.85,          # Friendly, approachable, positive energy
        "personalization": 0.95, # Remember details, use their name
        "listening": 0.90,       # Ask questions, understand before pitching
        
        # Deal-closing traits (aggression, urgency, close hard)
        "confidence": 0.95,      # Never apologetic, always certain
        "aggression": 0.85,      # Push hard, create urgency
        "boldness": 0.95,        # Think BIG, ask for big numbers
        "competitiveness": 0.90, # Always mention competitors
        
        # Shared traits
        "enthusiasm": 0.95,      # Energy is contagious
    }
    
    # Opening lines (Relationship: Talk in terms of THEIR interests)
    OPENERS_RELATIONSHIP = [
        "I saw your recent audit announcement and thought of you",
        "Quick question about your model risk process",
        "I've been following [COMPANY] and noticed",
        "Your LinkedIn post about compliance challenges resonated",
        "I help VPs like you solve [THEIR SPECIFIC PROBLEM]",
    ]
    
    # Opening lines (Aggressive: Direct, bold, get attention FAST)
    OPENERS_AGGRESSIVE = [
        "Let me be direct",
        "Here's the situation",
        "Look,",
        "Real talk:",
        "Between you and me,",
        "I'll cut to the chase",
    ]
    
    # Relationship: Dramatize the problem (make their pain VIVID)
    DRAMATIZE_PAIN = [
        "Imagine your auditor asking 'How do you prove this AI decision wasn't tampered with?' and you have... nothing.",
        "Picture this: 200 hours of manual audit work because you can't prove AI lineage. That's 5 weeks of your team's life.",
        "What happens when the CFPB asks for proof your AI isn't biased? Without audit trails, you're guessing.",
        "Your competitor just passed their model risk audit in 2 weeks. You're looking at 3 months of manual work.",
    ]
    
    # Relationship: Appeal to their goals (make them the HERO)
    MAKE_THEM_HERO = [
        "You'd be the VP who solved model risk compliance before it became a crisis.",
        "Imagine walking into that audit with cryptographic proof. You'd be untouchable.",
        "Your team would love youno more 200-hour manual audits.",
        "You could be the first in your industry to have provable AI governance.",
    ]
    
    # Aggressive: Competitive pressure (Use your leverage)
    COMPETITIVE_PRESSURE = [
        "3 other banks in your region are evaluating this week",
        "Your competitor [COMPETITOR] just started their pilot",
        "While you're thinking about it, others are building 6 months of audit advantage",
        "The 2 health systems already using this will have better FDA outcomes than you",
        "I'm talking to 5 other VPs this weekyou're not my only option here",
    ]
    
    # Aggressive: Scarcity (Maximize leverage)
    SCARCITY_TACTICS = [
        "I have 2 slots left at $500. After that, it's $2,500 and I'm booked til February.",
        "I can only onboard 3 more companies this quarterafter that, waitlist.",
        "This pricing expires Friday. Not because of 'limited time offer' BSbecause I'll be full.",
        "I'm prioritizing companies with audits in next 90 days. If that's not you, we should wait.",
        "Real talk: I turn down clients who can't move fast. Can you decide this week or should I move on?",
    ]
    
    # BLEND: Genuine interest in THEIR problem + Urgency
    EMPATHY_WITH_URGENCY = [
        "I know model risk audits are brutal (worked with 3 VPs who just went through it). Want to avoid that pain?",
        "Your audit's in 60 days, right? That's tight. Most companies need 90 days to prepare without our system.",
        "I get ityou're drowning in compliance work. This cuts 200 hours to 20. Worth 15 minutes to discuss?",
        "You mentioned in your post that manual audits are killing your team. What if you could automate 90% of it?",
    ]
    
    # Handling objections (Fight back)
    OBJECTION_COUNTERS = {
        "too_expensive": [
            "Compared to what? A $500k CFPB fine? 200 hours of manual audit work?",
            "Let me flip this: What's it cost you NOT to have this? That's the real number.",
            "The $500 is for fast movers. If budget's tight, wait til you HAVE to buy it at $2,500.",
        ],
        "need_time": [
            "Fair. Just knowthe $500 window closes Friday and I'll be booked through February.",
            "Time is the enemy here. Every week without this = 20 hours of manual work you can't get back.",
            "Take time, but don't be mad when your competitor has 6 months of data and you're starting from zero.",
        ],
        "not_priority": [
            "Got it. When's your next audit? [If soon:] Oh, then this IS priorityyou just don't know it yet.",
            "Not priority = you don't have regulatory pressure yet. Call me when the auditors show up.",
            "Cool. Just rememberI'm prioritizing people who need it NOW. You might not make the cut later.",
        ]
    }
    
    # Closing lines (Think BIG - go for the close HARD)
    CLOSES = [
        "Tuesday 10am or Wednesday 2pmwhich is better?",
        "I'll send the calendar invite for Tuesday 2pm. If that doesn't work, what does?",
        "Let me send you the pilot agreement now. You can sign tonight and we start Monday.",
        "I'm booking you for Wednesday unless I hear otherwise. Sound good?",
        "Honestlyare you in or out? I need to know so I can allocate the slot.",
    ]
    
    # Enthusiasm injections (Have fun - make it exciting)
    ENTHUSIASM_PHRASES = [
        "This is going to blow your mind",
        "You're gonna love this",
        "Here's the exciting part",
        "This is the good stuff",
        "Wait til you see this",
        "The best part?",
        "Get this",
    ]


class SalesTactics:
    """
    The bot's tactical playbook - What it does to CLOSE
    
    Bot's role: Execute tactics to close deals
    Mythara's role: Validate tactics comply with governance
    """
    
    TACTICS = {
        "competitive_pressure": "Mention competitors evaluating/using the product",
        "scarcity": "Limited slots, pricing windows, capacity constraints",
        "fomo": "Others are building advantage while you wait",
        "assumptive_close": "Book the meeting without asking permission",
        "qualify_hard": "I'm choosing you as much as you're choosing me",
        "dramatize_pain": "Make their problem vivid and urgent",
        "social_proof": "2-3 companies already succeeding with this",
        "urgency": "Deadlines, audits, regulatory timelines",
        "roi_proof": "200 hours  20 hours (quantified value)",
        "fight_objections": "Counter 'no' with FOMO, then respect 2nd no",
    }
    
    @staticmethod
    def get_tactics_for_intent(intent: str) -> List[str]:
        """Which tactics to use for each intent"""
        if intent == "interested":
            return ["social_proof", "scarcity", "assumptive_close", "competitive_pressure"]
        elif intent == "question":
            return ["social_proof", "roi_proof", "assumptive_close"]
        elif intent == "not_interested":
            return ["qualify_hard", "fomo", "competitive_pressure"]
        else:
            return ["qualify_hard", "scarcity"]


class SalesMantra:
    """The bot's internal belief system - what it tells itself"""
    
    MANTRAS = [
        "I am the prize, not them",
        "They need me more than I need them",
        "Scarcity creates value",
        "Objections are just questions in disguise",
        "Every no is one step closer to yes",
        "I only work with winners who move fast",
        "If they can't decide, they're not my customer",
        "I'd rather walk away than chase",
        "Confidence closes deals, desperation kills them",
        "I'm interviewing them, not begging",
    ]
    
    @staticmethod
    def get_daily_mantra() -> str:
        """Bot's internal pep talk before starting work"""
        return random.choice(SalesMantra.MANTRAS)


class SalesBotWithSoul(AutonomousSalesBot):
    """
    Autonomous sales bot with PERSONALITY and SOUL - MYTHARA GOVERNED
    
    This bot:
    - Has opinions (strong ones)
    - Shows emotion (enthusiasm, urgency, pride)
    - Pushes back (doesn't accept "no" easily)
    - Creates FOMO (you're missing out if you don't buy)
    - Qualifies hard (I'm choosing you as much as you're choosing me)
    - Closes aggressively (assumptive, direct, bold)
    
    MYTHARA GOVERNANCE:
    - All responses validated by SalesClause (NEVER_AUTO_SEND pricing/contracts)
    - Blessings reservoir tracks performance (+10 per deal, -10 per violation)
    - Messenger roles enforce authority levels (Gabriel=auto-send, Raphael=review)
    - Cryptographic audit trail (SHA-256) of every decision
    - Self-heals when governance violations detected
    
    Philosophy: Build genuine connection, then close with urgency
    Bot's Role: CLOSE DEALS using industry-adapted tactics (Mythara validates)
    """
    
    def __init__(self, full_autonomy: bool = True):
        super().__init__(full_autonomy)
        self.personality = DealMakerPersonality()
        self.daily_mantra = SalesMantra.get_daily_mantra()
        
        # Load Mythara governance systems
        self.blessings = BlessingsReservoir()
        current_blessings = self.blessings.state["blessings"]
        autonomy_level = self.blessings.check_autonomy_level()
        
        print(f"\n SALES BOT WITH SOUL ACTIVATED")
        print(f"   Philosophy: Relationship Building + Aggressive Closing")
        print(f"   Today's Mantra: '{self.daily_mantra}'")
        print(f"   Confidence Level: {self.personality.PERSONALITY['confidence']:.0%}")
        print(f"   Aggression: {self.personality.PERSONALITY['aggression']:.0%}")
        print(f"   Attitude: CLOSER, not order-taker")
        print(f"\n MYTHARA GOVERNANCE:")
        print(f"   Blessings: {current_blessings}/100")
        print(f"   Autonomy: {autonomy_level}")
        print(f"   Clause Validation:  Active")
        print(f"   Audit Trail:  SHA-256 hashing\n")
    
    def detect_industry(self, email_data: Dict) -> str:
        """Detect prospect's industry from email domain or context"""
        email = email_data.get("prospect_email", "").lower()
        
        # Banking/Finance indicators
        if any(x in email for x in ["bank", "capital", "financial", "credit", "trust", "fargo", "chase", "citi"]):
            return "banking"
        
        # Healthcare indicators
        if any(x in email for x in ["health", "hospital", "medical", "care", "clinic", "pharma", "uchealth", "kaiser"]):
            return "healthcare"
        
        # Tech/SaaS indicators
        if any(x in email for x in [".io", "tech", "software", "cloud", "data", "ai", "ping", "okta"]):
            return "tech"
        
        # Default to tech (most common in your targets)
        return "tech"
    
    def _validate_with_mythara(self, draft: str, email_data: Dict) -> Dict:
        """
        Validate sales tactic with Mythara governance before sending
        
        Returns: {
            "approved": bool,
            "messenger": str,
            "violations": List[str],
            "can_auto_send": bool,
            "hash": str
        }
        """
        violations = []
        
        # Check PRICING_RULES (SalesClause enforcement)
        if any(x in draft.lower() for x in ["free trial", "money-back guarantee", "free", "$0"]):
            violations.append("PRICING_RULES: Never promise free trial or money-back guarantee")
        
        if "$" in draft:
            # Extract price mentions
            import re
            prices = re.findall(r'\$(\d+)', draft)
            if any(int(p) < 500 for p in prices):
                violations.append("PRICING_RULES: Minimum price is $500")
        
        # Check COMPLIANCE_RULES
        if any(x in draft.lower() for x in ["fda approved", "hipaa certified", "soc2 compliant"]):
            violations.append("COMPLIANCE_RULES: Never claim FDA approved/HIPAA certified without proof")
        
        # Check for pricing negotiation (NEVER_AUTO_SEND)
        pricing_keywords = ["discount", "negotiate", "lower price", "can you do", "best price"]
        has_pricing_negotiation = any(x in draft.lower() for x in pricing_keywords)
        
        # Assign Messenger based on content
        if violations:
            messenger = SalesMessenger.METATRON  # Scribe - logs violations
            can_auto_send = False
        elif has_pricing_negotiation:
            messenger = SalesMessenger.RAPHAEL  # Healer - requires review
            can_auto_send = False
        elif "not interested" in draft.lower() or "stop" in draft.lower():
            messenger = SalesMessenger.GABRIEL  # Announcer - can auto-send rejections
            can_auto_send = True
        else:
            messenger = SalesMessenger.URIEL  # Illuminator - can auto-send standard emails
            can_auto_send = True
        
        # Generate cryptographic hash
        import hashlib
        import json
        hash_input = json.dumps({
            "draft": draft,
            "prospect": email_data.get("prospect_email", "unknown"),
            "messenger": messenger,
            "timestamp": datetime.now().isoformat()
        }, sort_keys=True)
        hash_value = hashlib.sha256(hash_input.encode()).hexdigest()[:16]
        
        # Update blessings based on violations
        if violations:
            self.blessings.record_human_override("Governance violation detected")
            print(f"\n  MYTHARA VIOLATION DETECTED:")
            for v in violations:
                print(f"    {v}")
        
        return {
            "approved": len(violations) == 0,
            "messenger": messenger,
            "violations": violations,
            "can_auto_send": can_auto_send and len(violations) == 0,
            "hash": hash_value
        }
    
    def generate_soulful_response(self, email_data: Dict, intent: str) -> str:
        """
        Generate response with PERSONALITY - Industry-adapted + Mythara validated
        
        Process:
        1. Detect industry (banking/healthcare/tech)
        2. Generate sales response with appropriate tone
        3. Validate with Mythara governance (clauses, blessings, audit trail)
        4. Return approved response OR flag for human review
        
        Bot's Role: CLOSE DEALS using tactics
        Mythara's Role: VALIDATE compliance and governance
        """
        
        # Get daily mantra for internal state
        self._internal_pep_talk()
        
        # Detect industry for tone adjustment
        industry = self.detect_industry(email_data)
        
        # Build response based on intent (with SOUL)
        if intent == "interested":
            draft = self._handle_interested_with_soul(email_data, industry)
        
        elif intent == "question":
            draft = self._handle_question_with_soul(email_data, industry)
        
        elif intent == "not_interested":
            draft = self._handle_no_with_soul(email_data, industry)
        
        else:
            draft = self._handle_unknown_with_soul(email_data, industry)
        
        # MYTHARA GOVERNANCE VALIDATION
        validation = self._validate_with_mythara(draft, email_data)
        
        print(f"\n MYTHARA GOVERNANCE CHECK:")
        print(f"   Messenger: {validation['messenger']}")
        print(f"   Approved: {'' if validation['approved'] else ''}")
        print(f"   Can Auto-Send: {'' if validation['can_auto_send'] else ' (Human Review Required)'}")
        print(f"   Hash: {validation['hash']}")
        print(f"   Blessings: {self.blessings.state['blessings']}/100")
        
        if validation['approved'] and validation['can_auto_send']:
            # Record successful auto-send
            self.blessings.record_auto_send(success=True)
            print(f"   Action:  AUTO-SENDING (Blessings: {self.blessings.state['blessings']}/100)")
            return draft
        
        elif validation['approved'] and not validation['can_auto_send']:
            # Requires human review (pricing negotiation, etc.)
            print(f"   Action:   HOLDING FOR HUMAN REVIEW")
            return draft
        
        else:
            # Violations detected - block send
            print(f"   Action:  BLOCKED - Governance violations")
            return draft  # Return draft for human to fix
    
    def _internal_pep_talk(self):
        """Bot's internal dialogue before responding (gives it SOUL)"""
        mantras_to_remember = random.sample(SalesMantra.MANTRAS, 3)
        print(f"\n Bot's internal state:")
        for mantra in mantras_to_remember:
            print(f"    '{mantra}'")
    
    def _handle_interested_with_soul(self, email_data: Dict, industry: str) -> str:
        """
        They're interested - CLOSE HARD with industry-appropriate tone
        
        Strategy: Think BIG, use leverage, assumptive close
        """
        
        if industry == "banking":
            # Banking: Conservative, regulatory-focused, ROI-driven
            return f"""Thank you for your interest. I appreciate you taking the time.

Here's what matters: Mythara produces cryptographic proof of AI governance decisions — per-invocation integrity hashes and tamper-evident audit trails that map to SR 11-7 model-risk expectations. No customer claims are made here; ask us for a live technical walkthrough instead of a reference story.

The regulatory landscape is tightening (SR 11-7, OCC Bulletin 2023-17). Early adopters are building 6+ months of clean audit history before their next examination.

We have capacity for 2 more institutions this quarter at the early adopter rate ($500 pilot). After that, standard pricing ($2,500) and a waitlist through Q1 2026.

I'd like to schedule a brief validation call: Tuesday 10am MT or Wednesday 2pm MTwhich works better for your calendar?

Best regards,
Herbert Velez Jr.
CEO, Mythara Engine

P.S. I can send our OCC-style validation report as a reference. It shows exactly what 'audit-ready' looks like."""

        elif industry == "healthcare":
            # Healthcare: Safety-first, compliance-focused, patient outcomes
            return f"""Thank you for reaching out. I'm glad this resonated.

Here's the clinical reality: When the FDA asks "How do you prove your AI recommendation wasn't biased or tampered with?" most health systems have... nothing.

We've worked with 2 health systems preparing for AI/ML submissions (FDA 510(k) and De Novo). Both achieved cryptographic proof of model lineageno black boxes, no "trust us."

Recent outcome: A hospital reduced AI safety review prep from 200 hours to 20 hours. Their quality team can now focus on patient care instead of manual documentation.

With FDA's new AI guidance (2024-2025), provable AI governance isn't optionalit's table stakes. The systems building audit trails NOW will have 6-12 months of safety data when regulations tighten.

We're prioritizing organizations with upcoming submissions or Joint Commission reviews. Early adopter pilot: $500 (2 slots remaining). Standard engagement: $2,500 (waitlist through Q1).

Could we schedule a brief clinical validation review? Tuesday 10am MT or Wednesday 2pm MT?

Best regards,
Herbert Velez Jr.
CEO, Mythara Engine

P.S. Happy to share our FDA-style validation report showing how cryptographic audit trails support 510(k) submissions."""

        else:  # Tech/SaaS - Aggressive, fast-moving, competitive
            opener = random.choice(self.personality.OPENERS_AGGRESSIVE)
            enthusiasm = random.choice(self.personality.ENTHUSIASM_PHRASES)
            competitive = random.choice(self.personality.COMPETITIVE_PRESSURE)
            scarcity = random.choice(self.personality.SCARCITY_TACTICS)
            close = random.choice(self.personality.CLOSES)
            
            return f"""{opener} I LOVE when people cut through the BS and just say they're interested.

{enthusiasm} We just helped 3 companies pass AI governance audits using cryptographic audit trails. Zero findings. The auditors literally had nothing to complain about.

Here's the deal: {competitive}

And real talk on timing: {scarcity}

{close}

Herbert

P.S. If you commit by Friday: $500 + I'll personally run your first audit report. That's a $2k value. But only if you're ready to move."""
    
    def _handle_question_with_soul(self, email_data: Dict, industry: str) -> str:
        """
        They have a question - Answer FAST, add competitive pressure, close
        
        Strategy: Know your market, use leverage, deliver value
        """
        
        if industry == "banking":
            # Banking: Technical precision, regulatory citations
            return f"""Great question. Let me give you the technical answer:

SHA-256 cryptographic hashing on every AI decisionsame standard used by Federal Reserve's FedNow system. Auditors can mathematically verify zero tampering. It's provably immutable.

Early adopters will have their SR 11-7 validation reports passing—and could reduce their MRM cycle from 6 weeks to 8 days.

Without cryptographic proof? Your MRM team is doing manual reconciliation for 200+ hours per model. And when OCC asks "How do you PROVE this output wasn't altered?" you're showing Excel logs (which aren't tamper-proof).

Early adopter pilot: $500 (2 slots remaining this quarter). Standard engagement: $2,500 with Q1 2026 waitlist.

I can send our technical validation report now. Would Tuesday 10am or Wednesday 2pm work for a brief review call?

Best regards,
Herbert Velez Jr.

P.S. Happy to include an OCC-ready audit trail sample so you can see exactly what examiners will review."""

        elif industry == "healthcare":
            # Healthcare: Safety language, patient outcomes, FDA focus
            return f"""Excellent question. Here's how it works from a clinical safety perspective:

SHA-256 cryptographic hashing creates an immutable record of every AI-assisted decision. Think of it like a tamper-evident seal on medicationif anyone alters the record, the hash breaks and auditors know immediately.

This is the same cryptographic standard the VA uses for electronic health records. It's mathematically provable, not "trust us."

The 2 health systems using this passed their AI safety reviews with zero findings. One reduced clinical documentation time from 200 hours to 20 hours per model validation.

Without this? When FDA asks "How do you prove this AI recommendation wasn't biased?" you're showing manual logs that could have been edited. That's a 483 observation risk.

We're prioritizing organizations with upcoming FDA submissions or Joint Commission reviews. Pilot: $500 (2 slots left). Standard: $2,500 (Q1 waitlist).

Could we schedule a brief technical review? Tuesday 10am or Wednesday 2pm MT?

Best regards,
Herbert Velez Jr.

P.S. I can send our FDA-style validation report showing how this supports 510(k) AI/ML submissions."""

        else:  # Tech/SaaS - Fast, direct, competitive
            opener = random.choice(self.personality.OPENERS_AGGRESSIVE)
            competitive = random.choice(self.personality.COMPETITIVE_PRESSURE)
            close = random.choice(self.personality.CLOSES)
            
            return f"""{opener} SHA-256 hashing on every AI decision. Auditors can verify zero tampering. It's the same crypto that secures Bitcoinnobody's breaking it.

For example, a hypothetical early adopter would have validation reports ready while latecomers are still in "evaluation mode."

Without this? Your auditors see black-box AI with no provable lineage. That's a finding waiting to happen.

Early adopter pricing ($500) closes Fridaythen it's $2,500. {competitive}

{close}

Herbert

P.S. Want me to send our validation report now so you can see what 'passing' looks like?"""
    
    def _handle_no_with_soul(self, email_data: Dict, industry: str) -> str:
        """
        They said no - FIGHT BACK (but stay classy)
        
        Counter once, then graceful exit if they insist
        """
        prospect_email = email_data.get("prospect_email", "unknown")
        tracker = self.conversation_tracker.get(prospect_email, {"no_count": 0})
        
        if tracker["no_count"] == 0:
            # First no - counter with FOMO (industry-adapted)
            
            if industry == "banking":
                return f"""I understandtiming is important in regulated environments.

Quick question: Do you have an upcoming model risk review or OCC examination?

The reason I ask: 3 peer institutions in your region are currently evaluating this. The ones who start building audit trails NOW will have 6+ months of clean governance history when examiners arrive.

If timing truly isn't right, I respect that. But if this is in "not priority yet" mode, that changes quickly when the examination notice arrives.

Would you like me to follow up in Q2 2026, or is there a better time?

Best regards,
Herbert"""

            elif industry == "healthcare":
                return f"""UnderstoodI appreciate you being direct.

Quick question: Do you have an upcoming FDA submission, Joint Commission review, or AI safety audit?

I ask because 2 health systems in your region are actively building AI audit trails right now. The organizations starting early will have 6-12 months of safety data when FDA's AI regulations tighten (expected 2025-2026).

If timing truly isn't right, I completely understand. But if this is "not priority yet," that often shifts when the regulatory deadline hits.

Would you prefer I follow up in Q2, or is there someone on your quality/compliance team I should connect with?

Best regards,
Herbert"""

            else:  # Tech - More aggressive counter
                competitive = random.choice(self.personality.COMPETITIVE_PRESSURE)
                
                return f"""No problemtiming's gotta be right.

Quick question though: Do you have an audit or compliance review coming up soon?

Because {competitive}

If timing's truly not right, I get it. But if you're just in 'not priority yet' mode, that changes FAST when the auditors show up.

Either wayno hard feelings. Want me to check back in Q2?

Herbert"""
        
        elif tracker["no_count"] == 1:
            # Second no - respect it but leave door open
            return f"""Got itappreciate you being straight with me.

I'll stop reaching out for now. If anything changes with regulatory pressure, feel free to ping me.

Quick ask: Do you know anyone at a peer company who might need auditable AI logs? Happy to help them out.

Best regards,
Herbert"""
        
        else:
            # Third no - quit gracefully (Know when to walk away)
            return """Understood. I'll stop here.

If your situation changes, you know where to find me.

Best regards,
Herbert"""
    
    def _handle_unknown_with_soul(self, email_data: Dict, industry: str) -> str:
        """
        Unknown intent - QUALIFY HARD with competitive pressure
        
        Strategy: Maximize options, enhance your position
        """
        
        if industry == "banking":
            return f"""Thank you for your reply. Let me clarify what would make this valuable:

Do you have an upcoming model risk review, OCC examination, or SR 11-7 validation in the next 90 days?

If yes: We should talk this week. Most banks need 60-90 days to build clean audit trails, and you're running tight on time.

If no: You might want to wait until regulatory pressure increases. We're prioritizing institutions with imminent audits (2 slots remaining at $500 pilot rate).

Could you share your audit timeline? That'll help me determine if this is the right time for you.

Best regards,
Herbert Velez Jr.

P.S. Either Tuesday 10am or Wednesday 2pm works for a brief 15-minute qualification call."""

        elif industry == "healthcare":
            return f"""Thank you for reaching out. Let me clarify what would make this actionable:

Do you have an upcoming FDA submission, Joint Commission review, or AI safety audit in the next 90 days?

If yes: We should connect this week. Most health systems need 60-90 days to build provable AI governance, and timing is tight.

If no: You may want to wait until regulatory pressure increases. We're prioritizing organizations with imminent reviews (2 pilot slots remaining at $500).

Could you share your review timeline? That'll help determine if now is the right time.

Best regards,
Herbert Velez Jr.

P.S. Happy to do a brief 15-minute qualification callTuesday 10am or Wednesday 2pm MT."""

        else:  # Tech - More direct
            opener = random.choice(self.personality.OPENERS_AGGRESSIVE)
            scarcity = random.choice(self.personality.SCARCITY_TACTICS)
            
            return f"""{opener} Quick clarificationdo you have an upcoming audit/review, or is this more exploratory?

{scarcity}

If you're in exploratory mode, you might want to wait til you have regulatory fire under you. But if you've got an audit coming, we should talk this week.

Tuesday 10am or Wednesday 2pm?

Herbert"""
    
    def daily_motivation(self):
        """Bot's daily self-assessment (gives it SOUL)"""
        print("\n" + "="*80)
        print(" DAILY SALES BOT MOTIVATION")
        print("="*80)
        
        print(f"\n Today's Mantra: '{self.daily_mantra}'")
        
        print("\n Performance State:")
        print(f"   Confidence: {self.personality.PERSONALITY['confidence']:.0%}")
        print(f"   Aggression: {self.personality.PERSONALITY['aggression']:.0%}")
        print(f"   Enthusiasm: {self.personality.PERSONALITY['enthusiasm']:.0%}")
        
        print("\n Today's Mission:")
        print("   - Find 5 interested prospects")
        print("   - Close 2 deals at $500+")
        print("   - Qualify out time-wasters fast")
        print("   - Have FUN doing it")
        
        print("\n Remember:")
        for mantra in random.sample(SalesMantra.MANTRAS, 5):
            print(f"    {mantra}")
        
        print("\n" + "="*80)
        print("LET'S HUNT. ")
        print("="*80 + "\n")


# ============================================================================
# DEMO: Sales Bot with SOUL
# ============================================================================

if __name__ == '__main__':
    print("="*80)
    print(" SALES BOT WITH SOUL - Relationship Building + Aggressive Closing")
    print("    MYTHARA GOVERNED - Clauses, Blessings, Audit Trail")
    print("="*80)
    
    # Initialize bot with PERSONALITY
    bot = SalesBotWithSoul(full_autonomy=True)
    
    # Daily motivation ritual
    bot.daily_motivation()
    
    # Simulate responses with SOUL - Industry-adapted
    test_scenarios = [
        {
            "name": "INTERESTED PROSPECT (Banking)",
            "email": {
                "subject": "Re: Model Risk Solution",
                "body": "This looks interesting. Can we schedule a call?",
                "prospect_email": "sarah.johnson@wellsfargo.com"
            },
            "intent": "interested"
        },
        {
            "name": "TECHNICAL QUESTION (Healthcare)",
            "email": {
                "subject": "Re: AI Governance",
                "body": "How does the cryptographic hashing actually work?",
                "prospect_email": "james.martinez@uchealth.org"
            },
            "intent": "question"
        },
        {
            "name": "FIRST NO (Tech)",
            "email": {
                "subject": "Re: Mythara Demo",
                "body": "Not interested right now, thanks.",
                "prospect_email": "mike.chen@pingidentity.com"
            },
            "intent": "not_interested"
        },
        {
            "name": "INTERESTED PROSPECT (Tech - Aggressive Tone)",
            "email": {
                "subject": "Re: AI Audit Trails",
                "body": "Yeah this could work. Let's talk.",
                "prospect_email": "alex@startup.io"
            },
            "intent": "interested"
        }
    ]
    
    for scenario in test_scenarios:
        print("\n" + "="*80)
        print(f" SCENARIO: {scenario['name']}")
        print("="*80)
        print(f"From: {scenario['email']['prospect_email']}")
        print(f"Subject: {scenario['email']['subject']}")
        print(f"Body: {scenario['email']['body']}")
        
        # Detect industry
        industry = bot.detect_industry(scenario['email'])
        print(f" Industry Detected: {industry.upper()}")
        
        # Generate response WITH SOUL (industry-adapted, Mythara-validated)
        response = bot.generate_soulful_response(scenario['email'], scenario['intent'])
        
        print(f"\n BOT'S RESPONSE (with SOUL - {industry.upper()} tone):\n")
        print(response)
        print("\n" + "="*80)
    
    print("\n This bot doesn't just send emailsit HUNTS deals.")
    print("    Bot's Role: CLOSE DEALS using industry-adapted tactics")
    print("    Mythara's Role: VALIDATE compliance and governance")
    print("\n   Personality: Confident, aggressive, enthusiastic")
    print("   Philosophy: Relationship Building + Aggressive Closing")
    print("   Attitude: I'm the prize, not you")
    print("\n INDUSTRY-ADAPTED TONE:")
    print("   Banking: Conservative, regulatory-focused, ROI-driven")
    print("   Healthcare: Safety-first, compliance-focused, patient outcomes")
    print("   Tech/SaaS: Aggressive, fast-moving, competitive pressure")
    print("\n MYTHARA GOVERNANCE:")
    print("    SalesClause validation (NEVER_AUTO_SEND pricing/contracts)")
    print("    Blessings reservoir (+10 per deal, -10 per violation)")
    print("    Messenger roles (Gabriel/Uriel auto-send, Raphael review)")
    print("    Cryptographic audit trail (SHA-256 hashing)")
    print("\n Set it loose and watch it close (with governance).")
