@echo off
REM =============================================================================
REM ALA-Web Complete Setup Script
REM Install all dependencies for backend and frontend
REM =============================================================================

echo.
echo ===============================================
echo ALA-Web Complete Setup
echo ===============================================
echo.
echo This script will set up:
echo   1. Python virtual environment (.venv)
echo   2. Backend dependencies
echo   3. Frontend dependencies
echo   4. AI models (optional)
echo.

REM Check if we're in the correct directory
if not exist "backend" (
    echo ERROR: Please run this script from the ALA-Web root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ERROR: Frontend directory not found
    pause
    exit /b 1
)

echo.
echo ===============================================
echo Step 1/4: Python Environment Setup
echo ===============================================
echo.

REM Check for Conda
where conda >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Conda found. Creating virtual environment...
    REM Skip conda - use venv for consistency
    echo Conda detected but using standard venv for consistency...
    if errorlevel 1 (
        echo ERROR: Failed to create conda environment
        pause
        exit /b 1
    )
    
    REM Fallback to venv
    
) else (
    echo Conda not found. Using venv...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create venv
        echo Please install Python 3.11 or higher
        pause
        exit /b 1
    )
    
    call .venv\Scripts\activate
)

echo Python environment ready!
python --version

echo.
echo ===============================================
echo Step 2/4: Backend Dependencies
echo ===============================================
echo.

cd backend

echo Installing core dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some packages failed to install
    echo Continuing with installation...
)

echo Creating data directories...
if not exist "data" mkdir data
if not exist "data\uploads" mkdir data\uploads
if not exist "lib" mkdir lib

cd ..

echo.
echo ===============================================
echo Step 3/4: Frontend Dependencies
echo ===============================================
echo.

cd frontend

REM Check for npm
where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: npm not found!
    echo Please install Node.js from https://nodejs.org/
    cd ..
    pause
    exit /b 1
)

echo Node.js version:
node --version
echo npm version:
npm --version

echo.
echo Installing frontend packages...
echo This may take a few minutes...
npm install --legacy-peer-deps
if errorlevel 1 (
    echo ERROR: npm install failed
    echo Try running: npm cache clean --force
    cd ..
    pause
    exit /b 1
)

cd ..

echo.
echo ===============================================
echo Step 4/4: AI Models (Optional)
echo ===============================================
echo.

set /p INSTALL_AI="Do you want to install AI models (SAM2 + Florence-2)? This requires ~2GB and takes 5-10 minutes. (Y/N): "

if /i "%INSTALL_AI%"=="Y" (
    echo.
    echo Installing AI models to backend/lib...
    cd backend
    call setup_local_lib.bat
    cd ..
) else (
    echo.
    echo Skipping AI model installation.
    echo You can install later by running: backend\setup_local_lib.bat
)

echo.
echo ===============================================
echo Installation Complete!
echo ===============================================
echo.
echo Setup Summary:
echo   - Python environment: .venv (activated)
echo   - Backend dependencies: Installed
echo   - Frontend dependencies: Installed
echo   - AI models: %INSTALL_AI%
@echo off
REM =============================================================================
REM ALA-Web Complete Setup Script
REM Install all dependencies for backend and frontend
REM =============================================================================

echo.
echo ===============================================
echo ALA-Web Complete Setup
echo ===============================================
echo.
echo This script will set up:
echo   1. Python virtual environment (.venv)
echo   2. Backend dependencies
echo   3. Frontend dependencies
echo   4. AI models (optional)
echo.

REM Check if we're in the correct directory
if not exist "backend" (
    echo ERROR: Please run this script from the ALA-Web root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ERROR: Frontend directory not found
    pause
    exit /b 1
)

echo.
echo ===============================================
echo Step 1/4: Python Environment Setup
echo ===============================================
echo.

REM Check for Conda
where conda >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Conda found. Creating virtual environment...
    REM Skip conda - use venv for consistency
    echo Conda detected but using standard venv for consistency...
    if errorlevel 1 (
        echo ERROR: Failed to create conda environment
        pause
        exit /b 1
    )
    
    REM Fallback to venv
    
) else (
    echo Conda not found. Using venv...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create venv
        echo Please install Python 3.11 or higher
        pause
        exit /b 1
    )
    
    call .venv\Scripts\activate
)

echo Python environment ready!
python --version

echo.
echo ===============================================
echo Step 2/4: Backend Dependencies
echo ===============================================
echo.

cd backend

echo Installing core dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some packages failed to install
    echo Continuing with installation...
)

echo Creating data directories...
if not exist "data" mkdir data
if not exist "data\uploads" mkdir data\uploads
if not exist "lib" mkdir lib

cd ..

echo.
echo ===============================================
echo Step 3/4: Frontend Dependencies
echo ===============================================
echo.

cd frontend

REM Check for npm
where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: npm not found!
    echo Please install Node.js from https://nodejs.org/
    cd ..
    pause
    exit /b 1
)

echo Node.js version:
node --version
echo npm version:
npm --version

echo.
echo Installing frontend packages...
echo This may take a few minutes...
npm install --legacy-peer-deps
if errorlevel 1 (
    echo ERROR: npm install failed
    echo Try running: npm cache clean --force
    cd ..
    pause
    exit /b 1
)

cd ..

echo.
echo ===============================================
echo Step 4/4: AI Models (Optional)
echo ===============================================
echo.

set /p INSTALL_AI="Do you want to install AI models (SAM2 + Florence-2)? This requires ~2GB and takes 5-10 minutes. (Y/N): "

if /i "%INSTALL_AI%"=="Y" (
    echo.
    echo Installing AI models to backend/lib...
    cd backend
    call setup_local_lib.bat
    cd ..
) else (
    echo.
    echo Skipping AI model installation.
    echo You can install later by running: backend\setup_local_lib.bat
)

echo.
echo ===============================================
echo Installation Complete!
echo ===============================================
echo.
echo Setup Summary:
echo   - Python environment: .venv (activated)
echo   - Backend dependencies: Installed
echo   - Frontend dependencies: Installed
echo   - AI models: %INSTALL_AI%
echo.
echo To start the application:
echo   1. Run: start_all.bat
echo   2. Open browser to: http://localhost:5173
echo.
echo To activate Python environment later:
  echo   - Windows: .venv\Scripts\activate
  echo   - Linux/macOS: source .venv/bin/activate
echo.

pause
