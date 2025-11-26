"""
Diagnostic script to see the exact error when adding a client
"""

import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("MINDBODY_API_KEY")
SITE_ID = os.getenv("MINDBODY_SITE_ID")
BASE_URL = os.getenv("MINDBODY_BASE_URL")

HEADERS = {
    "Api-Key": API_KEY,
    "SiteId": SITE_ID,
    "Content-Type": "application/json"
}

print("="*80)
print("🔍 DIAGNOSING ADD CLIENT ERROR")
print("="*80)

print(f"\n📋 Configuration:")
print(f"   BASE_URL: {BASE_URL}")
print(f"   SITE_ID: {SITE_ID}")
print(f"   API_KEY: {API_KEY[:10]}... (truncated)")

# Test 1: Minimal payload (only required fields)
print("\n" + "="*80)
print("TEST 1: Minimal Payload (Test Mode)")
print("="*80)

url = f"{BASE_URL}/client/addclient"

payload1 = {
    "FirstName": "John",
    "LastName": "Doe",
    "Email": "john.doe.test@example.com",
    "Test": True
}

print(f"\n🔗 URL: {url}")
print(f"📦 Payload:")
print(json.dumps(payload1, indent=2))

response1 = requests.post(url, headers=HEADERS, json=payload1)

print(f"\n📊 Status Code: {response1.status_code}")
print(f"📝 Response:")
print(response1.text)

if response1.status_code != 200:
    try:
        error_data = response1.json()
        print(f"\n❌ Error Details:")
        print(json.dumps(error_data, indent=2))
    except:
        print(f"\n❌ Raw Error: {response1.text}")

# Test 2: With all fields
print("\n" + "="*80)
print("TEST 2: Full Payload (Test Mode)")
print("="*80)

payload2 = {
    "FirstName": "Jane",
    "LastName": "Smith",
    "Email": "jane.smith.test@example.com",
    "MobilePhone": "5551234567",
    "AddressLine1": "123 Main St",
    "City": "San Luis Obispo",
    "State": "CA",
    "PostalCode": "93401",
    "BirthDate": "1990-05-15",
    "Test": True
}

print(f"\n📦 Payload:")
print(json.dumps(payload2, indent=2))

response2 = requests.post(url, headers=HEADERS, json=payload2)

print(f"\n📊 Status Code: {response2.status_code}")
print(f"📝 Response:")
print(response2.text)

if response2.status_code != 200:
    try:
        error_data = response2.json()
        print(f"\n❌ Error Details:")
        print(json.dumps(error_data, indent=2))
    except:
        print(f"\n❌ Raw Error: {response2.text}")

# Test 3: Check if we need to send it differently
print("\n" + "="*80)
print("TEST 3: Alternative Format")
print("="*80)

payload3 = {
    "Client": {
        "FirstName": "Test",
        "LastName": "User",
        "Email": "test.user@example.com"
    },
    "Test": True
}

print(f"\n📦 Payload (wrapped in 'Client'):")
print(json.dumps(payload3, indent=2))

response3 = requests.post(url, headers=HEADERS, json=payload3)

print(f"\n📊 Status Code: {response3.status_code}")
print(f"📝 Response:")
print(response3.text)

# Test 4: Check the endpoint documentation
print("\n" + "="*80)
print("TEST 4: Try Different Endpoint")
print("="*80)

alternative_endpoints = [
    f"{BASE_URL}/client/addclient",
    f"{BASE_URL}/client/addorupdateclient",
]

for endpoint in alternative_endpoints:
    print(f"\n🔗 Trying: {endpoint}")
    
    test_payload = {
        "FirstName": "Test",
        "LastName": "User",
        "Email": "test@example.com",
        "Test": True
    }
    
    try:
        resp = requests.post(endpoint, headers=HEADERS, json=test_payload, timeout=10)
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"   ✅ THIS ONE WORKS!")
            print(f"   Response: {resp.text[:200]}")
        else:
            print(f"   Response: {resp.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}")

print("\n" + "="*80)
print("🏁 DIAGNOSTIC COMPLETE")
print("="*80)
print("\n💡 Share the output above to identify the exact issue!")