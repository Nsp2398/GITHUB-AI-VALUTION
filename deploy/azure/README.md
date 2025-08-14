# Azure Deployment Guide for ValuAI UCaaS Valuation Platform

## Overview
This guide provides step-by-step instructions for deploying the ValuAI UCaaS valuation platform to Microsoft Azure using Azure App Service, Azure Database for PostgreSQL, and other Azure services.

## Prerequisites

### 1. Azure Account Setup
- Active Azure subscription
- Azure CLI installed on your machine
- Git repository access (GitHub/Azure DevOps)

### 2. Local Development Environment
- Node.js 18.x or later
- Python 3.11 or later
- Azure CLI 2.50.0 or later

### 3. Install Azure CLI
```bash
# Windows (using winget)
winget install Microsoft.AzureCLI

# Windows (using PowerShell)
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'

# macOS
brew install azure-cli

# Linux
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

## Architecture Overview

The deployment includes:
- **Frontend**: React app on Azure App Service (Linux)
- **Backend**: Flask API on Azure App Service (Linux)
- **Database**: Azure Database for PostgreSQL Flexible Server
- **Storage**: Azure Storage Account for reports and file uploads
- **Monitoring**: Application Insights for telemetry
- **Security**: Azure Key Vault for secrets management

## Deployment Options

### Option 1: Automated Deployment (Recommended)

#### Using PowerShell (Windows)
```powershell
# Navigate to Azure deployment directory
cd deploy/azure

# Run the automated deployment script
.\azure-deploy.ps1
Deploy-ValuAI
```

#### Using Bash (Linux/macOS)
```bash
# Navigate to Azure deployment directory
cd deploy/azure

# Make script executable
chmod +x deploy.sh

# Run the deployment script
./deploy.sh
```

#### Using Windows Batch
```batch
cd deploy\azure
deploy.bat
```

### Option 2: Manual Deployment

#### Step 1: Login to Azure
```bash
az login
```

#### Step 2: Create Resource Group
```bash
az group create --name valuai-rg --location "East US"
```

#### Step 3: Deploy Infrastructure
```bash
az deployment group create \
    --resource-group valuai-rg \
    --template-file arm-template.json \
    --parameters @parameters.json
```

#### Step 4: Deploy Backend Application
```bash
# Build backend package
cd ../../server
zip -r ../deploy/azure/backend.zip . -x "venv/*" "__pycache__/*" "*.pyc" "tests/*"

# Deploy to App Service
az webapp deploy --resource-group valuai-rg --name valuai-backend-dev --src-path ../deploy/azure/backend.zip --type zip

# Configure startup command
az webapp config set --resource-group valuai-rg --name valuai-backend-dev --startup-file "gunicorn --bind 0.0.0.0:8000 app:app"
```

#### Step 5: Deploy Frontend Application
```bash
# Build frontend
cd ../client
npm ci
npm run build

# Create deployment package
cd dist
zip -r ../../deploy/azure/frontend.zip .

# Deploy to App Service
az webapp deploy --resource-group valuai-rg --name valuai-frontend-dev --src-path ../../deploy/azure/frontend.zip --type zip
```

#### Step 6: Initialize Database
```bash
# Set environment variables
export DATABASE_URL="postgresql://username:password@server.postgres.database.azure.com:5432/valuai"
export FLASK_APP=app.py

# Run migrations
cd ../../server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
```

## Configuration

### Environment Variables

#### Backend App Service Settings
```bash
az webapp config appsettings set --resource-group valuai-rg --name valuai-backend-dev --settings \
    FLASK_ENV="production" \
    DATABASE_URL="postgresql://admin:password@server.postgres.database.azure.com:5432/valuai" \
    SECRET_KEY="your-secret-key" \
    JWT_SECRET_KEY="your-jwt-secret" \
    OPENAI_API_KEY="your-openai-key"
```

#### Frontend App Service Settings
```bash
az webapp config appsettings set --resource-group valuai-rg --name valuai-frontend-dev --settings \
    REACT_APP_API_URL="https://valuai-backend-dev.azurewebsites.net" \
    NODE_ENV="production"
```

### Database Configuration

#### Firewall Rules
```bash
# Allow Azure services
az postgres flexible-server firewall-rule create \
    --resource-group valuai-rg \
    --name valuai-postgres-dev \
    --rule-name AllowAzureServices \
    --start-ip-address 0.0.0.0 \
    --end-ip-address 0.0.0.0
