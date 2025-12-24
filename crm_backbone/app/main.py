from fastapi import FastAPI, Depends
from app.db.database import engine, Base
from app.api import contacts, clinics # Industry-specific and core module imports
from app.core.security import get_current_tenant_id

# Database Initialization: 
# Automatically creates all tables defined in your models on application startup.
# In a larger production app, you would use 'Alembic' for migrations.
Base.metadata.create_all(bind=engine)

# FastAPI App Configuration:
# Defines the metadata for the interactive Swagger documentation (/docs).
app = FastAPI(
    title="NexCell CRM",
    description="Multi-tenant CRM with shared core and industry modules",
    version="1.0.0"
)

# --- REGISTER ROUTERS ---
# Each router adds its own endpoints (e.g., /contacts and /appointments) to the app.
app.include_router(contacts.router)
app.include_router(clinics.router)

@app.get("/")
def health_check():
    """
    Root Endpoint:
    Used for monitoring and confirming the API is successfully deployed.
    """
    return {"status": "online", "message": "NexCell CRM Core Active"}

@app.post("/auth/login")
def login():
    """
    Mock Authentication Endpoint:
    Simulates the generation of a JWT for testing and challenge purposes.
    Provides the 'Bearer' token required for protected routes.
    """
    return {
        "access_token": "mock_token_with_tenant_id", 
        "token_type": "bearer",
        "note": "Use this token in the 'Authorize' button in Swagger docs."
    }

@app.get("/tenant-check")
def verify_isolation(tenant_id: str = Depends(get_current_tenant_id)):
    """
    Security Verification:
    Demonstrates the system's ability to extract and verify 
    the current tenant context from the request header.
    """
    return {"active_tenant_id": tenant_id}