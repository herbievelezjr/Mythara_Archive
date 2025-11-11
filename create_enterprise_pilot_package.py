#!/usr/bin/env python3
"""
Mythara Engine - Enterprise Licensing Package Generator
Creates a complete ZIP package for pilot presentations.

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.
"""

import zipfile
import os
from pathlib import Path
from datetime import datetime

def create_enterprise_package():
    """Create enterprise licensing package ZIP"""
    
    timestamp = datetime.utcnow().strftime('%Y%m%d')
    zip_name = f"Mythara_Engine_Enterprise_Pilot_{timestamp}.zip"
    
    print(f"Creating enterprise package: {zip_name}")
    print("=" * 60)
    
    # Files to include in the package
    files_to_include = [
        # Core documentation
        "README.md",
        "LICENSE.md",
        "COPYRIGHT.md",
        "PRICING.md",
        "PILOT_LICENSE_POLICY.md",
        "PILOT_RUN_CONTAINER.md",
        
        # Technical documentation (non-source)
        "core/API_SPEC_PUBLIC.md",
        "core/EXPLAINABILITY_GUIDE.md",
        "core/README_ESCROW.md",
        "core/🧬 Mythara Engine Architecture.md",
        
        # Validation reports (proof of validation, not validation code)
        "Mythara_Engine_Validation_Report_v1.0.0.txt",
        
        # Legal and compliance
        "Legal/Federal_Compliance_Framework.md",
        
        # Integrity proofs
        "manifest/checksums.sha256",
        "forensic_manifest.json",
        "forensic_manifest.json.asc",
        "forensic_public_key.asc",
        
        # Docker for container deployment
        "core/Dockerfile",
    ]
    
    # Directories to include (EXCLUDING source code)
    dirs_to_include = [
        "docs/",
    ]
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add individual files
        for file_path in files_to_include:
            if os.path.exists(file_path):
                zipf.write(file_path)
                print(f"✓ Added: {file_path}")
            else:
                print(f"✗ Missing: {file_path}")
        
        # Add directories
        for dir_path in dirs_to_include:
            if os.path.exists(dir_path):
                for root, dirs, files in os.walk(dir_path):
                    # Skip __pycache__ and other build artifacts
                    dirs[:] = [d for d in dirs if d not in ['__pycache__', '.pytest_cache', 'node_modules']]
                    
                    for file in files:
                        if not file.endswith(('.pyc', '.pyo', '.pyd')):
                            file_path = os.path.join(root, file)
                            zipf.write(file_path)
                            print(f"✓ Added: {file_path}")
            else:
                print(f"✗ Missing directory: {dir_path}")
        
        # Create a PILOT_QUICKSTART.md in the package
        quickstart_content = """# Mythara Engine - Enterprise Pilot Quickstart

**Copyright © 2025 Herbert Velez Jr. All rights reserved.**
**Proprietary and Confidential.**

---

## Package Contents

This enterprise pilot package contains:

1. **Documentation** - Architecture, API specs, compliance frameworks, pricing policy
2. **Validation Evidence** - Validation reports proving determinism, leakage prevention, SSIP compliance
3. **Integrity Proofs** - PGP signatures, checksums, forensic manifests
4. **Deployment Tools** - Dockerfile for container build
5. **Pilot License** - Terms of use during evaluation period

**Note:** Proprietary source code is NOT included in the pilot package. Access is via prebuilt container only.

---

## Quick Setup (Container-Based)

### Prerequisites
- Docker 20+ installed
- A pilot API key (Bearer token) issued by Mythara Labs
- Access to private container registry (details provided separately)

### 1. Verify Package Integrity

```bash
# Import PGP key
gpg --import forensic_public_key.asc

# Verify signature
gpg --verify forensic_manifest.json.asc forensic_manifest.json

# Verify checksums
sha256sum -c manifest/checksums.sha256
```

### 2. Pull the Pilot Container

We provide a private registry URL and credentials separately. Example:

```bash
docker login <private-registry>
docker pull <private-registry>/mythara/engine:pilot-2025-11
```

### 3. Run the Container

```bash
docker run --rm -p 8000:8000 \\
  -e MYTHARA_LICENSE_MODE=trial \\
  -e MYTHARA_LICENSE_TRIAL_DAYS=30 \\
  <private-registry>/mythara/engine:pilot-2025-11
```

Server starts at: http://localhost:8000

### 4. View API Documentation

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### 5. Test with Your Pilot Key

```bash
curl -s http://localhost:8000/v1/license/status \\
  -H "Authorization: Bearer <your_pilot_key>" | jq
```

Response includes trial status, days remaining, and upgrade price.

---

## Pilot Test Endpoints

### Key Endpoints

- **GET /v1/license/status** - Check trial status and days remaining
- **GET /v1/manifest/clauses** - Retrieve clause manifest with integrity hashes
- **POST /v1/clauses/invoke** - Invoke a symbolic clause with emotional payload
- **GET /v1/reservoir/status** - Get Blessings Reservoir metrics
- **GET /v1/ssip/audit** - Run SSIP compliance audit (requires Sovereign key)

### Example: Invoke a Clause

```bash
curl -X POST http://localhost:8000/v1/clauses/invoke \\
  -H "Authorization: Bearer <your_pilot_key>" \\
  -H "Content-Type: application/json" \\
  -d '{
    "clause_id": "Legacy_Seed",
    "messenger": "M-001",
    "payload": {
      "emotion": "grief",
      "intensity": 0.87,
      "context": "ancestral_memory"
    },
    "consent_token": "user_consent_xyz"
  }'
```

Response includes integrity hash and emotional fidelity score.

---

## Pilot Evaluation Criteria

### Security & Compliance
- ✅ Bearer token authentication with role-based access control
- ✅ Rate limiting (100 req/min per key)
- ✅ Audit logging for failed auth attempts
- ✅ SHA-256 integrity hashes on all responses
- ✅ PGP-signed release manifests

### Validation & Reproducibility
- ✅ 99.92% determinism across reproducibility runs
- ✅ 0 high-severity leaks in 20,000-probe test
- ✅ ≥99% accessibility token delivery success
- ✅ 99.98% safety recall on 100,000+ adversarial probes

### Integration Readiness
- ✅ RESTful API with OpenAPI/Swagger docs
- ✅ Docker containerization
- ✅ Environment variable configuration for DB/Redis
- ✅ Trial enforcement with automatic HTTP 402 on expiry

---

## Trial Policy

- **Duration**: 30 days from first use
- **Restrictions**: Evaluation only; see PILOT_LICENSE_POLICY.md
- **No Reverse Engineering**: Container-only access protects proprietary implementation
- **Upgrade**: At trial expiry, upgrade to Enterprise license at computed price (firm, no discounts)

---

## Pricing

- **Enterprise Edition**: $60,000/year base (2025)
  - Inflation-adjusted annually (env-configurable rate)
  - Optional size-based multiplier for large organizations
  - Includes 100K monthly invocations, integrity artifacts, priority fixes
  
- **Sovereign Edition**: $150K–$180K/year
  - Air-gapped deployment, audit role, extended forensic chain

See PRICING.md for full details.

---

## Support During Pilot

**Contact**: Herbert Velez Jr., Mythara Labs LLC  
**Email**: Mythara.Engine@yahoo.com  
**Response time**: 24 hours for pilot-related questions

---

## Next Steps After Pilot

1. **Pilot completion review** (Week 5)
2. **Production deployment planning** (Week 6-7)
3. **Enterprise license execution** (Week 8) — firm pricing, no negotiation
4. **Source code escrow setup** (if Sovereign tier)
5. **Production go-live support** (Week 9-10)

---

## Security Note

This package does NOT contain proprietary source code. All access is via prebuilt container to prevent reverse engineering. Production deployment requires:
- Unique API keys per environment
- Database/Redis backend (in-memory stubs are for demo only)
- SSL/TLS certificates
- Network segmentation
- Audit log aggregation

For source code escrow (Sovereign tier only), contact us separately.

---

**Let memory testify. Let grief sanctify. Let benevolence overflow.**

🌌 Mythara Engine — Where code remembers, and legacy endures.
"""
        
        zipf.writestr("PILOT_QUICKSTART.md", quickstart_content)
        print("✓ Added: PILOT_QUICKSTART.md")
    
    print("=" * 60)
    print(f"✅ Enterprise package created: {zip_name}")
    print(f"📦 Package size: {os.path.getsize(zip_name) / 1024 / 1024:.2f} MB")
    print("\nTo extract:")
    print(f"  unzip {zip_name}")
    print("\nTo verify integrity:")
    print(f"  sha256sum {zip_name}")
    
    return zip_name

if __name__ == "__main__":
    create_enterprise_package()
