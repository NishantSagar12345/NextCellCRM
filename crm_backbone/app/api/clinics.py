from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.db.database import get_db
from app.core.security import get_current_tenant_id
from app.models.clinic_models import Appointment

router = APIRouter(prefix="/appointments", tags=["Clinics"])

#The Schema to parse the JSON Body
class AppointmentCreate(BaseModel):
    patient_id: str
    practitioner_name: str
    treatment_type: Optional[str] = "Consultation"
    appointment_time: datetime
    status: str = "Scheduled"

@router.get("/")
def get_appointments(
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_current_tenant_id)
):
    # Mandatory tenant isolation
    return db.query(Appointment).filter(Appointment.tenant_id == tenant_id).all()

@router.post("/")
def create_appointment(
    appointment_data: AppointmentCreate, # This tells FastAPI to read the JSON body
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_current_tenant_id)
):
    new_app = Appointment(
        patient_id=appointment_data.patient_id,
        practitioner_name=appointment_data.practitioner_name,
        appointment_time=appointment_data.appointment_time, 
        status=appointment_data.status,
        tenant_id=tenant_id
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app) # Populates the ID for the test response
    return new_app