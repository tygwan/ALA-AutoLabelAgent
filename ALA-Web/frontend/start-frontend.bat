@echo off
REM Frontend startup script

echo Starting ALA-Web Frontend...
echo.

cd /d %~dp0

REM Check if node_modules exists
if not exist "node_modules" (
    echo ERROR: node_modules not found!
    echo Please run: npm install --legacy-peer-deps
    pause
    exit /b 1
)

echo Starting Vite dev server...
echo Frontend will be available at: http://localhost:5173
echo.

npm run dev
