"""
Script to add multiple clients to Mindbody
Based on: https://developers.mindbodyonline.com/PublicDocumentation/V6
Endpoint: POST /public/v6/client/addclient
"""

import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
import random

load_dotenv()

API_KEY = os.getenv("MINDBODY_API_KEY")
SITE_ID = os.getenv("MINDBODY_SITE_ID")
BASE_URL = os.getenv("MINDBODY_BASE_URL")

HEADERS = {
    "Api-Key": API_KEY,
    "SiteId": SITE_ID,
    "Content-Type": "application/json"
}

# ============================================================================
# SAMPLE CLIENT DATA (10 Clients)
# ============================================================================

SAMPLE_CLIENTS = [
    {
        "FirstName": "John",
        "LastName": "Doe",
        "Email": "john.doe@example.com",
        "MobilePhone": "5551234567",
        "AddressLine1": "123 Main St",
        "City": "San Luis Obispo",
        "State": "CA",
        "PostalCode": "93401",
        "BirthDate": "1990-05-15",
        "ReferredBy": "Website"
    },
    {
        "FirstName": "Jane",
        "LastName": "Smith",
        "Email": "jane.smith@example.com",
        "MobilePhone": "5552345678",
        "AddressLine1": "456 Oak Ave",
        "City": "San Luis Obispo",
        "State": "CA",
        "PostalCode": "93401",
        "BirthDate": "1985-08-22",
        "ReferredBy": "Friend"
    },
    {
        "FirstName": "Michael",
        "LastName": "Johnson",
        "Email": "michael.johnson@example.com",
        "MobilePhone": "5553456789",
        "AddressLine1": "789 Pine Rd",
        "City": "San Luis Obispo",
        "State": "CA",
        "PostalCode": "93401",
        "BirthDate": "1992-12-10",
        "ReferredBy": "Social Media"
    },
    {
        "FirstName": "Emily",
        "LastName": "Williams",
        "Email": "emily.williams@example.com",
        "MobilePhone": "5554567890",
        "AddressLine1": "321 Elm St",
        "City": "San Luis Obispo",
        "State": "CA",
        "PostalCode": "93401",
        "BirthDate": "1988-03-18",
        "ReferredBy": "Google Search"
    },
    {
        "FirstName": "David",
        "LastName": "Brown",
        "Email": "david.brown@example.com",
        "MobilePhone": "5555678901",
        "AddressLine1": "654 Maple Dr",
        "City": "San Luis Obispo",
        "State": "CA",
        "PostalCode": "93401",
        "BirthDate": "1995-07-25",
        "ReferredBy": "Walk-in"
    },
    {
        "FirstName": "Sarah",
        "LastName": "Davis",
        "Email": "sarah.davis@example.com",
        "MobilePhone": "5556789012",
        "AddressLine1": "987 Cedar Ln",
        "City": "San Luis Obispo",
        "State": "CA",
        "PostalCode": "93401",
        "BirthDate": "1991-11-30",
        "ReferredBy": "Email Marketing"
    },
    {
        "FirstName": "Robert",
        "LastName": "Miller",
        "Email": "robert.miller@example.com",
        "MobilePhone": "5557890123",
        "AddressLine1": "147 Birch Way",
        "City": "San Luis Obispo",
        "State": "CA",
        "PostalCode": "93401",
        "BirthDate": "1987-04-12",
        "ReferredBy": "Instagram"
    },
    {
        "FirstName": "Lisa",
        "LastName": "Wilson",
        "Email": "lisa.wilson@example.com",
        "MobilePhone": "5558901234",
        "AddressLine1": "258 Spruce St",
        "City": "San Luis Obispo",
        "State": "CA",
        "PostalCode": "93401",
        "BirthDate": "1993-09-05",
        "ReferredBy": "Facebook"
    },
    {
        "FirstName": "James",
        "LastName": "Moore",
        "Email": "james.moore@example.com",
        "MobilePhone": "5559012345",
        "AddressLine1": "369 Willow Ave",
        "City": "San Luis Obispo",
        "State": "CA",
        "PostalCode": "93401",
        "BirthDate": "1989-01-20",
        "ReferredBy": "Referral"
    },
    {
        "FirstName": "Amanda",
        "LastName": "Taylor",
        "Email": "amanda.taylor@example.com",
        "MobilePhone": "5550123456",
        "AddressLine1": "741 Aspen Rd",
        "City": "San Luis Obispo",
        "State": "CA",
        "PostalCode": "93401",
        "BirthDate": "1994-06-08",
        "ReferredBy": "Yelp"
    }
]


# ============================================================================
# ADD CLIENT FUNCTION
# ============================================================================

