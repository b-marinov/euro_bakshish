#!/bin/bash
set -e

echo "Starting Euro Bakshish application..."

# Initialize the NextPy app on first run if needed
if [ ! -f ".web/package.json" ]; then
    echo "Initializing NextPy application (first run)..."
    # Accept blank template by piping echo
    echo "" | nextpy init || true
fi

# Start the application
echo "Running NextPy application..."
exec nextpy run --env prod --loglevel info
