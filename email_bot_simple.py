#!/usr/bin/env python3
"""
Mythara Email Bot - Simple Manual Version
Read exported emails and generate drafts using Mythara Engine.

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

SETUP INSTRUCTIONS:
1. Export emails from Yahoo Mail to a folder
2. Point this script at that folder
3. Script generates drafts for review
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

# Mythara Engine Settings
MYTHARA_API = os.getenv("MYTHARA_API_URL", "http://localhost:8000")
MYTHARA_API_KEY = os.getenv("MYTHARA_API_KEY", "ent_prod_key_001")

# Directories
INBOX_DIR = Path("inbox_export")  # Put exported emails here
DRAFTS_DIR = Path("email_drafts")
DRAFTS_DIR.mkdir(exist_ok=True)
LOG_FILE = DRAFTS_DIR / "email_bot.log"

# ============================================================================
# SIMPLIFIED APPROACH
# ============================================================================

def log(message):
    """Log messages"""
    timestamp = datetime.utcnow().isoformat() + "Z"
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")

def classify_email(sender, subject, body):
    """Classify email intent"""
    body_lower = body.lower()
    
    if any(word in body_lower for word in ["trial", "pilot", "demo"]):
        return {"intent": "pilot_inquiry", "template": "pilot_delivery"}
    elif any(word in body_lower for word in ["price", "cost", "expensive"]):
        return {"intent": "pricing_objection", "template": "objection_price"}
    elif "re:" in subject.lower():
        return {"intent": "follow_up", "template": "follow_up"}
    else:
        return {"intent": "initial_inquiry", "template": "initial_outreach"}

def generate_draft(sender_name, classification):
    """Generate email draft"""
    templates = {
        "initial_outreach": f"""Hi {sender_name},

Thanks for reaching out about Mythara Engine.

We help compliance-focused organizations deliver cryptographic integrity proofs and SSIP audit metrics that cut validation time from weeks to days.

Would a 30-day pilot be valuable? I can send the pilot package today.

Best,
Herbert Velez Jr.
Mythara Labs LLC
mythara.engine@yahoo.com
Enterprise: $60K/year (firm pricing)""",

        "pilot_delivery": f"""Hi {sender_name},

Great! I'll send your pilot package today with:
- Secure pilot ZIP with documentation
- Unique API key for 30-day trial
- Container registry access

I'll follow up within 2 hours with the package.

Best,
Herbert""",

        "follow_up": f"""Hi {sender_name},

Following up on my previous note. Mythara Engine provides cryptographic integrity proofs for compliance validation.

30-day container-based pilot available if timing works.

Best,
Herbert""",

        "objection_price": f"""Hi {sender_name},

I understand budget considerations.

$60K/year covers:
- Cryptographic integrity proofs
- 99.92% determinism
- SSIP audit metrics
- Priority support

Even one prevented compliance incident offsets the subscription.

Firm pricing; 30-day trial is the evaluation period.

Best,
Herbert"""
    }
    
    template_id = classification.get("template", "initial_outreach")
    return templates.get(template_id, templates["initial_outreach"])

def process_manual_email(sender, sender_name, subject, body):
    """Process a single email and generate draft"""
    classification = classify_email(sender, subject, body)
    draft_body = generate_draft(sender_name, classification)
    
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    draft_filename = DRAFTS_DIR / f"draft_{timestamp}.txt"
    
    with open(draft_filename, "w", encoding="utf-8") as f:
        f.write("="*80 + "\n")
        f.write("MYTHARA EMAIL BOT - DRAFT FOR REVIEW\n")
        f.write("="*80 + "\n\n")
        f.write(f"To: {sender}\n")
        f.write(f"Subject: Re: {subject}\n")
        f.write(f"\nClassification: {classification['intent']}\n")
        f.write("\n" + "-"*80 + "\n\n")
        f.write(draft_body)
        f.write("\n\n" + "="*80 + "\n")
    
    log(f"Draft created: {draft_filename}")
    return draft_filename

# ============================================================================
# INTERACTIVE MODE
# ============================================================================

def interactive_mode():
    """Run bot in interactive mode - you paste email details"""
    log("="*80)
    log("MYTHARA EMAIL BOT - Interactive Mode")
    log("="*80)
    
    print("\n" + "="*80)
    print("MYTHARA EMAIL BOT")
    print("="*80)
    print("\nThis bot will help you generate email drafts.")
    print("You'll paste email details, and it will create a draft response.\n")
    
    while True:
        print("\n" + "-"*80)
        print("Enter email details (or type 'quit' to exit):")
        print("-"*80)
        
        sender_email = input("\nSender's email address: ").strip()
        if sender_email.lower() == 'quit':
            break
            
        sender_name = input("Sender's name (or press Enter to skip): ").strip() or "there"
        subject = input("Email subject: ").strip()
        
        print("\nEmail body (paste the message, then press Enter twice):")
        body_lines = []
        empty_count = 0
        while empty_count < 2:
            line = input()
            if line == "":
                empty_count += 1
            else:
                empty_count = 0
                body_lines.append(line)
        body = "\n".join(body_lines)
        
        # Generate draft
        print("\n" + "="*80)
        print("Generating draft...")
        print("="*80)
        
        draft_file = process_manual_email(
            sender=sender_email,
            sender_name=sender_name,
            subject=subject,
            body=body
        )
        
        print(f"\n✓ Draft saved to: {draft_file}")
        print("\nYou can:")
        print("1. Open the file to review the draft")
        print("2. Copy it to Yahoo Mail")
        print("3. Process another email\n")
        
        continue_prompt = input("Process another email? (yes/no): ").strip().lower()
        if continue_prompt != 'yes':
            break
    
    print("\n" + "="*80)
    print(f"All drafts saved to: {DRAFTS_DIR}")
    print("="*80)

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    interactive_mode()
