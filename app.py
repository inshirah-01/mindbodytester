from fastapi import FastAPI, Query
from mindbody_client import (
    fetch_clients,
    fetch_classes,
    fetch_appointments,
    add_client,
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
    You can use any of:
    - /clients?client_id=123
    - /clients?email=test@example.com
    - /clients?phone=9999999999
    - /clients?name=John
    """

    # MINDBODY: client_id uses ClientIds
    if client_id:
        return fetch_clients(client_id=client_id)

    # MINDBODY: SearchText handles email, phone, name
    search_text = email or phone or name
    if search_text:
        return fetch_clients(search_text=search_text)

    return {"error": "Please pass at least one query parameter"}


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