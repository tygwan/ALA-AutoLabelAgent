Model files directory

This folder is excluded from Git. Model weights (e.g., *.pt, *.pth, *.onnx) are downloaded or generated at runtime.

Common models
- YOLO v8: downloaded by ultralytics on first use
- Florence-2, SAM2: installed per README instructions

Do not commit large binaries to the repository.

# Models Directory

This directory contains the model files used by the project. The structure is as follows:

```
models/
├── sam2/                  # Segment Anything Model 2 files
│   ├── sam2_vit_h.pt      # SAM2 ViT-H model weights
│   └── ...                # Other SAM2 related files
└── yolo/                  # YOLO model files
    ├── yolov8n.pt         # YOLOv8 nano model weights
    ├── yolov8n-seg.pt     # YOLOv8 nano segmentation model weights
    ├── yolov8x-seg.pt     # YOLOv8 extra large segmentation model weights
    └── ...                # Other YOLO related files
```

## Model Download

The model files are not included in the repository due to their large size. They will be automatically downloaded when you first run the scripts. Alternatively, you can manually download them:

### SAM2 Models

- Download from: [https://github.com/facebookresearch/segment-anything-2](https://github.com/facebookresearch/segment-anything-2)
- Place in the `models/sam2/` directory

### YOLO Models

- Download from: [https://github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics)
- Place in the `models/yolo/` or project root directory

## Important Notes

- The model files are quite large (several hundred MB each)
- These models require significant computational resources
- GPU acceleration is recommended for optimal performance
