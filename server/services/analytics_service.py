"""
Database Enhancement Service for ValuAI
Provides analytics, benchmarking, and advanced database operations
"""

from sqlalchemy.orm import Session
from models.enhanced_models import (
    ValuationAnalytics, MarketBenchmarks, CompanyMetricsHistory,
    AIModelPerformance, UserActivity, CompanyComparables
)
from models.models import Company, Valuation, User
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional

class AnalyticsService:
    """Service for handling analytics and benchmarking"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def create_valuation_analytics(self, valuation_id: int, company_data: Dict):
        """Create detailed analytics for a valuation"""
        try:
            valuation = self.db.query(Valuation).filter(Valuation.id == valuation_id).first()
            if not valuation:
                return None
            
            # Calculate key metrics
            revenue = float(company_data.get('revenue', 0))
            ltv = float(company_data.get('ltv', 0))
            cac = float(company_data.get('cac', 1))
            growth_rate = float(company_data.get('growthRate', 0))
            churn_rate = float(company_data.get('churnRate', 0))
            
            # Define metrics to track
            metrics = [
                {
                    'name': 'ltv_cac_ratio',
                    'value': ltv / cac if cac > 0 else 0,
                    'benchmark': 3.0,  # Industry standard
                    'percentile': self._calculate_percentile(ltv / cac if cac > 0 else 0, 3.0, 'ltv_cac_ratio')
                },
                {
                    'name': 'growth_rate',
                    'value': growth_rate,
                    'benchmark': 25.0,  # UCaaS industry average
                    'percentile': self._calculate_percentile(growth_rate, 25.0, 'growth_rate')
                },
                {
                    'name': 'churn_rate',
                    'value': churn_rate,
                    'benchmark': 8.0,  # Lower is better
                    'percentile': self._calculate_percentile(churn_rate, 8.0, 'churn_rate', lower_is_better=True)
                },
                {
                    'name': 'revenue_per_employee',
                    'value': revenue / int(company_data.get('employees', 1)) if company_data.get('employees') else 0,
                    'benchmark': 200000,  # $200k per employee
                    'percentile': self._calculate_percentile(
                        revenue / int(company_data.get('employees', 1)) if company_data.get('employees') else 0,
                        200000, 'revenue_per_employee'
                    )
                }
            ]
            
            # Store analytics
            analytics_records = []
            for metric in metrics:
                analytics = ValuationAnalytics(
                    valuation_id=valuation_id,
                    company_id=valuation.company_id,
                    user_id=valuation.user_id,
                    metric_name=metric['name'],
                    metric_value=metric['value'],
                    industry_benchmark=metric['benchmark'],
                    percentile_rank=metric['percentile'],
                    data_source='calculated'
                )
                analytics_records.append(analytics)
                self.db.add(analytics)
            
            self.db.commit()
            return analytics_records
            
        except Exception as e:
            self.db.rollback()
            print(f"Error creating valuation analytics: {e}")
            return None
    
    def _calculate_percentile(self, value: float, benchmark: float, metric_type: str, lower_is_better: bool = False) -> float:
        """Calculate percentile rank based on value vs benchmark"""
        if value == 0:
            return 0
        
        # Simple percentile calculation - in production, use actual industry data
        ratio = value / benchmark
        
        if lower_is_better:
            # For metrics like churn rate, lower is better
            if ratio <= 0.5:
                return 90  # Very good
            elif ratio <= 0.8:
                return 75  # Good
            elif ratio <= 1.0:
                return 50  # Average
            elif ratio <= 1.5:
                return 25  # Below average
            else:
                return 10  # Poor
        else:
            # For metrics like growth rate, higher is better
            if ratio >= 2.0:
                return 90  # Excellent
            elif ratio >= 1.5:
                return 75  # Good
            elif ratio >= 1.0:
                return 50  # Average
            elif ratio >= 0.5:
                return 25  # Below average
            else:
                return 10  # Poor
    
    def get_company_analytics_summary(self, company_id: int) -> Dict:
        """Get analytics summary for a company"""
        try:
            # Get latest valuation
            latest_valuation = self.db.query(Valuation).filter(
                Valuation.company_id == company_id
            ).order_by(Valuation.valuation_date.desc()).first()
            
            if not latest_valuation:
                return {}
            
            # Get analytics for latest valuation
            analytics = self.db.query(ValuationAnalytics).filter(
                ValuationAnalytics.valuation_id == latest_valuation.id
            ).all()
            
            summary = {
                'company_id': company_id,
                'valuation_date': latest_valuation.valuation_date.isoformat(),
                'final_valuation': latest_valuation.final_valuation,
                'confidence_score': latest_valuation.confidence_score,
                'metrics': {}
            }
            
            for analytic in analytics:
                summary['metrics'][analytic.metric_name] = {
                    'value': analytic.metric_value,
                    'benchmark': analytic.industry_benchmark,
                    'percentile': analytic.percentile_rank,
                    'performance': self._get_performance_rating(analytic.percentile_rank)
                }
            
            return summary
            
        except Exception as e:
            print(f"Error getting company analytics: {e}")
            return {}
    
    def _get_performance_rating(self, percentile: float) -> str:
        """Convert percentile to performance rating"""
        if percentile >= 75:
            return "Excellent"
        elif percentile >= 50:
            return "Good"
        elif percentile >= 25:
            return "Average"
        else:
            return "Below Average"

class BenchmarkingService:
    """Service for managing industry benchmarks"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def populate_ucaas_benchmarks(self):
        """Populate UCaaS industry benchmarks"""
        benchmarks = [
            # Revenue metrics
            {'industry': 'UCaaS', 'metric': 'revenue_growth_rate', 'avg': 25, 'median': 22, 'p25': 15, 'p75': 35, 'p90': 50},
            {'industry': 'UCaaS', 'metric': 'revenue_multiple', 'avg': 12.5, 'median': 10, 'p25': 6, 'p75': 15, 'p90': 20},
            
            # Customer metrics
            {'industry': 'UCaaS', 'metric': 'churn_rate_monthly', 'avg': 2.5, 'median': 2.0, 'p25': 1.0, 'p75': 3.5, 'p90': 5.0},
            {'industry': 'UCaaS', 'metric': 'ltv_cac_ratio', 'avg': 3.5, 'median': 3.0, 'p25': 2.0, 'p75': 4.5, 'p90': 6.0},
            {'industry': 'UCaaS', 'metric': 'cac_payback_months', 'avg': 18, 'median': 15, 'p25': 10, 'p75': 24, 'p90': 36},
            
            # Efficiency metrics
            {'industry': 'UCaaS', 'metric': 'gross_margin', 'avg': 0.75, 'median': 0.78, 'p25': 0.65, 'p75': 0.85, 'p90': 0.90},
            {'industry': 'UCaaS', 'metric': 'revenue_per_employee', 'avg': 200000, 'median': 180000, 'p25': 120000, 'p75': 250000, 'p90': 350000},
            
            # Valuation metrics
            {'industry': 'UCaaS', 'metric': 'ebitda_multiple', 'avg': 35, 'median': 30, 'p25': 20, 'p75': 45, 'p90': 60},
            {'industry': 'UCaaS', 'metric': 'customer_multiple', 'avg': 4200, 'median': 3800, 'p25': 2500, 'p75': 5500, 'p90': 7500},
        ]
        
        try:
            for benchmark in benchmarks:
                existing = self.db.query(MarketBenchmarks).filter(
                    MarketBenchmarks.industry == benchmark['industry'],
                    MarketBenchmarks.metric_name == benchmark['metric']
                ).first()
                
                if existing:
                    # Update existing
                    existing.avg_value = benchmark['avg']
                    existing.median_value = benchmark['median']
                    existing.p25_value = benchmark['p25']
                    existing.p75_value = benchmark['p75']
                    existing.p90_value = benchmark['p90']
                    existing.last_updated = datetime.utcnow()
                else:
                    # Create new
                    new_benchmark = MarketBenchmarks(
                        industry=benchmark['industry'],
                        metric_name=benchmark['metric'],
                        avg_value=benchmark['avg'],
                        median_value=benchmark['median'],
                        p25_value=benchmark['p25'],
                        p75_value=benchmark['p75'],
                        p90_value=benchmark['p90'],
                        sample_size=100,  # Simulated sample size
                        data_source='Industry Research 2024'
                    )
                    self.db.add(new_benchmark)
            
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            print(f"Error populating benchmarks: {e}")
            return False
    
    def get_benchmark(self, industry: str, metric_name: str) -> Optional[MarketBenchmarks]:
        """Get benchmark for specific industry and metric"""
        return self.db.query(MarketBenchmarks).filter(
            MarketBenchmarks.industry == industry,
            MarketBenchmarks.metric_name == metric_name
        ).first()

