# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    musl-dev \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy entrypoint script first and ensure it has correct permissions and line endings
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh && \
    # Remove any potential Windows line endings
    sed -i 's/\r$//' /app/entrypoint.sh

# Copy rest of project
COPY . /app/

# Run entrypoint script with explicit bash interpreter
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
