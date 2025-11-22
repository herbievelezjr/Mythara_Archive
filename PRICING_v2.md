# Mythara Engine Pricing Policy

**Copyright © 2025 Mythara Labs LLC. All rights reserved.**  
**Proprietary and Confidential.**

---

## Overview

Mythara uses a transparent tier structure with firm pricing and automatic inflation adjustment. This policy preserves sustainable R&D investment while maintaining predictable, transparent pricing for customers.

---

## Pricing Tiers (2025 Base Year)

| Tier | Annual Price | Monthly Invocations | Target Customer | Indemnification |
|------|--------------|---------------------|-----------------|-----------------|
| **Startup (Small Teams)** | $2,988 ($249/mo) | 5,000 | <50 employees | None |
| **Professional (Growing Teams)** | $11,988 ($999/mo) | 25,000 | 50-200 employees | None |
| **Growth License** | $120,000 | 100,000 | 200-1000 employees | $10M/$20M |
| **Enterprise** | $300,000 | Unlimited | >1000 employees | $25M/$50M |
| **Sovereign/Air-Gap** | $180,000+ | Custom | Government, defense | $50M/$100M |
| **Perpetual License** | $2,000,000 (one-time) | Unlimited | Strategic customers | $25M/$50M |

### Tier Inclusions

**All Tiers Include:**
- Mythara Engine API access
- Global Governance Framework (34 regulatory frameworks)
- Soul Cradle Enterprise Edition
- Cryptographic integrity artifacts
- Documentation and training materials
- Basic email support

**Growth+ Tiers Add:**
- Priority support (phone + email)
- SLA guarantees (99.5%-99.9% uptime)
- Insurance-backed indemnification
- Dedicated success manager (Enterprise+)
- On-premise deployment option (Sovereign)
- Source code escrow (Sovereign)

### Overage Pricing

**Invocation overages** (Enterprise/Sovereign tiers only):
- $0.50 per additional 1,000 invocations
- Rounded to nearest 10,000
- Billed monthly in arrears

---

## Inflation Adjustment Formula

Beginning from base year 2025, prices adjust annually using transparent compound formula:

```
price(year) = base_price × (1 + inflation_rate) ^ max(0, year - 2025)
```

**Parameters:**
- `base_price`: Tier price as of 2025 (see table above)
- `inflation_rate`: Configurable annual rate (default: 3% or 0.03)
- `base_year`: 2025
- Applied once per calendar year (no partial-year proration)

**Example: Growth Tier with 3% inflation**

| Year | Calculation | Annual Price |
|------|-------------|--------------|
| 2025 | $120,000 × (1.03^0) | $120,000 |
| 2026 | $120,000 × (1.03^1) | $123,600 |
| 2027 | $120,000 × (1.03^2) | $127,308 |
| 2028 | $120,000 × (1.03^3) | $131,127 |

**Customer Impact:**
- New contracts use current year's price
- Existing contracts locked at signing year price for full term
- Communicated 90 days in advance of effective date

---

## Firm Pricing Policy

### NO NEGOTIATED DISCOUNTS

Mythara enforces firm, non-discounted pricing. The free trial period is the only evaluation mechanism.

**All customers pay:**
- Published tier price
- Inflation-adjusted rate (if applicable)
- No percentage discounts
- No ad-hoc dollar reductions
- No "design partner" under-market pricing
- No retroactive credits beyond defined trial

**Rationale:**
1. Preserves integrity/security investment cadence
2. Ensures consistent treatment across all customers (regulated + non-regulated)
3. Avoids hidden pricing complexity
4. Aligns value with delivered trust guarantees

### ALLOWED FLEXIBILITY (Not Discounts)

**1. Automatic Renewal Credits (Extended Service Period)**

Loyal customers receive extended service periods (NOT price reductions):

| Renewal | Credit | Result |
|---------|--------|--------|
| **2nd year** | +2 months free | Pay for 12 months, receive 14 months service |
| **3rd year** | +3 months free | Pay for 12 months, receive 15 months service |
| **4th+ year** | +4 months free | Pay for 12 months, receive 16 months service |

