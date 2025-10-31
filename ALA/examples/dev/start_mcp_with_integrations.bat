@echo off
REM MCP API Server Launcher with Integrations
REM This script starts the entire MCP system with Cloudflare tunnel and n8n integrations

echo Creating required directories...
mkdir mcp\categories 2>nul
mkdir mcp\config 2>nul
mkdir n8n-data 2>nul

REM Check if cloudflared is installed
where cloudflared >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo cloudflared is not installed. Please install it first:
    echo Download from: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
    pause
    exit /b
)

REM Check if docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b
)

echo Starting MCP API server with integrations...

REM Start the entire system using docker-compose
docker-compose up

REM This script will remain active until docker-compose is stopped with Ctrl+C 