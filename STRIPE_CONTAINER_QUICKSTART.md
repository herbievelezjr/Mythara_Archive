# Stripe + Container Wiring - Quickstart
**Copyright © 2025 Herbert Velez Jr. All rights reserved.**

## ✅ What You Have Working
- ✅ Local API running on port 8000
- ✅ Pilot paywall logic tested with force-unlock
- ✅ `/v1/pilot/status` confirmed working
- ✅ Stripe Payment Link created: https://buy.stripe.com/YOUR_LINK_HERE

## 🎯 What We Need to Do
1. **Deploy container to accessible URL** (3 options below)
2. **Wire Stripe webhook** to that URL
3. **Test real $49 purchase** to unlock pilot access

---

## Option 1: Quick Deploy with Railway (Recommended - 5 minutes)

### Why Railway?
- Free tier available
- Auto-generates public URL
- Built-in environment variable management
- No credit card required to start

### Steps:

1. **Sign up at [Railway.app](https://railway.app)** (GitHub login works)

2. **Create new project from GitHub:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your `Mythara_Archive` repo
   - Railway auto-detects Dockerfile

3. **Set environment variables in Railway dashboard:**
   ```bash
   MYTHARA_PILOT_PAYWALL=true
   MYTHARA_PILOT_PURCHASE_URL=https://buy.stripe.com/YOUR_LINK_HERE
   MYTHARA_PILOT_FORCE_UNLOCK=false
   STRIPE_WEBHOOK_SECRET=get_this_from_stripe_step_4
   PORT=8000
   ```

4. **Generate public domain:**
   - In Railway project → Settings → Generate Domain
   - Copy URL (e.g., `mythara-engine-production.up.railway.app`)

5. **Update Dockerfile CMD for API server:**
   - Railway needs the API to run, not validation suite
   - See Dockerfile fix below ⬇️

---

## Option 2: Cloudflare Tunnel (For Air-Gapped Demo)

If you want to keep running locally but expose publicly:

```bash
# Install cloudflared
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb

# Start your API locally
export MYTHARA_PILOT_PAYWALL=true
export MYTHARA_PILOT_FORCE_UNLOCK=false
export MYTHARA_PILOT_PURCHASE_URL="https://buy.stripe.com/YOUR_LINK"
export STRIPE_WEBHOOK_SECRET="whsec_xxx"
python core/source_proprietary/main.py

# In another terminal, create tunnel
cloudflared tunnel --url http://localhost:8000
```

This gives you a public URL like `https://xxx.trycloudflare.com` that routes to your local API.

---

## Option 3: Docker + Render.com (Production-Ready)

1. **Create account at [Render.com](https://render.com)**

2. **Create new Web Service:**
   - Select "Deploy an existing image from a registry" OR connect GitHub
   - If using GitHub: Point to `Mythara_Archive` repo
   - Render auto-detects Dockerfile

3. **Set environment variables:**
   ```bash
   MYTHARA_PILOT_PAYWALL=true
   MYTHARA_PILOT_PURCHASE_URL=https://buy.stripe.com/YOUR_LINK
   MYTHARA_PILOT_FORCE_UNLOCK=false
   STRIPE_WEBHOOK_SECRET=whsec_xxx
   PORT=8000
   ```

4. **Deploy** - Render builds and hosts your container
   - Free tier: `https://your-app.onrender.com`

---

## 🔧 Required Dockerfile Fix

**Problem:** Current Dockerfile runs `run_validation_suite.py`, not the API server.

**Fix:** Create production Dockerfile for API:

```dockerfile
# File: core/Dockerfile.api
FROM python:3.11.6-slim-bookworm

WORKDIR /app

# Install deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*

# Copy API requirements
COPY core/source_proprietary/requirements-api.txt .
RUN pip install --no-cache-dir --upgrade pip==23.3.1 && \
    pip install --no-cache-dir -r requirements-api.txt

# Copy only API code
COPY core/source_proprietary/ /app/core/source_proprietary/

# Environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Health check for API
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Run API server
EXPOSE 8000
CMD ["python", "core/source_proprietary/main.py"]
```

**Usage:**
```bash
docker build -f core/Dockerfile.api -t mythara-api:latest .
docker run -p 8000:8000 \
  -e MYTHARA_PILOT_PAYWALL=true \
  -e MYTHARA_PILOT_FORCE_UNLOCK=false \
  -e MYTHARA_PILOT_PURCHASE_URL="https://buy.stripe.com/YOUR_LINK" \
  -e STRIPE_WEBHOOK_SECRET="whsec_xxx" \
  mythara-api:latest
```

---

## 🔗 Stripe Webhook Setup (Do This After Deployment)

1. **Get your public URL** from Railway/Render/Cloudflare (e.g., `https://mythara.up.railway.app`)

2. **Go to Stripe Dashboard → Developers → Webhooks**

3. **Click "Add endpoint":**
   - **Endpoint URL:** `https://YOUR_PUBLIC_URL/api/webhooks/stripe`
   - **Events to send:** Select `checkout.session.completed`
   - Click "Add endpoint"

4. **Reveal signing secret:**
   - Click on the webhook you just created
   - Click "Reveal" next to "Signing secret"
   - Copy the `whsec_xxx` value

5. **Update environment variable:**
   - In Railway/Render dashboard, set `STRIPE_WEBHOOK_SECRET=whsec_xxx`
   - Restart service

---

## 🎫 Payment Link Metadata (Critical!)

**Current state:** Your Payment Link doesn't tell the webhook it's a "pilot" purchase.

**Fix in Stripe Dashboard:**

1. Go to **Products → Payment Links**
2. Find your $49 link, click the `⋯` menu → **Edit**
3. Scroll to **Metadata** section → **Add metadata**
   - Key: `license_type`
   - Value: `pilot`
4. **Save**

This ensures the webhook correctly grants pilot access (not enterprise).

---

## ✅ Test End-to-End

1. **Verify API is live:**
   ```bash
   curl https://YOUR_PUBLIC_URL/health
   curl https://YOUR_PUBLIC_URL/v1/pilot/status
   ```
   Should return `access_granted: false` (paywall active, no purchase yet)

2. **Complete $49 purchase:**
   - Open your Payment Link: `https://buy.stripe.com/YOUR_LINK`
   - Use Stripe test card: `4242 4242 4242 4242`
   - Expiry: Any future date (e.g., `12/34`)
   - CVC: Any 3 digits (e.g., `123`)

3. **Check webhook delivery:**
   - Stripe Dashboard → Developers → Webhooks → Your endpoint
   - Should show `checkout.session.completed` event with ✅ success

4. **Verify pilot access granted:**
   ```bash
   curl https://YOUR_PUBLIC_URL/v1/pilot/status
   ```
   Should now return `access_granted: true`

5. **Test a clause invocation:**
   ```bash
   curl -X POST https://YOUR_PUBLIC_URL/v1/clauses/invoke \
     -H "Content-Type: application/json" \
     -d '{
       "clause_id": "cl_test",
       "invocation_context": {"test": "pilot_access"}
     }'
   ```
   Should return invocation response (no 402 paywall error)

---

## 🚨 Common Issues

**Issue:** Webhook fails with "signature verification failed"
- **Fix:** Double-check `STRIPE_WEBHOOK_SECRET` matches Stripe Dashboard value
- **Fix:** Ensure no extra spaces/quotes when setting env var

**Issue:** Pilot access not granted after purchase
- **Fix:** Verify Payment Link has `metadata.license_type=pilot`
- **Fix:** Check webhook logs in Stripe Dashboard for errors

**Issue:** Container won't start
- **Fix:** Verify `core/source_proprietary/requirements-api.txt` exists
- **Fix:** Check Railway/Render logs for Python import errors

**Issue:** API returns 502 Bad Gateway
- **Fix:** Verify `PORT=8000` env var is set
- **Fix:** Check container logs for startup errors

---

## 📊 What's Next

After successful pilot wiring:
1. ✅ You can demo Mythara to prospects with real payment flow
2. ✅ Pilot buyers get 30-day access automatically
3. ✅ You can track purchases in Stripe Dashboard
4. ✅ Ready to add enterprise tier ($50k/year) when needed

---

## 🎯 My Recommendation

**Start with Railway** (Option 1):
- Takes 5 minutes
- Free tier sufficient for pilots
- Auto-SSL, auto-deploy on git push
- Easy env var management

Once you have Railway URL → Wire Stripe webhook → Test $49 purchase → Done!

---

**Need help?** Tell me which option you want to use and I'll walk you through it step-by-step.
