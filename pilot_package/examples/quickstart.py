#!/usr/bin/env python3
"""
Mythara Engine - Quick Start Examples
Copyright © 2025 Herbert Velez Jr. All rights reserved.
"""

import os
import sys
from pathlib import Path

# Add client library to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from client.mythara_client import MytharaClient


def example_1_basic_invocation():
    """Example 1: Basic clause invocation."""
    print("=" * 60)
    print("Example 1: Basic Clause Invocation")
    print("=" * 60)
    
    client = MytharaClient(
        api_url=os.getenv('MYTHARA_API_URL', 'http://localhost:8000'),
        api_key=os.getenv('MYTHARA_API_KEY', 'demo_key')
    )
    
    # Invoke a test clause
    result = client.invoke_clause(
        clause_id='cl_test',
        context={'message': 'Hello from pilot!'}
    )
    
    print(f"\n✅ Invocation successful!")
    print(f"   Invocation ID: {result['invocation_id']}")
    print(f"   Integrity Hash: {result['integrity_hash']}")
    print(f"   Timestamp: {result['timestamp']}")
    

def example_2_compliance_workflow():
    """Example 2: Compliance validation workflow."""
    print("\n" + "=" * 60)
    print("Example 2: Compliance Validation Workflow")
    print("=" * 60)
    
    client = MytharaClient(
        api_url=os.getenv('MYTHARA_API_URL', 'http://localhost:8000'),
        api_key=os.getenv('MYTHARA_API_KEY', 'demo_key')
    )
    
    # Step 1: Check pilot status
    print("\n📋 Step 1: Verify pilot access...")
    status = client.get_pilot_status()
    if not status['access_granted']:
        print("❌ Pilot access required!")
        return
    print(f"✅ Pilot active (expires in {status.get('days_remaining', 'N/A')} days)")
    
    # Step 2: Get available clauses
    print("\n📋 Step 2: Fetch clause manifest...")
    manifest = client.get_clause_manifest()
    print(f"✅ {len(manifest['clauses'])} clauses available")
    print(f"   Manifest Integrity: {manifest['manifest_integrity_hash'][:32]}...")
    
    # Step 3: Run compliance check
    print("\n📋 Step 3: Execute compliance validation...")
    result = client.invoke_clause(
        clause_id='cl_nist_sp_800_53_ac_2',  # Example NIST control
        context={
            'control_family': 'Access Control',
            'control_id': 'AC-2',
            'system_id': 'demo_system',
            'validation_type': 'automated'
        },
        metadata={
            'auditor': 'pilot_user',
            'audit_date': '2025-11-11',
            'framework': 'NIST SP 800-53 Rev 5'
        }
    )
    
    print(f"✅ Validation complete!")
    print(f"   Control: AC-2 (Account Management)")
    print(f"   Result Integrity: {result['integrity_hash'][:32]}...")
    print(f"   Use this hash for audit trail!")


def example_3_error_handling():
    """Example 3: Proper error handling."""
    print("\n" + "=" * 60)
    print("Example 3: Error Handling")
    print("=" * 60)
    
    from requests.exceptions import HTTPError, Timeout
    
    client = MytharaClient(
        api_url=os.getenv('MYTHARA_API_URL', 'http://localhost:8000'),
        api_key=os.getenv('MYTHARA_API_KEY', 'demo_key'),
        timeout=5
    )
    
    try:
        # Try to invoke invalid clause
        print("\n🧪 Testing invalid clause ID...")
        result = client.invoke_clause(
            clause_id='cl_nonexistent',
            context={}
        )
    except HTTPError as e:
        if e.response.status_code == 404:
            print(f"✅ Correctly handled 404: Clause not found")
        elif e.response.status_code == 402:
            print(f"✅ Correctly handled 402: Payment required")
        else:
            print(f"❌ HTTP Error: {e.response.status_code}")
    except Timeout:
        print(f"⏱️  Request timed out")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def example_4_batch_processing():
    """Example 4: Batch clause invocations."""
    from requests.exceptions import HTTPError
    
    print("\n" + "=" * 60)
    print("Example 4: Batch Processing")
    print("=" * 60)
    
    client = MytharaClient(
        api_url=os.getenv('MYTHARA_API_URL', 'http://localhost:8000'),
        api_key=os.getenv('MYTHARA_API_KEY', 'demo_key')
    )
    
    # Simulate validating multiple controls
    controls = [
        {'id': 'AC-2', 'name': 'Account Management'},
        {'id': 'AC-3', 'name': 'Access Enforcement'},
        {'id': 'AU-2', 'name': 'Audit Events'},
    ]
    
    print(f"\n📋 Validating {len(controls)} NIST controls...")
    
    results = []
    for control in controls:
        try:
            result = client.invoke_clause(
                clause_id=f"cl_nist_sp_800_53_{control['id'].lower().replace('-', '_')}",
                context={
                    'control_id': control['id'],
                    'control_name': control['name']
                }
            )
            results.append({
                'control': control['id'],
                'status': 'validated',
                'integrity': result['integrity_hash']
            })
            print(f"   ✅ {control['id']}: {control['name']}")
        except HTTPError as e:
            results.append({
                'control': control['id'],
                'status': 'error',
                'error': str(e.response.status_code)
            })
            print(f"   ⚠️  {control['id']}: Validation skipped")
    
    validated_count = len([r for r in results if r['status'] == 'validated'])
    print(f"\n✅ Batch complete: {validated_count}/{len(controls)} successful")


if __name__ == '__main__':
    print("\n🚀 Mythara Engine - Quick Start Examples\n")
    
    # Check environment
    api_url = os.getenv('MYTHARA_API_URL')
    api_key = os.getenv('MYTHARA_API_KEY')
    
    if not api_url or not api_key:
        print("⚠️  Set environment variables first:")
        print("   export MYTHARA_API_URL='https://your-api-endpoint'")
        print("   export MYTHARA_API_KEY='sk_pilot_xxx'")
        print("\nUsing defaults for demo...\n")
    
    # Run examples
    try:
        example_1_basic_invocation()
        example_2_compliance_workflow()
        example_3_error_handling()
        example_4_batch_processing()
        
        print("\n" + "=" * 60)
        print("✅ All examples complete!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nMake sure your API is running and credentials are correct.")
