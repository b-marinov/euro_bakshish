# Docker Deployment Guide

This guide explains how to run the Euro Bakshish application using Docker on your PC.

## Architecture Overview

The Docker setup consists of three main services:

1. **PostgreSQL Database** (`db`)
   - Image: `postgres:15-alpine`
   - Port: 5432
   - Stores all application data
   - Includes health checks for reliable startup

2. **Django Backend** (`backend`)
   - Built from: `backend/Dockerfile`
   - Port: 8000
   - Entry point: `backend/entrypoint.sh` (automatically runs migrations, collects static files, and starts server)
   - Depends on: Database (waits for it to be healthy)
   - Serves: REST API and admin interface

3. **React Frontend** (`web`)
   - Built from: `web/Dockerfile`
   - Port: 80
   - Nginx server serving static React build
   - Depends on: Backend API

All services communicate through a dedicated Docker network: `euro_bakshish_network`

## Prerequisites

- **Docker**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)
- **Minimum Requirements**: 4GB RAM, 10GB disk space

## Quick Start (Production Mode)

Run the entire application stack with one command:

```bash
docker-compose up -d
```

This will start:
- **PostgreSQL database** on port 5432
- **Django backend** on port 8000
- **React web frontend** on port 80

### Access the Application

- **Web Frontend**: http://localhost
- **Backend API**: http://localhost:8000/api/
- **API Documentation**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/
  - Username: `admin`
  - Password: `admin123`

### Stop the Application

```bash
docker-compose down
```

### Stop and Remove All Data

```bash
docker-compose down -v
```

## Development Mode (Hot Reload)

For active development with automatic code reloading:

```bash
docker-compose -f docker-compose.dev.yml up
```

This provides:
- **Hot reload** for both backend and frontend
- **Source code mounted** as volumes
- **React development server** on port 3000
- **Django development server** with auto-reload

### Access Development Environment

- **Web Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/

### Stop Development Environment

```bash
docker-compose -f docker-compose.dev.yml down
```

## Docker Commands Reference

### Building Images

```bash
# Build all images
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build web

# Build without cache (fresh build)
docker-compose build --no-cache
```

### Managing Services

```bash
# Start services in background
docker-compose up -d

# Start specific service
docker-compose up -d backend

# View logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend

# Restart a service
docker-compose restart backend

# Stop all services
docker-compose stop

# Remove stopped containers
docker-compose down
```

### Database Operations

```bash
# Create migrations
docker-compose exec backend python manage.py makemigrations

# Apply migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Access PostgreSQL shell
docker-compose exec db psql -U postgres -d euro_bakshish

# Backup database
docker-compose exec db pg_dump -U postgres euro_bakshish > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres euro_bakshish < backup.sql
```

### Accessing Container Shells

```bash
# Backend (Django) shell
docker-compose exec backend bash
docker-compose exec backend python manage.py shell

# Web frontend container
docker-compose exec web sh

# Database container
docker-compose exec db psql -U postgres
```

### Viewing Container Status

```bash
# List running containers
docker-compose ps

# View resource usage
docker stats

# Inspect specific container
docker inspect euro_bakshish_backend
```

## Configuration

### Environment Variables

Edit the `docker-compose.yml` file to customize:

```yaml
environment:
  - SECRET_KEY=your-secret-key-here
  - DEBUG=False  # Set to False for production
  - ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
  - CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### Ports

Change exposed ports in `docker-compose.yml`:

```yaml
ports:
  - "8080:8000"  # Map host:container
```

### Volumes

Data persistence is handled by Docker volumes:
- `postgres_data`: Database files
- `static_volume`: Django static files
- `media_volume`: User uploaded files

## Production Deployment

### Security Checklist

- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Set `DEBUG=False`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Configure proper `CORS_ALLOWED_ORIGINS`
- [ ] Use HTTPS (add reverse proxy like Nginx or Traefik)
- [ ] Set strong database password
- [ ] Enable database backups
- [ ] Configure proper firewall rules
- [ ] Use Docker secrets for sensitive data

### Production Example

```yaml
environment:
  - SECRET_KEY=${SECRET_KEY}
  - DEBUG=False
  - ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
  - DB_PASSWORD=${DB_PASSWORD}
  - CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

