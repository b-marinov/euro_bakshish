# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Node.js and unzip
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libpq-dev \
    curl \
    unzip \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements-nextpy.txt .

# Install Python dependencies and remove build tools to reduce image size
RUN pip install --no-cache-dir -r requirements-nextpy.txt \
    && apt-get purge -y gcc g++ make \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Create app user for security
RUN useradd -m -u 1000 appuser

# Copy application code and config
COPY euro_bakshish_app.py .
COPY docker-entrypoint.sh .

# Make entrypoint executable
RUN chmod +x docker-entrypoint.sh

# Create directory for database and .web structure
RUN mkdir -p /app/data /app/.web /app/assets \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose ports
# Port 3000 for frontend
# Port 8000 for backend API
EXPOSE 3000 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV NODE_ENV=production
ENV DATABASE_URL=sqlite:///./data/euro_bakshish.db

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/ping || exit 1

# Run the application using entrypoint script
ENTRYPOINT ["./docker-entrypoint.sh"]
