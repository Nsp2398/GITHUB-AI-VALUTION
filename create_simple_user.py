"""
Simple user creation script for SQLite database
"""
import sqlite3
from werkzeug.security import generate_password_hash
import uuid
from datetime import datetime

def create_user():
    # Connect to the database
    conn = sqlite3.connect('server/valuai.db')
    cursor = conn.cursor()
    
    # User data
    email = 'nsp6575@gmail.com'
    password = 'Newpassword123'
    hashed_password = generate_password_hash(password)
    user_uuid = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    
    try:
        # Check if user exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            # Update existing user
            cursor.execute('''
                UPDATE users 
                SET password_hash = ?, user_uuid = ?, updated_at = ?
                WHERE email = ?
            ''', (hashed_password, user_uuid, created_at, email))
            print(f'✅ Updated existing user: {email}')
        else:
            # Create new user
            cursor.execute('''
                INSERT INTO users (user_uuid, first_name, last_name, email, password_hash, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_uuid, 'NSP', 'User', email, hashed_password, True, created_at))
            print(f'✅ Created new user: {email}')
        
        conn.commit()
        print(f'✅ User credentials set successfully!')
        print(f'📧 Email: {email}')
        print(f'🔑 Password: {password}')
        
    except Exception as e:
        print(f'❌ Error: {e}')
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    create_user()
