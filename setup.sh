#!/bin/bash

# ValuAI Setup Script
# This script helps set up the development environment

set -e  # Exit on any error

echo "🚀 Setting up ValuAI Development Environment"
echo "============================================="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.13+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install backend dependencies
echo "📥 Installing backend dependencies..."
cd server
pip install --upgrade pip
pip install -r requirements.txt

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating environment configuration..."
    cp .env.example .env
    echo "⚠️  Please edit server/.env file with your configuration"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data
mkdir -p logs
mkdir -p uploads

# Go back to root directory
cd ..

# Install frontend dependencies
echo "📥 Installing frontend dependencies..."
cd client
npm install

# Go back to root directory
cd ..

# Remove incorrect venv directory in client if it exists
if [ -d "client/venv" ]; then
    echo "🧹 Removing incorrect venv directory from client..."
    rm -rf client/venv
fi

# Move database file to proper location if it exists
if [ -f "valuai.db" ]; then
    echo "📊 Moving database to proper location..."
    mv valuai.db server/data/
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit server/.env with your configuration (especially OPENAI_API_KEY)"
echo "2. Start the backend: cd server && python app.py"
echo "3. Start the frontend: cd client && npm run dev"
echo ""
echo "🌐 Access the application:"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:5000"
echo ""
echo "📚 For more information, see README.md"
