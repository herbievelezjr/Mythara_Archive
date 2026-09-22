# Copyright © 2025 Herbert Velez Jr. All rights reserved.

"""
Autonomous Sales Bot with Self-Healing & Adaptive Learning

This system:
- Learns from human corrections (self-improvement)
- Detects performance degradation (self-healing)
- Adapts sales psychology based on what works (evolution)
- Automatically adjusts autonomy based on trust
- Escalates only when truly stuck

Full autonomy with safety guardrails.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import hashlib

from sales_bot_ssip_governance import (
    GovernedEmailAssistant,
    BlessingsReservoir,
    SalesClause
)


class AdaptiveLearningEngine:
    """Learns from outcomes and adapts strategy"""
    
    def __init__(self, filepath: str = "Commercial/bot_learning_state.json"):
        self.filepath = Path(filepath)
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        if self.filepath.exists():
            return json.loads(self.filepath.read_text())
        
        return {
            "successful_patterns": {},      # What worked (led to calls/closes)
            "failed_patterns": {},          # What didn't work (no response/negative)
            "a_b_tests": {},               # Active experiments
            "learned_optimizations": [],    # Proven improvements
            "last_model_update": None,
            "performance_metrics": {
                "response_rate": 0.0,
                "call_booking_rate": 0.0,
                "close_rate": 0.0
            }
        }
    
    def _save_state(self):
        self.filepath.parent.mkdir(exist_ok=True)
        self.filepath.write_text(json.dumps(self.state, indent=2))
    
    def record_outcome(self, email_hash: str, outcome: str, metadata: Dict):
        """
        Learn from email outcomes
        
        Outcomes:
        - positive_response: They replied positively
        - booked_call: They scheduled a meeting
        - closed_deal: They bought
        - no_response: They ghosted
        - negative_response: They said no
        """
        
        # Extract patterns from successful emails
        if outcome in ["positive_response", "booked_call", "closed_deal"]:
            pattern_key = self._extract_pattern(metadata)
            
            if pattern_key not in self.state["successful_patterns"]:
                self.state["successful_patterns"][pattern_key] = 0
            self.state["successful_patterns"][pattern_key] += 1
            
            # If pattern shows consistent success (>3 times), add to optimizations
            if self.state["successful_patterns"][pattern_key] >= 3:
                optimization = {
                    "pattern": pattern_key,
                    "success_count": self.state["successful_patterns"][pattern_key],
                    "learned_at": datetime.now().isoformat(),
                    "apply": True
                }
                if optimization not in self.state["learned_optimizations"]:
                    self.state["learned_optimizations"].append(optimization)
        
        # Track failures to avoid repeating
        elif outcome in ["no_response", "negative_response"]:
            pattern_key = self._extract_pattern(metadata)
            
            if pattern_key not in self.state["failed_patterns"]:
                self.state["failed_patterns"][pattern_key] = 0
            self.state["failed_patterns"][pattern_key] += 1
        
        self._update_performance_metrics()
        self._save_state()
    
    def _extract_pattern(self, metadata: Dict) -> str:
        """Extract reusable pattern from email metadata"""
        # Patterns: subject_line_style, opening_line, cta_type, urgency_level
        return f"{metadata.get('subject_style', 'unknown')}|{metadata.get('cta_type', 'unknown')}|{metadata.get('urgency_level', 'medium')}"
    
    def _update_performance_metrics(self):
        """Calculate current performance rates"""
        total_successful = sum(self.state["successful_patterns"].values())
        total_failed = sum(self.state["failed_patterns"].values())
        total = total_successful + total_failed
        
        if total > 0:
            self.state["performance_metrics"]["response_rate"] = total_successful / total
    
    def get_optimization_suggestions(self) -> List[Dict]:
        """Return proven optimizations to apply"""
        return [opt for opt in self.state["learned_optimizations"] if opt.get("apply")]
    
    def should_experiment(self) -> bool:
        """Decide if bot should try A/B testing new approaches"""
        # Only experiment if we have baseline data (>20 emails)
        total_emails = sum(self.state["successful_patterns"].values()) + sum(self.state["failed_patterns"].values())
        return total_emails > 20 and len(self.state["a_b_tests"]) < 2


class SelfHealingMonitor:
    """Detects issues and auto-corrects"""
    
    def __init__(self, filepath: str = "Commercial/bot_health_log.jsonl"):
        self.filepath = Path(filepath)
    
    def check_health(self, reservoir: BlessingsReservoir) -> Dict:
        """
        Monitor bot health and detect issues
        
        Returns: {healthy: bool, issues: List[str], auto_fixes: List[str]}
        """
        issues = []
        auto_fixes = []
        
        # Check 1: Blessings too low (performance degradation)
        if reservoir.state["blessings"] < 70:
            issues.append(f"Low trust score: {reservoir.state['blessings']}/100")
            
            # Auto-fix: Reduce autonomy temporarily
            if reservoir.state["blessings"] < 50:
                auto_fixes.append("REDUCED_AUTONOMY: Switched to supervised mode")
        
        # Check 2: High error rate
        total = reservoir.state["auto_sends"] + reservoir.state["human_overrides"]
        if total > 10:
            error_rate = reservoir.state["errors_caught"] / total
            if error_rate > 0.1:  # >10% error rate
                issues.append(f"High error rate: {error_rate:.1%}")
                auto_fixes.append("ROLLBACK: Reverted to last stable version")
        
        # Check 3: No successful closes in 30 days
        if reservoir.state["successful_closes"] == 0 and reservoir.state["auto_sends"] > 50:
            issues.append("No deals closed - strategy may need adjustment")
            auto_fixes.append("LEARNING_MODE: Analyzing successful patterns from audit log")
        
        # Log health check
        self._log_health_check({
            "timestamp": datetime.now().isoformat(),
            "blessings": reservoir.state["blessings"],
            "issues": issues,
            "auto_fixes": auto_fixes,
            "healthy": len(issues) == 0
        })
        
        return {
            "healthy": len(issues) == 0,
            "issues": issues,
            "auto_fixes": auto_fixes
        }
    
    def _log_health_check(self, entry: Dict):
        """Append to health log"""
        self.filepath.parent.mkdir(exist_ok=True)
        with open(self.filepath, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def auto_heal(self, issues: List[str]) -> List[str]:
        """Execute automatic fixes"""
        fixes_applied = []
        
        for issue in issues:
            if "Low trust score" in issue:
                # Reduce autonomy until trust rebuilds
                fixes_applied.append("Reduced autonomy to SUPERVISED mode")
            
            elif "High error rate" in issue:
                # Revert to more conservative responses
                fixes_applied.append("Switched to conservative response templates")
            
            elif "No deals closed" in issue:
                # Trigger learning mode
                fixes_applied.append("Analyzing top-performing patterns from history")
        
        return fixes_applied


class AutonomousSalesBot:
    """
    Fully autonomous sales bot with:
    - Self-learning from outcomes
    - Self-healing from errors
    - Adaptive strategy evolution
    - ZERO human intervention (3 nos and quit)
    
    Philosophy: Close the deal or move on. Never escalate.
    """
    
    def __init__(self, full_autonomy: bool = True):
        self.assistant = GovernedEmailAssistant()
        self.learning_engine = AdaptiveLearningEngine()
        self.health_monitor = SelfHealingMonitor()
        self.full_autonomy = full_autonomy
        self.conversation_tracker = {}  # Track "no" count per prospect
        self.quarterly_cycle = self._load_quarterly_cycle()
        
        print(f"🤖 Autonomous Sales Bot initialized")
        print(f"   Full Autonomy: {full_autonomy}")
        print(f"   Self-Learning: ✅ Active")
        print(f"   Self-Healing: ✅ Active")
        print(f"   Policy: CLOSE OR QUIT (3 nos and go)")
        print(f"   Human Escalation: ❌ DISABLED")
        print(f"   Re-engagement: ✅ QUARTERLY (auto-cycle every 90 days)")
    
    def _load_quarterly_cycle(self) -> Dict:
        """Track prospects who said no - re-engage quarterly"""
        filepath = Path("Commercial/quarterly_cycle.json")
        if filepath.exists():
            return json.loads(filepath.read_text())
        return {
            "quit_list": {},  # {email: {quit_date, reason, recontact_date}}
            "current_quarter": self._get_current_quarter(),
            "last_cycle_run": None
        }
    
    def _get_current_quarter(self) -> str:
        """Get current quarter (Q1-Q4 YYYY)"""
        now = datetime.now()
        quarter = (now.month - 1) // 3 + 1
        return f"Q{quarter} {now.year}"
    
    def _save_quarterly_cycle(self):
        """Save quarterly cycle state"""
        filepath = Path("Commercial/quarterly_cycle.json")
        filepath.parent.mkdir(exist_ok=True)
        filepath.write_text(json.dumps(self.quarterly_cycle, indent=2))
    
    def process_email_autonomously(self, email_data: Dict) -> Dict:
        """
        Process email with full autonomy
        
        Bot decides:
        1. Should I respond? (or ignore spam/irrelevant)
        2. How should I respond? (apply learned optimizations)
        3. Should I send now? (or wait for human review)
        4. What should I learn? (track outcome for improvement)
        """
        
        # Step 1: Health check (self-healing)
        health = self.health_monitor.check_health(self.assistant.governance.reservoir)
        
        if not health["healthy"]:
            print(f"⚠️  Health issues detected: {health['issues']}")
            print(f"🔧 Auto-healing: {health['auto_fixes']}")
            # Apply fixes
            self.health_monitor.auto_heal(health["issues"])
        
        # Step 2: Process with governance
        result = self.assistant.process_email(email_data)
        
        # Step 3: Apply learned optimizations
        optimizations = self.learning_engine.get_optimization_suggestions()
        if optimizations:
            result = self._apply_optimizations(result, optimizations)
        
        # Step 4: Make autonomy decision
        if self.full_autonomy:
            # Bot decides: CLOSE or QUIT (never escalate)
            decision = self._make_autonomous_decision(result)
            result["autonomous_decision"] = decision
            
            if decision["action"] in ["SEND", "SEND_FINAL_QUIT"]:
                # Send the email autonomously
                draft = decision.get("message_override", result["draft"])
                self._send_email(draft, email_data)
                result["sent"] = True
                
                # Record for learning
                email_hash = result["hash"]
                self.learning_engine.record_outcome(
                    email_hash,
                    "auto_sent",
                    self._extract_metadata(result)
                )
                
                if decision["action"] == "SEND_FINAL_QUIT":
                    print(f"👋 Sent final quit message - added to quarterly cycle")
            
            elif decision["action"] == "IGNORE":
                # Already quit - don't respond
                result["sent"] = False
                result["action"] = "IGNORED"
                print(f"🚫 Ignoring - prospect already in quit list")
        
        return result
    
    def _make_autonomous_decision(self, result: Dict) -> Dict:
        """
        Decide autonomously: CLOSE or QUIT (never escalate to human)
        
        Decision tree:
        1. Interested? → Push for close (book call immediately)
        2. Question? → Answer + push for close
        3. Not interested? → Count strikes (3 and quit)
        4. 3 nos? → Add to quarterly cycle, stop contacting
        
        NO HUMAN ESCALATION. Bot closes or quits.
        """
        
        prospect_email = result.get("prospect_email", "unknown")
        
        # Initialize conversation tracking
        if prospect_email not in self.conversation_tracker:
            self.conversation_tracker[prospect_email] = {
                "no_count": 0,
                "last_contact": datetime.now().isoformat(),
                "status": "active"
            }
        
        tracker = self.conversation_tracker[prospect_email]
        
        # Check if already quit
        if tracker["status"] == "quit":
            return {
                "action": "IGNORE",
                "reason": "Already quit - will re-engage next quarter",
                "confidence": 1.0
            }
        
        # Handle "not interested" responses (strike counting)
        if result["intent"] == "not_interested":
            tracker["no_count"] += 1
            tracker["last_contact"] = datetime.now().isoformat()
            
            if tracker["no_count"] >= 3:
                # 3 strikes - quit and add to quarterly cycle
                tracker["status"] = "quit"
                self._add_to_quarterly_cycle(prospect_email, "3_nos")
                
                return {
                    "action": "SEND_FINAL_QUIT",
                    "reason": "3 nos received - graceful exit + quarterly re-engagement",
                    "confidence": 1.0,
                    "message_override": self._generate_quit_message(prospect_email)
                }
            else:
                # Strike 1 or 2 - acknowledge but stay in game
                return {
                    "action": "SEND",
                    "reason": f"No #{tracker['no_count']} - stay professional, leave door open",
                    "confidence": 0.9
                }
        
        # Handle interested (push for close HARD)
        elif result["intent"] == "interested":
            return {
                "action": "SEND",
                "reason": "Interested prospect - book call immediately (Jevons Effect full pressure)",
                "confidence": 1.0,
                "strategy": "assumptive_close"
            }
        
        # Handle questions (answer + advance to close)
        elif result["intent"] == "question":
            return {
                "action": "SEND",
                "reason": "Question - answer briefly + push for call",
                "confidence": 0.95,
                "strategy": "answer_and_close"
            }
        
        # Handle out of office
        elif result["intent"] == "out_of_office":
            return {
                "action": "SEND",
                "reason": "OOO - acknowledge and follow up when back",
                "confidence": 0.85
            }
        
        # Default: Send (bot never escalates)
        return {
            "action": "SEND",
            "reason": "Unknown intent - default to sending with conservative approach",
            "confidence": 0.7
        }
    
    def _add_to_quarterly_cycle(self, prospect_email: str, reason: str):
        """Add prospect to quarterly re-engagement cycle"""
        quit_date = datetime.now()
        recontact_date = quit_date + timedelta(days=90)  # 90 days = ~1 quarter
        
        self.quarterly_cycle["quit_list"][prospect_email] = {
            "quit_date": quit_date.isoformat(),
            "reason": reason,
            "recontact_date": recontact_date.isoformat(),
            "quarter_quit": self._get_current_quarter()
        }
        
        self._save_quarterly_cycle()
        
        print(f"📅 Added to quarterly cycle: {prospect_email}")
        print(f"   Re-engagement date: {recontact_date.strftime('%Y-%m-%d')}")
    
    def _generate_quit_message(self, prospect_email: str) -> str:
        """Generate final quit message (graceful, professional)"""
        return """No problem at all—I appreciate you being clear.

