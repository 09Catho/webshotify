@echo off
REM Webshotify - GCP Cloud Run Deployment Script
REM ============================================

echo ============================================================
echo   WEBSHOTIFY - GCP CLOUD RUN DEPLOYMENT
echo ============================================================
echo.

REM Check if gcloud is installed
where gcloud >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] gcloud CLI is not found in PATH
    echo.
    echo Please add gcloud to your PATH or run this from Cloud SDK Shell
    echo.
    echo Google Cloud SDK is typically installed at:
    echo   C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin
    echo.
    echo Add it to PATH or run:
    echo   "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud" init
    echo.
    pause
    exit /b 1
)

echo [OK] gcloud CLI found
echo.

REM Step 1: Check authentication
echo [1/8] Checking authentication...
gcloud auth list
if %errorlevel% neq 0 (
    echo [ERROR] Not authenticated. Please run: gcloud auth login
    pause
    exit /b 1
)
echo.

REM Step 2: Set project
echo [2/8] Setting GCP project...
set /p PROJECT_ID="Enter your GCP Project ID (e.g., webshotify-prod): "
gcloud config set project %PROJECT_ID%
echo.

REM Step 3: Enable required APIs
echo [3/8] Enabling required APIs...
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
echo.

REM Step 4: Set region
echo [4/8] Setting deployment region...
set REGION=us-central1
echo Using region: %REGION%
echo.

REM Step 5: Build and deploy
echo [5/8] Building and deploying to Cloud Run...
echo This may take 5-10 minutes...
echo.

gcloud run deploy webshotify ^
  --source . ^
  --platform managed ^
  --region %REGION% ^
  --allow-unauthenticated ^
  --memory 2Gi ^
  --cpu 2 ^
  --timeout 120s ^
  --max-instances 10 ^
  --min-instances 0 ^
  --port 8080

if %errorlevel% neq 0 (
    echo [ERROR] Deployment failed!
    pause
    exit /b 1
)
echo.

REM Step 6: Get service URL
echo [6/8] Getting service URL...
for /f "tokens=*" %%i in ('gcloud run services describe webshotify --platform managed --region %REGION% --format="value(status.url)"') do set SERVICE_URL=%%i
echo.
echo ============================================================
echo   DEPLOYMENT SUCCESSFUL!
echo ============================================================
echo.
echo Your API is now live at:
echo   %SERVICE_URL%
echo.
echo Test it:
echo   curl %SERVICE_URL%/health
echo.

REM Step 7: Set environment variables (optional)
echo [7/8] Setting environment variables...
set /p SET_ENV="Do you want to set environment variables? (y/n): "
if /i "%SET_ENV%"=="y" (
    echo.
    echo Setting production environment variables...
    gcloud run services update webshotify ^
      --platform managed ^
      --region %REGION% ^
      --update-env-vars FLASK_ENV=production,RATE_LIMIT_PER_MINUTE=60,CACHE_DURATION_HOURS=24
    echo Environment variables set!
)
echo.

REM Step 8: Display summary
echo [8/8] Deployment Summary
echo ============================================================
echo   Service Name: webshotify
echo   Region: %REGION%
echo   URL: %SERVICE_URL%
echo   Status: LIVE
echo ============================================================
echo.
echo Next steps:
echo   1. Test your API: %SERVICE_URL%/health
echo   2. View landing page: %SERVICE_URL%
echo   3. Configure custom domain (optional)
echo   4. Set up monitoring and alerts
echo   5. List on RapidAPI marketplace
echo.
echo View logs:
echo   gcloud run services logs tail webshotify --region %REGION%
echo.
echo Update deployment:
echo   gcloud run deploy webshotify --source . --region %REGION%
echo.
echo ============================================================
echo   CONGRATULATIONS! Webshotify is in production!
echo ============================================================
echo.

pause
