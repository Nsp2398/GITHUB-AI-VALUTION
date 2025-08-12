from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=True, index=True)
    phone = Column(String(20), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    companies = relationship("Company", back_populates="user")
    valuations = relationship("Valuation", back_populates="user")
    file_uploads = relationship("FileUpload", back_populates="user")
    reports = relationship("Report", back_populates="user")

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_uuid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False, index=True)
    industry = Column(String(50), default='UCaaS')
    description = Column(Text)
    stage = Column(String(20), default='growth')  # idea, pre-revenue, mvp, growth, etc.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Financial metrics
    revenue = Column(Float)
    expenses = Column(Float)
    ebitda = Column(Float)
    growth_rate = Column(Float)
    profit_margin = Column(Float)
    employees = Column(Integer)
    
    # UCaaS specific metrics (PostgreSQL JSON support)
    ucaas_metrics = Column(JSON, default={
        'mrr': None,
        'arr': None,
        'arpu': None,
        'churn_rate': None,
        'cac': None,
        'ltv': None,
        'customer_count': None,
        'nrr': None  # Net Revenue Retention
    })
    
    # Valuation model data (PostgreSQL JSON support)
    valuation_inputs = Column(JSON, default={
        'team_experience': 'medium',
        'product_stage': 'market',
        'market_size': 'medium',
        'traction': 'moderate',
        'risk_factors': [],
        'competitive_advantages': []
    })
    
    # Relationships
    user = relationship("User", back_populates="companies")
    valuations = relationship("Valuation", back_populates="company")
    file_uploads = relationship("FileUpload", back_populates="company")

class Valuation(Base):
    __tablename__ = 'valuations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    valuation_uuid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    valuation_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Valuation method used
    method_used = Column(String(50), nullable=False)  # dcf, ucaas_metrics, ai_powered, etc.
    
    # Valuation results (PostgreSQL JSON support)
    valuation_results = Column(JSON, default={})
    
    # Individual method results
    dcf_value = Column(Float)
    ucaas_metrics_value = Column(Float)
    ai_powered_value = Column(Float)
    market_comparables_value = Column(Float)
    final_valuation = Column(Float)
    confidence_score = Column(Float)
    
    # Valuation parameters
    discount_rate = Column(Float)
    terminal_growth_rate = Column(Float)
    projection_years = Column(Integer, default=5)
    
    # AI recommendations (PostgreSQL JSON support)
    ai_recommendations = Column(JSON, default={})
    
    # Market data snapshot (PostgreSQL JSON support)
    market_data = Column(JSON, default={})
    
    # Report status
    report_generated = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="valuations")
    company = relationship("Company", back_populates="valuations")
    reports = relationship("Report", back_populates="valuation")

class FileUpload(Base):
    __tablename__ = 'file_uploads'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_uuid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=True)
    
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    file_type = Column(String(50))
    mime_type = Column(String(100))
    
    # Extracted data (PostgreSQL JSON support)
    extracted_data = Column(JSON, default={})
    processing_status = Column(String(20), default='pending')  # pending, processing, completed, failed
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="file_uploads")
    company = relationship("Company", back_populates="file_uploads")

class Report(Base):
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    report_uuid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    valuation_id = Column(Integer, ForeignKey('valuations.id'), nullable=False)
    
    report_type = Column(String(20), nullable=False)  # pdf, docx, png, txt
    file_path = Column(String(500))
    file_size = Column(Integer)
    
    # Report metadata (PostgreSQL JSON support) - renamed to avoid SQLAlchemy conflict
    report_metadata = Column(JSON, default={})
    
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    downloaded_at = Column(DateTime, nullable=True)
    download_count = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="reports")
    valuation = relationship("Valuation", back_populates="reports")
