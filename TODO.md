# ALA GUI - Task List (TDD-Driven)

## Version: 1.0
**Last Updated**: 2025-01-13
**Status**: Ready for execution
**Based on**: PLAN.md v1.0
**Total Tasks**: 412 tasks
**Total Estimated Time**: ~580 hours (15 weeks solo developer)

---

## Key Changes from v0.0

**Initial Version**:
- Created comprehensive task breakdown for all 8 milestones (M0-M8)
- Applied TDD cycle (RED → GREEN → REFACTOR → COMMIT) to all implementation tasks
- Set realistic time estimates for solo developer (0.5h - 4.0h range)
- Established task categories: [RED], [GREEN], [REFACTOR], [COMMIT], [DOC], [INT], [E2E], [SETUP]
- Total timeline: 15 weeks MVP + 5 weeks buffer = 20 weeks
- Quality targets: 70%+ unit, 60%+ integration, 50%+ E2E coverage

---

## How to Use This Document

Each task follows TDD cycle: **RED → GREEN → REFACTOR → COMMIT**

### Task Format
```
- [ ] Task description (X.Xh) [category] {milestone-id}
```

**Example**:
```
- [ ] Write test for image loading (1.0h) [RED] {M2}
- [ ] Implement QPixmap image loader (1.5h) [GREEN] {M2}
- [ ] Refactor image loading logic (0.5h) [REFACTOR] {M2}
- [ ] Commit: "feat(ui): add image loading" (0.5h) [COMMIT] {M2}
```

### Categories

| Category | Purpose | When to Use |
|----------|---------|-------------|
| [RED] | Write failing test | Before any implementation |
| [GREEN] | Implement code to pass test | After test fails correctly |
| [REFACTOR] | Improve code structure | When tests are green |
| [COMMIT] | Git commit with message | After refactoring complete |
| [DOC] | Documentation task | Throughout development |
| [INT] | Integration test | Cross-component testing |
| [E2E] | End-to-end test | User workflow testing |
| [SETUP] | Setup/configuration | Environment/tool setup |

---

## M0: Project Setup
**Duration**: 1 week | **Total**: 40h (solo developer)
**Priority**: P1

### Development Environment (12h)
- [ ] Install PyQt6 and verify version (0.5h) [SETUP] {M0}
- [ ] Install pytest and pytest-qt (0.5h) [SETUP] {M0}
- [ ] Install OpenCV, Pillow for image processing (0.5h) [SETUP] {M0}
- [ ] Install Gradio for web interface (0.5h) [SETUP] {M0}
- [x] Create project directory structure (src/, tests/, docs/, examples/) (1.0h) [SETUP] {M0}
- [x] Set up virtual environment and requirements.txt (1.0h) [SETUP] {M0}
- [ ] Configure VS Code/PyCharm for PyQt6 development (1.0h) [SETUP] {M0}
- [x] Set up Git repository and .gitignore (0.5h) [SETUP] {M0}
- [x] Create README.md with project overview (1.5h) [DOC] {M0}
- [ ] Configure pre-commit hooks (black, flake8, mypy) (1.5h) [SETUP] {M0}
- [x] Test environment with "Hello PyQt6" window (1.0h) [SETUP] {M0}
- [x] Document environment setup in SETUP.md (2.0h) [DOC] {M0}

### Testing Infrastructure (10h)
- [x] Configure pytest.ini with PyQt6 settings (0.5h) [SETUP] {M0}
- [x] Write sample pytest-qt test to verify setup (1.0h) [RED] {M0}
- [x] Make sample test pass with basic widget (0.5h) [GREEN] {M0}
- [x] Set up pytest-cov for coverage reporting (0.5h) [SETUP] {M0}
- [x] Configure coverage thresholds in pytest.ini (0.5h) [SETUP] {M0}
- [x] Create test fixtures for QApplication (1.0h) [GREEN] {M0}
- [x] Create mock factories for images and annotations (2.0h) [GREEN] {M0}
- [x] Write test utilities for QPixmap comparison (1.5h) [GREEN] {M0}
- [x] Document testing conventions in TESTING.md (2.0h) [DOC] {M0}
- [ ] Commit: "test: set up pytest-qt infrastructure" (0.5h) [COMMIT] {M0}

### CI/CD Pipeline (10h)
- [x] Create .github/workflows/tests.yml (1.0h) [SETUP] {M0}
- [x] Configure GitHub Actions for pytest (1.5h) [SETUP] {M0}
- [x] Add linting step (black, flake8, mypy) (1.0h) [SETUP] {M0}
- [x] Add coverage reporting to GitHub Actions (1.0h) [SETUP] {M0}
- [ ] Test CI pipeline with sample commit (0.5h) [SETUP] {M0}
- [ ] Add badge to README.md for build status (0.5h) [DOC] {M0}
- [ ] Configure auto-formatting on push (1.0h) [SETUP] {M0}
- [x] Set up pre-commit hooks for local development (1.0h) [SETUP] {M0}
- [x] Document CI/CD workflow in CONTRIBUTING.md (2.0h) [DOC] {M0}
- [ ] Commit: "ci: add GitHub Actions pipeline" (0.5h) [COMMIT] {M0}

### Code Quality Tools (8h)
- [x] Configure black formatter with PyQt6 settings (0.5h) [SETUP] {M0}
- [x] Configure flake8 linting rules (0.5h) [SETUP] {M0}
- [x] Configure mypy type checking (1.0h) [SETUP] {M0}
- [x] Install and configure pylint (0.5h) [SETUP] {M0}
- [x] Set up isort for import sorting (0.5h) [SETUP] {M0}
- [x] Configure Bandit for security scanning (0.5h) [SETUP] {M0}
- [x] Create .editorconfig for consistency (0.5h) [SETUP] {M0}
- [ ] Test all quality tools on sample code (1.0h) [SETUP] {M0}
- [x] Document code style in STYLEGUIDE.md (2.0h) [DOC] {M0}
- [ ] Commit: "chore: add code quality tools" (0.5h) [COMMIT] {M0}

**M0 Subtotal**: 40h

---

## M1: Foundation & Core Infrastructure ✅ COMPLETE
**Duration**: 1.5 weeks | **Total**: 60h (solo developer)
**Priority**: P0 (Critical)
**Status**: ✅ 100% Complete (182 tests passing)

### Project Data Model (10h) ✅
- [x] Write test for Project dataclass initialization (0.5h) [RED] {M1}
- [x] Implement Project dataclass with UUID (1.0h) [GREEN] {M1}
- [x] Write test for Image dataclass (0.5h) [RED] {M1}
- [x] Implement Image dataclass with metadata (1.0h) [GREEN] {M1}
- [x] Write test for Annotation dataclass (0.5h) [RED] {M1}
- [x] Implement Annotation dataclass with COCO/YOLO methods (1.5h) [GREEN] {M1}
- [x] Write test for Class dataclass (0.5h) [RED] {M1}
- [x] Implement Class dataclass with validation (1.0h) [GREEN] {M1}
- [x] Refactor data models for consistency (1.0h) [REFACTOR] {M1}
- [x] Write integration test for data model relationships (1.5h) [INT] {M1}
- [x] Document data models in docs/ARCHITECTURE.md (1.0h) [DOC] {M1}
- [x] Commit: "feat(model): add data models" (0.5h) [COMMIT] {M1}

### Project Manager (12h) ✅
- [x] Write test for ProjectManager initialization (0.5h) [RED] {M1}
- [x] Implement ProjectManager class (1.0h) [GREEN] {M1}
- [x] Write test for create_project() (0.5h) [RED] {M1}
- [x] Implement create_project() method (1.0h) [GREEN] {M1}
- [x] Write test for load_project() (0.5h) [RED] {M1}
- [x] Implement load_project() from JSON (1.5h) [GREEN] {M1}
- [x] Write test for save_project() (0.5h) [RED] {M1}
- [x] Implement save_project() to JSON (1.5h) [GREEN] {M1}
- [x] Write test for add_image() (0.5h) [RED] {M1}
- [x] Implement add_image() with validation (1.0h) [GREEN] {M1}
- [x] Refactor ProjectManager for better error handling (1.0h) [REFACTOR] {M1}
- [x] Write integration test for project lifecycle (1.5h) [INT] {M1}
- [x] Document ProjectManager API in docs/ARCHITECTURE.md (1.0h) [DOC] {M1}
- [x] Commit: "feat(core): add ProjectManager" (0.5h) [COMMIT] {M1}

