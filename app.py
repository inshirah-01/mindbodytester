from fastapi import FastAPI, Query
from mindbody_client import (
    issue_user_token,
    add_client,
    get_client_info,
    get_client_visits,
    get_class_schedule,
    book_class,
    get_attendance_history,
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
