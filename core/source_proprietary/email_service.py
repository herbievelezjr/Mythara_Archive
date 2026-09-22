#!/usr/bin/env python3
"""
Mythara Engine - Email Service
SendGrid integration for automated API key delivery and alerts.

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.
"""

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import Optional, Dict, Any
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

# SendGrid API key from environment
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "Mythara.Engine@yahoo.com")
FROM_NAME = os.getenv("FROM_NAME", "Mythara Engine")
SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", "Mythara.Engine@yahoo.com")


def send_email(
    to_email: str, subject: str, body_html: str, body_text: str
) -> Dict[str, Any]:
    """
    Send email via SendGrid.
    Returns status dict with success/error info.
    """
    if not SENDGRID_API_KEY:
        logger.error("SENDGRID_API_KEY not configured - email not sent")
        return {"success": False, "error": "SendGrid not configured"}

    try:
        message = Mail(
            from_email=Email(FROM_EMAIL, FROM_NAME),
            to_emails=To(to_email),
            subject=subject,
            plain_text_content=Content("text/plain", body_text),
            html_content=Content("text/html", body_html),
        )

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        logger.info(
            f"Email sent to {to_email}: {subject} (status {response.status_code})"
        )
        return {"success": True, "status_code": response.status_code}

    except Exception as e:
        logger.error(f"Email send failed to {to_email}: {e}")
        return {"success": False, "error": str(e)}


