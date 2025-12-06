# ALA-Web Installation Guide

## 🚀 Quick Start

### Windows
1. Clone the repository
2. Run `setup.bat` (Double-click)
3. Run `run.bat` (Double-click)

### Linux/macOS
1. Clone the repository
2. Run `./setup.sh`
3. Run `./run.sh`

---

## 📋 Automatic Installation Details

The setup scripts (`setup.bat` / `setup.sh`) automatically handle:

1.  **Environment Check**: Verifies Python 3.11+ and Node.js 18+ are installed.
2.  **Virtual Environment**: Creates a Python virtual environment in `.venv` (root directory).
3.  **Backend Setup**: Installs all Python dependencies (FastAPI, PyTorch, etc.).
4.  **AI Models (Optional)**: Downloads SAM2 and Florence-2 models (~2GB).
5.  **Frontend Setup**: Installs Node.js dependencies (React, Vite, etc.).

> **Note**: This project uses `.venv` in the root directory as the canonical Python environment.

---

## 🔧 Manual Installation

If the automatic scripts fail, follow these steps manually.

### Windows (PowerShell)

```powershell
# 1. Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate

# 2. Install Backend Dependencies
cd backend
pip install -r requirements.txt

# 3. Install AI Models (Optional)
python ..\scripts\download_models.py

# 4. Install Frontend Dependencies
cd ..\frontend
npm install --legacy-peer-deps
```

### Linux/macOS (Bash)

```bash
# 1. Create Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install Backend Dependencies
cd backend
pip install -r requirements.txt

# 3. Install AI Models (Optional)
python ../scripts/download_models.py

# 4. Install Frontend Dependencies
cd ../frontend
npm install --legacy-peer-deps
```

---

## 🏃‍♂️ Running the Application

### Windows
Run `run.bat`. This will open two terminal windows:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:5173

### Linux/macOS
Run `./run.sh`. This will start both servers in the current terminal.

### Manual Start

**Backend**:
```bash
# Activate virtual environment first!
cd backend
python main.py
```

**Frontend**:
```bash
cd frontend
npm run dev
```

---

## ❓ Troubleshooting

See [docs/troubleshooting.md](docs/troubleshooting.md) for detailed solutions to common issues like:
- Python/Node.js version mismatches
- CUDA/GPU errors
- Port conflicts