def add_client(client_data, test_mode=True):
    """
    Add a single client to Mindbody
    
    Args:
        client_data: Dictionary with client information
        test_mode: If True, won't actually add to database (for testing)
    
    Returns:
        Dictionary with result
    """
    url = f"{BASE_URL}/client/addclient"
    
    # Add Test parameter if in test mode
    payload = client_data.copy()
    if test_mode:
        payload["Test"] = True
    
    print(f"\n{'='*80}")
    print(f"Adding Client: {client_data['FirstName']} {client_data['LastName']}")
    print(f"Email: {client_data['Email']}")
    print(f"Test Mode: {test_mode}")
    print(f"{'='*80}")
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                
                # Check if client was added successfully
                if "Client" in result:
                    client_id = result["Client"].get("Id")
                    print(f"✅ SUCCESS! Client added with ID: {client_id}")
                    print(f"Full Name: {result['Client'].get('FirstName')} {result['Client'].get('LastName')}")
                    return {
                        "success": True,
                        "client_id": client_id,
                        "data": result["Client"]
                    }
                else:
                    print(f"⚠️ Unexpected response structure")
                    print(f"Response: {json.dumps(result, indent=2)}")
                    return {
                        "success": False,
                        "error": "Unexpected response structure",
                        "response": result
                    }
                    
            except ValueError as e:
                print(f"❌ Failed to parse JSON: {e}")
                print(f"Response text: {response.text[:500]}")
                return {
                    "success": False,
                    "error": f"JSON parse error: {e}",
                    "response_text": response.text[:500]
                }
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return {
                "success": False,
                "error": f"HTTP {response.status_code}",
                "response_text": response.text[:500]
            }
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# ADD MULTIPLE CLIENTS
# ============================================================================

def add_multiple_clients(clients_list, test_mode=True):
    """
    Add multiple clients in batch
    
    Args:
        clients_list: List of client dictionaries
        test_mode: If True, won't actually add to database
    
    Returns:
        Summary of results
    """
    print(f"\n🚀 ADDING {len(clients_list)} CLIENTS TO MINDBODY")
    print(f"Test Mode: {test_mode}")
    print(f"Base URL: {BASE_URL}")
    print(f"Site ID: {SITE_ID}\n")
    
    results = {
        "success": [],
        "failed": [],
        "total": len(clients_list)
    }
    
    for i, client in enumerate(clients_list, 1):
        print(f"\n[{i}/{len(clients_list)}] Processing...")
        result = add_client(client, test_mode)
        
        if result["success"]:
            results["success"].append({
                "name": f"{client['FirstName']} {client['LastName']}",
                "email": client['Email'],
                "client_id": result.get("client_id")
            })
        else:
            results["failed"].append({
                "name": f"{client['FirstName']} {client['LastName']}",
                "email": client['Email'],
                "error": result.get("error")
            })
    
    # Print summary
    print(f"\n{'='*80}")
    print(f"📊 SUMMARY")
    print(f"{'='*80}")
    print(f"Total Clients: {results['total']}")
    print(f"✅ Successfully Added: {len(results['success'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    
    if results['success']:
        print(f"\n✅ Successful Additions:")
        for client in results['success']:
            print(f"   - {client['name']} (ID: {client['client_id']}) - {client['email']}")
    
    if results['failed']:
        print(f"\n❌ Failed Additions:")
        for client in results['failed']:
            print(f"   - {client['name']} - {client['email']}")
            print(f"     Error: {client['error']}")
    
    return results


# ============================================================================
# VERIFY CLIENTS WERE ADDED
# ============================================================================

def verify_clients(email_list):
    """
    Verify that clients were added by searching for them
    """
    print(f"\n🔍 VERIFYING CLIENTS...")
    url = f"{BASE_URL}/client/clients"
    
    for email in email_list:
        params = {"SearchText": email, "Limit": 1}
        try:
            response = requests.get(url, headers=HEADERS, params=params)
            if response.status_code == 200:
                data = response.json()
                if "Clients" in data and len(data["Clients"]) > 0:
                    client = data["Clients"][0]
                    print(f"✅ Found: {client['FirstName']} {client['LastName']} (ID: {client['Id']})")
                else:
                    print(f"❌ Not found: {email}")
        except Exception as e:
            print(f"❌ Error checking {email}: {e}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("MINDBODY CLIENT ADDITION TOOL")
    print("="*80)
    
    # Show menu
    print("\nOptions:")
    print("1. Add clients in TEST mode (won't affect database)")
    print("2. Add clients in LIVE mode (will add to database)")
    print("3. Add custom client")
    print("4. Verify existing clients")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        print("\n🧪 TEST MODE - Adding clients...")
        results = add_multiple_clients(SAMPLE_CLIENTS, test_mode=True)
        
    elif choice == "2":
        confirm = input("\n⚠️  WARNING: This will add clients to your LIVE database. Continue? (yes/no): ")
        if confirm.lower() == "yes":
            results = add_multiple_clients(SAMPLE_CLIENTS, test_mode=False)
            
            # Verify
            if results['success']:
                verify_input = input("\nVerify added clients? (yes/no): ")
                if verify_input.lower() == "yes":
                    emails = [c['email'] for c in results['success']]
                    verify_clients(emails)
        else:
            print("Cancelled.")
            
    elif choice == "3":
        print("\n📝 Add Custom Client")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("Email: ")
        phone = input("Phone (10 digits): ")
        referred_by = input("Referred By (e.g., Website, Friend, Social Media): ")
        
        custom_client = {
            "FirstName": first_name,
            "LastName": last_name,
            "Email": email,
            "MobilePhone": phone,
            "AddressLine1": "123 Main St",
            "City": "San Luis Obispo",
            "State": "CA",
            "PostalCode": "93401",
            "BirthDate": "1990-01-01",
            "ReferredBy": referred_by
        }
        
        test_mode = input("Test mode? (yes/no): ").lower() == "yes"
        result = add_client(custom_client, test_mode)
        
    elif choice == "4":
        print("\n🔍 Verify Clients")
        print("Enter emails to check (comma-separated):")
        emails_input = input("Emails: ")
        emails = [e.strip() for e in emails_input.split(",")]
        verify_clients(emails)
        
    elif choice == "5":
        print("\n👋 Goodbye!")
    else:
        print("\n❌ Invalid choice!")