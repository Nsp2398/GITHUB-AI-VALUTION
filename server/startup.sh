#!/bin/bash

# Azure App Service startup script for ValuAI backend
echo "Starting ValuAI backend on Azure App Service..."

# Set default environment variables if not provided
export FLASK_ENV=${FLASK_ENV:-production}
export PYTHONPATH=${PYTHONPATH:-/home/site/wwwroot}
export PORT=${PORT:-8000}

# Azure App Service specific environment variables
export WEBSITE_HOSTNAME=${WEBSITE_HOSTNAME:-localhost}
export WEBSITE_INSTANCE_ID=${WEBSITE_INSTANCE_ID:-local}

echo "Environment: $FLASK_ENV"
echo "Python Path: $PYTHONPATH"
echo "Port: $PORT"
echo "Website Hostname: $WEBSITE_HOSTNAME"

# Change to application directory
cd /home/site/wwwroot

# Install dependencies if requirements.txt has changed
if [ -f requirements.txt ]; then
    echo "Installing Python dependencies..."
    pip install --no-cache-dir -r requirements.txt
fi

# Run database migrations if needed
if [ "$FLASK_ENV" = "production" ] && [ -n "$DATABASE_URL" ]; then
    echo "Running database migrations..."
    export FLASK_APP=app.py
    flask db upgrade || echo "Migration failed or not needed"
fi

# Start the application with Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn --config gunicorn.conf.py app:app
