# Azure Configuration for Production Deployment

# Resource Configuration
$resourceGroup = "valuai-prod-rg"
$location = "East US"
$environment = "prod"

# App Service Configuration
$appServicePlan = "valuai-asp-prod"
$backendAppName = "valuai-backend-prod"
$frontendAppName = "valuai-frontend-prod"

# Database Configuration
$postgresServerName = "valuai-postgres-prod"
$databaseName = "valuai"
$adminUsername = "valuai_admin"
$adminPassword = "ComplexPassword123!"  # Change this in production

# Storage Configuration
$storageAccountName = "valuaistorageprod"

# Key Vault Configuration
$keyVaultName = "valuai-kv-prod"

# Application Insights Configuration
$applicationInsightsName = "valuai-ai-prod"

# Function to create Azure resources
function Deploy-ValuAIInfrastructure {
    Write-Host "Creating resource group..." -ForegroundColor Green
    az group create --name $resourceGroup --location $location

    Write-Host "Deploying infrastructure..." -ForegroundColor Green
    az deployment group create `
        --resource-group $resourceGroup `
        --template-file "arm-template.json" `
        --parameters `
            projectName="valuai" `
            environment=$environment `
            location=$location `
            administratorLogin=$adminUsername `
            administratorLoginPassword=$adminPassword

    Write-Host "Infrastructure deployment completed!" -ForegroundColor Green
}

# Function to deploy backend application
function Deploy-Backend {
    Write-Host "Deploying backend application..." -ForegroundColor Green
    
    # Build and package backend
    Set-Location "..\..\server"
    
    # Create virtual environment and install dependencies
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    
    # Run tests
    pytest tests/ --verbose
    
    # Create deployment package
    Compress-Archive -Path "." -DestinationPath "..\deploy\azure\backend.zip" -Exclude "venv\*", "__pycache__\*", "*.pyc", "tests\*"
    
    # Deploy to Azure App Service
    az webapp deploy --resource-group $resourceGroup --name $backendAppName --src-path "..\deploy\azure\backend.zip" --type zip
    
    # Configure application settings
    az webapp config appsettings set --resource-group $resourceGroup --name $backendAppName --settings `
        FLASK_ENV="production" `
        DATABASE_URL="postgresql://$adminUsername`:$adminPassword@$postgresServerName.postgres.database.azure.com:5432/$databaseName" `
        SECRET_KEY="$(New-Guid)" `
        JWT_SECRET_KEY="$(New-Guid)"
    
    # Configure startup command
    az webapp config set --resource-group $resourceGroup --name $backendAppName --startup-file "gunicorn --bind 0.0.0.0:8000 app:app"
    
    deactivate
    Set-Location "..\deploy\azure"
    
    Write-Host "Backend deployment completed!" -ForegroundColor Green
}

# Function to deploy frontend application
function Deploy-Frontend {
    Write-Host "Deploying frontend application..." -ForegroundColor Green
    
    Set-Location "..\..\client"
    
    # Install dependencies and build
    npm ci
    npm run build
    
    # Run tests
    npm test -- --coverage --watchAll=false
    
    # Create deployment package
    Set-Location "dist"
    Compress-Archive -Path "." -DestinationPath "..\..\deploy\azure\frontend.zip"
    
    # Deploy to Azure App Service
    az webapp deploy --resource-group $resourceGroup --name $frontendAppName --src-path "..\..\deploy\azure\frontend.zip" --type zip
    
    # Configure application settings
    $backendUrl = "https://$backendAppName.azurewebsites.net"
    az webapp config appsettings set --resource-group $resourceGroup --name $frontendAppName --settings `
        REACT_APP_API_URL=$backendUrl `
        NODE_ENV="production"
    
    Set-Location "..\..\deploy\azure"
    
    Write-Host "Frontend deployment completed!" -ForegroundColor Green
}

