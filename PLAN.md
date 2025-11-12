# ALA-GUI Hybrid Application - Implementation Plan (TDD-Driven)

## Version: 1.0
**Last Updated**: 2025-01-13
**Review Status**: Draft
**Target Timeline**: 15 weeks MVP (Hybrid Desktop + Web), 20 weeks (with buffer)
**Scope**: Production-ready desktop GUI with integrated web interface for Few-Shot Learning

---

## Overview

Transform ALA (Auto-Label Agent) from a CLI-based pipeline into a user-friendly hybrid application combining desktop GUI capabilities with web-based Few-Shot Learning interface. The system will integrate SAM2, Florence-2, and Few-Shot classification models into a unified workflow similar to X-AnyLabeling but customized for ALA's specific pipeline requirements.

**Current State**: 6+ separate Python scripts requiring manual execution, no visual feedback, complex CLI parameter configuration.

**Target State**:
- Desktop GUI (PyQt6) for image annotation, model execution, and project management
- Web interface (existing Gradio webapp) for Few-Shot Learning experiments
- Seamless integration between desktop and web components
- Unified user experience from image import to YOLO training

**Development Philosophy**: Red → Green → Refactor

Core TDD principles for this project:
- Write failing tests first for all GUI components
- Implement minimum code to pass UI interaction tests
- Refactor only when all tests (unit + integration + E2E) pass
- Commit only after complete TDD cycle with test evidence

**Key Principles**:
- **User-Centric Design**: Every UI decision prioritizes user workflow efficiency
- **Modular Architecture**: MVC pattern with clear separation of concerns
- **Reuse Existing Code**: Leverage existing ALA pipeline components
- **Incremental Integration**: Test each model integration independently
- **Performance First**: Background threads for all AI inference tasks

**Success Criteria**:
- ✅ Load and display 1000+ images with smooth navigation
- ✅ Execute SAM2 + Florence-2 auto-annotation with visual progress tracking
- ✅ Complete annotation workflow 80% faster than CLI approach
- ✅ Test coverage ≥ 70% (unit), ≥ 60% (integration), ≥ 50% (E2E)
- ✅ Support full ALA pipeline: annotation → Few-Shot → ground truth → YOLO training
- ✅ One-click project save/load with all settings
- ✅ Cross-platform compatibility (Windows, macOS, Linux)

---

## Dependency Graph

```
M0 (Project Setup)
  ↓
M1 (Foundation & Core Infrastructure) ← Critical Path Start
  ↓
M2 (PyQt6 Image Display & Navigation) ← Critical Path
  ↓
M3 (Model Integration - SAM2 & Florence-2) ← Critical Path
  ├─────────────┐
  ↓             ↓
M4 (Annotation Tools)  M5 (Web Integration - Few-Shot) [Parallel]
  ↓             ↓
  └─────┬───────┘
        ↓
M6 (Pipeline Integration - Ground Truth & YOLO) ← Critical Path
  ↓
M7 (Polish & User Experience) ← Critical Path
  ↓
M8 (Deployment & Distribution) ← Critical Path End

Parallel opportunities:
- M4 (Annotation Tools) and M5 (Web Integration) can proceed concurrently after M3
- Some testing phases can overlap with feature development
```

**Critical Path**: M0 → M1 → M2 → M3 → M4/M5 → M6 → M7 → M8
**Estimated Duration**: 15 weeks (critical path) + 5 weeks (buffer) = **20 weeks total**

---

## Milestones

### M0: Project Setup & Environment Configuration
**Priority**: P0 (Critical)
**Duration**:
- Optimistic: 2 days
- Realistic: 3 days
- Pessimistic: 5 days
- **Expected**: 3.5 days (~1 week with learning)

**Goal**: Establish development environment, testing infrastructure, and project scaffolding

**Test-First Approach**:
1. Create simple PyQt6 "Hello World" test to verify GUI framework works
2. Set up pytest with PyQt6 integration (qtbot fixtures)
3. Configure CI/CD with automated test execution (GitHub Actions)
4. Establish code quality gates (black, pylint, mypy)

