from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Use SQLite for development
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./valuai.db')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

def get_db():
    """Database dependency for FastAPI/Flask routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
