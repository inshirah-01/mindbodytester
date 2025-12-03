from fastapi import FastAPI, Query
from mindbody_client import (
    issue_user_token,
    add_client,
    get_client_info,
    get_client_visits,
    get_class_schedule,
    book_class,
    get_attendance_history,
    get_clients,
    update_client,
    remove_client_from_class,
    get_active_session_times,
    add_appointment,
    get_services,
    get_contracts,
    get_products,
    get_packages,
    get_sales,
    get_accepted_card_types,
    purchase_contract,
    checkout_shopping_cart,
)

app = FastAPI(title="Mindbody Integration API")


# ============================================================
# 1) MANUAL TOKEN GENERATION (optional)
# ============================================================
@app.post("/token")
def generate_token(username: str, password: str):
    """
    Manually issue a MINDBODY staff token.
    Only needed if you want to test manually.
    """
    return issue_user_token(username, password)


# ============================================================
# 2) ADD CLIENT
# ============================================================
@app.post("/clients/add")
def create_new_client(client: dict):
    """
    Add a new client to MINDBODY sandbox.
    Requires staff token (auto-generated internally).
    """
    return add_client(client)


# ============================================================
# 3) GET CLIENT FULL INFO
# ============================================================
@app.get("/clients/{client_id}")
def client_details(client_id: str):
    """
    Fetch full details about a client.
    Includes demographics, alerts, locations, history, etc.
    """
    return get_client_info(client_id)


# ============================================================
# 4) GET CLIENT VISIT HISTORY
# ============================================================
@app.get("/clients/{client_id}/visits")
def client_visits(client_id: str):
    """
    Get client's visit history (arrivals, classes, attendance).
    """
    return get_client_visits(client_id)


# ============================================================
# 5) GET CLASS SCHEDULE
# ============================================================
@app.get("/classes")
def fetch_classes(
    start_date: str = Query(None, description="YYYY-MM-DD"),
    end_date: str = Query(None, description="YYYY-MM-DD")
):
    """
    Fetch class schedule between optional dates.
    MINDBODY sandbox (-99) already contains sample classes.
    """
    return get_class_schedule(start_date, end_date)


# ============================================================
# 6) BOOK A CLASS
# ============================================================
@app.post("/classes/book")
def book_class_for_client(client_id: str, class_id: int):
    """
    Book a client into a class.
    Requires staff token (auto-handled).
    """
    return book_class(client_id, class_id)


# ============================================================
# 7) ATTENDANCE HISTORY
# ============================================================
@app.get("/clients/{client_id}/attendance")
def attendance_history(client_id: str):
    """
    Fetch attendance history for a client.
    """
    return get_attendance_history(client_id)

# ============================================================
# 8) PHASE 1 - GET ALL CLIENTS
# ============================================================
@app.get("/clients")
def list_clients(
    search_text: str = Query(None, description="Search by name, email, or phone"),
    limit: int = Query(100, description="Number of results to return"),
    offset: int = Query(0, description="Number of results to skip")
):
    """
    Get list of all clients with optional search and pagination.
    Search by name, email, phone number, etc.
    """
    return get_clients(search_text, limit, offset)


# ============================================================
# 9) PHASE 1 - UPDATE CLIENT
# ============================================================
@app.put("/clients/{client_id}")
def update_existing_client(client_id: str, client_data: dict):
    """
    Update existing client information.
    Provide only the fields you want to update.
    """
    return update_client(client_id, client_data)


# ============================================================
# 10) PHASE 1 - REMOVE CLIENT FROM CLASS
# ============================================================
@app.delete("/classes/booking")
def cancel_class_booking(
    client_id: str = Query(..., description="Client ID"),
    class_id: int = Query(..., description="Class ID"),
    late_cancel: bool = Query(False, description="Mark as late cancellation")
):
    """
    Remove/cancel a client's booking from a class.
    Set late_cancel=true if cancelling after deadline.
    """
    return remove_client_from_class(client_id, class_id, late_cancel)


