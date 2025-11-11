# Mythara Engine Pricing & Inflation Policy
# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

## Overview
Mythara uses a transparent tier structure with an annual Enterprise anchor price that can adjust over time based on inflation. The goal: preserve sustainable R&D and integrity assurance investment without sudden pricing shocks.

## Tiers (Indicative)
| Tier | Annual (Base Year 2025) | Included | Notes |
|------|-------------------------|----------|-------|
| Pilot (30–90 days) | $15K–$20K (pro‑rated) | Limited invocations, onboarding | 100% credit if upgraded within 30 days post‑pilot |
| Growth | $35K–$40K | Invocation cap, standard support | For scaling teams proving value |
| Enterprise | $60K | 100K monthly invocations pooled, integrity artifacts, priority fixes | Anchor tier; inflation-adjusted annually |
| Sovereign / Air‑Gap | $150K–$180K | On‑prem / isolated deployment, audit role | Can exceed $180K if bespoke controls |
| Premium Support Add‑On | +$20K–$24K | 24/7 escalation, enhanced SLA | Separate from core license |

Invocation overages (Enterprise/Sovereign): $0.50 per additional 1K invocations (rounded to nearest 10K).

## Inflation Adjustment Logic
Beginning from the base price year (default 2025), the Enterprise price can automatically apply a compound annual adjustment:

```
enterprise_price(year) = base_price * (1 + inflation_rate) ^ max(0, year - base_year)
```
- `base_price` (2025): 60000 USD
- `inflation_rate`: Configurable (example 0.03 for 3%)
- `base_year`: 2025 by default
- Applied once per calendar year difference (no partial year proration).

This ensures predictable, steady increases rather than reactive jumps.

## Environment Variables
| Variable | Purpose | Default |
|----------|---------|---------|
| `MYTHARA_ENTERPRISE_PRICE_USD` | Base enterprise anchor (used if inflation vars absent) | `60000` |
| `MYTHARA_PRICE_BASE_YEAR` | Year used as starting point for compounding | `2025` |
| `MYTHARA_INFLATION_RATE_ANNUAL` | Annual inflation rate (decimal) | unset (no adjustment) |
| `MYTHARA_PURCHASE_URL` | Upgrade / purchase landing page | `https://mythara.ai/enterprise` |
| `MYTHARA_SOVEREIGN_PRICE_USD` | Reference sovereign price | `180000` |
| `MYTHARA_PRICE_MULTIPLIER` | Optional multiplier for company size segment (e.g., 0.9 small, 1.0 mid, 1.3 large) | unset (no change) |

## Runtime Behavior
- Trial endpoint responses and expired trial (HTTP 402) payloads include the *current* computed Enterprise price.
- Price headers: `X-Mythara-Enterprise-Price-USD` show the inflation-adjusted value during trial responses.
- Enterprise/Sovereign keys bypass trial and pricing prompts.

## Example Computation
Inflation rate: 3% (0.03); Size multiplier (large): 1.2

| Year | Calculation | Result |
|------|-------------|--------|
| 2025 | 60000 * (1.03^0) * 1.2 | 72000 |
| 2026 | 60000 * (1.03^1) * 1.2 | 74160 |
| 2027 | 60000 * (1.03^2) * 1.2 | 76385 |
| 2028 | 60000 * (1.03^3) * 1.2 | 78675 |

(Rounded to nearest whole dollar.)

## Change Management
1. Update `MYTHARA_INFLATION_RATE_ANNUAL` at start of year (e.g., based on CPI or internal policy).
2. Optionally reset `MYTHARA_ENTERPRISE_PRICE_USD` if re-basing.
3. Communicate new computed price 30 days before effective date.
4. For existing contracts: honor previous year’s price until renewal.

## Firm Pricing Policy
Mythara enforces non-discounted, firm pricing. The free trial period (time-limited license) is the only concession. All customers pay the computed price (base × inflation × optional size multiplier) upon conversion. No percentage discounts, credits, or negotiation floors are offered.

Rationale:
1. Preserves integrity/security investment cadence.
2. Ensures consistent treatment across regulated and non-regulated clients.
3. Avoids hidden pricing complexity and internal exceptions.
4. Aligns value with delivered trust guarantees (integrity artifacts, SSIP metrics).

Allowed flexibility (non-discount, within policy):
- Size multiplier (ENV `MYTHARA_PRICE_MULTIPLIER`) selected pre-offer, not negotiated post hoc.
- Multi-year prepayment: same annual price, optional operational prioritization (not a discount).
- Sovereign / Air-Gap tier: priced separately; still firm once quoted.

Not permitted:
- Percentage or ad-hoc dollar reductions.
- “Design partner” under-market pricing.
- Retroactive credits or free extensions beyond the defined trial.

Trial Conversion Rule:
- At trial expiry, customer either upgrades at full current computed price or access is suspended (HTTP 402 responses). No grace period beyond a short administrative window (≤5 business days).

## Sovereign / Air‑Gap Justification
Higher price accounts for:
- Isolated infrastructure & audit trail hardening
- Potential SLAs requiring specialized incident response
- Additional artifact attestation (extended forensic chain)

## Roadmap Alignment
Inflation-linked pricing helps fund:
- Continued SSIP metric expansion
- Integrity hash lineage improvements
- Automated Clause Manifest delta attestations

## Recommended Annual Review Process
1. Gather prior year support + integrity maintenance cost deltas.
2. Pull published CPI or internal index.
3. Simulate new price under multiple inflation scenarios (e.g., 2%, 3%, 5%).
4. Decide target rate; set `MYTHARA_INFLATION_RATE_ANNUAL`.
5. Announce to customers with justification (value delivered + roadmap preview).

## FAQ (External Facing)
**Q: Why does the price increase annually?**  
To preserve the integrity/security roadmap and offset rising operational costs while keeping predictable, low, transparent adjustments.

**Q: Can we opt out of inflation increases?**  
No. We publish methodology; signed multi-year agreements use the prevailing price at renewal start.

**Q: Does inflation adjustment affect our existing term?**  
No—only recalculated at renewal; active term remains fixed.

**Q: Can we pay usage-only?**  
No. Core integrity and SSIP features are bundled to maintain verified trust guarantees.

**Q: Do you offer discounts?**  
No. Trial access is the evaluation mechanism; production pricing is firm.

---
*For internal use: Do not distribute externally without removing confidential notes.*