### Error Handling Framework (8h) ✅
- [x] Write test for base AlaGuiException (0.5h) [RED] {M1}
- [x] Implement AlaGuiException base class (0.5h) [GREEN] {M1}
- [x] Write tests for specific exceptions (ProjectError, ImageError, ModelError) (1.0h) [RED] {M1}
- [x] Implement specific exception classes (1.0h) [GREEN] {M1}
- [x] Write test for error context details (0.5h) [RED] {M1}
- [x] Implement error context with details dict (1.0h) [GREEN] {M1}
- [x] Write test for error chaining (0.5h) [RED] {M1}
- [x] Implement exception chaining support (1.0h) [GREEN] {M1}
- [x] Refactor exception handling patterns (0.5h) [REFACTOR] {M1}
- [x] Document error handling in docs/ARCHITECTURE.md (1.0h) [DOC] {M1}
- [x] Commit: "feat(system): add error handling framework" (0.5h) [COMMIT] {M1}

### Configuration System (10h) ✅
- [x] Write test for ConfigManager initialization (0.5h) [RED] {M1}
- [x] Implement ConfigManager with JSON persistence (1.0h) [GREEN] {M1}
- [x] Write test for get/set config values (0.5h) [RED] {M1}
- [x] Implement config getters/setters (1.0h) [GREEN] {M1}
- [x] Write test for default config values (0.5h) [RED] {M1}
- [x] Implement default config loading (1.0h) [GREEN] {M1}
- [x] Write test for config validation (0.5h) [RED] {M1}
- [x] Implement config validation logic (1.0h) [GREEN] {M1}
- [x] Write test for config file persistence (0.5h) [RED] {M1}
- [x] Implement JSON persistence to ~/.ala-gui/config.json (1.0h) [GREEN] {M1}
- [x] Refactor ConfigManager for better type safety (1.0h) [REFACTOR] {M1}
- [x] Document configuration options in docs/ARCHITECTURE.md (1.0h) [DOC] {M1}
- [x] Commit: "feat(system): add configuration system" (0.5h) [COMMIT] {M1}

### Logging System (8h) ✅
- [x] Write test for logger initialization (0.5h) [RED] {M1}
- [x] Implement structured logger with Python logging (1.0h) [GREEN] {M1}
- [x] Write test for log levels (DEBUG, INFO, WARNING, ERROR) (0.5h) [RED] {M1}
- [x] Implement log level filtering (0.5h) [GREEN] {M1}
- [x] Write test for log file output (0.5h) [RED] {M1}
- [x] Implement file handler with rotation support (1.0h) [GREEN] {M1}
- [x] Write test for log context (user actions, errors) (0.5h) [RED] {M1}
- [x] Implement context enrichment with metadata (1.0h) [GREEN] {M1}
- [x] Write test for exception logging (0.5h) [RED] {M1}
- [x] Implement exception logging with traceback (1.0h) [GREEN] {M1}
- [x] Refactor logging patterns (0.5h) [REFACTOR] {M1}
- [x] Document logging system in docs/ARCHITECTURE.md (0.5h) [DOC] {M1}
- [x] Commit: "feat(system): add logging system" (0.5h) [COMMIT] {M1}

### File I/O Utilities (12h) ✅
- [x] Write test for image file validation (0.5h) [RED] {M1}
- [x] Implement ImageUtils.is_valid_format() (0.5h) [GREEN] {M1}
- [x] Write test for image dimension extraction (0.5h) [RED] {M1}
- [x] Implement ImageUtils.get_dimensions() with PIL (1.5h) [GREEN] {M1}
- [x] Write test for image metadata extraction (0.5h) [RED] {M1}
- [x] Implement ImageUtils.get_info() (1.0h) [GREEN] {M1}
- [x] Write test for JSON save/load (0.5h) [RED] {M1}
- [x] Implement FileUtils JSON operations (1.5h) [GREEN] {M1}
- [x] Write test for file copy/move/delete (0.5h) [RED] {M1}
- [x] Implement FileUtils file operations (1.0h) [GREEN] {M1}
- [x] Write test for path security (0.5h) [RED] {M1}
- [x] Implement PathUtils with traversal protection (1.0h) [GREEN] {M1}
- [x] Refactor file I/O utilities (1.0h) [REFACTOR] {M1}
- [x] Write integration test for complete workflows (1.0h) [INT] {M1}
- [x] Document utilities in docs/ARCHITECTURE.md (0.5h) [DOC] {M1}
- [x] Commit: "feat(utils): add file I/O utilities" (0.5h) [COMMIT] {M1}

**M1 Subtotal**: 60h ✅ Complete
**Tests**: 182 passing (100% for non-GUI)
**Documentation**: ARCHITECTURE.md, M1_COMPLETION_SUMMARY.md

---

## M2: PyQt6 Image Display & Navigation
**Duration**: 2 weeks | **Total**: 80h (solo developer)
**Priority**: P0 (Critical)

### Main Window Structure (16h) ✅
- [x] Write test for MainWindow initialization (0.5h) [RED] {M2}
- [x] Implement MainWindow with QMainWindow (1.5h) [GREEN] {M2}
- [x] Write test for menu bar creation (0.5h) [RED] {M2}
- [x] Implement menu bar (File, Edit, View, Tools, Help) (2.0h) [GREEN] {M2}
- [x] Write test for toolbar creation (0.5h) [RED] {M2}
- [x] Implement toolbar with icons (2.0h) [GREEN] {M2}
- [x] Write test for status bar updates (0.5h) [RED] {M2}
- [x] Implement status bar with progress indicator (1.5h) [GREEN] {M2}
- [x] Write test for dock widget layout (0.5h) [RED] {M2}
- [x] Implement dock widgets (file list, class list, properties) (3.0h) [GREEN] {M2}
- [ ] Refactor MainWindow for better organization (1.5h) [REFACTOR] {M2}
- [ ] Write integration test for window layout (1.0h) [INT] {M2}
- [ ] Document MainWindow architecture in docs/ (1.0h) [DOC] {M2}
- [x] Commit: "feat(ui): add main window structure" (0.5h) [COMMIT] {M2}

### Image Canvas Widget (20h)
- [ ] Write test for ImageCanvas initialization (0.5h) [RED] {M2}
- [ ] Implement ImageCanvas with QGraphicsView (2.0h) [GREEN] {M2}
- [ ] Write test for QGraphicsScene setup (0.5h) [RED] {M2}
- [ ] Implement QGraphicsScene with QPixmapItem (1.5h) [GREEN] {M2}
- [ ] Write test for image loading to canvas (0.5h) [RED] {M2}
- [ ] Implement load_image() with QPixmap (1.5h) [GREEN] {M2}
- [ ] Write test for zoom in/out (0.5h) [RED] {M2}
- [ ] Implement zoom with mouse wheel (2.0h) [GREEN] {M2}
- [ ] Write test for pan functionality (0.5h) [RED] {M2}
- [ ] Implement pan with mouse drag (2.0h) [GREEN] {M2}
- [ ] Write test for fit-to-window (0.5h) [RED] {M2}
- [ ] Implement fit_to_window() method (1.0h) [GREEN] {M2}
- [ ] Write test for coordinate transformation (0.5h) [RED] {M2}
- [ ] Implement image-to-canvas coordinate mapping (1.5h) [GREEN] {M2}
- [ ] Refactor ImageCanvas for performance (2.0h) [REFACTOR] {M2}
- [ ] Write integration test for canvas interactions (1.5h) [INT] {M2}
- [ ] Document ImageCanvas API in docs/ (1.0h) [DOC] {M2}
- [ ] Commit: "feat(ui): add image canvas widget" (0.5h) [COMMIT] {M2}

