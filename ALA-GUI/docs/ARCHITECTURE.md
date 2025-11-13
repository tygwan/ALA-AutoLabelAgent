# ALA-GUI Architecture

## Overview

ALA-GUI follows a layered MVC architecture with clear separation of concerns and comprehensive testing.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        GUI Layer (M2)                        │
│                  PyQt6 UI Components                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                   Controller Layer (M1)                      │
│              ProjectManager, Image Processing                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                     Model Layer (M1)                         │
│          Project, Image, Annotation, ClassDefinition         │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│              Utility & System Layer (M1)                     │
│     Config, Logging, File I/O, Image Utils, Path Utils      │
└─────────────────────────────────────────────────────────────┘
```

## M1: Foundation & Core Infrastructure (Complete)

M1 provides the foundational layers for data management, system utilities, and business logic.

### Data Layer

#### Models (`src/models/`)

**Project** (`project.py`)
- Central data structure for labeling projects
- Features:
  - UUID-based identification
  - Timestamp tracking (created_at, updated_at)
  - JSON serialization/deserialization
  - Platform-independent path handling
  - Image and class management
- Serialization: Properly converts nested objects (images, classes) to/from JSON

**Image** (`image.py`)
- Represents image files with metadata
- Features:
  - Automatic filename extraction
  - Dimension tracking (width, height)
  - Aspect ratio calculation
  - Annotation management
  - Custom metadata support

**Annotation** (`annotation.py`)
- Bounding box and segmentation data
- Features:
  - COCO format export
  - YOLO format export
  - Area calculation
  - Automatic type detection (bbox vs segmentation)

**ClassDefinition** (`class_definition.py`)
- Object class definitions with colors
- Features:
  - Hex color validation
  - RGB tuple conversion
  - Unique identification

### Controller Layer

#### ProjectManager (`src/controllers/`)

Manages project lifecycle and operations:
- **Project Creation**: Creates project directories and initializes Project objects
- **Project Persistence**: JSON-based save/load with error handling
- **Image Management**: Validates and adds images to projects
- **State Management**: Tracks current active project

### System Layer (`src/utils/`)

#### Error Handling (`exceptions.py`)

Custom exception hierarchy:
- **AlaGuiException**: Base exception with details dict
- **ProjectError**: Project-specific errors
- **ImageError**: Image operation errors
- **ModelError**: Model loading/inference errors
- **ConfigError**: Configuration validation errors

Features:
- Exception chaining support
- Contextual error details
- Type-safe error handling

#### Configuration (`config_manager.py`)

Type-safe configuration management:
- **Default Values**: Window settings, app configuration
- **Validation**: Min/max range validation, type checking
- **Persistence**: JSON storage in ~/.ala-gui/config.json
- **Type-Safe Getters**: `get_int()`, `get_str()`, `get_bool()`

Configuration Keys:
- `app_name`, `version`
- `window_width`, `window_height`, `window_x`, `window_y`
- `recent_projects`, `max_recent_projects`
- `auto_save`, `auto_save_interval`
- `theme`, `language`

#### Logging (`logger.py`)

Structured logging system:
- **Multiple Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Output Targets**: File and console with configurable formatting
- **Context Logging**: Extra context information support
- **Exception Logging**: Traceback capture
- **Timestamped**: ISO format timestamps

### Utility Layer (`src/utils/`)

#### Image Utilities (`image_utils.py`)

PIL-based image operations:
- **Format Validation**: JPG, PNG, BMP, GIF, TIFF support
- **Dimension Extraction**: Width/height detection
- **Metadata Extraction**: Comprehensive image info
- **Aspect Ratio**: Calculation with zero-height handling
- **Path Validation**: Security checks with unicode support

Supported Formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, `.tiff`, `.tif`

#### File I/O Utilities (`file_utils.py`)

File system operations:
- **JSON Operations**: Save/load with unicode support
- **Directory Operations**: Recursive creation, pattern-based listing
- **File Operations**: Copy, move, delete with error handling
- **Safe Operations**: Automatic backups before overwrites

Features:
- Platform-independent paths
- Unicode filename support
- Error recovery with AlaGuiException

#### Path Utilities (`path_utils.py`)

Secure path manipulation:
- **Security Validation**: Path traversal attack prevention
- **Filename Sanitization**: Invalid character removal
- **Path Normalization**: `.` and `..` resolution
- **Relative/Absolute**: Conversion operations
- **Subpath Detection**: Parent-child relationship checks

Security Features:
- Prevents directory traversal (e.g., `../../etc/passwd`)
- Validates paths against base directory
- Sanitizes Windows and Unix invalid characters

## Testing Strategy

### Test Organization

```
tests/
├── unit/              # Unit tests (168 tests)
│   ├── test_*_model.py
│   ├── test_*_manager.py
│   └── test_*_utils.py
├── integration/       # Integration tests (10 tests)
│   └── test_project_workflow.py
└── conftest.py        # Shared fixtures
```

### Test Coverage

**M1 Total: 178 tests (100% passing for non-GUI tests)**

- **Data Models**: 56 tests
  - Project: 8 tests
  - Image: 11 tests
  - Annotation: 10 tests
  - ClassDefinition: 12 tests
  - ProjectManager: 15 tests

- **System Layer**: 50 tests
  - Exceptions: 13 tests
  - ConfigManager: 19 tests
  - Logger: 18 tests

- **Utility Layer**: 62 tests
  - ImageUtils: 21 tests
  - FileUtils: 20 tests
  - PathUtils: 21 tests

- **Integration**: 10 tests
  - Project workflows
  - Image persistence
  - Logging integration
  - Error handling
  - Complete lifecycle

### Testing Approach

Following TDD (Test-Driven Development):
1. **RED**: Write failing test
2. **GREEN**: Implement minimal code to pass
3. **REFACTOR**: Improve code quality

Test Categories:
- **Unit Tests**: Individual component testing
- **Integration Tests**: Multi-component workflows
- **Fixtures**: Shared test data (conftest.py)

## Design Patterns

### Data Access Pattern
- **Repository**: ProjectManager acts as repository for Project objects
- **Serialization**: to_dict/from_dict pattern for JSON persistence
- **Validation**: Path and data validation at boundaries

### Error Handling Pattern
- **Exception Hierarchy**: Domain-specific exceptions
- **Context Preservation**: Details dict for debugging
- **Fail Fast**: Validate early, report clearly

### Utility Pattern
- **Static Methods**: All utility classes use static methods
- **Type Safety**: Type hints throughout
- **Defensive Programming**: Input validation, Path object enforcement

## Data Flow

### Project Creation Flow

```
User Input
    ↓
