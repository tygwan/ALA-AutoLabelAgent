# ALA-GUI - Auto Label Agent Desktop Application

Modern PyQt6 desktop application for automated image annotation with AI-powered models and Few-Shot Learning.

## Overview

ALA-GUI transforms the ALA (Auto Label Agent) pipeline into a user-friendly desktop application similar to X-AnyLabeling. It combines powerful computer vision models (SAM2, Florence-2, YOLO) with an intuitive graphical interface for efficient image annotation workflows.

## Features

### ✅ Implemented (v0.3.0-alpha)

- 🖼️ **Interactive Image Viewer**: PyQt6-based canvas with zoom, pan, and navigation
  - File list management with Previous/Next navigation
  - Image display with zoom controls
  - Keyboard shortcuts (Ctrl+O, Ctrl+A, Arrow keys)
- 🤖 **Auto-Annotation**: Florence-2 + SAM2 integration for AI-powered segmentation
  - Text-prompt-based object detection with Florence-2 VLM
  - Refined mask generation with SAM2 segmentation
  - Manual model selection (VLM + Segmentation dropdowns)
  - Model directory management (~/.cache/ala-gui/models/)
- 🔧 **Model Compatibility**: Universal GPU support and Python version flexibility
  - Flash attention compatibility (all GPUs, CPU, Apple Silicon MPS)
  - Python 3.10+ for full SAM2 support
  - Python 3.9+ fallback with Florence-2 only
- 📚 **Comprehensive Documentation**: Setup and troubleshooting guides
  - Model setup guide (MODEL_SETUP.md)
  - Python upgrade guide (PYTHON_UPGRADE.md)
  - Component documentation (MAINWINDOW.md, IMAGECANVAS.md, MODEL_UI.md)

### 🚧 In Progress (v0.4.0)

- ✏️ **Manual Editing**: Drawing tools (polygon, box, pencil, eraser) with undo/redo
- 🎨 **Class Management**: Class list widget and label management

### 📋 Planned (v0.5.0+)

- 🎯 **Few-Shot Learning**: Embedded Gradio interface for classification with ResNet/CLIP/DINOv2
- ✅ **Ground Truth Workflow**: Accept/reject annotations and build high-quality datasets
- 🏋️ **YOLO Training**: Integrated YOLOv8 training from annotated data
- 🎨 **Themes**: Light/Dark theme support
- 🌐 **Internationalization**: Multi-language support (EN/KO)

### 🔮 Future (v2.0+)

- 🎬 Video annotation support
- 🔌 Plugin system for custom models
- ☁️ Cloud synchronization
- 📊 Advanced analytics and reporting

## Architecture

```
ALA-GUI/
├── src/
│   ├── models/          # Data models (Project, Image, Annotation)
│   ├── views/           # PyQt6 UI components (MainWindow, Canvas, Dialogs)
│   ├── controllers/     # Business logic (ModelController, ProjectManager)
│   └── utils/           # Utilities (file I/O, logging, config)
├── tests/
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── e2e/             # End-to-end tests
├── docs/                # Documentation
└── examples/            # Example scripts and projects
```

**Design Pattern**: MVC (Model-View-Controller)
**GUI Framework**: PyQt6 6.6+
**Testing**: pytest + pytest-qt
**Development**: TDD (Test-Driven Development)

## Installation

### Prerequisites

- **Python 3.10+** (Recommended - full SAM2 segmentation support)
- **Python 3.9+** (Basic - Florence-2 bounding boxes only)
- Windows 10/11 (Linux/macOS support planned)
- CUDA-capable GPU (recommended for model inference)

**Note**: SAM2 segmentation requires Python 3.10+. If using Python 3.9, only Florence-2 bounding box detection is available. See [Python Upgrade Guide](docs/PYTHON_UPGRADE.md) to upgrade from 3.9 to 3.10.

### Setup

```bash
# Clone the repository
cd ALA-AutoLabelAgent/ALA-GUI

# Create virtual environment (Python 3.10 recommended)
py -3.10 -m venv venv  # Windows with Python 3.10
# OR
python -m venv venv    # Use default Python

# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install Florence-2 dependencies
pip install timm einops

# Run the application
python src/main.py
```

**For Python 3.9 → 3.10 upgrade**, see [docs/PYTHON_UPGRADE.md](docs/PYTHON_UPGRADE.md)

## Quick Start

### 1. Launch Application

```bash
cd ALA-GUI
python src\main.py  # Windows
# python src/main.py  # Linux/macOS
```

### 2. Import Images

- **File → Import Images** (Ctrl+O)
- Select one or more image files
- Images appear in the left file list

### 3. Run Auto-Annotation

**First-time setup**: Install model dependencies
```bash
pip install timm einops
```

**Steps**:
1. Click **Tools → Auto-Annotate** (Ctrl+A)
2. Select models:
   - **VLM Model**: Florence-2-large-no-flash (HF) - for object detection
   - **Seg Model**: SAM2 Base+ (Auto-download) OR None (VLM only)
3. Enter object classes (e.g., "person, car, dog")
4. Click **Run Auto-Annotation**

**Model Download**: On first run, models download automatically (~1.5GB for Florence-2, ~300MB for SAM2)

**Note**: SAM2 requires Python 3.10+. See [docs/PYTHON_UPGRADE.md](docs/PYTHON_UPGRADE.md) if using Python 3.9.

### 4. Navigate Images

- **Previous Image**: Ctrl+Left or ← key
- **Next Image**: Ctrl+Right or → key
- **Zoom In/Out**: Mouse wheel or Ctrl++/Ctrl+-