**Deliverables**:
- [ ] PyQt6 development environment configured (venv, requirements.txt)
- [ ] Testing framework operational (pytest, pytest-qt, coverage)
- [ ] Git repository initialized with .gitignore for Python/PyQt6
- [ ] CI/CD pipeline setup (GitHub Actions: test + lint on push)
- [ ] Project structure created following MVC pattern
- [ ] Development documentation (CONTRIBUTING.md, SETUP.md)

**Test Coverage Target**: 100% (setup scripts and sample tests)

**Dependencies**: None

**Risks**:
- **Technical**: PyQt6 installation issues on different platforms
  - *Mitigation*: Document installation for Windows/macOS/Linux, provide Docker fallback
- **Schedule**: Learning curve for pytest-qt and GUI testing
  - *Mitigation*: Allocate extra time for learning, use simple examples first

---

### M1: Foundation & Core Infrastructure
**Priority**: P0 (Critical)
**Duration**:
- Optimistic: 4 days
- Realistic: 7 days
- Pessimistic: 10 days
- **Expected**: 7.5 days (~1.5 weeks)

**Goal**: Build foundational MVC architecture, logging, configuration management, and base classes

**Test-First Approach**:
1. Write tests for configuration loader before implementing
2. Test exception handling layer with various error scenarios
3. Test logging system with different log levels
4. Test event bus/signal system for component communication

**Deliverables**:
- [ ] MVC base classes (BaseModel, BaseView, BaseController)
- [ ] Configuration management system (load/save settings)
- [ ] Logging infrastructure with file and console handlers
- [ ] Exception handling framework with user-friendly error display
- [ ] Event system for inter-component communication (PyQt signals)
- [ ] Resource manager for images, icons, themes
- [ ] Unit tests for all foundation components (≥80% coverage)

**Test Coverage Target**: 80%+ unit tests for all core utilities

**Dependencies**: M0 (Project Setup)

**Risks**:
- **Technical**: Over-engineering foundation components
  - *Mitigation*: Follow YAGNI principle, implement only what's needed for M2
- **Schedule**: Perfectionism delaying progress
  - *Mitigation*: Set strict time box, move advanced features to refactoring phase

---

### M2: PyQt6 Image Display & Navigation
**Priority**: P0 (Critical)
**Duration**:
- Optimistic**: 5 days
- Realistic: 8 days
- Pessimistic: 12 days
- **Expected**: 8.5 days (~2 weeks)

**Goal**: Implement interactive image viewer with zoom, pan, and multi-image navigation

**Test-First Approach**:
1. Write tests for QGraphicsView image loading
2. Test zoom functionality (mouse wheel, buttons)
3. Test pan functionality (mouse drag)
4. Test image list navigation (next/previous, selection)
5. Test keyboard shortcuts (←→ for navigation, +/- for zoom)
6. E2E test: Load 100 images and navigate smoothly

**Deliverables**:
- [ ] Main application window with menu bar and toolbar
- [ ] QGraphicsView-based image display widget
- [ ] Zoom controls (fit-to-window, actual-size, custom zoom)
- [ ] Pan functionality (mouse drag, scroll bars)
- [ ] Image list panel with thumbnails
- [ ] Keyboard shortcuts for common actions
- [ ] Multi-image navigation (next/prev, jump to index)
- [ ] Image metadata display (filename, dimensions, format)
- [ ] Memory-efficient image caching system
- [ ] Unit tests for all image display components (≥75% coverage)
- [ ] Integration tests for user workflows
- [ ] E2E tests with Playwright/pytest-qt

**Test Coverage Target**: 75%+ unit, 60%+ integration

**Dependencies**: M1 (Foundation)

**Risks**:
- **Technical**: Performance issues with large images (>4K resolution)
  - *Mitigation*: Implement image downsampling, lazy loading, thumbnail generation
- **Technical**: Memory leaks from improper image disposal
  - *Mitigation*: Implement proper cleanup in QGraphicsScene, monitor memory usage
- **UX**: Unintuitive navigation controls
  - *Mitigation*: Study X-AnyLabeling/labelme UX patterns, user testing

---

### M3: Model Integration - SAM2 & Florence-2
**Priority**: P0 (Critical)
**Duration**:
- Optimistic: 7 days
- Realistic: 12 days
- Pessimistic: 18 days
- **Expected**: 13 days (~2.5 weeks)

