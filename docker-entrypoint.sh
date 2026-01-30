#!/bin/bash
set -e

echo "Starting Euro Bakshish application..."

# Run the app using NextPy
exec nextpy run --env prod --loglevel info --frontend-port 3000 --backend-port 8000