Create a `.env` file:
```
SECRET_KEY=your-production-secret-key
DB_PASSWORD=strong-database-password
```

Run with:
```bash
docker-compose --env-file .env up -d
```

## Troubleshooting

### Backend container fails to start or shows "no entrypoint" error

The backend uses an entrypoint script (`backend/entrypoint.sh`) that automatically:
1. Waits for PostgreSQL to be ready
2. Runs database migrations
3. Collects static files
4. Creates a default admin user
5. Starts the Django server

**Common issues:**

```bash
# 1. Check if entrypoint script is executable
cd backend && ls -la entrypoint.sh
# Should show: -rwxr-xr-x (executable permissions)

# 2. If permissions are wrong, fix them:
chmod +x backend/entrypoint.sh

# 3. Check backend logs for detailed error
docker-compose logs backend

# 4. Verify Dockerfile has correct entrypoint
cat backend/Dockerfile | grep ENTRYPOINT
# Should show: ENTRYPOINT ["/app/entrypoint.sh"]

# 5. Rebuild backend image after fixing
docker-compose build --no-cache backend
docker-compose up -d backend
```

**Note**: The `docker-compose.yml` should NOT have a `command:` directive for the backend service, as this would override the Dockerfile's ENTRYPOINT. The entrypoint is properly configured in the Dockerfile.

### Backend won't start

```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Database not ready - wait a few seconds and restart
docker-compose restart backend

# 2. Migration errors - run migrations manually
docker-compose exec backend python manage.py migrate

# 3. Permission errors - check file permissions
ls -la backend/entrypoint.sh
```

### Frontend shows API errors

```bash
# Check backend is running
docker-compose ps

# Verify environment variable
docker-compose exec web env | grep REACT_APP_API_URL

# Rebuild frontend with correct API URL
docker-compose build web
docker-compose up -d web
```

### Database connection errors

```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Port already in use

```bash
# Find process using port
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Change port in docker-compose.yml
ports:
  - "8001:8000"
```

### Reset everything

```bash
# Stop and remove all containers, networks, and volumes
docker-compose down -v

# Remove all images
docker-compose down --rmi all

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

## Performance Optimization

### Reduce Build Time

```bash
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker-compose build
```

### Memory Limits

Add to service configuration:
```yaml
deploy:
  resources:
    limits:
      memory: 512M
```

### Multi-stage Builds

The production Dockerfile already uses multi-stage builds for smaller images.

## Monitoring

### View Resource Usage

```bash
docker stats
```

### Health Checks

Services include health checks. View status:
```bash
docker-compose ps
```

### Logs

```bash
# All services
docker-compose logs

# Specific service with timestamp
docker-compose logs -f -t backend

# Last 100 lines
docker-compose logs --tail=100
```

## Backup and Restore

### Backup

```bash
# Database backup
docker-compose exec db pg_dump -U postgres euro_bakshish > backup_$(date +%Y%m%d).sql

# Volume backup
docker run --rm -v euro_bakshish_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz /data
```

### Restore

```bash
# Database restore
cat backup.sql | docker-compose exec -T db psql -U postgres euro_bakshish

# Volume restore
docker run --rm -v euro_bakshish_postgres_data:/data -v $(pwd):/backup alpine tar xzf /backup/postgres_backup.tar.gz -C /
```

## Testing

Run tests in Docker:

```bash
# Backend tests
docker-compose exec backend pytest

# With coverage
docker-compose exec backend pytest --cov=apps

# Web tests
docker-compose exec web npm test
```

## Android Development

For Android development, connect to backend on host:
- **Windows/Mac**: Use `host.docker.internal:8000`
- **Linux**: Use `172.17.0.1:8000` (Docker bridge IP)

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

## Support

For issues or questions:
1. Check logs: `docker-compose logs`
2. Review troubleshooting section above
3. Open an issue on GitHub