**Legal distinction:** Customer pays full annual price, receives extended term. This is an operational credit, not a price discount.

**2. Multi-Year Prepayment (Price Lock)**

- Customer may prepay 2-3 years at current year's price
- Locks in pricing, avoids future inflation adjustments
- Payment received upfront (cash flow benefit to Mythara)
- NOT marketed as "discount" — marketed as "price protection"

**3. Pilot-to-Paid Upgrade Credit**

- Pilot customers ($49 one-time) who upgrade to Startup/Professional within 30 days receive credit
- Pilot fee applied to first month of paid tier
- Conversion incentive, not a discount policy

**4. Enterprise Size Multiplier (Pre-Set, Not Negotiated)**

Optional size-based adjustment applied BEFORE customer engagement:
- Small: 0.9× (companies <500 employees)
- Standard: 1.0× (companies 500-5000 employees)
- Large: 1.2× (companies >5000 employees)

**Applied transparently at tier selection, not negotiated post-engagement.**

### PROHIBITED PRACTICES

❌ Percentage discounts (10% off, 20% off)  
❌ Volume discounts  
❌ Competitive price matching  
❌ "Founder pricing" or "early adopter pricing"  
❌ Enterprise RFP-based price reductions  
❌ Post-contract credits or extensions (beyond renewal credits)  

---

## Refund Policy

### Pilot Tier

- **No refunds** after 7-day access period begins
- **Full refund** if pilot access fails to activate within 48 hours (technical failure only)
- **One pilot per business entity** (enforced via email domain verification)

### Annual Tiers (Startup, Professional, Growth, Enterprise)

- **30-day money-back guarantee** if service fails to meet documented SLA
- **No refunds** after 30-day acceptance period
- **SLA breach remedy:** Pro-rated credit for downtime per SLA terms (NOT refund)
- **Upgrade exchanges allowed:** Credit unused months toward higher tier
- **No downgrade exchanges:** Protects revenue, prevents gaming

### Sovereign/Air-Gap Tier

- **No refunds** after deployment begins
- **SLA breach remedy:** Service credits only
- **Contract disputes:** Resolved per arbitration agreement

### Perpetual License

- **No refunds under any circumstances** (disclosed at purchase)
- **Buyer assumes all risk**
- **Suitable for:** M&A exits, strategic partnerships only

**Legal Compliance:**
- **FTC Mail/Telephone Order Rule:** 30-day acceptance period satisfies reasonable cancellation window
- **California Consumer Protection:** 30-day SLA-based refund option provides recourse (not "all sales final")
- **Stripe/Payment Processor TOS:** Refund policy disclosed at checkout

---

## Trial Conversion Rules

### Pilot Tier (7-Day Evaluation)

- **Price:** $49 one-time fee
- **Duration:** 7 days
- **Access:** Rate-limited API (1,000 calls total)
- **Support:** Email only, best-effort
- **Upgrade:** 100% pilot fee credit if upgraded within 30 days

### Trial Expiration

At trial expiry, customer must either:
1. **Upgrade** to paid tier at full current computed price
2. **Accept suspension** - API access disabled, HTTP 402 responses

**No grace period** beyond 5 business days (administrative window only).

---

## Sovereign/Air-Gap Pricing Justification

Higher price accounts for:
- Isolated infrastructure and audit trail hardening
- Specialized incident response SLAs
- Additional artifact attestation (extended forensic chain)
- On-premise deployment complexity
- Source code escrow administration
- Government/defense compliance overhead

---

## Annual Review Process

### Recommended Steps

1. **Cost Analysis:** Gather prior year support + integrity maintenance cost deltas
2. **Economic Index:** Pull published CPI or internal inflation index
3. **Scenario Modeling:** Simulate new price under 2%, 3%, 5% inflation scenarios
4. **Rate Decision:** Select target inflation rate for coming year
5. **Configuration:** Set `MYTHARA_INFLATION_RATE_ANNUAL` environment variable
6. **Customer Communication:** Announce 90 days before effective date with value justification

