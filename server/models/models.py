from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=True)
    phone = Column(String(20), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    industry = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Financial metrics
    revenue = Column(Float)
    ebitda = Column(Float)
    growth_rate = Column(Float)
    profit_margin = Column(Float)
    
    # UCaaS specific metrics
    mrr = Column(Float)  # Monthly Recurring Revenue
    arpu = Column(Float)  # Average Revenue Per User
    churn_rate = Column(Float)
    cac = Column(Float)  # Customer Acquisition Cost
    ltv = Column(Float)  # Lifetime Value

class Valuation(Base):
    __tablename__ = 'valuations'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, nullable=False)
    valuation_date = Column(DateTime, default=datetime.utcnow)
    
    # Valuation results
    dcf_value = Column(Float)
    market_value = Column(Float)
    final_value = Column(Float)
    
    # Valuation parameters
    discount_rate = Column(Float)
    terminal_growth_rate = Column(Float)
    projection_years = Column(Integer)
    
    # AI recommendations
    ai_confidence_score = Column(Float)
    ai_recommendations = Column(Text)
    
    # Report status
    report_generated = Column(Boolean, default=False)
    report_url = Column(String(255))