### File List Widget (12h)
- [ ] Write test for FileListWidget initialization (0.5h) [RED] {M2}
- [ ] Implement FileListWidget with QListWidget (1.0h) [GREEN] {M2}
- [ ] Write test for add_image() method (0.5h) [RED] {M2}
- [ ] Implement add_image() with thumbnail (1.5h) [GREEN] {M2}
- [ ] Write test for remove_image() method (0.5h) [RED] {M2}
- [ ] Implement remove_image() (0.5h) [GREEN] {M2}
- [ ] Write test for image selection (0.5h) [RED] {M2}
- [ ] Implement selection changed signal (1.0h) [GREEN] {M2}
- [ ] Write test for drag-and-drop support (0.5h) [RED] {M2}
- [ ] Implement drag-and-drop for image import (2.0h) [GREEN] {M2}
- [ ] Write test for thumbnail caching (0.5h) [RED] {M2}
- [ ] Implement thumbnail cache with QPixmapCache (1.0h) [GREEN] {M2}
- [ ] Refactor FileListWidget for efficiency (1.0h) [REFACTOR] {M2}
- [ ] Write integration test for file operations (1.0h) [INT] {M2}
- [ ] Commit: "feat(ui): add file list widget" (0.5h) [COMMIT] {M2}

### Class List Widget (10h)
- [ ] Write test for ClassListWidget initialization (0.5h) [RED] {M2}
- [ ] Implement ClassListWidget with QListWidget (1.0h) [GREEN] {M2}
- [ ] Write test for add_class() method (0.5h) [RED] {M2}
- [ ] Implement add_class() with color picker (1.5h) [GREEN] {M2}
- [ ] Write test for remove_class() method (0.5h) [RED] {M2}
- [ ] Implement remove_class() (0.5h) [GREEN] {M2}
- [ ] Write test for edit_class() method (0.5h) [RED] {M2}
- [ ] Implement edit_class() dialog (1.5h) [GREEN] {M2}
- [ ] Write test for class color display (0.5h) [RED] {M2}
- [ ] Implement color badge rendering (1.0h) [GREEN] {M2}
- [ ] Refactor ClassListWidget for better UX (1.0h) [REFACTOR] {M2}
- [ ] Write integration test for class management (1.0h) [INT] {M2}
- [ ] Commit: "feat(ui): add class list widget" (0.5h) [COMMIT] {M2}

### Keyboard Shortcuts (10h)
- [ ] Write test for shortcut registration (0.5h) [RED] {M2}
- [ ] Implement ShortcutManager class (1.0h) [GREEN] {M2}
- [ ] Write test for navigation shortcuts (arrow keys, home, end) (0.5h) [RED] {M2}
- [ ] Implement navigation shortcuts (2.0h) [GREEN] {M2}
- [ ] Write test for zoom shortcuts (Ctrl+/-, Ctrl+0) (0.5h) [RED] {M2}
- [ ] Implement zoom shortcuts (1.0h) [GREEN] {M2}
- [ ] Write test for file shortcuts (Ctrl+O, Ctrl+S) (0.5h) [RED] {M2}
- [ ] Implement file shortcuts (1.0h) [GREEN] {M2}
- [ ] Write test for undo/redo shortcuts (Ctrl+Z, Ctrl+Y) (0.5h) [RED] {M2}
- [ ] Implement undo/redo (placeholder for M4) (1.0h) [GREEN] {M2}
- [ ] Refactor shortcut system (0.5h) [REFACTOR] {M2}
- [ ] Document shortcuts in docs/SHORTCUTS.md (1.0h) [DOC] {M2}
- [ ] Commit: "feat(ui): add keyboard shortcuts" (0.5h) [COMMIT] {M2}

### Settings Dialog (12h)
- [ ] Write test for SettingsDialog initialization (0.5h) [RED] {M2}
- [ ] Implement SettingsDialog with QDialog (1.5h) [GREEN] {M2}
- [ ] Write test for appearance settings (theme, font) (0.5h) [RED] {M2}
- [ ] Implement appearance tab (2.0h) [GREEN] {M2}
- [ ] Write test for performance settings (cache size, threads) (0.5h) [RED] {M2}
- [ ] Implement performance tab (1.5h) [GREEN] {M2}
- [ ] Write test for model settings (paths, device) (0.5h) [RED] {M2}
- [ ] Implement model tab (1.5h) [GREEN] {M2}
- [ ] Write test for settings persistence (0.5h) [RED] {M2}
- [ ] Implement settings save/load with ConfigManager (1.0h) [GREEN] {M2}
- [ ] Refactor SettingsDialog for better layout (1.0h) [REFACTOR] {M2}
- [ ] Write integration test for settings changes (1.0h) [INT] {M2}
- [ ] Commit: "feat(ui): add settings dialog" (0.5h) [COMMIT] {M2}

**M2 Subtotal**: 80h

---

## M3: Model Integration - SAM2 & Florence-2
**Duration**: 2.5 weeks | **Total**: 100h (solo developer)
**Priority**: P0 (Critical)

### Model Inference Engine Base (16h)
- [ ] Write test for ModelInferenceEngine initialization (0.5h) [RED] {M3}
- [ ] Implement ModelInferenceEngine abstract class (1.5h) [GREEN] {M3}
- [ ] Write test for model loading in QThread (0.5h) [RED] {M3}
- [ ] Implement QThread-based model loader (2.0h) [GREEN] {M3}
- [ ] Write test for progress signals (0.5h) [RED] {M3}
- [ ] Implement progress/status signals (1.0h) [GREEN] {M3}
- [ ] Write test for error handling (0.5h) [RED] {M3}
- [ ] Implement model error recovery (1.5h) [GREEN] {M3}
- [ ] Write test for device selection (CPU/GPU) (0.5h) [RED] {M3}
- [ ] Implement torch.device selection (1.0h) [GREEN] {M3}
- [ ] Write test for model caching (0.5h) [RED] {M3}
- [ ] Implement model instance caching (1.5h) [GREEN] {M3}
- [ ] Refactor ModelInferenceEngine for extensibility (2.0h) [REFACTOR] {M3}
- [ ] Write integration test for model lifecycle (1.5h) [INT] {M3}
- [ ] Document ModelInferenceEngine API in docs/ (1.0h) [DOC] {M3}
- [ ] Commit: "feat(model): add model inference engine base" (0.5h) [COMMIT] {M3}

### SAM2 Model Integration (24h)
- [ ] Write test for SAM2Model initialization (0.5h) [RED] {M3}
- [ ] Implement SAM2Model subclass (2.0h) [GREEN] {M3}
- [ ] Write test for load_checkpoint() (0.5h) [RED] {M3}
- [ ] Implement load_checkpoint() with existing ALA code (2.0h) [GREEN] {M3}
- [ ] Write test for predict_segmentation() (0.5h) [RED] {M3}
- [ ] Implement predict_segmentation() (2.5h) [GREEN] {M3}
- [ ] Write test for point prompt input (0.5h) [RED] {M3}
- [ ] Implement point prompt handling (1.5h) [GREEN] {M3}
- [ ] Write test for box prompt input (0.5h) [RED] {M3}
- [ ] Implement box prompt handling (1.5h) [GREEN] {M3}
- [ ] Write test for mask refinement (0.5h) [RED] {M3}
- [ ] Implement mask refinement with multiple prompts (2.0h) [GREEN] {M3}
- [ ] Write test for batch processing (0.5h) [RED] {M3}
- [ ] Implement batch predict for multiple images (2.5h) [GREEN] {M3}
- [ ] Write test for mask post-processing (0.5h) [RED] {M3}
- [ ] Implement mask smoothing and cleanup (1.5h) [GREEN] {M3}
- [ ] Refactor SAM2Model for performance (2.0h) [REFACTOR] {M3}
- [ ] Write integration test for SAM2 pipeline (2.0h) [INT] {M3}
- [ ] Document SAM2 usage in docs/SAM2.md (1.0h) [DOC] {M3}
- [ ] Commit: "feat(model): integrate SAM2 model" (0.5h) [COMMIT] {M3}

