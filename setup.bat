@echo off
REM ValuAI Setup Script for Windows
REM This script helps set up the development environment

echo 🚀 Setting up ValuAI Development Environment
echo =============================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.13+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Create virtual environment
echo 📦 Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install backend dependencies
echo 📥 Installing backend dependencies...
cd server
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create environment file if it doesn't exist
if not exist .env (
    echo 📝 Creating environment configuration...
    copy .env.example .env
    echo ⚠️  Please edit server\.env file with your configuration
)

REM Create necessary directories
echo 📁 Creating necessary directories...
if not exist data mkdir data
if not exist logs mkdir logs
if not exist uploads mkdir uploads

REM Go back to root directory
cd ..

REM Install frontend dependencies
echo 📥 Installing frontend dependencies...
cd client
npm install

REM Go back to root directory
cd ..

REM Remove incorrect venv directory in client if it exists
if exist client\venv (
    echo 🧹 Removing incorrect venv directory from client...
    rmdir /s /q client\venv
)

REM Move database file to proper location if it exists
if exist valuai.db (
    echo 📊 Moving database to proper location...
    move valuai.db server\data\
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Edit server\.env with your configuration ^(especially OPENAI_API_KEY^)
echo 2. Start the backend: cd server ^&^& python app.py
echo 3. Start the frontend: cd client ^&^& npm run dev
echo.
echo 🌐 Access the application:
echo    Frontend: http://localhost:5173
echo    Backend:  http://localhost:5000
echo.
echo 📚 For more information, see README.md

pause
