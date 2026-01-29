#!/bin/bash

# validate-docker-setup.sh
# This script validates the Docker setup for Euro Bakshish application

set -e

echo "======================================"
echo "Euro Bakshish Docker Setup Validator"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check functions
check_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
}

check_warn() {
    echo -e "${YELLOW}!${NC} $1"
}

# 1. Check Docker is installed
echo "1. Checking Docker installation..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    check_pass "Docker is installed: $DOCKER_VERSION"
else
    check_fail "Docker is not installed. Please install Docker Desktop from https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# 2. Check Docker Compose is available
echo ""
echo "2. Checking Docker Compose..."
if docker compose version &> /dev/null; then
    COMPOSE_VERSION=$(docker compose version)
    check_pass "Docker Compose is available: $COMPOSE_VERSION"
else
    check_fail "Docker Compose is not available. Please update Docker to the latest version."
    exit 1
fi

# 3. Check docker-compose.yml exists
echo ""
echo "3. Checking docker-compose.yml..."
if [ -f "docker-compose.yml" ]; then
    check_pass "docker-compose.yml found"
else
    check_fail "docker-compose.yml not found. Please run this script from the project root directory."
    exit 1
fi

# 4. Validate docker-compose.yml syntax
echo ""
echo "4. Validating docker-compose.yml syntax..."
if docker compose config > /dev/null 2>&1; then
    check_pass "docker-compose.yml syntax is valid"
else
    check_fail "docker-compose.yml has syntax errors"
    echo "Run 'docker compose config' to see the errors"
    exit 1
fi

# 5. Check backend Dockerfile
echo ""
echo "5. Checking backend Dockerfile..."
if [ -f "backend/Dockerfile" ]; then
    check_pass "backend/Dockerfile found"
    
    # Check if ENTRYPOINT is set
    if grep -q "ENTRYPOINT" backend/Dockerfile; then
        check_pass "ENTRYPOINT directive found in Dockerfile"
    else
        check_warn "ENTRYPOINT directive not found in Dockerfile"
    fi
else
    check_fail "backend/Dockerfile not found"
    exit 1
fi

# 6. Check entrypoint.sh exists and is executable
echo ""
echo "6. Checking backend entrypoint script..."
if [ -f "backend/entrypoint.sh" ]; then
    check_pass "backend/entrypoint.sh found"
    
    if [ -x "backend/entrypoint.sh" ]; then
        check_pass "backend/entrypoint.sh is executable"
    else
        check_warn "backend/entrypoint.sh is not executable"
        echo "   Run: chmod +x backend/entrypoint.sh"
    fi
else
    check_fail "backend/entrypoint.sh not found"
    exit 1
fi

# 7. Check for conflicting command in docker-compose.yml
echo ""
echo "7. Checking for configuration conflicts..."
if grep -A 5 "^  backend:" docker-compose.yml | grep -q "command:"; then
    check_warn "Found 'command:' directive in backend service"
    echo "   This may conflict with the ENTRYPOINT in Dockerfile"
    echo "   Consider removing the 'command:' line from docker-compose.yml"
else
    check_pass "No conflicting command directive found"
fi

# 8. Check ports are available (informational only)
echo ""
echo "8. Checking port availability..."
check_port() {
    PORT=$1
    # Try multiple methods for cross-platform compatibility
    if command -v lsof >/dev/null 2>&1; then
        # Unix/Linux/Mac using lsof
        if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
            check_warn "Port $PORT may be in use"
            return 1
        fi
    elif command -v netstat >/dev/null 2>&1; then
        # Try netstat (works on most systems)
        if netstat -tuln 2>/dev/null | grep -q ":$PORT "; then
            check_warn "Port $PORT may be in use"
            return 1
        fi
    elif command -v ss >/dev/null 2>&1; then
        # Modern Linux using ss
        if ss -tuln 2>/dev/null | grep -q ":$PORT "; then
            check_warn "Port $PORT may be in use"
            return 1
        fi
    else
        # No port checking tool available
        check_warn "Cannot verify port $PORT availability (no lsof/netstat/ss found)"
        return 0
    fi
    check_pass "Port $PORT appears available"
    return 0
}

echo "   Note: Port checks are informational. Docker will report errors if ports are unavailable."
check_port 5432 || echo "   → PostgreSQL port may conflict"
check_port 8000 || echo "   → Backend API port may conflict"
check_port 80 || echo "   → Frontend port may conflict (often requires elevated privileges)"

# 9. Check Docker daemon is running
echo ""
echo "9. Checking Docker daemon..."
if docker ps > /dev/null 2>&1; then
    check_pass "Docker daemon is running"
else
    check_fail "Docker daemon is not running. Please start Docker Desktop."
    exit 1
fi

# Summary
echo ""
echo "======================================"
echo "Validation Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Start the application: docker compose up -d"
echo "2. Check logs: docker compose logs -f"
echo "3. Access the API docs: http://localhost:8000/api/docs/"
echo "4. Access the web app: http://localhost"
echo ""
echo "For troubleshooting, see docs/DOCKER.md"