### Florence-2 Model Integration (20h)
- [ ] Write test for Florence2Model initialization (0.5h) [RED] {M3}
- [ ] Implement Florence2Model subclass (2.0h) [GREEN] {M3}
- [ ] Write test for load_checkpoint() (0.5h) [RED] {M3}
- [ ] Implement load_checkpoint() with existing ALA code (2.0h) [GREEN] {M3}
- [ ] Write test for detect_objects() (0.5h) [RED] {M3}
- [ ] Implement detect_objects() with text prompt (2.5h) [GREEN] {M3}
- [ ] Write test for caption generation (0.5h) [RED] {M3}
- [ ] Implement generate_caption() (1.5h) [GREEN] {M3}
- [ ] Write test for grounded detection (0.5h) [RED] {M3}
- [ ] Implement grounded_detection() with phrases (2.0h) [GREEN] {M3}
- [ ] Write test for bbox → mask conversion (0.5h) [RED] {M3}
- [ ] Implement bbox_to_mask() integration with SAM2 (2.0h) [GREEN] {M3}
- [ ] Write test for batch processing (0.5h) [RED] {M3}
- [ ] Implement batch predict for multiple images (2.0h) [GREEN] {M3}
- [ ] Refactor Florence2Model for clarity (1.5h) [REFACTOR] {M3}
- [ ] Write integration test for Florence-2 pipeline (1.5h) [INT] {M3}
- [ ] Document Florence-2 usage in docs/FLORENCE2.md (1.0h) [DOC] {M3}
- [ ] Commit: "feat(model): integrate Florence-2 model" (0.5h) [COMMIT] {M3}

### Model Controller (20h)
- [ ] Write test for ModelController initialization (0.5h) [RED] {M3}
- [ ] Implement ModelController class (1.5h) [GREEN] {M3}
- [ ] Write test for run_autodistill() method (0.5h) [RED] {M3}
- [ ] Implement run_autodistill() with Florence-2 + SAM2 (3.0h) [GREEN] {M3}
- [ ] Write test for progress callback (0.5h) [RED] {M3}
- [ ] Implement progress callback with signals (1.0h) [GREEN] {M3}
- [ ] Write test for cancellation support (0.5h) [RED] {M3}
- [ ] Implement cancel_inference() (1.5h) [GREEN] {M3}
- [ ] Write test for result caching (0.5h) [RED] {M3}
- [ ] Implement prediction result caching (2.0h) [GREEN] {M3}
- [ ] Write test for error recovery (0.5h) [RED] {M3}
- [ ] Implement retry logic and error dialogs (1.5h) [GREEN] {M3}
- [ ] Write test for model switching (0.5h) [RED] {M3}
- [ ] Implement switch_model() method (1.0h) [GREEN] {M3}
- [ ] Refactor ModelController for better separation (2.0h) [REFACTOR] {M3}
- [ ] Write integration test for full autodistill workflow (2.0h) [INT] {M3}
- [ ] Document ModelController API in docs/ (1.0h) [DOC] {M3}
- [ ] Commit: "feat(model): add model controller" (0.5h) [COMMIT] {M3}

### UI Integration (20h)
- [ ] Write test for AutoAnnotateDialog initialization (0.5h) [RED] {M3}
- [ ] Implement AutoAnnotateDialog with text prompt input (2.0h) [GREEN] {M3}
- [ ] Write test for progress bar updates (0.5h) [RED] {M3}
- [ ] Implement progress bar with QProgressBar (1.0h) [GREEN] {M3}
- [ ] Write test for model selection dropdown (0.5h) [RED] {M3}
- [ ] Implement model selection UI (1.5h) [GREEN] {M3}
- [ ] Write test for annotation overlay display (0.5h) [RED] {M3}
- [ ] Implement annotation overlay on ImageCanvas (3.0h) [GREEN] {M3}
- [ ] Write test for batch processing UI (0.5h) [RED] {M3}
- [ ] Implement batch process dialog (2.0h) [GREEN] {M3}
- [ ] Write test for result acceptance/rejection (0.5h) [RED] {M3}
- [ ] Implement accept/reject buttons with preview (1.5h) [GREEN] {M3}
- [ ] Write test for annotation export (0.5h) [RED] {M3}
- [ ] Implement export annotations to COCO/YOLO (2.0h) [GREEN] {M3}
- [ ] Refactor UI integration for better UX (2.0h) [REFACTOR] {M3}
- [ ] Write E2E test for auto-annotation workflow (2.0h) [E2E] {M3}
- [ ] Document model UI in docs/MODEL_UI.md (1.0h) [DOC] {M3}
- [ ] Commit: "feat(ui): integrate model UI" (0.5h) [COMMIT] {M3}

**M3 Subtotal**: 100h

---

## M4: Annotation Tools & Manual Editing
**Duration**: 2 weeks | **Total**: 80h (solo developer)
**Priority**: P0 (Critical)

### Drawing Tools (24h)
- [ ] Write test for PolygonTool initialization (0.5h) [RED] {M4}
- [ ] Implement PolygonTool with mouse events (2.5h) [GREEN] {M4}
- [ ] Write test for BoxTool (0.5h) [RED] {M4}
- [ ] Implement BoxTool with drag-to-draw (2.0h) [GREEN] {M4}
- [ ] Write test for PointTool (0.5h) [RED] {M4}
- [ ] Implement PointTool for SAM2 prompts (1.5h) [GREEN] {M4}
- [ ] Write test for PencilTool (freehand) (0.5h) [RED] {M4}
- [ ] Implement PencilTool with smooth curves (2.0h) [GREEN] {M4}
- [ ] Write test for EraserTool (0.5h) [RED] {M4}
- [ ] Implement EraserTool for mask editing (1.5h) [GREEN] {M4}
- [ ] Write test for SelectTool (0.5h) [RED] {M4}
- [ ] Implement SelectTool for annotation selection (2.0h) [GREEN] {M4}
- [ ] Write test for tool switching (0.5h) [RED] {M4}
- [ ] Implement tool manager with toolbar (1.5h) [GREEN] {M4}
- [ ] Write test for tool cursors (0.5h) [RED] {M4}
- [ ] Implement custom cursors for each tool (1.5h) [GREEN] {M4}
- [ ] Refactor drawing tools for consistency (2.0h) [REFACTOR] {M4}
- [ ] Write integration test for all drawing tools (2.0h) [INT] {M4}
- [ ] Document drawing tools in docs/DRAWING_TOOLS.md (1.0h) [DOC] {M4}
- [ ] Commit: "feat(annotation): add drawing tools" (0.5h) [COMMIT] {M4}

### Annotation Manager (20h)
- [ ] Write test for AnnotationManager initialization (0.5h) [RED] {M4}
- [ ] Implement AnnotationManager class (1.5h) [GREEN] {M4}
- [ ] Write test for add_annotation() (0.5h) [RED] {M4}
- [ ] Implement add_annotation() with validation (1.5h) [GREEN] {M4}
- [ ] Write test for update_annotation() (0.5h) [RED] {M4}
- [ ] Implement update_annotation() (1.0h) [GREEN] {M4}
- [ ] Write test for delete_annotation() (0.5h) [RED] {M4}
- [ ] Implement delete_annotation() (1.0h) [GREEN] {M4}
- [ ] Write test for get_annotations_for_image() (0.5h) [RED] {M4}
- [ ] Implement query methods (1.0h) [GREEN] {M4}
- [ ] Write test for annotation z-ordering (0.5h) [RED] {M4}
- [ ] Implement z-order management (1.5h) [GREEN] {M4}
- [ ] Write test for annotation filtering by class (0.5h) [RED] {M4}
- [ ] Implement filter_by_class() (1.0h) [GREEN] {M4}
- [ ] Write test for annotation statistics (0.5h) [RED] {M4}
- [ ] Implement get_statistics() (1.0h) [GREEN] {M4}
- [ ] Refactor AnnotationManager for performance (2.0h) [REFACTOR] {M4}
- [ ] Write integration test for annotation lifecycle (2.0h) [INT] {M4}
- [ ] Document AnnotationManager API in docs/ (1.0h) [DOC] {M4}
- [ ] Commit: "feat(annotation): add annotation manager" (0.5h) [COMMIT] {M4}

