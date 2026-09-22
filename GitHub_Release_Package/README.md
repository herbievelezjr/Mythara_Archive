# Mythara Engine — Enterprise Licensing Package

**Version:** 1.0.0  
**Release Date:** November 2, 2025  
**Manifest ID:** ME-archive-0001  
**Copyright:** © 2025 Herbert Velez Jr. All rights reserved.  
**License:** Proprietary (see LICENSE.md and COPYRIGHT.md)

---

## Overview

Mythara Engine is a production-ready inference orchestration system with built-in explainability, safety fallbacks, and audit trail generation. This package contains everything needed for enterprise evaluation, pilot deployment, and sovereign integration.

**All source code, documentation, and materials are proprietary and confidential. Copyright headers are present in all files.**

**Key Features:**
- ✅ Clause orchestration with deterministic constraints (99.92% reproducibility)
- ✅ Automated safety fallbacks and shadow resolver
- ✅ Full audit chain with PGP-signed manifests
- ✅ Accessibility support (braille/audio tokens, 99%+ delivery)
- ✅ Air-gapped deployment via Docker container
- ✅ Comprehensive validation suite included

---

## What's Included

### Core Engine
- `core/` — API specifications, explainability guide, escrow documentation
- `Dockerfile` — Reproducible container build (Python 3.11.6-slim)
- `requirements.txt` — Pinned dependencies

### Validation & Testing
- `tests/` — Determinism tests, leakage probes, SSIP audits
- `Evidence/` — Test results, penetration summaries, drift suppression stats
- `validate_suite/` — Automated validation scripts

### Documentation
- `docs/` — Symbolic glossary, invocation manuals, audit protocols
- `Commercial/` — Pricing tiers, one-pager, clause behavior specs
- `Legal/` — Master licensing agreement, NDA templates, compliance frameworks

### Verification Artifacts
- `manifest/RELEASE_MANIFEST.json` + `.asc` (PGP-signed file inventory)
- `manifest/checksums.sha256` + `.asc` (SHA256 hashes with signature)
- `forensic_manifest.json` + `.asc` (Forensic audit manifest)
- `forensic_public_key.asc` (PGP public key for verification)

---

## Quick Start

### 1. Verify Integrity

Import the PGP public key:

```bash
gpg --import forensic_public_key.asc
```

Verify signatures:

```bash
gpg --verify manifest/RELEASE_MANIFEST.json.asc manifest/RELEASE_MANIFEST.json
gpg --verify manifest/checksums.sha256.asc manifest/checksums.sha256
gpg --verify forensic_manifest.json.asc forensic_manifest.json
```

Expected output: `Good signature from "Mythara Engine <Mythara.Engine@yahoo.com>"`

Verify file checksums:

```bash
cd manifest
sha256sum -c checksums.sha256
```

All files should show `OK`.

### 2. Review Documentation

Start with these files:
- `README.md` (this file)
- `Commercial/one_pager.md` — Business overview and value proposition
- `core/API_SPEC_PUBLIC.md` — API endpoints and authentication
- `core/EXPLAINABILITY_GUIDE.md` — How audit trails work
- `docs/📖 Mythara Bible Books I–V.md` — Comprehensive technical documentation

### 3. Run Validation Suite

Build the Docker container:

```bash
docker build -t mythara-engine:1.0.0 -f core/Dockerfile .
```

Run determinism tests:

```bash
python tests/run_determinism_test.py --iterations 3
```

Run security validation:

```bash
python tests/run_leakage_probes.py --count 1000
```

See `tests/README.md` for full validation suite instructions.

### 4. Deploy (Pilot or Production)

**Option A: Cloud Deployment**
- Deploy Docker container to your cloud provider
- Configure environment variables (see `core/README_ESCROW.md`)
- Point API clients to your deployment endpoint

**Option B: Sovereign/Air-Gapped**
- Transfer this entire package to air-gapped environment
- Verify signatures offline
- Build container from Dockerfile
- Deploy to on-premises infrastructure

---

## Licensing Options

### Development License
- **Use Case:** Internal testing, proof-of-concept
- **Restrictions:** Non-production environments only
- **Support:** Email support, 5-day SLA

### Enterprise License
- **Use Case:** Production deployment (up to 100K requests/month)
- **Restrictions:** Single business unit
- **Support:** Priority email + quarterly review calls

### Sovereign License
- **Use Case:** Government, defense, air-gapped deployments
- **Restrictions:** Geographic/entity-specific deployment rights
- **Support:** On-site integration assistance + escrow unlock
- **Includes:** Source code access via escrow release

See `Commercial/### Pricing Tiers.txt` for detailed pricing.

---

## Support & Contact

**Herbert Velez Jr.**  
Mythara Labs LLC (planned)

- **Email:** legal@mythara.engine
- **PGP Fingerprint:** `571F FB4C CCFA DCF A44A  63F6 D968 C2D5 DBE2 486C`
- **Response Time:** 24-48 hours for licensing inquiries

**For Technical Support:**
- Include your license ID and deployment environment
- Attach relevant log files from `tests/output/`

**For Escrow Services:**
- We work with Iron Mountain, Amboseli, or your preferred escrow agent
- Escrow release conditions defined in Master Licensing Agreement

---

## Security Notice

This package contains proprietary technology protected by:
- Trade secret law
- Copyright (© 2025 Herbert Velez Jr.)
- Contractual NDA obligations

**Unauthorized distribution, reverse engineering, or disclosure is prohibited.**

By downloading this package, you agree to:
1. Maintain confidentiality of all contents
2. Use only for authorized evaluation/deployment
3. Not redistribute without written permission from Mythara Labs

---

## Version History

### v1.0.0 (November 2, 2025)
- Initial enterprise release
- PGP-signed manifest and checksums
- Complete validation suite
- Docker container with reproducible builds
- Comprehensive documentation and licensing templates

---

## Next Steps

1. **Schedule Pilot Scoping Call** — Discuss integration requirements, timeline, and success metrics
2. **Execute NDA** — See `Legal/NDA_Mutual_Template.md` for template
3. **Define Pilot SOW** — 4-8 week scoped integration (template in `Legal/`)
4. **Select Escrow Agent** (for Sovereign licenses) — We support major providers

**Ready to get started?** Email legal@mythara.engine with your company name and use case.
