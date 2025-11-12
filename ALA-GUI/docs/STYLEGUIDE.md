# ALA-GUI Code Style Guide

Coding standards and best practices for ALA-GUI development.

## Overview

**Code Formatter**: Black (line length: 88)
**Import Sorter**: isort (black profile)
**Linter**: flake8, pylint
**Type Checker**: mypy
**Security Scanner**: bandit

## Python Style

### General Principles

1. **PEP 8 Compliance**: Follow PEP 8 with Black modifications
2. **Readability First**: Code is read more than written
3. **Explicit Over Implicit**: Clear is better than clever
4. **DRY Principle**: Don't Repeat Yourself
5. **SOLID Principles**: Write maintainable OOP code

### Naming Conventions

**Modules and Packages**:
```python
# Use lowercase with underscores
import image_utils
from models.project_data import Project
```

**Classes**:
```python
# Use PascalCase
class ProjectManager:
    pass

class ImageCanvas:
    pass
```

**Functions and Methods**:
```python
# Use lowercase with underscores
def load_project(path: str) -> Project:
    pass

def calculate_confidence_score(annotations: list) -> float:
    pass
```

**Constants**:
```python
# Use UPPER_CASE with underscores
MAX_IMAGE_SIZE = 4096
DEFAULT_CONFIDENCE_THRESHOLD = 0.5
MODEL_CHECKPOINT_PATH = "models/sam2_checkpoint.pt"
```

**Private Members**:
```python
class MyClass:
    def __init__(self):
        self._private_var = 0  # Single underscore
        self.__very_private = 0  # Double underscore (name mangling)

    def _private_method(self):
        pass
```

### Type Hints

**Always use type hints** (Python 3.9+):
```python
from typing import List, Dict, Optional, Union
from pathlib import Path

def process_images(
    image_paths: List[Path],
    confidence_threshold: float = 0.5
) -> Dict[str, List[str]]:
    """Process multiple images and return results."""
    results: Dict[str, List[str]] = {}
    # Implementation
    return results

def get_annotation(annotation_id: str) -> Optional[Annotation]:
    """Get annotation by ID or None if not found."""
    # Implementation
    return None
```

**Use modern syntax (Python 3.9+)**:
```python
# Preferred (Python 3.9+)
def get_items() -> list[str]:
    return ["item1", "item2"]

# Old style (still acceptable)
from typing import List
def get_items() -> List[str]:
    return ["item1", "item2"]
```

### Docstrings

**Use Google-style docstrings**:

**Module-level**:
```python
"""
Project Manager Module

Handles project creation, loading, saving, and management.
Provides the core business logic for project operations.
"""
```

**Class-level**:
```python
class ProjectManager:
    """
    Manages ALA-GUI project lifecycle.

    Handles project creation, loading, saving, and state management.
    Supports .alagui ZIP archive format for project storage.

    Attributes:
        current_project: Currently loaded project or None
        config: Configuration manager instance

    Example:
        >>> manager = ProjectManager()
        >>> project = manager.create_project("My Project", Path("/path"))
        >>> manager.save_project(project, Path("/path/project.alagui"))
    """
```

**Function-level**:
```python
def load_project(project_path: Path) -> Project:
    """
    Load project from .alagui file.

    Args:
        project_path: Path to .alagui ZIP archive

    Returns:
        Loaded Project instance with all data

    Raises:
        FileNotFoundError: If project file doesn't exist
        ProjectError: If project file is corrupted

    Example:
        >>> project = load_project(Path("my_project.alagui"))
        >>> print(project.name)
        'My Project'
    """
```

### Import Organization

**Order** (enforced by isort):
1. Standard library
2. Third-party libraries
3. Local application imports

```python
# Standard library
import os
import sys
from pathlib import Path
from typing import List, Optional

# Third-party
import numpy as np
from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtCore import Qt, pyqtSignal

# Local application
from models.project import Project
from models.annotation import Annotation
from utils.file_io import load_image
```

### Code Formatting

**Line Length**: 88 characters (Black default)

**String Quotes**: Double quotes for strings, single for characters
```python
message = "This is a string"
char = 'a'
```

**Function Arguments**:
```python
# Short function call
result = process_image(image, threshold=0.5)

# Long function call (auto-formatted by Black)
result = process_multiple_images(
    image_paths=paths,
    confidence_threshold=0.5,
    batch_size=32,
    device="cuda",
)
```

**Collections**:
```python
# Lists
items = [1, 2, 3, 4, 5]

# Long lists
items = [
    "very_long_item_name_1",
    "very_long_item_name_2",
    "very_long_item_name_3",
]

# Dictionaries
config = {"name": "project", "version": "1.0"}

# Long dictionaries
config = {
    "name": "project",
    "version": "1.0",
    "author": "ALA Team",
    "settings": {"debug": False, "verbose": True},
}
```

## PyQt6 Style

### Widget Naming

```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Use descriptive names with widget type
        self.image_canvas = ImageCanvas()
        self.file_list_widget = QListWidget()
        self.save_button = QPushButton("Save")
        self.confidence_slider = QSlider()
```

### Signal/Slot Connections

```python
class MyWidget(QWidget):
    # Define custom signals
    data_changed = pyqtSignal(dict)
    processing_complete = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Connect signals
        self.button.clicked.connect(self.on_button_clicked)
        self.slider.valueChanged.connect(self.on_slider_changed)

    def on_button_clicked(self) -> None:
        """Handle button click event."""
        self.data_changed.emit({"status": "clicked"})

    def on_slider_changed(self, value: int) -> None:
        """Handle slider value change."""
        self.update_display(value)
```

### Layout Organization