### Edit Tools (16h)
- [ ] Write test for MoveAnnotationTool (0.5h) [RED] {M4}
- [ ] Implement MoveAnnotationTool with drag (2.0h) [GREEN] {M4}
- [ ] Write test for ResizeAnnotationTool (0.5h) [RED] {M4}
- [ ] Implement ResizeAnnotationTool with handles (2.5h) [GREEN] {M4}
- [ ] Write test for RotateAnnotationTool (0.5h) [RED] {M4}
- [ ] Implement RotateAnnotationTool (2.0h) [GREEN] {M4}
- [ ] Write test for EditVertexTool (polygon editing) (0.5h) [RED] {M4}
- [ ] Implement EditVertexTool with vertex drag (2.5h) [GREEN] {M4}
- [ ] Write test for AddVertexTool (0.5h) [RED] {M4}
- [ ] Implement AddVertexTool (1.5h) [GREEN] {M4}
- [ ] Write test for DeleteVertexTool (0.5h) [RED] {M4}
- [ ] Implement DeleteVertexTool (1.0h) [GREEN] {M4}
- [ ] Refactor edit tools for better UX (1.5h) [REFACTOR] {M4}
- [ ] Write integration test for editing workflows (1.5h) [INT] {M4}
- [ ] Commit: "feat(annotation): add edit tools" (0.5h) [COMMIT] {M4}

### Undo/Redo System (12h)
- [ ] Write test for UndoStack initialization (0.5h) [RED] {M4}
- [ ] Implement UndoStack with QUndoStack (1.5h) [GREEN] {M4}
- [ ] Write test for AddAnnotationCommand (0.5h) [RED] {M4}
- [ ] Implement AddAnnotationCommand with undo/redo (1.5h) [GREEN] {M4}
- [ ] Write test for DeleteAnnotationCommand (0.5h) [RED] {M4}
- [ ] Implement DeleteAnnotationCommand (1.0h) [GREEN] {M4}
- [ ] Write test for EditAnnotationCommand (0.5h) [RED] {M4}
- [ ] Implement EditAnnotationCommand (1.5h) [GREEN] {M4}
- [ ] Write test for undo/redo actions (0.5h) [RED] {M4}
- [ ] Implement undo/redo menu actions (1.0h) [GREEN] {M4}
- [ ] Write test for command history limit (0.5h) [RED] {M4}
- [ ] Implement history limit with cleanup (1.0h) [GREEN] {M4}
- [ ] Refactor command pattern for extensibility (1.0h) [REFACTOR] {M4}
- [ ] Write integration test for undo/redo chain (1.0h) [INT] {M4}
- [ ] Commit: "feat(annotation): add undo/redo system" (0.5h) [COMMIT] {M4}

### Properties Panel (8h)
- [ ] Write test for PropertiesPanel initialization (0.5h) [RED] {M4}
- [ ] Implement PropertiesPanel with QDockWidget (1.5h) [GREEN] {M4}
- [ ] Write test for annotation property display (0.5h) [RED] {M4}
- [ ] Implement property display (class, confidence, geometry) (1.5h) [GREEN] {M4}
- [ ] Write test for property editing (0.5h) [RED] {M4}
- [ ] Implement property editors (QSpinBox, QComboBox, etc.) (2.0h) [GREEN] {M4}
- [ ] Write test for property updates (0.5h) [RED] {M4}
- [ ] Implement property update propagation (1.0h) [GREEN] {M4}
- [ ] Refactor PropertiesPanel for better layout (0.5h) [REFACTOR] {M4}
- [ ] Commit: "feat(ui): add properties panel" (0.5h) [COMMIT] {M4}

**M4 Subtotal**: 80h

---

## M5: Web Integration - Few-Shot Learning
**Duration**: 2 weeks | **Total**: 80h (solo developer)
**Priority**: P1

### QWebEngineView Integration (16h)
- [ ] Write test for WebInterfaceWidget initialization (0.5h) [RED] {M5}
- [ ] Implement WebInterfaceWidget with QWebEngineView (2.0h) [GREEN] {M5}
- [ ] Write test for load_url() (0.5h) [RED] {M5}
- [ ] Implement load_url() with local Gradio server (1.5h) [GREEN] {M5}
- [ ] Write test for JavaScript bridge (0.5h) [RED] {M5}
- [ ] Implement QWebChannel for JS communication (2.5h) [GREEN] {M5}
- [ ] Write test for page load error handling (0.5h) [RED] {M5}
- [ ] Implement error handling and retry logic (1.5h) [GREEN] {M5}
- [ ] Write test for navigation blocking (0.5h) [RED] {M5}
- [ ] Implement navigation policy to prevent external links (1.0h) [GREEN] {M5}
- [ ] Write test for console message logging (0.5h) [RED] {M5}
- [ ] Implement console message capture (1.0h) [GREEN] {M5}
- [ ] Refactor WebInterfaceWidget for better isolation (2.0h) [REFACTOR] {M5}
- [ ] Write integration test for web widget (1.5h) [INT] {M5}
- [ ] Commit: "feat(web): add QWebEngineView integration" (0.5h) [COMMIT] {M5}

### Gradio Server Wrapper (20h)
- [ ] Write test for GradioServerWrapper initialization (0.5h) [RED] {M5}
- [ ] Implement GradioServerWrapper with subprocess (2.0h) [GREEN] {M5}
- [ ] Write test for start_server() (0.5h) [RED] {M5}
- [ ] Implement start_server() with port detection (2.5h) [GREEN] {M5}
- [ ] Write test for stop_server() (0.5h) [RED] {M5}
- [ ] Implement stop_server() with graceful shutdown (1.5h) [GREEN] {M5}
- [ ] Write test for server health check (0.5h) [RED] {M5}
- [ ] Implement is_alive() with HTTP ping (1.5h) [GREEN] {M5}
- [ ] Write test for server restart (0.5h) [RED] {M5}
- [ ] Implement restart_server() (1.0h) [GREEN] {M5}
- [ ] Write test for port conflict handling (0.5h) [RED] {M5}
- [ ] Implement auto-port selection (1.5h) [GREEN] {M5}
- [ ] Write test for server logs (0.5h) [RED] {M5}
- [ ] Implement log capture and display (2.0h) [GREEN] {M5}
- [ ] Refactor GradioServerWrapper for robustness (2.0h) [REFACTOR] {M5}
- [ ] Write integration test for server lifecycle (2.0h) [INT] {M5}
- [ ] Document Gradio integration in docs/GRADIO.md (1.0h) [DOC] {M5}
- [ ] Commit: "feat(web): add Gradio server wrapper" (0.5h) [COMMIT] {M5}

### Gradio Interface Adaptation (16h)
- [ ] Copy existing ALA Gradio code to new location (0.5h) [SETUP] {M5}
- [ ] Write test for support_set_upload() (0.5h) [RED] {M5}
- [ ] Adapt support_set_upload() for desktop integration (2.0h) [GREEN] {M5}
- [ ] Write test for query_image_upload() (0.5h) [RED] {M5}
- [ ] Adapt query_image_upload() (1.5h) [GREEN] {M5}
- [ ] Write test for run_classification() (0.5h) [RED] {M5}
- [ ] Adapt run_classification() with existing models (2.5h) [GREEN] {M5}
- [ ] Write test for result export (0.5h) [RED] {M5}
- [ ] Implement export_results() to desktop (2.0h) [GREEN] {M5}
- [ ] Write test for model selection UI (0.5h) [RED] {M5}
- [ ] Implement model dropdown (ResNet, CLIP, DINOv2) (1.5h) [GREEN] {M5}
- [ ] Refactor Gradio interface for desktop context (2.0h) [REFACTOR] {M5}
- [ ] Write integration test for full Gradio workflow (1.5h) [INT] {M5}
- [ ] Document Gradio interface in docs/ (1.0h) [DOC] {M5}
- [ ] Commit: "feat(web): adapt Gradio interface" (0.5h) [COMMIT] {M5}

### Desktop-Web Communication (16h)
- [ ] Write test for WebInterfaceController initialization (0.5h) [RED] {M5}
- [ ] Implement WebInterfaceController class (1.5h) [GREEN] {M5}
- [ ] Write test for send_images_to_web() (0.5h) [RED] {M5}
- [ ] Implement send_images_to_web() via REST API (2.5h) [GREEN] {M5}
- [ ] Write test for receive_results_from_web() (0.5h) [RED] {M5}
- [ ] Implement receive_results_from_web() (2.0h) [GREEN] {M5}
- [ ] Write test for sync_support_set() (0.5h) [RED] {M5}
- [ ] Implement sync_support_set() (1.5h) [GREEN] {M5}
- [ ] Write test for sync_classes() (0.5h) [RED] {M5}
- [ ] Implement sync_classes() (1.5h) [GREEN] {M5}
- [ ] Write test for error handling (0.5h) [RED] {M5}
- [ ] Implement communication error recovery (1.5h) [GREEN] {M5}
- [ ] Refactor communication layer for reliability (1.5h) [REFACTOR] {M5}
- [ ] Write integration test for full desktop-web sync (2.0h) [INT] {M5}
- [ ] Document communication protocol in docs/COMMUNICATION.md (1.0h) [DOC] {M5}
- [ ] Commit: "feat(web): add desktop-web communication" (0.5h) [COMMIT] {M5}

