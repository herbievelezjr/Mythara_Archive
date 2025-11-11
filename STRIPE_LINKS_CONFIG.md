# Stripe Payment Links - Configuration Checklist
**Copyright © 2025 Herbert Velez Jr. All rights reserved.**

## Your Stripe Links

### ✅ Pilot Access ($49)
**URL:** https://buy.stripe.com/28E9AU85SfFCa5MbucgjC01

**Usage:** Send this link to prospects for 30-day pilot access

**Status:** 
- [ ] Metadata added (license_type=pilot)
- [ ] Success redirect URL configured
- [ ] Test purchase completed

---

### ✅ Enterprise License ($60,000/year)
**URL:** https://buy.stripe.com/dRm28s5XKbpm2Dk41KgjC00

**Usage:** Enterprise annual license for unlimited use

**Status:**
- [ ] Metadata added (license_type=enterprise)
- [ ] Success redirect URL configured
- [ ] Webhook handles enterprise purchases

---

## Configuration Steps (Do These Now)

### Step 1: Add Metadata to Pilot Link

1. **Go to:** Stripe Dashboard → Products → Payment Links
2. **Find:** $49 link → Click ⋯ menu → Edit
3. **Scroll to:** Metadata section
4. **Add metadata:**
   - Key: `license_type`
   - Value: `pilot`
5. **Click:** Save

**Why:** This tells your webhook it's a pilot purchase (not enterprise)

---

### Step 2: Add Metadata to Enterprise Link

1. **Go to:** Stripe Dashboard → Products → Payment Links
2. **Find:** $60,000 link → Click ⋯ menu → Edit
3. **Scroll to:** Metadata section
4. **Add metadata:**
   - Key: `license_type`
   - Value: `enterprise`
5. **Click:** Save

**Why:** This tells your webhook to generate full enterprise license key

---

### Step 3: Configure Success Redirect (After You Deploy)

**Do this AFTER deploying to Railway/Render and hosting success page**

#### For Pilot Link:
1. **Edit pilot link** in Stripe Dashboard
2. **After payment → Redirect customers to this URL:**
   ```
   https://herbievelezjr.github.io/Mythara_Archive/?session_id={CHECKOUT_SESSION_ID}
   ```
3. **Save**

#### For Enterprise Link:
1. **Edit enterprise link** in Stripe Dashboard
2. **After payment → Show success message:**
   ```
   Thank you for purchasing Mythara Engine Enterprise!
   
   Your license key and setup instructions have been sent to your email.
   
   Questions? Email: Mythara.Engine@yahoo.com
   ```
3. **Save**

**Why:** Pilot customers get instant download page, Enterprise get white-glove onboarding

---

## Test Checklist

### Pilot Link Test
```bash
# 1. Open pilot link
open https://buy.stripe.com/28E9AU85SfFCa5MbucgjC01

# 2. Use test card
# Card: 4242 4242 4242 4242
# Expiry: 12/34
# CVC: 123
# Email: test@yourcompany.com

# 3. After payment, verify:
# - Redirected to success page ✓
# - Download link works ✓
# - API endpoint shown ✓
# - Webhook triggered (check Stripe Dashboard → Events) ✓

# 4. Check API
curl https://your-api.up.railway.app/v1/pilot/status
# Should return: access_granted: true

# 5. Check webhook generated API key
# Stripe Dashboard → Events → checkout.session.completed → View logs
# Should see: api_key: sk_pilot_xxx in response
```

### Enterprise Link Test
```bash
# 1. Open enterprise link
open https://buy.stripe.com/dRm28s5XKbpm2Dk41KgjC00

# 2. Use test card (same as above)

# 3. After payment, verify:
# - Success message shown ✓
# - Webhook triggered ✓
# - License key generated (check webhook logs) ✓
# - Email sent with license key ✓
```

---

## Quick Reference

### Environment Variables Needed
```bash
# For pilot paywall
MYTHARA_PILOT_PAYWALL=true
MYTHARA_PILOT_PURCHASE_URL=https://buy.stripe.com/28E9AU85SfFCa5MbucgjC01
MYTHARA_PILOT_FORCE_UNLOCK=false  # true for testing, false for production

# For Stripe webhook
STRIPE_WEBHOOK_SECRET=whsec_xxx  # Get from Stripe after creating webhook

# API config
PORT=8000
```

### Webhook Endpoint
```
POST https://your-api.up.railway.app/api/webhooks/stripe
```

**Events to select in Stripe:**
- ✅ `checkout.session.completed`

---

## Email Templates to Use

### In Outreach Emails
```markdown
**Try Mythara Engine Pilot (30 days, $49):**
https://buy.stripe.com/28E9AU85SfFCa5MbucgjC01

Setup takes 30 minutes. You'll get instant API access + Docker package.
```

### In LinkedIn Messages
```markdown
Quick pilot available: https://buy.stripe.com/28E9AU85SfFCa5MbucgjC01

$49 for 30 days, includes compliance validation examples.
```

### In Proposal Documents
```markdown
## Pricing

### Pilot Access (30 days)
- **Price:** $49 one-time
- **What's included:** Full API access, Docker package, documentation
- **Purchase:** https://buy.stripe.com/28E9AU85SfFCa5MbucgjC01

### Enterprise License (Annual)
- **Price:** $60,000/year
- **What's included:** Unlimited API access, source code escrow, SLA
- **Purchase:** https://buy.stripe.com/dRm28s5XKbpm2Dk41KgjC00
- **Contact:** Mythara.Engine@yahoo.com for volume/multi-year discounts
```

---

## Tracking Metrics

### Stripe Dashboard Metrics to Watch
1. **Conversion rate:** Link views → Purchases
2. **Revenue:** Total from pilot vs enterprise
3. **Abandoned checkouts:** Where people drop off
4. **Average time to purchase:** How fast they decide

### Your API Metrics to Track
1. **Pilot activations:** Count in webhook logs
2. **API usage:** Calls per pilot customer
3. **Most used endpoints:** What they test first
4. **Support tickets:** Common issues

---

## When Someone Purchases

### Pilot Purchase Flow:
1. ✅ Stripe charges $49
2. ✅ Webhook generates API key
3. ✅ Customer redirected to success page
4. ✅ Customer downloads pilot package
5. ✅ Receipt email with API key sent
6. ✅ Customer working in < 5 minutes

### Enterprise Purchase Flow:
1. ✅ Stripe charges $60,000
2. ✅ Webhook generates enterprise license key
3. ✅ License email sent automatically
4. ✅ You get notification (set up webhook notification)
5. ✅ Schedule onboarding call
6. ✅ Provide white-glove setup support

---

## Next Actions

**Right now (5 minutes):**
1. [ ] Add metadata to both Stripe links
2. [ ] Save this file for reference

**After deploying API (30 minutes):**
1. [ ] Create Stripe webhook endpoint
2. [ ] Update pilot link with success redirect URL
3. [ ] Test pilot purchase flow
4. [ ] Test enterprise purchase flow

**Before first real purchase:**
1. [ ] Switch Stripe to Live mode
2. [ ] Update links to live versions
3. [ ] Test with $0.50 to verify everything works
4. [ ] Update outreach emails with live pilot link

---

**Ready to configure Stripe?** Open Stripe Dashboard and follow Step 1 above!
