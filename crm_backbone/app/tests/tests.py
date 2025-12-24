import pytest
from fastapi.testclient import TestClient
from app.main import app
import jwt,os
import uuid
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
client = TestClient(app)

def create_token(tenant_id: str):
    return jwt.encode({"tenant_id": tenant_id}, SECRET_KEY, algorithm=ALGORITHM)

TENANT_A_ID = "550e8400-e29b-41d4-a716-446655440000"
TENANT_B_ID = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
# TEST 1: Prove Tenant Isolation (Non-negotiable) [cite: 55, 56]
def test_tenant_isolation():
    token_a = create_token(TENANT_A_ID)
    token_b = create_token(TENANT_B_ID)
    # Tenant A creates a contact
    client.post("/contacts/", 
                json={"first_name": "John", "last_name": "Doe", "email": "john@a.com"},
                headers={"Authorization": f"Bearer {token_a}"})

    # Tenant B tries to list contacts
    response = client.get("/contacts/", headers={"Authorization": f"Bearer {token_b}"})
    
    # Assert Tenant B gets an empty list (cannot see Tenant A's data) 
    assert response.status_code == 200
    assert len(response.json()) == 0

# TEST 2: Search/Filter functionality [cite: 49]
def test_search_contact():
    token = create_token(TENANT_A_ID)
    
    # 1. Create the contact first
    create_resp = client.post(
        "/contacts/",
        json={"first_name": "Alice", "last_name": "Smith", "email": "alice@test.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_resp.status_code == 200, f"Setup failed: {create_resp.text}"

    # 2. Search for the contact
    response = client.get(
        "/contacts/?email=alice@test.com", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0, "Search returned no results"
    assert data[0]["email"] == "alice@test.com"

def test_clinic_appointment_flow():
    token = create_token(str(uuid.uuid4()))
    
    # Create Patient
    p_resp = client.post(
        "/contacts/",
        json={"first_name": "Bob", "last_name": "Patient", "email": "bob@clinic.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # If this fails, the KeyError 'id' occurs. Check the status:
    assert p_resp.status_code == 200, f"Contact creation failed: {p_resp.text}"
    
    patient_id = p_resp.json()["id"]
    assert patient_id is not None


def test_clinic_main_flow():
    # 1. Setup - Create a unique tenant for this flow
    clinic_tenant = str(uuid.uuid4())
    token = create_token(clinic_tenant)
    headers = {"Authorization": f"Bearer {token}"}

    # 2. STEP ONE: Create a Patient (using the Shared Core Contact model)
    patient_data = {
        "first_name": "Nishant",
        "last_name": "Pandey",
        "email": "nishant@example.com"
    }
    p_resp = client.post("/contacts/", json=patient_data, headers=headers)
    assert p_resp.status_code == 200
    patient_id = p_resp.json()["id"]

    # 3. STEP TWO: Schedule an Appointment (using the Vertical Clinic model)
    # This links the 'Clinic' logic to the 'Core' logic via the patient_id
    appointment_data = {
        "patient_id": patient_id,
        "practitioner_name": "Dr. Smith",
        "treatment_type": "Dental Checkup",
        "appointment_time": "2025-12-25T10:00:00",
        "status": "Scheduled"
    }
    a_resp = client.post("/appointments/", json=appointment_data, headers=headers)
    assert a_resp.status_code == 200
    
    # 4. STEP THREE: Verify the data is correctly saved and isolated
    get_resp = client.get("/appointments/", headers=headers)
    appointments = get_resp.json()
    
    assert len(appointments) > 0
    assert appointments[0]["practitioner_name"] == "Dr. Smith"
    assert appointments[0]["patient_id"] == patient_id