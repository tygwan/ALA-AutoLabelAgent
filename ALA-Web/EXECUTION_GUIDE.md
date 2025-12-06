# ALA-Web Execution Guide

## Environment Requirements

### Backend
- **Python Version**: 3.10+ (3.11+ recommended per INSTALL.md)
- **Virtual Environment**: Uses `.venv` directory (Python venv)
- **Dependencies**: Installed via `pip install -r backend/requirements.txt`
- **AI Dependencies**: Optional, installed via `backend/setup_ai_env.bat`

### Frontend
- **Runtime**: Node.js 18+
- **Package Manager**: npm
- **No Python Required**: Frontend is pure JavaScript/TypeScript
- **Dependencies**: Installed via `npm install` in frontend directory

## Independent Execution

### Backend (Port 8000)

**Option 1: Using Batch Script (Recommended)**
```cmd
cd backend
start-backend.bat
```

**Option 2: Manual Execution**
```cmd
# 1. Activate virtual environment
.venv\Scripts\activate  # Windows
# OR source .venv/bin/activate  # Linux/macOS

# 2. Run backend
cd backend
python main.py
```

**Backend will be available at:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### Frontend (Port 5173)

**Option 1: Using Batch Script**
```cmd
cd frontend
start-frontend.bat
```

**Option 2: Manual Execution**
```cmd
cd frontend
npm run dev
```

**Frontend will be available at:**
- UI: http://localhost:5173

## Running Both Simultaneously

**Windows:**
```cmd
run.bat  # Runs both in separate windows
```

**Linux/macOS:**
```bash
./run.sh  # Runs both in same terminal
```

## Key Points

1. **Independence**: Backend and Frontend run as separate processes on different ports
2. **Communication**: Frontend (5173) makes HTTP requests to Backend (8000)
3. **CORS**: Backend configured to accept requests from http://localhost:5173
4. **Python Isolation**: Frontend has zero Python dependencies - uses only Node.js
5. **Virtual Environments**: Backend uses `.venv`, Frontend uses `node_modules`

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (should be 3.10+)
- Verify virtual environment is activated
- Check if port 8000 is already in use

### Frontend won't start
- Check Node.js version: `node --version` (should be 18+)
- Verify `npm install` completed successfully
- Check if port 5173 is already in use

### CORS Errors
- Ensure backend is running on port 8000
- Ensure frontend is accessing http://localhost:5173 (not 127.0.0.1)