class ActivityTracker:
    """Service for tracking user activity"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def log_activity(self, user_id: int, activity_type: str, details: Dict = None, ip_address: str = None):
        """Log user activity"""
        try:
            activity = UserActivity(
                user_id=user_id,
                activity_type=activity_type,
                activity_details=details or {},
                ip_address=ip_address,
                timestamp=datetime.utcnow()
            )
            self.db.add(activity)
            self.db.commit()
            return activity
        except Exception as e:
            self.db.rollback()
            print(f"Error logging activity: {e}")
            return None
    
    def get_user_activity_summary(self, user_id: int, days: int = 30) -> Dict:
        """Get user activity summary for the last N days"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            activities = self.db.query(UserActivity).filter(
                UserActivity.user_id == user_id,
                UserActivity.timestamp >= start_date
            ).all()
            
            # Summarize by activity type
            summary = {}
            for activity in activities:
                activity_type = activity.activity_type
                if activity_type not in summary:
                    summary[activity_type] = 0
                summary[activity_type] += 1
            
            return {
                'user_id': user_id,
                'period_days': days,
                'total_activities': len(activities),
                'activity_breakdown': summary,
                'most_recent': activities[-1].timestamp.isoformat() if activities else None
            }
            
        except Exception as e:
            print(f"Error getting activity summary: {e}")
            return {}