# Function to run database migrations
function Initialize-Database {
    Write-Host "Initializing database..." -ForegroundColor Green
    
    Set-Location "..\..\server"
    
    # Set environment variables
    $env:DATABASE_URL = "postgresql://$adminUsername`:$adminPassword@$postgresServerName.postgres.database.azure.com:5432/$databaseName"
    $env:FLASK_APP = "app.py"
    
    # Create virtual environment and install dependencies
    python -m venv temp_venv
    .\temp_venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    
    # Run migrations
    flask db upgrade
    
    deactivate
    Remove-Item -Recurse -Force temp_venv
    
    Set-Location "..\deploy\azure"
    
    Write-Host "Database initialization completed!" -ForegroundColor Green
}

# Function to configure monitoring
function Configure-Monitoring {
    Write-Host "Configuring monitoring and alerts..." -ForegroundColor Green
    
    # Configure Application Insights for backend
    $instrumentationKey = az monitor app-insights component show --app $applicationInsightsName --resource-group $resourceGroup --query instrumentationKey -o tsv
    
    az webapp config appsettings set --resource-group $resourceGroup --name $backendAppName --settings `
        APPINSIGHTS_INSTRUMENTATIONKEY=$instrumentationKey
    
    az webapp config appsettings set --resource-group $resourceGroup --name $frontendAppName --settings `
        APPINSIGHTS_INSTRUMENTATIONKEY=$instrumentationKey
    
    # Create alerts for critical metrics
    az monitor metrics alert create `
        --name "High CPU Usage" `
        --resource-group $resourceGroup `
        --scopes "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$resourceGroup/providers/Microsoft.Web/sites/$backendAppName" `
        --condition "avg Percentage CPU > 80" `
        --description "Alert when CPU usage is above 80%"
    
    az monitor metrics alert create `
        --name "High Memory Usage" `
        --resource-group $resourceGroup `
        --scopes "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$resourceGroup/providers/Microsoft.Web/sites/$backendAppName" `
        --condition "avg MemoryPercentage > 85" `
        --description "Alert when memory usage is above 85%"
    
    Write-Host "Monitoring configuration completed!" -ForegroundColor Green
}

# Main deployment function
function Deploy-ValuAI {
    Write-Host "Starting ValuAI deployment to Azure..." -ForegroundColor Yellow
    
    # Check prerequisites
    if (!(Get-Command az -ErrorAction SilentlyContinue)) {
        Write-Error "Azure CLI is not installed. Please install it first."
        return
    }
    
    # Check if logged in
    try {
        az account show | Out-Null
    }
    catch {
        Write-Host "Please login to Azure first..." -ForegroundColor Yellow
        az login
    }
    
    try {
        Deploy-ValuAIInfrastructure
        Deploy-Backend
        Deploy-Frontend
        Initialize-Database
        Configure-Monitoring
        
        Write-Host "`nDeployment completed successfully!" -ForegroundColor Green
        Write-Host "Frontend URL: https://$frontendAppName.azurewebsites.net" -ForegroundColor Cyan
        Write-Host "Backend URL: https://$backendAppName.azurewebsites.net" -ForegroundColor Cyan
        
        Write-Host "`nNext steps:" -ForegroundColor Yellow
        Write-Host "1. Configure custom domain names (optional)"
        Write-Host "2. Set up SSL certificates"
        Write-Host "3. Configure OpenAI API key in Key Vault"
        Write-Host "4. Set up automated backups"
        Write-Host "5. Configure CDN for frontend (optional)"
    }
    catch {
        Write-Error "Deployment failed: $_"
    }
    finally {
        # Clean up temporary files
        Remove-Item -Path "backend.zip" -ErrorAction SilentlyContinue
        Remove-Item -Path "frontend.zip" -ErrorAction SilentlyContinue
    }
}

# Export functions for module use
Export-ModuleMember -Function Deploy-ValuAI, Deploy-ValuAIInfrastructure, Deploy-Backend, Deploy-Frontend, Initialize-Database, Configure-Monitoring
