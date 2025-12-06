#!/bin/bash

echo "========================================"
echo "  ALA-Web Launcher"
echo "========================================"

# Check if setup has been run
if [ ! -d ".venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run ./setup.sh first."
    exit 1
fi

echo ""
echo "Starting servers..."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all servers."
echo ""

# Activate environment
source .venv/bin/activate

# Trap Ctrl+C to kill child processes
trap 'kill 0' SIGINT

# Start backend in background
cd backend
python main.py &
BACKEND_PID=$!

# Start frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Wait for processes
wait
