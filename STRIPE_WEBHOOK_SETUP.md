# 🔗 Stripe Webhook Setup Guide
**Step-by-step instructions for connecting Stripe to your API**

---

## What is a Webhook?

A webhook is like a notification system. When someone pays $49 for your pilot:
1. They complete payment on Stripe
2. Stripe immediately sends a notification to your API
3. Your API generates an API key
4. Customer gets access

**Your webhook URL:** `https://heroic-flexibility-production.up.railway.app/api/webhooks/stripe`

---

## 📋 Setup Steps (5 minutes)

### Step 1: Open Stripe Dashboard

**Go to:** https://dashboard.stripe.com/test/webhooks

You should see a page titled "Webhooks" with a list (probably empty).

---

### Step 2: Add New Endpoint

1. **Click the blue "+ Add endpoint" button** (top right corner)

2. **You'll see a form with these fields:**

   **Endpoint URL:**
   ```
   https://heroic-flexibility-production.up.railway.app/api/webhooks/stripe
   ```
   *(Copy and paste this exactly)*

   **Description:** *(optional but helpful)*
   ```
   Mythara Pilot Purchase Handler
   ```

   **Listen to:** Select **"Events on your account"** (default, should be already selected)

   **API Version:** Keep default (latest)

---

### Step 3: Select Event Type

1. **Click "Select events" button**

2. **In the search box, type:** `checkout.session.completed`

3. **Check the box next to:** `checkout.session.completed`
   - This event fires when a customer completes payment
   - Your API needs this to know when to generate an API key

4. **Click "Add events" button** (bottom of modal)

---

### Step 4: Save the Endpoint

1. **Click "Add endpoint"** button at the bottom

2. **Stripe will create the endpoint and show you a new page**

---

### Step 5: Get Your Signing Secret

On the endpoint details page, you'll see:

**Signing secret**
- Status: `Signing secret for this endpoint`
- Button: `Click to reveal`

1. **Click "Click to reveal"**
   - It will show something like: `whsec_abc123def456ghi789jkl012mno345pqr678stu901vwx234`

2. **Copy this entire secret** (including `whsec_`)
   - This proves to your API that requests are really from Stripe
   - Without this, anyone could fake payment notifications

---

### Step 6: Add Secret to Railway

**Open your terminal and run:**

```bash
railway variables --set "STRIPE_WEBHOOK_SECRET=whsec_YOUR_SECRET_HERE"
```

**Replace `whsec_YOUR_SECRET_HERE` with the actual secret you copied.**

**Example:**
```bash
railway variables --set "STRIPE_WEBHOOK_SECRET=whsec_abc123def456ghi789jkl012mno345pqr678stu901vwx234"
```

This will:
- Update your Railway environment variable
- Automatically redeploy your API (takes ~1 minute)
- Your API will now verify webhook signatures

---

### Step 7: Disable Force Unlock (Production Mode)

While testing, force unlock lets anyone use the API. Turn it off:

```bash
railway variables --set "MYTHARA_PILOT_FORCE_UNLOCK=false"
```

Now only paying customers get access.

---

## ✅ Verify It Works

### Test the Webhook Endpoint

```bash
curl https://heroic-flexibility-production.up.railway.app/api/webhooks/stripe
```

**Expected response:**
```json
{
  "status": "error",
  "code": 403,
  "message": "Invalid signature"
}
```

This is GOOD! It means:
- ✅ Endpoint is reachable
- ✅ Security is working (rejects unsigned requests)
- ✅ Ready to receive real Stripe events

---

### Test Purchase Flow

1. **Open your payment link:**
   ```
   https://buy.stripe.com/28E9AU85SfFCa5MbucgjC01
   ```

2. **Use Stripe test card:**
   - Card: `4242 4242 4242 4242`
   - Expiry: `12/34` (any future date)
   - CVC: `123` (any 3 digits)
   - ZIP: `12345` (any ZIP)

3. **Complete payment**

