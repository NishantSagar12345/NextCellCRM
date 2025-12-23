from fastapi import FastAPI, Depends
from app.db.database import engine, Base
from app.api import contacts, clinics # Import the new industry and core modules
from app.core.security import get_current_tenant_id

# Automatically create the database tables on startup [cite: 74]
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NexCell CRM",
    description="Multi-tenant CRM with shared core and industry modules [cite: 12]",
    version="1.0.0"
)

# --- REGISTER ROUTERS ---
# This links the files you created in Hour 2 to the main app [cite: 82]
app.include_router(contacts.router)
app.include_router(clinics.router)

@app.get("/")
def health_check():
    """Confirms the backbone is running."""
    return {"status": "online", "message": "NexCell CRM Core Active"}

@app.post("/auth/login")
def login():
    """
    Simple JWT login for the challenge[cite: 43].
    In a production app, this would verify credentials against the DB.
    """
    # Example token containing tenant context
    return {
        "access_token": "mock_token_with_tenant_id", 
        "token_type": "bearer",
        "note": "Use this token in the 'Authorize' button in Swagger docs."
    }

@app.get("/tenant-check")
def verify_isolation(tenant_id: str = Depends(get_current_tenant_id)):
    """Non-negotiable: Proves the system identifies the tenant from the token[cite: 55]."""
    return {"active_tenant_id": tenant_id}