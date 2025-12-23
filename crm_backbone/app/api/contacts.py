from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.db.database import get_db
from ..core.security import get_current_tenant_id
from ..models.core_models import Contact

router = APIRouter(prefix="/contacts", tags=["Contacts"])

# Define a Schema for the Request Body
class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None

@router.get("/")
def get_contacts(
    email: str = Query(None),
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_current_tenant_id)
):
    query = db.query(Contact).filter(Contact.tenant_id == tenant_id)
    if email:
        query = query.filter(Contact.email == email)
    return query.all()

@router.post("/")
def create_contact(
    contact_data: ContactCreate, # FastAPI now looks in the JSON body
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_current_tenant_id)
):
    new_contact = Contact(
        first_name=contact_data.first_name, 
        last_name=contact_data.last_name, 
        email=contact_data.email, 
        tenant_id=tenant_id
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact) # Ensures the ID is populated in the return object
    return new_contact