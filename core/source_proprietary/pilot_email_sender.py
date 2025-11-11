#!/usr/bin/env python3
"""
Mythara Pilot Purchase Email Sender
Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

Sends welcome email with API key and download link after pilot purchase.
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Email configuration
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("MYTHARA_FROM_EMAIL", "Mythara.Engine@yahoo.com")
FROM_NAME = os.getenv("MYTHARA_FROM_NAME", "Mythara Labs")
PILOT_DOWNLOAD_URL = os.getenv("MYTHARA_PILOT_DOWNLOAD_URL", "")

def send_pilot_welcome_email(
    to_email: str,
    api_key: str,
    customer_name: Optional[str] = None,
    payment_id: Optional[str] = None
) -> bool:
    """
    Send pilot welcome email with API key and download link.
    
    Args:
        to_email: Customer email address
        api_key: Generated pilot API key (sk_pilot_xxx)
        customer_name: Optional customer name
        payment_id: Optional Stripe payment ID for reference
    
    Returns:
        True if email sent successfully, False otherwise
    """
    if not SENDGRID_API_KEY:
        logger.warning("SENDGRID_API_KEY not set, skipping email")
        _log_email_to_console(to_email, api_key, customer_name, payment_id)
        return False
    
    if not PILOT_DOWNLOAD_URL:
        logger.error("MYTHARA_PILOT_DOWNLOAD_URL not set, cannot send email")
        return False
    
    try:
        import sendgrid
        from sendgrid.helpers.mail import Mail, Email, To, Content
        
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        
        # Build email
        subject = "🎉 Welcome to Mythara Engine Pilot Program"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
                .key-box {{ background: #fff; border: 2px solid #667eea; padding: 15px; 
                           border-radius: 6px; margin: 20px 0; font-family: monospace; 
                           word-break: break-all; }}
                .button {{ display: inline-block; background: #667eea; color: white; 
                          padding: 12px 30px; text-decoration: none; border-radius: 6px; 
                          margin: 20px 0; }}
                .steps {{ background: white; padding: 20px; border-radius: 6px; margin: 20px 0; }}
                .step {{ margin: 15px 0; padding-left: 30px; position: relative; }}
                .step:before {{ content: "✓"; position: absolute; left: 0; color: #667eea; 
                               font-weight: bold; font-size: 20px; }}
                .footer {{ text-align: center; color: #666; padding: 20px; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌌 Welcome to Mythara Engine</h1>
                    <p>Your Pilot Access is Ready!</p>
                </div>
                
                <div class="content">
                    <p>Hi{" " + customer_name if customer_name else ""},</p>
                    
                    <p>Thank you for purchasing <strong>Mythara Engine Pilot</strong> ($49 for 30 days). 
                    Your account is now active!</p>
                    
                    <h2>🔑 Your API Key</h2>
                    <div class="key-box">
                        {api_key}
                    </div>
                    <p><small>⚠️ Keep this secret! Don't share publicly or commit to git.</small></p>
                    
                    <h2>📦 Download Your Pilot Package</h2>
                    <p>Your pilot package includes:</p>
                    <ul>
                        <li>Python client library with examples</li>
                        <li>API documentation and quick start guide</li>
                        <li>Docker setup for self-hosted deployment</li>
                        <li>NIST/HIPAA compliance mapping guides</li>
                    </ul>
                    
                    <center>
                        <a href="{PILOT_DOWNLOAD_URL}" class="button">
                            📥 Download Pilot Package (13 KB)
                        </a>
                    </center>
                    
                    <h2>🚀 Quick Start (3 Minutes)</h2>
                    <div class="steps">
                        <div class="step">Unzip the pilot package</div>
                        <div class="step">Set your API key: <code>export MYTHARA_API_KEY="{api_key}"</code></div>
                        <div class="step">Run example: <code>python examples/quickstart.py</code></div>
                        <div class="step">Read README.md for detailed docs</div>
                    </div>
                    
                    <h2>🔗 API Endpoint</h2>
                    <p>Your pilot API is hosted at:</p>
                    <div class="key-box">
                        https://heroic-flexibility-production.up.railway.app
                    </div>
                    
                    <h2>📚 Resources</h2>
                    <ul>
                        <li><strong>API Docs:</strong> <a href="https://heroic-flexibility-production.up.railway.app/api/docs">Interactive Documentation</a></li>
                        <li><strong>Support:</strong> <a href="mailto:Mythara.Engine@yahoo.com">Mythara.Engine@yahoo.com</a></li>
                        <li><strong>Payment Reference:</strong> {payment_id or "N/A"}</li>
                    </ul>
                    
                    <h2>💡 Need Help?</h2>
                    <p>Reply to this email or contact us at 
                    <a href="mailto:Mythara.Engine@yahoo.com">Mythara.Engine@yahoo.com</a></p>
                    
                    <p>We typically respond within 24 hours (often much faster).</p>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                    
                    <p><strong>Ready to upgrade to Enterprise?</strong><br>
                    Contact us for custom deployments, dedicated support, and advanced features.</p>
                </div>
                
                <div class="footer">
                    <p>© 2025 Mythara Labs. All rights reserved.<br>
                    This email contains your API key. Please keep it confidential.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        message = Mail(
            from_email=Email(FROM_EMAIL, FROM_NAME),
            to_emails=To(to_email),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        
        response = sg.send(message)
        
        if response.status_code in [200, 201, 202]:
            logger.info(f"Pilot welcome email sent to {to_email} (status: {response.status_code})")
            return True
        else:
            logger.error(f"SendGrid returned unexpected status: {response.status_code}")
            return False
            
    except ImportError:
        logger.error("sendgrid package not installed. Run: pip install sendgrid")
        _log_email_to_console(to_email, api_key, customer_name, payment_id)
        return False
    except Exception as e:
        logger.error(f"Failed to send pilot email: {e}")
        _log_email_to_console(to_email, api_key, customer_name, payment_id)
        return False


def _log_email_to_console(
    to_email: str,
    api_key: str,
    customer_name: Optional[str],
    payment_id: Optional[str]
) -> None:
    """Log email content to console for manual sending if automated email fails."""
    logger.info("="*80)
    logger.info("PILOT WELCOME EMAIL (manual send required)")
    logger.info("="*80)
    logger.info(f"To: {to_email}")
    logger.info(f"Subject: Welcome to Mythara Engine Pilot Program")
    logger.info("")
    logger.info(f"Customer: {customer_name or 'N/A'}")
    logger.info(f"API Key: {api_key}")
    logger.info(f"Download: {PILOT_DOWNLOAD_URL or 'NOT CONFIGURED'}")
    logger.info(f"Payment ID: {payment_id or 'N/A'}")
    logger.info("="*80)


if __name__ == "__main__":
    # Test the email sender
    logging.basicConfig(level=logging.INFO)
    
    test_email = "test@example.com"
    test_key = "sk_pilot_test123456789"
    
    print("Testing pilot email sender...")
    print(f"SENDGRID_API_KEY set: {bool(SENDGRID_API_KEY)}")
    print(f"PILOT_DOWNLOAD_URL: {PILOT_DOWNLOAD_URL or 'NOT SET'}")
    print()
    
    success = send_pilot_welcome_email(
        to_email=test_email,
        api_key=test_key,
        customer_name="Test Customer",
        payment_id="test_payment_123"
    )
    
    print(f"\nEmail send {'succeeded' if success else 'failed'}")