# ============================================================
# 11) PHASE 1 - GET AVAILABLE APPOINTMENT SLOTS
# ============================================================
@app.get("/appointments/slots")
def available_appointment_slots(
    start_date: str = Query(..., description="YYYY-MM-DD"),
    end_date: str = Query(None, description="YYYY-MM-DD"),
    location_id: int = Query(None, description="Filter by location"),
    staff_id: int = Query(None, description="Filter by staff member")
):
    """
    Get available appointment time slots.
    Required: start_date
    Optional: end_date, location_id, staff_id
    """
    return get_active_session_times(start_date, end_date, location_id, staff_id)


# ============================================================
# 12) PHASE 1 - BOOK APPOINTMENT
# ============================================================
@app.post("/appointments/book")
def book_appointment(
    client_id: str,
    session_type_id: int,
    location_id: int,
    staff_id: int,
    start_datetime: str = Query(..., description="YYYY-MM-DDTHH:MM:SS")
):
    """
    Book an appointment for a client.
    start_datetime format: 2025-12-03T14:30:00
    """
    return add_appointment(client_id, session_type_id, location_id, staff_id, start_datetime)

# ============================================================
# 13) SALES - GET ENDPOINT (Mega Endpoint for Viewing)
# ============================================================
@app.get("/sale")
def handle_sales_get(
    action: str = Query(..., description="Action: services, contracts, products, packages, sales, cardtypes"),
    location_id: int = Query(None, description="Filter by location"),
    session_type_id: int = Query(None, description="Filter by session type (for services only)"),
    start_date: str = Query(None, description="Start date for sales history (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End date for sales history (YYYY-MM-DD)"),
    limit: int = Query(100, description="Results limit"),
    offset: int = Query(0, description="Results offset")
):
    """
    Mega GET endpoint for all sales browsing operations.
    
    Examples:
    - /sale?action=services → View class passes
    - /sale?action=contracts → View memberships
    - /sale?action=products → View retail products
    - /sale?action=packages → View service packages
    - /sale?action=sales&start_date=2025-12-01 → View transaction history
    - /sale?action=cardtypes → View accepted payment methods
    """
    
    if action == "services":
        return get_services(location_id, session_type_id, limit, offset)
    
    elif action == "contracts":
        return get_contracts(location_id, limit, offset)
    
    elif action == "products":
        return get_products(location_id, limit, offset)
    
    elif action == "packages":
        return get_packages(location_id, limit, offset)
    
    elif action == "sales":
        return get_sales(start_date, end_date, limit, offset)
    
    elif action == "cardtypes":
        return get_accepted_card_types()
    
    else:
        return {"error": "Invalid action. Use: services, contracts, products, packages, sales, or cardtypes"}


# ============================================================
# 14) SALES - POST ENDPOINT (Mega Endpoint for Purchasing)
# ============================================================
@app.post("/sale")
def handle_sales_post(
    action: str = Query(..., description="Action: purchase_contract or checkout"),
    data: dict = None
):
    """
    Mega POST endpoint for all sales/purchase operations.
    
    Examples:
    
    1) Purchase a contract/pass:
       POST /sale?action=purchase_contract
       Body: {
         "client_id": "100015630",
         "contract_id": 123,
         "location_id": 1,
         "test": false
       }
    
    2) Checkout shopping cart:
       POST /sale?action=checkout
       Body: {
         "client_id": "100015630",
         "items": [
           {"Type": "Service", "Id": 123, "Quantity": 1},
           {"Type": "Product", "Id": 456, "Quantity": 2}
         ],
         "payment_info": {
           "Amount": 100.00,
           "Method": "CreditCard",
           "CardNumber": "4111111111111111",
           "ExpMonth": "12",
           "ExpYear": "2026"
         },
         "test": false
       }
    """
    
    if not data:
        return {"error": "Request body required"}
    
    if action == "purchase_contract":
        return purchase_contract(
            client_id=data.get("client_id"),
            contract_id=data.get("contract_id"),
            location_id=data.get("location_id"),
            test=data.get("test", False)
        )
    
    elif action == "checkout":
        return checkout_shopping_cart(
            client_id=data.get("client_id"),
            items=data.get("items"),
            payment_info=data.get("payment_info"),
            test=data.get("test", False)
        )
    
    else:
        return {"error": "Invalid action. Use: purchase_contract or checkout"}