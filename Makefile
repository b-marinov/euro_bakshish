.PHONY: help build up down logs restart clean test migrate shell db-shell backup restore

# Default target
help:
	@echo "Euro Bakshish - Docker Commands"
	@echo "================================"
	@echo ""
	@echo "Production Commands:"
	@echo "  make build       - Build all Docker images"
	@echo "  make up          - Start all services in production mode"
	@echo "  make down        - Stop all services"
	@echo "  make logs        - View logs from all services"
	@echo "  make restart     - Restart all services"
	@echo "  make clean       - Stop and remove all containers, networks, and volumes"
	@echo ""
	@echo "Development Commands:"
	@echo "  make dev         - Start services in development mode (hot reload)"
	@echo "  make dev-down    - Stop development services"
	@echo "  make dev-logs    - View development logs"
	@echo ""
	@echo "Database Commands:"
	@echo "  make migrate     - Run database migrations"
	@echo "  make makemigrations - Create new migrations"
	@echo "  make db-shell    - Open PostgreSQL shell"
	@echo "  make backup      - Backup database to backup.sql"
	@echo "  make restore     - Restore database from backup.sql"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make test        - Run backend tests"
	@echo "  make test-web    - Run web frontend tests"
	@echo "  make test-all    - Run all tests (backend, db, health checks)"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make shell       - Open Django shell"
	@echo "  make bash        - Open backend container bash shell"
	@echo "  make createsuperuser - Create Django superuser"
	@echo "  make ps          - Show running containers"
	@echo "  make stats       - Show container resource usage"

# Production Commands
build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started!"
	@echo "Web: http://localhost"
	@echo "API: http://localhost:8000/api/"
	@echo "Admin: http://localhost:8000/admin/"

down:
	docker-compose down

logs:
	docker-compose logs -f

restart:
	docker-compose restart

clean:
	docker-compose down -v
	docker-compose down --rmi local

# Development Commands
dev:
	docker-compose -f docker-compose.dev.yml up
	@echo "Development services started!"
	@echo "Web: http://localhost:3000"
	@echo "API: http://localhost:8000/api/"

dev-build:
	docker-compose -f docker-compose.dev.yml build

dev-down:
	docker-compose -f docker-compose.dev.yml down

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

# Database Commands
migrate:
	docker-compose exec backend python manage.py migrate

makemigrations:
	docker-compose exec backend python manage.py makemigrations

db-shell:
	docker-compose exec db psql -U postgres -d euro_bakshish

backup:
	docker-compose exec db pg_dump -U postgres euro_bakshish > backup.sql
	@echo "Database backed up to backup.sql"

restore:
	@echo "Restoring database from backup.sql..."
	cat backup.sql | docker-compose exec -T db psql -U postgres euro_bakshish
	@echo "Database restored"

# Testing Commands
test:
	docker-compose exec backend pytest

test-web:
	docker-compose exec web npm test

test-coverage:
	docker-compose exec backend pytest --cov=apps --cov-report=html

test-all:
	@echo "Running all tests..."
	@echo "1. Backend tests with coverage..."
	docker-compose exec backend pytest --cov=apps --cov-report=term
	@echo "\n2. Database connectivity test..."
	docker-compose exec db psql -U postgres -d euro_bakshish -c "SELECT 1;"
	@echo "\n3. Backend API health check..."
	curl -f http://localhost:8000/api/ || echo "Backend API check failed"
	@echo "\n4. Frontend health check..."
	curl -f http://localhost/ || echo "Frontend check failed"
	@echo "\nAll tests completed!"

# Utility Commands
shell:
	docker-compose exec backend python manage.py shell

bash:
	docker-compose exec backend bash

createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

ps:
	docker-compose ps

stats:
	docker stats

# Individual service management
backend-logs:
	docker-compose logs -f backend

web-logs:
	docker-compose logs -f web

db-logs:
	docker-compose logs -f db

backend-restart:
	docker-compose restart backend

web-restart:
	docker-compose restart web

db-restart:
	docker-compose restart db
