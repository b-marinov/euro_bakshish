# Euro Bakshish - Ride Sharing Application

![Backend Tests](https://github.com/b-marinov/euro_bakshish/workflows/Backend%20Unit%20Tests/badge.svg)
![Frontend Tests](https://github.com/b-marinov/euro_bakshish/workflows/Frontend%20Unit%20Tests/badge.svg)
![Docker Tests](https://github.com/b-marinov/euro_bakshish/workflows/Docker%20Build%20and%20Test/badge.svg)
![E2E Tests](https://github.com/b-marinov/euro_bakshish/workflows/End-to-End%20Tests/badge.svg)

A comprehensive ride-sharing platform with web and Android applications.

## Features

- **User Profiles**: Create and manage profiles as either a passenger or driver
- **Trip Planning**: Select start and end locations for trips
- **Trip Completion**: Complete trips with mutual ratings between passengers and drivers
- **Trip History**: Track complete history of all trips for both drivers and passengers
- **Rating System**: Maintain user ratings based on reviews from completed trips

## Project Structure

```
euro_bakshish/
├── backend/          # Django REST API backend
├── web/              # React web frontend
├── android/          # Android application
└── docs/             # Project documentation
```

## Technology Stack

### Backend
- **Framework**: Django 4.x with Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT tokens

### Web Frontend
- **Framework**: React 18.x
- **State Management**: Redux
- **UI Library**: Material-UI
- **Maps**: Google Maps API

### Android
- **Language**: Kotlin
- **Architecture**: MVVM
- **Networking**: Retrofit
- **Maps**: Google Maps SDK

## Getting Started

### Option 1: Docker (Recommended) 🐳

**Fastest way to run the entire application:**

```bash
# Start all services (backend, frontend, database)
docker-compose up -d

# Access the application
# Web: http://localhost
# API: http://localhost:8000/api/
# Admin: http://localhost:8000/admin/ (admin/admin123)
```

For more Docker commands and options, see [docs/DOCKER.md](docs/DOCKER.md) or run:
```bash
make help
```

### Option 2: Manual Setup

#### Prerequisites
- Python 3.10+
- Node.js 18+
- Android Studio (for Android development)
- PostgreSQL

See [docs/SETUP.md](docs/SETUP.md) for detailed manual setup instructions.

### Security

⚠️ **Important**: Please review [docs/SECURITY.md](docs/SECURITY.md) before deploying to production.

Key security considerations:
- Set SECRET_KEY via environment variable (required)
- Use HTTPS in production
- Review token storage mechanisms
- Configure CORS properly
- Keep dependencies updated

## Quick Commands

### Using Docker (Recommended)

```bash
make up          # Start all services
make down        # Stop all services
make logs        # View logs
make dev         # Start with hot reload (development)
make migrate     # Run database migrations
make test        # Run tests
```

### Manual Setup

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Web Frontend Setup

```bash
cd web
npm install
npm start
```

### Android Setup

1. Open Android Studio
2. Open the `android` directory as a project
3. Sync Gradle files
4. Run the application

## API Documentation

The API provides comprehensive interactive documentation:

### Interactive Swagger UI
When the backend is running, access the interactive API documentation:
- **URL**: `http://localhost:8000/api/docs/`
- **Features**: 
  - Try out API endpoints directly in the browser
  - View request/response schemas
  - Test authentication flows
  - See example requests and responses

### OpenAPI Schema
Machine-readable API specification:
- **URL**: `http://localhost:8000/api/schema/`
- Import into Postman, Insomnia, or other API clients

### Static Documentation
Detailed API reference: [docs/API.md](docs/API.md)
- Complete endpoint descriptions
- Authentication guide
- Example workflows
- Error handling

### Quick API Test
Once the backend is running, test the API:
```bash
# Get API root
curl http://localhost:8000/api/

# Create a user (example)
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", ...}'
```

## Documentation

- **[Docker Guide](docs/DOCKER.md)**: Complete Docker setup and commands
- **[CI/CD Pipeline](docs/CI_CD.md)**: Continuous integration and testing
- **[Setup Guide](docs/SETUP.md)**: Manual installation instructions
- **[API Documentation](docs/API.md)**: API endpoints reference
- **[Architecture](docs/ARCHITECTURE.md)**: System architecture overview
- **[Security](docs/SECURITY.md)**: Security best practices
- **[Contributing](CONTRIBUTING.md)**: How to contribute

## Testing

The project includes comprehensive automated testing:

- **Unit Tests**: Backend (pytest) and frontend (Jest/React Testing Library)
- **Integration Tests**: Docker Compose validation and service connectivity
- **E2E Tests**: End-to-end browser testing with Playwright
- **CI/CD**: Automated testing on every push and pull request

Run tests locally:
```bash
# Backend tests
make test

# Frontend tests
cd web && npm test

# Docker tests
make up && docker-compose exec backend pytest

# All tests
make test-all
```

See [CI/CD documentation](docs/CI_CD.md) for detailed testing information.

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
