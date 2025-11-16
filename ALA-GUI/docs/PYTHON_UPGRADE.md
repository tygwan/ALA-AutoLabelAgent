# Python 3.10 Upgrade Guide

This guide explains how to upgrade your ALA-GUI environment from Python 3.9 to Python 3.10 to enable SAM2 segmentation.

## Why Upgrade?

- **Python 3.9**: Florence-2 bounding box detection only
- **Python 3.10**: Florence-2 + SAM2 refined segmentation ✅

## Current Environment Status

```bash
# Check available Python versions
py -0
```

**Your System:**
- ✅ Python 3.13 (64-bit) - Installed
- ✅ Python 3.10 (64-bit) - Installed
- ✅ Python 3.9 (64-bit) - Currently using (Anaconda)

**Result**: Python 3.10.1 is already installed and ready to use!

## Upgrade Steps

### Step 1: Backup Current Environment (Optional)

```bash
# Navigate to project directory
cd C:\Users\x8333\Desktop\AI_PJT\ALA-AutoLabelAgent\ALA-GUI

# Rename existing venv (backup)
mv venv venv_py39_backup
```

### Step 2: Create New Virtual Environment with Python 3.10

```bash
# Create new venv with Python 3.10
py -3.10 -m venv venv

# Verify Python version in new venv
venv\Scripts\python --version
# Should show: Python 3.10.1
```

### Step 3: Activate New Environment

```bash
# Activate venv (Windows)
venv\Scripts\activate

# Verify activation
python --version
# Should show: Python 3.10.1
```

### Step 4: Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 5: Install Dependencies

```bash
# Install all requirements
pip install -r requirements.txt

# Install Florence-2 dependencies
pip install timm einops

# Test torch installation
python -c "import torch; print(f'PyTorch {torch.__version__} - CUDA: {torch.cuda.is_available()}')"
```

### Step 6: Verify Installation

```bash
# Test Python version
python --version

# Test key packages
python -c "import PyQt6; import torch; import transformers; print('All imports successful')"
```

### Step 7: Test Application

```bash
# Run application
python src/main.py
```

**Test Checklist:**
1. Application starts without errors
2. Can open Auto-Annotate dialog
3. Can see both VLM and Seg Model dropdowns
4. Can load Florence-2 model
5. Can load SAM2 model (this should work now!)
6. Can run auto-annotation with refined masks

## Rollback (If Needed)

If you encounter issues and need to rollback to Python 3.9:

```bash
# Deactivate current venv
deactivate

# Remove Python 3.10 venv
rm -rf venv

# Restore Python 3.9 venv
mv venv_py39_backup venv

# Activate old venv
venv\Scripts\activate

# Verify
python --version
# Should show: Python 3.9.13
```

## Compatibility Notes

### Requirements Compatibility

All current requirements.txt dependencies are compatible with Python 3.10:

- ✅ PyQt6 6.6.1
- ✅ PyTorch 2.1.2
- ✅ Transformers 4.36.2
- ✅ timm, einops
- ✅ SAM2 (requires Python 3.10+)

### Breaking Changes

**None expected** - Python 3.10 is backward compatible with Python 3.9 code.

Key improvements in Python 3.10:
- Better error messages
- Structural pattern matching (match/case)
- Better type hints
- Performance improvements

## Troubleshooting

### "venv is not recognized"

```bash
# Use full path
C:\Users\x8333\Desktop\AI_PJT\ALA-AutoLabelAgent\ALA-GUI\venv\Scripts\activate
```

### "pip install fails for torch"

```bash
# Install PyTorch separately first
pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cu121

# Then install remaining requirements
pip install -r requirements.txt
```

### "SAM2 still fails to install"

Check Python version in activated venv:

```bash
python --version
# Must show 3.10 or higher
```

If showing 3.9, deactivate and recreate venv:

```bash
deactivate
rm -rf venv
py -3.10 -m venv venv
venv\Scripts\activate
```

## Expected Results After Upgrade

### Before (Python 3.9)
- Florence-2: ✅ Works
- SAM2: ❌ Installation fails
- Auto-Annotation: Bounding boxes only

### After (Python 3.10)
- Florence-2: ✅ Works
- SAM2: ✅ Works
- Auto-Annotation: Bounding boxes + refined segmentation masks

## Quick Upgrade Command (All-in-One)

```bash
# Navigate to project
cd C:\Users\x8333\Desktop\AI_PJT\ALA-AutoLabelAgent\ALA-GUI

# Backup old venv
mv venv venv_py39_backup

# Create new venv with Python 3.10
py -3.10 -m venv venv

# Activate
venv\Scripts\activate

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install timm einops

# Test
python src/main.py
```

## Post-Upgrade Verification

Run this Python script to verify everything:

```python
import sys
import torch
import PyQt6
import transformers

print(f"Python version: {sys.version}")
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"PyQt6 version: {PyQt6.QtCore.qVersion()}")
print(f"Transformers version: {transformers.__version__}")

# Test imports
try:
    import timm
    import einops
    print("✅ Florence-2 dependencies OK")
except ImportError as e:
    print(f"❌ Florence-2 dependencies missing: {e}")

print("\n✅ All checks passed! Ready to use SAM2.")
```

Save as `test_environment.py` and run:

```bash
python test_environment.py
```

## Support

If you encounter any issues during upgrade:
1. Check Python version: `python --version` (should be 3.10.x)
2. Check venv activation: Look for `(venv)` in terminal prompt
3. Reinstall dependencies: `pip install --force-reinstall -r requirements.txt`
4. Review error messages carefully
5. Rollback to Python 3.9 if needed (see Rollback section)
