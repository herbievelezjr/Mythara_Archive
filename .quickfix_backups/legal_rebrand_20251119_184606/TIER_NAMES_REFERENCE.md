# 🏷️ Mythara Enterprise Tier Names & Descriptions

**Quick Reference for Sales, Marketing, and Stripe Setup**

---

## 📊 Tier Summary

| Tier Key | Brand Name | Tagline | Price | Company Size |
|----------|-----------|---------|-------|--------------|
| `foundation` | **Mythara Foundation** | Perfect for early-stage startups and SMBs | $25,000/year | 1-50 employees |
| `professional` | **Mythara Professional** | Built for established small businesses | $40,000/year | 51-200 employees |
| `corporate` | **Mythara Corporate** | Enterprise-grade for mid-market leaders | $75,000/year | 201-1,000 employees |
| `enterprise` | **Mythara Enterprise** | Unlimited scale for healthcare enterprises | $150,000/year | 1,001-5,000 employees |
| `sovereign` | **Mythara Sovereign** | Complete ownership for global enterprises | $300,000/year | 5,000+ employees |

---

## 📝 Full Tier Details

### 1. Mythara Foundation ($25K)
**Tagline:** "Perfect for early-stage startups and SMBs"

**Description:**  
Essential SSIP orchestration for growing teams building compliant mental health applications

**Features:**
- Full API access with 100K clause invocations/month
- Standard support (48-hour response)
- NIST 800-53 & HIPAA compliance documentation
- Docker deployment templates
- Community Slack access
- Quarterly security updates

**Ideal For:**  
Startups, mental health apps, telehealth platforms (1-50 employees)

**Stripe Metadata:**
```
license_type=enterprise
tier=foundation
```

---

### 2. Mythara Professional ($40K)
**Tagline:** "Built for established small businesses"

**Description:**  
Advanced orchestration with priority support for scaling healthcare organizations

**Features:**
- Everything in Foundation, plus:
- 500K clause invocations/month
- Priority support (24-hour response)
- Custom integration assistance (5 hours/quarter)
- Advanced monitoring & analytics dashboard
- SOC 2 Type II compliance mapping
- Monthly security patches
- Dedicated onboarding session

**Ideal For:**  
Small healthcare providers, therapy platforms, wellness apps (51-200 employees)

**Stripe Metadata:**
```
license_type=enterprise
tier=professional
```

---

### 3. Mythara Corporate ($75K)
**Tagline:** "Enterprise-grade for mid-market leaders"

**Description:**  
High-volume orchestration with enhanced SLAs for mission-critical mental health infrastructure

**Features:**
- Everything in Professional, plus:
- 2M clause invocations/month
- Premium support (12-hour response, 24/7 emergency)
- Custom integration assistance (15 hours/quarter)
- Multi-environment deployment (dev/staging/prod)
- Dedicated Customer Success Manager
- Custom SLA agreements available
- Bi-weekly strategic review calls
- Early access to new features

**Ideal For:**  
Regional healthcare systems, EAP providers, large therapy networks (201-1K employees)

**Stripe Metadata:**
```
license_type=enterprise
tier=corporate
```

---

### 4. Mythara Enterprise ($150K)
**Tagline:** "Unlimited scale for healthcare enterprises"

**Description:**  
White-glove service with unlimited orchestration for national healthcare organizations

**Features:**
- Everything in Corporate, plus:
- Unlimited clause invocations
- Elite support (4-hour response, 24/7 dedicated hotline)
- Custom integration assistance (40 hours/quarter)
- On-premise deployment option
- Custom feature development prioritization
- Dedicated Technical Account Manager
- Architecture review & optimization
- Annual on-site training & consultation
- White-label options available

**Ideal For:**  
National healthcare networks, insurance companies, federal contractors (1K-5K employees)

**Stripe Metadata:**
```
license_type=enterprise
tier=enterprise
```

---

### 5. Mythara Sovereign ($300K)
**Tagline:** "Complete ownership for global enterprises"

**Description:**  
Full source code escrow and unlimited deployment rights for Fortune 500 healthcare leaders

**Features:**
- Everything in Enterprise, plus:
- Source code escrow agreement
- Unlimited global deployments
- VIP support (1-hour response, 24/7 executive escalation)
- Unlimited custom development hours
- Dedicated development team liaison
- Quarterly executive business reviews
- Joint go-to-market opportunities
- Custom compliance certifications (FedRAMP, etc.)
- Perpetual license option available
- Revenue sharing partnerships considered

**Ideal For:**  
Fortune 500 healthcare companies, global health systems, government agencies (5K+ employees)

**Stripe Metadata:**
```
license_type=enterprise
tier=sovereign
```

---

## 🎯 Usage Examples

### For Website Copy:
```html
<div class="pricing-tier">
  <h2>Mythara Foundation</h2>
  <p class="tagline">Perfect for early-stage startups and SMBs</p>
  <p class="price">$25,000<span>/year</span></p>
  <p class="description">Essential SSIP orchestration for growing teams 
     building compliant mental health applications</p>
  <button>Get Started</button>
</div>
```

### For Sales Emails:
```
Subject: Mythara Corporate - Perfect for [Company Name]

Hi [Name],

Based on [Company]'s size (~500 employees), I recommend 
**Mythara Corporate** - our enterprise-grade tier for mid-market leaders.

**Your Price:** $75,000/year

**What's Included:**
✓ 2M clause invocations/month
✓ Premium 24/7 support with 12-hour response time
✓ Dedicated Customer Success Manager
✓ 15 hours/quarter of custom integration assistance
✓ Multi-environment deployment
✓ Bi-weekly strategic review calls

**Ideal For:** Regional healthcare systems like yours

[Payment Link]
```

### For API Queries:
```bash
# Get Foundation tier pricing
curl "https://heroic-flexibility-production.up.railway.app/v1/pricing/enterprise?tier=foundation"

# Auto-detect tier for 150 employees (returns Professional)
curl "https://heroic-flexibility-production.up.railway.app/v1/pricing/enterprise?employees=150"
```

---

## 💡 Positioning Strategy

**Why These Names?**

- **Foundation** = Trust, stability, essential building block
- **Professional** = Maturity, expertise, reliability
- **Corporate** = Scale, structure, sophistication
- **Enterprise** = Power, capability, unlimited resources
- **Sovereign** = Ultimate control, ownership, independence

**Emotional Progression:**
Foundation → Professional → Corporate → Enterprise → Sovereign
(Building → Growing → Scaling → Leading → Dominating)

---

## 📋 Stripe Product Setup Checklist

For each tier, create:

1. **Product** in Stripe Dashboard
   - Name: `Mythara [Tier Name] - Annual License`
   - Description: Use tagline + description
   
2. **Price**
   - Amount: [Tier price]
   - Currency: USD
   - Billing: One-time (or recurring annual)
   
3. **Payment Link**
   - Success URL: `https://your-domain.com/success?session_id={CHECKOUT_SESSION_ID}`
   - Metadata:
     - `license_type`: `enterprise`
     - `tier`: `[tier_key]`

4. **Product Metadata** (optional but recommended)
   - `employee_range_min`: `[min]`
   - `employee_range_max`: `[max]`
   - `invocations_monthly`: `[limit or "unlimited"]`
   - `support_sla`: `[response time]`

---

**Your pricing is now professional, descriptive, and ready for enterprise marketing!** 🚀
