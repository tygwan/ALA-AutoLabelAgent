# Technical Troubleshooting Log

This document records notable technical issues encountered during development and their resolutions. It focuses on model inference stability, memory hygiene, preprocessing compatibility across backbones, and evaluation reproducibility.

## Contents
- Florence-2 (VLM) repeated inference memory accumulation
- CLIP/STL-10/CIFAR-10 embedding type and preprocessing incompatibilities
- DINOv2 inference stability and batching
- GPU/CPU memory hygiene playbook
- Few-shot pipeline data/transform invariants
- Verification checklist

---

## Florence-2 repeated inference memory accumulation

- Context:
  - Using Hugging Face `AutoImageProcessor('facebook/dinov2-base')` and Florence-2 VLM in loops to produce features/captions over large image sets.
  - Observed GPU memory growth across iterations and eventual OOM.
- Symptoms:
  - GPU memory steadily increases with each iteration; not reclaimed until process exit.
  - Even with small batch sizes, long runs fail after N images.
- Root causes (combined):
  - Tensors kept on GPU and retained by Python references (e.g., appending model outputs to lists) preventing deallocation.
  - Missing `torch.no_grad()` and/or `.detach()` which retains computational graph.
  - Moving outputs to CPU late, causing many GPU-resident tensors to accumulate.
  - Large list comprehensions that hold onto intermediate results for the whole epoch.
- Resolutions:
  - Switch to a plain `for` loop that processes a small batch, immediately extracts CPU copies, and releases GPU tensors.
  - Enforce inference mode: `model.eval()` + `with torch.no_grad():`
  - Convert to CPU arrays early: `output = output.detach().cpu().numpy()`.
  - Explicitly drop references and flush allocator between iterations when needed:
    ```python
    del output, inputs
    import torch, gc
    torch.cuda.empty_cache()
    gc.collect()
    ```
  - Prefer chunked iteration and avoid storing full-run outputs in memory; write incremental results to disk when feasible.

Example pattern (before → after):

```python
# BEFORE (problematic, accumulates GPU tensors)
outputs = []
for img in images:
    inputs = processor(images=img, return_tensors="pt").to(device)
    out = model(**inputs)
    outputs.append(out.pooler_output)  # stays on GPU, retains graph

# AFTER (streamed, CPU offload, no graph)
for img in images:
    with torch.no_grad():
        inputs = processor(images=img, return_tensors="pt").to(device)
        out = model(**inputs)
        vec = out.pooler_output.detach().cpu().numpy()
    save_vector(vec)  # write incrementally or queue
    del out, inputs
    torch.cuda.empty_cache()
```

---

## CLIP / STL-10 / CIFAR-10 embedding type & preprocessing incompatibilities

- Context:
  - Cross-backbone evaluation (CLIP ViT-B/32, ResNet-50, DINOv2) on STL-10/CIFAR-10 and project images.
  - Inconsistent preprocessing and dtypes led to poor accuracy or runtime errors.
- Symptoms:
  - Mismatched tensor shapes (e.g., channel order, crop size).
  - Dtype/device errors (float64 vs float32; CPU vs CUDA) and unexpected accuracy drops.
- Root causes:
  - Using OpenCV BGR instead of RGB without conversion; mixing PIL and cv2 flows improperly.
  - Not using backbone-specific preprocessors (e.g., CLIP’s own `preprocess`).
  - For ResNet-50, missing Imagenet mean/std normalization and 224×224 crops; for CLIP, ignoring its transform pipeline.
  - Feeding float64 numpy to torch instead of float32.
- Resolutions:
  - CLIP: always use `clip.load(...)[1]` preprocess; keep PIL RGB inputs.
  - ResNet-50: use torchvision transforms with Imagenet normalization and 224 center crop.
  - DINOv2: use `AutoImageProcessor` to produce normalized tensors.
  - Normalize dtype/device early: `torch.from_numpy(x).float().to(device)`; ensure `.contiguous()` if needed.
  - Convert cv2 images to RGB: `img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` before PIL conversion.

Backbone-specific transforms (reference):

```python
# ResNet-50 (torchvision)
from torchvision import transforms
resnet_pre = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# CLIP (ViT-B/32)
import clip
model, clip_pre = clip.load("ViT-B/32", device)
# Use clip_pre(image) directly on PIL.Image (RGB)

# DINOv2
from transformers import AutoImageProcessor
processor = AutoImageProcessor.from_pretrained("facebook/dinov2-base")
inputs = processor(images=pil_image, return_tensors="pt")
```

---

## DINOv2 inference stability and batching

- Ensure `model.eval()` and `torch.no_grad()` during inference.
- Prefer small batches; verify batch fits in GPU (feature extractor only, no gradients).
- Immediately move outputs to CPU (`.detach().cpu().numpy()`) and clear GPU references; call `torch.cuda.empty_cache()` in long loops.
- Avoid storing entire-run outputs; stream to disk or aggregate partial stats.

---

## GPU/CPU memory hygiene playbook

- Inference:
  - `model.eval()` and wrap forward in `with torch.no_grad():`
  - `.detach().cpu()` outputs ASAP; `del` intermediate tensors.
  - For extensive runs: `torch.cuda.empty_cache()`, periodic `gc.collect()`.
- Batching:
  - Right-size `batch_size`; chunk inputs; avoid giant lists of GPU tensors.
  - Prefer dataloaders with workers pinned only if beneficial and measured.
- Data movement:
  - Keep only the working set on GPU; avoid accidental `.to(device)` of large Python containers.
  - For numpy→torch: enforce `.astype(np.float32)` or `.float()` and device placement.

---

## Few-shot pipeline data/transform invariants

- Directory schema is part of the contract:
  - Support set: `data/<category>/2.support-set/(shotX | Class_X/shotX)`
  - Query images: `data/<category>/6.preprocessed/**`
- Backbone-specific preprocessors must be respected (CLIP vs ResNet vs DINOv2).
- Similarity is cosine over flattened embeddings; maintain the same embedding dimension and normalization per backbone.
- Thresholding policy:
  - Best score < threshold → `Unknown` (reject to reduce false positives).
  - Margin (top-1 − top-2) used as confidence heuristic.

---

## Verification checklist

- Memory
  - [ ] GPU memory stable across ≥ 1,000 images (no monotonic growth).
  - [ ] No OOM at configured batch size; outputs CPU-offloaded per step.
- Preprocessing
  - [ ] CLIP uses `clip_pre` (PIL RGB) pipeline.
  - [ ] ResNet-50 uses Imagenet mean/std and 224 center crop.
  - [ ] DINOv2 uses `AutoImageProcessor` outputs directly.
- Dtypes/devices
  - [ ] All tensors are float32 unless model requires otherwise.
  - [ ] Device consistency (CPU/CUDA) verified per module.
- Reproducibility
  - [ ] Table 7/8 totals consistent across runs given fixed inputs.

---

## Notes on Florence-2 pipeline ordering

- When composing VLM + detection/segmentation steps, prefer a strict sequence:
  1) Create minimal GPU resident state; 2) run forward; 3) extract CPU copy; 4) release GPU references; 5) proceed.
- Avoid accumulating lists of GPU tensors across the entire dataset in a single scope; write incremental outputs.
- If batching is necessary, small batches with immediate offload provide more predictable memory profiles.

