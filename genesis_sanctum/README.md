# Mythara Engine Pilot - Quick Start
**Copyright © 2025 Herbert Velez Jr. All rights reserved.**

## 🎯 You're Ready to Go!

Your pilot access is **already active**. No installation needed to start testing.

---

## ⚡ Test in 30 Seconds

**Your credentials are in the email** you received. Run this command:

```bash
curl -X POST https://YOUR_API_ENDPOINT/v1/clauses/invoke \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "clause_id": "cl_test",
    "invocation_context": {"test": true}
  }'
```

✅ **Success Response:**
```json
{
  "invocation_id": "inv_...",
  "clause_id": "cl_test",
  "result": {...},
  "integrity_hash": "sha256:...",
  "timestamp": "2025-11-11T..."
}
```

---

## 📚 What You Can Do

### 1. Check Your Pilot Status
```bash
curl https://YOUR_API_ENDPOINT/v1/pilot/status
```

### 2. Get Clause Manifest
```bash
curl https://YOUR_API_ENDPOINT/v1/manifest/clauses
```

### 3. Invoke Clauses
```bash
curl -X POST https://YOUR_API_ENDPOINT/v1/clauses/invoke \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "clause_id": "YOUR_CLAUSE_ID",
    "invocation_context": {
      "your": "data"
    }
  }'
```

---

## 🐍 Python Examples

See `examples/quickstart.py` for complete examples:

```python
from client.mythara_client import MytharaClient

client = MytharaClient(
    api_url="https://YOUR_API_ENDPOINT",
    api_key="YOUR_API_KEY"
)

# Invoke a clause
result = client.invoke_clause(
    clause_id="cl_test",
    context={"test": True}
)

print(f"Result: {result['result']}")
print(f"Integrity: {result['integrity_hash']}")
```

---

## 🏢 Self-Hosted Option (Air-Gapped)

**For compliance or air-gapped environments**, you can run Mythara locally:

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your credentials**

3. **Start container:**
   ```bash
   docker-compose up -d
   ```

4. **Test locally:**
   ```bash
   curl http://localhost:8000/health
   ```

See `README_SELFHOSTED.md` for detailed setup.

---

## 📖 Documentation

- **API Reference:** `docs/API_REFERENCE.md`
- **Compliance Guide:** `docs/COMPLIANCE_GUIDE.md` (NIST/HIPAA mapping)
- **Troubleshooting:** `docs/TROUBLESHOOTING.md`

---

## ⏰ Your Pilot Access

- **Duration:** 30 days from purchase
- **Endpoint:** Provided in your welcome email
- **API Key:** Provided in your welcome email
- **Support:** Reply to welcome email or open GitHub issue

---

## 🚀 Next Steps

1. ✅ Test the quick example above
2. ✅ Review API Reference docs
3. ✅ Try your compliance use case
4. ✅ Schedule walkthrough if needed

---

## ❓ Need Help?

- **Email:** Mythara.Engine@yahoo.com
- **Schedule:** https://calendly.com/mythara-engine/pilot-onboarding
- **Docs:** https://github.com/herbievelezjr/Mythara_Archive

---

**Your pilot started today. Let's make compliance validation fast!** 🎯
