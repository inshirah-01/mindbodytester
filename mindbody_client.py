import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MINDBODY_API_KEY")
SITE_ID = os.getenv("MINDBODY_SITE_ID")
BASE_URL = os.getenv("MINDBODY_BASE_URL")

# -------------------------
# INTERNAL TOKEN STORAGE
# -------------------------
USER_TOKEN = None
TOKEN_EXPIRY = 0   # Unix timestamp


# ============================================================
# 1) ISSUE USER TOKEN (Staff Login)
# ============================================================
def issue_user_token(username: str, password: str):
    global USER_TOKEN, TOKEN_EXPIRY

    url = f"{BASE_URL}/usertoken/issue"
    payload = {
        "Username": username,
        "Password": password
    }

    headers = {
        "Api-Key": API_KEY,
        "SiteId": SITE_ID,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if "AccessToken" in data:
        USER_TOKEN = data["AccessToken"]
        # Token expiry: now + 23 hours
        TOKEN_EXPIRY = time.time() + (23 * 60 * 60)

    return data


# ============================================================
# 2) ENSURE VALID TOKEN (auto-renew)
# ============================================================
def ensure_token():
    global USER_TOKEN, TOKEN_EXPIRY

    # still valid
    if USER_TOKEN and time.time() < TOKEN_EXPIRY:
        return USER_TOKEN

    # expired — reissue using default sandbox credentials
    username = "mindbodysandbox99@gmail.com"
    password = "Apitest1234"

    print("🔄 Refreshing MINDBODY Staff Token...")
    data = issue_user_token(username, password)

    if "AccessToken" not in data:
        raise Exception("Failed to refresh MINDBODY user token")

    return USER_TOKEN


# ============================================================
# 3) UNIVERSAL REQUEST HANDLER
# ============================================================
def mb_request(method, endpoint, params=None, body=None, require_auth=False):
    url = f"{BASE_URL}{endpoint}"

    headers = {
        "Api-Key": API_KEY,
        "SiteId": SITE_ID,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    if require_auth:
        token = ensure_token()
        headers["Authorization"] = f"Bearer {token}"

    response = requests.request(
        method=method,
        url=url,
        headers=headers,
        params=params,
        json=body
    )

    try:
        return response.json()
    except:
        return {"raw": response.text}


# ============================================================
# 4) CLIENT ENDPOINTS
# ============================================================
def add_client(client_data: dict):
    """Add a new client (requires auth token)."""
    return mb_request(
        method="POST",
        endpoint="/client/addclient",
        body=client_data,
        require_auth=True
    )


def get_client_info(client_id: str):
    """Get client complete info."""
    return mb_request(
        method="GET",
        endpoint="/client/clientcompleteinfo",
        params={"request.clientId": client_id},
        require_auth=True
    )


def get_client_visits(client_id: str):
    """Visit/attendance history."""
    return mb_request(
        method="GET",
        endpoint="/client/clientvisits",
        params={"ClientId": client_id},
        require_auth=True
    )


# ============================================================
# 5) CLASS ENDPOINTS
# ============================================================
def get_class_schedule(start_date=None, end_date=None):
    params = {
        "StartDate": start_date,
        "EndDate": end_date
    }
    return mb_request(
        method="GET",
        endpoint="/class/classes",
        params=params,
        require_auth=False
    )


def book_class(client_id: str, class_id: int):
    body = {
        "ClientId": client_id,
        "ClassId": class_id,
        "Test": False
    }
    return mb_request(
        method="POST",
        endpoint="/class/addclienttoclass",
        body=body,
        require_auth=True
    )


# ============================================================
# 6) ATTENDANCE ENDPOINTS
# ============================================================
def get_attendance_history(client_id: str):
    return mb_request(
        method="GET",
        endpoint="/attendance/getattendancehistory",
        params={"ClientId": client_id},
        require_auth=True
    )
# ============================================================
# 7) PHASE 1 - NEW CLIENT ENDPOINTS
# ============================================================
def get_clients(search_text=None, limit=100, offset=0):
    """Get list of all clients with optional search and pagination."""
    params = {
        "SearchText": search_text,
        "Limit": limit,
        "Offset": offset
    }
    return mb_request(
        method="GET",
        endpoint="/client/clients",
        params=params,
        require_auth=True
    )


def update_client(client_id: str, client_data: dict):
    """Update existing client information."""
    body = {
        "ClientId": client_id,
        **client_data
    }
    return mb_request(
        method="POST",
        endpoint="/client/updateclient",
        body=body,
        require_auth=True
    )


# ============================================================
# 8) PHASE 1 - NEW CLASS ENDPOINTS
# ============================================================
def remove_client_from_class(client_id: str, class_id: int, late_cancel: bool = False):
    """Remove/cancel client from a class."""
    body = {
        "ClientId": client_id,
        "ClassId": class_id,
        "LateCancel": late_cancel,
        "Test": False
    }
    return mb_request(
        method="POST",
        endpoint="/class/removeclientfromclass",
        body=body,
        require_auth=True
    )


# ============================================================
# 9) PHASE 1 - NEW APPOINTMENT ENDPOINTS
# ============================================================
def get_active_session_times(start_date=None, end_date=None, location_id=None, staff_id=None):
    """Get available appointment time slots."""
    params = {
        "StartDate": start_date,
        "EndDate": end_date,
        "LocationId": location_id,
        "StaffId": staff_id
    }
    return mb_request(
        method="GET",
        endpoint="/appointment/activesessiontimes",
        params=params,
        require_auth=True
    )


def add_appointment(client_id: str, session_type_id: int, location_id: int, staff_id: int, start_datetime: str):
    """Book an appointment for a client."""
    body = {
        "ClientId": client_id,
        "SessionTypeId": session_type_id,
        "LocationId": location_id,
        "StaffId": staff_id,
        "StartDateTime": start_datetime,
        "Test": False
    }
    return mb_request(
        method="POST",
        endpoint="/appointment/addappointment",
        body=body,
        require_auth=True
    )

# ============================================================
# 10) SALE ENDPOINTS - GET OPERATIONS
# ============================================================
def get_services(location_id=None, session_type_id=None, limit=100, offset=0):
    """Get available services/class passes."""
    params = {
        "LocationId": location_id,
        "SessionTypeId": session_type_id,
        "Limit": limit,
        "Offset": offset
    }
    return mb_request(
        method="GET",
        endpoint="/sale/services",
        params=params,
        require_auth=True
    )


def get_contracts(location_id=None, limit=100, offset=0):
    """Get available membership contracts."""
    params = {
        "LocationId": location_id,
        "Limit": limit,
        "Offset": offset
    }
    return mb_request(
        method="GET",
        endpoint="/sale/contracts",
        params=params,
        require_auth=True
    )


def get_products(location_id=None, limit=100, offset=0):
    """Get retail products."""
    params = {
        "LocationId": location_id,
        "Limit": limit,
        "Offset": offset
    }
    return mb_request(
        method="GET",
        endpoint="/sale/products",
        params=params,
        require_auth=True
    )


def get_packages(location_id=None, limit=100, offset=0):
    """Get service packages."""
    params = {
        "LocationId": location_id,
        "Limit": limit,
        "Offset": offset
    }
    return mb_request(
        method="GET",
        endpoint="/sale/packages",
        params=params,
        require_auth=True
    )


def get_sales(start_date=None, end_date=None, limit=100, offset=0):
    """Get sales/transaction history."""
    params = {
        "StartDate": start_date,
        "EndDate": end_date,
        "Limit": limit,
        "Offset": offset
    }
    return mb_request(
        method="GET",
        endpoint="/sale/sales",
        params=params,
        require_auth=True
    )


def get_accepted_card_types():
    """Get accepted payment card types."""
    return mb_request(
        method="GET",
        endpoint="/sale/acceptedcardtypes",
        require_auth=True
    )


# ============================================================
# 11) SALE ENDPOINTS - POST OPERATIONS
# ============================================================
def purchase_contract(client_id: str, contract_id: int, location_id: int, test: bool = False):
    """Purchase a contract/membership/class pass."""
    body = {
        "ClientId": client_id,
        "ContractId": contract_id,
        "LocationId": location_id,
        "Test": test
    }
    return mb_request(
        method="POST",
        endpoint="/sale/purchasecontract",
        body=body,
        require_auth=True
    )


def checkout_shopping_cart(client_id: str, items: list, payment_info: dict, test: bool = False):
    """Checkout shopping cart with payment."""
    body = {
        "ClientId": client_id,
        "Items": items,
        "PaymentInfo": payment_info,
        "Test": test
    }
    return mb_request(
        method="POST",
        endpoint="/sale/checkoutshoppingcart",
        body=body,
        require_auth=True
    )