**Goal**: Integrate existing ALA SAM2 and Florence-2 models with GUI using background threads

**Test-First Approach**:
1. Write tests for model loader (SAM2, Florence-2)
2. Test QThread-based inference worker
3. Test progress signal emission during inference
4. Test annotation result parsing and display
5. Test cancellation of long-running inference
6. Test error handling (model load failure, CUDA errors)

**Deliverables**:
- [ ] Model management system (load, unload, switch models)
- [ ] QThread-based inference workers for SAM2 and Florence-2
- [ ] Progress tracking with detailed status messages
- [ ] Text prompt input dialog for Florence-2
- [ ] Annotation result overlay on image canvas
- [ ] Bounding box and mask visualization
- [ ] Auto-save of detection results (JSON format)
- [ ] Model configuration UI (confidence threshold, NMS parameters)
- [ ] Error recovery system (retry, fallback to CPU)
- [ ] Unit tests for model wrappers (≥70% coverage)
- [ ] Integration tests for complete inference workflow
- [ ] Performance tests (inference time, memory usage)

**Test Coverage Target**: 70%+ unit, 65%+ integration, 50%+ E2E

**Dependencies**: M2 (Image Display)

**Risks**:
- **Technical**: GPU memory exhaustion with large images
  - *Mitigation*: Implement batch size reduction, image tiling, fallback to CPU
- **Technical**: Thread safety issues in PyQt6
  - *Mitigation*: Use QThread properly, signals for inter-thread communication
- **Schedule**: Debugging complex model integration issues
  - *Mitigation*: Extensive unit testing, incremental integration, SAM2 first then Florence-2

---

### M4: Annotation Tools & Manual Editing
**Priority**: P1 (High)
**Duration**:
- Optimistic: 6 days
- Realistic: 10 days
- Pessimistic: 15 days
- **Expected**: 10.5 days (~2 weeks)

**Goal**: Implement manual annotation tools for refining auto-generated annotations

**Test-First Approach**:
1. Write tests for polygon drawing on canvas
2. Test point addition/removal/dragging
3. Test bounding box resize handles
4. Test undo/redo stack
5. Test annotation save/load
6. E2E test: Draw polygon, undo, redo, save, reload

**Deliverables**:
- [ ] Polygon annotation tool (click to add points)
- [ ] Bounding box annotation tool (drag to create)
- [ ] Point editing (drag vertices, add/remove points)
- [ ] Annotation selection and deletion
- [ ] Undo/redo functionality (command pattern)
- [ ] Class assignment UI (dropdown, color coding)
- [ ] Annotation list panel (view/filter annotations)
- [ ] Keyboard shortcuts for annotation tools
- [ ] Annotation export (COCO, YOLO, Pascal VOC formats)
- [ ] Unit tests for annotation data structures (≥80% coverage)
- [ ] Integration tests for annotation workflows

**Test Coverage Target**: 80%+ unit, 60%+ integration

**Dependencies**: M3 (Model Integration) - can start in parallel after M2

**Risks**:
- **UX**: Complex annotation editing interactions
  - *Mitigation*: Study existing tools (labelme, labelImg), user testing
- **Technical**: Performance with 100+ annotations on screen
  - *Mitigation*: Efficient rendering, annotation culling outside viewport

---

### M5: Web Integration - Few-Shot Learning Interface
**Priority**: P1 (High)
**Duration**:
- Optimistic: 5 days
- Realistic: 8 days
- Pessimistic: 12 days
- **Expected**: 8.5 days (~2 weeks)

**Goal**: Integrate existing Gradio Few-Shot webapp with desktop GUI

**Test-First Approach**:
1. Write tests for subprocess management (Gradio server)
2. Test REST API communication between desktop and web
3. Test data synchronization (annotations → Few-Shot input)
4. Test result import (Few-Shot predictions → desktop)
5. Integration test: Full roundtrip annotation → Few-Shot → results

