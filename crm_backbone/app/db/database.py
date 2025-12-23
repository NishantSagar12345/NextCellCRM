import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Check for 'DATABASE_URL' environment variable (used by Docker)
# 2. Fallback to 'db' instead of 'localhost' for container networking
# 3. Use 'postgresql://' instead of 'postgres://' for SQLAlchemy 2.0 compatibility
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://user:password@db:5432/crm_db"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()