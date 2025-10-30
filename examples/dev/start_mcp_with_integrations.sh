#!/bin/bash
# MCP API Server Launcher with Integrations
# This script starts the entire MCP system with Cloudflare tunnel and n8n integrations

# Create required directories
mkdir -p mcp/categories
mkdir -p mcp/config
mkdir -p n8n-data

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo "cloudflared is not installed. Please install it first:"
    echo "On Linux: curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && sudo dpkg -i cloudflared.deb"
    echo "On macOS: brew install cloudflare/cloudflare/cloudflared"
    echo "On Windows: Install using the installer from https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/"
    exit 1
fi

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker and Docker Compose first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "Starting MCP API server with integrations..."

# Start the entire system using docker-compose
docker-compose up

# This script will remain active until docker-compose is stopped with Ctrl+C 