# Stripe Product Catalog Integration

**Copyright © 2025 Herbert Velez Jr. All rights reserved.**

## Product Mapping

Your Stripe product catalog is now integrated with the Mythara Engine pricing API. Here's how the tiers map:

| Internal Tier | Stripe Product Name | Price | Target Customers |
|--------------|---------------------|-------|------------------|
| `foundation` | **Startup** | $25,000/year | 1-50 employees |
| `professional` | **Small Business** | $40,000/year | 51-200 employees |
| `corporate` | **Mid-Market** | $75,000/year | 201-1,000 employees |
| `enterprise` | **Enterprise** | $150,000/year | 1,001-5,000 employees |
| `sovereign` | **Global** | $300,000/year | 5,000+ employees |
| `pilot` | **Mythara Engine Pilot** | $49 one-time | Trial access |

## Next Steps: Create Payment Links

For each Stripe product, you need to create a **Payment Link** and configure it in Railway:

### 1. Create Payment Links in Stripe Dashboard

For each product (Startup, Small Business, Mid-Market, Enterprise, Global):

1. Go to Stripe Dashboard → **Products**
2. Click on the product (e.g., "Startup")
3. Click **Create payment link** button
4. Configure:
   - **Quantity**: Fixed (1)
   - **Success URL**: `https://heroic-flexibility-production.up.railway.app/api/webhooks/stripe/success`
   - **Metadata** (IMPORTANT):
     - `license_type`: `enterprise`
     - `tier`: `foundation` (or `professional`, `corporate`, `enterprise`, `sovereign`)
5. Copy the payment link URL (e.g., `https://buy.stripe.com/test_xxxxx`)

### 2. Configure Payment Links in Railway

Set these environment variables in Railway:

```bash
# Foundation tier ($25K)
STRIPE_LINK_FOUNDATION=https://buy.stripe.com/test_xxxxx

# Professional tier ($40K)
STRIPE_LINK_PROFESSIONAL=https://buy.stripe.com/test_xxxxx

# Corporate tier ($75K)
STRIPE_LINK_CORPORATE=https://buy.stripe.com/test_xxxxx

# Enterprise tier ($150K)
STRIPE_LINK_ENTERPRISE=https://buy.stripe.com/test_xxxxx

# Sovereign tier ($300K)
STRIPE_LINK_SOVEREIGN=https://buy.stripe.com/test_xxxxx
```

You can set these in Railway with:
```bash
railway variables set STRIPE_LINK_FOUNDATION="https://buy.stripe.com/test_xxxxx"
railway variables set STRIPE_LINK_PROFESSIONAL="https://buy.stripe.com/test_xxxxx"
# ... etc
```

### 3. Update Webhook Handler

The webhook at `/api/webhooks/stripe` will need to:
1. Read the `license_type` metadata (pilot or enterprise)
2. Read the `tier` metadata (foundation, professional, etc.)
3. Generate appropriate license key:
   - Pilot: `sk_pilot_[random]`
   - Enterprise: `sk_ent_[tier]_[random]` (e.g., `sk_ent_foundation_abc123`)
4. Send appropriate email (pilot welcome vs enterprise onboarding)

## API Response Example

Once configured, the `/v1/pricing/enterprise` endpoint will return:

```json
{
  "tier": "foundation",
  "name": "Foundation",
  "display_name": "Mythara Foundation",
  "stripe_product_name": "Startup",
  "tagline": "Perfect for early-stage startups and SMBs",
  "description": "Essential SSIP orchestration...",
  "base_price": 25000,
  "final_price": 25000,
  "currency": "USD",
  "billing_period": "annual",
  "employee_range": [1, 50],
  "features": [...],
  "ideal_for": "Startups, mental health apps...",
  "payment_link": "https://buy.stripe.com/test_xxxxx"
}
```

## Testing Checklist

- [ ] Create 5 payment links in Stripe (one per enterprise tier)
- [ ] Add metadata to each link: `license_type=enterprise`, `tier=foundation/professional/etc`
- [ ] Configure 5 environment variables in Railway
- [ ] Test pricing API: `curl https://heroic-flexibility-production.up.railway.app/v1/pricing/enterprise?tier=foundation`
- [ ] Verify `payment_link` appears in API response
- [ ] Update webhook handler to process enterprise purchases
- [ ] Test enterprise purchase flow end-to-end
- [ ] Create success/confirmation page for enterprise customers

## Current Status

✅ Stripe products created (6 total: 1 pilot + 5 enterprise tiers)
✅ Code updated to map internal tiers to Stripe product names
✅ API response includes `stripe_product_name` field
✅ Infrastructure ready for payment link integration
⏳ Pending: Create payment links in Stripe
⏳ Pending: Configure Railway environment variables
⏳ Pending: Enhance webhook handler for enterprise licenses
