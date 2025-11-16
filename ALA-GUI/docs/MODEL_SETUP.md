# Model Setup Guide

This guide explains how to download and setup AI models for ALA-GUI auto-annotation.

## Quick Start

ALA-GUI uses two types of models:
1. **VLM (Visual Language Model)** - For object detection (e.g., Florence-2)
2. **Segmentation Model** - For mask refinement (e.g., SAM2)

## Model Directory Structure

Default model directory: `~/.cache/ala-gui/models/`

Recommended structure:
```
~/.cache/ala-gui/models/
├── florence2/
│   ├── Florence-2-large/        # HuggingFace model
│   └── Florence-2-base/          # Optional
└── sam2/
    └── sam2_hiera_base_plus.pth  # SAM2 checkpoint
```

## Method 1: Auto-Download (Recommended)

### Florence-2 (Automatic from HuggingFace)

1. Open Auto-Annotate dialog
2. Select "Florence-2-large (HF)" or "Florence-2-base (HF)" from VLM Model dropdown
3. Click "Run Auto-Annotation"
4. Model will download automatically (~1.5GB for large, ~500MB for base)

### SAM2 (Automatic Download)

1. Select "SAM2 Base+ (Auto-download)" from Seg Model dropdown
2. Click "Run Auto-Annotation"
3. SAM2 will download automatically (~300MB)

## Method 2: Manual Download

### Florence-2

#### Option A: Using HuggingFace CLI
```bash
# Install huggingface_hub
pip install huggingface_hub

# Download Florence-2-large
huggingface-cli download microsoft/Florence-2-large --local-dir ~/.cache/ala-gui/models/florence2/Florence-2-large

# Or Florence-2-base (smaller, faster)
huggingface-cli download microsoft/Florence-2-base --local-dir ~/.cache/ala-gui/models/florence2/Florence-2-base
```

#### Option B: Using Python
```python
from transformers import AutoModelForCausalLM, AutoProcessor

model_id = "microsoft/Florence-2-large"
cache_dir = "~/.cache/ala-gui/models/florence2"

# Download model and processor
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    cache_dir=cache_dir
)
processor = AutoProcessor.from_pretrained(
    model_id,
    trust_remote_code=True,
    cache_dir=cache_dir
)
```

#### Option C: Manual Browser Download
1. Visit https://huggingface.co/microsoft/Florence-2-large/tree/main
2. Download all files to `~/.cache/ala-gui/models/florence2/Florence-2-large/`
3. Required files:
   - `config.json`
   - `model.safetensors` (or `pytorch_model.bin`)
   - `processor_config.json`
   - `tokenizer.json`
   - `tokenizer_config.json`
   - `vocab.json`

### SAM2

#### Option A: Using wget/curl
```bash
# Create directory
mkdir -p ~/.cache/ala-gui/models/sam2

# Download checkpoint
cd ~/.cache/ala-gui/models/sam2
wget https://dl.fbaipublicfiles.com/segment_anything_2/072824/sam2_hiera_base_plus.pt
mv sam2_hiera_base_plus.pt sam2_hiera_base_plus.pth
```

#### Option B: Using Python
```python
import urllib.request
import os

url = "https://dl.fbaipublicfiles.com/segment_anything_2/072824/sam2_hiera_base_plus.pt"
save_path = os.path.expanduser("~/.cache/ala-gui/models/sam2/sam2_hiera_base_plus.pth")

os.makedirs(os.path.dirname(save_path), exist_ok=True)
urllib.request.urlretrieve(url, save_path)
```

#### Option C: Manual Browser Download
1. Visit https://ai.meta.com/sam2/
2. Download SAM2 Base+ checkpoint (~300MB)
3. Save as `~/.cache/ala-gui/models/sam2/sam2_hiera_base_plus.pth`

### SAM2 Repository (Required for SAM2)

```bash
# Clone SAM2 repository
cd ~/.cache/ala-gui/models/sam2
git clone https://github.com/facebookresearch/segment-anything-2.git

# Install SAM2
cd segment-anything-2
pip install -e .
```

## Verifying Installation

1. Open ALA-GUI
2. Click Tools → Auto-Annotate (Ctrl+A)
3. Check VLM Model dropdown:
   - Should show available Florence-2 models
   - Shows HuggingFace models if no local models found
4. Check Seg Model dropdown:
   - Should show SAM2 models if checkpoint exists
   - Shows "Auto-download" option

## Model Information

### Florence-2 Models

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| Florence-2-large | ~1.5GB | Slower | Higher | Best quality |
| Florence-2-base | ~500MB | Faster | Good | Faster processing |

### SAM2 Models

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| SAM2 Base+ | ~300MB | Medium | High |

## Troubleshooting

### "No VLM models found"
- Check model directory: `~/.cache/ala-gui/models/florence2/`
- Verify folder contains `config.json`
- Try selecting HuggingFace auto-download option

### "No segmentation models found"
- Check model directory: `~/.cache/ala-gui/models/sam2/`
- Verify checkpoint file exists: `sam2_hiera_base_plus.pth`
- Try selecting "Auto-download" option

### "Failed to load models"
- Ensure PyTorch is installed: `pip install torch`
- Ensure transformers is installed: `pip install transformers`
- Check internet connection (for HuggingFace downloads)
- Verify disk space (~2-5GB free)

### Model downloads are slow
- Use manual download methods (wget, browser)
- Download during off-peak hours
- Use mirror sites if available

## Custom Model Directory

To change the model directory:
1. Go to Tools → Preferences
2. Navigate to "Model" tab
3. Set "Model Directory" path
4. Click "OK"
5. Restart ALA-GUI

## Using HuggingFace Models Directly

You can use HuggingFace model IDs without downloading:
1. Select "Florence-2-large (HF)" or "Florence-2-base (HF)"
2. Model will download to cache on first use
3. Subsequent uses will load from cache

## Disk Space Requirements

- Florence-2-large: ~1.5GB
- Florence-2-base: ~500MB
- SAM2 Base+: ~300MB
- SAM2 repository: ~100MB
- **Total: ~2-3GB**

Ensure you have at least 5GB free space for safe installation.

## Performance Tips

### GPU Acceleration
- Install CUDA-enabled PyTorch for NVIDIA GPUs
- ~10-50x faster than CPU
- Requires CUDA toolkit installation

### MPS (Apple Silicon)
- Automatic on M1/M2/M3 Macs with PyTorch 1.12+
- ~5-10x faster than CPU

### CPU Only
- Works on any system
- Slower but functional
- Recommended for small datasets only

## Next Steps

After setting up models:
1. Load an image in ALA-GUI
2. Open Auto-Annotate dialog (Ctrl+A)
3. Select desired models
4. Enter object classes (e.g., "person, car, dog")
5. Click "Run Auto-Annotation"

For more information, see:
- [MODEL_UI.md](MODEL_UI.md) - Model UI usage guide
- [Florence-2 Documentation](https://huggingface.co/microsoft/Florence-2-large)
- [SAM2 Documentation](https://ai.meta.com/sam2/)