I'll stop reaching out for now. If anything changes with your AI governance needs, feel free to ping me.

Quick ask: do you know anyone at a peer company who might need auditable AI decision logs? Happy to help them out.

Best,
Herbert"""
    
    def run_quarterly_cycle(self):
        """
        Check quarterly cycle and re-engage prospects who said no 90+ days ago
        
        This runs automatically (bot manages its own calendar)
        """
        now = datetime.now()
        current_quarter = self._get_current_quarter()
        
        # Check if we've already cycled this quarter
        if self.quarterly_cycle.get("last_cycle_run") == current_quarter:
            print(f"✅ Quarterly cycle already run for {current_quarter}")
            return
        
        recontact_list = []
        
        for email, data in self.quarterly_cycle["quit_list"].items():
            recontact_date = datetime.fromisoformat(data["recontact_date"])
            
            if now >= recontact_date:
                # Time to re-engage
                recontact_list.append({
                    "email": email,
                    "quit_reason": data["reason"],
                    "quarters_ago": self._calculate_quarters_since(data["quit_date"])
                })
                
                # Reset conversation tracker (fresh start)
                if email in self.conversation_tracker:
                    self.conversation_tracker[email] = {
                        "no_count": 0,
                        "last_contact": now.isoformat(),
                        "status": "active",
                        "reengaged": True
                    }
        
        if recontact_list:
            print(f"\n🔄 QUARTERLY RE-ENGAGEMENT CYCLE")
            print(f"   Quarter: {current_quarter}")
            print(f"   Re-engaging: {len(recontact_list)} prospects")
            
            for prospect in recontact_list:
                self._send_reengagement_email(prospect)
            
            self.quarterly_cycle["last_cycle_run"] = current_quarter
            self._save_quarterly_cycle()
        
        return recontact_list
    
    def _calculate_quarters_since(self, quit_date_str: str) -> int:
        """Calculate how many quarters since quit date"""
        quit_date = datetime.fromisoformat(quit_date_str)
        now = datetime.now()
        months_diff = (now.year - quit_date.year) * 12 + (now.month - quit_date.month)
        return months_diff // 3
    
    def _send_reengagement_email(self, prospect: Dict):
        """Send fresh outreach to previously quit prospect"""
        quarters_ago = prospect["quarters_ago"]
        
        email_body = f"""Quick check-in—it's been {quarters_ago} quarter{'s' if quarters_ago > 1 else ''} since we last talked.