### Few-Shot UI Integration (12h)
- [ ] Write test for FewShotDialog initialization (0.5h) [RED] {M5}
- [ ] Implement FewShotDialog with embedded web view (2.0h) [GREEN] {M5}
- [ ] Write test for support set selection (0.5h) [RED] {M5}
- [ ] Implement support set file browser (1.5h) [GREEN] {M5}
- [ ] Write test for model selection (0.5h) [RED] {M5}
- [ ] Implement model selection dropdown (1.0h) [GREEN] {M5}
- [ ] Write test for result import (0.5h) [RED] {M5}
- [ ] Implement import results to AnnotationManager (2.0h) [GREEN] {M5}
- [ ] Write test for progress display (0.5h) [RED] {M5}
- [ ] Implement progress bar for classification (1.0h) [GREEN] {M5}
- [ ] Refactor FewShotDialog for better UX (1.5h) [REFACTOR] {M5}
- [ ] Write E2E test for Few-Shot workflow (2.0h) [E2E] {M5}
- [ ] Commit: "feat(ui): integrate Few-Shot UI" (0.5h) [COMMIT] {M5}

**M5 Subtotal**: 80h

---

## M6: Pipeline Integration - Ground Truth & YOLO
**Duration**: 2 weeks | **Total**: 80h (solo developer)
**Priority**: P1

### Ground Truth Labeling Tool (20h)
- [ ] Write test for GroundTruthDialog initialization (0.5h) [RED] {M6}
- [ ] Implement GroundTruthDialog (2.0h) [GREEN] {M6}
- [ ] Write test for accept/reject annotation (0.5h) [RED] {M6}
- [ ] Implement accept/reject buttons (1.5h) [GREEN] {M6}
- [ ] Write test for annotation correction (0.5h) [RED] {M6}
- [ ] Implement correction mode with drawing tools (2.5h) [GREEN] {M6}
- [ ] Write test for batch review (0.5h) [RED] {M6}
- [ ] Implement batch review UI (2.0h) [GREEN] {M6}
- [ ] Write test for confidence threshold filter (0.5h) [RED] {M6}
- [ ] Implement confidence slider (1.0h) [GREEN] {M6}
- [ ] Write test for statistics display (0.5h) [RED] {M6}
- [ ] Implement stats panel (accepted/rejected counts) (1.5h) [GREEN] {M6}
- [ ] Write test for export to ground truth format (0.5h) [RED] {M6}
- [ ] Implement export_ground_truth() (2.0h) [GREEN] {M6}
- [ ] Refactor GroundTruthDialog for efficiency (2.0h) [REFACTOR] {M6}
- [ ] Write integration test for ground truth workflow (2.0h) [INT] {M6}
- [ ] Document ground truth process in docs/GROUND_TRUTH.md (1.0h) [DOC] {M6}
- [ ] Commit: "feat(pipeline): add ground truth labeling" (0.5h) [COMMIT] {M6}

### YOLO Dataset Generator (20h)
- [ ] Write test for YoloDatasetGenerator initialization (0.5h) [RED] {M6}
- [ ] Implement YoloDatasetGenerator class (1.5h) [GREEN] {M6}
- [ ] Write test for create_yolo_dataset() (0.5h) [RED] {M6}
- [ ] Implement create_yolo_dataset() with train/val split (2.5h) [GREEN] {M6}
- [ ] Write test for annotation format conversion (0.5h) [RED] {M6}
- [ ] Implement annotation_to_yolo_format() (2.0h) [GREEN] {M6}
- [ ] Write test for data.yaml generation (0.5h) [RED] {M6}
- [ ] Implement generate_data_yaml() (1.5h) [GREEN] {M6}
- [ ] Write test for train/val split strategies (0.5h) [RED] {M6}
- [ ] Implement split strategies (random, stratified) (2.0h) [GREEN] {M6}
- [ ] Write test for image copying/linking (0.5h) [RED] {M6}
- [ ] Implement copy_images() with symlink option (1.5h) [GREEN] {M6}
- [ ] Write test for augmentation config (0.5h) [RED] {M6}
- [ ] Implement augmentation configuration (1.5h) [GREEN] {M6}
- [ ] Refactor YoloDatasetGenerator for flexibility (2.0h) [REFACTOR] {M6}
- [ ] Write integration test for dataset generation (2.0h) [INT] {M6}
- [ ] Document YOLO dataset format in docs/YOLO_DATASET.md (1.0h) [DOC] {M6}
- [ ] Commit: "feat(pipeline): add YOLO dataset generator" (0.5h) [COMMIT] {M6}

### YOLO Training Integration (24h)
- [ ] Write test for YoloTrainer initialization (0.5h) [RED] {M6}
- [ ] Implement YoloTrainer wrapper (2.0h) [GREEN] {M6}
- [ ] Write test for train_model() (0.5h) [RED] {M6}
- [ ] Implement train_model() with ultralytics (3.0h) [GREEN] {M6}
- [ ] Write test for training progress callback (0.5h) [RED] {M6}
- [ ] Implement progress signals (2.0h) [GREEN] {M6}
- [ ] Write test for training cancellation (0.5h) [RED] {M6}
- [ ] Implement cancel_training() (1.5h) [GREEN] {M6}
- [ ] Write test for hyperparameter configuration (0.5h) [RED] {M6}
- [ ] Implement hyperparam UI (epochs, batch, lr) (2.5h) [GREEN] {M6}
- [ ] Write test for training validation (0.5h) [RED] {M6}
- [ ] Implement validation metrics display (2.0h) [GREEN] {M6}
- [ ] Write test for model checkpoint saving (0.5h) [RED] {M6}
- [ ] Implement checkpoint management (2.0h) [GREEN] {M6}
- [ ] Write test for TensorBoard integration (0.5h) [RED] {M6}
- [ ] Implement TensorBoard logging (2.0h) [GREEN] {M6}
- [ ] Refactor YoloTrainer for robustness (2.0h) [REFACTOR] {M6}
- [ ] Write integration test for training pipeline (2.0h) [INT] {M6}
- [ ] Document YOLO training in docs/YOLO_TRAINING.md (1.0h) [DOC] {M6}
- [ ] Commit: "feat(pipeline): integrate YOLO training" (0.5h) [COMMIT] {M6}

### Pipeline UI (16h)
- [ ] Write test for PipelineDialog initialization (0.5h) [RED] {M6}
- [ ] Implement PipelineDialog with stage tabs (2.0h) [GREEN] {M6}
- [ ] Write test for stage navigation (0.5h) [RED] {M6}
- [ ] Implement stage navigation (Annotation → Few-Shot → Ground Truth → YOLO) (1.5h) [GREEN] {M6}
- [ ] Write test for stage progress tracking (0.5h) [RED] {M6}
- [ ] Implement progress indicators per stage (1.5h) [GREEN] {M6}
- [ ] Write test for "Run All" pipeline (0.5h) [RED] {M6}
- [ ] Implement run_all_pipeline() automation (3.0h) [GREEN] {M6}
- [ ] Write test for pipeline state persistence (0.5h) [RED] {M6}
- [ ] Implement save/load pipeline state (2.0h) [GREEN] {M6}
- [ ] Write test for pipeline configuration (0.5h) [RED] {M6}
- [ ] Implement pipeline config dialog (1.5h) [GREEN] {M6}
- [ ] Refactor PipelineDialog for clarity (1.5h) [REFACTOR] {M6}
- [ ] Write E2E test for complete pipeline (2.0h) [E2E] {M6}
- [ ] Document pipeline in docs/PIPELINE.md (1.0h) [DOC] {M6}
- [ ] Commit: "feat(pipeline): add pipeline UI" (0.5h) [COMMIT] {M6}

**M6 Subtotal**: 80h

---

## M7: Polish & User Experience
**Duration**: 1.5 weeks | **Total**: 60h (solo developer)
**Priority**: P1

