# Docker Setup Guide for Euro Bakshish

This guide explains how to run the Euro Bakshish application in Docker.

## Quick Start

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

### Using Docker directly

```bash
# Build the image
docker build -t euro_bakshish .

# Run the container
docker run -d \
  --name euro_bakshish_app \
  -p 3000:3000 \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  euro_bakshish
```

## Important Notes

### First Run Initialization

On the first run, the NextPy framework needs to initialize and download dependencies. This process:
- Takes 2-3 minutes
- Downloads Node.js dependencies
- Compiles the frontend

Monitor the initialization:
```bash
docker logs -f euro_bakshish_app
```

Wait for the message: "App running at http://localhost:3000"

### Accessing the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs
- **API Endpoints**: http://localhost:8000/api/

### Data Persistence

The application data is stored in the `./data` directory which is mounted as a volume. This ensures your database persists across container restarts.

## Configuration for Nginx Reverse Proxy

If you want to run this behind nginx, configure your nginx to proxy to:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`

Example nginx configuration:

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
}
```

## Troubleshooting

### Container Exits Immediately

Check the logs:
```bash
docker logs euro_bakshish_app
```

### Port Already in Use

If ports 3000 or 8000 are already in use, modify the port mappings:
```bash
docker run -d \
  --name euro_bakshish_app \
  -p 8080:3000 \
  -p 8081:8000 \
  -v $(pwd)/data:/app/data \
  euro_bakshish
```

### Rebuilding After Code Changes

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Development vs Production

For development, it's recommended to run the application locally without Docker for faster iteration:

```bash
pip install -r requirements-nextpy.txt
python euro_bakshish_app.py
```

Docker is ideal for production deployment on your home server.
