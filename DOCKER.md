# Docker Setup Guide for Euro Bakshish

Complete guide for running Euro Bakshish in Docker with development, testing, and production configurations.

## Table of Contents

- [Quick Start](#quick-start)
- [Docker Environments](#docker-environments)
- [Production Deployment](#production-deployment)
- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Using Make (Recommended)

```bash
# Production
make build && make up

# Development
make dev-up

# Testing
make test
```

### Using Docker Compose Directly

```bash
# Production
docker compose up -d

# Development
docker compose -f docker-compose.dev.yml up

# Testing
docker compose -f docker-compose.test.yml run --rm euro_bakshish_test
```

## Docker Environments

We provide three separate Docker environments:

### 1. Production Environment

**File**: `docker-compose.yml`, `Dockerfile`

- Optimized for deployment
- Minimal image size
- Security hardened (non-root user)
- Health checks enabled
- Persistent data volumes

**Usage**:
```bash
make up
# or
docker compose up -d
```

### 2. Development Environment

**File**: `docker-compose.dev.yml`, `Dockerfile.dev`

- Code mounted as volume for hot-reload
- All development tools included
- Debug logging enabled
- Faster iteration

**Usage**:
```bash
make dev-up
# or
docker compose -f docker-compose.dev.yml up
```

### 3. Test Environment

**File**: `docker-compose.test.yml`, `Dockerfile.test`

- Isolated test database
- All test dependencies included
- Coverage reporting

**Usage**:
```bash
make test
# or
docker compose -f docker-compose.test.yml run --rm euro_bakshish_test
```

## Production Deployment

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/b-marinov/euro_bakshish.git
   cd euro_bakshish
   ```

2. **Build the Docker image**
   ```bash
   docker compose build
   # or
   make build
   ```

3. **Start the application**
   ```bash
   docker compose up -d
   # or
   make up
   ```

4. **Verify it's running**
   ```bash
   docker compose logs -f
   # or
   make logs
   ```

### First Run Initialization

On the first run, NextPy needs to initialize and download dependencies. This process:
- Takes 2-3 minutes
- Downloads Node.js dependencies
- Compiles the frontend

**Monitor initialization:**
```bash
docker logs -f euro_bakshish_app
```

Wait for the message: **"App running at http://localhost:3000"**

### Accessing the Application

Once running, access:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs
- **API Endpoints**: http://localhost:8000/api/

### Data Persistence

Application data is stored in the `./data` directory which is mounted as a volume:

```yaml
volumes:
  - ./data:/app/data  # Database persists here
```

**To backup:**
```bash
tar -czf backup-$(date +%Y%m%d).tar.gz data/
```

**To restore:**
```bash
tar -xzf backup-YYYYMMDD.tar.gz
```

### Managing Production Containers

```bash
# View logs
docker compose logs -f

# Restart
docker compose restart

# Stop
docker compose down

# Stop and remove volumes (WARNING: deletes data)
docker compose down -v

# View container status
docker compose ps
```

## Development Setup

### Hot-Reload Development

The development environment mounts your code as a volume, enabling instant updates:

```bash
# Start development environment
make dev-up
# or
docker compose -f docker-compose.dev.yml up
```

**What's mounted:**
- `./euro_bakshish_app.py` - Your application code
- `./tests/` - Your tests
- `./data/` - Database (separate from production)

**What's excluded:**
- `.web/` - Generated frontend files
- `.nextpy/` - NextPy cache
- `__pycache__/` - Python cache

### Development Workflow

```bash
# 1. Start development containers
make dev-up

# 2. Make code changes in your editor
# Changes are immediately reflected in the container

# 3. View logs to see changes
make dev-logs

# 4. Run tests locally
make test-local

# 5. Stop when done
make dev-down
```

## Running Tests

### Quick Test Run

```bash
make test
```

This will:
1. Build the test Docker image
2. Run all tests with pytest
3. Show coverage report
4. Clean up test containers

### Running Specific Tests

```bash
# Run specific test file
docker compose -f docker-compose.test.yml run --rm euro_bakshish_test \
  pytest tests/test_models.py -v

# Run with pattern matching
docker compose -f docker-compose.test.yml run --rm euro_bakshish_test \
  pytest tests/ -k "test_user" -v

# Run only unit tests
docker compose -f docker-compose.test.yml run --rm euro_bakshish_test \
  pytest tests/ -m unit -v
```

### Coverage Report

```bash
make test-coverage
```

Generates HTML coverage report in `htmlcov/` directory.

## Configuration

### Environment Variables

**Production** (`docker-compose.yml`):
```yaml
environment:
  - PYTHONUNBUFFERED=1
  - DATABASE_URL=sqlite:///./data/euro_bakshish.db
  - NODE_ENV=production
```

**Development** (`docker-compose.dev.yml`):
```yaml
environment:
  - PYTHONUNBUFFERED=1
  - DATABASE_URL=sqlite:///./data/euro_bakshish.db
  - NODE_ENV=development
```

### Custom Configuration

Create a `.env` file for custom settings:

```bash
# .env
DATABASE_URL=sqlite:///./data/euro_bakshish.db
NODE_ENV=production
LOGLEVEL=info
```

Then reference in docker-compose.yml:

```yaml
env_file:
  - .env
```

### Port Configuration

To change ports, edit `docker-compose.yml`:

```yaml
ports:
  - "8080:3000"  # Frontend on 8080
  - "8081:8000"  # Backend on 8081
```

### Health Checks

Production container includes health checks:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/ping", "||", "exit", "1"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s
```

View health status:
```bash
docker inspect --format='{{.State.Health.Status}}' euro_bakshish_app
```

## Nginx Reverse Proxy

### Basic Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API Documentation
    location /docs {
        proxy_pass http://localhost:8000/docs;
        proxy_set_header Host $host;
    }
}
```

### HTTPS with Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Certbot will automatically configure nginx for HTTPS
```

## Troubleshooting

### Container Exits Immediately

**Check logs:**
```bash
docker logs euro_bakshish_app
# or
make logs
```

**Common causes:**
- Missing dependencies
- Database initialization failed
- Port already in use

### Port Already in Use

**Find process using port:**
```bash
# Linux/Mac
lsof -i :3000
lsof -i :8000

# Windows
netstat -ano | findstr :3000
netstat -ano | findstr :8000
```

**Solution**: Change port mapping in docker-compose.yml

### Container Stuck Initializing

NextPy initialization can take 2-3 minutes on first run.

**Check progress:**
```bash
docker logs -f euro_bakshish_app
```

**If stuck for >5 minutes**, restart:
```bash
docker compose down
docker compose up -d
```

### Database Issues

**Reset database:**
```bash
# Stop containers
docker compose down

# Remove database files
rm -rf data/*.db*

# Restart
docker compose up -d
```

### Out of Memory

**Check container memory:**
```bash
docker stats euro_bakshish_app
```

**Increase memory limit:**
```yaml
services:
  euro_bakshish:
    mem_limit: 2g
```

### Rebuilding After Code Changes

```bash
# Rebuild and restart
docker compose down
docker compose build --no-cache
docker compose up -d

# Or using Make
make clean
make build
make up
```

### Viewing Container Contents

```bash
# Execute shell
docker exec -it euro_bakshish_app /bin/bash

# View files
docker exec -it euro_bakshish_app ls -la /app

# View logs directly
docker exec -it euro_bakshish_app cat /app/logs/app.log
```

## Best Practices

### Production Deployment

1. **Use named volumes** for important data
2. **Enable health checks** for automatic recovery
3. **Set resource limits** to prevent runaway containers
4. **Use restart policies** for automatic recovery
5. **Regular backups** of data directory
6. **Monitor logs** for errors
7. **Keep images updated** for security

### Development

1. **Use dev compose** for development
2. **Don't commit** `.env` files with secrets
3. **Use volumes** for code mounting
4. **Clean up** regularly with `make clean`

### Security

1. **Run as non-root user** (already configured)
2. **Don't expose** unnecessary ports
3. **Use HTTPS** in production
4. **Keep dependencies updated**
5. **Use secrets management** for sensitive data

## Advanced Topics

### Multi-Container Setup

For production with PostgreSQL:

```yaml
services:
  euro_bakshish:
    # ... existing config ...
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/eurodb
    depends_on:
      - postgres

  postgres:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=eurodb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass

volumes:
  postgres_data:
```

### Docker Compose Override

Create `docker-compose.override.yml` for local customizations (not committed):

```yaml
services:
  euro_bakshish:
    ports:
      - "8080:3000"  # Custom port
    environment:
      - DEBUG=true
```

### Building for Different Platforms

```bash
# Build for ARM64 (Raspberry Pi, Apple Silicon)
docker buildx build --platform linux/arm64 -t euro_bakshish:arm64 .

# Build for AMD64 (most servers)
docker buildx build --platform linux/amd64 -t euro_bakshish:amd64 .

# Build multi-platform
docker buildx build --platform linux/amd64,linux/arm64 -t euro_bakshish:latest .
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [NextPy Documentation](https://nextpy.org/)
- [Development Guide](DEVELOPMENT.md)
- [README](README.md)