### Value Communication Template

```
Subject: 2026 Pricing Update - Mythara Engine

Dear Customer,

As part of our transparent pricing policy, we're announcing the 2026 pricing adjustment.

2026 Inflation Rate: 3.0%
Your Current Tier: Enterprise ($300,000/year)
2026 Price (new contracts): $309,000/year

Your Contract: UNAFFECTED - your current rate remains locked through [expiration date]

Why This Adjustment:
- Continued SSIP metric expansion
- Integrity hash lineage improvements
- Automated Clause Manifest delta attestations
- 24/7 support capacity growth

Questions? Contact your success manager.

Mythara Labs LLC
```

---

## Environment Variables (Deployment Configuration)

| Variable | Purpose | Default | Type |
|----------|---------|---------|------|
| `MYTHARA_ENTERPRISE_PRICE_USD` | Base enterprise price (fallback if inflation vars absent) | `300000` | Integer |
| `MYTHARA_PRICE_BASE_YEAR` | Year used as starting point for compounding | `2025` | Integer |
| `MYTHARA_INFLATION_RATE_ANNUAL` | Annual inflation rate (decimal) | unset | Float (e.g., 0.03) |
| `MYTHARA_PURCHASE_URL` | Upgrade / purchase landing page | `https://mythara.ai/enterprise` | URL |
| `MYTHARA_SOVEREIGN_PRICE_USD` | Reference sovereign price | `180000` | Integer |
| `MYTHARA_PRICE_MULTIPLIER` | Optional size-based multiplier | unset | Float (0.9, 1.0, 1.2) |

### Runtime Behavior

- Trial endpoint responses and expired trial (HTTP 402) payloads include *current* computed price
- Price headers: `X-Mythara-Enterprise-Price-USD` show inflation-adjusted value during trial
- Enterprise/Sovereign keys bypass trial and pricing prompts

---

## FAQ (External-Facing)

**Q: Why does the price increase annually?**  
To preserve the integrity/security roadmap and offset rising operational costs while keeping predictable, low, transparent adjustments.

**Q: Can we opt out of inflation increases?**  
No. We publish methodology; signed contracts lock your price for the full term, but renewals use prevailing market rate.

**Q: Does inflation adjustment affect our existing contract?**  
No—only recalculated at renewal; active contract term remains at signing price.

**Q: Can we pay usage-only instead of annual subscription?**  
No. Core integrity and SSIP features are bundled to maintain verified trust guarantees.

**Q: Do you offer discounts?**  
No. Pilot access ($49 for 7 days) is the evaluation mechanism; production pricing is firm. We offer renewal credits (extended service periods) for loyal customers.

**Q: What about volume discounts for large deployments?**  
No volume discounts. Enterprise tier includes unlimited invocations. If your organization needs multiple isolated deployments, contact us for multi-entity licensing (separate contracts per entity at standard rates).

**Q: Can we negotiate pricing?**  
No. Pricing is transparent and firm. The only flexibility is tier selection (choose tier that matches your company size and usage).

---

## Change Log

| Date | Change | Reason |
|------|--------|--------|
| 2025-11-18 | Updated entity from Herbert Velez Jr. to Mythara Labs LLC | LLC formation |
| 2025-11-18 | Replaced "discounts" with "renewal credits" (extended term) | Legal compliance (firm pricing policy) |
| 2025-11-18 | Added 30-day refund window for SLA breach | Consumer protection compliance |
| 2025-11-18 | Added insurance-backed indemnification details | Risk management transparency |
| 2025-11-18 | Added tier structure ($2,988-$2M range) | Product-market fit alignment |

---

**For internal use only. Do not distribute externally without removing confidential implementation details.**

---

**Last Updated:** November 18, 2025  
**Document Version:** 2.0  
**Owner:** Herbert Velez Jr., Managing Member, Mythara Labs LLC
