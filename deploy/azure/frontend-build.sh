#!/bin/bash

# Frontend build script for Azure deployment
echo "Building ValuAI frontend for Azure deployment..."

# Set environment variables for production
export NODE_ENV=production
export GENERATE_SOURCEMAP=false
export REACT_APP_API_URL=${REACT_APP_API_URL:-"https://valuai-backend.azurewebsites.net"}

echo "API URL: $REACT_APP_API_URL"
echo "Node Environment: $NODE_ENV"

# Install dependencies
echo "Installing dependencies..."
npm ci --only=production

# Build the application
echo "Building React application..."
npm run build

# Verify build was successful
if [ -d "dist" ] && [ -f "dist/index.html" ]; then
    echo "Build completed successfully!"
    echo "Build size:"
    du -sh dist/
    echo "Build contents:"
    ls -la dist/
else
    echo "Build failed - dist directory not found or empty"
    exit 1
fi

# Optional: Create deployment package
if [ "$CREATE_PACKAGE" = "true" ]; then
    echo "Creating deployment package..."
    cd dist
    tar -czf ../frontend-build.tar.gz .
    cd ..
    echo "Package created: frontend-build.tar.gz"
fi

echo "Frontend build process completed!"
