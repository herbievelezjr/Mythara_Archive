#!/usr/bin/env python3
"""
Mythara Engine - Python Client Library
Copyright © 2025 Herbert Velez Jr. All rights reserved.
"""

import requests
import json
from typing import Dict, Any, Optional
from datetime import datetime


class MytharaClient:
    """Official Python client for Mythara Engine API."""
    
    def __init__(self, api_url: str, api_key: str, timeout: int = 30):
        """
        Initialize Mythara client.
        
        Args:
            api_url: Base URL of Mythara API (e.g., https://mythara.up.railway.app)
            api_key: Your pilot API key (starts with sk_pilot_)
            timeout: Request timeout in seconds (default: 30)
        """
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'MytharaClient/1.0.0'
        })
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health status."""
        response = self.session.get(
            f'{self.api_url}/health',
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def get_pilot_status(self) -> Dict[str, Any]:
        """Get current pilot access status."""
        response = self.session.get(
            f'{self.api_url}/v1/pilot/status',
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def get_clause_manifest(self) -> Dict[str, Any]:
        """Get available clauses and their integrity hashes."""
        response = self.session.get(
            f'{self.api_url}/v1/manifest/clauses',
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def invoke_clause(
        self,
        clause_id: str,
        context: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Invoke a clause with given context.
        
        Args:
            clause_id: ID of clause to invoke (e.g., "cl_test")
            context: Invocation context data
            metadata: Optional metadata for invocation
            
        Returns:
            Invocation result with integrity hash
        """
        payload = {
            'clause_id': clause_id,
            'invocation_context': context
        }
        if metadata:
            payload['metadata'] = metadata
        
        response = self.session.post(
            f'{self.api_url}/v1/clauses/invoke',
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def __repr__(self):
        return f'MytharaClient(api_url="{self.api_url}")'


# Example usage
if __name__ == '__main__':
    import os
    
    # Load from environment or use defaults
    API_URL = os.getenv('MYTHARA_API_URL', 'http://localhost:8000')
    API_KEY = os.getenv('MYTHARA_API_KEY', 'demo_key')
    
    client = MytharaClient(api_url=API_URL, api_key=API_KEY)
    
    try:
        # Health check
        print("🔍 Checking API health...")
        health = client.health_check()
        print(f"✅ Status: {health['status']}")
        
        # Pilot status
        print("\n🎫 Checking pilot access...")
        pilot = client.get_pilot_status()
        print(f"✅ Access: {pilot['access_granted']}")
        
        # Clause manifest
        print("\n📋 Fetching clause manifest...")
        manifest = client.get_clause_manifest()
        print(f"✅ Available clauses: {len(manifest['clauses'])}")
        
        # Invoke test clause
        print("\n⚡ Invoking test clause...")
        result = client.invoke_clause(
            clause_id='cl_test',
            context={'test': True, 'timestamp': datetime.utcnow().isoformat()}
        )
        print(f"✅ Invocation ID: {result['invocation_id']}")
        print(f"✅ Integrity: {result['integrity_hash'][:32]}...")
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ API Error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
