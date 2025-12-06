@echo off
title ALA-Web Setup

echo ========================================
echo   ALA-Web Automated Setup
echo ========================================

REM Check for Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found! Please install Python 3.11 or higher from python.org
    pause
    exit /b 1
)

REM Create virtual environment
echo.
echo [1/4] Creating Python virtual environment (.venv)...
if not exist ".venv" (
    python -m venv .venv
) else (
    echo .venv already exists.
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install backend dependencies
echo.
echo [2/4] Installing backend dependencies...
cd backend

REM FIX: Create local temp directory to avoid "Path too long" errors (e.g., flash-attn)
if not exist "tmp" mkdir tmp
set TMP=%cd%\tmp
set TEMP=%cd%\tmp
echo Set temporary build directory to: %TMP%

pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install backend dependencies.
    echo Trying to clean up temp files...
    rmdir /s /q tmp
    pause
    exit /b 1
)
rmdir /s /q tmp

REM Install AI models (Optional)
echo.
echo [3/4] AI Model Setup
set /p INSTALL_AI="Do you want to install AI models (SAM2 + Florence-2)? This requires ~2GB. (Y/N): "
if /i "%INSTALL_AI%"=="Y" (
    echo Installing AI models...
    python ..\scripts\download_models.py
) else (
    echo Skipping AI model installation.
)

REM Install frontend dependencies
echo.
echo [4/4] Installing frontend dependencies...
cd ..\frontend
call npm install --legacy-peer-deps
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install frontend dependencies. Please check if Node.js is installed.
    pause
    exit /b 1
)

cd ..
echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo You can now run the application using "run.bat"
echo.
pause
