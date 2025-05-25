#!/usr/bin/env python3
"""
MidPay API Example - How to call the API with an API key to get accounts

This example demonstrates how to:
1. Make authenticated requests to the MidPay API
2. Get all account balances
3. Get individual user balances
4. Handle API responses and errors

Prerequisites:
- You need a valid API key (generate one using generate_api_key.py)
- The MidPay API server should be running (python fast_api.py)
"""

import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8000/api"  # Change this to your API server URL
API_KEY = "your_api_key_here"  # Replace with your actual API key

def make_authenticated_request(endpoint, method="GET", data=None):
    """
    Make an authenticated request to the MidPay API
    
    Args:
        endpoint (str): API endpoint (e.g., "/accounts")
        method (str): HTTP method (GET, POST, etc.)
        data (dict): Request data for POST requests
    
    Returns:
        dict: API response data
    """
    url = f"{API_BASE_URL}{endpoint}"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        # Check if request was successful
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return None

def get_all_accounts():
    """
    Get all account balances including escrow
    
    Returns:
        dict: All account balances
    """
    print("Getting all account balances...")
    result = make_authenticated_request("/accounts")
    
    if result:
        print("✅ Successfully retrieved account balances:")
        print(json.dumps(result, indent=2))
        return result
    else:
        print("❌ Failed to retrieve account balances")
        return None

def get_user_balance(user_id):
    """
    Get balance for a specific user
    
    Args:
        user_id (str): User ID ("A" or "B")
    
    Returns:
        dict: User balance information
    """
    print(f"Getting balance for user {user_id}...")
    result = make_authenticated_request(f"/balance/{user_id}")
    
    if result:
        print(f"✅ Successfully retrieved balance for user {user_id}:")
        print(json.dumps(result, indent=2))
        return result
    else:
        print(f"❌ Failed to retrieve balance for user {user_id}")
        return None

def main():
    """
    Main function demonstrating API usage
    """
    print("🚀 MidPay API Example")
    print("=" * 50)
    
    # Check if API key is set
    if API_KEY == "your_api_key_here":
        print("❌ Please set your API key in the API_KEY variable")
        print("   You can generate an API key using: python generate_api_key.py")
        return
    
    print(f"Using API Base URL: {API_BASE_URL}")
    print(f"Using API Key: {API_KEY[:10]}...")
    print()
    
    # Example 1: Get all accounts
    print("📊 Example 1: Get All Accounts")
    print("-" * 30)
    accounts_data = get_all_accounts()
    print()
    
    if accounts_data and accounts_data.get("status") == "success":
        accounts = accounts_data.get("accounts", {})
        print(f"Account A Balance: ${accounts.get('A', 0)}")
        print(f"Account B Balance: ${accounts.get('B', 0)}")
        print(f"Escrow Balance: ${accounts.get('escrow', 0)}")
    
    print()
    
    # Example 2: Get individual user balances
    print("👤 Example 2: Get Individual User Balances")
    print("-" * 40)
    
    # Get balance for user A
    user_a_data = get_user_balance("A")
    if user_a_data and user_a_data.get("status") == "success":
        print(f"User A Balance: ${user_a_data.get('balance', 0)}")
    
    print()
    
    # Get balance for user B
    user_b_data = get_user_balance("B")
    if user_b_data and user_b_data.get("status") == "success":
        print(f"User B Balance: ${user_b_data.get('balance', 0)}")
    
    print()
    print("✨ API example completed!")

if __name__ == "__main__":
    main()
