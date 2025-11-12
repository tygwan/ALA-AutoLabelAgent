# ALA-GUI Testing Guide

Comprehensive guide for testing ALA-GUI following TDD methodology.

## Testing Philosophy

**Test-Driven Development (TDD)**: RED → GREEN → REFACTOR → COMMIT

1. **RED**: Write a failing test first
2. **GREEN**: Write minimal code to make test pass
3. **REFACTOR**: Improve code while keeping tests green
4. **COMMIT**: Commit with conventional commit message

## Testing Framework

### Core Tools

- **pytest**: Testing framework
- **pytest-qt**: PyQt6 widget testing
- **pytest-cov**: Code coverage reporting
- **pytest-mock**: Mocking utilities

### Test Structure

```
tests/
├── unit/               # Fast, isolated tests
├── integration/        # Component interaction tests
├── e2e/               # End-to-end workflow tests
├── conftest.py        # Shared fixtures
└── utils_test.py      # Testing utilities
```

## Test Categories

### Unit Tests

**Purpose**: Test individual functions/classes in isolation

**Characteristics**:
- Fast execution (<1ms per test)
- No external dependencies
- Mock all I/O operations
- High coverage target (90%+)

**Example**:
```python
import pytest
from models.annotation import Annotation

def test_annotation_to_coco():
    """Test annotation conversion to COCO format."""
    annotation = Annotation(
        id="test-1",
        image_id="img-1",
        class_id=0,
        type="polygon",
        geometry={"points": [[10, 10], [50, 10], [50, 50]]},
        confidence=0.95
    )

    coco_dict = annotation.to_coco()

    assert coco_dict["id"] == "test-1"
    assert coco_dict["image_id"] == "img-1"
    assert coco_dict["category_id"] == 0
```

### Integration Tests

**Purpose**: Test component interactions

**Characteristics**:
- Moderate execution time
- Tests multiple components together
- May use real file I/O, databases
- Coverage target (70%+)

**Example**:
```python
import pytest
from controllers.project_manager import ProjectManager

def test_project_save_and_load(tmp_path):
    """Test project save and load workflow."""
    # Create project
    manager = ProjectManager()
    project = manager.create_project("Test Project", tmp_path)

    # Add data
    manager.add_image(project, "test.jpg")

    # Save project
    project_path = tmp_path / "test.alagui"
    manager.save_project(project, project_path)

    # Load project
    loaded_project = manager.load_project(project_path)

    assert loaded_project.name == "Test Project"
    assert len(loaded_project.images) == 1
```

### E2E Tests

**Purpose**: Test complete user workflows

**Characteristics**:
- Slow execution (seconds to minutes)
- Tests full application flow
- Uses real GUI interactions
- Coverage target (50%+)

**Example**:
```python
import pytest

@pytest.mark.e2e
def test_auto_annotation_workflow(qtbot, main_window):
    """Test complete auto-annotation workflow."""
    # 1. Load project
    main_window.load_project("test_project.alagui")
    qtbot.wait(100)

    # 2. Open auto-annotate dialog
    main_window.show_auto_annotate_dialog()
    qtbot.wait(100)

    # 3. Enter text prompt
    dialog = main_window.findChild(AutoAnnotateDialog)
    dialog.prompt_input.setText("dog")

    # 4. Run annotation
    dialog.run_button.click()
    qtbot.waitUntil(lambda: dialog.is_complete(), timeout=30000)

    # 5. Verify results
    assert len(main_window.annotation_manager.annotations) > 0
```

## PyQt6 Testing

### QApplication Setup

**Automatic setup via pytest-qt**:
```python
# conftest.py provides qapp_cls fixture
def test_widget(qtbot):
    widget = MyWidget()
    qtbot.addWidget(widget)  # Automatic cleanup
    assert widget.isVisible()
```

### Widget Testing

**Button clicks**:
```python
def test_button_click(qtbot, main_window):
    button = main_window.save_button

    with qtbot.waitSignal(button.clicked):
        button.click()
```

**Text input**:
```python
def test_text_input(qtbot):
    line_edit = QLineEdit()
    qtbot.addWidget(line_edit)

    qtbot.keyClicks(line_edit, "test input")

    assert line_edit.text() == "test input"
```

**Wait for signals**:
```python
def test_signal_emission(qtbot, widget):
    with qtbot.waitSignal(widget.data_changed, timeout=1000):
        widget.update_data()
```

**Wait for conditions**:
```python
def test_async_operation(qtbot, widget):
    widget.start_operation()

    qtbot.waitUntil(lambda: widget.is_complete(), timeout=5000)

    assert widget.result is not None
```

### Image Testing

**Using test utilities**:
```python
from tests.utils_test import create_test_pixmap, pixmaps_equal

def test_image_loading():
    # Create test image
    pixmap = create_test_pixmap(100, 100, color=(255, 0, 0))

    # Test loading
    canvas = ImageCanvas()
    canvas.load_image(pixmap)

    # Verify
    assert pixmaps_equal(canvas.current_image, pixmap)
```

## Fixtures

### Built-in Fixtures

**qtbot**: PyQt6 widget testing helper
```python
def test_widget(qtbot):
    widget = MyWidget()
    qtbot.addWidget(widget)
```

**tmp_path**: Temporary directory
```python
def test_file_io(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("test")
```

