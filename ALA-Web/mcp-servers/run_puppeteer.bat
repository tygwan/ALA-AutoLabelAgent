@echo off
cd /d "%~dp0"
echo Starting Puppeteer MCP Server...
npx -y @modelcontextprotocol/server-puppeteer
pause
