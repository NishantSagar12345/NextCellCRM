from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt,os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_tenant_id(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        tenant_id: str = payload.get("tenant_id")
        if not tenant_id:
            raise HTTPException(status_code=401, detail="Invalid tenant context")
        return tenant_id
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )