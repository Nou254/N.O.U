# N.O.U Digital Systems - Getting Started Guide

## Quick Start

This guide will help you set up and run the N.O.U Digital Systems platform on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

1. **Node.js 18+** and npm
   - Download: https://nodejs.org/
   - Verify: `node --version` and `npm --version`

2. **Python 3.10+**
   - Download: https://python.org/
   - Verify: `python --version`

3. **PostgreSQL 14+**
   - Download: https://postgresql.org/
   - Verify: `psql --version`

4. **Git**
   - Download: https://git-scm.com/
   - Verify: `git --version`

### Step 1: Clone or Navigate to Project

```bash
cd N.O.U
```

### Step 2: Set Up Backend

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env file with your database credentials
# DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/nou_database
```

### Step 3: Set Up Database

```bash
# Create PostgreSQL database
psql -U postgres -c "CREATE DATABASE nou_database"

# Run database schema
psql -U postgres -d nou_database -f database/schema.sql

# Run seed data (optional - for development)
psql -U postgres -d nou_database -f database/seeds.sql
```

### Step 4: Set Up Frontend

```bash
# Navigate to frontend directory (from root)
cd frontend

# Install Node.js dependencies
npm install

# Copy environment file
cp .env.example .env
```

### Step 4b: Enable AI-Powered Assessments (Groq)

Assessments are **AI-powered**: Groq generates a fresh set of advanced,
randomized open-ended questions spanning the entire tech world for every
candidate, and grades each written answer with feedback plus a hiring
recommendation.

1. Create a free Groq account and API key: https://console.groq.com/keys
2. Add the key to `backend/.env`:

```
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

3. Restart the backend.

> **Note:** Without `GROQ_API_KEY`, starting an assessment returns `503`
> with a clear message. Everything else in the app works without a key.
> The migration `database/migrations/ai_assessment.sql` was applied to add
> the per-session question snapshot table and AI feedback columns.

### Step 5: Start Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
# Activate virtual environment if not already active
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Start FastAPI server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend

# Start Vite development server
npm run dev
```

### Step 6: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Alternative API Docs**: http://localhost:8000/api/redoc

### Step 7: Test the Application

1. **Register a new user**:
   - Go to http://localhost:3000/register
   - Create an account as a "customer" or "applicant"

2. **Login**:
   - Go to http://localhost:3000/login
   - Use your credentials

3. **Test admin access** (if you ran seeds.sql):
   - Email: admin@nou.com
   - Password: admin123

## Docker Setup (Alternative)

If you prefer using Docker:

```bash
cd deployment

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Project Structure

```
N.O.U/
├── backend/                 # FastAPI application
│   ├── app/                # Application code
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment template
├── frontend/               # React application
│   ├── src/                # Source code
│   ├── package.json        # Node.js dependencies
│   └── vite.config.ts      # Vite configuration
├── database/               # Database scripts
│   ├── schema.sql          # Database schema
│   └── seeds.sql           # Sample data
├── deployment/             # Docker configurations
└── docs/                   # Documentation
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/auth/me` - Get current user

### Products
- `GET /api/v1/products` - List products
- `GET /api/v1/products/{id}` - Get product details
- `GET /api/v1/products/{id}/download` - Download product

### Employment
- `GET /api/v1/employment/jobs` - List job listings
- `POST /api/v1/employment/applications` - Submit application

### Assessments
- `GET /api/v1/assessments` - List assessments
- `POST /api/v1/assessments/{id}/start` - Start assessment
- `POST /api/v1/assessments/sessions/{id}/submit` - Submit answers

### Support
- `POST /api/v1/support/tickets` - Create support ticket
- `GET /api/v1/support/tickets/me` - Get my tickets

### Admin
- `GET /api/v1/admin/dashboard/stats` - Dashboard statistics
- `POST /api/v1/admin/products` - Create product
- `GET /api/v1/admin/users` - List users

## User Roles

### Visitor
- Browse company information
- View products
- View job listings

### Customer
- Download software
- Submit support tickets
- Request projects
- Manage profile

### Applicant
- Apply for jobs
- Take technical assessments
- View application status
- View assessment results

### Admin
- Manage users
- Manage products
- Manage job listings
- Manage assessments
- View reports
- Manage support tickets

## Development Workflow

### Making Changes

1. **Backend changes**: Edit files in `backend/app/`
2. **Frontend changes**: Edit files in `frontend/src/`
3. **Database changes**: Update `database/schema.sql` and run migrations

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
cd backend
black .
flake8 .

# Frontend linting
cd frontend
npm run lint
```

## Troubleshooting

### Common Issues

1. **Database connection error**:
   - Ensure PostgreSQL is running
   - Check credentials in `backend/.env`
   - Verify database exists

2. **Port already in use**:
   - Change port in `backend/.env` or `frontend/vite.config.ts`
   - Kill process using the port

3. **Module not found errors**:
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt` again
   - Run `npm install` again

4. **CORS errors**:
   - Check CORS settings in `backend/app/core/config.py`
   - Ensure frontend URL is in allowed origins

### Getting Help

- Check the documentation in `docs/`
- Review the implementation summary
- Check API documentation at http://localhost:8000/api/docs

## Next Steps

1. Explore the codebase
2. Read the technical specification
3. Follow the development roadmap
4. Start building features
5. Write tests
6. Deploy to production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

---

**Happy Coding!**