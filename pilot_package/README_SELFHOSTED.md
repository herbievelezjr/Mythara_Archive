# Mythara Engine Pilot - Self-Hosted Deployment
**Copyright © 2025 Herbert Velez Jr. All rights reserved.**

## When to Use Self-Hosted

Use this option if you need to:
- ✅ Run entirely in your own infrastructure
- ✅ Keep data within your network (air-gapped)
- ✅ Meet compliance requirements (HIPAA, FISMA, etc.)
- ✅ Test offline without internet connectivity

**Otherwise, use the cloud-hosted API endpoint from your welcome email** (easier setup).

---

## Prerequisites

- Docker 20.10+ and Docker Compose
- 2GB RAM minimum
- Port 8000 available

---

## Quick Start (5 minutes)

### 1. Copy environment template
```bash
cp .env.example .env
```

### 2. Edit `.env` file

For **pilot testing** (recommended):
```bash
MYTHARA_PILOT_PAYWALL=true
MYTHARA_PILOT_FORCE_UNLOCK=true
MYTHARA_PILOT_PURCHASE_URL=https://buy.stripe.com/YOUR_LINK
STRIPE_WEBHOOK_SECRET=whsec_demo
PORT=8000
```

**Note:** `MYTHARA_PILOT_FORCE_UNLOCK=true` bypasses payment for local testing.

### 3. Start container
```bash
docker-compose up -d
```

### 4. Verify it's running
```bash
# Check health
curl http://localhost:8000/health

# Check pilot status
curl http://localhost:8000/v1/pilot/status
# Should return: access_granted: true

# Test invocation
curl -X POST http://localhost:8000/v1/clauses/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "clause_id": "cl_test",
    "invocation_context": {"test": true}
  }'
```

---

## Configuration Options

### Option A: Pilot Testing (Force Unlock)
```bash
# .env file
MYTHARA_PILOT_PAYWALL=true
MYTHARA_PILOT_FORCE_UNLOCK=true  # No payment required
```
**Use for:** Local development, demos, testing

### Option B: Production Self-Hosted (Webhook Required)
```bash
# .env file
MYTHARA_PILOT_PAYWALL=true
MYTHARA_PILOT_FORCE_UNLOCK=false  # Requires payment
STRIPE_WEBHOOK_SECRET=whsec_xxx   # Get from Stripe Dashboard
```
**Use for:** Production deployments where you want to validate payment

### Option C: No Paywall (Open Access)
```bash
# .env file
MYTHARA_PILOT_PAYWALL=false
```
**Use for:** Internal enterprise use (no payment required)

---

## Managing the Container

### View logs
```bash
docker-compose logs -f
```

### Stop container
```bash
docker-compose down
```

### Restart container
```bash
docker-compose restart
```

### Update to latest version
```bash
docker-compose pull
docker-compose up -d
```

---

## Exposing to Network (Optional)

### On local network
```bash
# Edit docker-compose.yml, change ports to:
ports:
  - "0.0.0.0:8000:8000"

# Restart
docker-compose restart

# Access from other machines:
curl http://YOUR_IP:8000/health
```

### Behind reverse proxy (Nginx/Traefik)
```nginx
# /etc/nginx/sites-available/mythara
server {
    listen 80;
    server_name mythara.yourcompany.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Air-Gapped Deployment

### 1. On internet-connected machine:
```bash
# Save Docker image
docker pull herbievelezjr/mythara-engine:pilot
docker save herbievelezjr/mythara-engine:pilot > mythara-pilot.tar

# Copy mythara-pilot.tar to air-gapped machine
```

### 2. On air-gapped machine:
```bash
# Load image
docker load < mythara-pilot.tar

# Copy pilot_package/ directory
# Edit .env with MYTHARA_PILOT_FORCE_UNLOCK=true

# Start
docker-compose up -d
```

---

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs

# Common issues:
# - Port 8000 already in use → Change PORT in .env
# - Missing .env file → Copy from .env.example
# - Invalid environment variables → Check syntax in .env
```

### API returns 502 Bad Gateway
```bash
# Check if container is running
docker ps

# Check container health
docker inspect mythara-pilot-api | grep Health

# Restart if unhealthy
docker-compose restart
```

### Pilot access denied (402)
```bash
# Check pilot status
curl http://localhost:8000/v1/pilot/status

# If access_granted: false, check .env:
# - Is MYTHARA_PILOT_FORCE_UNLOCK=true? (for testing)
# - Is STRIPE_WEBHOOK_SECRET correct? (for production)
```

### Can't reach from other machines
```bash
# Check firewall
sudo ufw allow 8000/tcp

# Check docker-compose ports binding
# Should be "0.0.0.0:8000:8000" not "127.0.0.1:8000:8000"
```

---

## Security Considerations

### Production Checklist
- [ ] Set `MYTHARA_PILOT_FORCE_UNLOCK=false`
- [ ] Use real `STRIPE_WEBHOOK_SECRET` from Stripe
- [ ] Generate unique `MYTHARA_API_KEYS` (not demo keys)
- [ ] Enable HTTPS (use reverse proxy with SSL)
- [ ] Restrict network access (firewall rules)
- [ ] Regular updates: `docker-compose pull && docker-compose up -d`

### Compliance Notes
- Data stays in your infrastructure (never leaves your network)
- Audit logs available: `docker-compose logs`
- Integrity hashes in all responses for non-repudiation
- PGP-signed manifests available at `/v1/manifest/clauses`

---

## Performance Tuning

### For high load:
```yaml
# docker-compose.yml
services:
  mythara-api:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

### Scale horizontally:
```bash
docker-compose up -d --scale mythara-api=3
```
**Note:** Requires load balancer (Nginx/HAProxy) in front.

---

## Support

**Email:** Mythara.Engine@yahoo.com
**Docs:** https://github.com/herbievelezjr/Mythara_Archive
**Issues:** https://github.com/herbievelezjr/Mythara_Archive/issues

---

**Your pilot package is ready to deploy!** 🚀