**Deliverables**:
- [ ] Embedded browser widget (QWebEngineView) for Gradio UI
- [ ] Gradio server lifecycle management (start/stop/restart)
- [ ] REST API endpoint for data exchange
- [ ] Support set management UI in desktop app
- [ ] One-click Few-Shot experiment launch from desktop
- [ ] Result import and visualization in desktop app
- [ ] Configuration sync between desktop and web
- [ ] Error handling for server connection issues
- [ ] Unit tests for API communication (≥70% coverage)
- [ ] Integration tests for desktop-web workflow

**Test Coverage Target**: 70%+ unit, 65%+ integration

**Dependencies**: M3 (Model Integration) - can start in parallel with M4

**Risks**:
- **Technical**: Port conflicts with Gradio server
  - *Mitigation*: Dynamic port allocation, port availability check
- **Technical**: Browser widget compatibility issues
  - *Mitigation*: Test on multiple platforms, fallback to external browser
- **Integration**: Data format mismatch between desktop and web
  - *Mitigation*: Define clear API contract, validation layer

---

### M6: Pipeline Integration - Ground Truth & YOLO Training
**Priority**: P1 (High)
**Duration**:
- Optimistic: 6 days
- Realistic: 10 days
- Pessimistic: 14 days
- **Expected**: 10.5 days (~2 weeks)

**Goal**: Integrate remaining ALA pipeline stages (ground truth labeling, YOLO training)

**Test-First Approach**:
1. Write tests for ground truth data structure
2. Test YOLO dataset generation (images + labels)
3. Test training configuration UI
4. Test training process monitoring
5. Integration test: Complete pipeline end-to-end

**Deliverables**:
- [ ] Ground truth labeling workflow UI
- [ ] Batch labeling tools (accept/reject, bulk edit)
- [ ] YOLO dataset generator integration
- [ ] Training configuration dialog (epochs, batch size, augmentation)
- [ ] Training progress monitoring with TensorBoard integration
- [ ] Model evaluation results display
- [ ] Export trained model functionality
- [ ] Pipeline state management (resume from any stage)
- [ ] Unit tests for pipeline components (≥70% coverage)
- [ ] Integration tests for complete pipeline
- [ ] E2E test: Image → annotation → Few-Shot → ground truth → training

**Test Coverage Target**: 70%+ unit, 65%+ integration, 50%+ E2E

**Dependencies**: M4 (Annotation Tools), M5 (Web Integration)

**Risks**:
- **Schedule**: Training long-running, hard to test
  - *Mitigation*: Mock training for tests, integration tests with tiny dataset
- **Technical**: Complex state management across pipeline stages
  - *Mitigation*: Clear state machine, comprehensive logging, checkpointing

---

### M7: Polish & User Experience Enhancement
**Priority**: P2 (Medium)
**Duration**:
- Optimistic: 4 days
- Realistic: 7 days
- Pessimistic: 10 days
- **Expected**: 7.5 days (~1.5 weeks)

**Goal**: Refine UI/UX, add themes, improve performance, fix bugs

**Test-First Approach**:
1. Performance tests (load 1000 images, measure response time)
2. Usability tests (task completion time benchmarks)
3. Visual regression tests (screenshot comparison)
4. Accessibility tests (keyboard navigation, screen reader)

**Deliverables**:
- [ ] Dark/light theme support (theme-factory skill)
- [ ] UI polish (icons, spacing, colors, animations)
- [ ] Performance optimizations (profile and fix bottlenecks)
- [ ] Settings/preferences dialog
- [ ] User onboarding (first-run wizard, tooltips)
- [ ] Keyboard shortcut reference (help menu)
- [ ] Bug fixes from internal testing
- [ ] Documentation (user guide, video tutorial)
- [ ] Visual regression test suite
- [ ] Performance benchmarks documented

**Test Coverage Target**: Maintain ≥70% coverage after refactoring

**Dependencies**: M6 (Pipeline Integration)

**Risks**:
- **Schedule**: Scope creep with endless polish requests
  - *Mitigation*: Strict prioritization, time box to 1.5 weeks
- **Technical**: Performance optimizations breaking tests
  - *Mitigation*: Run full test suite after each optimization

---

### M8: Deployment & Distribution
**Priority**: P2 (Medium)
**Duration**:
- Optimistic: 3 days
- Realistic: 5 days
- Pessimistic: 8 days
- **Expected**: 5.5 days (~1 week)

