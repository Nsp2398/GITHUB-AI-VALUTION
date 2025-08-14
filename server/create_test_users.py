"""
Create test user for ValuAI application
This script creates a test user with the credentials from the frontend
"""

from database.database import SessionLocal
from models.models import User
from werkzeug.security import generate_password_hash
import uuid

def create_test_user():
    """Create test user with predefined credentials"""
    db = SessionLocal()
    
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == 'nsp6575@gmail.com').first()
        
        if existing_user:
            print("✅ Test user already exists!")
            print(f"User: {existing_user.first_name} {existing_user.last_name}")
            print(f"Email: {existing_user.email}")
            return existing_user
        
        # Create test user
        test_user = User(
            user_uuid=str(uuid.uuid4()),
            first_name='Test',
            last_name='User',
            email='nsp6575@gmail.com',
            password_hash=generate_password_hash('Newpassword123'),
            is_active=True
        )
        
        db.add(test_user)
        db.commit()
        
        print("✅ Test user created successfully!")
        print(f"Email: nsp6575@gmail.com")
        print(f"Password: Newpassword123")
        print(f"Name: {test_user.first_name} {test_user.last_name}")
        
        return test_user
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating test user: {e}")
        return None
    finally:
        db.close()

def create_additional_test_users():
    """Create additional test users"""
    db = SessionLocal()
    
    test_users = [
        {
            'email': 'admin@valuai.com',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'User'
        },
        {
            'email': 'demo@valuai.com', 
            'password': 'demo123',
            'first_name': 'Demo',
            'last_name': 'User'
        }
    ]
    
    try:
        for user_data in test_users:
            existing = db.query(User).filter(User.email == user_data['email']).first()
            
            if not existing:
                user = User(
                    user_uuid=str(uuid.uuid4()),
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    password_hash=generate_password_hash(user_data['password']),
                    is_active=True
                )
                db.add(user)
                print(f"✅ Created user: {user_data['email']} / {user_data['password']}")
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating additional users: {e}")
    finally:
        db.close()

def verify_users():
    """Verify all users in database"""
    db = SessionLocal()
    
    try:
        users = db.query(User).all()
        print(f"\n📊 Total users in database: {len(users)}")
        print("-" * 50)
        
        for user in users:
            print(f"👤 {user.first_name} {user.last_name}")
            print(f"   Email: {user.email}")
            print(f"   Phone: {user.phone}")
            print(f"   Active: {user.is_active}")
            print(f"   UUID: {user.user_uuid}")
            print(f"   Created: {user.created_at}")
            print()
            
    except Exception as e:
        print(f"❌ Error verifying users: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🔐 CREATING TEST USERS FOR VALUAI")
    print("=" * 40)
    
    # Create main test user
    create_test_user()
    
    # Create additional test users
    create_additional_test_users()
    
    # Verify all users
    verify_users()
    
    print("🎉 Test users created successfully!")
    print("\n📋 You can now sign in with:")
    print("Email: nsp6575@gmail.com")
    print("Password: Sai@123456")
    print("\nOr use these additional accounts:")
    print("admin@valuai.com / admin123")
    print("demo@valuai.com / demo123")
