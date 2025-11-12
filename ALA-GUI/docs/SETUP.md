# ALA-GUI Development Environment Setup

Complete guide for setting up the ALA-GUI development environment.

## Prerequisites

### Required Software

- **Python 3.9+** (3.9, 3.10, or 3.11 recommended)
  - Download: https://www.python.org/downloads/
  - Verify: `python --version`

- **Git** (for version control)
  - Download: https://git-scm.com/downloads
  - Verify: `git --version`

- **CUDA Toolkit** (optional but recommended for GPU acceleration)
  - Download: https://developer.nvidia.com/cuda-downloads
  - Recommended: CUDA 11.8 or 12.1
  - Verify: `nvcc --version`

### Recommended Tools

- **Visual Studio Code** or **PyCharm** (IDE)
- **Windows Terminal** (for better command-line experience)
- **Qt Designer** (for UI design, included with PyQt6-tools)

## Installation Steps

### 1. Clone Repository

```bash
cd C:\Users\YourName\Desktop\AI_PJT
git clone https://github.com/tygwan/ALA-AutoLabelAgent.git
cd ALA-AutoLabelAgent/ALA-GUI
```

### 2. Create Virtual Environment

**Windows (CMD/PowerShell)**:
```bash
python -m venv venv
venv\Scripts\activate
```

**Windows (Git Bash)**:
```bash
python -m venv venv
source venv/Scripts/activate
```

**Linux/macOS**:
```bash
python3 -m venv venv
source venv/bin/activate
```

**Verify activation**: Your prompt should show `(venv)` prefix

### 3. Upgrade pip

```bash
python -m pip install --upgrade pip setuptools wheel
```

### 4. Install Dependencies

**Option A: Install all dependencies** (recommended for development):
```bash
pip install -r requirements.txt
```

**Option B: Install in stages** (for troubleshooting):
```bash
# 1. Core GUI dependencies
pip install PyQt6 PyQt6-WebEngine

# 2. Testing framework
pip install pytest pytest-qt pytest-cov pytest-mock

# 3. Image processing
pip install opencv-python Pillow numpy

# 4. Machine learning (large downloads)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# 5. Additional dependencies
pip install gradio fastapi uvicorn transformers ultralytics
```

### 5. Verify Installation

**Check PyQt6**:
```bash
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 installed successfully')"
```

**Check pytest-qt**:
```bash
pytest --version
pytest --markers | grep gui
```

**Run sample test**:
```bash
pytest tests/unit/test_main_window.py -v
```

**Run main application** (simple window):
```bash
python src/main.py
```

## IDE Configuration

### Visual Studio Code

#### 1. Install Extensions

- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Python Test Explorer (littlefoxteam.vscode-python-test-adapter)
- Black Formatter (ms-python.black-formatter)
- Pylint (ms-python.pylint)

#### 2. Workspace Settings

Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.analysis.typeCheckingMode": "basic"
}
```

#### 3. Launch Configuration

Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: ALA-GUI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/main.py",
            "console": "integratedTerminal",
            "justMyCode": true
        },
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "Python: Pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "-v"
            ],
            "console": "integratedTerminal"
        }
    ]
}
```

### PyCharm

#### 1. Configure Interpreter

1. File → Settings → Project → Python Interpreter
2. Add Interpreter → Existing Environment
3. Select: `ALA-GUI/venv/Scripts/python.exe`

#### 2. Configure Testing

1. File → Settings → Tools → Python Integrated Tools
2. Default test runner: pytest
3. Apply and OK

#### 3. Code Quality

1. File → Settings → Editor → Code Style → Python
2. Set line length: 88 (Black default)
3. Enable "Reformat code" on save

## Development Tools Setup

### 1. Pre-commit Hooks

Install pre-commit (optional but recommended):
```bash
pip install pre-commit
pre-commit install
```

Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
        language_version: python3.9

  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

### 2. Code Formatting

**Format entire project**:
```bash
black src/ tests/
```

**Check formatting without changes**:
```bash
black --check src/ tests/
```

### 3. Linting

**Run flake8**:
```bash
flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203
```

### 4. Type Checking

**Run mypy**:
```bash
mypy src/
```

### 5. Security Scanning

**Run bandit**:
```bash
bandit -r src/
```

## Testing Workflow

### Run Tests

**All tests**:
```bash
pytest
```

**Specific test file**:
```bash
pytest tests/unit/test_main_window.py
```

**With coverage**:
```bash
pytest --cov=src --cov-report=html
```

**View coverage report**:
```bash
# Windows
start htmlcov/index.html

# Linux/macOS
open htmlcov/index.html
```

**Markers**:
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip GUI tests (useful for CI)
pytest -m "not gui"
```

## Troubleshooting

### PyQt6 Import Error

**Error**: `ImportError: DLL load failed while importing QtCore`

**Solution**:
```bash
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip
pip install PyQt6==6.6.1
```

### Torch CUDA Not Available

**Error**: `torch.cuda.is_available()` returns False

**Solutions**:
1. Reinstall PyTorch with CUDA:
   ```bash
   pip uninstall torch torchvision
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

2. Verify CUDA installation:
   ```bash
   nvidia-smi
   nvcc --version
   ```

### Pytest Not Finding Tests

**Error**: No tests found

**Solutions**:
1. Check pytest.ini configuration
2. Verify test file names start with `test_`
3. Verify test functions start with `test_`
4. Run from project root: `cd ALA-GUI && pytest`

### Virtual Environment Not Activating

**Windows PowerShell Error**: "execution of scripts is disabled"

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Next Steps

After successful setup:

1. ✅ Run all tests to verify: `pytest -v`
2. ✅ Run main application: `python src/main.py`
3. ✅ Check code quality: `black --check src/ && flake8 src/`
4. 📖 Read [PLAN.md](../../PLAN.md) for development roadmap
5. 📋 Start with tasks from [TODO.md](../../TODO.md) - M0 section

## Resources

- **PyQt6 Documentation**: https://www.riverbankcomputing.com/static/Docs/PyQt6/
- **pytest-qt Documentation**: https://pytest-qt.readthedocs.io/
- **Black Code Style**: https://black.readthedocs.io/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html

## Support

For issues or questions:
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review [FAQ.md](FAQ.md)
- Open issue on GitHub: https://github.com/tygwan/ALA-AutoLabelAgent/issues

---

**Last Updated**: 2025-01-13
**M0: Project Setup**