```python
def setup_ui(self) -> None:
    """Set up the user interface layout."""
    # Create widgets
    self.create_widgets()

    # Create layouts
    main_layout = QVBoxLayout()
    toolbar_layout = QHBoxLayout()

    # Add widgets to layouts
    toolbar_layout.addWidget(self.save_button)
    toolbar_layout.addWidget(self.load_button)

    main_layout.addLayout(toolbar_layout)
    main_layout.addWidget(self.canvas)

    # Set layout
    self.setLayout(main_layout)
```

## Testing Style

### Test Function Names

```python
# Use descriptive names: test_what_when_expected
def test_load_project_when_file_exists_returns_project():
    pass

def test_add_annotation_with_invalid_class_raises_error():
    pass

def test_save_project_creates_zip_file():
    pass
```

### Test Structure (AAA Pattern)

```python
def test_annotation_to_coco_format():
    # Arrange
    annotation = Annotation(
        id="test-1",
        class_id=0,
        type="polygon",
        geometry={"points": [[10, 10], [50, 50]]}
    )

    # Act
    coco_dict = annotation.to_coco()

    # Assert
    assert coco_dict["id"] == "test-1"
    assert coco_dict["category_id"] == 0
    assert "segmentation" in coco_dict
```

### Fixtures Usage

```python
@pytest.fixture
def sample_project():
    """Create a sample project for testing."""
    return Project(name="Test", path="/tmp/test.alagui")

def test_with_fixture(sample_project):
    """Test using fixture."""
    assert sample_project.name == "Test"
```

## Error Handling

### Exception Hierarchy

```python
class AlaGuiException(Exception):
    """Base exception for ALA-GUI."""

class ProjectError(AlaGuiException):
    """Project-related errors."""

class ModelError(AlaGuiException):
    """Model inference errors."""

class FileIOError(AlaGuiException):
    """File I/O errors."""
```

### Exception Raising

```python
def load_image(path: Path) -> np.ndarray:
    """Load image from file."""
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    if not path.suffix.lower() in ['.jpg', '.png']:
        raise ValueError(f"Unsupported image format: {path.suffix}")

    # Load image
    return image
```

### Exception Handling

```python
def safe_load_project(path: Path) -> Optional[Project]:
    """Safely load project with error handling."""
    try:
        return load_project(path)
    except FileNotFoundError:
        logger.error(f"Project file not found: {path}")
        return None
    except ProjectError as e:
        logger.error(f"Failed to load project: {e}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error loading project: {e}")
        raise
```

## Logging

### Logger Setup

```python
import logging

logger = logging.getLogger(__name__)

def process_images(paths: List[Path]) -> None:
    """Process multiple images."""
    logger.info(f"Processing {len(paths)} images")

    for path in paths:
        logger.debug(f"Processing: {path}")
        # Process image

    logger.info("Processing complete")
```

### Log Levels

```python
logger.debug("Detailed diagnostic information")
logger.info("General informational messages")
logger.warning("Warning messages for potential issues")
logger.error("Error messages for failures")
logger.exception("Error with full traceback")
logger.critical("Critical errors requiring immediate attention")
```

## Comments

### When to Comment

```python
# GOOD: Explain WHY, not WHAT
# Use binary search for O(log n) performance on large datasets
result = binary_search(items, target)

# BAD: Obvious comment
# Increment counter by 1
counter += 1
```

### TODO Comments

```python
# TODO(username): Add support for video files
# FIXME(username): Memory leak in image caching
# HACK(username): Temporary workaround for PyQt6 bug #12345
# NOTE(username): This approach chosen for compatibility with v1.0
```

## Best Practices

### DO ✅

- Use type hints for all functions
- Write docstrings for public APIs
- Follow TDD: RED → GREEN → REFACTOR
- Keep functions small (<50 lines)
- Use descriptive variable names
- Handle errors explicitly
- Log important operations
- Write tests for edge cases

### DON'T ❌

- Use `import *`
- Mutate function arguments
- Use bare `except:` clauses
- Ignore type checker warnings
- Leave commented-out code
- Use single-letter variables (except loops)
- Hard-code file paths or URLs
- Skip docstrings for public APIs

## Code Review Checklist

Before committing:

- [ ] Code formatted with Black
- [ ] Imports sorted with isort
- [ ] No flake8 warnings
- [ ] No mypy errors
- [ ] All tests passing
- [ ] Test coverage meets target
- [ ] Docstrings added for public APIs
- [ ] Type hints added
- [ ] No security issues (bandit)
- [ ] Commit message follows conventions

## Tools Usage

### Format Code

```bash
# Format all code
black src/ tests/

# Check without modifying
black --check src/
```

### Sort Imports

```bash
# Sort all imports
isort src/ tests/

# Check without modifying
isort --check src/
```

### Lint Code

```bash
# Run flake8
flake8 src/ tests/

# Run pylint
pylint src/
```

### Type Check

```bash
# Run mypy
mypy src/
```

### Security Scan

```bash
# Run bandit
bandit -r src/
```

### Run All Checks

```bash
# Format
black src/ tests/
isort src/ tests/

# Lint
flake8 src/ tests/
pylint src/

# Type check
mypy src/

# Security
bandit -r src/

# Test
pytest
```

## Resources

- **PEP 8**: https://pep8.org/
- **Black**: https://black.readthedocs.io/
- **Google Python Style Guide**: https://google.github.io/styleguide/pyguide.html
- **Type Hints**: https://docs.python.org/3/library/typing.html
- **PyQt6 Best Practices**: https://www.riverbankcomputing.com/static/Docs/PyQt6/

---

**Last Updated**: 2025-01-13
**M0: Project Setup**
