# Copyright © 2025 Herbert Velez Jr. All rights reserved.
# Proprietary and Confidential.

"""
Sales Bot SSIP Governance - COMPILED/OBFUSCATED VERSION

This is a DEMO-SAFE version with proprietary logic protected.

For production deployment:
1. Compile to .pyc (bytecode)
2. Use PyArmor for obfuscation
3. Deploy only .pyd (compiled extension)
4. API-only access (no source exposure)
"""

from pathlib import Path
import json
from datetime import datetime

# Import the proprietary governance engine (compiled)
try:
    # In production, this would import from compiled .pyd file
    # from mythara_governance_engine import SalesGovernanceEngine
    from sales_bot_ssip_governance import SalesGovernanceEngine
except ImportError:
    print("⚠️  Proprietary governance engine not available")
    print("   Contact sales@mythara.com for licensing")
    raise


class PublicSalesBotInterface:
    """
    Public interface for sales bot - hides proprietary SSIP logic
    
    Customers see:
    - Input: email_data
    - Output: draft + governance decision
    
    Customers DON'T see:
    - How clauses are enforced
    - How blessings are calculated
    - How violations are detected
    - How hashing algorithm works
    """
    
    def __init__(self):
        # Proprietary engine (compiled, not readable)
        self._engine = SalesGovernanceEngine()  # This would be .pyd in production
        
        # Import email assistant for processing
        from sales_bot_ssip_governance import GovernedEmailAssistant
        self._assistant = GovernedEmailAssistant()
    
    def process_email(self, email_data: dict) -> dict:
        """
        Process email with Mythara SSIP governance
        
        Args:
            email_data: {"subject": str, "body": str}
        
        Returns:
            {
                "draft": str,                    # Generated response
                "can_auto_send": bool,          # Whether bot can send without human
                "action_taken": str,            # AUTO_SEND or HUMAN_REVIEW_REQUIRED
                "messenger": str,               # Authority level (Gabriel/Raphael/etc)
                "governance_summary": {         # Transparency (no proprietary logic)
                    "intent": str,
                    "autonomy_level": str,
                    "blessings": int,
                    "violations": list,
                    "hash": str
                }
            }
        
        NOTE: Clause enforcement logic is proprietary and hidden in compiled module
        """
        # Proprietary logic hidden in compiled _assistant
        result = self._assistant.process_email(email_data)
        
        # Return only public interface (no internal implementation details)
        return {
            "draft": result["draft"],
            "can_auto_send": result["can_auto_send"],
            "action_taken": result["action_taken"],
            "messenger": result["messenger"],
            "governance_summary": {
                "intent": result["intent"],
                "autonomy_level": result["autonomy_level"],
                "blessings": result["blessings"],
                "violations": result["violations"],  # What was wrong (not HOW detected)
                "hash": result["hash"]
            }
        }
    
    def get_audit_log(self, limit: int = 100) -> list:
        """
        Retrieve audit trail (for transparency)
        
        Returns governance decisions (WHAT happened), 
        not enforcement logic (HOW it works)
        """
        log_path = Path("Commercial/bot_audit_log.jsonl")
        if not log_path.exists():
            return []
        
        entries = []
        with open(log_path, 'r') as f:
            for line in f:
                entries.append(json.loads(line))
                if len(entries) >= limit:
                    break
        
        return entries
    
    def get_governance_stats(self) -> dict:
        """
        Public stats (transparency without revealing proprietary logic)
        """
        report = self._assistant.get_governance_report()
        
        return {
            "autonomy_level": report["autonomy_level"],
            "blessings": report["blessings"],
            "total_emails_processed": report["total_auto_sends"] + report["human_overrides"],
            "auto_sends": report["total_auto_sends"],
            "human_overrides": report["human_overrides"],
            "violations_caught": report["errors_caught"],
            
            # Proprietary implementation hidden
            "note": "Clause enforcement algorithm: Proprietary (Mythara Engine SSIP)"
        }


# ============================================================================
# PRODUCTION DEPLOYMENT GUIDE (Keep Source Code Hidden)
# ============================================================================

