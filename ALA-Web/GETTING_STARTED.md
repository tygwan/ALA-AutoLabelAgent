# 🏁 Getting Started with ALA-Web

Welcome! This guide will help you set up and run the **ALA-Web** auto-labeling tool from scratch.

---

## 📋 1. Prerequisites (Before You Start)

Ensure you have the following installed on your computer.

### Windows
1.  **Git**: [Download Git](https://git-scm.com/download/win)
2.  **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
    *   *Important*: Check "Add Python to PATH" during installation.
3.  **Node.js 18+ (LTS)**: [Download Node.js](https://nodejs.org/)

### Quick Check
Open `Command Prompt` (cmd) or `PowerShell` and run:
```cmd
python --version
node --version
git --version
```
*If any command says "not recognized", please install that tool first.*

---

## 🛠️ 2. Automated Setup

We have made setup easy with a "one-click" script.

1.  **Navigate** to the `ALA-Web` folder in your file explorer.
2.  **Double-click** `setup.bat`.

### What happens next?
1.  **Environment Check**: Checks if Python and Node.js are ready.
2.  **Virtual Environment**: Creates a private python environment (`.venv`) so it doesn't mess with your system.
3.  **Dependencies**: Installs all required AI libraries (starts downloading ~2GB of data if you choose 'Y' for AI models).
    *   *Note*: A temporary folder `C:\ala_tmp_build` might be created to help install large files. This is normal.
4.  **Frontend**: Installs the web interface parts.

**Success Message**:
You should see:
```text
========================================
  Setup Complete!
========================================
You can now run the application using "run.bat"
```

---

## 🚀 3. Running the App

1.  **Double-click** `run.bat` in the `ALA-Web` folder.
2.  Two black terminal windows will open:
    *   **Backend**: The AI brain server (API)
    *   **Frontend**: The Web interface launcher
3.  Your internet browser should automatically open to **http://localhost:5173**.

---

## ❓ Common Issues (FAQ)

### "Path too long" or Installation Errors
*   **Solution**: We recently updated `setup.bat` to fix this. Run `git pull` to get the latest version, or re-download the project.

### "Python not found"
*   **Solution**: Re-install Python and make sure to check the box **"Add Python to PATH"** in the installer.

### Browser doesn't open
*   **Solution**: Manually open your browser (Chrome/Edge) and type `http://localhost:5173` in the address bar.

### App is stuck on "Loading..."
*   **Solution**: Check the black terminal window labeled "Backend". If it shows an error, please take a screenshot and report it.
