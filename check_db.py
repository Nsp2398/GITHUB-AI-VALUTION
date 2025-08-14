import sqlite3

conn = sqlite3.connect('valuai.db')
cursor = conn.cursor()

print('🗄️ DATABASE: SQLite')
print('📍 Location: valuai.db (in root directory)')
print()

# Show table structure
cursor.execute('PRAGMA table_info(users)')
columns = cursor.fetchall()
print('👤 USER TABLE STRUCTURE:')
print('-' * 40)
for col in columns:
    nullable = "NULL" if not col[3] else "NOT NULL"
    primary = "PRIMARY" if col[5] else ""
    print(f'{col[1]:<15} {col[2]:<10} {primary:<8} {nullable}')

print()
print('📊 CURRENT USERS:')
print('-' * 60)
cursor.execute('SELECT id, first_name, last_name, email, phone, is_active, created_at FROM users')
users = cursor.fetchall()
for user in users:
    email = user[3] if user[3] else "No email"
    phone = user[4] if user[4] else "No phone" 
    print(f'ID: {user[0]} | {user[1]} {user[2]} | {email} | Active: {user[5]}')

print()
print('📍 Database file location: c:\\Users\\saini\\GITHUB AI VALUTION\\valuai.db')
conn.close()
