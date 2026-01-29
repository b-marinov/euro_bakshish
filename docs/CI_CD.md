# CI/CD Pipeline Documentation

This document describes the continuous integration and deployment pipeline for the Euro Bakshish project.

## Overview

The CI/CD pipeline consists of multiple automated workflows that ensure code quality, run tests, and validate Docker deployments.

## Workflows

### 1. Backend Unit Tests (`backend-tests.yml`)

**Triggers:**
- Push to `main` or `develop` branches (when backend files change)
- Pull requests to `main` or `develop` (when backend files change)

**What it does:**
- Sets up Python 3.11 environment
- Installs backend dependencies
- Runs code linting with flake8
- Sets up PostgreSQL test database
- Runs Django migrations
- Executes pytest with coverage reporting
- Uploads coverage reports to Codecov
- Archives coverage HTML reports as artifacts

**Environment:**
- PostgreSQL 15 (alpine)
- Python 3.11
- Ubuntu latest

**Key Features:**
- Coverage reporting with multiple formats (XML, HTML, terminal)
- Automatic artifact upload for coverage reports
- Database health checks

### 2. Frontend Unit Tests (`frontend-tests.yml`)

**Triggers:**
- Push to `main` or `develop` branches (when web files change)
- Pull requests to `main` or `develop` (when web files change)

**What it does:**
- Sets up Node.js 18 environment
- Installs npm dependencies
- Runs linting (if configured)
- Executes React tests with coverage
- Builds production application
- Uploads coverage reports to Codecov
- Archives build artifacts

**Environment:**
- Node.js 18
- Ubuntu latest

**Key Features:**
- npm cache for faster builds
- Coverage reporting
- Production build validation
- Artifact archiving

### 3. Docker Build and Test (`docker-tests.yml`)

**Triggers:**
- Push to `main` or `develop` branches (when Docker-related files change)
- Pull requests to `main` or `develop` (when Docker-related files change)

**What it does:**
- **Job 1: Docker Build**
  - Builds backend Docker image
  - Builds frontend Docker image
  - Uses BuildKit cache for optimization
  
- **Job 2: Docker Compose Test**
  - Starts full stack with docker-compose
  - Waits for services to be healthy
  - Checks backend API accessibility
  - Checks frontend accessibility
  - Runs pytest inside Docker container
  - Validates database connectivity
  - Shows logs on failure

**Environment:**
- Docker Buildx
- Docker Compose
- Ubuntu latest

**Key Features:**
- Multi-stage build validation
- Health checks for all services
- Automated service startup and teardown
- Comprehensive logging on failures
- Build cache optimization

### 4. End-to-End Tests (`e2e-tests.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual workflow dispatch

**What it does:**
- Starts full application stack with Docker Compose
- Waits for all services to be ready
- Installs Playwright for browser testing
- Runs E2E tests that verify:
  - Frontend loads correctly
  - API is accessible
  - API documentation loads
  - Register page works
  - Login page works
- Captures screenshots on failure
- Shows detailed logs on failure

**Environment:**
- Docker Compose
- Playwright (Chromium)
- Node.js 18
- Python 3.11
- Ubuntu latest

**Key Features:**
- Real browser testing with Playwright
- Full stack integration testing
- Automatic screenshot capture on failures
- Comprehensive service health checks
- 30-minute timeout for long-running tests

### 5. Main CI Pipeline (`ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

**What it does:**
- Orchestrates all other workflows
- Runs backend, frontend, and Docker tests in parallel
- Runs E2E tests after unit tests pass
- Provides summary of all test results

**Key Features:**
- Parallel test execution for speed
- Sequential E2E tests (after unit tests)
- Single status check for all tests

## Status Badges

Add these badges to your README.md:

```markdown
![Backend Tests](https://github.com/b-marinov/euro_bakshish/workflows/Backend%20Unit%20Tests/badge.svg)
![Frontend Tests](https://github.com/b-marinov/euro_bakshish/workflows/Frontend%20Unit%20Tests/badge.svg)
![Docker Tests](https://github.com/b-marinov/euro_bakshish/workflows/Docker%20Build%20and%20Test/badge.svg)
![E2E Tests](https://github.com/b-marinov/euro_bakshish/workflows/End-to-End%20Tests/badge.svg)
```

## Running Tests Locally

### Backend Tests
```bash
cd backend
pytest --cov=apps
```

### Frontend Tests
```bash
cd web
npm test -- --coverage
```

### Docker Tests
```bash
docker-compose up -d
docker-compose exec backend pytest
```

### E2E Tests
```bash
# Start services
docker-compose up -d

# Wait for services
sleep 45

# Install Playwright
npm install -g playwright
playwright install chromium

# Run tests
node e2e-tests/test.spec.js

# Cleanup
docker-compose down
```

## Viewing Test Results

### In GitHub Actions

1. Go to the "Actions" tab in your repository
2. Click on a workflow run
3. View logs for each job
4. Download artifacts (coverage reports, screenshots)

### Coverage Reports

Coverage reports are automatically uploaded to Codecov and available as downloadable artifacts in GitHub Actions.

## Environment Variables

The CI pipeline uses these environment variables:

**Backend:**
- `SECRET_KEY`: Test secret key
- `DEBUG`: Set to True for tests
- `DB_NAME`: Test database name
- `DB_USER`: postgres
- `DB_PASSWORD`: postgres
- `DB_HOST`: localhost (or db in Docker)
- `DB_PORT`: 5432
- `CORS_ALLOWED_ORIGINS`: Allowed CORS origins

**Frontend:**
- `REACT_APP_API_URL`: Backend API URL
- `CI`: Set to true for CI environment

## Troubleshooting

### Tests Fail in CI but Pass Locally

1. Check environment variables
2. Verify database connectivity
3. Check for race conditions
4. Review service startup order

### Docker Compose Fails to Start

1. Check Docker image build logs
2. Verify health check configurations
3. Increase wait times if services are slow
4. Check for port conflicts

### E2E Tests Timeout

1. Increase timeout in workflow (default 30 minutes)
2. Check if services are starting correctly
3. Review Playwright logs
4. Check screenshot artifacts for clues

### Coverage Upload Fails

1. Verify Codecov token (if using private repo)
2. Check coverage file paths
3. Ensure coverage files are generated

## Best Practices

1. **Keep tests fast**: Aim for <5 minutes total test time
2. **Use caching**: npm and pip caches speed up builds
3. **Fail fast**: Run quick tests first
4. **Parallel execution**: Run independent tests in parallel
5. **Artifact collection**: Save logs and screenshots on failures
6. **Clear error messages**: Make failures easy to diagnose

## Future Improvements

- [ ] Add performance testing
- [ ] Add security scanning (SAST/DAST)
- [ ] Add dependency vulnerability scanning
- [ ] Add automatic deployment on successful tests
- [ ] Add integration with Slack/Discord for notifications
- [ ] Add mobile app build and test workflow
- [ ] Add database migration validation
- [ ] Add API contract testing

## Maintenance

### Updating Dependencies

When updating dependencies, remember to:
1. Update version in workflow files
2. Test locally before pushing
3. Check for breaking changes in GitHub Actions

### Adding New Tests

1. Add test files to appropriate directory
2. Update workflow if new test commands needed
3. Verify tests run in CI
4. Update documentation

## Security

- Secrets are stored in GitHub Secrets (not in workflow files)
- Test databases use temporary credentials
- Docker images are not pushed to registry during tests
- Artifacts are automatically deleted after retention period

## Support

For issues with CI/CD:
1. Check workflow logs in GitHub Actions
2. Review this documentation
3. Open an issue with CI logs attached
