# Euro Bakshish - Quick Start with Docker 🚀

Get the entire application running in under 2 minutes!

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

That's it! No need to install Python, Node.js, PostgreSQL, or any other dependencies.

### 🪟 Windows Users - Important!

If you're on Windows, Git may have converted line endings when cloning. To ensure proper line endings for shell scripts:

```bash
# Option 1: Configure Git before cloning (recommended)
git config --global core.autocrlf input
git clone https://github.com/b-marinov/euro_bakshish.git
cd euro_bakshish

# Option 2: If already cloned, rebuild without cache
docker-compose build --no-cache
docker-compose up -d
```

The repository now includes a `.gitattributes` file that enforces correct line endings, but if you cloned before this fix, use Option 2.

## Start the Application

### Step 1: Clone the Repository

```bash
git clone https://github.com/b-marinov/euro_bakshish.git
cd euro_bakshish
```

### Step 2: Start All Services

```bash
docker-compose up -d
```

This single command will:
- ✅ Start PostgreSQL database
- ✅ Build and start Django backend
- ✅ Build and start React frontend
- ✅ Run database migrations
- ✅ Create admin user
- ✅ Set up networking between services

### Step 3: Access the Application

**Give it 30-60 seconds for initial setup, then:**

- 🌐 **Web Application**: http://localhost
- 🔧 **API**: http://localhost:8000/api/
- 📚 **API Docs**: http://localhost:8000/api/docs/
- 👤 **Admin Panel**: http://localhost:8000/admin/
  - Username: `admin`
  - Password: `admin123`

## Common Commands

```bash
# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Restart services
docker-compose restart

# View running containers
docker-compose ps
```

## Development Mode (Hot Reload)

For development with automatic code reloading:

```bash
docker-compose -f docker-compose.dev.yml up
```

Access at:
- Web: http://localhost:3000
- API: http://localhost:8000/api/

## Using Makefile (Optional but Easier)

If you have `make` installed:

```bash
make help         # Show all commands
make up           # Start services
make down         # Stop services
make logs         # View logs
make dev          # Start in development mode
make test         # Run tests
```

## Troubleshooting

### 🪟 Windows: "entrypoint.sh not found" error?

This is usually caused by Windows line ending issues. Try:

```bash
# Rebuild without cache to fix line endings
docker-compose down
docker-compose build --no-cache backend
docker-compose up -d

# Or if that doesn't work, ensure Git is configured correctly
git config core.autocrlf input
# Then re-clone the repository
```

The Dockerfile now automatically converts line endings, but if you cloned before the fix, rebuild is necessary.

### Services won't start?

```bash
# Check what's running
docker-compose ps

# View logs for errors
docker-compose logs

# Try restarting
docker-compose restart
```

### Port already in use?

Edit `docker-compose.yml` and change the port:
```yaml
ports:
  - "8080:8000"  # Change 8080 to any free port
```

### Want to start fresh?

```bash
# Stop and remove everything
docker-compose down -v

# Start again
docker-compose up -d
```

## Next Steps

1. **Register a user**: http://localhost/register
2. **Create a trip**: http://localhost/plan-trip
3. **Explore the API**: http://localhost:8000/api/docs/

## Full Documentation

- [Complete Docker Guide](docs/DOCKER.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [API Documentation](docs/API.md)

## Need Help?

- View logs: `docker-compose logs -f backend`
- Check database: `docker-compose exec db psql -U postgres -d euro_bakshish`
- Access backend shell: `docker-compose exec backend bash`

Happy coding! 🎉
