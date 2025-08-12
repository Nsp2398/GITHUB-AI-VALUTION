#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'server'))

from database.database import SessionLocal
from models.models import User
from werkzeug.security import check_password_hash
import traceback

def test_signin():
    print("Testing signin process...")
    db = SessionLocal()
    
    try:
        email = "nsp6575@gmail.com"
        password = "Newpassword123"
        
        print(f"1. Looking for user with email: {email}")
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print("❌ User not found")
            return
            
        print(f"✅ User found: {user.first_name} {user.last_name}")
        print(f"   ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Active: {user.is_active}")
        
        print(f"2. Testing password verification...")
        is_valid = check_password_hash(user.password_hash, password)
        print(f"   Password valid: {is_valid}")
        
        if is_valid:
            print("✅ Authentication would succeed")
        else:
            print("❌ Authentication would fail")
            
    except Exception as e:
        print(f"❌ Error during signin test: {e}")
        print("Full traceback:")
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_signin()
