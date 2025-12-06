@echo off
REM Setup script for installing AI libraries to local lib folder
REM This mimics project-agi's approach of using a local lib directory

echo ===============================================
echo ALA-Web Local Lib Setup
echo ===============================================
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo ERROR: Please activate the '.venv' virtual environment first!
    echo Run: .venv\Scripts\activate
    pause
    exit /b 1
)

echo Current Python: %VIRTUAL_ENV%\python.exe
echo.

set LIB_DIR=%~dp0lib
set SAM2_DIR=%LIB_DIR%\segment-anything-2
set CACHE_DIR=%LIB_DIR%\cache

echo Creating lib directory structure...
if not exist "%LIB_DIR%" mkdir "%LIB_DIR%"
if not exist "%CACHE_DIR%\" mkdir "%CACHE_DIR%"

echo.
echo ===============================================
echo Step 1: Installing PyTorch (if needed)
echo ===============================================
python -c "import torch; print(f'PyTorch {torch.__version__} already installed')" 2>nul
if errorlevel 1 (
    echo Installing PyTorch with CUDA support...
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
) else (
    echo PyTorch is already installed.
)

echo.
echo ===============================================
echo Step 2: Cloning SAM2 Repository
echo ===============================================
if exist "%SAM2_DIR%" (
    echo SAM2 directory already exists at %SAM2_DIR%
    echo Skipping clone...
) else (
    echo Cloning segment-anything-2 to lib folder...
    cd /d "%LIB_DIR%"
    git clone https://github.com/facebookresearch/segment-anything-2.git
    if errorlevel 1 (
        echo ERROR: Failed to clone SAM2 repository
        pause
        exit /b 1
    )
)

echo.
echo ===============================================
echo Step 3: Installing SAM2 in editable mode
echo ===============================================
cd /d "%SAM2_DIR%"
pip install -e .
if errorlevel 1 (
    echo WARNING: SAM2 installation had issues, but continuing...
    echo This might be due to CUDA extension compilation failures.
    echo The model should still work for basic functionality.
)

echo.
echo ===============================================
echo Step 4: Downloading SAM2 Checkpoint
echo ===============================================
set CHECKPOINT_FILE=%CACHE_DIR%\sam2_hiera_base_plus.pt
if exist "%CHECKPOINT_FILE%" (
    echo Checkpoint already exists at %CHECKPOINT_FILE%
) else (
    echo Downloading SAM2 checkpoint (~150MB)...
    python -c "import urllib.request; urllib.request.urlretrieve('https://dl.fbaipublicfiles.com/segment_anything_2/072824/sam2_hiera_base_plus.pt', r'%CHECKPOINT_FILE%')"
    if errorlevel 1 (
        echo ERROR: Failed to download checkpoint
        pause
        exit /b 1
    )
)

echo.
echo ===============================================
echo Step 5: Installing autodistill packages
echo ===============================================
pip install autodistill autodistill-grounded-sam-2 autodistill-florence-2 autodistill-yolov8
if errorlevel 1 (
    echo ERROR: Failed to install autodistill packages
    pause
    exit /b 1
)

echo.
echo ===============================================
echo Step 6: Installing additional dependencies
echo ===============================================
pip install supervision opencv-python pillow numpy

echo.
echo ===============================================
echo Installation Complete!
echo ===============================================
echo.
echo Library structure:
echo   %LIB_DIR%\segment-anything-2  (SAM2 source)
echo   %CACHE_DIR%\sam2_hiera_base_plus.pt  (model checkpoint)
echo.
echo To update the backend PATH configuration:
echo   - main.py already adds lib/ to sys.path
echo   - auto_annotator.py imports from this path
echo.
echo You can now run the backend with AI support!
echo.
pause
