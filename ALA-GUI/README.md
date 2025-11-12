# ALA-GUI - Auto Label Agent Desktop Application

Modern PyQt6 desktop application for automated image annotation with AI-powered models and Few-Shot Learning.

## Overview

ALA-GUI transforms the ALA (Auto Label Agent) pipeline into a user-friendly desktop application similar to X-AnyLabeling. It combines powerful computer vision models (SAM2, Florence-2, YOLO) with an intuitive graphical interface for efficient image annotation workflows.

## Features

### Current (v1.0 MVP - In Development)

- 🖼️ **Interactive Image Viewer**: PyQt6-based canvas with zoom, pan, and navigation
- 🤖 **Auto-Annotation**: SAM2 + Florence-2 integration for text-prompt-based segmentation
- ✏️ **Manual Editing**: Drawing tools (polygon, box, pencil, eraser) with undo/redo
- 🎯 **Few-Shot Learning**: Embedded Gradio interface for classification with ResNet/CLIP/DINOv2
- ✅ **Ground Truth Workflow**: Accept/reject annotations and build high-quality datasets
- 🏋️ **YOLO Training**: Integrated YOLOv8 training from annotated data
- 🎨 **Professional UI**: Light/Dark themes, keyboard shortcuts, internationalization (EN/KO)

### Planned (v2.0+)

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

- Python 3.9+
- Windows 10/11 (Linux/macOS support planned)
- CUDA-capable GPU (recommended for model inference)

### Setup

```bash
# Clone the repository
cd ALA-AutoLabelAgent/ALA-GUI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application (coming soon)
python src/main.py
```

## Development Status

**Current Phase**: M0 - Project Setup (Week 1/15)
**Last Updated**: 2025-01-13
**Version**: 0.1.0-dev

### Milestone Progress

- [x] M0: Project Setup (1 week) - **In Progress**
- [ ] M1: Foundation & Core Infrastructure (1.5 weeks)
- [ ] M2: PyQt6 Image Display & Navigation (2 weeks)
- [ ] M3: Model Integration - SAM2 & Florence-2 (2.5 weeks)
- [ ] M4: Annotation Tools & Manual Editing (2 weeks)
- [ ] M5: Web Integration - Few-Shot Learning (2 weeks)
- [ ] M6: Pipeline Integration - Ground Truth & YOLO (2 weeks)
- [ ] M7: Polish & User Experience (1.5 weeks)
- [ ] M8: Deployment & Distribution (1 week)

**Total**: 15 weeks MVP + 5 weeks buffer = 20 weeks

See [PLAN.md](../PLAN.md) for detailed roadmap.
See [TODO.md](../TODO.md) for task breakdown (412 tasks, 580h).
See [TECHSPEC.md](../TECHSPEC.md) for technical specifications.

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

- [PLAN.md](../PLAN.md) - Strategic implementation plan
- [TECHSPEC.md](../TECHSPEC.md) - Technical specifications
- [TODO.md](../TODO.md) - Detailed task list
- [NEXT_STEPS.md](../NEXT_STEPS.md) - Quick start guide
- docs/ - Component documentation (coming soon)

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

**Status**: 🚧 Under Active Development | **Target Release**: Q2 2025
