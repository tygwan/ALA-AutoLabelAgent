# Troubleshooting Guide

## 🐍 Python Environment Issues

### "Python not found" or Version Mismatch
- **Requirement**: Python 3.11 or higher.
- **Check**: Run `python --version`.
- **Solution**: Install from [python.org](https://www.python.org/downloads/). Ensure "Add Python to PATH" is checked during installation.

### Virtual Environment Activation Fails
- **Windows**:
    - Error: `running scripts is disabled on this system`.
    - Fix: Run PowerShell as Administrator and execute: `Set-ExecutionPolicy RemoteSigned`.
- **General**:
    - Ensure you are in the project root.
    - Try deleting `.venv` folder and running setup again.

---

## 📦 Node.js & Frontend Issues

### "npm not found"
- **Requirement**: Node.js 18 or higher.
- **Check**: Run `node -v` and `npm -v`.
- **Solution**: Install from [nodejs.org](https://nodejs.org/).

### `npm install` Fails
- **Error**: `ERESOLVE unable to resolve dependency tree`.
- **Solution**: Use the legacy peer deps flag (already in scripts):
  ```bash
  npm install --legacy-peer-deps
  ```
- **Clear Cache**:
  ```bash
  npm cache clean --force
  rm -rf node_modules
  rm package-lock.json
  npm install --legacy-peer-deps
  ```

---

## 🎮 GPU & AI Model Issues

### "CUDA not available" / Slow Performance
- **Cause**: PyTorch installed without CUDA support or drivers missing.
- **Solution**:
  1. Install latest [NVIDIA Drivers](https://www.nvidia.com/Download/index.aspx).
  2. Reinstall PyTorch with CUDA support:
     ```bash
     pip uninstall torch torchvision
     pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
     ```

### AI Model Download Fails
- **Cause**: Network interruption or Git missing.
- **Solution**:
  - Ensure Git is installed (`git --version`).
  - Run the download script manually:
    ```bash
    python scripts/download_models.py
    ```

---

## 🌐 Server & Network Issues

### "Port already in use"
- **Error**: Port 8000 (Backend) or 5173 (Frontend) is busy.
- **Solution (Windows)**:
  ```powershell
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  ```
- **Solution (Linux/Mac)**:
  ```bash
  lsof -ti:8000 | xargs kill -9
  ```

### Frontend cannot connect to Backend
- **Check**: Is the backend server running on port 8000?
- **Check**: Look for CORS errors in browser console (F12).
