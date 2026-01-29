# Euro Bakshish Backend

Django REST API backend for the Euro Bakshish ride-sharing platform.

## Quick Start with Docker

The easiest way to run the backend is with Docker Compose from the project root:

```bash
# From the project root directory
docker compose up

# Access the API at:
# - API Root: http://localhost:8000/api/
# - API Docs: http://localhost:8000/api/docs/
# - Admin: http://localhost:8000/admin/ (admin/admin123)
```

The Docker setup automatically:
- Starts PostgreSQL database
- Runs database migrations
- Collects static files
- Creates an admin superuser (admin/admin123)
- Starts the Django development server

### 🪟 Windows Users

If you encounter an "entrypoint.sh not found" error on Windows:

```bash
# From the project root, rebuild without cache
docker compose down
docker compose build --no-cache backend
docker compose up -d
```

This error occurs when Git converts Unix line endings (LF) to Windows line endings (CRLF). The Dockerfile now automatically handles this, but if you cloned before this fix, a rebuild is necessary.

To prevent this issue in the future:
```bash
git config --global core.autocrlf input
```

## Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your settings

# Setup database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## API Documentation

### Interactive Documentation
Visit `http://localhost:8000/api/docs/` for interactive Swagger UI documentation where you can:
- Explore all API endpoints
- Test endpoints directly in the browser
- View request/response schemas
- See authentication examples

### Static Documentation
See [../docs/API.md](../docs/API.md) for comprehensive API reference including:
- All endpoints with examples
- Authentication flows
- Error handling
- Example workflows

### OpenAPI Schema
Download the machine-readable OpenAPI schema at `http://localhost:8000/api/schema/` for use with:
- Postman
- Insomnia
- API client code generation tools

## Project Structure

```
backend/
├── apps/                   # Django applications
│   ├── users/             # User management and authentication
│   ├── trips/             # Trip management
│   └── ratings/           # Rating and review system
├── euro_bakshish/         # Project settings
│   ├── settings.py        # Django settings
│   └── urls.py            # URL routing
├── manage.py              # Django management script
├── entrypoint.sh          # Docker entrypoint script
├── Dockerfile             # Docker image configuration
└── requirements.txt       # Python dependencies
```

## Technology Stack

- **Django 4.x**: Web framework
- **Django REST Framework**: RESTful API toolkit
- **PostgreSQL**: Database
- **JWT Authentication**: Token-based authentication (djangorestframework-simplejwt)
- **drf-spectacular**: OpenAPI 3.0 schema generation and Swagger UI
- **django-cors-headers**: CORS support for web clients
- **django-filter**: Filtering support for API endpoints
- **Pillow**: Image handling for profile pictures
- **geopy**: Geolocation utilities

## Environment Variables

Key environment variables (see `.env.example`):

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=euro_bakshish
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60    # minutes
JWT_REFRESH_TOKEN_LIFETIME=1440 # minutes (24 hours)
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest apps/users/tests.py

# Run with coverage
pytest --cov=apps
```

## Development

### Code Style
Follow PEP 8 guidelines. The project uses Django's coding style.

### Adding New Endpoints
1. Create or modify views in the appropriate app's `views.py`
2. Update URL patterns in the app's `urls.py`
3. Add tests in the app's `tests.py`
4. Document the endpoint (drf-spectacular will auto-generate schema)

### Database Migrations
```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# View migration SQL
python manage.py sqlmigrate app_name migration_name
```
