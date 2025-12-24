from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.db.database import get_db
from app.core.security import get_current_tenant_id
from app.models.clinic_models import Appointment

# Initialize the router for clinic-specific appointment endpoints
router = APIRouter(prefix="/appointments", tags=["Clinics"])

# Pydantic Schema: Validates the incoming JSON request body for creating an appointment
class AppointmentCreate(BaseModel):
    patient_id: str
    practitioner_name: str
    treatment_type: Optional[str] = "Consultation" # Default value if not provided
    appointment_time: datetime
    status: str = "Scheduled"

@router.get("/")
def get_appointments(
    db: Session = Depends(get_db),                  # Injects the database session
    tenant_id: str = Depends(get_current_tenant_id) # Injects the tenant ID extracted from the JWT token
):
    """
    Fetch all appointments for the authenticated tenant.
    Mandatory tenant isolation ensures a user only sees their own clinic's data.
    """
    return db.query(Appointment).filter(Appointment.tenant_id == tenant_id).all()

@router.post("/")
def create_appointment(
    appointment_data: AppointmentCreate,            # FastAPI automatically parses and validates JSON against the schema
    db: Session = Depends(get_db),                  # Injects database session
    tenant_id: str = Depends(get_current_tenant_id) # Injects verified tenant ID
):
    """
    Create a new appointment and bind it to the current tenant.
    """
    # Initialize the SQLAlchemy model instance with data from the request and the injected tenant_id
    new_app = Appointment(
        patient_id=appointment_data.patient_id,
        practitioner_name=appointment_data.practitioner_name,
        treatment_type=appointment_data.treatment_type,
        appointment_time=appointment_data.appointment_time, 
        status=appointment_data.status,
        tenant_id=tenant_id                        # Critical: Ensures data ownership
    )
    
    db.add(new_app)                                # Stages the new record for insertion
    db.commit()                                     # Persists the record to the database
    db.refresh(new_app)                            # Reloads the object to include database-generated fields like 'id'
    
    return new_app                                  # Returns the created record as JSON