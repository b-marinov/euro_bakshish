# Quick Start Guide - Euro Bakshish

Get started with the Euro Bakshish ride-sharing application in minutes!

## Prerequisites

- Docker and Docker Compose (Recommended)
- OR: Python 3.10+, Node.js 16+, PostgreSQL

## Quick Start with Docker (Recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/b-marinov/euro_bakshish.git
cd euro_bakshish
```

### 2. Start the Application

```bash
docker compose up -d
```

The application will:
- Start PostgreSQL database
- Run database migrations automatically
- Start Django backend server
- Start React frontend server
- Create default admin user (admin/admin123)

### 3. Access the Application

- **Web Frontend**: http://localhost
- **API Documentation**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/
  - Username: `admin`
  - Password: `admin123`

## Manual Setup (Alternative)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### Frontend Setup

```bash
cd web

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Edit .env with your API URL

# Start development server
npm start
```

The frontend will be available at http://localhost:3000

## First Steps

### 1. Register a New User
1. Go to http://localhost (or http://localhost:3000 for manual setup)
2. Click "Register" or "Sign Up"
3. Fill in your details and select user type (Passenger/Driver)
4. Click "Register"

### 2. Login
1. Enter your credentials
2. Click "Login"

### 3. Create a Trip (as Passenger)
1. Navigate to "Create Trip"
2. Fill in trip details (start location, end location, etc.)
3. Click "Create Trip"

### 4. Accept a Trip (as Driver)
1. Navigate to "Available Trips"
2. Browse available trips
3. Click "Accept" on a trip

## Common Tasks

### Using Docker

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# View specific service logs
docker compose logs -f backend
docker compose logs -f web

# Rebuild containers
docker compose build --no-cache

# Access backend shell
docker compose exec backend bash

# Run Django commands
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

### Database Operations

```bash
# Access PostgreSQL (Docker)
docker compose exec db psql -U postgres -d euro_bakshish

# View database
\dt  # List tables
\d+ user  # Describe user table
SELECT * FROM users_customuser;
```

### Reset Database (Docker)

```bash
docker compose down -v  # Remove volumes
docker compose up -d    # Restart with fresh database
```

## Troubleshooting

### Docker issues
- Ensure Docker Desktop is running
- Check port availability (80, 8000, 5432)
- Try `docker compose down -v && docker compose up -d`

### API not accessible
- Check if backend is running: `docker compose ps`
- View logs: `docker compose logs backend`
- Verify migrations: `docker compose exec backend python manage.py showmigrations`

### Frontend not loading
- Check if web service is running: `docker compose ps`
- View logs: `docker compose logs web`
- Clear browser cache

For more details, see [README.md](README.md) and [docs/DOCKER.md](docs/DOCKER.md).

Happy coding! 🚀
