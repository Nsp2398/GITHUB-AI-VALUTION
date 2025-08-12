"""
Test script to verify PostgreSQL setup and database functionality
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test environment configuration"""
    print("🔧 TESTING ENVIRONMENT CONFIGURATION")
    print("-" * 40)
    
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL')
    print(f"Database URL: {database_url}")
    
    if database_url:
        if database_url.startswith('postgresql://'):
            print("✅ PostgreSQL configuration detected")
            return 'postgresql'
        elif database_url.startswith('sqlite://'):
            print("✅ SQLite configuration detected (development)")
            return 'sqlite'
    else:
        print("❌ No DATABASE_URL found")
        return None

def test_models():
    """Test model imports"""
    print("\n📋 TESTING MODEL IMPORTS")
    print("-" * 40)
    
    try:
        from models.models import User, Company, Valuation, FileUpload, Report, Base
        print("✅ All models imported successfully")
        
        tables = list(Base.metadata.tables.keys())
        print(f"✅ Tables defined: {', '.join(tables)}")
        return True
    except Exception as e:
        print(f"❌ Model import failed: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n🔌 TESTING DATABASE CONNECTION")
    print("-" * 40)
    
    try:
        from database.database import engine
        print(f"✅ Database engine created: {engine.url}")
        
        # Test connection
        conn = engine.connect()
        print("✅ Database connection successful")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_flask_app():
    """Test Flask app initialization"""
    print("\n🌐 TESTING FLASK APP")
    print("-" * 40)
    
    try:
        # Set testing environment
        os.environ['FLASK_ENV'] = 'testing'
        
        from app import app
        print("✅ Flask app imported successfully")
        
        # Test app context
        with app.app_context():
            print("✅ Flask app context works")
        
        return True
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def test_alembic():
    """Test Alembic configuration"""
    print("\n🔄 TESTING ALEMBIC CONFIGURATION")
    print("-" * 40)
    
    try:
        import subprocess
        result = subprocess.run(['python', '-m', 'alembic', 'current'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Alembic is properly configured")
            print(f"Current revision: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Alembic error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Alembic test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 VALUAI POSTGRESQL SETUP VERIFICATION")
    print("=" * 50)
    
    tests = [
        ("Environment Configuration", test_environment),
        ("Model Imports", test_models),
        ("Database Connection", test_database_connection),
        ("Flask App", test_flask_app),
        ("Alembic Configuration", test_alembic)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("Your ValuAI PostgreSQL setup is ready!")
        print("\n📋 NEXT STEPS:")
        print("1. Install PostgreSQL if you haven't already")
        print("2. Run 'python setup_postgresql.py' to create database")
        print("3. Update .env with PostgreSQL connection string")
        print("4. Run 'python app.py' to start your application")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
