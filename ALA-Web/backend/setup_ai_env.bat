@echo off
setlocal EnableDelayedExpansion

title ALA-Web AI Environment Setup

echo ===================================================
echo ALA-Web AI Environment Setup (Torch 2.3.1 + SAM2)
echo ===================================================
echo.

REM 1. Check Python Version
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

for /f "tokens=2" %%I in ('python --version 2^>^&1') do set PYTHON_VER=%%I
echo Detected Python: %PYTHON_VER%
echo.

REM 2. Check for Virtual Environment
if not defined VIRTUAL_ENV (
    echo WARNING: No virtual environment detected!
    echo It is HIGHLY recommended to run this inside a virtual environment (e.g., .venv or ala).
    echo.
    set /p CONTINUE="Continue anyway? (Y/N): "
    if /i "!CONTINUE!" NEQ "Y" exit /b 1
) else (
    echo Detected Virtual Environment: !VIRTUAL_ENV!
)

REM 3. Clean Install of Torch
echo.
echo [1/6] Removing existing Torch installation...
pip uninstall -y torch torchvision torchaudio
if %ERRORLEVEL% NEQ 0 echo Warning: Failed to uninstall torch (maybe not installed)

echo.
echo [2/6] Installing PyTorch 2.3.1 + CUDA 12.1...
pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu121
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install PyTorch 2.3.1
    pause
    exit /b 1
)

REM 4. Install Flash Attention
echo.
echo [3/6] Installing Flash Attention...
if exist "flash_attn-2.6.3+cu123torch2.3.1cxx11abiFALSE-cp310-cp310-win_amd64.whl" (
    echo Found local wheel: flash_attn-2.6.3+cu123torch2.3.1cxx11abiFALSE-cp310-cp310-win_amd64.whl
    pip install flash_attn-2.6.3+cu123torch2.3.1cxx11abiFALSE-cp310-cp310-win_amd64.whl
) else (
    echo WARNING: Flash Attention wheel not found in current directory!
    echo Expected: flash_attn-2.6.3+cu123torch2.3.1cxx11abiFALSE-cp310-cp310-win_amd64.whl
    echo Skipping Flash Attention installation...
)

REM 5. Install Dependencies
echo.
echo [4/6] Installing Core Dependencies...
pip install opencv-python opencv-contrib-python cmake matplotlib PyQt6
pip install supervision roboflow
pip install autodistill autodistill-grounded-sam-2 autodistill-florence-2 autodistill-yolov8

REM 6. Setup SAM2
echo.
echo [5/6] Setting up SAM2...
set LIB_DIR=%~dp0lib
if not exist "%LIB_DIR%" mkdir "%LIB_DIR%"
cd /d "%LIB_DIR%"

if exist "segment-anything-2" (
    echo SAM2 repository already exists. Updating...
    cd segment-anything-2
    git pull
) else (
    echo Cloning SAM2...
    git clone https://github.com/facebookresearch/segment-anything-2.git
    cd segment-anything-2
)

echo Patching setup.py to prevent version conflicts...
python -c "import sys; lines = sys.stdin.readlines(); print(''.join([l.replace('torch>=', '# torch>=') if 'torch>=' in l else l for l in lines]))" < setup.py > setup.py.tmp
move /y setup.py.tmp setup.py >nul

echo Installing SAM2 with CUDA extension...
pip install -v -e ".[demo]"
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: SAM2 CUDA extension compilation failed.
    echo Falling back to standard installation...
    pip install -e .
)

REM 7. Download Checkpoint
echo.
echo [6/6] Downloading SAM2 Checkpoint...
set CACHE_DIR=%LIB_DIR%\cache
if not exist "%CACHE_DIR%" mkdir "%CACHE_DIR%"
set CHECKPOINT=%CACHE_DIR%\sam2_hiera_large.pt

if not exist "%CHECKPOINT%" (
    echo Downloading sam2_hiera_large.pt...
    python -c "import urllib.request; urllib.request.urlretrieve('https://dl.fbaipublicfiles.com/segment_anything_2/092824/sam2.1_hiera_large.pt', r'%CHECKPOINT%')"
) else (
    echo Checkpoint already exists.
)

echo.
echo ===================================================
echo Setup Complete!
echo ===================================================
echo Please restart the backend server.
echo.
pause
