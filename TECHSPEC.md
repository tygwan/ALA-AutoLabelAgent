# ALA-GUI Hybrid Application - Technical Specification

## Version: 1.0
**Last Updated**: 2025-01-13
**Status**: Draft
**Related Documents**: PLAN.md v1.0, TODO.md v1.0, UI_TRANSFORMATION_REQUIREMENTS.md

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Design](#architecture-design)
3. [Technology Stack](#technology-stack)
4. [Component Specifications](#component-specifications)
5. [Data Models](#data-models)
6. [API Specifications](#api-specifications)
7. [Integration Points](#integration-points)
8. [Performance Requirements](#performance-requirements)
9. [Security Considerations](#security-considerations)
10. [Testing Strategy](#testing-strategy)

---

## System Overview

### Purpose

Transform ALA (Auto-Label Agent) from a CLI-based pipeline into a hybrid desktop+web application that provides:
- Desktop GUI for image annotation with auto-labeling (SAM2, Florence-2)
- Web interface for Few-Shot Learning experiments
- Integrated workflow from image import to YOLO model training

### System Context

```
┌──────────────────────────────────────────────────────────┐
│                    ALA-GUI System                         │
│                                                            │
│  ┌─────────────────────────────────────────────────┐    │
│  │          Desktop Application (PyQt6)            │    │
│  │  ┌───────────────────────────────────────────┐  │    │
│  │  │  Main Window                              │  │    │
│  │  │  ├─ Image Viewer (QGraphicsView)          │  │    │
│  │  │  ├─ Annotation Tools                      │  │    │
│  │  │  ├─ Model Controls                        │  │    │
│  │  │  └─ Project Manager                       │  │    │
│  │  └───────────────────────────────────────────┘  │    │
│  │                                                   │    │
│  │  ┌───────────────────────────────────────────┐  │    │
│  │  │  Embedded Web View (QWebEngineView)       │  │    │
│  │  │  ├─ Few-Shot Interface (Gradio)           │  │    │
│  │  │  ├─ Support Set Management                │  │    │
│  │  │  └─ Experiment Dashboard                  │  │    │
│  │  └───────────────────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────┘    │
│                                                            │
│  ┌─────────────────────────────────────────────────┐    │
│  │          Backend Services                       │    │
│  │  ├─ Model Inference Engine (SAM2, Florence-2)  │    │
│  │  ├─ Few-Shot Classifier (ResNet, CLIP, DINOv2) │    │
│  │  ├─ YOLO Training Pipeline                     │    │
│  │  └─ Data Export/Import                         │    │
│  └─────────────────────────────────────────────────┘    │
│                                                            │
│  ┌─────────────────────────────────────────────────┐    │
│  │          Data Layer                             │    │
│  │  ├─ Project Files (.alagui format)             │    │
│  │  ├─ Annotation Data (COCO JSON)                │    │
│  │  ├─ Model Checkpoints (.pt, .pth)              │    │
│  │  └─ Configuration (.json, .yaml)               │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘

External Integrations:
├─ File System (images, annotations, models)
├─ GPU (CUDA for model inference)
└─ Web Browser (optional external Few-Shot interface)
```

---

## Architecture Design

### Architectural Pattern: Model-View-Controller (MVC)

```
┌────────────────────── VIEW LAYER ──────────────────────┐
│                                                          │
│  MainWindow (PyQt6.QtWidgets.QMainWindow)              │
│  ├─ MenuBar (File, Edit, View, Models, Tools, Help)   │
│  ├─ ToolBar (Quick actions)                            │
│  ├─ CentralWidget (QSplitter)                          │
│  │   ├─ LeftPanel (QWidget)                            │
│  │   │   └─ ImageListView (QListWidget)                │
│  │   ├─ CenterPanel (QWidget)                          │
│  │   │   └─ ImageCanvas (QGraphicsView)                │
│  │   └─ RightPanel (QWidget)                           │
│  │       ├─ ModelSelectorWidget                        │
│  │       ├─ AnnotationListWidget                       │
│  │       └─ ClassManagerWidget                         │
│  ├─ BottomPanel (QDockWidget)                          │
│  │   └─ WebInterfaceWidget (QWebEngineView)           │
│  └─ StatusBar (QStatusBar)                             │
│                                                          │
│  Dialogs:                                               │
│  ├─ SettingsDialog                                      │
│  ├─ ModelConfigDialog                                   │
│  ├─ ProjectPropertiesDialog                            │
│  └─ AboutDialog                                         │
│                                                          │
└──────────────────────────────────────────────────────────┘
                              ↕
                         Signals/Slots
                              ↕
┌─────────────────── CONTROLLER LAYER ───────────────────┐
│                                                          │
│  ApplicationController                                  │
│  ├─ ImageController                                     │
│  │   ├─ load_images()                                   │
│  │   ├─ navigate_next/prev()                           │
│  │   └─ zoom/pan controls                              │
│  ├─ ModelController                                     │
│  │   ├─ load_model()                                    │
│  │   ├─ run_inference()                                 │
│  │   └─ handle_results()                               │
│  ├─ AnnotationController                                │
│  │   ├─ create/edit/delete_annotation()                │
│  │   ├─ undo/redo()                                     │
│  │   └─ export_annotations()                           │
│  ├─ ProjectController                                   │
│  │   ├─ new_project()                                   │
│  │   ├─ save/load_project()                            │
│  │   └─ export_project()                               │
│  └─ WebInterfaceController                              │
│      ├─ start_gradio_server()                          │
│      ├─ sync_data()                                     │
│      └─ import_results()                               │
│                                                          │
└──────────────────────────────────────────────────────────┘
                              ↕
                         Method Calls
                              ↕
┌──────────────────── MODEL LAYER ───────────────────────┐
│                                                          │
│  Data Models:                                           │
│  ├─ Project                                             │
│  ├─ Image                                               │
│  ├─ Annotation (Polygon, BBox, Mask)                   │
│  ├─ Class                                               │
│  └─ Configuration                                       │
│                                                          │
│  Business Logic:                                        │
│  ├─ ModelInferenceEngine                                │
│  │   ├─ SAM2Wrapper                                     │
│  │   ├─ Florence2Wrapper                                │
│  │   └─ FewShotClassifier                              │
│  ├─ AnnotationManager                                   │
│  │   ├─ validate_annotation()                          │
│  │   ├─ convert_format()                               │
│  │   └─ calculate_metrics()                            │
│  ├─ DataExporter                                        │
│  │   ├─ export_coco()                                   │
│  │   ├─ export_yolo()                                   │
│  │   └─ export_pascal_voc()                            │
│  └─ YOLOTrainingPipeline                                │
│      ├─ prepare_dataset()                              │
│      ├─ train_model()                                   │
│      └─ evaluate_model()                               │
│                                                          │
│  Storage:                                               │
│  ├─ ProjectRepository (File-based)                     │
│  ├─ AnnotationRepository (JSON)                        │
│  └─ ModelRepository (Model files)                      │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

**Example: Auto-Annotation Workflow**

```
1. User clicks "Auto-Annotate" button in View
   ↓
2. View emits signal → ModelController.run_inference()
   ↓
3. ModelController:
   a. Gets current image from ImageController
   b. Gets model config from SettingsDialog
   c. Creates InferenceWorker (QThread)
   d. Starts worker with progress callback
   ↓
4. InferenceWorker (Background Thread):
   a. Loads SAM2/Florence-2 model
   b. Runs inference on image
   c. Emits progress signals (0-100%)
   d. Returns annotations when complete
   ↓
5. ModelController receives results:
   a. Validates annotation format
   b. Passes to AnnotationController
   ↓
6. AnnotationController:
   a. Creates Annotation objects
   b. Updates AnnotationManager
   c. Emits signal → View updates
   ↓
7. View updates:
   a. ImageCanvas displays annotations
   b. AnnotationListWidget shows list
   c. StatusBar shows completion message
```

---

## Technology Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Desktop GUI** | PyQt6 | 6.6+ | Main application framework |
| **Web Integration** | PyQt6.QtWebEngineWidgets | 6.6+ | Embedded browser for Gradio |
| **Web Interface** | Gradio | 4.x | Few-Shot Learning UI |
| **Deep Learning** | PyTorch | 2.0+ | Model inference backend |
| **Computer Vision** | OpenCV-Python | 4.8+ | Image processing |
| **Testing** | pytest | 8.x | Unit/integration testing |
| **GUI Testing** | pytest-qt | 4.x | PyQt6 testing framework |
| **Code Quality** | pylint, black, mypy | Latest | Linting, formatting, type checking |
| **Packaging** | PyInstaller | 6.x | Application packaging |

### Model Dependencies

| Model | Library | Version | Purpose |
|-------|---------|---------|---------|
| **SAM2** | segment-anything-2 | Latest | Instance segmentation |
| **Florence-2** | autodistill-florence-2 | 0.1.0+ | Object detection |
| **ResNet** | torchvision.models | 0.15+ | Few-Shot feature extraction |
| **CLIP** | openai/CLIP | Latest | Few-Shot classification |
| **DINOv2** | torch hub | Latest | Few-Shot classification |
| **YOLOv8** | ultralytics | 8.x | Model training |

### Development Tools

| Tool | Purpose |
|------|---------|
| **pytest-cov** | Code coverage measurement |
| **pytest-benchmark** | Performance testing |
| **pytest-mock** | Mocking for unit tests |
| **Qt Designer** | UI layout design (optional) |
| **GitHub Actions** | CI/CD automation |
| **pre-commit** | Git hooks for code quality |

---

## Component Specifications

### 1. Main Window (View Layer)

**Class**: `MainWindow` extends `QMainWindow`

**Responsibilities**:
- Application lifecycle management
- Menu bar and toolbar setup
- Layout management (splitters, dock widgets)
- Signal/slot connections
- Keyboard shortcut handling

**Key Methods**:
```python
class MainWindow(QMainWindow):
    def __init__(self):
        """Initialize main window with MVC components"""

    def setup_ui(self):
        """Create and layout all UI components"""

    def setup_connections(self):
        """Connect signals and slots between components"""

    def setup_shortcuts(self):
        """Register keyboard shortcuts"""

    def closeEvent(self, event: QCloseEvent):
        """Handle application exit (save state, cleanup)"""
```

**UI Components**:
- MenuBar: File, Edit, View, Models, Tools, Help
- ToolBar: Quick actions (New Project, Open, Save, Auto-Annotate, etc.)
- CentralWidget: 3-panel layout (Image List | Canvas | Controls)
- BottomDock: Embedded web interface (collapsible)
- StatusBar: Status messages, progress indicator, zoom level

---

### 2. Image Canvas (View Layer)

**Class**: `ImageCanvas` extends `QGraphicsView`

**Responsibilities**:
- Display images with efficient rendering
- Handle zoom and pan interactions
- Render annotation overlays (polygons, bboxes, masks)
- Support annotation creation/editing
- Manage drawing tools

**Key Features**:
```python
class ImageCanvas(QGraphicsView):
    # Signals
    annotation_created = pyqtSignal(dict)
    annotation_modified = pyqtSignal(str, dict)  # id, updated_data
    annotation_selected = pyqtSignal(str)  # annotation_id

    def load_image(self, image_path: str):
        """Load and display image efficiently"""

    def set_zoom_level(self, level: float):
        """Set zoom (1.0 = 100%, 0.5 = 50%, 2.0 = 200%)"""

    def fit_to_window(self):
        """Auto-zoom to fit image in viewport"""

    def add_annotation_overlay(self, annotation: Annotation):
        """Render annotation on canvas"""

    def set_drawing_tool(self, tool: DrawingTool):
        """Switch annotation tool (polygon, bbox, point)"""

    def handle_mouse_event(self, event: QMouseEvent):
        """Process mouse clicks for drawing/editing"""
```

**Performance Optimizations**:
- Image downsampling for display (keep original for export)
- Lazy loading with thumbnail cache
- Annotation culling (only render visible annotations)
- GPU-accelerated rendering (if available)

---

### 3. Model Inference Engine (Model Layer)

**Class**: `ModelInferenceEngine`

**Responsibilities**:
- Load and manage AI models (SAM2, Florence-2)
- Execute inference in background threads
- Handle GPU/CPU allocation
- Provide progress callbacks

**Architecture**:
```python
class ModelInferenceEngine:
    """Facade for all AI model operations"""

    def __init__(self, device: str = "auto"):
        """Initialize with device selection (cuda/cpu/auto)"""
        self.sam2 = SAM2Wrapper(device)
        self.florence2 = Florence2Wrapper(device)
        self.few_shot = FewShotClassifier(device)

    def run_sam2(self,
                 image: np.ndarray,
                 prompts: List[dict],
                 progress_callback: Callable[[float], None]) -> List[dict]:
        """Run SAM2 segmentation"""

    def run_florence2(self,
                      image: np.ndarray,
                      text_prompt: str,
                      progress_callback: Callable[[float], None]) -> List[dict]:
        """Run Florence-2 detection"""

    def run_few_shot(self,
                     query_images: List[np.ndarray],
                     support_set: Dict[str, List[np.ndarray]],
                     model_name: str = "resnet",
                     progress_callback: Callable[[float], None]) -> List[dict]:
        """Run Few-Shot classification"""


class InferenceWorker(QThread):
    """Background worker for model inference"""

    progress = pyqtSignal(float)  # 0.0 to 1.0
    finished = pyqtSignal(list)  # List[Annotation]
    error = pyqtSignal(str)  # Error message

    def __init__(self, engine: ModelInferenceEngine, task_config: dict):
        super().__init__()
        self.engine = engine
        self.config = task_config
        self._cancelled = False

    def run(self):
        """Execute inference in background thread"""
        try:
            if self.config["model"] == "sam2":
                results = self.engine.run_sam2(
                    self.config["image"],
                    self.config["prompts"],
                    lambda p: self.progress.emit(p)
                )
            elif self.config["model"] == "florence2":
                results = self.engine.run_florence2(
                    self.config["image"],
                    self.config["text_prompt"],
                    lambda p: self.progress.emit(p)
                )
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))

    def cancel(self):
        """Request cancellation of inference"""
        self._cancelled = True
```

---

### 4. Annotation Manager (Model Layer)

**Class**: `AnnotationManager`

**Responsibilities**:
- CRUD operations for annotations
- Undo/redo stack management
- Format conversion (COCO, YOLO, Pascal VOC)
- Validation and quality checks

**Data Structure**:
```python
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum

class AnnotationType(Enum):
    POLYGON = "polygon"
    BBOX = "bbox"
    MASK = "mask"
    POINT = "point"

@dataclass
class Annotation:
    id: str  # UUID
    image_id: str
    class_id: int
    class_name: str
    type: AnnotationType
    geometry: dict  # Format depends on type
    confidence: float = 1.0
    metadata: dict = None

    def to_coco(self) -> dict:
        """Convert to COCO format"""

    def to_yolo(self, image_width: int, image_height: int) -> str:
        """Convert to YOLO format (normalized coords)"""

    def to_pascal_voc(self, image_path: str) -> str:
        """Convert to Pascal VOC XML"""


class AnnotationManager:
    """Manage all annotations with undo/redo support"""

    def __init__(self):
        self.annotations: Dict[str, Annotation] = {}
        self._undo_stack: List[Command] = []
        self._redo_stack: List[Command] = []

    def add(self, annotation: Annotation) -> str:
        """Add annotation (returns ID)"""

    def update(self, annotation_id: str, updates: dict):
        """Update annotation (undo-able)"""

    def delete(self, annotation_id: str):
        """Delete annotation (undo-able)"""

    def undo(self):
        """Undo last action"""

    def redo(self):
        """Redo last undone action"""

    def export_coco(self, output_path: str):
        """Export all annotations as COCO JSON"""

    def export_yolo(self, output_dir: str, images: List[Image]):
        """Export annotations as YOLO format"""

    def validate(self) -> List[str]:
        """Validate all annotations, return list of issues"""
```

---

### 5. Project Manager (Model + Controller)

**Class**: `ProjectManager`

**Responsibilities**:
- Project lifecycle (new, open, save, close)
- Project file format (.alagui)
- Manage project settings
- Track dirty state for save prompts

**Project File Format** (.alagui - ZIP archive):
```
project_name.alagui (ZIP)
├── project.json          # Project metadata
├── images/
│   ├── image_list.json   # Image registry
│   └── [symlinks or relative paths to actual images]
├── annotations/
│   └── coco_format.json  # All annotations
├── models/
│   ├── model_config.json # Model settings
│   └── checkpoints/      # Trained model weights (optional)
├── support_sets/
│   └── [few-shot support sets]
└── config/
    └── settings.json     # UI preferences, last state
```

**project.json Structure**:
```json
{
  "version": "1.0.0",
  "name": "Project Name",
  "created_at": "2025-01-13T10:00:00Z",
  "last_modified": "2025-01-13T15:30:00Z",
  "image_count": 150,
  "annotation_count": 450,
  "classes": [
    {"id": 0, "name": "class_0", "color": "#FF0000"},
    {"id": 1, "name": "class_1", "color": "#00FF00"}
  ],
  "pipeline_stage": "annotation",  // annotation|few-shot|ground-truth|training
  "settings": {
    "model_config": {...},
    "few_shot_config": {...}
  }
}
```

**Code Structure**:
```python
class ProjectManager:
    """Manage ALA project lifecycle"""

    project_changed = pyqtSignal()  # Dirty state changed
    project_loaded = pyqtSignal(str)  # Project path

    def __init__(self):
        self.current_project: Optional[Project] = None
        self._dirty = False

    def new_project(self, project_path: str, name: str) -> Project:
        """Create new project"""

    def open_project(self, project_path: str) -> Project:
        """Open existing .alagui project"""

    def save_project(self, project_path: Optional[str] = None):
        """Save current project (Save As if path provided)"""

    def close_project(self) -> bool:
        """Close project (returns False if cancelled by user)"""

    def is_dirty(self) -> bool:
        """Check if project has unsaved changes"""

    def mark_dirty(self):
        """Mark project as modified"""
```

---

### 6. Web Interface Integration (Controller + View)

**Class**: `WebInterfaceController` + `WebInterfaceWidget`

**Responsibilities**:
- Manage Gradio server lifecycle
- Embed web interface in desktop app
- Sync data between desktop and web
- Handle REST API communication

**Architecture**:
```python
class WebInterfaceController:
    """Manage Gradio server and data sync"""

    server_started = pyqtSignal(str)  # URL
    server_stopped = pyqtSignal()
    results_ready = pyqtSignal(dict)  # Few-Shot results

    def __init__(self):
        self.gradio_process: Optional[subprocess.Popen] = None
        self.server_url: Optional[str] = None
        self.api_client: Optional[httpx.Client] = None

    def start_server(self, port: int = 7860) -> str:
        """Start Gradio server subprocess"""
        # Find available port
        # Launch: python -m gradio scripts/03_classification/few_shot_webapp.py
        # Return URL: http://localhost:{port}

    def stop_server(self):
        """Gracefully stop Gradio server"""

    def sync_annotations_to_web(self, annotations: List[Annotation]):
        """Send annotation data to Gradio webapp via REST API"""

    def fetch_results_from_web(self) -> dict:
        """Get Few-Shot classification results from Gradio"""

    def check_server_health(self) -> bool:
        """Ping server to check if alive"""


class WebInterfaceWidget(QWidget):
    """Embedded browser widget for Gradio UI"""

    def __init__(self, controller: WebInterfaceController):
        super().__init__()
        self.controller = controller
        self.browser = QWebEngineView()
        self.setup_ui()

    def setup_ui(self):
        """Layout browser widget with controls"""
        layout = QVBoxLayout()

        # Control bar
        control_bar = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh")
        self.external_btn = QPushButton("Open in Browser")
        self.toggle_btn = QPushButton("Hide/Show")
        control_bar.addWidget(self.refresh_btn)
        control_bar.addWidget(self.external_btn)
        control_bar.addStretch()
        control_bar.addWidget(self.toggle_btn)

        layout.addLayout(control_bar)
        layout.addWidget(self.browser)
        self.setLayout(layout)

    def load_url(self, url: str):
        """Load Gradio interface"""
        self.browser.setUrl(QUrl(url))

    def toggle_visibility(self):
        """Show/hide web interface"""
        self.setVisible(not self.isVisible())
```

**REST API Endpoints** (Gradio webapp side):
```python
# Add to few_shot_webapp.py

@app.post("/api/annotations/upload")
def upload_annotations(annotations: List[dict]):
    """Receive annotations from desktop app"""
    # Save to temporary location for Few-Shot processing
    return {"status": "success", "count": len(annotations)}

@app.get("/api/results/{experiment_id}")
def get_results(experiment_id: str):
    """Retrieve Few-Shot experiment results"""
    # Load results from disk
    return {"experiment_id": experiment_id, "results": [...]}

@app.post("/api/support_set/upload")
def upload_support_set(support_set: dict):
    """Receive support set from desktop"""
    return {"status": "success"}
```

---

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from enum import Enum
import uuid

# ==================== Project ====================

@dataclass
class Project:
    """Top-level project container"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    path: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)
    version: str = "1.0.0"

    images: List['Image'] = field(default_factory=list)
    annotations: List['Annotation'] = field(default_factory=list)
    classes: List['Class'] = field(default_factory=list)

    pipeline_stage: str = "annotation"  # annotation|few-shot|ground-truth|training
    settings: Dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Serialize to dict for JSON export"""
        return {
            "id": self.id,
            "name": self.name,
            "path": self.path,
            "created_at": self.created_at.isoformat(),
            "last_modified": self.last_modified.isoformat(),
            "version": self.version,
            "image_count": len(self.images),
            "annotation_count": len(self.annotations),
            "classes": [c.to_dict() for c in self.classes],
            "pipeline_stage": self.pipeline_stage,
            "settings": self.settings
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        """Deserialize from dict"""
        ...


# ==================== Image ====================

@dataclass
class Image:
    """Image metadata"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    filename: str = ""
    path: str = ""  # Absolute or relative to project
    width: int = 0
    height: int = 0
    format: str = ""  # jpg, png, etc.
    file_size: int = 0  # bytes
    date_added: datetime = field(default_factory=datetime.now)

    # Annotations linked to this image
    annotation_ids: List[str] = field(default_factory=list)

    # Processing status
    status: str = "pending"  # pending|processing|annotated|validated

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "filename": self.filename,
            "path": self.path,
            "width": self.width,
            "height": self.height,
            "format": self.format,
            "file_size": self.file_size,
            "date_added": self.date_added.isoformat(),
            "annotation_ids": self.annotation_ids,
            "status": self.status
        }


# ==================== Annotation ====================

class AnnotationType(Enum):
    POLYGON = "polygon"
    BBOX = "bbox"
    MASK = "mask"
    POINT = "point"

@dataclass
class Annotation:
    """Generic annotation structure"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    image_id: str = ""
    class_id: int = 0
    class_name: str = ""
    type: AnnotationType = AnnotationType.POLYGON

    # Geometry varies by type:
    # POLYGON: {"points": [[x1,y1], [x2,y2], ...]}
    # BBOX: {"xmin": x, "ymin": y, "xmax": x, "ymax": y}
    # MASK: {"rle": "...", "size": [h, w]}
    # POINT: {"x": x, "y": y}
    geometry: Dict = field(default_factory=dict)

    confidence: float = 1.0  # 0.0-1.0 (1.0 for manual annotations)
    metadata: Dict = field(default_factory=dict)

    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = "user"  # user|sam2|florence2|few-shot

    def to_coco(self, category_id: int, image_width: int, image_height: int) -> dict:
        """Convert to COCO annotation format"""
        coco_ann = {
            "id": self.id,
            "image_id": self.image_id,
            "category_id": category_id,
            "iscrowd": 0,
            "area": self._calculate_area(),
        }

        if self.type == AnnotationType.POLYGON:
            coco_ann["segmentation"] = [
                [coord for point in self.geometry["points"] for coord in point]
            ]
            coco_ann["bbox"] = self._polygon_to_bbox()
        elif self.type == AnnotationType.BBOX:
            x, y, w, h = self._to_xywh()
            coco_ann["bbox"] = [x, y, w, h]
            coco_ann["segmentation"] = []

        return coco_ann

    def to_yolo(self, class_id: int, image_width: int, image_height: int) -> str:
        """Convert to YOLO format (normalized coords)"""
        if self.type == AnnotationType.BBOX:
            x, y, w, h = self._to_xywh()
            x_center = (x + w/2) / image_width
            y_center = (y + h/2) / image_height
            w_norm = w / image_width
            h_norm = h / image_height
            return f"{class_id} {x_center} {y_center} {w_norm} {h_norm}"

        elif self.type == AnnotationType.POLYGON:
            points_flat = []
            for x, y in self.geometry["points"]:
                points_flat.append(x / image_width)
                points_flat.append(y / image_height)
            coords_str = " ".join(f"{p:.6f}" for p in points_flat)
            return f"{class_id} {coords_str}"

    def _calculate_area(self) -> float:
        """Calculate annotation area in pixels"""
        ...

    def _polygon_to_bbox(self) -> List[float]:
        """Convert polygon to bounding box [x, y, width, height]"""
        ...

    def _to_xywh(self) -> Tuple[float, float, float, float]:
        """Convert to x, y, width, height format"""
        ...


# ==================== Class ====================

@dataclass
class Class:
    """Annotation class/category"""
    id: int
    name: str
    color: str = "#FF0000"  # Hex color for display
    description: str = ""

    # Few-Shot support set
    support_images: List[str] = field(default_factory=list)  # Image IDs

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "description": self.description,
            "support_image_count": len(self.support_images)
        }


# ==================== Configuration ====================

@dataclass
class AppSettings:
    """Application-wide settings"""
    # UI preferences
    theme: str = "light"  # light|dark
    language: str = "en"  # en|ko
    window_geometry: Dict = field(default_factory=dict)

    # Model defaults
    default_model: str = "sam2"  # sam2|florence2
    device: str = "auto"  # auto|cuda|cpu

    # Performance
    max_cache_size_mb: int = 2048
    num_worker_threads: int = 4

    # Few-Shot
    gradio_port: int = 7860
    auto_start_gradio: bool = False

    def to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict) -> 'AppSettings':
        return cls(**data)
```

---

## API Specifications

### Desktop ↔ Web REST API

**Base URL**: `http://localhost:{port}/api/v1`

#### 1. Upload Annotations
```http
POST /api/v1/annotations/upload
Content-Type: application/json

{
  "project_id": "uuid",
  "images": [
    {
      "image_id": "uuid",
      "filename": "image001.jpg",
      "annotations": [...]
    }
  ]
}

Response:
{
  "status": "success",
  "uploaded_count": 150,
  "timestamp": "2025-01-13T10:00:00Z"
}
```

#### 2. Start Few-Shot Experiment
```http
POST /api/v1/experiments/start
Content-Type: application/json

{
  "experiment_name": "test_experiment_1",
  "model": "resnet",
  "n_shots": [1, 5, 10],
  "thresholds": [0.5, 0.7, 0.9],
  "support_set_path": "/path/to/support_set"
}

Response:
{
  "experiment_id": "exp_uuid",
  "status": "started",
  "estimated_time_seconds": 300
}
```

#### 3. Get Experiment Results
```http
GET /api/v1/experiments/{experiment_id}/results

Response:
{
  "experiment_id": "exp_uuid",
  "status": "completed",
  "results": {
    "accuracy": 0.85,
    "predictions": [
      {"image_id": "uuid", "predicted_class": 0, "confidence": 0.92},
      ...
    ],
    "confusion_matrix": [[...], ...],
    "metrics": {...}
  }
}
```

#### 4. Sync Support Set
```http
POST /api/v1/support_set/sync
Content-Type: application/json

{
  "classes": [
    {
      "class_id": 0,
      "class_name": "class_0",
      "images": ["path1", "path2", ...]
    }
  ]
}

Response:
{
  "status": "success",
  "synced_classes": 4,
  "total_images": 120
}
```

---

## Integration Points

### 1. Existing ALA Pipeline Integration

**Reusable Components**:
```
ALA/
├── scripts/
│   ├── 01_data_preparation/
│   │   ├── autodistill_runner.py  → Wrap in SAM2Wrapper
│   │   └── advanced_preprocessor.py → Integrate in preprocessing step
│   ├── 02_preprocessing/
│   │   └── support_set_manager.py → Use for support set management
│   ├── 03_classification/
│   │   ├── classifier_cosine.py → Few-Shot engine
│   │   └── few_shot_webapp.py → Gradio web interface
│   ├── 04_ground_truth/
│   │   └── ground_truth_labeler.py → Convert to GUI widget
│   └── 05_yolo_training/
│       └── train_yolo_segmentation.py → Training pipeline integration
└── modified_packages/
    ├── autodistill_florence_2/ → Florence2Wrapper
    └── autodistill_grounded_sam_2/ → SAM2Wrapper
```

**Wrapper Strategy**:
```python
# Example: SAM2Wrapper
from ALA.modified_packages.autodistill_grounded_sam_2 import GroundedSAM2

class SAM2Wrapper:
    """GUI-friendly wrapper for SAM2"""

    def __init__(self, device: str = "auto"):
        self.model = GroundedSAM2(device=device)

    def segment(self,
                image: np.ndarray,
                text_prompt: str,
                progress_callback: Optional[Callable] = None) -> List[dict]:
        """
        Run segmentation with progress tracking

        Args:
            image: Input image (H, W, 3)
            text_prompt: Text description for segmentation
            progress_callback: Function to call with progress (0.0-1.0)

        Returns:
            List of annotation dicts with masks and boxes
        """
        if progress_callback:
            progress_callback(0.1)  # Model loading

        # Run existing ALA code
        results = self.model.predict(image, text_prompt)

        if progress_callback:
            progress_callback(0.9)  # Processing complete

        # Convert to standard annotation format
        annotations = self._convert_results(results)

        if progress_callback:
            progress_callback(1.0)

        return annotations

    def _convert_results(self, results) -> List[dict]:
        """Convert ALA format to GUI annotation format"""
        ...
```

### 2. File System Integration

**Directory Structure**:
```
User's Working Directory/
├── project_name.alagui  # Project file (ZIP)
├── images/              # Source images
├── models/              # Downloaded model checkpoints
└── exports/             # Exported datasets
    ├── coco/
    ├── yolo/
    └── pascal_voc/
```

**File Operations**:
- Read: Load images, annotations, project files
- Write: Save annotations, export datasets, save project
- Watch: Monitor image directory for new files (optional)

### 3. External Tools Integration

**Optional Integrations**:
- **TensorBoard**: Display training metrics
  ```python
  from PyQt6.QtWebEngineWidgets import QWebEngineView
  tensorboard_widget.load(QUrl("http://localhost:6006"))
  ```
- **Roboflow**: Export annotations to Roboflow
- **CVAT**: Import annotations from CVAT format

---

## Performance Requirements

### Response Time Requirements

| Action | Target | Maximum | Measurement |
|--------|--------|---------|-------------|
| Application startup | <2s | <5s | Time to main window visible |
| Image load (10MB) | <300ms | <500ms | File read + display |
| Zoom/Pan interaction | <16ms | <33ms | 60 FPS minimum |
| Annotation creation | <50ms | <100ms | Click to display |
| Model inference (SAM2) | <5s | <10s | 1024x1024 image on GPU |
| Project save | <1s | <3s | Write all data to disk |
| Project load | <2s | <5s | Read and initialize |

### Throughput Requirements

| Operation | Target | Conditions |
|-----------|--------|------------|
| Image navigation | 10 images/sec | Using keyboard arrows |
| Batch annotation import | 1000 annotations/sec | From COCO JSON |
| Batch export | 100 images/sec | To YOLO format |
| Few-Shot inference | 10 images/sec | ResNet on GPU |

### Resource Usage Limits

| Resource | Limit | Fallback |
|----------|-------|----------|
| Memory | <2GB base | Reduce cache size |
| GPU Memory | <6GB | Fallback to CPU |
| Disk Cache | <10GB | Auto-cleanup old cache |
| CPU Usage | <50% average | Reduce worker threads |

### Scalability Targets

| Metric | MVP | v1.0 | v2.0 |
|--------|-----|------|------|
| Max images per project | 1,000 | 10,000 | 100,000 |
| Max annotations per image | 50 | 100 | 500 |
| Max classes | 10 | 50 | 100 |
| Concurrent inference tasks | 1 | 3 | 5 |

---

## Security Considerations

### Data Security

1. **Local Data Only** (MVP)
   - All data stored locally on user's machine
   - No cloud sync (future feature)
   - No telemetry or analytics

2. **File Access Control**
   - Read-only access to source images
   - Write access only to project directory
   - No arbitrary file system access

3. **Project File Encryption** (Future)
   - Optional AES-256 encryption for .alagui files
   - Password protection for sensitive projects

### Model Security

1. **Model Loading**
   - Verify model checksums before loading
   - Sandbox model execution (PyTorch safety)
   - Limit model file size (<2GB)

2. **Web Interface Security**
   - Gradio server bound to localhost only
   - CORS restricted to localhost
   - No external network access

### Input Validation

1. **Image Files**
   - Validate image format (PIL.Image verification)
   - Limit image dimensions (max 8192x8192)
   - Scan for corrupted files

2. **Annotation Data**
   - Validate coordinate ranges (within image bounds)
   - Sanitize text inputs (class names, descriptions)
   - Limit annotation complexity (max 1000 points per polygon)

3. **Configuration Files**
   - JSON schema validation
   - Whitelist allowed settings
   - Reject malicious payloads

---

## Testing Strategy

### Test Pyramid

```
        /\
       /  \      E2E Tests (50% coverage)
      /____\     - Complete workflows
     /      \    - User scenarios
    /________\   Integration Tests (60% coverage)
   /          \  - Component interaction
  /____________\ - API testing
 /              \ Unit Tests (70% coverage)
/________________\ - Individual functions
                   - Data structures
```

### Unit Testing

**Target**: 70%+ coverage

**Tools**: pytest, pytest-cov, pytest-mock

**Test Categories**:
1. **Data Models**: Test all dataclass methods, serialization
2. **Utilities**: Test helper functions, converters
3. **Business Logic**: Test annotation validation, format conversion
4. **Model Wrappers**: Test with mocked models

**Example**:
```python
# tests/unit/test_annotation.py

def test_annotation_to_coco_format():
    """Test COCO format conversion"""
    annotation = Annotation(
        id="test_id",
        image_id="img_001",
        class_id=0,
        class_name="class_0",
        type=AnnotationType.POLYGON,
        geometry={"points": [[10, 10], [20, 10], [20, 20], [10, 20]]}
    )

    coco_ann = annotation.to_coco(category_id=1, image_width=100, image_height=100)

    assert coco_ann["id"] == "test_id"
    assert coco_ann["category_id"] == 1
    assert "segmentation" in coco_ann
    assert "bbox" in coco_ann
```

### Integration Testing

**Target**: 60%+ coverage

**Tools**: pytest-qt (qtbot fixtures)

**Test Categories**:
1. **GUI Components**: Test widget interactions
2. **Signal/Slot Connections**: Test event propagation
3. **File I/O**: Test project save/load
4. **Model Integration**: Test end-to-end inference workflow

**Example**:
```python
# tests/integration/test_image_canvas.py

def test_image_load_and_display(qtbot):
    """Test loading and displaying image"""
    canvas = ImageCanvas()
    qtbot.addWidget(canvas)

    # Load test image
    test_image_path = "tests/fixtures/test_image.jpg"
    canvas.load_image(test_image_path)

    # Wait for image to load
    qtbot.wait(100)

    # Verify image is displayed
    assert canvas.scene().items()
    assert canvas.current_image is not None
```

### E2E Testing

**Target**: 50%+ coverage of critical workflows

**Tools**: pytest-qt or Playwright

**Test Scenarios**:
1. **Happy Path**: Complete annotation workflow
2. **Model Inference**: Auto-annotate with SAM2
3. **Few-Shot Integration**: Send annotations to web, get results
4. **Export**: Export to YOLO format and validate

**Example**:
```python
# tests/e2e/test_annotation_workflow.py

def test_complete_annotation_workflow(qtbot, tmp_path):
    """Test complete workflow: load images → annotate → export"""
    app = MainWindow()
    qtbot.addWidget(app)

    # 1. Create new project
    project_path = tmp_path / "test_project.alagui"
    app.project_controller.new_project(str(project_path), "Test Project")

    # 2. Load images
    image_dir = "tests/fixtures/images"
    app.image_controller.load_images_from_directory(image_dir)
    qtbot.wait(500)
    assert app.image_controller.image_count() > 0

    # 3. Run auto-annotation
    app.model_controller.run_sam2(text_prompt="object")
    qtbot.waitSignal(app.model_controller.inference_finished, timeout=15000)
    assert app.annotation_controller.annotation_count() > 0

    # 4. Export to YOLO
    export_dir = tmp_path / "yolo_export"
    app.annotation_controller.export_yolo(str(export_dir))
    assert (export_dir / "dataset.yaml").exists()
```

### Performance Testing

**Tools**: pytest-benchmark, memory_profiler

**Benchmarks**:
```python
# tests/performance/test_benchmarks.py

def test_image_load_performance(benchmark):
    """Benchmark image loading time"""
    def load_image():
        canvas = ImageCanvas()
        canvas.load_image("tests/fixtures/large_image.jpg")

    result = benchmark(load_image)
    assert result.stats.mean < 0.5  # <500ms average
```

### Visual Regression Testing

**Tools**: pytest-qt screenshot comparison

**Strategy**:
1. Capture baseline screenshots of key UI states
2. Compare against baseline on each test run
3. Flag visual differences for review

---

## Appendix

### Glossary

| Term | Definition |
|------|------------|
| **Annotation** | Labeled region in an image (polygon, bbox, mask) |
| **Few-Shot Learning** | Classification with few examples per class |
| **Support Set** | Example images for each class in Few-Shot |
| **Ground Truth** | Manually verified correct labels |
| **Auto-Annotation** | Automatic annotation using AI models |
| **COCO Format** | Common annotation format (JSON) |
| **YOLO Format** | Object detection format (txt files) |

### References

- **PyQt6 Documentation**: https://doc.qt.io/qtforpython-6/
- **SAM2 Paper**: https://arxiv.org/abs/2304.02643
- **Florence-2 Paper**: https://arxiv.org/abs/2311.06242
- **COCO Format Spec**: https://cocodataset.org/#format-data
- **YOLO Format Spec**: https://docs.ultralytics.com/datasets/

---

**End of TECHSPEC.md v1.0**
