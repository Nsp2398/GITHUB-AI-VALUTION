# PostgreSQL Setup Guide for ValuAI

## 🚀 Quick Setup Guide

### Step 1: Install PostgreSQL on Windows

1. **Download PostgreSQL**: Go to https://www.postgresql.org/download/windows/
2. **Run the installer** and select these components:
   - ✅ **PostgreSQL Server** (REQUIRED)
   - ✅ **pgAdmin 4** (HIGHLY RECOMMENDED)
   - ✅ **Command Line Tools** (RECOMMENDED)
   - ❌ Stack Builder (skip for now)
   - ❌ Language Pack (skip for now)

3. **Configuration during installation**:
   - Port: `5432` (default)
   - Superuser: `postgres`
   - Password: Choose a strong password (remember this!)
   - Data Directory: Use default location

### Step 2: Set Up ValuAI Database

After PostgreSQL is installed, run our setup script:

```bash
cd server
python setup_postgresql.py
```

**OR** manually create the database:

1. **Open pgAdmin 4** or use command line
2. **Create database**:
   ```sql
   CREATE DATABASE valuai_db;
   CREATE USER valuai_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE valuai_db TO valuai_user;
   ```

### Step 3: Update Environment Configuration

Your `.env` file should look like this:

```env
# Database Configuration
DATABASE_URL=postgresql://valuai_user:your_password@localhost:5432/valuai_db
DATABASE_ECHO=False

# Other configurations...
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 4: Initialize Database Schema

```bash
# Generate initial migration
python -m alembic revision --autogenerate -m "Initial migration"

# Apply migration to create tables
python -m alembic upgrade head
```

### Step 5: Start Your Application

```bash
python app.py
```

## 🔧 Manual Commands (Alternative)

If you prefer to set up manually:

### Create Database via psql:
```bash
psql -U postgres -h localhost
CREATE DATABASE valuai_db;
CREATE USER valuai_user WITH PASSWORD 'valuai123';
GRANT ALL PRIVILEGES ON DATABASE valuai_db TO valuai_user;
\q
```

### Test Connection:
```bash
psql -U valuai_user -d valuai_db -h localhost
```

## 📊 Database Schema Overview

Your ValuAI database will have these tables:

- **users**: User accounts and authentication
- **companies**: Company information and financial data
- **valuations**: Valuation results and analysis
- **file_uploads**: Uploaded documents and extracted data
- **reports**: Generated reports and metadata

## 🆘 Troubleshooting

### Common Issues:

1. **"psycopg2 not found"**: Already installed in requirements.txt
2. **"Connection refused"**: Check if PostgreSQL service is running
3. **"Authentication failed"**: Verify username/password in .env
4. **"Database does not exist"**: Run the setup script first

### Check PostgreSQL Service:
```bash
# Windows Services
services.msc
# Look for "postgresql-x64-XX" service
```

### Reset Database (if needed):
```sql
DROP DATABASE IF EXISTS valuai_db;
DROP USER IF EXISTS valuai_user;
```

## 🎯 Production Considerations

For production deployment:
- Use environment-specific passwords
- Configure connection pooling
- Set up database backups
- Monitor performance with pgAdmin

## 📝 Migration Commands Reference

```bash
# Create new migration
python -m alembic revision --autogenerate -m "Description"

# Apply migrations
python -m alembic upgrade head

# Rollback migration
python -m alembic downgrade -1

# View migration history
python -m alembic history

# Current revision
python -m alembic current
```

## ✅ Verification Checklist

- [ ] PostgreSQL installed and running
- [ ] Database `valuai_db` created
- [ ] User `valuai_user` created with permissions
- [ ] `.env` file updated with PostgreSQL URL
- [ ] Alembic migrations initialized
- [ ] Initial migration generated and applied
- [ ] Flask app starts without database errors
- [ ] Can create users and companies through the UI

## 🔄 Fallback to SQLite

If PostgreSQL setup fails, the app will automatically fall back to SQLite:

```env
# Comment out PostgreSQL and use SQLite
# DATABASE_URL=postgresql://valuai_user:password@localhost:5432/valuai_db
DATABASE_URL=sqlite:///./valuai.db
```

Your ValuAI app is designed to work with both databases!
