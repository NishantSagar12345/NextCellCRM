from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.db.database import get_db
from ..core.security import get_current_tenant_id
from ..models.core_models import Contact

# Initialize the router for Contact management
router = APIRouter(prefix="/contacts", tags=["Contacts"])

# Pydantic Schema: Defines the structure and validation for incoming JSON data
class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None  # EmailStr provides automatic format validation
    phone: Optional[str] = None

@router.get("/")
def get_contacts(
    email: str = Query(None, description="Filter contacts by email address"), # Optional search parameter
    db: Session = Depends(get_db),                                            # Injects DB session
    tenant_id: str = Depends(get_current_tenant_id)                           # Injects verified tenant ID
):
    """
    Retrieve contacts with strict tenant isolation.
    If an email is provided, it filters within that tenant's data scope only.
    """
    # Base query: Always filtered by tenant_id to prevent data leakage between clients
    query = db.query(Contact).filter(Contact.tenant_id == tenant_id)
    
    # Optional search filtering logic
    if email:
        query = query.filter(Contact.email == email)
        
    return query.all()

@router.post("/")
def create_contact(
    contact_data: ContactCreate,                    # FastAPI parses the request body automatically
    db: Session = Depends(get_db),                  # Injects DB session
    tenant_id: str = Depends(get_current_tenant_id) # Injects verified tenant ID
):
    """
    Create a new contact record.
    The tenant_id is automatically assigned from the JWT token for security.
    """
    # Instantiate the SQLAlchemy model with validated data and the secure tenant_id
    new_contact = Contact(
        first_name=contact_data.first_name, 
        last_name=contact_data.last_name, 
        email=contact_data.email, 
        tenant_id=tenant_id                        # Mandatory: Bind the record to the tenant
    )
    
    db.add(new_contact)                             # Prepare the transaction
    db.commit()                                     # Finalize the transaction in the DB
    db.refresh(new_contact)                         # Reload the object to retrieve the generated ID
    
    return new_contact                              # Return the newly created contact as a JSON response