**Goal**: Package application for distribution across platforms

**Test-First Approach**:
1. Test PyInstaller build on Windows, macOS, Linux
2. Test installer creation and installation process
3. Test application startup on fresh system
4. Test auto-update mechanism (if implemented)

**Deliverables**:
- [ ] PyInstaller build configuration
- [ ] Windows installer (NSIS or Inno Setup)
- [ ] macOS app bundle (.app with DMG)
- [ ] Linux AppImage or .deb package
- [ ] Dependency bundling (models, configs)
- [ ] Installation documentation
- [ ] Release notes and changelog
- [ ] Distribution testing on clean VMs
- [ ] Auto-update system (optional, future)
- [ ] Deployment tests for each platform

**Test Coverage Target**: 100% deployment process coverage

**Dependencies**: M7 (Polish)

**Risks**:
- **Technical**: Platform-specific packaging issues
  - *Mitigation*: Test early on all platforms, maintain VM snapshots
- **Technical**: Large executable size (>500MB with models)
  - *Mitigation*: Separate model downloads, optional components
- **Legal**: PyQt6 licensing considerations (GPL)
  - *Mitigation*: Review license, consider PySide6 if commercial

---

## Resource Allocation

**Solo Developer Time Commitment:**
- **Full-time equivalent**: 40 hours/week
- **Recommended schedule**: 4-6 hours/day for quality-focused development
- **Total project hours**: 15 weeks × 40 hours = **600 hours**

**Time Distribution by Phase:**
| Phase | Duration | Percentage | Hours |
|-------|----------|-----------|--------|
| M0: Setup | 1 week | 5% | 30h |
| M1: Foundation | 1.5 weeks | 10% | 60h |
| M2: Image Display | 2 weeks | 13% | 78h |
| M3: Model Integration | 2.5 weeks | 17% | 102h |
| M4: Annotation Tools | 2 weeks | 13% | 78h |
| M5: Web Integration | 2 weeks | 13% | 78h |
| M6: Pipeline Integration | 2 weeks | 13% | 78h |
| M7: Polish | 1.5 weeks | 10% | 60h |
| M8: Deployment | 1 week | 6% | 36h |
| **Total** | **15 weeks** | **100%** | **600h** |

**Buffer Allocation (5 weeks / 200 hours):**
- Learning curve (TDD + PyQt6): 80 hours
- Unexpected technical challenges: 60 hours
- Testing and bug fixing: 40 hours
- Documentation: 20 hours

**Realistic Timeline with Buffer: 20 weeks (~5 months)**

---

## Risk Analysis

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| PyQt6 learning curve steeper than expected | High | Medium | Allocate 2 weeks for tutorials, use my-skills guides |
| Model integration performance issues | Medium | High | Implement threading early, profile regularly |
| Memory leaks in GUI | Medium | Medium | Use Python profilers, proper object cleanup |
| Platform-specific packaging problems | High | Medium | Test on all platforms early, maintain VMs |
| Web-desktop integration complexity | Medium | High | Start with simple REST API, incremental complexity |

### Schedule Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Solo developer bandwidth constraints | High | High | Quality-first timeline, no hard deadlines |
| TDD slowing initial development | Medium | Low | TDD speeds up later phases, fewer bugs |
| Scope creep from feature requests | High | Medium | Strict prioritization, defer P2 features |
| Testing infrastructure setup delays | Low | Medium | M0 focuses solely on setup, minimal features |

### Resource Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| GPU unavailability for model testing | Low | High | Implement CPU fallback, cloud GPU testing |
| Lack of PyQt6 expertise | High | Medium | Leverage senior-architect skill, study references |
| Insufficient test coverage | Medium | High | TDD from day 1, coverage gates in CI/CD |

---

## Quality Gates

All milestones must pass these gates before proceeding:

1. **Unit Test Coverage**: ≥70% for all new code
2. **Integration Test Coverage**: ≥60% for workflows
3. **E2E Test Coverage**: ≥50% for critical paths
4. **Code Quality**: Pylint score ≥8.0/10, no critical mypy errors
5. **Performance**: Meet defined benchmarks (image load <500ms, inference <10s)
6. **Documentation**: All public APIs documented, README updated
7. **User Testing**: At least 1 manual walkthrough per milestone

