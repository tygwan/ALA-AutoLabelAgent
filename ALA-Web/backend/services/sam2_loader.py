"""
SAM2 Loader for ALA-Web
Mimics the loading pattern from autodistill-grounded-sam-2 helpers.py
but adapted for local lib folder structure
"""
import os
import sys
import subprocess
import urllib.request
import torch

# Get paths
BACKEND_DIR = os.path.dirname(os.path.dirname(__file__))
LIB_DIR = os.path.join(BACKEND_DIR, 'lib')
SAM2_DIR = os.path.join(LIB_DIR, 'segment-anything-2')
CACHE_DIR = os.path.join(LIB_DIR, 'cache')
CHECKPOINT_PATH = os.path.join(CACHE_DIR, 'sam2_hiera_base_plus.pt')

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if not torch.cuda.is_available():
    print("WARNING: CUDA not available. SAM2 will run slowly on CPU.")

def ensure_sam2_installed():
    """
    Ensure SAM2 is cloned and installed in the local lib directory.
    This mimics the behavior of autodistill helpers but uses local lib.
    """
    # Ensure directories exist
    os.makedirs(LIB_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    # Check if SAM2 is cloned
    if not os.path.isdir(SAM2_DIR):
        print(f"SAM2 not found in {SAM2_DIR}")
        print("Please run: backend/setup_local_lib.bat")
        raise RuntimeError(
            "SAM2 is not installed. Run setup_local_lib.bat to install required libraries."
        )
    
    # Add SAM2 to path if not already there
    if SAM2_DIR not in sys.path:
        sys.path.insert(0, SAM2_DIR)
        print(f"Added SAM2 to path: {SAM2_DIR}")
    
    # Check for checkpoint
    if not os.path.isfile(CHECKPOINT_PATH):
        print(f"Downloading SAM2 checkpoint to {CHECKPOINT_PATH}...")
        url = "https://dl.fbaipublicfiles.com/segment_anything_2/072824/sam2_hiera_base_plus.pt"
        urllib.request.urlretrieve(url, CHECKPOINT_PATH)
        print("Checkpoint downloaded successfully")

def load_sam2_predictor():
    """
    Load SAM2 predictor following the pattern from autodistill helpers.
    Returns: SAM2ImagePredictor instance
    """
    ensure_sam2_installed()
    
    try:
        from sam2.build_sam import build_sam2
        from sam2.sam2_image_predictor import SAM2ImagePredictor
    except ImportError as e:
        raise ImportError(
            f"Failed to import SAM2 modules: {e}\n"
            f"Please run setup_local_lib.bat to install SAM2"
        )
    
    # Build model
    model_cfg = "sam2_hiera_b+.yaml"
    checkpoint = CHECKPOINT_PATH
    
    print(f"Loading SAM2 model from {checkpoint}")
    
    sam2_model = build_sam2(model_cfg, checkpoint, device=DEVICE)
    predictor = SAM2ImagePredictor(sam2_model)
    
    print("SAM2 predictor loaded successfully")
    return predictor

# Global predictor instance (lazy loaded)
_sam2_predictor = None

def get_sam2_predictor():
    """
    Get or create the SAM2 predictor instance (singleton pattern).
    """
    global _sam2_predictor
    if _sam2_predictor is None:
        _sam2_predictor = load_sam2_predictor()
    return _sam2_predictor
