# Euro Bakshish - Ride Sharing Application

![Backend Tests](https://github.com/b-marinov/euro_bakshish/workflows/Backend%20Unit%20Tests/badge.svg)
![Frontend Tests](https://github.com/b-marinov/euro_bakshish/workflows/Frontend%20Unit%20Tests/badge.svg)
![Docker Tests](https://github.com/b-marinov/euro_bakshish/workflows/Docker%20Build%20and%20Test/badge.svg)
![E2E Tests](https://github.com/b-marinov/euro_bakshish/workflows/End-to-End%20Tests/badge.svg)

A comprehensive ride-sharing platform built with Django REST Framework backend and React frontend.

## Features

- **User Profiles**: Create and manage profiles as either a passenger or driver
- **Trip Planning**: Select start and end locations for trips
- **Trip Completion**: Complete trips with mutual ratings between passengers and drivers
- **Trip History**: Track complete history of all trips for both drivers and passengers
- **Rating System**: Maintain user ratings based on reviews from completed trips

## Project Structure

```
euro_bakshish/
├── backend/                # Django REST Framework backend
├── web/                    # React frontend
├── docker-compose.yml      # Docker orchestration
└── docs/                   # Project documentation
```

## Technology Stack

- **Backend**: Django 4.x with Django REST Framework
- **Frontend**: React 18.x with Redux
- **Database**: PostgreSQL
- **Authentication**: JWT tokens
- **API**: RESTful API with Swagger/OpenAPI documentation

## Getting Started

### Quick Start with Docker (Recommended) 🚀

```bash
# Start all services
docker compose up -d

# Access the application
# Web: http://localhost
# API: http://localhost:8000/api/
# API Docs: http://localhost:8000/api/docs/
# Admin: http://localhost:8000/admin/
```

### Prerequisites
- Docker and Docker Compose
- OR: Python 3.10+, Node.js 16+, PostgreSQL

### Security

⚠️ **Important**: See [docs/SECURITY.md](docs/SECURITY.md) before deploying to production.

Key security features:
- ✅ JWT token-based authentication
- ✅ Secure password hashing (PBKDF2)
- ✅ CORS configuration
- ⚠️ Requires HTTPS in production
- ⚠️ Keep dependencies updated

## Quick Commands

### Running with Docker

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Rebuild containers
docker compose build --no-cache
```

### Manual Development Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend:**
```bash
cd web
npm install
npm start
```

## API Documentation

The Django REST Framework backend provides a comprehensive RESTful API.

### Interactive API Documentation
When the application is running, access:
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **Browsable API**: `http://localhost:8000/api/`

### Key Endpoints

- **Authentication**: 
  - `POST /api/users/token/` - Login (get JWT tokens)
  - `POST /api/users/` - Register
- **Users**: 
  - `GET /api/users/me/` - Get current user profile
- **Trips**: 
  - `POST /api/trips/` - Create trip
  - `GET /api/trips/my_trips/` - Get my trips
  - `GET /api/trips/available_trips/` - Get available trips
- **Reviews**: 
  - `POST /api/ratings/reviews/` - Create review

See [docs/API.md](docs/API.md) for complete API documentation.

## Documentation

- **[Docker Guide](docs/DOCKER.md)**: Complete Docker setup and commands
- **[CI/CD Pipeline](docs/CI_CD.md)**: Continuous integration and testing
- **[Setup Guide](docs/SETUP.md)**: Manual installation instructions
- **[API Documentation](docs/API.md)**: API endpoints reference
- **[Architecture](docs/ARCHITECTURE.md)**: System architecture overview
- **[Security](docs/SECURITY.md)**: Security best practices
- **[Contributing](CONTRIBUTING.md)**: How to contribute

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd web
npm test
```

### Docker Tests
```bash
# Tests are automatically run in CI/CD
# See .github/workflows/ for test configurations
```

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
