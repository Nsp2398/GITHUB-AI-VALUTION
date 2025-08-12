"""
Database setup and initialization script for ValuAI PostgreSQL database.

This script helps set up PostgreSQL database for the ValuAI project.
Run this after installing PostgreSQL to create the database and user.
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

def create_database_and_user():
    """Create PostgreSQL database and user for ValuAI"""
    
    print("🐘 POSTGRESQL SETUP FOR VALUAI")
    print("="*50)
    
    # Database configuration
    db_name = "valuai_db"
    db_user = "valuai_user"
    db_password = input("Enter password for valuai_user (or press Enter for default 'valuai123'): ").strip()
    if not db_password:
        db_password = "valuai123"
    
    postgres_password = input("Enter PostgreSQL superuser (postgres) password: ").strip()
    
    try:
        # Connect to PostgreSQL as superuser
        print("\n📡 Connecting to PostgreSQL...")
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password=postgres_password
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create database
        print(f"🗄️  Creating database '{db_name}'...")
        try:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"✅ Database '{db_name}' created successfully!")
        except psycopg2.errors.DuplicateDatabase:
            print(f"⚠️  Database '{db_name}' already exists.")
        
        # Create user
        print(f"👤 Creating user '{db_user}'...")
        try:
            cursor.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(db_user)), [db_password])
            print(f"✅ User '{db_user}' created successfully!")
        except psycopg2.errors.DuplicateObject:
            print(f"⚠️  User '{db_user}' already exists.")
            # Update password
            cursor.execute(sql.SQL("ALTER USER {} WITH PASSWORD %s").format(sql.Identifier(db_user)), [db_password])
            print(f"🔐 Password updated for user '{db_user}'.")
        
        # Grant privileges
        print(f"🔑 Granting privileges to '{db_user}'...")
        cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
            sql.Identifier(db_name), sql.Identifier(db_user)
        ))
        print(f"✅ Privileges granted to '{db_user}'!")
        
        cursor.close()
        conn.close()
        
        # Update .env file
        print("\n📝 Updating .env file...")
        update_env_file(db_user, db_password, db_name)
        
        print("\n🎉 POSTGRESQL SETUP COMPLETED!")
        print("="*50)
        print(f"Database: {db_name}")
        print(f"User: {db_user}")
        print(f"Password: {db_password}")
        print(f"Connection String: postgresql://{db_user}:{db_password}@localhost:5432/{db_name}")
        print("\n📋 NEXT STEPS:")
        print("1. Your .env file has been updated with PostgreSQL settings")
        print("2. Run 'python -m alembic revision --autogenerate -m \"Initial migration\"'")
        print("3. Run 'python -m alembic upgrade head' to create tables")
        print("4. Start your Flask application!")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ PostgreSQL Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def update_env_file(db_user, db_password, db_name):
    """Update .env file with PostgreSQL configuration"""
    
    env_file_path = ".env"
    
    # Read current .env file
    with open(env_file_path, 'r') as file:
        lines = file.readlines()
    
    # Update DATABASE_URL
    new_database_url = f"postgresql://{db_user}:{db_password}@localhost:5432/{db_name}"
    
    updated_lines = []
    database_url_updated = False
    
    for line in lines:
        if line.startswith("DATABASE_URL="):
            if "postgresql://" in line:
                # Update existing PostgreSQL URL
                updated_lines.append(f"DATABASE_URL={new_database_url}\n")
                database_url_updated = True
            elif "sqlite://" in line:
                # Comment out SQLite and add PostgreSQL
                updated_lines.append(f"# {line}")
                updated_lines.append(f"DATABASE_URL={new_database_url}\n")
                database_url_updated = True
            else:
                updated_lines.append(f"DATABASE_URL={new_database_url}\n")
                database_url_updated = True
        else:
            updated_lines.append(line)
    
    # If DATABASE_URL wasn't found, add it
    if not database_url_updated:
        updated_lines.append(f"\n# PostgreSQL Database Configuration\n")
        updated_lines.append(f"DATABASE_URL={new_database_url}\n")
    
    # Write updated .env file
    with open(env_file_path, 'w') as file:
        file.writelines(updated_lines)
    
    print(f"✅ .env file updated with PostgreSQL configuration")

def test_connection():
    """Test connection to PostgreSQL database"""
    
    print("🔌 Testing database connection...")
    
    try:
        # Load the updated environment
        load_dotenv(override=True)
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url or not database_url.startswith('postgresql://'):
            print("❌ PostgreSQL DATABASE_URL not found in .env file")
            return False
        
        # Test connection
        engine = create_engine(database_url)
        connection = engine.connect()
        connection.close()
        
        print("✅ Database connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def main():
    """Main setup function"""
    
    print("ValuAI PostgreSQL Database Setup")
    print("This script will help you set up PostgreSQL for your ValuAI project.\n")
    
    choice = input("Do you want to create the database and user? (y/n): ").lower().strip()
    
    if choice in ['y', 'yes']:
        if create_database_and_user():
            print("\n" + "="*50)
            test_choice = input("Test database connection? (y/n): ").lower().strip()
            if test_choice in ['y', 'yes']:
                test_connection()
    else:
        print("Setup cancelled.")

if __name__ == "__main__":
    main()
