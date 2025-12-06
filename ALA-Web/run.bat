@echo off
title ALA-Web Launcher

echo ========================================
echo   ALA-Web Launcher
echo ========================================

REM Check if setup has been run
if not exist ".venv" (
    echo ERROR: Virtual environment not found!
    echo Please run "setup.bat" first.
    pause
    exit /b 1
)

echo.
echo Starting servers...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Press Ctrl+C in the new windows to stop servers.
echo.

REM Activate environment and start backend
call .venv\Scripts\activate.bat
start "ALA-Web Backend" cmd /k "cd backend && python main.py"

REM Start frontend
start "ALA-Web Frontend" cmd /k "cd frontend && npm run dev"

REM Wait a moment to ensure windows open
timeout /t 2 >nul
