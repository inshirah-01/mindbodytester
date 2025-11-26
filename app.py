from fastapi import FastAPI, Query
from mindbody_client import (
    fetch_clients,
    fetch_classes,
    fetch_appointments,
    add_client,
    search_clients_by_phone,  # NEW!
)

app = FastAPI(title="Mindbody CRM API")


@app.get("/clients")
def get_clients(
    client_id: str | None = Query(None),
    email: str | None = Query(None),
    phone: str | None = Query(None),
    name: str | None = Query(None),
):
    """
    Search MINDBODY clients.
    
    IMPORTANT: Mindbody's SearchText only searches FirstName, LastName, and Email.
    Phone searches require fetching all clients and filtering locally (slower).
    
    Examples:
    - /clients?client_id=100015633  → Search by ID (fastest)
    - /clients?name=John            → Search by name
    - /clients?email=john.doe       → Search by email (partial match)
    - /clients?phone=5551234567     → Search by phone (slower, fetches all clients)
    """

    # Search by client ID (most efficient)
    if client_id:
        return fetch_clients(client_id=client_id)

    # Search by phone (special handling - fetches all and filters)
    if phone:
        return search_clients_by_phone(phone)

    # Search by name or email using SearchText
    search_text = email or name
    if search_text:
        return fetch_clients(search_text=search_text)

    # No parameters - return first 100 clients
    return fetch_clients()


# ----------------------------
# 2. CLASSES ENDPOINT
# ----------------------------
@app.get("/classes")
def get_classes():
    """
    Fetch class list from MINDBODY.
    Example:
    /classes
    """
    return fetch_classes()


# ----------------------------
# 3. APPOINTMENTS ENDPOINT
# ----------------------------
@app.get("/appointments")
def get_appointments(
    staff_id: str | None = Query(None),
    from_date: str | None = Query(None),
    to_date: str | None = Query(None)
):
    """
    Fetch appointments from MINDBODY.
    Optional:
    - staff_id
    - from_date (YYYY-MM-DD)
    - to_date (YYYY-MM-DD)

    Example:
    /appointments?staff_id=1
    /appointments?from_date=2024-01-01&to_date=2024-01-31
    """
    return fetch_appointments(staff_id, from_date, to_date)


# ----------------------------
# 4. ADD CLIENT ENDPOINT
# ----------------------------
@app.post("/clients/add")
def add_new_client(
    first_name: str = Query(...),
    last_name: str = Query(...),
    email: str = Query(...),
    phone: str = Query(...),
    address: str = Query("123 Main St"),
    city: str = Query("San Luis Obispo"),
    state: str = Query("CA"),
    postal_code: str = Query("93401"),
    birth_date: str = Query("1990-01-01"),
    referred_by: str = Query("Website"),
    test_mode: bool = Query(True)
):
    """
    Add a new client via API
    
    Example:
    POST /clients/add?first_name=Mike&last_name=Test&email=mike@test.com&phone=5559999999&test_mode=true
    """
    return add_client(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        address=address,
        city=city,
        state=state,
        postal_code=postal_code,
        birth_date=birth_date,
        referred_by=referred_by,
        test_mode=test_mode
    )