@echo off
REM =============================================================================
REM ALA-Web Startup Script
REM Starts both backend and frontend servers
REM =============================================================================

echo.
echo ===============================================
echo Starting ALA-Web Application
echo ===============================================
echo.

REM Check if in correct directory
if not exist "backend" (
    echo ERROR: Please run this script from the ALA-Web root directory
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ERROR: Frontend directory not found
    pause
    exit /b 1
)

echo This will open 2 terminal windows:
echo   - Backend server (http://localhost:8000)
echo   - Frontend server (http://localhost:5173)
echo.
echo Press Ctrl+C in each window to stop the servers.
echo.
pause

REM Start backend in new window
echo Starting backend server...
start "ALA-Web Backend" cmd /k "cd /d %~dp0backend && (conda activate ala 2>nul || call ..\ala\Scripts\activate.bat) && python main.py"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in new window
echo Starting frontend server...
start "ALA-Web Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ===============================================
echo Servers Starting...
echo ===============================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo The frontend should automatically open in your browser.
echo If not, manually navigate to: http://localhost:5173
echo.
echo To stop servers: Close both terminal windows or press Ctrl+C
echo.
