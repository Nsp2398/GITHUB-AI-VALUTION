from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

# Import the base from the main models to ensure table inheritance
from models.models import Base

class ValuationAnalytics(Base):
    """Track detailed analytics for each valuation"""
    __tablename__ = 'valuation_analytics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    valuation_id = Column(Integer, ForeignKey('valuations.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Metric tracking
    metric_name = Column(String(100), nullable=False)  # 'revenue_multiple', 'ltv_cac_ratio', etc.
    metric_value = Column(Float)
    industry_benchmark = Column(Float)
    percentile_rank = Column(Float)  # Where this company ranks (0-100)
    
    # Metadata
    calculated_at = Column(DateTime, default=datetime.utcnow)
    data_source = Column(String(50))  # 'user_input', 'api_integration', 'calculated'
    
    # Relationships
    valuation = relationship("Valuation", back_populates="analytics")
    company = relationship("Company", back_populates="analytics")
    user = relationship("User", back_populates="analytics")

class MarketBenchmarks(Base):
    """Industry benchmarks for comparison"""
    __tablename__ = 'market_benchmarks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    industry = Column(String(50), nullable=False, index=True)
    metric_name = Column(String(100), nullable=False)
    
    # Statistical values
    avg_value = Column(Float)
    median_value = Column(Float)
    p25_value = Column(Float)  # 25th percentile
    p75_value = Column(Float)  # 75th percentile
    p90_value = Column(Float)  # 90th percentile
    
    # Metadata
    sample_size = Column(Integer)
    last_updated = Column(DateTime, default=datetime.utcnow)
    data_source = Column(String(100))
    
    # Composite index for fast lookups
    __table_args__ = (
        Index('idx_industry_metric', 'industry', 'metric_name'),
    )

class CompanyMetricsHistory(Base):
    """Track changes in company metrics over time"""
    __tablename__ = 'company_metrics_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    # Snapshot data
    snapshot_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    revenue = Column(Float)
    growth_rate = Column(Float)
    customer_count = Column(Integer)
    churn_rate = Column(Float)
    ltv = Column(Float)
    cac = Column(Float)
    
    # Full metrics snapshot
    metrics_snapshot = Column(JSON)
    
    # Change tracking
    change_reason = Column(String(100))  # 'quarterly_update', 'data_correction', etc.
    changed_by = Column(Integer, ForeignKey('users.id'))
    
    # Relationships
    company = relationship("Company", back_populates="metrics_history")

class AIModelPerformance(Base):
    """Track AI model accuracy and performance"""
    __tablename__ = 'ai_model_performance'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_version = Column(String(50), nullable=False)
    valuation_id = Column(Integer, ForeignKey('valuations.id'))
    
    # Predictions
    predicted_value = Column(Float)
    confidence_score = Column(Float)
    
    # Actual outcomes (filled in later)
    actual_value = Column(Float, nullable=True)
    accuracy_score = Column(Float, nullable=True)
    
    # Model details
    model_inputs = Column(JSON)  # What data was used
    prediction_date = Column(DateTime, default=datetime.utcnow)
    evaluation_date = Column(DateTime, nullable=True)
    
    # Relationships
    valuation = relationship("Valuation", back_populates="ai_performance")

class UserActivity(Base):
    """Track user engagement and activity"""
    __tablename__ = 'user_activity'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Activity details
    activity_type = Column(String(50), nullable=False)  # 'valuation_created', 'report_downloaded', etc.
    activity_details = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # Timing
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    session_id = Column(String(100))
    
    # Relationships
    user = relationship("User", back_populates="activities")

class CompanyComparables(Base):
    """Store comparable companies data"""
    __tablename__ = 'company_comparables'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    target_company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    # Comparable company info
    comparable_name = Column(String(100), nullable=False)
    comparable_industry = Column(String(50))
    comparable_stage = Column(String(20))
    
    # Financial metrics
    comparable_revenue = Column(Float)
    comparable_valuation = Column(Float)
    comparable_multiple = Column(Float)
    
    # Similarity score
    similarity_score = Column(Float)  # 0-1 how similar to target
    
    # Metadata
    data_source = Column(String(100))
    last_updated = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    company = relationship("Company", back_populates="comparables")
