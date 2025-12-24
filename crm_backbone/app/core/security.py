from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt, os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configuration for JWT signing and verification
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# This tells FastAPI to look for a "Bearer <token>" in the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_tenant_id(token: str = Depends(oauth2_scheme)) -> str:
    """
    Dependency function to verify the JWT and extract the tenant_id.
    This acts as a gatekeeper for all protected routes.
    """
    try:
        # Decode the token using the secret key and designated algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract the tenant_id claim from the JWT payload
        tenant_id: str = payload.get("tenant_id")
        
        # If the token is valid but doesn't contain a tenant_id, deny access
        if not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid tenant context"
            )
            
        # Return the tenant_id to be used in database filters (Isolation)
        return tenant_id

    except jwt.PyJWTError:
        # If the token is expired, tampered with, or incorrectly signed, raise a 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )