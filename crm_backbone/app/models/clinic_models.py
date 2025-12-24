from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.database import Base

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), index=True, nullable=False) # 
    patient_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"))
    practitioner_name = Column(String)
    appointment_time = Column(DateTime)
    status = Column(String) # e.g., Scheduled, Completed   