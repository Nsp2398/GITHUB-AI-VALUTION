from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL with fallback to SQLite for development
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL is None:
    # Default to SQLite for development
    DATABASE_URL = 'sqlite:///./database/valuai.db'
    connect_args = {"check_same_thread": False}
elif DATABASE_URL.startswith('postgresql'):
    # PostgreSQL configuration
    connect_args = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
else:
    connect_args = {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=os.getenv('DATABASE_ECHO', 'False').lower() == 'true'
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

def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