def send_api_key_delivery(
    to_email: str,
    api_key: str,
    company_name: str,
    employee_count: int,
    total_limit: int,
    pilot_expires: str,
) -> Dict[str, Any]:
    """
    Send API key delivery email post-payment.
    Includes quick start guide and expiration info.
    """
    subject = f"🌱 Your Mythara Pilot API Key - {company_name}"

    body_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; }}
            .api-key {{ background: #f7fafc; padding: 15px; border-radius: 5px; font-family: monospace; font-size: 14px; word-break: break-all; border: 2px solid #4299e1; }}
            .warning {{ background: #fff5f5; border-left: 4px solid #f56565; padding: 15px; margin: 20px 0; }}
            .info {{ background: #ebf8ff; border-left: 4px solid #4299e1; padding: 15px; margin: 20px 0; }}
            .cta {{ background: #4299e1; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌱 Welcome to Mythara Engine Pilot</h1>
                <p>{company_name}</p>
            </div>
            
            <h2>✅ Payment Confirmed - Your Pilot Starts Now</h2>
            <p>Your 7-day pilot access is active! Here's everything you need to get started.</p>
            
            <h3>🔑 Your API Key</h3>
            <div class="api-key">{api_key}</div>
            
            <div class="warning">
                <strong>⚠️ Keep This Secret!</strong><br>
                This API key grants access to your pilot. Never share it publicly or commit it to version control.
            </div>
            
            <h3>📊 Your Pilot Details</h3>
            <ul>
                <li><strong>Company:</strong> {company_name}</li>
                <li><strong>Employees:</strong> {employee_count}</li>
                <li><strong>7-Day Total Limit:</strong> {total_limit:,} API calls</li>
                <li><strong>Pilot Expires:</strong> {pilot_expires}</li>
            </ul>
            
            <div class="info">
                <strong>💡 24/7 AI Agent Operation</strong><br>
                Your rate limit is designed for continuous AI agent operation (20 calls/hour per employee). Use it wisely across your team!
            </div>
            
            <h3>🚀 Quick Start Guide</h3>
            <pre style="background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 5px; overflow-x: auto;">
# Test your API key
curl -X POST https://mythara-engine.railway.app/v1/clauses/invoke \\
  -H "Authorization: Bearer {api_key}" \\
  -H "Content-Type: application/json" \\
  -d '{{"clause_name": "test", "input_text": "Hello Mythara"}}'
            </pre>
            
            <h3>📚 Documentation</h3>
            <p>Full API documentation: <a href="https://mythara-engine.railway.app/api/docs">https://mythara-engine.railway.app/api/docs</a></p>
            
            <h3>📈 Check Your Pilot Status</h3>
            <pre style="background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 5px; overflow-x: auto;">
curl -X GET https://mythara-engine.railway.app/v1/pilot/status \\
  -H "Authorization: Bearer {api_key}"
            </pre>
            
            <h3>🎯 Need Help?</h3>
            <ul>
                <li><strong>Support:</strong> <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></li>
                <li><strong>Upgrade to Enterprise:</strong> Unlimited calls, dedicated support, 99.9% SLA</li>
                <li><strong>Refund Policy:</strong> ALL SALES FINAL - Exchanges to equal or lesser value only</li>
            </ul>
            
            <a href="mailto:{SUPPORT_EMAIL}?subject=Pilot%20Support%20-%20{company_name}" class="cta">Get Support</a>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #e2e8f0;">
            <p style="font-size: 12px; color: #718096;">
                <strong>Mythara Engine</strong><br>
                Copyright © 2025 Herbert Velez Jr. All rights reserved.<br>
                Proprietary and Confidential.
            </p>
        </div>
    </body>
    </html>
    """

    body_text = f"""
🌱 Welcome to Mythara Engine Pilot - {company_name}

✅ PAYMENT CONFIRMED - Your Pilot Starts Now

Your 7-day pilot access is active! Here's everything you need to get started.

🔑 YOUR API KEY
{api_key}

⚠️ KEEP THIS SECRET! Never share it publicly or commit it to version control.

📊 YOUR PILOT DETAILS
- Company: {company_name}
- Employees: {employee_count}
- 7-Day Total Limit: {total_limit:,} API calls
- Pilot Expires: {pilot_expires}

💡 Your rate limit is designed for continuous AI agent operation (20 calls/hour per employee).

🚀 QUICK START GUIDE
Test your API key:
curl -X POST https://mythara-engine.railway.app/v1/clauses/invoke \\
  -H "Authorization: Bearer {api_key}" \\
  -H "Content-Type: application/json" \\
  -d '{{"clause_name": "test", "input_text": "Hello Mythara"}}'

📚 DOCUMENTATION
Full API docs: https://mythara-engine.railway.app/api/docs

📈 CHECK YOUR PILOT STATUS
curl -X GET https://mythara-engine.railway.app/v1/pilot/status \\
  -H "Authorization: Bearer {api_key}"

🎯 NEED HELP?
Support: {SUPPORT_EMAIL}
Upgrade to Enterprise: Unlimited calls, dedicated support, 99.9% SLA
Refund Policy: ALL SALES FINAL - Exchanges to equal or lesser value only

---
Mythara Engine
Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.
    """

    return send_email(to_email, subject, body_html, body_text)


def send_usage_alert_80_percent(
    to_email: str,
    api_key: str,
    company_name: str,
    calls_used: int,
    total_limit: int,
    pilot_expires: str,
) -> Dict[str, Any]:
    """
    Send alert when pilot hits 80% of call limit.
    Proactive warning to prevent surprise lockout.
    """
    percent_used = (calls_used / total_limit) * 100
    calls_remaining = total_limit - calls_used

    subject = f"⚠️ 80% Usage Alert - {company_name} Pilot"

    body_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .warning {{ background: #fff5f5; border-left: 4px solid #f56565; padding: 20px; margin: 20px 0; border-radius: 5px; }}
            .stats {{ background: #f7fafc; padding: 15px; border-radius: 5px; }}
            .cta {{ background: #4299e1; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚠️ Usage Alert: 80% of Pilot Limit Reached</h1>
            
            <div class="warning">
                <h2>Action Required: You're Running Low on API Calls</h2>
                <p>Your {company_name} pilot has used <strong>{calls_used:,} of {total_limit:,} calls ({percent_used:.1f}%)</strong>.</p>
                <p>Only <strong>{calls_remaining:,} calls remaining</strong> before your pilot is exhausted.</p>
            </div>
            
            <div class="stats">
                <h3>📊 Usage Statistics</h3>
                <ul>
                    <li><strong>Calls Used:</strong> {calls_used:,} / {total_limit:,}</li>
                    <li><strong>Calls Remaining:</strong> {calls_remaining:,}</li>
                    <li><strong>Pilot Expires:</strong> {pilot_expires}</li>
                </ul>
            </div>
            
            <h3>🎯 What Happens Next?</h3>
            <p>Once you reach {total_limit:,} calls OR {pilot_expires}, whichever comes first:</p>
            <ul>
                <li>❌ All API requests will return HTTP 402 (Payment Required)</li>
                <li>❌ No additional calls will be processed</li>
                <li>✅ Your pilot data remains accessible for 30 days for exchange purposes</li>
            </ul>
            
            <h3>💼 Upgrade to Enterprise</h3>
            <p>Never worry about limits again:</p>
            <ul>
                <li>🚀 Unlimited API calls</li>
                <li>☁️ Fully managed hosting</li>
                <li>🛡️ 99.9% SLA with 24/7 support</li>
                <li>💰 $49 pilot credit applied to your Enterprise tier</li>
            </ul>
            
            <a href="mailto:{SUPPORT_EMAIL}?subject=Upgrade%20to%20Enterprise%20-%20{company_name}" class="cta">Upgrade Now</a>
            
            <p style="font-size: 12px; color: #718096; margin-top: 30px;">
                <strong>Refund Policy:</strong> ALL SALES FINAL - Exchanges to equal or lesser value only.<br>
                Support: {SUPPORT_EMAIL}
            </p>
        </div>
    </body>
    </html>
    """

    body_text = f"""
⚠️ USAGE ALERT: 80% of Pilot Limit Reached

ACTION REQUIRED: You're Running Low on API Calls

Your {company_name} pilot has used {calls_used:,} of {total_limit:,} calls ({percent_used:.1f}%).
Only {calls_remaining:,} calls remaining before your pilot is exhausted.

📊 USAGE STATISTICS
- Calls Used: {calls_used:,} / {total_limit:,}
- Calls Remaining: {calls_remaining:,}
- Pilot Expires: {pilot_expires}

🎯 WHAT HAPPENS NEXT?
Once you reach {total_limit:,} calls OR {pilot_expires}, whichever comes first:
❌ All API requests will return HTTP 402 (Payment Required)
❌ No additional calls will be processed
✅ Your pilot data remains accessible for 30 days for exchange purposes

💼 UPGRADE TO ENTERPRISE
Never worry about limits again:
🚀 Unlimited API calls
☁️ Fully managed hosting
🛡️ 99.9% SLA with 24/7 support
💰 $49 pilot credit applied to your Enterprise tier

To upgrade, email: {SUPPORT_EMAIL}

---
Refund Policy: ALL SALES FINAL - Exchanges to equal or lesser value only.
Support: {SUPPORT_EMAIL}
    """

    return send_email(to_email, subject, body_html, body_text)


def send_expiration_alert_24hr(
    to_email: str,
    api_key: str,
    company_name: str,
    calls_used: int,
    total_limit: int,
    pilot_expires: str,
) -> Dict[str, Any]:
    """
    Send alert 24 hours before pilot expiration.
    Final warning before lockout.
    """
    calls_remaining = total_limit - calls_used
    percent_used = (calls_used / total_limit) * 100

    subject = f"⏰ 24 Hour Warning - {company_name} Pilot Expires Tomorrow"

    body_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .urgent {{ background: #fff5f5; border: 3px solid #f56565; padding: 20px; margin: 20px 0; border-radius: 5px; }}
            .stats {{ background: #f7fafc; padding: 15px; border-radius: 5px; }}
            .cta {{ background: #f56565; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⏰ Final Warning: Pilot Expires in 24 Hours</h1>
            
            <div class="urgent">
                <h2>🚨 Your {company_name} Pilot Ends Tomorrow</h2>
                <p><strong>Expiration Date:</strong> {pilot_expires}</p>
                <p>After this time, all API requests will be rejected with HTTP 402 (Payment Required).</p>
            </div>
            
            <div class="stats">
                <h3>📊 Final Usage Report</h3>
                <ul>
                    <li><strong>Calls Used:</strong> {calls_used:,} / {total_limit:,} ({percent_used:.1f}%)</li>
                    <li><strong>Calls Remaining:</strong> {calls_remaining:,}</li>
                    <li><strong>Time Remaining:</strong> ~24 hours</li>
                </ul>
            </div>
            
            <h3>🎯 Options After Expiration</h3>
            
            <h4>💼 Option 1: Upgrade to Enterprise (Recommended)</h4>
            <ul>
                <li>🚀 Unlimited API calls (no more limits)</li>
                <li>☁️ Fully managed hosting</li>
                <li>🛡️ 99.9% SLA with 24/7 support</li>
                <li>💰 <strong>$49 pilot credit applied</strong> (pay only $24,951 for $25K Foundation tier)</li>
            </ul>
            
            <h4>🔄 Option 2: Exchange to Self-Hosted Pilot</h4>
            <ul>
                <li>Same $49 value</li>
                <li>You host on your infrastructure (AWS, Azure, Docker)</li>
                <li>No usage limits</li>
                <li>Full control over deployment</li>
            </ul>
            
            <h4>❌ Option 3: Do Nothing</h4>
            <ul>
                <li>API access terminates at expiration</li>
                <li>30-day grace period to request exchange</li>
                <li>After 30 days, pilot data is purged</li>
            </ul>
            
            <a href="mailto:{SUPPORT_EMAIL}?subject=Upgrade%20or%20Exchange%20-%20{company_name}" class="cta">Take Action Now</a>
            
            <p style="font-size: 12px; color: #718096; margin-top: 30px;">
                <strong>Refund Policy:</strong> ALL SALES FINAL - Exchanges to equal or lesser value only.<br>
                No refunds, no extensions, no exceptions.<br>
                Support: {SUPPORT_EMAIL}
            </p>
        </div>
    </body>
    </html>
    """

    body_text = f"""
⏰ FINAL WARNING: Pilot Expires in 24 Hours

🚨 YOUR {company_name.upper()} PILOT ENDS TOMORROW

Expiration Date: {pilot_expires}
After this time, all API requests will be rejected with HTTP 402 (Payment Required).

📊 FINAL USAGE REPORT
- Calls Used: {calls_used:,} / {total_limit:,} ({percent_used:.1f}%)
- Calls Remaining: {calls_remaining:,}
- Time Remaining: ~24 hours

🎯 OPTIONS AFTER EXPIRATION

💼 OPTION 1: Upgrade to Enterprise (Recommended)
🚀 Unlimited API calls (no more limits)
☁️ Fully managed hosting
🛡️ 99.9% SLA with 24/7 support
💰 $49 pilot credit applied (pay only $24,951 for $25K Foundation tier)

🔄 OPTION 2: Exchange to Self-Hosted Pilot
- Same $49 value
- You host on your infrastructure (AWS, Azure, Docker)
- No usage limits
- Full control over deployment

❌ OPTION 3: Do Nothing
- API access terminates at expiration
- 30-day grace period to request exchange
- After 30 days, pilot data is purged

To upgrade or exchange, email: {SUPPORT_EMAIL}

---
Refund Policy: ALL SALES FINAL - Exchanges to equal or lesser value only.
No refunds, no extensions, no exceptions.
Support: {SUPPORT_EMAIL}
    """

    return send_email(to_email, subject, body_html, body_text)


def send_strike_warning(
    to_email: str,
    api_key: str,
    company_name: str,
    strike_count: int,
    reason: str,
    suspended_until: Optional[datetime] = None,
) -> Dict[str, Any]:
    """
    Send strike notification to pilot for self-regulation violation.
    """
    if strike_count == 1:
        subject = f"⚠️ Strike #1 Warning - {company_name}"
        action = "This is a warning. Please adjust your usage patterns."
    elif strike_count == 2:
        subject = f"🚫 Strike #2: 7-Day Suspension - {company_name}"
        action = f"Your account is suspended until {suspended_until.strftime('%Y-%m-%d %H:%M UTC')}. API calls will be rejected during this period."
    else:
        subject = f"❌ Strike #3: Account Terminated - {company_name}"
        action = "Your account has been permanently terminated. Contact support if you believe this is an error."

    body_html = f"""
    <html>
    <body style="font-family: sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1>Self-Regulation Strike #{strike_count}</h1>
        <p><strong>Company:</strong> {company_name}</p>
        <p><strong>Reason:</strong> {reason}</p>
        <p><strong>Action Taken:</strong> {action}</p>
        
        <h2>What Happened?</h2>
        <p>Our self-regulation system detected abuse patterns in your API usage:</p>
        <ul>
            <li>Velocity abuse: Exhausted pilot in less than 24 hours</li>
            <li>Usage mismatch: Actual usage 3x+ higher than expected for your employee count</li>
        </ul>
        
        <h2>Graduated Enforcement</h2>
        <ul>
            <li><strong>Strike 1:</strong> Warning (current: {strike_count})</li>
            <li><strong>Strike 2:</strong> 7-day suspension</li>
            <li><strong>Strike 3:</strong> Permanent termination</li>
        </ul>
        
        <p>Support: {SUPPORT_EMAIL}</p>
    </body>
    </html>
    """

    body_text = f"""
Self-Regulation Strike #{strike_count}

Company: {company_name}
Reason: {reason}
Action Taken: {action}

WHAT HAPPENED?
Our self-regulation system detected abuse patterns in your API usage:
- Velocity abuse: Exhausted pilot in less than 24 hours
- Usage mismatch: Actual usage 3x+ higher than expected for your employee count

GRADUATED ENFORCEMENT
- Strike 1: Warning (current: {strike_count})
- Strike 2: 7-day suspension
- Strike 3: Permanent termination

Support: {SUPPORT_EMAIL}
    """

    return send_email(to_email, subject, body_html, body_text)
