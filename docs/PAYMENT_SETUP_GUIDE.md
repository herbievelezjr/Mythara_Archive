# Mythara Engine - Payment & License Activation Guide

**Copyright © 2025 Herbert Velez Jr. All rights reserved.**  
**Proprietary and Confidential.**

---

## Overview

This guide covers:
1. Setting up payment processing (Stripe recommended)
2. Generating and validating license keys
3. Automating pilot → enterprise transitions
4. Direct deposit configuration

---

## 1. Payment Provider Setup (Stripe)

### Why Stripe?
- ACH direct deposit to business account (2-day settlement)
- Built-in invoice/receipt generation
- PCI compliance handled
- Webhook automation for license delivery
- Lower fees than PayPal for B2B (2.9% + $0.30)

### Quick Setup Steps

```bash
# 1. Create Stripe account at https://stripe.com
# 2. Get your API keys from Dashboard → Developers → API keys
# 3. Add to your .env file:

STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# 4. Install Stripe SDK
pip install stripe
```

### Environment variables

Configure these in your container or .env (test vs live values accordingly):

```bash
# Enterprise purchase link (Stripe Payment Link)
MYTHARA_PURCHASE_URL=https://buy.stripe.com/your-enterprise-link

# Stripe secrets
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Contact email shown in prompts and error payloads
MYTHARA_CONTACT_EMAIL=Mythara.Engine@yahoo.com
```

#### Optional: $49 pilot paywall

To require a one-time pilot access fee before activating the 30‑day trial, set:

```bash
MYTHARA_PILOT_PAYWALL=true
MYTHARA_PILOT_PRICE_USD=49
MYTHARA_PILOT_PURCHASE_URL=https://buy.stripe.com/your-pilot-link
```

Recommended Stripe settings for Payment Links:
- $49 link: set Payment Link metadata `license_type=pilot` and add a Custom field named `company_name`.
- Enterprise link: set metadata `license_type=enterprise` and a Custom field named `company_name`.

The webhook uses `session.metadata.license_type` to decide whether to grant pilot access or issue a license. If metadata is missing, it infers by amount (≈ $49 → pilot; larger → enterprise).

### Bank Account Connection
1. Go to Stripe Dashboard → Settings → Bank accounts and scheduling
2. Add your business checking account (routing + account number)
3. Verify micro-deposits (1-2 business days)
4. Set payout schedule: Daily automatic (funds arrive in 2 business days)

---

## 2. License Key Generation System

### License Key Format
```
MYTHARA-ENT-[COMPANY_HASH]-[RANDOM]-[CHECKSUM]
Example: MYTHARA-ENT-A7F3D-8K2P9-X4M1
```

### Implementation (`core/source_proprietary/license_manager.py`)

```python
"""
License key generation and validation for Mythara Engine.
Copyright © 2025 Herbert Velez Jr. All rights reserved.
"""

import hashlib
import secrets
import json
from datetime import datetime, timedelta
from typing import Optional, Dict

def generate_license_key(
    edition: str,  # "ENT" or "SOV"
    company_name: str,
    email: str,
    expires_at: Optional[datetime] = None
) -> str:
    """Generate cryptographically secure license key."""
    # Hash company identifier
    company_hash = hashlib.sha256(
        f"{company_name}:{email}".encode()
    ).hexdigest()[:5].upper()
    
    # Random component
    random_part = secrets.token_hex(3).upper()
    
    # Checksum (prevents tampering)
    checksum_input = f"{edition}{company_hash}{random_part}"
    checksum = hashlib.sha256(checksum_input.encode()).hexdigest()[:4].upper()
    
    key = f"MYTHARA-{edition}-{company_hash}-{random_part}-{checksum}"
    
    return key

def validate_license_key(key: str) -> Dict[str, any]:
    """Validate license key format and checksum."""
    try:
        parts = key.split("-")
        if len(parts) != 5 or parts[0] != "MYTHARA":
            return {"valid": False, "error": "Invalid format"}
        
        prefix, edition, company_hash, random_part, checksum = parts
        
        # Verify checksum
        checksum_input = f"{edition}{company_hash}{random_part}"
        expected = hashlib.sha256(checksum_input.encode()).hexdigest()[:4].upper()
        
        if checksum != expected:
            return {"valid": False, "error": "Invalid checksum"}
        
        return {
            "valid": True,
            "edition": "Enterprise" if edition == "ENT" else "Sovereign",
            "company_hash": company_hash
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}

def save_license_to_file(key: str, metadata: Dict, path: str = "/etc/mythara/license.json"):
    """Save license key with metadata (called after payment)."""
    license_data = {
        "license_key": key,
        "issued_at": datetime.utcnow().isoformat() + "Z",
        "company": metadata.get("company_name"),
        "email": metadata.get("email"),
        "edition": metadata.get("edition"),
        "expires_at": metadata.get("expires_at"),  # None for perpetual
        "payment_id": metadata.get("stripe_payment_id")
    }
    
    with open(path, 'w') as f:
        json.dump(license_data, f, indent=2)
    
    return license_data
```

