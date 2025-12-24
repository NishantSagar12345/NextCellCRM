from sqlalchemy import Column, String, ForeignKey, Float, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.database import Base

# --- CORE CRM MODELS ---

class Contact(Base):
    """
    The central entity for the CRM. 
    Serves as the base for Patients, Leads, or Customers across different modules.
    """
    __tablename__ = "contacts"
    
    # UUIDs ensure global uniqueness and prevent ID guessing attacks
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Mandatory for multi-tenancy: All queries filter by this indexed column
    tenant_id = Column(UUID(as_uuid=True), index=True, nullable=False) 
    
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    
    # Indexed email for high-performance searching/lookups
    email = Column(String, index=True)
    phone = Column(String)

class Deal(Base):
    """
    Represents a sales opportunity.
    Linked to a Contact to track potential revenue per person/lead.
    """
    __tablename__ = "deals"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    
    title = Column(String, nullable=False)
    amount = Column(Float)
    
    # Tracking the sales pipeline status (e.g., 'Discovery', 'Negotiation', 'Won')
    stage = Column(String) 
    
    # Relational link to the Contact model
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"))

class Activity(Base):
    """
    A generic log for interactions (Notes, Tasks, Meetings).
    Essential for maintaining a history of engagement within each tenant's workspace.
    """
    __tablename__ = "activities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    
    # Flexible type field to differentiate between a Note, Task, or Call Log
    activity_type = Column(String) 
    description = Column(Text) # 'Text' used for longer, unstructured content