**Gate Enforcement**: CI/CD blocks merge if any gate fails

---

## Testing Strategy

### Unit Tests (pytest)
- **Target**: 70%+ coverage
- **Focus**: Individual functions, classes, utilities
- **Tools**: pytest, pytest-cov, pytest-mock

### Integration Tests (pytest-qt)
- **Target**: 60%+ coverage
- **Focus**: Component interactions, workflows
- **Tools**: pytest-qt (qtbot), fixtures for GUI testing

### E2E Tests (Playwright or pytest-qt)
- **Target**: 50%+ coverage
- **Focus**: Complete user workflows
- **Tools**: Playwright (if web-heavy) or pytest-qt

### Performance Tests
- **Benchmarks**:
  - Image load: <500ms for 10MB image
  - Zoom/pan: 60 FPS minimum
  - Model inference: <10s for SAM2 on 1024x1024 image
- **Tools**: pytest-benchmark, memory_profiler

### Visual Regression Tests
- **Tool**: pytest-qt screenshot comparison
- **Frequency**: Before each release

---

## Success Metrics

### Functional Metrics
- ✅ All 6 ALA pipeline stages integrated and working
- ✅ Support 5+ annotation formats (COCO, YOLO, Pascal VOC, etc.)
- ✅ Load and process 1000+ images without crashes
- ✅ Complete annotation workflow in <5 minutes per image

### Performance Metrics
- ✅ Application startup: <3 seconds
- ✅ Image load time: <500ms
- ✅ UI responsiveness: <100ms for user interactions
- ✅ Model inference: SAM2 <10s, Florence-2 <15s (GPU)

### Quality Metrics
- ✅ Test coverage: ≥70% unit, ≥60% integration, ≥50% E2E
- ✅ Code quality: Pylint ≥8.0/10
- ✅ Zero critical security vulnerabilities
- ✅ Crash rate: <0.1% per session

### User Experience Metrics
- ✅ First-run success rate: >90%
- ✅ Task completion time: 80% faster than CLI
- ✅ User satisfaction: ≥4.0/5.0 (internal testing)

---

## Next Steps

1. **Immediate (Week 1)**:
   - ✅ Set up development environment (M0)
   - ✅ Study PyQt6 tutorials and reference projects
   - ✅ Create project structure following MVC pattern

2. **Short-term (Weeks 2-4)**:
   - Build foundation infrastructure (M1)
   - Implement image display and navigation (M2)
   - Begin SAM2 integration (M3 start)

3. **Mid-term (Weeks 5-10)**:
   - Complete model integration (M3 finish)
   - Develop annotation tools (M4)
   - Integrate web Few-Shot interface (M5)

4. **Long-term (Weeks 11-15)**:
   - Complete pipeline integration (M6)
   - Polish and optimize (M7)
   - Package and deploy (M8)

5. **Post-MVP (Weeks 16-20 Buffer)**:
   - Bug fixes from testing
   - Performance optimizations
   - Additional features (plugin system, cloud sync, etc.)

---

## Appendix

### Reference Projects
- **X-AnyLabeling**: https://github.com/CVHub520/X-AnyLabeling
- **labelme**: https://github.com/wkentaro/labelme
- **anylabeling**: https://github.com/vietanhdev/anylabeling
- **labelImg**: https://github.com/tzutalin/labelImg

### Learning Resources
- **PyQt6 Tutorial**: https://www.pythonguis.com/pyqt6-tutorial/
- **PyQt6 Book**: "Create GUI Applications with Python & Qt6" (2025)
- **TDD Guide**: my-skills/test-driven-development/SKILL.md
- **Architecture Guide**: my-skills/senior-architect/SKILL.md

### Tools & Technologies
- **GUI Framework**: PyQt6 6.x
- **Testing**: pytest, pytest-qt, pytest-cov
- **Code Quality**: pylint, black, mypy
- **Packaging**: PyInstaller
- **Version Control**: Git + GitHub
- **CI/CD**: GitHub Actions

---

**End of PLAN.md v1.0**
