@echo off
REM Backend startup script

echo Starting ALA-Web Backend...
echo.

cd /d %~dp0

REM Strict check for .venv in root
if exist "..\.venv\Scripts\activate.bat" (
    call ..\.venv\Scripts\activate.bat
    echo Using Python environment: .venv
) else (
    echo ERROR: .venv not found in root! Run setup.bat first.
    pause
    exit /b 1
)

REM Check Python
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo.
echo Starting FastAPI server...
echo Backend will be available at: http://localhost:8000
echo API docs: http://localhost:8000/docs
echo.

python main.py
if errorlevel 1 (
    echo.
    echo ERROR: Backend server crashed or failed to start.
    pause
)
pause
