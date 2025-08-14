@echo off
REM Azure Deployment Script for ValuAI UCaaS Valuation Platform (Windows)
REM This script deploys the infrastructure and applications to Azure

setlocal enabledelayedexpansion

REM Configuration
set RESOURCE_GROUP=valuai-rg
set LOCATION=eastus
set DEPLOYMENT_NAME=valuai-deployment-%date:~-4,4%%date:~-10,2%%date:~-7,2%-%time:~0,2%%time:~3,2%%time:~6,2%

echo [INFO] Starting ValuAI deployment to Azure...

REM Check if Azure CLI is installed
az --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Azure CLI is not installed. Please install it first.
    exit /b 1
)

REM Check if logged in to Azure
az account show >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Not logged in to Azure. Please login first.
    az login
)

REM Create resource group if it doesn't exist
echo [INFO] Creating resource group: %RESOURCE_GROUP%
az group create --name %RESOURCE_GROUP% --location %LOCATION%

REM Deploy ARM template
echo [INFO] Deploying infrastructure using ARM template...
az deployment group create ^
    --resource-group %RESOURCE_GROUP% ^
    --template-file arm-template.json ^
    --parameters @parameters.json ^
    --name %DEPLOYMENT_NAME%

if %errorlevel% neq 0 (
    echo [ERROR] Infrastructure deployment failed
    exit /b 1
)

REM Get deployment outputs
echo [INFO] Getting deployment outputs...
for /f "delims=" %%i in ('az deployment group show --resource-group %RESOURCE_GROUP% --name %DEPLOYMENT_NAME% --query properties.outputs.backendUrl.value -o tsv') do set BACKEND_URL=%%i
for /f "delims=" %%i in ('az deployment group show --resource-group %RESOURCE_GROUP% --name %DEPLOYMENT_NAME% --query properties.outputs.frontendUrl.value -o tsv') do set FRONTEND_URL=%%i
for /f "delims=" %%i in ('az deployment group show --resource-group %RESOURCE_GROUP% --name %DEPLOYMENT_NAME% --query properties.outputs.databaseServer.value -o tsv') do set DB_SERVER=%%i

echo [SUCCESS] Infrastructure deployed successfully!
echo [INFO] Backend URL: %BACKEND_URL%
echo [INFO] Frontend URL: %FRONTEND_URL%
echo [INFO] Database Server: %DB_SERVER%

REM Build and deploy backend
echo [INFO] Building and deploying backend...
cd ..\..\server

REM Create deployment package
echo [INFO] Creating backend deployment package...
if exist ..\deploy\azure\backend.zip del ..\deploy\azure\backend.zip
powershell -command "Compress-Archive -Path * -DestinationPath ..\deploy\azure\backend.zip -Exclude venv\*, __pycache__\*, *.pyc, tests\*"

REM Extract backend app name from URL
for /f "tokens=2 delims=/." %%i in ("%BACKEND_URL%") do set BACKEND_APP_NAME=%%i

echo [INFO] Deploying backend to App Service: %BACKEND_APP_NAME%
az webapp deploy --resource-group %RESOURCE_GROUP% --name %BACKEND_APP_NAME% --src-path ..\deploy\azure\backend.zip --type zip

REM Configure backend startup command
az webapp config set --resource-group %RESOURCE_GROUP% --name %BACKEND_APP_NAME% --startup-file "gunicorn --bind 0.0.0.0:8000 app:app"

REM Build and deploy frontend
echo [INFO] Building and deploying frontend...
cd ..\client

REM Install dependencies and build
call npm ci
call npm run build

REM Create deployment package
echo [INFO] Creating frontend deployment package...
cd dist
if exist ..\..\deploy\azure\frontend.zip del ..\..\deploy\azure\frontend.zip
powershell -command "Compress-Archive -Path * -DestinationPath ..\..\deploy\azure\frontend.zip"

REM Extract frontend app name from URL
for /f "tokens=2 delims=/." %%i in ("%FRONTEND_URL%") do set FRONTEND_APP_NAME=%%i

echo [INFO] Deploying frontend to App Service: %FRONTEND_APP_NAME%
az webapp deploy --resource-group %RESOURCE_GROUP% --name %FRONTEND_APP_NAME% --src-path ..\..\deploy\azure\frontend.zip --type zip

echo [SUCCESS] Deployment completed successfully!
echo [INFO] Application URLs:
echo [INFO]   Frontend: %FRONTEND_URL%
echo [INFO]   Backend API: %BACKEND_URL%
echo.
echo [INFO] Next steps:
echo [INFO] 1. Configure custom domain names (optional)
echo [INFO] 2. Set up SSL certificates
echo [INFO] 3. Configure monitoring and alerts
echo [INFO] 4. Set up backup schedules
echo [INFO] 5. Configure OpenAI API key in App Service settings

REM Clean up deployment packages
if exist ..\deploy\azure\backend.zip del ..\deploy\azure\backend.zip
if exist ..\deploy\azure\frontend.zip del ..\deploy\azure\frontend.zip

echo [SUCCESS] ValuAI deployment to Azure completed!
pause