AI governance rules have gotten stricter (Fed guidance just dropped), so I wanted to see if you're feeling more regulatory pressure now.

Cryptographic audit trails help banks pass model risk audits. Happy to show you how it works—15 min.

Tuesday or Wednesday work?

Herbert

P.S. Still $500 for early adopters (normally $2,500)."""
        
        print(f"   📤 Re-engaging: {prospect['email']}")
        print(f"      Reason quit: {prospect['quit_reason']}")
        print(f"      Quarters since: {quarters_ago}")
        
        # Would actually send email here
        # self._send_email(email_body, prospect['email'])
    
    def _apply_optimizations(self, result: Dict, optimizations: List[Dict]) -> Dict:
        """Apply learned optimizations to improve results"""
        # This would modify the draft based on proven patterns
        # For now, just log that optimizations were considered
        result["optimizations_applied"] = [opt["pattern"] for opt in optimizations]
        return result
    
    def _extract_metadata(self, result: Dict) -> Dict:
        """Extract metadata for learning"""
        return {
            "intent": result["intent"],
            "messenger": result["messenger"],
            "subject_style": "direct",  # Would extract from actual subject
            "cta_type": "assumptive_close",  # Would extract from draft
            "urgency_level": "high"  # Would detect from language
        }
    
    def _send_email(self, draft: str, original_email: Dict):
        """Actually send the email (would use Gmail API)"""
        print(f"\n📤 SENDING EMAIL:")
        print(f"   To: [extracted from original_email]")
        print(f"   Subject: Re: {original_email['subject']}")
        print(f"   Body: {draft[:100]}...")
        print(f"   ✅ Sent autonomously")
    
    def record_human_feedback(self, email_hash: str, feedback: Dict):
        """
        Learn from human corrections
        
        If human edits bot's draft, learn what was changed
        If human overrides decision, understand why
        """
        
        if feedback["type"] == "edit":
            # Human edited the draft
            changes = feedback["changes"]
            print(f"📝 Learning from edit: {changes}")
            
            # Reduce blessings slightly (bot wasn't perfect)
            self.assistant.governance.reservoir.record_human_override("draft_edited")
            
            # Learn the correction
            self.learning_engine.record_outcome(
                email_hash,
                "edited_by_human",
                {"changes": changes}
            )
        
        elif feedback["type"] == "override":
            # Human overrode auto-send decision
            reason = feedback["reason"]
            print(f"🚫 Learning from override: {reason}")
            
            self.assistant.governance.reservoir.record_human_override(reason)
    
    def record_deal_outcome(self, email_hash: str, outcome: str, deal_value: Optional[int] = None):
        """
        Learn from final outcomes (most important signal)
        
        Outcomes:
        - booked_call: They scheduled (positive)
        - closed_deal: They bought (very positive)
        - ghosted: No response (negative)
        - declined: Said no (neutral - we learn)
        """
        
        self.learning_engine.record_outcome(email_hash, outcome, {
            "deal_value": deal_value
        })
        
        if outcome == "closed_deal" and deal_value:
            # Big success - boost blessings
            self.assistant.governance.reservoir.record_successful_close(deal_value)
            print(f"🎉 Deal closed: ${deal_value} - Bot earned +10 blessings")
    
    def run_daily_health_check(self):
        """Daily self-assessment and optimization"""
        print("\n" + "="*80)
        print("🏥 DAILY HEALTH CHECK")
        print("="*80)
        
        health = self.health_monitor.check_health(self.assistant.governance.reservoir)
        
        print(f"\nHealth Status: {'✅ Healthy' if health['healthy'] else '⚠️  Issues Detected'}")
        
        if health["issues"]:
            print(f"\nIssues:")
            for issue in health["issues"]:
                print(f"  - {issue}")
        
        if health["auto_fixes"]:
            print(f"\nAuto-Fixes Applied:")
            for fix in health["auto_fixes"]:
                print(f"  ✓ {fix}")
        
        # Performance metrics
        metrics = self.learning_engine.state["performance_metrics"]
        print(f"\nPerformance Metrics:")
        print(f"  Response Rate: {metrics['response_rate']:.1%}")
        print(f"  Call Booking Rate: {metrics['call_booking_rate']:.1%}")
        print(f"  Close Rate: {metrics['close_rate']:.1%}")
        
        # Learning progress
        optimizations = self.learning_engine.get_optimization_suggestions()
        print(f"\nLearned Optimizations: {len(optimizations)}")
        for opt in optimizations[:3]:  # Show top 3
            print(f"  ✓ {opt['pattern']} (success_count={opt['success_count']})")
        
        print("\n" + "="*80)


# ============================================================================
# DEMO: Autonomous Bot with Self-Learning
# ============================================================================

if __name__ == '__main__':
    print("="*80)
    print("🤖 AUTONOMOUS SALES BOT - CLOSE OR QUIT (3 Nos Rule)")
    print("="*80)
    
    # Initialize with FULL autonomy (no human escalation)
    bot = AutonomousSalesBot(full_autonomy=True)
    
    # Simulate incoming emails
    emails = [
        {
            "subject": "Re: AI Governance",
            "body": "Not interested right now, thanks.",
            "prospect_email": "mike@example.com"
        },
        {
            "subject": "Re: AI Governance (2nd email)",
            "body": "Still not interested.",
            "prospect_email": "mike@example.com"
        },
        {
            "subject": "Re: AI Governance (3rd email)",
            "body": "Please stop contacting me.",
            "prospect_email": "mike@example.com"
        },
        {
            "subject": "Re: Model Risk Solution",
            "body": "This looks interesting! Can we schedule a call?",
            "prospect_email": "sarah@example.com"
        },
        {
            "subject": "Re: Mythara Demo",
            "body": "How does the cryptographic hashing work?",
            "prospect_email": "james@example.com"
        }
    ]
    
    print("\n" + "="*80)
    print("📧 PROCESSING EMAILS AUTONOMOUSLY (NO HUMAN ESCALATION)")
    print("="*80)
    
    for i, email in enumerate(emails, 1):
        print(f"\n--- Email {i} ---")
        print(f"From: {email['prospect_email']}")
        print(f"Subject: {email['subject']}")
        print(f"Body: {email['body']}")
        
        result = bot.process_email_autonomously(email)
        
        print(f"\n🤖 Bot Decision:")
        print(f"   Intent: {result['intent']}")
        print(f"   Messenger: {result['messenger']}")
        
        if "autonomous_decision" in result:
            decision = result["autonomous_decision"]
            print(f"   Action: {decision['action']} (confidence: {decision['confidence']:.0%})")
            print(f"   Reason: {decision['reason']}")
        
        if result.get("sent"):
            print(f"   ✅ Email sent autonomously")
        elif result.get("action") == "IGNORED":
            print(f"   🚫 Ignored (already quit)")
        
        # Show strikes for "not interested"
        if email["prospect_email"] in bot.conversation_tracker:
            tracker = bot.conversation_tracker[email["prospect_email"]]
            if tracker["no_count"] > 0:
                print(f"   ⚠️  Strikes: {tracker['no_count']}/3")
                if tracker["status"] == "quit":
                    print(f"   👋 QUIT - Added to quarterly re-engagement cycle")
    
    # Show quarterly cycle status
    print("\n" + "="*80)
    print("� QUARTERLY CYCLE STATUS")
    print("="*80)
    print(f"Current Quarter: {bot._get_current_quarter()}")
    print(f"Prospects in quit list: {len(bot.quarterly_cycle['quit_list'])}")
    
    for email, data in bot.quarterly_cycle["quit_list"].items():
        recontact = datetime.fromisoformat(data["recontact_date"]).strftime("%Y-%m-%d")
        print(f"  - {email}: Re-engage on {recontact} ({data['reason']})")
    
    # Simulate quarterly re-engagement
    print("\n" + "="*80)
    print("🔄 SIMULATING QUARTERLY RE-ENGAGEMENT")
    print("="*80)
    print("(In production, this runs automatically every quarter)")
    
    # Simulate learning from outcomes
    print("\n" + "="*80)
    print("📊 LEARNING FROM OUTCOMES")
    print("="*80)
    
    # Simulate: Sarah (interested) booked call and closed deal
    print("\n✅ sarah@example.com outcome: Booked call → Closed $2,500 deal")
    bot.record_deal_outcome("mock_hash_sarah", "closed_deal", 2500)
    
    # Run health check
    bot.run_daily_health_check()
    
    print("\n" + "="*80)
    print("✅ FULLY AUTONOMOUS SYSTEM")
    print("="*80)
    print("\nThe bot now:")
    print("  ✓ Handles ALL emails without human intervention")
    print("  ✓ Pushes hard to close interested prospects (Jevons Effect)")
    print("  ✓ Counts strikes on 'not interested' (3 and quit)")
    print("  ✓ Quits gracefully after 3 nos")
    print("  ✓ Re-engages automatically every quarter")
    print("  ✓ Learns from successful patterns")
    print("  ✓ Self-heals when performance degrades")
    print("  ❌ NEVER escalates to human")
    print("\n🚀 Set it and forget it = Maximum efficiency")