4. **Check webhook logs in Stripe:**
   - Go back to: https://dashboard.stripe.com/test/webhooks
   - Click your endpoint
   - Click "Events" tab
   - You should see a `checkout.session.completed` event
   - Status should be `200` (success)

5. **Check API access:**
   ```bash
   curl https://heroic-flexibility-production.up.railway.app/v1/pilot/status
   ```
   
   Should return: `"access_granted": true`

---

## 🔍 Visual Reference

### What the Stripe Webhook Page Looks Like:

```
┌─────────────────────────────────────────────────────┐
│ Webhooks                    [+ Add endpoint]        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📋 Your endpoints                                  │
│                                                     │
│  [Empty list or existing endpoints]                │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### After clicking "+ Add endpoint":

```
┌─────────────────────────────────────────────────────┐
│ Add endpoint                                   [X]  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Endpoint URL *                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │ https://heroic-flexibility-production.up...   │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│  Description (optional)                             │
│  ┌───────────────────────────────────────────────┐ │
│  │ Mythara Pilot Purchase Handler                │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│  Listen to                                          │
│  ⦿ Events on your account                          │
│  ○ Events on Connected accounts                    │
│                                                     │
│  [Select events]                                   │
│                                                     │
│                            [Add endpoint]          │
└─────────────────────────────────────────────────────┘
```

### After clicking "Select events":

```
┌─────────────────────────────────────────────────────┐
│ Select events                              [X]      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Search events                                      │
│  ┌───────────────────────────────────────────────┐ │
│  │ checkout.session.completed          🔍        │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│  ☑ checkout.session.completed                      │
│    Occurs when a Checkout Session has been         │
│    successfully completed.                         │
│                                                     │
│                            [Add events]            │
└─────────────────────────────────────────────────────┘
```

### After saving - Endpoint Details Page:

```
┌─────────────────────────────────────────────────────┐
│ ← Webhooks                                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  https://heroic-flexibility-production.up...        │
│                                                     │
│  Status: ● Active                                   │
│                                                     │
│  Signing secret                                     │
│  Signing secret for this endpoint                   │
│  [Click to reveal]                                  │
│                                                     │
│  Events to send                                     │
│  checkout.session.completed                         │
│                                                     │
│  Tabs: [Details] [Events] [Settings]               │
└─────────────────────────────────────────────────────┘
```

---

## 🆘 Troubleshooting

### "I don't see the + Add endpoint button"
- Make sure you're logged into Stripe
- You might be in the wrong mode (live vs test)
- Click "Developers" in left sidebar → "Webhooks"

### "Endpoint returns 500 error"
- Check Railway logs: `railway logs`
- Verify STRIPE_WEBHOOK_SECRET is set correctly
- Make sure API is running (test /health endpoint)

### "Payment works but no API key generated"
- Check Stripe webhook logs (click endpoint → Events tab)
- Look for error messages in Railway logs
- Verify webhook secret is correct

### "How do I test without paying?"
- Use Stripe test mode (you're already in it)
- Test card `4242 4242 4242 4242` is free
- No real money is charged

---

## 📞 Quick Commands Reference

**Check if webhook endpoint is reachable:**
```bash
curl https://heroic-flexibility-production.up.railway.app/api/webhooks/stripe
```

**Update webhook secret:**
```bash
railway variables --set "STRIPE_WEBHOOK_SECRET=whsec_YOUR_SECRET"
```

**Disable test mode (production):**
```bash
railway variables --set "MYTHARA_PILOT_FORCE_UNLOCK=false"
```

**Check API status:**
```bash
curl https://heroic-flexibility-production.up.railway.app/v1/pilot/status
```

**View Railway logs:**
```bash
railway logs
```

---

## ✨ You're Done!

Once you complete these steps:
- ✅ Customers can purchase pilot for $49
- ✅ Stripe notifies your API instantly
- ✅ API generates unique API key
- ✅ Customer gets access automatically

**Total setup time:** 5 minutes
**Business result:** Automated sales system! 🚀

---

**Next:** Configure success page redirect in your Payment Link settings.
