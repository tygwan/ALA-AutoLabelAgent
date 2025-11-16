# ALA-AutoLabelAgent

**AI-Powered Image Annotation Tool with PyQt6 GUI**

PyQt6 기반의 자동 이미지 라벨링 데스크톱 애플리케이션입니다. Florence-2 VLM과 SAM2 세그멘테이션을 통합하여 텍스트 프롬프트 기반의 AI 자동 어노테이션을 제공합니다.

**Current Status**: 🚀 **Alpha v0.3.0** - Core Features Functional
**Capabilities**: ✅ Interactive Image Viewer ✅ AI Auto-Annotation (Florence-2 + SAM2) ✅ Manual Model Management

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (Recommended - full SAM2 segmentation support)
- **Python 3.9+** (Basic - Florence-2 bounding boxes only)
- Windows / macOS / Linux
- CUDA GPU (recommended for faster inference)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/tygwan/ALA-AutoLabelAgent.git
cd ALA-AutoLabelAgent/ALA-GUI

# 2. Create virtual environment (Python 3.10 recommended)
py -3.10 -m venv venv  # Windows
# python3.10 -m venv venv  # Linux/macOS

# 3. Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# 4. Install dependencies
pip install -r requirements.txt
pip install timm einops  # Florence-2 dependencies
```

### Run Application

```bash
cd ALA-GUI
python src\main.py  # Windows
# python src/main.py  # Linux/macOS
```

### First-time Usage

1. **Import Images**: File → Import Images (Ctrl+O)
2. **Run Auto-Annotation**: Tools → Auto-Annotate (Ctrl+A)
3. **Select Models**:
   - VLM: Florence-2-large-no-flash (HF)
   - Seg: SAM2 Base+ (Auto-download) or None
4. **Enter Classes**: e.g., "person, car, dog"
5. **Run**: Models download automatically on first use (~1.5GB Florence-2, ~300MB SAM2)

**📖 Detailed Guide**: See [ALA-GUI/README.md](ALA-GUI/README.md) for comprehensive documentation

## ✨ Key Features

### 🖼️ Interactive Image Viewer
- PyQt6-based canvas with zoom/pan/navigation
- File list management with Previous/Next (Ctrl+Left/Right)
- Keyboard shortcuts (Ctrl+O, Ctrl+A, Arrow keys)
- Real-time image display with smooth interactions

### 🤖 AI-Powered Auto-Annotation
- **Florence-2 VLM**: Text-prompt-based object detection
- **SAM2**: Refined mask segmentation
- **Two-dropdown model selection**: VLM + Segmentation
- **Manual model management**: `~/.cache/ala-gui/models/`
- **Auto-download**: Models download on first use

### 🔧 Universal Compatibility
- **Flash attention compatibility**: Works on all GPUs, CPU, Apple Silicon (MPS)
- **Python 3.10+**: Full SAM2 segmentation support
- **Python 3.9+**: Fallback with Florence-2 bounding boxes
- **Cross-platform**: Windows, macOS, Linux

### 📚 Comprehensive Documentation
- Model setup guide with troubleshooting
- Python upgrade guide (3.9 → 3.10)
- Component architecture documentation
- Testing and development guides

## 📁 Project Structure

```
ALA-AutoLabelAgent/
├── ALA-GUI/                # Main GUI application (v0.3.0-alpha)
│   ├── src/               # Source code (MVC architecture)
│   │   ├── models/        # AI models (Florence-2, SAM2, ModelManager)
│   │   ├── views/         # PyQt6 UI (MainWindow, Canvas, Dialogs)
│   │   ├── controllers/   # Business logic (ShortcutManager)
│   │   └── utils/         # Utilities (AnnotationExporter)
│   ├── tests/             # Test suite (50+ unit, 20+ integration)
│   │   ├── unit/          # Component tests
│   │   ├── integration/   # Workflow tests
│   │   └── e2e/           # End-to-end tests
│   ├── docs/              # Documentation (7 comprehensive guides)
│   └── requirements.txt   # Python dependencies
├── model_references/      # Reference implementations (autodistill)
└── LICENSE                # MIT License
```

## 🎯 Development Roadmap

**Current Status**: M4 In Progress (Annotation Tools) 🚧
**Version**: v0.3.0-alpha
**Last Updated**: 2025-01-17

### Completed Milestones

- ✅ **M0**: Project Setup & Infrastructure
- ✅ **M1**: Foundation & Core Infrastructure
- ✅ **M2**: PyQt6 Image Display & Navigation
  - MainWindow with menu/toolbar/shortcuts
  - FileListWidget for image management
  - ImageCanvas with zoom/pan
- ✅ **M3**: AI Model Integration
  - Florence-2 VLM for object detection
  - SAM2 for mask segmentation
  - ModelManager for model discovery
  - Flash attention compatibility (all GPUs)
  - Python 3.10 support with 3.9 fallback

### In Progress

- 🚧 **M4**: Annotation Tools & Manual Editing (Current)

### Upcoming

- **M5**: Web Integration - Few-Shot Learning (Gradio)
- **M6**: Pipeline Integration - Ground Truth & YOLO Training
- **M7**: Polish & User Experience
- **M8**: Deployment & Distribution

**📖 Detailed Roadmap**: See [ALA-GUI/README.md](ALA-GUI/README.md#development-status)

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test category
pytest -m unit
pytest -m integration
pytest -m e2e
```

