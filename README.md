# Euro Bakshish - Ride Sharing Application

A comprehensive ride-sharing platform built with **NextPy** - a pure Python full-stack framework that handles both backend and frontend in a single, unified codebase.

[![CI/CD Pipeline](https://github.com/b-marinov/euro_bakshish/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/b-marinov/euro_bakshish/actions)
[![Docker Tests](https://github.com/b-marinov/euro_bakshish/workflows/Docker%20Tests/badge.svg)](https://github.com/b-marinov/euro_bakshish/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## ✨ Features

- **User Profiles**: Create and manage profiles as either a passenger or driver
- **Trip Planning**: Select start and end locations for trips
- **Trip Completion**: Complete trips with mutual ratings between passengers and drivers
- **Trip History**: Track complete history of all trips for both drivers and passengers
- **Rating System**: Maintain user ratings based on reviews from completed trips

## 🚀 Quick Start

### Prerequisites

Choose one option:
- **Docker** (Recommended for consistency)
- **Python 3.10+** (For local development)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/b-marinov/euro_bakshish.git
cd euro_bakshish

# Start with Docker Compose
docker compose up -d

# Or use Make for convenience
make up
```

**Access the application:**
- 🌐 **Frontend**: http://localhost:3000
- 📚 **API Docs**: http://localhost:8000/docs
- 🔧 **API**: http://localhost:8000/api/

### Option 2: Local Development

```bash
# Clone the repository
git clone https://github.com/b-marinov/euro_bakshish.git
cd euro_bakshish

# Install dependencies
pip install -r requirements-nextpy.txt

# Run the application
python euro_bakshish_app.py
```

## 🛠️ Development

### Quick Development Setup

```bash
# Using Make (Recommended)
make quickstart

# Or manually with Docker Compose
docker compose -f docker-compose.dev.yml up
```

This starts a development environment with:
- ✅ Hot-reload on code changes
- ✅ Debug logging enabled
- ✅ All dev tools included
- ✅ Code mounted as volume

### Available Commands

We provide a Makefile with common commands:

```bash
# Production
make build          # Build production Docker image
make up             # Start production containers
make down           # Stop containers
make logs           # View logs

# Development
make dev-up         # Start dev environment with hot-reload
make dev-down       # Stop dev environment
make dev-logs       # View dev logs

# Testing
make test           # Run tests in Docker
make test-local     # Run tests locally
make test-coverage  # Generate coverage report

# Code Quality
make format         # Format code with Black and isort
make lint           # Run linters
make pre-commit     # Run pre-commit hooks

# Cleanup
make clean          # Remove containers and artifacts
make clean-all      # Deep clean including images
```

For more details, see [DEVELOPMENT.md](DEVELOPMENT.md).

## 🧪 Testing

### Run Tests

```bash
# In Docker (isolated environment)
make test

# Locally (faster iteration)
make test-local

# With coverage report
make test-coverage
```

### Test Structure

```
tests/
├── conftest.py          # Test fixtures and configuration
├── test_models.py       # Database model unit tests
├── test_integration.py  # Application workflow tests
└── test_docker.py       # Docker configuration tests
```

## 📋 Code Quality

This project uses modern Python development tools:

- **Black**: Code formatting
- **isort**: Import sorting
- **Flake8**: Linting
- **Mypy**: Type checking
- **Pre-commit**: Automated checks before commits

### Setup Code Quality Tools

```bash
# Install pre-commit hooks
make pre-commit-install

# Format code
make format

# Run linters
make lint
```

Pre-commit hooks run automatically on `git commit` to ensure code quality.

## 🐳 Docker

We provide three Docker environments:

1. **Production** - Optimized for deployment
   ```bash
   make up
   ```

2. **Development** - Hot-reload with mounted code
   ```bash
   make dev-up
   ```

3. **Testing** - Isolated test environment
   ```bash
   make test
   ```

For complete Docker documentation, see [DOCKER.md](DOCKER.md).

## 📁 Project Structure

```
euro_bakshish/
├── .github/
│   └── workflows/          # CI/CD workflows
├── tests/                  # Test suite
├── euro_bakshish_app.py   # Main NextPy application
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

## 🏗️ Technology Stack

- **Framework**: [NextPy](https://nextpy.org/) - Pure Python full-stack framework
- **Backend**: FastAPI (built into NextPy)
- **Frontend**: React components via NextPy (no JavaScript needed!)
- **Database**: SQLModel with SQLite/PostgreSQL support
- **State Management**: Built-in NextPy state management
- **Authentication**: Session-based with bcrypt password hashing
- **Container**: Docker with multi-stage builds
- **CI/CD**: GitHub Actions

### Why NextPy?

- ✅ **Single Language**: Everything in Python - no context switching
- ✅ **Unified Codebase**: Frontend and backend in one file
- ✅ **Type Safety**: Pydantic models ensure data validation
- ✅ **Auto-Generated API**: REST API created automatically
- ✅ **Hot Reload**: Fast development with instant updates
- ✅ **Easy Deployment**: Single Python app to deploy

## 🔒 Security

This application implements security best practices:

- ✅ Secure password hashing with bcrypt
- ✅ Session-based authentication
- ✅ Non-root Docker user
- ✅ Input validation with Pydantic
- ✅ SQL injection protection via SQLModel
- ⚠️ **Production**: Use HTTPS and configure secrets properly

See the [Security Guide](docs/SECURITY.md) for more details (if available).

## 📚 Documentation

- **[README.md](README.md)** - This file (overview and quick start)
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Complete development guide
- **[DOCKER.md](DOCKER.md)** - Docker setup and deployment
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[QUICKSTART.md](QUICKSTART.md)** - Quick reference guide

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/my-feature`
3. **Make your changes**
4. **Run tests**: `make test`
5. **Format code**: `make format`
6. **Commit**: `git commit -m "Add my feature"`
7. **Push**: `git push origin feature/my-feature`
8. **Open a Pull Request**

Pre-commit hooks will automatically:
- Format code with Black
- Sort imports with isort
- Run linters
- Check for common issues

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## 🧩 CI/CD

Automated testing runs on every push and pull request:

- ✅ Code quality checks (Black, isort, Flake8)
- ✅ Type checking (Mypy)
- ✅ Unit and integration tests
- ✅ Docker build and validation
- ✅ Pre-commit hook verification

## 📝 API Documentation

When the application is running, access interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

All API endpoints are automatically generated by NextPy based on the application state:

- **Authentication**: Login, Register, Logout
- **Users**: Profile management
- **Trips**: Create, view, accept, manage trips
- **Reviews**: Rate and review completed trips

## 🌐 Deployment

### Production Deployment

```bash
# Using Docker Compose (Recommended)
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

### With Nginx Reverse Proxy

See [DOCKER.md](DOCKER.md) for complete Nginx configuration examples.

### Environment Variables

```bash
DATABASE_URL=sqlite:///./data/euro_bakshish.db  # Database connection
NODE_ENV=production                              # Environment
PYTHONUNBUFFERED=1                              # Python output buffering
```

## 🐛 Troubleshooting

### Common Issues

**Container exits immediately:**
```bash
docker logs euro_bakshish_app
```

**Port already in use:**
```bash
# Change ports in docker-compose.yml
ports:
  - "8080:3000"  # Use different port
```

**Tests failing:**
```bash
# Clean and rebuild
make clean
make test
```

See [DOCKER.md](DOCKER.md) for more troubleshooting tips.

## 📊 Project Status

- ✅ Active development
- ✅ Docker-oriented architecture
- ✅ Automated testing and CI/CD
- ✅ Code quality tools integrated
- ✅ Production-ready
