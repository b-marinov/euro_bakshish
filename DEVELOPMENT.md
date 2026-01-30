# Development Guide - Euro Bakshish

This guide covers everything you need to know to develop Euro Bakshish locally.

## Table of Contents

- [Quick Start](#quick-start)
- [Development Environment](#development-environment)
- [Docker Setup](#docker-setup)
- [Code Quality](#code-quality)
- [Testing](#testing)
- [Common Tasks](#common-tasks)

## Quick Start

### First Time Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/b-marinov/euro_bakshish.git
   cd euro_bakshish
   ```

2. **Choose your development approach**

   **Option A: Docker Development (Recommended)**
   ```bash
   # Install Docker and Docker Compose, then:
   make quickstart
   ```

   **Option B: Local Development**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   make install
   # Or manually:
   pip install -r requirements-nextpy.txt -r requirements-dev.txt

   # Install pre-commit hooks
   make pre-commit-install

   # Run the application
   python euro_bakshish_app.py
   ```

## Development Environment

### Prerequisites

- **Python 3.10+** (for local development)
- **Docker & Docker Compose** (for containerized development)
- **Git**
- **Make** (optional, but recommended)

### Project Structure

```
euro_bakshish/
├── .github/
│   └── workflows/          # CI/CD workflows
├── tests/                  # Test suite
│   ├── conftest.py        # Test fixtures
│   ├── test_models.py     # Model unit tests
│   ├── test_integration.py # Integration tests
│   └── test_docker.py     # Docker tests
├── euro_bakshish_app.py   # Main application
├── requirements-nextpy.txt # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── Dockerfile             # Production Docker image
├── Dockerfile.dev         # Development Docker image
├── Dockerfile.test        # Test Docker image
├── docker-compose.yml     # Production compose
├── docker-compose.dev.yml # Development compose
├── docker-compose.test.yml # Test compose
├── pyproject.toml         # Python project config
├── .pre-commit-config.yaml # Pre-commit hooks
└── Makefile               # Common commands
```

## Docker Setup

### Docker Development Workflow

We provide three Docker environments:

1. **Production** - Optimized for deployment
2. **Development** - Hot-reload with mounted code
3. **Test** - For running test suite

### Development with Docker

```bash
# Build and start development environment
make dev-up

# View logs
make dev-logs

# Stop development environment
make dev-down
```

The development environment:
- Mounts your code directory for instant changes
- Includes all dev dependencies
- Runs with debug logging
- Hot-reloads on code changes

### Production with Docker

```bash
# Build production image
make build

# Start production containers
make up

# View logs
make logs

# Stop containers
make down
```

### Running Tests with Docker

```bash
# Run all tests in Docker
make test

# Run tests with coverage
make test-coverage
```

## Code Quality

We use several tools to maintain code quality:

### Black (Code Formatting)

```bash
# Format all code
make format

# Or manually
black euro_bakshish_app.py tests/
```

### isort (Import Sorting)

```bash
# Sort imports
isort euro_bakshish_app.py tests/
```

### Flake8 (Linting)

```bash
# Run linter
make lint

# Or manually
flake8 euro_bakshish_app.py tests/ --max-line-length=100
```

### Mypy (Type Checking)

```bash
# Type check
mypy euro_bakshish_app.py --ignore-missing-imports
```

### Pre-commit Hooks

We use pre-commit to automatically run checks before commits:

```bash
# Install hooks
make pre-commit-install

# Run manually on all files
make pre-commit

# Hooks run automatically on git commit
```

## Testing

### Running Tests Locally

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_models.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run tests matching a pattern
pytest tests/ -k "test_user"

# Run only unit tests
pytest tests/ -m unit

# Run only integration tests
pytest tests/ -m integration
```

### Writing Tests

Tests are organized by type:
- `test_models.py` - Unit tests for database models
- `test_integration.py` - Integration tests for workflows
- `test_docker.py` - Docker configuration tests

Example test:

```python
import pytest
from euro_bakshish_app import User, hash_password

@pytest.mark.unit
def test_create_user(db_session):
    """Test creating a user."""
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=hash_password("password"),
        user_type="passenger"
    )
    db_session.add(user)
    db_session.commit()
    
    assert user.id is not None
    assert user.username == "testuser"
```

## Common Tasks

### Adding a New Feature

1. **Create a new branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes**
   - Update `euro_bakshish_app.py`
   - Add tests in `tests/`

3. **Format and lint**
   ```bash
   make format
   make lint
   ```

4. **Run tests**
   ```bash
   make test-local
   # or
   make test  # in Docker
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add new feature"
   # Pre-commit hooks will run automatically
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/my-new-feature
   ```

### Updating Dependencies

**Production dependencies:**
```bash
# Edit requirements-nextpy.txt
pip install -r requirements-nextpy.txt

# Rebuild Docker image
make build
```

**Development dependencies:**
```bash
# Edit requirements-dev.txt
pip install -r requirements-dev.txt
```

### Database Management

```bash
# Initialize database
make db-init

# Database is automatically created when app starts
# Location: ./data/euro_bakshish.db (in Docker)
#           ./euro_bakshish.db (local)
```

### Cleaning Up

```bash
# Remove containers and generated files
make clean

# Deep clean including Docker images
make clean-all
```

### Debugging

**Local debugging:**
```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Run application
python euro_bakshish_app.py
```

**Docker debugging:**
```bash
# View logs
make logs  # or make dev-logs

# Execute shell in container
docker exec -it euro_bakshish_app /bin/bash

# View application files
docker exec -it euro_bakshish_app ls -la /app
```

### Accessing the Application

When running:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Workflow Summary

### Daily Development Workflow

```bash
# 1. Pull latest changes
git pull origin main

# 2. Start development environment
make dev-up

# 3. Make changes to code
# Files are mounted, changes reflect immediately

# 4. Run tests
make test-local

# 5. Format and lint
make format
make lint

# 6. Commit changes
git add .
git commit -m "Description of changes"
# Pre-commit hooks run automatically

# 7. Push to GitHub
git push origin feature/my-branch

# 8. Clean up when done
make dev-down
```

## Tips and Best Practices

1. **Always run tests** before committing
2. **Use pre-commit hooks** to catch issues early
3. **Format code** with Black before committing
4. **Write tests** for new features
5. **Use Docker** for consistent environment
6. **Keep commits small** and focused
7. **Write descriptive commit messages**
8. **Update documentation** when changing features

## Getting Help

- **Documentation**: Check README.md and DOCKER.md
- **Issues**: Open an issue on GitHub
- **Code Style**: Follow existing patterns in the codebase

## Next Steps

- Read [README.md](README.md) for project overview
- Read [DOCKER.md](DOCKER.md) for Docker details
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
