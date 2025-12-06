@echo off
REM Setup SAM2 model for ALA-Web

echo ========================================
echo Installing SAM2
echo ========================================

cd /d %~dp0

REM Activate Python environment
call ..\.venv\Scripts\activate.bat

REM Clone SAM2 if not exists
if not exist "sam2\" (
    echo Cloning SAM2 repository...
    git clone https://github.com/facebookresearch/sam2.git
    if errorlevel 1 (
        echo ERROR: Failed to clone SAM2 repository
        echo Make sure git is installed
        pause
        exit /b 1
    )
    cd sam2
) else (
    echo SAM2 already cloned
    cd sam2
)

REM Install SAM2
echo.
echo Installing SAM2...
pip install -e .
if errorlevel 1 (
    echo ERROR: Failed to install SAM2
    pause
    exit /b 1
)

REM Download checkpoint
echo.
echo Downloading SAM2 checkpoint...
cd ..
if not exist "checkpoints\" mkdir checkpoints

REM Download SAM2 Hiera Large checkpoint (~300MB)
echo Downloading sam2.1_hiera_large.pt ...
powershell -Command "& {Invoke-WebRequest -Uri 'https://dl.fbaipublicfiles.com/segment_anything_2/092824/sam2.1_hiera_large.pt' -OutFile 'checkpoints\sam2.1_hiera_large.pt'}"

if errorlevel 1 (
    echo ERROR: Failed to download checkpoint
    pause
    exit /b 1
)

echo.
echo ========================================
echo SAM2 Setup Complete!
echo ========================================
echo Checkpoint saved to: checkpoints\sam2.1_hiera_large.pt
echo.
pause
