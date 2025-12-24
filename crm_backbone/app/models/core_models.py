from sqlalchemy import Column, String, ForeignKey, Float, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.database import Base

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), index=True, nullable=False) 
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, index=True)
    phone = Column(String)

class Deal(Base):
    __tablename__ = "deals"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    title = Column(String, nullable=False)
    amount = Column(Float)
    stage = Column(String) # e.g., Qualification, Proposal, Closed 
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"))

class Activity(Base):
    __tablename__ = "activities"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    activity_type = Column(String) # e.g., 'Note', 'Task', 'Meeting' 
    description = Column(Text)

 