## 🔧 Development

**TDD Workflow**: RED → GREEN → REFACTOR → COMMIT

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint
flake8 src/ tests/

# Type check
mypy src/

# Security scan
bandit -r src/
```

자세한 개발 가이드는 [ALA-GUI/CONTRIBUTING.md](ALA-GUI/CONTRIBUTING.md) 참고

## 📚 Documentation

### 🌟 Main Documentation
- **[ALA-GUI/README.md](ALA-GUI/README.md)**: Complete user and developer guide

### 🛠️ Setup & Installation
- **[PYTHON_UPGRADE.md](ALA-GUI/docs/PYTHON_UPGRADE.md)**: Python 3.10 upgrade guide
- **[MODEL_SETUP.md](ALA-GUI/docs/MODEL_SETUP.md)**: AI model setup and troubleshooting

### 📖 Component Guides
- **[MAINWINDOW.md](ALA-GUI/docs/MAINWINDOW.md)**: Main window architecture
- **[IMAGECANVAS.md](ALA-GUI/docs/IMAGECANVAS.md)**: Image canvas implementation
- **[MODEL_UI.md](ALA-GUI/docs/MODEL_UI.md)**: Auto-annotate dialog guide

### 🧪 Development
- **[BRANCHING_STRATEGY.md](ALA-GUI/docs/BRANCHING_STRATEGY.md)**: Git workflow
- **[tests/](ALA-GUI/tests/)**: Unit and integration tests

## 🏗️ Technology Stack

| Category | Technology | Version | Status |
|----------|------------|---------|--------|
| **GUI Framework** | PyQt6 | 6.6.1 | ✅ |
| **Language** | Python | 3.10+ | ✅ |
| **AI Models** | Florence-2 | microsoft/Florence-2-large | ✅ |
| | SAM2 | Base+ | ✅ |
| | YOLOv8 | - | 📋 Planned |
| **Deep Learning** | PyTorch | 2.1.2 | ✅ |
| | Transformers | 4.36.2 | ✅ |
| | timm | 1.0.22+ | ✅ |
| | einops | 0.8.1+ | ✅ |
| **Image Processing** | OpenCV | 4.9+ | ✅ |
| | Pillow | 10.2+ | ✅ |
| **Testing** | pytest + pytest-qt | - | ✅ |
| | pytest-cov | - | ✅ |
| **Code Quality** | Black, flake8, mypy | - | ✅ |
| | isort, bandit, pylint | - | ✅ |

**Key Features**:
- 🔧 Flash attention compatibility (all GPU architectures, CPU, MPS)
- 🔧 Python 3.9+ fallback support (Florence-2 only)
- 🔧 Manual model management with ModelManager
- 🔧 Lazy model loading for faster startup

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](ALA-GUI/CONTRIBUTING.md) for details.

### Development Process

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests (TDD approach)
4. Commit changes (`git commit -m 'feat: add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Known Issues

- **PyQt6 on Windows**: DLL loading issue 문서화됨 ([KNOWN_ISSUES.md](ALA-GUI/KNOWN_ISSUES.md))
- 해결 방법 및 workaround 제공

## 📊 Project Status

### Current Release: v0.3.0-alpha (2025-01-17)

**Completed**:
- ✅ **M0-M3**: Project Setup → AI Model Integration
- ✅ Interactive image viewer with zoom/pan
- ✅ Florence-2 + SAM2 auto-annotation
- ✅ Manual model management system
- ✅ Python 3.10 upgrade support
- ✅ Flash attention compatibility
- ✅ Comprehensive documentation

**In Progress**:
- 🚧 **M4**: Annotation Tools & Manual Editing

**Coming Next**:
- 📋 Drawing tools (polygon, box, pencil)
- 📋 Class management widget
- 📋 Few-shot learning integration (Gradio)

### Statistics
- **88 files changed** in M2-M3
- **14,783+ lines added**
- **50+ unit tests**
- **20+ integration tests**
- **7 comprehensive documentation files**

---

**Last Updated**: 2025-01-17
**Version**: 0.3.0-alpha (M2-M3 Complete)
**Next Milestone**: M4 - Annotation Tools (Q1 2025)
