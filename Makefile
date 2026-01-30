# Makefile for Euro Bakshish - Docker-oriented development

.PHONY: help build up down logs test clean dev dev-build dev-up dev-down format lint pre-commit-install

# Default target
help:
	@echo "Euro Bakshish - Available Commands:"
	@echo ""
	@echo "Production:"
	@echo "  make build          - Build production Docker image"
	@echo "  make up             - Start production containers"
	@echo "  make down           - Stop production containers"
	@echo "  make logs           - View production container logs"
	@echo ""
	@echo "Development:"
	@echo "  make dev-build      - Build development Docker image"
	@echo "  make dev-up         - Start development containers with hot-reload"
	@echo "  make dev-down       - Stop development containers"
	@echo "  make dev-logs       - View development container logs"
	@echo ""
	@echo "Testing:"
	@echo "  make test           - Run tests in Docker"
	@echo "  make test-local     - Run tests locally (requires deps)"
	@echo "  make test-watch     - Run tests in watch mode"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format         - Format code with black and isort"
	@echo "  make lint           - Run linters (flake8, mypy)"
	@echo "  make pre-commit-install - Install pre-commit hooks"
	@echo "  make pre-commit     - Run pre-commit on all files"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Remove containers, volumes, and generated files"
	@echo "  make clean-all      - Deep clean including images"

# Production targets
build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

restart:
	docker compose restart

# Development targets
dev-build:
	docker compose -f docker-compose.dev.yml build

dev-up:
	docker compose -f docker-compose.dev.yml up

dev-down:
	docker compose -f docker-compose.dev.yml down

dev-logs:
	docker compose -f docker-compose.dev.yml logs -f

# Testing targets
test:
	docker compose -f docker-compose.test.yml build
	docker compose -f docker-compose.test.yml run --rm euro_bakshish_test
	docker compose -f docker-compose.test.yml down -v

test-local:
	pytest tests/ -v

test-watch:
	pytest tests/ -v --watch

test-coverage:
	docker compose -f docker-compose.test.yml run --rm euro_bakshish_test \
		pytest tests/ --cov=. --cov-report=html --cov-report=term

# Code quality targets
format:
	black euro_bakshish_app.py tests/
	isort euro_bakshish_app.py tests/

lint:
	flake8 euro_bakshish_app.py tests/ --max-line-length=100 --extend-ignore=E203,W503
	mypy euro_bakshish_app.py --ignore-missing-imports

pre-commit-install:
	pre-commit install

pre-commit:
	pre-commit run --all-files

# Cleanup targets
clean:
	docker compose down -v
	docker compose -f docker-compose.dev.yml down -v
	docker compose -f docker-compose.test.yml down -v
	rm -rf .web .nextpy __pycache__ .pytest_cache .mypy_cache .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.db" -delete 2>/dev/null || true
	find . -type f -name "*.db-shm" -delete 2>/dev/null || true
	find . -type f -name "*.db-wal" -delete 2>/dev/null || true

clean-all: clean
	docker rmi euro_bakshish:latest euro_bakshish:dev euro_bakshish:test 2>/dev/null || true
	docker system prune -f

# Install dependencies locally
install:
	pip install -r requirements-nextpy.txt -r requirements-dev.txt

# Run application locally (without Docker)
run-local:
	python euro_bakshish_app.py

# Database management
db-init:
	python -c "from euro_bakshish_app import init_db; init_db()"

# Quick start for new developers
quickstart: pre-commit-install dev-build dev-up
	@echo "✅ Development environment is ready!"
	@echo "📝 Access the app at http://localhost:3000"
	@echo "📚 API docs at http://localhost:8000/docs"
