# 🏢 Enterprise Pricing Tiers - Mythara Engine

**Copyright © 2025 Herbert Velez Jr. All rights reserved.**

---

## 📊 Tiered Pricing Based on Company Size

Your enterprise pricing now automatically scales based on company size:

### Pricing Tiers:

| Tier | Company Size | Base Price | Multiplier |
|------|-------------|------------|------------|
| **Startup** | 1-50 employees | $25,000/year | 1.0x |
| **Small Business** | 51-200 employees | $40,000/year | 1.6x |
| **Mid-Market** | 201-1,000 employees | $75,000/year | 3.0x |
| **Enterprise** | 1,001-5,000 employees | $150,000/year | 6.0x |
| **Global Enterprise** | 5,000+ employees | $300,000/year | 12.0x |

---

## 🔍 How It Works:

### 1. API Endpoint for Pricing

Customers can query pricing based on their company size:

```bash
# Get all tiers
curl https://heroic-flexibility-production.up.railway.app/v1/pricing/enterprise

# Get pricing for specific employee count
curl "https://heroic-flexibility-production.up.railway.app/v1/pricing/enterprise?employees=250"

# Get specific tier pricing
curl "https://heroic-flexibility-production.up.railway.app/v1/pricing/enterprise?tier=enterprise"
```

### 2. Example Response:

```json
{
  "tiers": {
    "startup": {
      "tier": "startup",
      "tier_name": "Startup (1-50 employees)",
      "base_price": 25000,
      "final_price": 25000,
      "employee_range": [1, 50],
      "multiplier": 1.0
    },
    "small": {
      "tier": "small",
      "tier_name": "Small Business (51-200 employees)",
      "base_price": 40000,
      "final_price": 40000,
      "employee_range": [51, 200],
      "multiplier": 1.6
    },
    // ... more tiers
  },
  "currency": "USD",
  "billing": "one-time annual license",
  "note": "Custom pricing available for unique requirements"
}
```

---

## 💳 Creating Stripe Payment Links:

### For Each Tier, Create a Separate Payment Link:

**1. Startup Tier ($25k):**
```
Product: Mythara Engine Enterprise - Startup
Price: $25,000 USD
Metadata: license_type=enterprise, tier=startup
```

**2. Small Business ($40k):**
```
Product: Mythara Engine Enterprise - Small Business
Price: $40,000 USD
Metadata: license_type=enterprise, tier=small
```

**3. Mid-Market ($75k):**
```
Product: Mythara Engine Enterprise - Mid-Market
Price: $75,000 USD
Metadata: license_type=enterprise, tier=mid
```

**4. Enterprise ($150k):**
```
Product: Mythara Engine Enterprise
Price: $150,000 USD
Metadata: license_type=enterprise, tier=enterprise
```

**5. Global Enterprise ($300k):**
```
Product: Mythara Engine Enterprise - Global
Price: $300,000 USD
Metadata: license_type=enterprise, tier=global
```

---

## 📧 Sales Process:

### Option A: Self-Service (Startups/Small Business)
1. Customer checks pricing via API endpoint
2. Customer clicks appropriate payment link
3. Automated license delivery via webhook

### Option B: Sales Call (Mid-Market+)
1. Customer inquires at Mythara.Engine@yahoo.com
2. Sales call to understand needs
3. Confirm employee count
4. Send appropriate payment link
5. Automated license delivery

---

## 🔧 Configuration:

### Adjust Tiers in Code:

Edit `core/source_proprietary/main.py`:

```python
ENTERPRISE_TIERS = {
    "startup": {
        "name": "Startup (1-50 employees)",
        "base_price": 25000,  # <-- Change here
        "employee_range": (1, 50),
        "multiplier": 1.0
    },
    # ... more tiers
}
```

### Enable Inflation Adjustment:

Set environment variable:

```bash
# 3% annual price increase
railway variables --set "MYTHARA_INFLATION_RATE_ANNUAL=0.03"

# Base year for inflation calculation
railway variables --set "MYTHARA_PRICE_BASE_YEAR=2025"
```

**Example:** In 2026, prices automatically increase by 3%:
- Startup: $25,000 → $25,750
- Enterprise: $150,000 → $154,500

---

## 📈 Why Tiered Pricing?

### Benefits:

1. **Fair Pricing** - Small companies pay less, large companies pay more
2. **Easier Sales** - Clear pricing reduces friction
3. **Revenue Optimization** - Capture value from all company sizes
4. **Market Positioning** - Shows you serve everyone from startups to Fortune 500

### Industry Standard:

Most B2B SaaS uses tiered pricing:
- Salesforce
- HubSpot
- Datadog
- Snowflake

---

## 🎯 Marketing Your Tiers:

### On Your Website:

```
┌─────────────────────────────────────────────────────────┐
│                 MYTHARA ENGINE PRICING                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🚀 STARTUP          💼 SMALL BUSINESS    🏢 MID-MARKET│
│  $25,000/year        $40,000/year         $75,000/year │
│  1-50 employees      51-200 employees     201-1K emps  │
│  [Buy Now]           [Buy Now]            [Contact]    │
│                                                         │
│  🌐 ENTERPRISE       🌍 GLOBAL ENTERPRISE              │
│  $150,000/year       $300,000/year                     │
│  1K-5K employees     5K+ employees                     │
│  [Contact Sales]     [Contact Sales]                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🤝 Sales Email Template:

```
Subject: Mythara Engine Pricing for [Company Name]

Hi [Name],

Based on [Company Name]'s size (~[X] employees), here's your pricing:

Tier: [Tier Name]
Annual License: $[Price] USD
Includes:
  ✓ Full API access
  ✓ Enterprise support
  ✓ Compliance documentation (NIST, HIPAA)
  ✓ On-premise deployment option
  ✓ Custom integration assistance

Payment Link: [Stripe Link]

Questions? Let's schedule a 15-minute call: [Calendly Link]

Best,
Herb Velez
Mythara Labs
Mythara.Engine@yahoo.com
```

---

## 📊 Track Revenue by Tier:

Your webhook automatically captures tier info from Stripe metadata, so you can track:
- Which tiers sell most
- Average deal size
- Revenue by company size

---

**Your pricing is now professional, scalable, and ready for enterprise sales!** 🚀