### 5. Next Steps

- **Model Setup**: See [docs/MODEL_SETUP.md](docs/MODEL_SETUP.md) for manual model installation
- **Troubleshooting**: Check MODEL_SETUP.md for common issues
- **Documentation**: Explore [docs/](docs/) folder for component guides

## Development Status

**Current Phase**: M4 - Annotation Tools & Manual Editing
**Last Updated**: 2025-01-17
**Version**: 0.3.0-alpha

### Milestone Progress

- [x] **M0: Project Setup** (1 week) - ✅ Completed
- [x] **M1: Foundation & Core Infrastructure** (1.5 weeks) - ✅ Completed
- [x] **M2: PyQt6 Image Display & Navigation** (2 weeks) - ✅ Completed
  - MainWindow with menu bar, toolbar, and status bar
  - FileListWidget for image management
  - ImageCanvas for image display with zoom/pan
  - Keyboard shortcuts (Ctrl+O, Ctrl+A, Arrow keys, etc.)
- [x] **M3: Model Integration - SAM2 & Florence-2** (2.5 weeks) - ✅ Completed
  - Florence-2 VLM integration for object detection
  - SAM2 segmentation integration for mask refinement
  - ModelManager for model discovery and selection
  - Auto-annotate dialog with VLM + Seg model selection
  - Flash attention compatibility for all GPU architectures
  - Python 3.10 support with 3.9 fallback
- [ ] **M4: Annotation Tools & Manual Editing** (2 weeks) - 🚧 In Progress
- [ ] M5: Web Integration - Few-Shot Learning (2 weeks)
- [ ] M6: Pipeline Integration - Ground Truth & YOLO (2 weeks)
- [ ] M7: Polish & User Experience (1.5 weeks)
- [ ] M8: Deployment & Distribution (1 week)

**Total**: 15 weeks MVP + 5 weeks buffer = 20 weeks

### Recent Major Updates

- ✅ Manual model management system with two-dropdown selection
- ✅ Python 3.10 upgrade support with comprehensive guide
- ✅ Flash attention compatibility (works on all GPUs, CPU, MPS)
- ✅ SAM2 optional fallback for Python 3.9 users
- ✅ Complete GUI implementation with image viewer and navigation

See [docs/](docs/) folder for detailed component documentation.

## Technology Stack

| Category | Technology |
|----------|------------|
| GUI Framework | PyQt6 6.6+ |
| Web Integration | Gradio 4.14+, QWebEngineView |
| Image Processing | OpenCV 4.9+, Pillow 10.2+ |
| Deep Learning | PyTorch 2.1+, Transformers 4.36+ |
| Object Detection | Ultralytics YOLOv8 |
| Segmentation | SAM2, Florence-2 |
| Few-Shot Learning | ResNet, CLIP, DINOv2 |
| Testing | pytest, pytest-qt, pytest-cov |
| Code Quality | black, flake8, mypy, pylint |

## Development Workflow

### TDD Approach

All features follow Test-Driven Development:

1. **RED**: Write failing test
2. **GREEN**: Implement minimal code to pass
3. **REFACTOR**: Improve code structure
4. **COMMIT**: Git commit with conventional message

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_project_manager.py

# Run with pytest-qt
pytest tests/integration/test_main_window.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type check
mypy src/

# Security scan
bandit -r src/
```

## Contributing

**Solo Developer Project** (currently)

Future contributions welcome after v1.0 release. Guidelines will be added in CONTRIBUTING.md.

## Documentation

### Setup & Installation
- [PYTHON_UPGRADE.md](docs/PYTHON_UPGRADE.md) - Python 3.10 upgrade guide
- [MODEL_SETUP.md](docs/MODEL_SETUP.md) - AI model setup and troubleshooting

### Component Guides
- [MAINWINDOW.md](docs/MAINWINDOW.md) - Main window architecture and UI components
- [IMAGECANVAS.md](docs/IMAGECANVAS.md) - Image canvas implementation details
- [MODEL_UI.md](docs/MODEL_UI.md) - Auto-annotate dialog and model integration
- [BRANCHING_STRATEGY.md](docs/BRANCHING_STRATEGY.md) - Git workflow and branching

### Testing
- [tests/unit/](tests/unit/) - Unit tests for components and models
- [tests/integration/](tests/integration/) - Integration tests for workflows

## Comparison with X-AnyLabeling

| Feature | X-AnyLabeling | ALA-GUI |
|---------|---------------|---------|
| GUI Framework | PyQt5 | PyQt6 |
| Auto-Annotation | 40+ models | SAM2 + Florence-2 (focused) |
| Few-Shot Learning | ❌ | ✅ Integrated Gradio |
| YOLO Training | ❌ | ✅ Built-in |
| Ground Truth Tool | Basic | Advanced workflow |
| Languages | EN/CN | EN/KO |

## License

See [LICENSE](../LICENSE) file.

## References

- [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) - Reference GUI architecture
- [labelme](https://github.com/wkentaro/labelme) - Polygon annotation inspiration
- [ALA Pipeline](../ALA/) - Original CLI-based pipeline

## Contact

Project Repository: https://github.com/tygwan/ALA-AutoLabelAgent

---

**Status**: 🚧 Alpha Release (v0.3.0) - Core Features Functional | **Target v1.0**: Q2 2025

**Current Capabilities**: ✅ Image Viewer ✅ AI Auto-Annotation ✅ Model Management
