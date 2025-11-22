"""
Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

Demo: Attorney Referral System
Shows how Gopher matches users with attorneys based on case type and location.
"""

from mythara_gopher_nlp_engine import MytharaGopherNLP

def main():
    print("=" * 80)
    print("MYTHARA GOPHER - ATTORNEY REFERRAL SYSTEM DEMO")
    print("=" * 80)
    print()
    
    # Initialize Gopher
    print("Initializing Gopher...")
    gopher = MytharaGopherNLP()
    print("✅ Gopher initialized successfully\n")
    
    # Test queries
    test_queries = [
        "I need an employment lawyer in California",
        "Find me a personal injury attorney in New York",
        "Looking for a criminal defense lawyer in Florida",
        "I was wrongfully terminated in Los Angeles, need legal help",
        "Can you recommend an immigration lawyer?",
        "I need a lawyer for a car accident in Texas",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print("=" * 80)
        print(f"TEST {i}: {query}")
        print("=" * 80)
        print()
        
        response = gopher.process_query(query, user_id=f"test_user_{i}")
        print(response)
        print()
    
    print("=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