"""
## OPTION 1: Compile to Bytecode (.pyc)

```bash
# Compile to bytecode (basic obfuscation)
py -3.11 -m py_compile sales_bot_ssip_governance.py

# Deploy only .pyc file (not .py source)
# Users can import but can't read source
```

## OPTION 2: PyArmor (Professional Obfuscation)

```bash
# Install PyArmor
pip install pyarmor

# Obfuscate the proprietary module
pyarmor obfuscate sales_bot_ssip_governance.py

# Deploy obfuscated files (unreadable even with decompilers)
```

## OPTION 3: Compile to C Extension (.pyd/.so)

```bash
# Install Cython
pip install cython

# Create setup.py:
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("sales_bot_ssip_governance.py")
)

# Compile
python setup.py build_ext --inplace

# Deploy only .pyd file (Windows) or .so (Linux)
# Completely unreadable - it's compiled C code
```

## OPTION 4: API-Only (No Code Shared at All)

```python
# Host on your server
# Customers call API endpoint, never see code

import requests

def process_email_via_api(email_data):
    response = requests.post(
        "https://api.mythara.com/sales-bot/process",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json=email_data
    )
    return response.json()
```

## OPTION 5: License File Protection

```python
# sales_bot_ssip_governance.py

def _check_license():
    license_path = Path("mythara_license.key")
    if not license_path.exists():
        raise Exception("No valid Mythara license. Contact sales@mythara.com")
    
    # Verify license signature (proprietary crypto)
    # Only runs with valid license key
    ...

# At module import
_check_license()
```

## RECOMMENDED: Combination Approach

1. **Obfuscate with PyArmor** (prevents reverse engineering)
2. **Add license check** (prevents unauthorized use)
3. **Deploy only compiled files** (.pyc or .pyd)
4. **Offer API option** for highest security customers

This way:
- ✅ Customers can USE the technology
- ✅ Audit logs are transparent (builds trust)
- ❌ Customers CANNOT steal the implementation
- ❌ Competitors CANNOT reverse engineer

---

## FOR DEMOS: Show Results, Not Code

On sales calls:
- ✅ Show: bot_audit_log.jsonl (transparency)
- ✅ Show: Governance stats (blessings, violations)
- ✅ Show: Email drafts being validated
- ❌ Don't show: sales_bot_ssip_governance.py (proprietary)

Say: "The clause enforcement engine is proprietary Mythara SSIP. 
      I can show you the audit trail and governance decisions,
      but the implementation is licensed technology."
"""

if __name__ == '__main__':
    print("="*80)
    print("MYTHARA SALES BOT - PUBLIC INTERFACE (Proprietary Logic Hidden)")
    print("="*80)
    
    # Public interface - customers can use this
    bot = PublicSalesBotInterface()
    
    # Test email
    email = {
        "subject": "Re: Mythara Demo",
        "body": "This looks interesting. Can we schedule a call?"
    }
    
    print("\n📧 Processing email (proprietary SSIP validation running...):\n")
    result = bot.process_email(email)
    
    print(f"Draft: {result['draft'][:100]}...")
    print(f"\nCan Auto-Send: {result['can_auto_send']}")
    print(f"Action: {result['action_taken']}")
    print(f"Messenger: {result['messenger']}")
    print(f"\nGovernance Summary:")
    print(f"  Intent: {result['governance_summary']['intent']}")
    print(f"  Autonomy: {result['governance_summary']['autonomy_level']}")
    print(f"  Blessings: {result['governance_summary']['blessings']}/100")
    print(f"  Violations: {result['governance_summary']['violations']}")
    print(f"  Hash: {result['governance_summary']['hash'][:16]}...")
    
    print("\n" + "="*80)
    print("✅ PROPRIETARY LOGIC PROTECTED")
    print("="*80)
    print("\nCustomers see:")
    print("  ✓ Audit trail (transparency)")
    print("  ✓ Governance decisions (what happened)")
    print("  ✓ Violation summaries (what was wrong)")
    print("\nCustomers DON'T see:")
    print("  ✗ Clause enforcement algorithm (how violations detected)")
    print("  ✗ Blessings calculation logic (how trust scored)")
    print("  ✗ Hashing implementation (proprietary crypto)")
    print("  ✗ Source code (compiled/obfuscated)")
    print("\n💰 Proprietary technology licensed under Mythara Engine SSIP")