```

#### SSL Configuration
The PostgreSQL server is configured with SSL enforcement. Update your connection string to include SSL parameters:
```
postgresql://username:password@server.postgres.database.azure.com:5432/valuai?sslmode=require
```

## Monitoring and Logging

### Application Insights Setup
Application Insights is automatically configured for both frontend and backend applications. View telemetry at:
- Azure Portal → Application Insights → valuai-ai-{environment}

### Log Streaming
```bash
# Backend logs
az webapp log tail --resource-group valuai-rg --name valuai-backend-dev

# Frontend logs
az webapp log tail --resource-group valuai-rg --name valuai-frontend-dev
```

## Security Best Practices

### 1. Key Vault Integration
Store sensitive configuration in Azure Key Vault:
```bash
# Create secrets
az keyvault secret set --vault-name valuai-kv-dev --name "database-password" --value "your-password"
az keyvault secret set --vault-name valuai-kv-dev --name "openai-api-key" --value "your-api-key"

# Reference in App Service
az webapp config appsettings set --resource-group valuai-rg --name valuai-backend-dev --settings \
    DATABASE_PASSWORD="@Microsoft.KeyVault(VaultName=valuai-kv-dev;SecretName=database-password)"
```

### 2. Managed Identity
Enable managed identity for secure access to Azure resources:
```bash
az webapp identity assign --resource-group valuai-rg --name valuai-backend-dev
```

### 3. Network Security
- Configure network security groups
- Enable App Service authentication
- Use private endpoints for database access

## Scaling and Performance

### 1. Auto-scaling
```bash
az monitor autoscale create \
    --resource-group valuai-rg \
    --resource valuai-asp-dev \
    --resource-type Microsoft.Web/serverfarms \
    --name autoscale-valuai \
    --min-count 1 \
    --max-count 10 \
    --count 2
```

### 2. CDN Configuration
```bash
# Create CDN profile
az cdn profile create --resource-group valuai-rg --name valuai-cdn --sku Standard_Microsoft

# Create CDN endpoint
az cdn endpoint create \
    --resource-group valuai-rg \
    --profile-name valuai-cdn \
    --name valuai-frontend \
    --origin valuai-frontend-dev.azurewebsites.net
```

## Backup and Recovery

### 1. Database Backup
Automated backups are enabled by default. Configure additional settings:
```bash
az postgres flexible-server parameter set \
    --resource-group valuai-rg \
    --server-name valuai-postgres-dev \
    --name backup_retention_days \
    --value 30
```

### 2. App Service Backup
```bash
az webapp config backup create \
    --resource-group valuai-rg \
    --webapp-name valuai-backend-dev \
    --backup-name initial-backup \
    --storage-account-url "https://storage.blob.core.windows.net/backups"
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check firewall rules
   - Verify connection string
   - Ensure SSL configuration

2. **App Service Deployment Failures**
   - Check deployment logs: `az webapp log deployment list`
   - Verify startup command
   - Check application settings

3. **Frontend Build Issues**
   - Verify Node.js version
   - Check environment variables
   - Review build logs

### Useful Commands

```bash
# View deployment status
az deployment group show --resource-group valuai-rg --name deployment-name

# Check app service status
az webapp show --resource-group valuai-rg --name app-name --query state

# View application logs
az webapp log download --resource-group valuai-rg --name app-name

# Restart app service
az webapp restart --resource-group valuai-rg --name app-name
```

## Cost Optimization

1. **Use appropriate SKUs for development vs production**
2. **Enable auto-shutdown for development environments**
3. **Monitor resource utilization with Azure Advisor**
4. **Use Azure Reserved Instances for production workloads**

## Support and Maintenance

### Regular Tasks
- Monitor application performance
- Review security recommendations
- Update dependencies
- Backup verification
- Cost analysis

### Updates and Patches
- Use Azure DevOps pipelines for automated deployments
- Implement blue-green deployment strategy
- Monitor health checks during deployments

## Resources

- [Azure App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
- [Azure Database for PostgreSQL Documentation](https://docs.microsoft.com/en-us/azure/postgresql/)
- [Azure DevOps Pipelines](https://docs.microsoft.com/en-us/azure/devops/pipelines/)
- [Azure CLI Reference](https://docs.microsoft.com/en-us/cli/azure/)

---

For additional support or questions about the deployment process, please refer to the project documentation or contact the development team.
