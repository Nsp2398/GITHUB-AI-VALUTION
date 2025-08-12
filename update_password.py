import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('valuai.db')
cursor = conn.cursor()

# User data
email = 'nsp6575@gmail.com'
new_password = 'Newpassword123'
hashed_password = generate_password_hash(new_password)
updated_at = datetime.utcnow().isoformat()

try:
    # Update the password
    cursor.execute('''
        UPDATE users 
        SET password_hash = ?, updated_at = ?
        WHERE email = ?
    ''', (hashed_password, updated_at, email))
    
    conn.commit()
    
    # Verify the update
    cursor.execute('SELECT password_hash FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()
    
    if result:
        # Test the new password
        is_valid = check_password_hash(result[0], new_password)
        if is_valid:
            print(f'✅ Password successfully updated for {email}')
            print(f'🔑 New password: {new_password}')
            print(f'✅ Password verification: SUCCESSFUL')
        else:
            print(f'❌ Password update failed - verification failed')
    else:
        print(f'❌ User not found: {email}')
        
except Exception as e:
    print(f'❌ Error updating password: {e}')
    conn.rollback()
finally:
    conn.close()