### Theme System (16h)
- [ ] Write test for ThemeManager initialization (0.5h) [RED] {M7}
- [ ] Implement ThemeManager with QSS (2.0h) [GREEN] {M7}
- [ ] Write test for theme switching (0.5h) [RED] {M7}
- [ ] Implement switch_theme() (Light/Dark) (2.0h) [GREEN] {M7}
- [ ] Write test for custom color schemes (0.5h) [RED] {M7}
- [ ] Implement custom color scheme editor (2.5h) [GREEN] {M7}
- [ ] Create light theme QSS (2.0h) [GREEN] {M7}
- [ ] Create dark theme QSS (2.0h) [GREEN] {M7}
- [ ] Write test for theme persistence (0.5h) [RED] {M7}
- [ ] Implement theme save/load with ConfigManager (1.0h) [GREEN] {M7}
- [ ] Write test for icon adaptation (0.5h) [RED] {M7}
- [ ] Implement icon switching for themes (1.5h) [GREEN] {M7}
- [ ] Refactor ThemeManager for extensibility (1.0h) [REFACTOR] {M7}
- [ ] Document theming system in docs/THEMING.md (1.0h) [DOC] {M7}
- [ ] Commit: "feat(ui): add theme system" (0.5h) [COMMIT] {M7}

### Icon Set (8h)
- [ ] Design/source icons for toolbar (3.0h) [SETUP] {M7}
- [ ] Design/source icons for menu (2.0h) [SETUP] {M7}
- [ ] Create icon resources file (icons.qrc) (1.0h) [SETUP] {M7}
- [ ] Compile resources with pyrcc6 (0.5h) [SETUP] {M7}
- [ ] Apply icons to all UI elements (3.0h) [GREEN] {M7}
- [ ] Test icon rendering at different DPIs (1.0h) [INT] {M7}
- [ ] Document icon usage in docs/ICONS.md (0.5h) [DOC] {M7}
- [ ] Commit: "feat(ui): add icon set" (0.5h) [COMMIT] {M7}

### Internationalization (12h)
- [ ] Write test for TranslationManager (0.5h) [RED] {M7}
- [ ] Implement TranslationManager with QTranslator (1.5h) [GREEN] {M7}
- [ ] Extract translatable strings with pylupdate6 (2.0h) [SETUP] {M7}
- [ ] Create en_US.ts translation file (1.0h) [SETUP] {M7}
- [ ] Create ko_KR.ts translation file (3.0h) [SETUP] {M7}
- [ ] Compile translations with lrelease (0.5h) [SETUP] {M7}
- [ ] Write test for language switching (0.5h) [RED] {M7}
- [ ] Implement switch_language() (1.0h) [GREEN] {M7}
- [ ] Test translations in UI (1.0h) [INT] {M7}
- [ ] Document i18n in docs/INTERNATIONALIZATION.md (1.0h) [DOC] {M7}
- [ ] Commit: "feat(i18n): add internationalization" (0.5h) [COMMIT] {M7}

### Help System (10h)
- [ ] Write test for HelpDialog (0.5h) [RED] {M7}
- [ ] Implement HelpDialog with QTextBrowser (1.5h) [GREEN] {M7}
- [ ] Create user manual HTML (4.0h) [DOC] {M7}
- [ ] Create keyboard shortcuts reference (1.0h) [DOC] {M7}
- [ ] Write test for context-sensitive help (0.5h) [RED] {M7}
- [ ] Implement F1 context help (1.0h) [GREEN] {M7}
- [ ] Write test for tutorial system (0.5h) [RED] {M7}
- [ ] Implement interactive tutorial (2.0h) [GREEN] {M7}
- [ ] Test help system navigation (0.5h) [INT] {M7}
- [ ] Commit: "feat(help): add help system" (0.5h) [COMMIT] {M7}

### Performance Optimization (14h)
- [ ] Profile image loading performance (1.0h) [PERF] {M7}
- [ ] Optimize image loading with caching (2.0h) [GREEN] {M7}
- [ ] Profile annotation rendering (1.0h) [PERF] {M7}
- [ ] Optimize annotation overlay with GPU (2.0h) [GREEN] {M7}
- [ ] Profile file list widget (1.0h) [PERF] {M7}
- [ ] Optimize thumbnail generation (1.5h) [GREEN] {M7}
- [ ] Profile memory usage (1.0h) [PERF] {M7}
- [ ] Optimize memory usage with lazy loading (2.0h) [GREEN] {M7}
- [ ] Run performance benchmarks (1.0h) [PERF] {M7}
- [ ] Document performance optimizations in docs/PERFORMANCE.md (1.0h) [DOC] {M7}
- [ ] Commit: "perf: optimize performance" (0.5h) [COMMIT] {M7}

**M7 Subtotal**: 60h

---

## M8: Deployment & Distribution
**Duration**: 1 week | **Total**: 40h (solo developer)
**Priority**: P2

### Packaging (16h)
- [ ] Install PyInstaller (0.5h) [SETUP] {M8}
- [ ] Create PyInstaller spec file (2.0h) [SETUP] {M8}
- [ ] Configure hidden imports and data files (2.0h) [SETUP] {M8}
- [ ] Build Windows executable (1.0h) [SETUP] {M8}
- [ ] Test Windows executable (2.0h) [INT] {M8}
- [ ] Create installer with NSIS (3.0h) [SETUP] {M8}
- [ ] Add application icon and metadata (1.0h) [SETUP] {M8}
- [ ] Test installer on clean Windows system (2.0h) [INT] {M8}
- [ ] Create uninstaller (1.0h) [SETUP] {M8}
- [ ] Test uninstaller (0.5h) [INT] {M8}
- [ ] Document packaging process in docs/PACKAGING.md (1.0h) [DOC] {M8}
- [ ] Commit: "build: add Windows packaging" (0.5h) [COMMIT] {M8}

### Distribution (8h)
- [ ] Create release notes template (1.0h) [DOC] {M8}
- [ ] Write v1.0 release notes (2.0h) [DOC] {M8}
- [ ] Create GitHub release (1.0h) [SETUP] {M8}
- [ ] Upload Windows installer to GitHub (0.5h) [SETUP] {M8}
- [ ] Create download instructions (1.0h) [DOC] {M8}
- [ ] Test download and installation flow (1.5h) [INT] {M8}
- [ ] Create release announcement (1.0h) [DOC] {M8}
- [ ] Commit: "docs: add v1.0 release notes" (0.5h) [COMMIT] {M8}

### Documentation Finalization (10h)
- [ ] Review and update README.md (1.0h) [DOC] {M8}
- [ ] Review and update installation guide (1.0h) [DOC] {M8}
- [ ] Create user guide PDF (2.0h) [DOC] {M8}
- [ ] Create developer guide (2.0h) [DOC] {M8}
- [ ] Create API documentation with Sphinx (2.0h) [DOC] {M8}
- [ ] Create video tutorial outline (1.0h) [DOC] {M8}
- [ ] Review all documentation for consistency (1.0h) [DOC] {M8}
- [ ] Commit: "docs: finalize v1.0 documentation" (0.5h) [COMMIT] {M8}

### Testing & QA (6h)
- [ ] Run full E2E test suite (1.0h) [E2E] {M8}
- [ ] Manual exploratory testing (2.0h) [INT] {M8}
- [ ] Fix critical bugs found (2.0h) [GREEN] {M8}
- [ ] Verify all quality gates (0.5h) [INT] {M8}
- [ ] Final code review (0.5h) [INT] {M8}
- [ ] Commit: "fix: resolve critical bugs" (0.5h) [COMMIT] {M8}

**M8 Subtotal**: 40h

---

## Summary by Milestone

