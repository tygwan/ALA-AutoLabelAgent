# Local Lib Installation Guide

## Overview

ALA-Web uses a **local library approach** similar to project-agi, where AI models and dependencies are installed in a local `backend/lib` folder rather than globally. This approach:

- ✅ Isolates AI dependencies from the core application
- ✅ Allows version control of exact package versions
- ✅ Mimics project-agi's proven architecture
- ✅ Makes the project portable

## Architecture

```
backend/
├── lib/                          # Local library folder (like project-agi)
│   ├── segment-anything-2/      # SAM2 cloned from GitHub
│   └── cache/                    # Model checkpoints
│       └── sam2_hiera_base_plus.pt
├── services/
│   ├── sam2_loader.py           # Custom SAM2 loader (mimics autodistill helpers)
│   └── auto_annotator.py        # Uses local lib
└── main.py                       # Adds lib/ to sys.path
```

## Installation Steps

### Prerequisites

1. **Activate Virtual Environment**
   ```bash
   conda activate ala
   # OR
   ala\Scripts\activate
   ```

2. **Ensure Git is Installed**
   ```bash
   git --version
   ```

### Automatic Installation (Recommended)

Run the setup script:

```bash
cd backend
setup_local_lib.bat
```

This script will:
1. ✅ Install/verify PyTorch
2. ✅ Clone SAM2 to `backend/lib/segment-anything-2`
3. ✅ Install SAM2 in editable mode (`pip install -e .`)
4. ✅ Download SAM2 checkpoint (~150MB)
5. ✅ Install autodistill packages
6. ✅ Install additional dependencies

### Manual Installation

If the automatic script fails:

```bash
# 1. Create lib directory
mkdir backend\lib
cd backend\lib

# 2. Clone SAM2
git clone https://github.com/facebookresearch/segment-anything-2.git
cd segment-anything-2
pip install -e .

# 3. Download checkpoint
mkdir ..\cache
# Use Python to download:
python -c "import urllib.request; urllib.request.urlretrieve('https://dl.fbaipublicfiles.com/segment_anything_2/072824/sam2_hiera_base_plus.pt', r'..\cache\sam2_hiera_base_plus.pt')"

# 4. Install autodistill packages  
pip install autodistill autodistill-grounded-sam-2 autodistill-florence-2 autodistill-yolov8

# 5. Install dependencies
pip install supervision opencv-python pillow numpy
```

## How It Works

### SAM2 Loading Mechanism

The `autodistill-grounded-sam-2` package uses a `helpers.py` module that:

1. **Checks for SAM2**: Looks in `~/.cache/autodistill/segment_anything_2/`
2. **Git Clone**: If not found, clones SAM2 repository
3. **Editable Install**: Runs `pip install -e .` to install SAM2
4. **Checkpoint Download**: Downloads model weights
5. **Import**: Adds to `sys.path` and imports SAM2 modules

### Our Adaptation

We replicate this pattern but use `backend/lib` instead:

**`services/sam2_loader.py`**:
```python
# Check backend/lib/segment-anything-2
# Download checkpoint to backend/lib/cache
# Add to sys.path
# Load SAM2 predictor
```

**`main.py`**:
```python
# Add backend/lib to sys.path at startup
lib_path = os.path.join(os.path.dirname(__file__), 'lib')
sys.path.insert(0, lib_path)
```

**`services/auto_annotator.py`**:
```python
# Import from local lib
from services.sam2_loader import get_sam2_predictor
# Use custom implementation instead of GroundedSAM2
```

## Verification

After installation, verify everything works:

```bash
cd backend
python -c "from services.sam2_loader import get_sam2_predictor; print('SAM2 loaded successfully!')"
```

Expected output:
```
Added SAM2 to path: C:\...\backend\lib\segment-anything-2
Loading SAM2 model from C:\...\backend\lib\cache\sam2_hiera_base_plus.pt
SAM2 predictor loaded successfully
SAM2 loaded successfully!
```

## Troubleshooting

### CUDA Extension Compilation Failures

If you see:
```
Failed to build the SAM 2 CUDA extension
```

This is **normal** and can be ignored. SAM2 will still work, though some post-processing may be slower.

### Import Errors

If you get `ModuleNotFoundError: No module named 'sam2'`:

1. Verify SAM2 is cloned: `dir backend\lib\segment-anything-2`
2. Check sys.path: Run backend and look for "Added SAM2 to path" message
3. Reinstall SAM2: `cd backend\lib\segment-anything-2 && pip install -e .`

### Git Not Found

Install Git from: https://git-scm.com/download/win

### Slow Performance

- SAM2 requires CUDA for good performance
- Verify CUDA is available: `python -c "import torch; print(torch.cuda.is_available())"`
- Install PyTorch with CUDA: `pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118`

## Comparison: Global vs Local Lib

| Aspect | Global Install | Local Lib (Our Approach) |
|--------|---------------|--------------------------|
| Installation | `pip install autodistill-grounded-sam-2` | `setup_local_lib.bat` |
| Location | Site-packages | `backend/lib/` |
| Portability | ❌ Environment-dependent | ✅ Self-contained |
| Version Control | ⚠️ May vary | ✅ Fixed versions |
| project-agi compatibility | ❌ Different approach | ✅ Same pattern |

## References

- [SAM2 GitHub](https://github.com/facebookresearch/segment-anything-2)
- [autodistill-grounded-sam-2](https://github.com/autodistill/autodistill-grounded-sam-2)
- [autodistill helpers.py](https://github.com/autodistill/autodistill-grounded-sam-2/blob/main/autodistill_grounded_sam_2/helpers.py) - Our implementation is based on this
