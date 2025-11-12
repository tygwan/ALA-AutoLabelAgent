# ALA-AutoLabelAgent

**Automatic Labeling Agent with GUI Interface**

PyQt6 기반의 자동 이미지 라벨링 도구입니다. Florence-2, GroundedSAM2, YOLOv8 등의 비전 모델을 통합하여 효율적인 어노테이션 워크플로우를 제공합니다.

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Windows / macOS / Linux
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/tygwan/ALA-AutoLabelAgent.git
cd ALA-AutoLabelAgent/ALA-GUI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

### Run Application

```bash
cd ALA-GUI
python src/main.py
```

## 📁 Project Structure

```
ALA-AutoLabelAgent/
├── ALA-GUI/                # Main GUI application
│   ├── src/               # Source code (MVC architecture)
│   │   ├── models/        # Data models
│   │   ├── views/         # PyQt6 UI components
│   │   ├── controllers/   # Business logic
│   │   └── utils/         # Utility functions
│   ├── tests/             # Test suite
│   │   ├── unit/          # Unit tests
│   │   ├── integration/   # Integration tests
│   │   └── e2e/           # End-to-end tests
│   ├── docs/              # Documentation
│   └── requirements.txt   # Python dependencies
├── PLAN.md                # 15-week development roadmap
├── TECHSPEC.md            # Technical specifications
├── TODO.md                # 412 detailed tasks
└── LICENSE                # MIT License
```

## 🎯 Development Roadmap

**Current Status**: M0 Complete (Project Setup) ✅

### Milestones

- **M0**: Project Setup ✅ (완료)
- **M1**: Foundation & Core Infrastructure (진행 예정)
- **M2**: PyQt6 Image Display & Navigation
- **M3**: Model Integration (Florence-2, SAM2, YOLO)
- **M4**: Annotation Tools
- **M5**: Web Integration (Gradio)
- **M6**: Pipeline Integration
- **M7**: Polish & UX Improvements
- **M8**: Deployment & Documentation

자세한 계획은 [PLAN.md](PLAN.md) 참고

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

- **[SETUP.md](ALA-GUI/docs/SETUP.md)**: 설치 가이드
- **[TESTING.md](ALA-GUI/docs/TESTING.md)**: 테스트 가이드
- **[STYLEGUIDE.md](ALA-GUI/docs/STYLEGUIDE.md)**: 코드 스타일 가이드
- **[CONTRIBUTING.md](ALA-GUI/CONTRIBUTING.md)**: 기여 가이드
- **[KNOWN_ISSUES.md](ALA-GUI/KNOWN_ISSUES.md)**: 알려진 이슈

## 🏗️ Technology Stack

**Core Framework**:
- PyQt6 6.6.1 - Desktop GUI framework
- Python 3.9+ - Programming language

**Testing**:
- pytest + pytest-qt - Testing framework
- pytest-cov - Coverage reporting

**Code Quality**:
- Black - Code formatter
- flake8 - Linter
- mypy - Type checker
- pylint - Additional linting
- isort - Import sorter
- bandit - Security scanner

**Computer Vision** (M3+):
- Florence-2 - Vision-language model
- GroundedSAM2 - Segmentation
- YOLOv8 - Object detection
- OpenCV - Image processing

**ML/DL** (M3+):
- PyTorch - Deep learning framework
- transformers - Model hub

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

**M0: Project Setup** ✅ 완료 (2025-01-13)
- 프로젝트 구조 생성
- 테스팅 프레임워크 설정
- CI/CD 파이프라인 구성
- 코드 품질 도구 설정
- 문서화 완료

**다음 단계**: M1 Foundation & Core Infrastructure

---

**Last Updated**: 2025-01-13
**Version**: 0.1.0 (M0 Complete)
