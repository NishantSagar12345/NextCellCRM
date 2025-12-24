from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.database import Base

class Appointment(Base):
    """
    SQLAlchemy model representing a clinical appointment.
    This model supports multi-tenancy through a mandatory tenant_id field.
    """
    __tablename__ = "appointments"

    # Primary Key: Uses a UUID to ensure global uniqueness across distributed environments
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Multi-Tenant Identifier: Indexed for performance, ensures data isolation between clinics
    tenant_id = Column(UUID(as_uuid=True), index=True, nullable=False)

    # Foreign Key Relationship: Links the appointment to a specific contact (patient)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"))

    # Practitioner details for the session
    practitioner_name = Column(String)

    # Type of service provided (e.g., Consultation, Dental Checkup)
    treatment_type = Column(String) 

    # Timestamp for the scheduled appointment
    appointment_time = Column(DateTime)

    # Current lifecycle state of the appointment (e.g., Scheduled, Completed, Cancelled)
    status = Column(String)