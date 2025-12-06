#!/bin/bash
set -e

echo "========================================"
echo "  ALA-Web Automated Setup"
echo "========================================"

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found! Please install Python 3.11 or higher."
    exit 1
fi

# Check for Node.js
if ! command -v npm &> /dev/null; then
    echo "ERROR: npm not found! Please install Node.js."
    exit 1
fi

# Create virtual environment
echo ""
echo "[1/4] Creating Python virtual environment (.venv)..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
else
    echo ".venv already exists."
fi

# Activate virtual environment
source .venv/bin/activate

# Install backend dependencies
echo ""
echo "[2/4] Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# Install AI models (Optional)
echo ""
echo "[3/4] AI Model Setup"
read -p "Do you want to install AI models (SAM2 + Florence-2)? This requires ~2GB. (Y/N): " INSTALL_AI
if [[ "$INSTALL_AI" =~ ^[Yy]$ ]]; then
    echo "Installing AI models..."
    python ../scripts/download_models.py
else
    echo "Skipping AI model installation."
fi

# Install frontend dependencies
echo ""
echo "[4/4] Installing frontend dependencies..."
cd ../frontend
npm install --legacy-peer-deps

cd ..
echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "You can now run the application using ./run.sh"
echo ""
