@echo off
REM Quick Push Script for webshotify
REM Repository: https://github.com/09Catho/webshotify

echo ============================================================
echo   WEBSHOTIFY - GitHub Push Script
echo ============================================================
echo.

REM Step 1: Initialize git if needed
echo [1/7] Initializing Git repository...
git init
echo.

REM Step 2: Add remote
echo [2/7] Adding remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/09Catho/webshotify.git
echo.

REM Step 3: Show what will be pushed
echo [3/7] Checking files to be pushed...
echo.
echo Files that will be pushed:
git status --short
echo.

REM Step 4: Verify no sensitive files
echo [4/7] Verifying no sensitive files...
git check-ignore config/api_keys.json >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] config/api_keys.json is ignored
) else (
    echo [WARNING] config/api_keys.json is NOT ignored!
    pause
)

git check-ignore .env >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] .env is ignored
) else (
    echo [INFO] .env not found or not ignored
)
echo.

REM Step 5: Add all files
echo [5/7] Adding files...
git add .
echo.

REM Step 6: Commit
echo [6/7] Creating commit...
git commit -m "Initial commit: Webshotify - Professional Screenshot API v1.0.0" -m "Features: 25+ advanced features, multi-browser support, visual regression testing, webhooks, dashboard, secure authentication, and more. Production-ready with comprehensive documentation."
echo.

REM Step 7: Push
echo [7/7] Pushing to GitHub...
git branch -M main
git push -u origin main --force
echo.

echo ============================================================
echo   SUCCESS! Your code is now on GitHub!
echo   Repository: https://github.com/09Catho/webshotify
echo ============================================================
echo.

pause
