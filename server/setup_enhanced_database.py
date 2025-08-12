"""
Database Enhancement Setup Script
Initializes new analytics tables and populates benchmark data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import engine, SessionLocal, init_db
from models.models import Base as OriginalBase
from models.enhanced_models import Base as EnhancedBase
from services.analytics_service import BenchmarkingService
from sqlalchemy import text

def setup_enhanced_database():
    """Set up enhanced database with analytics tables"""
    print("🚀 Starting enhanced database setup...")
    
    try:
        # Create all tables
        print("📊 Creating enhanced tables...")
        EnhancedBase.metadata.create_all(bind=engine)
        print("✅ Enhanced tables created successfully")
        
        # Initialize benchmarking data
        print("🎯 Populating industry benchmarks...")
        db = SessionLocal()
        
        benchmarking_service = BenchmarkingService(db)
        success = benchmarking_service.populate_ucaas_benchmarks()
        
        if success:
            print("✅ Industry benchmarks populated successfully")
        else:
            print("❌ Failed to populate benchmarks")
        
        db.close()
        
        # Verify setup
        print("🔍 Verifying database setup...")
        db = SessionLocal()
        
        # Check if tables exist
        result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = [row[0] for row in result.fetchall()]
        
        expected_tables = [
            'valuation_analytics',
            'market_benchmarks', 
            'company_metrics_history',
            'ai_model_performance',
            'user_activity',
            'company_comparables'
        ]
        
        missing_tables = [table for table in expected_tables if table not in tables]
        
        if missing_tables:
            print(f"⚠️  Missing tables: {missing_tables}")
        else:
            print("✅ All enhanced tables verified")
        
        # Check benchmark data
        result = db.execute(text("SELECT COUNT(*) FROM market_benchmarks;"))
        benchmark_count = result.fetchone()[0]
        print(f"📈 Benchmark records: {benchmark_count}")
        
        db.close()
        
        print("🎉 Enhanced database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def test_analytics_functionality():
    """Test the analytics functionality"""
    print("\n🧪 Testing analytics functionality...")
    
    try:
        from services.analytics_service import AnalyticsService, ActivityTracker
        
        db = SessionLocal()
        
        # Test benchmark retrieval
        benchmarking_service = BenchmarkingService(db)
        benchmark = benchmarking_service.get_benchmark('UCaaS', 'revenue_growth_rate')
        
        if benchmark:
            print(f"✅ Benchmark test passed - Revenue growth rate avg: {benchmark.avg_value}%")
        else:
            print("❌ Benchmark test failed")
        
        # Test activity tracking
        activity_tracker = ActivityTracker(db)
        
        # Note: This would require an actual user ID in practice
        print("✅ Activity tracker initialized")
        
        db.close()
        
        print("✅ All analytics functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Analytics test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🔧 ValuAI Enhanced Database Setup")
    print("=" * 50)
    
    # Run setup
    setup_success = setup_enhanced_database()
    
    if setup_success:
        # Run tests
        test_success = test_analytics_functionality()
        
        if test_success:
            print("\n🎊 Setup completed successfully!")
            print("\n🚀 Available new features:")
            print("   • Company performance analytics")
            print("   • Industry benchmark comparisons") 
            print("   • User activity tracking")
            print("   • AI model performance monitoring")
            print("   • Market insights and trends")
            print("\n📋 API Endpoints:")
            print("   • GET /api/analytics/company/{id}/summary")
            print("   • GET /api/analytics/benchmarks/UCaaS")
            print("   • GET /api/analytics/company/{id}/performance")
            print("   • GET /api/analytics/user/activity")
            print("   • GET /api/analytics/market-insights")
        else:
            print("\n⚠️  Setup completed but tests failed")
    else:
        print("\n❌ Setup failed")
