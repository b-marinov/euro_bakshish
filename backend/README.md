# Euro Bakshish Backend

Django REST API backend for the Euro Bakshish ride-sharing platform.

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## API Documentation

Visit `http://localhost:8000/api/docs/` for interactive API documentation.

## Technology Stack

- Django 4.x
- Django REST Framework
- PostgreSQL
- JWT Authentication
- drf-spectacular (OpenAPI documentation)
