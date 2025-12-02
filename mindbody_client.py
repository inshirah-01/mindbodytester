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