# Mythara Engine - Pilot to Purchase Conversion Template

**Copyright © 2025 Herbert Velez Jr. All rights reserved.**  
**Proprietary and Confidential.**

---

## Email Template: Initial Pilot Package with Pricing

### Subject Options
1. `Mythara Engine pilot + Enterprise pricing`
2. `30-day free pilot (container-only, air-gapped ready)`
3. `Quick question re CIO-SP3 compliance validation`

### Body Template (< 100 words)

```
Hi [Name],

Attaching our 30-day free pilot for Mythara Engine (container-only, air-gapped deployment supported).

**After pilot validation:**
→ Enterprise Edition: $60,000/year* (ACH/wire/credit card)
→ Purchase: [STRIPE_PAYMENT_LINK]
→ License key delivered instantly via email

*Pricing increases 3% annually to match inflation. Lock in 2025 rate before Dec 31.

Pilot spins up in 30 minutes. 15-min walkthrough available this week?

Best,
Herbert Velez Jr.
Mythara Labs LLC
Mythara.Engine@yahoo.com
```

---

## Follow-Up Template: Day 3 (If No Response)

### Subject
`Re: Mythara Engine pilot + Enterprise pricing`

### Body (≤ 45 words)

```
Hi [Name] — quick nudge.

Mythara produces deterministic NIST SP 800-53 evidence + PGP-signed manifests (Task Area 7 focus). Takes 30 minutes to provision.

Worth a 15-min look? Can show the artifact chain and pricing structure.

Best, Herbert
```

---

## Follow-Up Template: Day 7 (Final Touch)

### Subject
`Re: Mythara Engine pilot + Enterprise pricing`

### Body (≤ 60 words)

```
Looping back in case this is useful for near-term [CIO-SP3/FISMA/DoD] compliance work.

If compliance automation isn't a fit for you, happy to get routed to the right team (InfoSec, Risk, Audit).

I can also share a one-pager and sample signed evidence manifest.

Best,
Herbert Velez Jr.
Mythara Labs LLC
```

---

## In-Trial Upgrade Prompt (Container Startup)

When customer runs the pilot container, they see:

```
============================================================
⏰ MYTHARA ENGINE - TRIAL MODE
   Days remaining: 27
   Expires: 2025-12-11T00:00:00Z
   Upgrade: https://buy.stripe.com/[your-link]
   Price: $60,000 USD/year
============================================================
```

---

## After Trial Expiration (HTTP 402 Response)

API returns:

```json
{
  "error": "Trial expired",
  "message": "Your 30-day trial has ended. Upgrade to Enterprise Edition to continue using Mythara Engine.",
  "purchase_url": "https://buy.stripe.com/[your-link]",
  "price_usd_year": 60000,
  "contact": "Mythara.Engine@yahoo.com"
}
```

---

## Post-Purchase Email (Automated)

**Subject:** `Your Mythara Enterprise License Key`

```
Hi [Company] team,

Thank you for purchasing Mythara Engine Enterprise Edition ($60,000 USD).

Your license key:
MYTHARA-ENT-A7F3D-8K2P9-X4M1

**Activation Instructions:**
1. Set environment variable: MYTHARA_LICENSE_KEY=MYTHARA-ENT-A7F3D-8K2P9-X4M1
2. Restart your Mythara container
3. Verify with: curl http://localhost:8000/v1/license/status

The pilot restrictions have been removed. You now have full Enterprise access with:
- Unlimited API calls
- Production support
- Access to all SSIP audit protocols
- Air-gapped deployment

**Support:**
- Email: Mythara.Engine@yahoo.com
- Docs: https://mytharalabs.com/docs
- Response time: <4 business hours

Need help with deployment? Reply to this email or schedule a call at [calendly-link].

Best regards,
Herbert Velez Jr.
Mythara Labs LLC
```

---

## Stripe Payment Link Setup Checklist

- [ ] Create Stripe account at https://stripe.com
- [ ] Connect business bank account (Settings → Bank accounts)
- [ ] Verify bank account via micro-deposits (1-2 days)
- [ ] Create Payment Link:
  - Product: Mythara Engine Enterprise Edition
  - Amount: $60,000 USD (one-time)
  - Collect: Name, Email, Company Name
  - After payment: Redirect to success page
  - Metadata field: `company_name` (for license generation)
- [ ] Configure webhook endpoint: `https://api.mytharalabs.com/api/webhooks/stripe`
- [ ] Test payment with $1.00 test charge
- [ ] Update `PURCHASE_URL` env var in container: `MYTHARA_PURCHASE_URL=https://buy.stripe.com/...`
- [ ] Update email templates with real payment link

---

## Key Messaging Points

1. **Urgency:** "Pricing increases 3% annually - lock in 2025 rate"
2. **Risk mitigation:** "30-day free pilot, no credit card required"
3. **Fast activation:** "License delivered instantly via email"
4. **Easy deployment:** "30-minute container spin-up"
5. **Compliance positioning:** "Task Area 7 / NIST SP 800-53 / Air-gapped ready"
6. **Direct payment:** "ACH direct deposit to business account (2-day settlement)"

---

## Objection Handling

**"We need approval from procurement."**
→ "Understood. I can provide a quote + invoice for your procurement process. The pilot can validate technical fit while approvals run in parallel."

**"Can we negotiate on price?"**
→ "The $60K/year rate is firm. It's priced at cost plus minimal margin for early adopters. Pricing automatically increases 3% annually to match inflation, so purchasing now locks in the lowest rate."

**"We need to test for 90 days."**
→ "The 30-day pilot provides full functionality for validation. If you need more time to complete internal reviews after technical validation, we can extend on a case-by-case basis."

**"Can we pay monthly?"**
→ "Annual billing only for Enterprise Edition. This keeps our operational costs low and passes savings to customers. Payment via ACH, wire, or credit card accepted."

---

**Next Steps:**
1. Set up Stripe account and payment link
2. Update `PURCHASE_URL` in `.env` and outreach templates
3. Test payment flow end-to-end
4. Send pilot packages with clear upgrade path