---

## 3. Stripe Payment Integration

### Create Payment Link (Easiest Option)

**No code required** - use Stripe's Payment Links:

1. Go to Stripe Dashboard → Payment Links
2. Click "New payment link"
3. Configure:
   - **Name**: Mythara Enterprise Edition
   - **Amount**: $60,000 USD
   - **Type**: One-time payment
    - **After payment**: Use Stripe-hosted success page (no custom domain required). Optionally add a simple thank-you page later.
   - **Collect**: Name, Email, Company Name
4. Copy the payment link (e.g., `https://buy.stripe.com/abc123`)
5. Add to your outreach emails and `PURCHASE_URL` env var

### Optional Pilot ($49) Payment Link

If you enable a pilot paywall (`MYTHARA_PILOT_PAYWALL=true`), create a second Payment Link:
1. **Name**: Mythara Pilot Access
2. **Amount**: $49 USD (one-time)
3. **Metadata**: `license_type=pilot`
4. **Collect**: Name, Email, Company Name (metadata key should be `company_name`)
5. Set `MYTHARA_PILOT_PURCHASE_URL` to this link in the container

Until the pilot fee is paid, API requests return HTTP 402 with a JSON body:
```json
{
    "error": "pilot_fee_required",
    "message": "A one-time $49 pilot access fee is required before activating the 30-day trial.",
    "pilot_purchase_url": "<your pilot link>",
    "pilot_price_usd": 49
}
```
Once paid, a small JSON file (default `/tmp/mythara_pilot_access.json`) is written and the standard 30‑day trial begins.

### Webhook Handler (Automated License Delivery)

```python
# Add to core/source_proprietary/main.py

import stripe
from fastapi import Request

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

@app.post("/api/webhooks/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe payment confirmation and deliver license."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        logger.error(f"Webhook signature verification failed: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle successful payment
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        
        # Extract customer details
        customer_email = session["customer_details"]["email"]
        customer_name = session["customer_details"]["name"]
        company_name = session.get("metadata", {}).get("company_name", customer_name)
        amount_paid = session["amount_total"] / 100  # Convert cents to dollars
        
        # Generate license key
        edition = "ENT" if amount_paid < 100000 else "SOV"
        license_key = generate_license_key(edition, company_name, customer_email)
        
        # Save to database (or send via email)
        logger.info(f"Generated license {license_key} for {customer_email}")
        
        # Send license key via email (integrate with SendGrid/AWS SES)
        send_license_email(
            to_email=customer_email,
            license_key=license_key,
            company_name=company_name,
            amount_paid=amount_paid
        )
    
    return {"status": "success"}

def send_license_email(to_email: str, license_key: str, company_name: str, amount_paid: float):
    """Send license key via email after payment (implement with your email provider)."""
    subject = f"Your Mythara Enterprise License Key"
    body = f"""
Hi {company_name} team,

Thank you for purchasing Mythara Engine Enterprise Edition (${amount_paid:,.0f} USD).

Your license key:
{license_key}

Activation Instructions:
1. Set environment variable: MYTHARA_LICENSE_KEY={license_key}
2. Restart your Mythara container
3. Verify with: curl http://localhost:8000/v1/license/status

The pilot restrictions have been removed. You now have full Enterprise access.

Need help? Reply to this email or visit https://mytharalabs.com/support

Best regards,
Mythara Labs LLC
"""
    # TODO: Integrate with SendGrid, AWS SES, or your email provider
    logger.info(f"License email sent to {to_email}")
    print(body)  # Replace with actual email send
```

---

## 4. Container License Validation

Update the container startup to check for license key:

