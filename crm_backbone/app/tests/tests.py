import pytest
from fastapi.testclient import TestClient
from app.main import app
import jwt, os
import uuid
from dotenv import load_dotenv

# Load environment variables for JWT signing
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Initialize the FastAPI TestClient to simulate API requests without a real server
client = TestClient(app)

def create_token(tenant_id: str):
    """Utility to generate a signed JWT for a specific tenant."""
    return jwt.encode({"tenant_id": tenant_id}, SECRET_KEY, algorithm=ALGORITHM)

# Static UUIDs for consistent tenant testing
TENANT_A_ID = "550e8400-e29b-41d4-a716-446655440000"
TENANT_B_ID = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"

# --- TEST 1: Multi-Tenant Isolation ---
def test_tenant_isolation():
    """
    Critical Security Test: Ensures Tenant B cannot access Tenant A's data.
    This validates that the 'get_current_tenant_id' dependency and DB filters work.
    """
    token_a = create_token(TENANT_A_ID)
    token_b = create_token(TENANT_B_ID)

    # Action: Tenant A creates a contact
    client.post("/contacts/", 
                json={"first_name": "John", "last_name": "Doe", "email": "john@a.com"},
                headers={"Authorization": f"Bearer {token_a}"})

    # Verification: Tenant B attempts to list contacts
    response = client.get("/contacts/", headers={"Authorization": f"Bearer {token_b}"})
    
    # Assert: Tenant B receives an empty list, confirming data is isolated
    assert response.status_code == 200
    assert len(response.json()) == 0

# --- TEST 2: Search & Query Parameters ---
def test_search_contact():
    """
    Validates that the GET /contacts/ endpoint correctly filters results by email.
    """
    token = create_token(TENANT_A_ID)
    
    # 1. Setup: Create the contact to be searched
    create_resp = client.post(
        "/contacts/",
        json={"first_name": "Alice", "last_name": "Smith", "email": "alice@test.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_resp.status_code == 200

    # 2. Action: Search for the contact by email query parameter
    response = client.get(
        "/contacts/?email=alice@test.com", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Verification: Ensure only the matching contact is returned
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["email"] == "alice@test.com"

# --- TEST 3: Component Linking (Clinic Logic) ---
def test_clinic_appointment_flow():
    """
    Ensures that the Contact creation returns a valid ID required for Appointments.
    """
    token = create_token(str(uuid.uuid4()))
    
    p_resp = client.post(
        "/contacts/",
        json={"first_name": "Bob", "last_name": "Patient", "email": "bob@clinic.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert p_resp.status_code == 200
    patient_id = p_resp.json()["id"]
    assert patient_id is not None

# --- TEST 4: End-to-End Clinic Workflow ---
def test_clinic_main_flow():
    """
    Simulates a real-world clinic scenario:
    1. Register a Patient (Core Module)
    2. Book an Appointment (Vertical Module) linked to that Patient.
    3. Verify relational integrity within the tenant scope.
    """
    clinic_tenant = str(uuid.uuid4())
    token = create_token(clinic_tenant)
    headers = {"Authorization": f"Bearer {token}"}

    # Step 1: Create a Patient using the Shared Core Contact model
    patient_data = {"first_name": "Nishant", "last_name": "Pandey", "email": "nishant@example.com"}
    p_resp = client.post("/contacts/", json=patient_data, headers=headers)
    assert p_resp.status_code == 200
    patient_id = p_resp.json()["id"]

    # Step 2: Schedule an Appointment linking the 'Clinic' logic to the 'Core' patient
    appointment_data = {
        "patient_id": patient_id,
        "practitioner_name": "Dr. Smith",
        "treatment_type": "Dental Checkup",
        "appointment_time": "2025-12-25T10:00:00",
        "status": "Scheduled"
    }
    a_resp = client.post("/appointments/", json=appointment_data, headers=headers)
    assert a_resp.status_code == 200
    
    # Step 3: Final Verification - Retrieve and validate the appointment record
    get_resp = client.get("/appointments/", headers=headers)
    appointments = get_resp.json()
    
    assert len(appointments) > 0
    assert appointments[0]["practitioner_name"] == "Dr. Smith"
    assert appointments[0]["patient_id"] == patient_id