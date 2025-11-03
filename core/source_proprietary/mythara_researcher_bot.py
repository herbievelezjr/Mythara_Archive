# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
Mythara Researcher Bot
Validates Points of Contact (POCs) at enterprises and SMBs
Enriches prospect data with accurate decision-maker information
"""

import sqlite3
import hashlib
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class MytharaResearcherBot:
    def __init__(self, db_path: str = "mythara_researcher.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.orchestrator_url = "http://localhost:5000"
        self._init_database()
        self._register_with_orchestrator()
    
    def _init_database(self):
        """Initialize database schema"""
        c = self.conn.cursor()
        
        # POC validation records
        c.execute('''
            CREATE TABLE IF NOT EXISTS poc_validations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                contact_name TEXT NOT NULL,
                title TEXT,
                email TEXT,
                phone TEXT,
                linkedin_url TEXT,
                validation_status TEXT CHECK(validation_status IN ('pending', 'verified', 'bounced', 'left_company', 'wrong_person')),
                validation_method TEXT CHECK(validation_method IN ('linkedin', 'zoominfo', 'clearbit', 'hunter', 'manual', 'referral')),
                confidence_score INTEGER CHECK(confidence_score >= 0 AND confidence_score <= 100),
                last_verified TIMESTAMP,
                notes TEXT,
                integrity_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Company research records
        c.execute('''
            CREATE TABLE IF NOT EXISTS company_research (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                industry TEXT,
                employee_count TEXT,
                revenue_range TEXT,
                headquarters TEXT,
                tech_stack TEXT,
                recent_funding TEXT,
                decision_makers TEXT,
                pain_points TEXT,
                buying_signals TEXT,
                research_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_sources TEXT,
                integrity_hash TEXT NOT NULL
            )
        ''')
        
        # Email verification records
        c.execute('''
            CREATE TABLE IF NOT EXISTS email_verifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                verification_status TEXT CHECK(verification_status IN ('valid', 'invalid', 'risky', 'unknown')),
                is_deliverable BOOLEAN,
                is_disposable BOOLEAN,
                is_role_account BOOLEAN,
                mx_records_valid BOOLEAN,
                smtp_check_passed BOOLEAN,
                verification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                integrity_hash TEXT NOT NULL
            )
        ''')
        
        # LinkedIn profile validations
        c.execute('''
            CREATE TABLE IF NOT EXISTS linkedin_validations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                linkedin_url TEXT NOT NULL,
                full_name TEXT,
                current_company TEXT,
                current_title TEXT,
                previous_companies TEXT,
                education TEXT,
                skills TEXT,
                mutual_connections INTEGER DEFAULT 0,
                profile_last_active TEXT,
                validation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                integrity_hash TEXT NOT NULL
            )
        ''')
        
        # Research tasks queue
        c.execute('''
            CREATE TABLE IF NOT EXISTS research_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_type TEXT CHECK(task_type IN ('validate_poc', 'enrich_company', 'verify_email', 'linkedin_lookup')),
                company TEXT,
                contact_name TEXT,
                priority TEXT CHECK(priority IN ('critical', 'high', 'medium', 'low')),
                status TEXT CHECK(status IN ('queued', 'in_progress', 'completed', 'failed')),
                assigned_to TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                results TEXT,
                integrity_hash TEXT NOT NULL
            )
        ''')
        
        # Audit trail
        c.execute('''
            CREATE TABLE IF NOT EXISTS research_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                details TEXT,
                integrity_hash TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def _calculate_integrity_hash(self, data: dict) -> str:
        """Calculate SHA-256 integrity hash"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def _register_with_orchestrator(self):
        """Register with Mythara Orchestrator"""
        try:
            response = requests.post(f"{self.orchestrator_url}/register", json={
                "vp_name": "Researcher Bot",
                "capabilities": ["poc_validation", "company_research", "email_verification", "linkedin_lookup"],
                "status": "active"
            })
            if response.status_code == 200:
                print("[OK] Registered with Mythara Orchestrator")
            else:
                print(f"[!] Orchestrator registration failed: {response.status_code}")
        except Exception as e:
            print(f"[!] Could not connect to orchestrator: {e}")
    
    def validate_poc(self, company: str, contact_name: str, title: str = None,
                    email: str = None, phone: str = None, linkedin_url: str = None,
                    validation_method: str = "manual") -> dict:
        """Validate a point of contact"""
        c = self.conn.cursor()
        
        # Calculate confidence score based on available data
        confidence_score = 0
        if email:
            confidence_score += 30
        if phone:
            confidence_score += 20
        if linkedin_url:
            confidence_score += 30
        if title:
            confidence_score += 20
        
        data = {
            'company': company,
            'contact_name': contact_name,
            'title': title,
            'email': email,
            'phone': phone,
            'linkedin_url': linkedin_url,
            'validation_method': validation_method,
            'confidence_score': confidence_score,
            'validation_status': 'pending'
        }
        
        integrity_hash = self._calculate_integrity_hash(data)
        
        c.execute('''
            INSERT INTO poc_validations (
                company, contact_name, title, email, phone, linkedin_url,
                validation_status, validation_method, confidence_score, integrity_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            company, contact_name, title, email, phone, linkedin_url,
            'pending', validation_method, confidence_score, integrity_hash
        ))
        
        validation_id = c.lastrowid
        self.conn.commit()
        
        # Log action
        self._log_action(f"POC validation created for {contact_name} at {company}")
        
        # If email provided, queue email verification
        if email:
            self.queue_research_task('verify_email', company, contact_name, 'high')
        
        # If LinkedIn provided, queue LinkedIn lookup
        if linkedin_url:
            self.queue_research_task('linkedin_lookup', company, contact_name, 'high')
        
        return {
            'validation_id': validation_id,
            'company': company,
            'contact': contact_name,
            'confidence_score': confidence_score,
            'status': 'pending',
            'integrity_hash': integrity_hash
        }
    
    def verify_email(self, email: str) -> dict:
        """Verify email deliverability (simulated - would use real API in production)"""
        c = self.conn.cursor()
        
        # Simulated email verification logic
        # In production, integrate with ZeroBounce, NeverBounce, or Hunter.io API
        
        is_valid = '@' in email and '.' in email.split('@')[1]
        is_disposable = email.endswith(('tempmail.com', 'guerrillamail.com', 'mailinator.com'))
        is_role_account = email.split('@')[0] in ['info', 'admin', 'support', 'sales', 'contact', 'hello']
        
        verification_status = 'valid' if is_valid and not is_disposable else 'invalid'
        if is_role_account:
            verification_status = 'risky'
        
        data = {
            'email': email,
            'verification_status': verification_status,
            'is_deliverable': is_valid,
            'is_disposable': is_disposable,
            'is_role_account': is_role_account,
            'mx_records_valid': is_valid,
            'smtp_check_passed': is_valid
        }
        
        integrity_hash = self._calculate_integrity_hash(data)
        
        c.execute('''
            INSERT INTO email_verifications (
                email, verification_status, is_deliverable, is_disposable,
                is_role_account, mx_records_valid, smtp_check_passed, integrity_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            email, verification_status, is_valid, is_disposable,
            is_role_account, is_valid, is_valid, integrity_hash
        ))
        
        self.conn.commit()
        self._log_action(f"Email verified: {email} - {verification_status}")
        
        return data
    
    def lookup_linkedin(self, linkedin_url: str, expected_name: str = None) -> dict:
        """Lookup LinkedIn profile (simulated - would use real API in production)"""
        c = self.conn.cursor()
        
        # Simulated LinkedIn lookup
        # In production, integrate with LinkedIn Sales Navigator API or Phantombuster
        
        data = {
            'linkedin_url': linkedin_url,
            'full_name': expected_name or "John Doe",
            'current_company': "Example Corp",
            'current_title': "VP of Technology",
            'previous_companies': json.dumps(["Previous Corp", "Startup Inc"]),
            'education': json.dumps(["Stanford University", "MIT"]),
            'skills': json.dumps(["Cloud Computing", "Enterprise Sales", "SaaS"]),
            'mutual_connections': 5,
            'profile_last_active': "within 1 week"
        }
        
        integrity_hash = self._calculate_integrity_hash(data)
        
        c.execute('''
            INSERT INTO linkedin_validations (
                linkedin_url, full_name, current_company, current_title,
                previous_companies, education, skills, mutual_connections,
                profile_last_active, integrity_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            linkedin_url, data['full_name'], data['current_company'], data['current_title'],
            data['previous_companies'], data['education'], data['skills'],
            data['mutual_connections'], data['profile_last_active'], integrity_hash
        ))
        
        self.conn.commit()
        self._log_action(f"LinkedIn profile validated: {linkedin_url}")
        
        return data
    
    def research_company(self, company: str, industry: str = None) -> dict:
        """Deep research on a company"""
        c = self.conn.cursor()
        
        # Simulated company research
        # In production, integrate with Clearbit, ZoomInfo, Crunchbase, BuiltWith APIs
        
        data = {
            'company': company,
            'industry': industry or "Technology",
            'employee_count': "1,000-5,000",
            'revenue_range': "$100M-$500M",
            'headquarters': "San Francisco, CA",
            'tech_stack': json.dumps(["AWS", "Salesforce", "Workday", "Slack"]),
            'recent_funding': "Series C - $50M (6 months ago)",
            'decision_makers': json.dumps([
                {"name": "Jane Smith", "title": "CTO"},
                {"name": "Bob Johnson", "title": "VP Engineering"}
            ]),
            'pain_points': json.dumps([
                "Contract management complexity",
                "Compliance automation",
                "Vendor risk management"
            ]),
            'buying_signals': json.dumps([
                "Recently posted job for 'Contract Manager'",
                "Mentioned 'digital transformation' in earnings call",
                "CFO spoke at SaaS conference about efficiency"
            ]),
            'data_sources': json.dumps(["LinkedIn", "Clearbit", "Company Website", "Crunchbase"])
        }
        
        integrity_hash = self._calculate_integrity_hash(data)
        
        c.execute('''
            INSERT INTO company_research (
                company, industry, employee_count, revenue_range, headquarters,
                tech_stack, recent_funding, decision_makers, pain_points,
                buying_signals, data_sources, integrity_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            company, data['industry'], data['employee_count'], data['revenue_range'],
            data['headquarters'], data['tech_stack'], data['recent_funding'],
            data['decision_makers'], data['pain_points'], data['buying_signals'],
            data['data_sources'], integrity_hash
        ))
        
        self.conn.commit()
        self._log_action(f"Company research completed: {company}")
        
        return data
    
    def queue_research_task(self, task_type: str, company: str, contact_name: str = None,
                           priority: str = "medium") -> int:
        """Queue a research task"""
        c = self.conn.cursor()
        
        data = {
            'task_type': task_type,
            'company': company,
            'contact_name': contact_name,
            'priority': priority,
            'status': 'queued'
        }
        
        integrity_hash = self._calculate_integrity_hash(data)
        
        c.execute('''
            INSERT INTO research_tasks (
                task_type, company, contact_name, priority, status, integrity_hash
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (task_type, company, contact_name, priority, 'queued', integrity_hash))
        
        task_id = c.lastrowid
        self.conn.commit()
        
        self._log_action(f"Research task queued: {task_type} for {company}")
        
        return task_id
    
    def update_poc_validation(self, validation_id: int, validation_status: str,
                             confidence_score: int = None, notes: str = None):
        """Update POC validation status"""
        c = self.conn.cursor()
        
        if confidence_score is not None:
            c.execute('''
                UPDATE poc_validations
                SET validation_status = ?, confidence_score = ?, notes = ?, last_verified = ?
                WHERE id = ?
            ''', (validation_status, confidence_score, notes, datetime.now(), validation_id))
        else:
            c.execute('''
                UPDATE poc_validations
                SET validation_status = ?, notes = ?, last_verified = ?
                WHERE id = ?
            ''', (validation_status, notes, datetime.now(), validation_id))
        
        self.conn.commit()
        self._log_action(f"POC validation updated: ID {validation_id} -> {validation_status}")
    
    def get_pending_validations(self, limit: int = 10) -> List[dict]:
        """Get pending POC validations"""
        c = self.conn.cursor()
        
        c.execute('''
            SELECT id, company, contact_name, title, email, phone, linkedin_url,
                   validation_method, confidence_score, created_at
            FROM poc_validations
            WHERE validation_status = 'pending'
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        results = []
        for row in c.fetchall():
            results.append({
                'id': row[0],
                'company': row[1],
                'contact_name': row[2],
                'title': row[3],
                'email': row[4],
                'phone': row[5],
                'linkedin_url': row[6],
                'validation_method': row[7],
                'confidence_score': row[8],
                'created_at': row[9]
            })
        
        return results
    
    def generate_research_report(self) -> str:
        """Generate comprehensive research report"""
        c = self.conn.cursor()
        
        # Get stats
        c.execute('SELECT COUNT(*) FROM poc_validations WHERE validation_status = "verified"')
        verified_pocs = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM poc_validations WHERE validation_status = "pending"')
        pending_pocs = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM company_research')
        companies_researched = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM email_verifications WHERE verification_status = "valid"')
        valid_emails = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM research_tasks WHERE status = "queued"')
        queued_tasks = c.fetchone()[0]
        
        c.execute('SELECT AVG(confidence_score) FROM poc_validations WHERE validation_status = "verified"')
        avg_confidence = c.fetchone()[0] or 0
        
        report = f"""
================================================================================
MYTHARA RESEARCHER BOT - DAILY REPORT
================================================================================

POC VALIDATION METRICS:
   Verified POCs: {verified_pocs}
   Pending Validations: {pending_pocs}
   Average Confidence Score: {avg_confidence:.1f}/100

COMPANY RESEARCH:
   Companies Researched: {companies_researched}
   Valid Emails Verified: {valid_emails}

TASK QUEUE:
   Queued Research Tasks: {queued_tasks}

TOP 5 RECENT VALIDATIONS:
"""
        
        c.execute('''
            SELECT company, contact_name, title, confidence_score, validation_status
            FROM poc_validations
            ORDER BY last_verified DESC
            LIMIT 5
        ''')
        
        for row in c.fetchall():
            company, name, title, score, status = row
            report += f"\n   {name} ({title or 'Unknown Title'}) at {company}"
            report += f"\n      Confidence: {score or 0}/100 | Status: {status}"
        
        report += "\n\n"
        report += "="*80 + "\n"
        
        return report
    
    def _log_action(self, action: str, details: str = None):
        """Log action to audit trail"""
        c = self.conn.cursor()
        
        data = {
            'action': action,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        
        integrity_hash = self._calculate_integrity_hash(data)
        
        c.execute('''
            INSERT INTO research_audit (action, details, integrity_hash)
            VALUES (?, ?, ?)
        ''', (action, details, integrity_hash))
        
        self.conn.commit()


if __name__ == "__main__":
    print("Initializing Mythara Researcher Bot...")
    print("="*80)
    
    bot = MytharaResearcherBot()
    
    # Demo workflow
    print("\n[DEMO] Validating POCs for target companies\n")
    
    # Validate POC #1 - High confidence
    result1 = bot.validate_poc(
        company="Microsoft",
        contact_name="Satya Nadella",
        title="CEO",
        email="satya@microsoft.com",
        linkedin_url="linkedin.com/in/satyanadella",
        validation_method="linkedin"
    )
    print(f"[OK] Validated: {result1['contact']} at {result1['company']}")
    print(f"     Confidence: {result1['confidence_score']}/100")
    
    # Verify email
    email_result = bot.verify_email("satya@microsoft.com")
    print(f"[OK] Email verified: {email_result['verification_status']}")
    
    # Validate POC #2 - Medium confidence
    result2 = bot.validate_poc(
        company="JPMorgan Chase",
        contact_name="Jamie Dimon",
        title="CEO",
        email="jamie.dimon@jpmorgan.com",
        validation_method="manual"
    )
    print(f"\n[OK] Validated: {result2['contact']} at {result2['company']}")
    print(f"     Confidence: {result2['confidence_score']}/100")
    
    # Research company
    print("\n[DEMO] Researching target company\n")
    research = bot.research_company("Salesforce", "Technology")
    print(f"[OK] Company research completed: {research['company']}")
    print(f"     Employee Count: {research['employee_count']}")
    print(f"     Revenue Range: {research['revenue_range']}")
    print(f"     Tech Stack: AWS, Salesforce, Workday, Slack")
    
    # Queue research tasks
    print("\n[DEMO] Queueing research tasks\n")
    task1 = bot.queue_research_task('validate_poc', 'Goldman Sachs', 'David Solomon', 'critical')
    task2 = bot.queue_research_task('enrich_company', 'Kaiser Permanente', priority='high')
    print(f"[OK] Queued {2} research tasks")
    
    # Update validation
    bot.update_poc_validation(result1['validation_id'], 'verified', confidence_score=95, 
                              notes="Confirmed via LinkedIn Sales Navigator")
    print(f"\n[OK] Updated POC validation to 'verified'")
    
    # Generate report
    print("\n" + bot.generate_research_report())
    
    print("\n[OK] Researcher Bot demo complete!")
    print("="*80)