```python
# Add to core/source_proprietary/main.py startup

LICENSE_KEY = os.getenv("MYTHARA_LICENSE_KEY")

@app.on_event("startup")
async def validate_license_on_startup():
    """Check license status and enforce trial limits."""
    global LICENSE_MODE
    
    if LICENSE_KEY:
        # Validate enterprise license
        validation = validate_license_key(LICENSE_KEY)
        if validation["valid"]:
            LICENSE_MODE = "enterprise"
            logger.info(f"✅ Enterprise license activated: {validation['edition']}")
            return
        else:
            logger.error(f"❌ Invalid license key: {validation['error']}")
            # Fall through to trial mode
    
    # No valid license - enforce trial
    if LICENSE_MODE == "trial":
        _init_trial_if_needed()
        trial_status = _get_trial_status()
        
        if trial_status["status"] == "EXPIRED":
            logger.error(f"❌ TRIAL EXPIRED - Purchase at {PURCHASE_URL}")
            print("\n" + "="*60)
            print("🚨 MYTHARA ENGINE TRIAL EXPIRED 🚨")
            print(f"Purchase Enterprise license at: {PURCHASE_URL}")
            print(f"Price: ${compute_current_enterprise_price():,} USD/year")
            print("="*60 + "\n")
            # Exit to force upgrade
            import sys
            sys.exit(1)
        else:
            logger.info(f"⏰ Trial mode: {trial_status['days_remaining']} days remaining")

# Block API calls if trial expired
@app.middleware("http")
async def enforce_trial_expiration(request: Request, call_next):
    """Block all API calls if trial has expired."""
    if LICENSE_MODE == "trial":
        trial_status = _get_trial_status()
        if trial_status["status"] == "EXPIRED":
            return Response(
                content=json.dumps({
                    "error": "Trial expired",
                    "message": f"Purchase Enterprise license at {PURCHASE_URL}",
                    "price_usd": compute_current_enterprise_price()
                }),
                status_code=402,  # Payment Required
                media_type="application/json"
            )
    
    response = await call_next(request)
    return response
```

---

## 5. Upgrade Messaging in Trial

Add clear upgrade prompts to the API responses:

```python
# Update license status endpoint
@app.get("/v1/license/status", response_model=LicenseStatusResponse)
async def license_status(api_key: str = Depends(verify_api_key)):
    """Get current license status and upgrade pricing"""
    if LICENSE_KEY:
        validation = validate_license_key(LICENSE_KEY)
        return LicenseStatusResponse(
            edition="Enterprise",
            is_trial=False,
            status="ACTIVE",
            purchase_url=None,
            upgrade_price_usd_year=None,
            message="Enterprise license active"
        )
    
    trial_status = _get_trial_status()
    price = compute_current_enterprise_price()
    
    if trial_status["status"] == "EXPIRED":
        message = f"⚠️ Trial expired. Upgrade now at {PURCHASE_URL}"
    else:
        message = f"✅ {trial_status['days_remaining']} days remaining. Upgrade anytime to remove restrictions."
    
    return LicenseStatusResponse(
        edition="Trial",
        is_trial=True,
        trial_started_at=trial_status.get("trial_started_at"),
        trial_ends_at=trial_status.get("trial_ends_at"),
        days_remaining=trial_status.get("days_remaining"),
        status=trial_status["status"],
        purchase_url=PURCHASE_URL,
        upgrade_price_usd_year=price,
        message=message
    )
```

---

## 6. Outreach Email Update

Add clear purchase CTA to your pilot package emails:

```
Subject: Mythara Engine pilot + Enterprise pricing

Hi [Name],

Attaching our 30-day free pilot (container-only, air-gapped ready).

After pilot validation:
→ Enterprise Edition: $60,000/year*
→ Purchase: https://buy.stripe.com/[your-link]
→ License delivered instantly via email

*Pricing increases 3% annually. Lock in 2025 rate before Dec 31.

15-min walkthrough available this week.

Best,
Herbert
```

---

## 7. Post-Purchase Flow

1. **Customer pays via Stripe Payment Link**
2. **Stripe webhook fires** → `/api/webhooks/stripe`
3. **License key generated** → Sent to customer email
4. **Customer adds key** → `MYTHARA_LICENSE_KEY=MYTHARA-ENT-...`
5. **Container restarts** → Detects license, exits trial mode
6. **Full access activated** → No more expiration checks

---

## 8. Testing the Flow

```bash
# 1. Test trial mode (default)
docker run -e MYTHARA_LICENSE_MODE=trial mythara:v1.0.0

# 2. Generate test license key
python3 -c "from license_manager import generate_license_key; print(generate_license_key('ENT', 'Acme Corp', 'test@acme.com'))"

# 3. Test enterprise mode
docker run -e MYTHARA_LICENSE_KEY=MYTHARA-ENT-A7F3D-8K2P9-X4M1 mythara:v1.0.0

# 4. Verify license status
curl http://localhost:8000/v1/license/status
```

---

## Summary Checklist

- [ ] Create Stripe account and connect bank account
- [ ] Create Stripe Payment Link for $60,000 one-time payment
- [ ] Add `license_manager.py` with key generation/validation
- [ ] Add `/api/webhooks/stripe` endpoint to API
- [ ] Update container startup to validate `MYTHARA_LICENSE_KEY`
- [ ] Add trial expiration enforcement (HTTP 402 after 30 days)
- [ ] Configure email delivery (SendGrid/AWS SES) for license keys
- [ ] Update outreach emails with Stripe payment link
- [ ] Test end-to-end: payment → webhook → email → container activation

---

**Questions? Email Mythara.Engine@yahoo.com**
