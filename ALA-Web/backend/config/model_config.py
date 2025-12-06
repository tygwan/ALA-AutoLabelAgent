"""
Model configuration for ALA-Web AI models
"""

import os
from pathlib import Path
import torch

# Base paths
BASE_DIR = Path(__file__).parent.parent  # backend/
CHECKPOINT_DIR = BASE_DIR / "checkpoints"
SAM2_DIR = BASE_DIR / "sam2"

# SAM2 Configuration
SAM2_CONFIG = "sam2.1_hiera_l.yaml"
SAM2_CHECKPOINT = CHECKPOINT_DIR / "sam2.1_hiera_large.pt"

# Florence-2 Configuration
FLORENCE2_MODEL = "microsoft/Florence-2-large"  # Auto-downloads from HuggingFace

# Device Configuration
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Ensure directories exist
CHECKPOINT_DIR.mkdir(exist_ok=True, parents=True)

# Print configuration on import
print(f"[Model Config] Device: {DEVICE}")
print(f"[Model Config] SAM2 Checkpoint: {SAM2_CHECKPOINT}")
print(f"[Model Config] Florence-2: {FLORENCE2_MODEL}")