ProjectManager.create_project()
    ↓
1. Validate inputs
2. Create directory (FileUtils)
3. Create Project instance
4. Set as current_project
    ↓
Return Project
```

### Image Addition Flow

```
Image File
    ↓
1. ImageUtils.validate_path()
2. ImageUtils.get_dimensions()
    ↓
ProjectManager.add_image()
    ↓
1. Check active project
2. Create Image instance
3. Append to project.images
    ↓
Return Image
```

### Project Persistence Flow

```
Project Object
    ↓
Project.to_dict()
    ↓
1. Serialize nested objects (images, classes)
2. Convert UUIDs to strings
3. Convert Paths to POSIX format
    ↓
FileUtils.save_json()
    ↓
JSON File
```

## Code Organization

### Module Structure

```
src/
├── models/              # Data models
│   ├── __init__.py      # Public API
│   ├── project.py
│   ├── image.py
│   ├── annotation.py
│   └── class_definition.py
├── controllers/         # Business logic
│   ├── __init__.py
│   └── project_manager.py
└── utils/              # Utilities & system
    ├── __init__.py      # Public API
    ├── exceptions.py
    ├── config_manager.py
    ├── logger.py
    ├── image_utils.py
    ├── file_utils.py
    └── path_utils.py
```

### Import Strategy

- **Absolute Imports**: All imports use absolute paths from `src/`
- **Public API**: `__init__.py` files export public interfaces
- **Type Hints**: Full type annotation for clarity

### Naming Conventions

- **Classes**: PascalCase (`ProjectManager`, `ImageUtils`)
- **Functions/Methods**: snake_case (`create_project`, `save_json`)
- **Constants**: UPPER_SNAKE_CASE (`SUPPORTED_FORMATS`, `DEFAULTS`)
- **Private**: Leading underscore (`_config`, `_validate_value`)

## Security Considerations

### Path Security
- **Traversal Prevention**: PathUtils validates all paths against base
- **Sanitization**: Remove invalid filename characters
- **Validation**: Check file existence before operations

### Data Validation
- **Type Checking**: Enforce types at boundaries
- **Range Validation**: Min/max checks for numeric values
- **Format Validation**: Hex colors, image formats, JSON structure

### Error Information
- **No Sensitive Data**: Error messages don't leak system details
- **Controlled Logging**: Sensitive info not logged
- **User-Friendly**: Clear error messages for users

## Performance Considerations

### File Operations
- **Buffered I/O**: Use Python's buffered file operations
- **Lazy Loading**: Load images on demand, not at startup
- **Caching**: ConfigManager caches config in memory

### Image Processing
- **PIL Optimization**: Use PIL's optimized image operations
- **Dimension Caching**: Cache image dimensions after first read
- **Format Detection**: Quick header-based format detection

### Memory Management
- **Context Managers**: Use `with` statements for file operations
- **Resource Cleanup**: Explicit cleanup in error paths
- **Small Footprint**: Minimize in-memory data structures

## Future Architecture (M2-M5)

### M2: GUI Layer
- **MainWindow**: PyQt6 main window
- **Widgets**: Image viewer, annotation tools, class manager
- **Dialogs**: Project settings, preferences
- **Integration**: Connect GUI to M1 controllers

### M3: Annotation Tools
- **Bounding Box**: Rectangle drawing
- **Segmentation**: Polygon drawing
- **Keyboard Shortcuts**: Efficient workflow

### M4: Model Integration
- **Florence-2**: Caption generation
- **Grounded SAM 2**: Segmentation
- **YOLO**: Object detection

### M5: Advanced Features
- **Batch Processing**: Multiple images
- **Import/Export**: COCO, YOLO formats
- **Undo/Redo**: Action history

## Development Guidelines

### Adding New Features
1. Write tests first (TDD)
2. Implement minimal code
3. Refactor for quality
4. Update documentation
5. Commit with logical grouping

### Code Quality Standards
- **Type Hints**: All functions have type annotations
- **Docstrings**: All public APIs documented
- **Error Handling**: Use custom exceptions
- **Testing**: ≥95% coverage for new code

### Git Workflow
- **Logical Commits**: Group related changes
- **Clear Messages**: Describe what and why
- **TDD Cycle**: Commit after GREEN phase

## Dependencies

### Core Dependencies
- **Python**: 3.9+
- **PyQt6**: 6.6.1 (GUI framework)
- **Pillow**: 10.2.0 (Image processing)

### Development Dependencies
- **pytest**: 7.4.3 (Testing framework)
- **black**: 24.1.1 (Code formatter)
- **isort**: 5.13.2 (Import sorter)
- **mypy**: 1.8.0 (Type checker)

### AI/ML Dependencies (Future)
- **torch**: 2.1.2
- **transformers**: 4.36.2
- **ultralytics**: 8.1.11

## Conclusion

M1 establishes a solid foundation with:
- ✅ Clean architecture with clear layers
- ✅ Comprehensive test coverage (178 tests)
- ✅ Type-safe operations throughout
- ✅ Robust error handling
- ✅ Secure file operations
- ✅ Extensible design for future features

The architecture supports TDD workflow and enables rapid development of GUI (M2) and advanced features (M3-M5).
