import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables (DATABASE_URL) from the .env file
load_dotenv()

# The Connection String:
# In Docker, 'db' refers to the service name defined in docker-compose.yml.
# Format: postgresql://user:password@hostname:port/dbname
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine:
# This is the "starting point" for any SQLAlchemy application, managing the connection pool.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory:
# Each instance of SessionLocal will be a database session. 
# autocommit/autoflush=False gives us full control over transaction boundaries.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our Database Models:
# Our 'Contact' and 'Appointment' classes will inherit from this Base.
Base = declarative_base()

def get_db():
    """
    Dependency Generator:
    Creates a new database session for each request and ensures 
    it is closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db # The session is provided to the route function (Dependency Injection)
    finally:
        db.close() # Guaranteed cleanup to prevent database connection leaks