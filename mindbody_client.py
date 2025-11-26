import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MINDBODY_API_KEY")
SITE_ID = os.getenv("MINDBODY_SITE_ID")
BASE_URL = os.getenv("MINDBODY_BASE_URL")

HEADERS = {
    "Api-Key": API_KEY,
    "SiteId": SITE_ID,
    "Content-Type": "application/json"
}


# ----------------------------
# 1. FETCH CLIENTS
# ----------------------------
def fetch_clients(search_text: str = None, client_id: str = None):
    """
    Fetch clients from MINDBODY.
    
    IMPORTANT: SearchText only searches FirstName, LastName, and partial Email.
    It does NOT search phone numbers!
    
    Supports:
    - SearchText: Searches first name, last name, partial email (min 3 chars recommended)
    - ClientIds: Search by exact client ID
    
    Examples:
    - fetch_clients(search_text="John") → finds "John Doe"
    - fetch_clients(search_text="doe") → finds "John Doe"  
    - fetch_clients(search_text="john.doe") → finds "john.doe@example.com"
    - fetch_clients(client_id="100015633") → finds specific client
    """
    url = f"{BASE_URL}/client/clients"
    params = {}

    if client_id:
        params["ClientIds"] = client_id
        print("Fetching clients by ID →", params)
    elif search_text:
        # SearchText searches FirstName, LastName, and Email only
        if len(search_text) < 3:
            return {
                "error": "Search text must be at least 3 characters",
                "Clients": [],
                "PaginationResponse": {
                    "RequestedLimit": 0,
                    "RequestedOffset": 0,
                    "PageSize": 0,
                    "TotalResults": 0
                }
            }
        params["SearchText"] = search_text
        print("Fetching clients by search text →", params)
    else:
        # If no parameters, get first 100 clients
        params["Limit"] = 100
        params["Offset"] = 0
        print("Fetching all clients (first 100) →", params)

    response = requests.get(url, headers=HEADERS, params=params)
    
    try:
        return response.json()
    except:
        return {
            "error": "Failed to parse response",
            "status_code": response.status_code,
            "response": response.text[:500]
        }


# ----------------------------
# 2. SEARCH CLIENTS BY PHONE (WORKAROUND)
# ----------------------------
def search_clients_by_phone(phone: str):
    """
    Search for clients by phone number.
    
    NOTE: Mindbody's SearchText doesn't search phone numbers,
    so we fetch all clients and filter locally.
    
    This is slower but works for phone searches.
    """
    print(f"Searching for phone: {phone} (fetching all clients and filtering locally)")
    
    url = f"{BASE_URL}/client/clients"
    all_clients = []
    offset = 0
    limit = 100
    
    # Fetch all clients in batches
    while True:
        params = {"Limit": limit, "Offset": offset}
        response = requests.get(url, headers=HEADERS, params=params)
        
        try:
            data = response.json()
            clients = data.get("Clients", [])
            
            if not clients:
                break
            
            all_clients.extend(clients)
            
            # Check if we got all clients
            total = data.get("PaginationResponse", {}).get("TotalResults", 0)
            if len(all_clients) >= total:
                break
            
            offset += limit
        except:
            break
    
    # Filter by phone
    matching_clients = [
        c for c in all_clients 
        if c.get("MobilePhone") == phone or 
           c.get("HomePhone") == phone or 
           c.get("WorkPhone") == phone
    ]
    
    print(f"Found {len(matching_clients)} clients with phone {phone}")
    
    return {
        "Clients": matching_clients,
        "PaginationResponse": {
            "RequestedLimit": 100,
            "RequestedOffset": 0,
            "PageSize": len(matching_clients),
            "TotalResults": len(matching_clients)
        }
    }


# ----------------------------
# 3. FETCH CLASSES
# ----------------------------
def fetch_classes():
    """
    Fetch MINDBODY classes.
    """
    url = f"{BASE_URL}/class/classes"

    print("Fetching classes…")
    response = requests.get(url, headers=HEADERS)
    
    try:
        return response.json()
    except:
        return {
            "error": "Failed to parse response",
            "status_code": response.status_code,
            "response": response.text[:500]
        }


# ----------------------------
# 4. FETCH APPOINTMENTS
# ----------------------------
def fetch_appointments(staff_id: str = None, start_date: str = None, end_date: str = None):
    """
    Fetch MINDBODY appointments.
    Supports optional:
    - StaffIds
    - StartDate
    - EndDate
    """
    url = f"{BASE_URL}/appointment/appointments"
    params = {}

    if staff_id:
        params["StaffIds"] = staff_id
    if start_date:
        params["StartDate"] = start_date
    if end_date:
        params["EndDate"] = end_date

    print("Fetching appointments →", params)
    response = requests.get(url, headers=HEADERS, params=params)
    
    try:
        return response.json()
    except:
        return {
            "error": "Failed to parse response",
            "status_code": response.status_code,
            "response": response.text[:500]
        }


# ----------------------------
# 5. ADD CLIENT
# ----------------------------
def add_client(
    first_name: str,
    last_name: str,
    email: str,
    phone: str = None,
    address: str = None,
    city: str = None,
    state: str = None,
    postal_code: str = None,
    birth_date: str = None,
    referred_by: str = "Website",
    test_mode: bool = True
):
    """
    Add a new client to MINDBODY.
    
    Args:
        first_name: First name (required)
        last_name: Last name (required)
        email: Email address (required)
        phone: Phone number (required for some sites)
        address: Street address (required for some sites)
        city: City (required for some sites)
        state: State code like "CA" (required for some sites)
        postal_code: Zip code (required for some sites)
        birth_date: Birth date in YYYY-MM-DD format (required for some sites)
        referred_by: How client found you - Required! (default: "Website")
        test_mode: If True, won't actually add to database
    
    Returns:
        Dictionary with result
    """
    url = f"{BASE_URL}/client/addclient"
    
    # Build payload
    payload = {
        "FirstName": first_name,
        "LastName": last_name,
        "Email": email,
        "ReferredBy": referred_by
    }
    
    # Add optional fields
    if phone:
        payload["MobilePhone"] = phone
    if address:
        payload["AddressLine1"] = address
    if city:
        payload["City"] = city
    if state:
        payload["State"] = state
    if postal_code:
        payload["PostalCode"] = postal_code
    if birth_date:
        payload["BirthDate"] = birth_date
    
    # Add test mode flag
    if test_mode:
        payload["Test"] = True
    
    print(f"Adding client: {first_name} {last_name} (Test Mode: {test_mode})")
    print(f"Payload: {payload}")
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Check if client was added
            if "Client" in result:
                client_id = result["Client"].get("Id")
                print(f"✅ Client added successfully! ID: {client_id}")
                return {
                    "success": True,
                    "message": f"Client {first_name} {last_name} added successfully",
                    "client_id": client_id,
                    "client": result["Client"]
                }
            else:
                return {
                    "success": False,
                    "error": "Unexpected response structure",
                    "response": result
                }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}",
                "response": response.text[:500]
            }
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "success": False,
            "error": str(e)
        }