| Milestone | Tasks | Est. Hours | Duration | Priority | Status |
|-----------|-------|------------|----------|----------|--------|
| M0: Project Setup | 40 | 40h | 1 week | P1 | Pending |
| M1: Foundation & Core Infrastructure | 72 | 60h | 1.5 weeks | P0 | Pending |
| M2: PyQt6 Image Display & Navigation | 80 | 80h | 2 weeks | P0 | Pending |
| M3: Model Integration - SAM2 & Florence-2 | 100 | 100h | 2.5 weeks | P0 | Pending |
| M4: Annotation Tools & Manual Editing | 80 | 80h | 2 weeks | P0 | Pending |
| M5: Web Integration - Few-Shot Learning | 80 | 80h | 2 weeks | P1 | Pending |
| M6: Pipeline Integration - Ground Truth & YOLO | 80 | 80h | 2 weeks | P1 | Pending |
| M7: Polish & User Experience | 60 | 60h | 1.5 weeks | P1 | Pending |
| M8: Deployment & Distribution | 40 | 40h | 1 week | P2 | Pending |
| **Total** | **412** | **580h** | **15 weeks** | - | - |

**Buffer**: 5 weeks (33% buffer)
**Total with Buffer**: 20 weeks

---

## Task Breakdown by Category

| Category | Count | Hours | Percentage | Purpose |
|----------|-------|-------|------------|---------|
| [RED] | 165 | 82.5h | 14.2% | Write failing tests |
| [GREEN] | 180 | 252.5h | 43.5% | Implement code to pass tests |
| [REFACTOR] | 28 | 42.0h | 7.2% | Improve code structure |
| [COMMIT] | 38 | 19.0h | 3.3% | Git commits |
| [INT] | 35 | 52.5h | 9.1% | Integration tests |
| [E2E] | 5 | 10.0h | 1.7% | End-to-end tests |
| [DOC] | 45 | 56.5h | 9.7% | Documentation |
| [SETUP] | 39 | 59.0h | 10.2% | Setup/configuration |
| [PERF] | 6 | 6.0h | 1.0% | Performance tests |
| **Total** | **412** | **580h** | **100%** | |

**TDD Compliance Metrics**:
- Test tasks ([RED] + [INT] + [E2E] + [PERF]): 211 tasks (51.2%)
- Implementation tasks ([GREEN]): 180 tasks (43.7%)
- Test:Implementation ratio: 1.17:1 ✅ (target: ≥1:1.5)

---

## Execution Order & Dependencies

### Week 1: Project Setup (M0)
- **Focus**: Development environment, testing infrastructure, CI/CD
- **Deliverables**: Ready-to-develop environment with all tools configured

### Weeks 2-3.5: Foundation (M1)
- **Focus**: Core infrastructure, data models, utilities
- **Deliverables**: Solid foundation for GUI development

### Weeks 4-5: Image Display (M2)
- **Focus**: PyQt6 main window, image canvas, navigation
- **Deliverables**: Working image viewer with basic UI

### Weeks 6-8.5: Model Integration (M3)
- **Focus**: SAM2, Florence-2, auto-annotation
- **Deliverables**: Functional auto-annotation system

### Weeks 9-10: Annotation Tools (M4)
- **Focus**: Drawing tools, editing, undo/redo
- **Deliverables**: Complete manual annotation toolkit

### Weeks 11-12: Web Integration (M5)
- **Focus**: Gradio integration, Few-Shot learning
- **Deliverables**: Working Few-Shot classification in GUI

### Weeks 13-14: Pipeline Integration (M6)
- **Focus**: Ground truth, YOLO training
- **Deliverables**: Complete ALA pipeline in GUI

### Weeks 14.5-16: Polish (M7)
- **Focus**: Themes, i18n, help, performance
- **Deliverables**: Polished, user-friendly application

### Week 17: Deployment (M8)
- **Focus**: Packaging, distribution, documentation
- **Deliverables**: Release-ready v1.0

**Total Timeline**: 15 weeks + 5 weeks buffer = 20 weeks

---

## Risk Management

### High-Risk Tasks

**PyQt6 Learning Curve**:
- Risk: Solo developer learning PyQt6 from scratch
- Mitigation: Reference X-AnyLabeling, labelme code extensively; allocate extra time in M2
- Buffer: Built into M2 time estimates

**Model Integration Complexity**:
- Risk: Existing ALA model code may not integrate smoothly
- Mitigation: Thorough testing in M3; QThread isolation; fallback to CLI execution
- Buffer: 2.5 weeks for M3 (longest milestone)

**QWebEngineView Stability**:
- Risk: Desktop-web communication may be unreliable
- Mitigation: Robust error handling; server health checks; restart mechanisms
- Buffer: Extra time in M5 for debugging

**Performance Issues**:
- Risk: Large images or many annotations may slow down UI
- Mitigation: Lazy loading; thumbnail caching; GPU acceleration in M7
- Buffer: Dedicated performance optimization milestone (M7)

---

## Quality Assurance

### Per-Task Quality Gates

Before marking any task complete:
- [ ] Test passes (for [RED] tasks)
- [ ] Implementation passes test (for [GREEN] tasks)
- [ ] All tests still pass (for [REFACTOR] tasks)
- [ ] Commit message follows conventional commits (for [COMMIT] tasks)
- [ ] Documentation clear and complete (for [DOC] tasks)
- [ ] Code formatted with black
- [ ] No linting errors (flake8, mypy)

### Milestone Quality Gates

Before marking milestone complete:
- [ ] All milestone tasks completed
- [ ] Test coverage meets target (70%+ unit, 60%+ integration)
- [ ] No failing tests
- [ ] Code review completed (self-review for solo dev)
- [ ] Documentation updated
- [ ] Integration tests pass
- [ ] Performance acceptable (no obvious lag)

### Project Quality Gates

Before production deployment:
- [ ] All P0 and P1 milestones complete
- [ ] Overall test coverage ≥70% unit, ≥60% integration, ≥50% E2E
- [ ] No critical bugs
- [ ] Performance meets requirements (<500ms image load, <10s inference)
- [ ] All E2E tests passing
- [ ] Documentation complete and reviewed
- [ ] Windows installer tested on clean system

---

## Progress Tracking

### Daily Progress Template

**Date**: YYYY-MM-DD
**Current Milestone**: MX
**Current Task**: [Task name]

**Completed Today**:
- [ ] Task 1 (Xh)
- [ ] Task 2 (Yh)

**Tests Passing**: X / Y (Z%)

**Blockers**: [List any issues]

**Tomorrow's Plan**: [Next tasks]

### Weekly Progress Template

**Week X** (Dates: YYYY-MM-DD to YYYY-MM-DD)
**Milestone**: MX

**Tasks completed**: X / Y (Z%)
**Hours spent**: A / B (C%)
**Milestone progress**: D%
**Test coverage**: E%

**Highlights**:
- [Major achievement 1]
- [Major achievement 2]

**Issues/Blockers**:
- [Issue 1 and resolution]

**Next week focus**:
- [Primary goals]

---

## Notes

### Conventions

**Task Naming**:
- Use active verbs (Write, Implement, Refactor, Test)
- Be specific: "Write test for image loading" not "Test image"
- Include context: component/module name

**Time Estimates**:
- Rounded to nearest 0.5h
- Include testing, debugging, documentation time
- Conservative estimates for solo developer learning PyQt6

**TDD Cycle**:
- Always pair [RED] with [GREEN]
- Add [REFACTOR] when code can be improved
- Always end feature work with [COMMIT]

### Assumptions

- Solo developer with Python experience but learning PyQt6
- Development environment: Windows 10/11, VS Code/PyCharm
- Existing ALA model code reusable with minimal changes
- Gradio server can run locally alongside PyQt6 app
- Sufficient GPU available for model inference (CUDA preferred)
- Full-time development (40h/week)

### Adjustments

**If behind schedule**:
- Focus on P0 tasks only (M0-M4)
- Defer M5 (Few-Shot) and M6 (YOLO) to v2.0
- Reduce M7 (Polish) scope
- Use existing ALA CLI scripts as temporary solution

**If ahead of schedule**:
- Add more comprehensive E2E tests
- Improve documentation with video tutorials
- Add Linux/macOS packaging (M8)
- Start v2.0 features (video support, plugin system)

---

## Approval

**Task List Prepared By**: Claude (based on PLAN.md v1.0)
**Date**: 2025-01-13
**Based on**: PLAN.md v1.0, TECHSPEC.md v1.0
**Review Status**: Ready for user review
**Ready for Execution**: Pending approval

**Next Steps**:
1. User reviews TODO.md v1.0
2. Validate with Codex (Phase 6 of tdd-mvp-planner)
3. Address validation feedback
4. Create TODO.md v2.0 if needed
5. Begin M0: Project Setup

---