**monkeypatch**: Mock objects
```python
def test_with_mock(monkeypatch):
    monkeypatch.setattr("os.path.exists", lambda x: True)
```

### Custom Fixtures

**Project fixtures** (conftest.py):
```python
@pytest.fixture
def sample_project(tmp_path):
    return {
        "name": "Test Project",
        "path": str(tmp_path / "test.alagui"),
        "classes": [{"id": 0, "name": "dog"}]
    }

@pytest.fixture
def sample_annotation():
    return {
        "id": "test-1",
        "class_id": 0,
        "type": "polygon",
        "geometry": {"points": [[10, 10], [50, 50]]}
    }
```

## Test Markers

### Using Markers

**Mark tests by category**:
```python
@pytest.mark.unit
def test_fast_unit():
    pass

@pytest.mark.integration
def test_integration():
    pass

@pytest.mark.e2e
def test_slow_e2e():
    pass

@pytest.mark.slow
def test_very_slow():
    pass

@pytest.mark.gui
def test_requires_gui():
    pass
```

**Run specific markers**:
```bash
# Only unit tests
pytest -m unit

# Only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# Skip GUI tests (for CI)
pytest -m "not gui"
```

## Mocking

### Mocking PyQt6

**Mock QMessageBox**:
```python
def test_error_dialog(monkeypatch, qtbot):
    mock_box = MagicMock()
    monkeypatch.setattr("PyQt6.QtWidgets.QMessageBox.critical", mock_box)

    widget = MyWidget()
    widget.show_error("Test error")

    mock_box.assert_called_once()
```

### Mocking Models

**Mock model inference**:
```python
def test_auto_annotate(monkeypatch):
    def mock_predict(image, prompt):
        return [{"bbox": [10, 10, 50, 50], "score": 0.95}]

    monkeypatch.setattr(SAM2Model, "predict", mock_predict)

    controller = ModelController()
    results = controller.run_autodistill("test.jpg", "dog")

    assert len(results) == 1
```

## Coverage

### Running Coverage

**Generate coverage report**:
```bash
pytest --cov=src --cov-report=html --cov-report=term
```

**View HTML report**:
```bash
# Windows
start htmlcov/index.html

# Linux/macOS
open htmlcov/index.html
```

### Coverage Targets

| Test Type | Target | Requirement |
|-----------|--------|-------------|
| Unit | 90%+ | Per module |
| Integration | 70%+ | Per component |
| E2E | 50%+ | Critical paths |
| Overall | 70%+ | Project-wide |

### Excluding from Coverage

**In code**:
```python
def debug_function():  # pragma: no cover
    """Development helper, not covered."""
    print("Debug info")
```

**In pytest.ini**:
```ini
[coverage:run]
omit =
    */tests/*
    */test_*.py
    */__pycache__/*
```

## Running Tests

### Basic Commands

**All tests**:
```bash
pytest
```

**Verbose output**:
```bash
pytest -v
```

**Specific file**:
```bash
pytest tests/unit/test_project_manager.py
```

**Specific test**:
```bash
pytest tests/unit/test_project_manager.py::test_create_project
```

**Last failed**:
```bash
pytest --lf
```

**Stop on first failure**:
```bash
pytest -x
```

### Advanced Options

**Parallel execution**:
```bash
pytest -n auto  # Requires pytest-xdist
```

**Show print output**:
```bash
pytest -s
```

**Show local variables on failure**:
```bash
pytest -l
```

**Generate JUnit XML**:
```bash
pytest --junit-xml=test-results.xml
```

## Continuous Integration

### GitHub Actions

Tests run automatically on:
- Every push to main
- Every pull request
- Scheduled daily runs

**Workflow file** (.github/workflows/tests.yml):
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v3
```

## Best Practices

### DO

✅ Write tests before implementation (TDD)
✅ Use descriptive test names (test_what_when_expected)
✅ Test one thing per test
✅ Use fixtures for setup
✅ Mock external dependencies
✅ Test edge cases and errors
✅ Keep tests fast and independent
✅ Clean up resources (use qtbot.addWidget)

### DON'T

❌ Skip tests to save time
❌ Test implementation details
❌ Use real file I/O in unit tests
❌ Depend on test execution order
❌ Use time.sleep() (use qtbot.wait)
❌ Test private methods directly
❌ Ignore failing tests

## Troubleshooting

### Common Issues

**QApplication already exists**:
```python
# Use qtbot fixture instead of creating QApplication
def test_widget(qtbot):  # Correct
    widget = MyWidget()
```

**Widget not shown**:
```python
def test_widget(qtbot):
    widget = MyWidget()
    qtbot.addWidget(widget)
    widget.show()
    qtbot.waitExposed(widget)
```

**Signal not emitted**:
```python
# Increase timeout
with qtbot.waitSignal(widget.signal, timeout=5000):
    widget.trigger_action()
```

**Tests hang**:
```python
# Use qtbot.waitUntil with timeout
qtbot.waitUntil(lambda: condition, timeout=1000)
```

## Resources

- **pytest Documentation**: https://docs.pytest.org/
- **pytest-qt Documentation**: https://pytest-qt.readthedocs.io/
- **PyQt6 Documentation**: https://www.riverbankcomputing.com/static/Docs/PyQt6/
- **Testing Best Practices**: https://docs.python-guide.org/writing/tests/

---

**Last Updated**: 2025-01-13
**M0: Project Setup**
