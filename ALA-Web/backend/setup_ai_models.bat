@echo off
REM Simplified AI Models Setup - No manual SAM2 download needed!

echo ========================================
echo ALA-Web AI Models Setup
echo ========================================
echo.
echo This will install:
echo - autodistill-grounded-sam-2 (includes Florence-2 + SAM2!)
echo - PyTorch and dependencies
echo - Vision utilities (OpenCV, supervision)
echo.
echo NO manual SAM2 download required!
echo Everything is handled automatically.
echo.
echo Estimated time: 5-10 minutes
echo Required space: ~3GB
echo.
pause

cd /d %~dp0
call ..\.venv\Scripts\activate.bat

echo.
echo Installing AI dependencies...
pip install -r requirements_ai.txt

if errorlevel 1 (
    echo ERROR: Failed to install AI dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Testing model imports...
echo ========================================
python -c "from autodistill_grounded_sam_2 import GroundedSAM2; print('GroundedSAM2: OK')"

if errorlevel 1 (
    echo ERROR: Failed to import GroundedSAM2
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Models installed:
echo - GroundedSAM2 (Florence-2 + SAM2): Ready
echo.
echo You can now use auto-annotation features!
echo.
echo Note: Models will auto-download on first use (~2GB)
echo.
pause
