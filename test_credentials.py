import sqlite3
from werkzeug.security import check_password_hash

conn = sqlite3.connect('valuai.db')
cursor = conn.cursor()

print('🔍 CHECKING YOUR ACCOUNT CREDENTIALS')
print('=' * 50)

# Get your user data
cursor.execute('SELECT id, first_name, last_name, email, password_hash, is_active FROM users WHERE email = ?', ('nsp6575@gmail.com',))
user = cursor.fetchone()

if user:
    print(f'✅ User found in database:')
    print(f'   ID: {user[0]}')
    print(f'   Name: {user[1]} {user[2]}')
    print(f'   Email: {user[3]}')
    print(f'   Active: {"Yes" if user[5] else "No"}')
    print(f'   Password hash exists: {"Yes" if user[4] else "No"}')
    
    # Test password verification
    test_passwords = ['Newpassword123', 'Sai@123456']
    print(f'\n🔐 Testing passwords:')
    for pwd in test_passwords:
        is_valid = check_password_hash(user[4], pwd)
        print(f'   "{pwd}": {"✅ VALID" if is_valid else "❌ Invalid"}')
else:
    print('❌ User not found in database')

conn.close()
