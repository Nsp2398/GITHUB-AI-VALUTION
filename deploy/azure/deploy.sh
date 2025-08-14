#!/bin/bash

# Azure Deployment Script for ValuAI UCaaS Valuation Platform
# This script deploys the infrastructure and applications to Azure

set -e

# Configuration
RESOURCE_GROUP="valuai-rg"
LOCATION="eastus"
DEPLOYMENT_NAME="valuai-deployment-$(date +%Y%m%d-%H%M%S)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    print_error "Azure CLI is not installed. Please install it first."
    exit 1
fi

# Check if logged in to Azure
if ! az account show &> /dev/null; then
    print_warning "Not logged in to Azure. Please login first."
    az login
fi

print_status "Starting ValuAI deployment to Azure..."

# Create resource group if it doesn't exist
print_status "Creating resource group: $RESOURCE_GROUP"
az group create --name $RESOURCE_GROUP --location $LOCATION

# Deploy ARM template
print_status "Deploying infrastructure using ARM template..."
az deployment group create \
    --resource-group $RESOURCE_GROUP \
    --template-file arm-template.json \
    --parameters @parameters.json \
    --name $DEPLOYMENT_NAME

# Get deployment outputs
print_status "Getting deployment outputs..."
BACKEND_URL=$(az deployment group show --resource-group $RESOURCE_GROUP --name $DEPLOYMENT_NAME --query properties.outputs.backendUrl.value -o tsv)
FRONTEND_URL=$(az deployment group show --resource-group $RESOURCE_GROUP --name $DEPLOYMENT_NAME --query properties.outputs.frontendUrl.value -o tsv)
DB_SERVER=$(az deployment group show --resource-group $RESOURCE_GROUP --name $DEPLOYMENT_NAME --query properties.outputs.databaseServer.value -o tsv)

print_success "Infrastructure deployed successfully!"
print_status "Backend URL: $BACKEND_URL"
print_status "Frontend URL: $FRONTEND_URL"
print_status "Database Server: $DB_SERVER"

# Build and deploy backend
print_status "Building and deploying backend..."
cd ../../server

# Create deployment package
print_status "Creating backend deployment package..."
zip -r ../deploy/azure/backend.zip . -x "venv/*" "__pycache__/*" "*.pyc" "tests/*"

# Deploy to Azure App Service
BACKEND_APP_NAME=$(az deployment group show --resource-group $RESOURCE_GROUP --name $DEPLOYMENT_NAME --query properties.outputs.backendUrl.value -o tsv | sed 's/https:\/\///' | sed 's/\.azurewebsites\.net//')

print_status "Deploying backend to App Service: $BACKEND_APP_NAME"
az webapp deploy --resource-group $RESOURCE_GROUP --name $BACKEND_APP_NAME --src-path ../deploy/azure/backend.zip --type zip

# Configure backend startup command
az webapp config set --resource-group $RESOURCE_GROUP --name $BACKEND_APP_NAME --startup-file "gunicorn --bind 0.0.0.0:8000 app:app"

# Build and deploy frontend
print_status "Building and deploying frontend..."
cd ../client

# Install dependencies and build
npm ci
npm run build

# Create deployment package
print_status "Creating frontend deployment package..."
cd dist
zip -r ../../deploy/azure/frontend.zip .

# Deploy to Azure App Service
FRONTEND_APP_NAME=$(az deployment group show --resource-group $RESOURCE_GROUP --name $DEPLOYMENT_NAME --query properties.outputs.frontendUrl.value -o tsv | sed 's/https:\/\///' | sed 's/\.azurewebsites\.net//')

print_status "Deploying frontend to App Service: $FRONTEND_APP_NAME"
az webapp deploy --resource-group $RESOURCE_GROUP --name $FRONTEND_APP_NAME --src-path ../../deploy/azure/frontend.zip --type zip

# Run database migrations
print_status "Running database migrations..."
cd ../../server

# Install dependencies in a temporary virtual environment
python -m venv temp_venv
source temp_venv/bin/activate
pip install -r requirements.txt

# Set environment variables for migration
export DATABASE_URL="postgresql://valuai_admin:ComplexPassword123!@$DB_SERVER:5432/valuai"
export FLASK_APP=app.py

# Run migrations
flask db upgrade

# Clean up
deactivate
rm -rf temp_venv

print_success "Deployment completed successfully!"
print_status "Application URLs:"
print_status "  Frontend: $FRONTEND_URL"
print_status "  Backend API: $BACKEND_URL"
print_status ""
print_status "Next steps:"
print_status "1. Configure custom domain names (optional)"
print_status "2. Set up SSL certificates"
print_status "3. Configure monitoring and alerts"
print_status "4. Set up backup schedules"
print_status "5. Configure OpenAI API key in App Service settings"

# Clean up deployment packages
rm -f ../deploy/azure/backend.zip
rm -f ../deploy/azure/frontend.zip

print_success "ValuAI deployment to Azure completed!"
