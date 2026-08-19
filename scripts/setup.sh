#!/bin/bash

# N.O.U Digital Systems - Development Setup Script

set -e

echo "=================================="
echo "N.O.U Digital Systems Setup"
echo "=================================="

# Check prerequisites
echo ""
echo "Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

# Check Python
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed"
    echo "Please install Python 3.10+ from https://python.org/"
    exit 1
fi

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "Warning: PostgreSQL client not found"
    echo "Please ensure PostgreSQL is installed and running"
fi

echo "Prerequisites check passed!"

# Setup backend
echo ""
echo "Setting up backend..."
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "Please update .env file with your configuration"
fi

cd ..

# Setup frontend
echo ""
echo "Setting up frontend..."
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
fi

cd ..

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Start PostgreSQL database"
echo "2. Update backend/.env with your database credentials"
echo "3. Run database setup: psql -U postgres -d nou_database -f database/schema.sql"
echo "4. Start backend: cd backend && python -m uvicorn app.main:app --reload"
echo "5. Start frontend: cd frontend && npm run dev"
echo ""
echo "The application will be available at:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/api/docs"
echo ""
echo "Happy coding!"