# MainWindow Architecture Documentation

**Version**: 1.0
**Last Updated**: 2025-01-13
**Milestone**: M2 - PyQt6 Image Display & Navigation

---

## Overview

The `MainWindow` class is the main application window for ALA-GUI, built using PyQt6's `QMainWindow`. It provides the primary user interface with a menu bar, toolbar, status bar, dock widgets, and a central image canvas.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         MainWindow                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      Menu Bar                              │  │
│  │  File | Edit | View | Tools | Help                        │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      Toolbar                               │  │
│  │  [New] [Open] [Save] | [<<] [>>] | [+] [-] [Fit]         │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌─────────┬───────────────────────────────────┬─────────────┐  │
│  │  Files  │      ImageCanvas (Central)       │  Classes    │  │
│  │  Dock   │                                   │  Dock       │  │
│  │         │  [Image Display & Navigation]     │             │  │
│  │ [img1]  │                                   │ [person]    │  │
│  │ [img2]  │                                   │ [car]       │  │
│  │ [img3]  │                                   │ [bike]      │  │
│  │         │                                   ├─────────────┤  │
│  │         │                                   │ Properties  │  │
│  │         │                                   │  Dock       │  │
│  │         │                                   │             │  │
│  └─────────┴───────────────────────────────────┴─────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Status Bar                               │  │
│  │  Ready | Progress: 45%                                    │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Structure

### 1. Menu Bar

The menu bar provides access to all major application features through five menus:

#### File Menu
- **New Project** (Ctrl+N): Create a new annotation project
- **Open Project** (Ctrl+O): Load an existing project
- **Save Project** (Ctrl+S): Save current project
- **Import Images** (Ctrl+I): Add images to project
- **Export Annotations** (Ctrl+E): Export to COCO/YOLO format
- **Exit** (Ctrl+Q): Close application

#### Edit Menu
- **Undo** (Ctrl+Z): Undo last action
- **Redo** (Ctrl+Y): Redo undone action
- **Preferences** (Ctrl+,): Open settings dialog

#### View Menu
- **Zoom In** (Ctrl++): Zoom in on image
- **Zoom Out** (Ctrl+-): Zoom out on image
- **Fit to Window** (Ctrl+0): Fit image to viewport
- **File List** (toggle): Show/hide file list dock
- **Class List** (toggle): Show/hide class list dock
- **Properties** (toggle): Show/hide properties dock

#### Tools Menu
- **Auto-Annotate** (Ctrl+A): Run AI auto-annotation
- **Few-Shot Classification** (Ctrl+F): Run few-shot learning
- **Train YOLO Model**: Train custom YOLO model

#### Help Menu
- **Documentation** (F1): Open user documentation
- **Keyboard Shortcuts**: Show shortcut reference
- **About ALA-GUI**: Application information

### 2. Toolbar

Quick access toolbar with frequently used actions:

**File Actions**:
- New, Open, Save

**Navigation**:
- Previous Image, Next Image

**View Controls**:
- Zoom In, Zoom Out, Fit to Window

### 3. Central Widget: ImageCanvas

The central area displays images using a custom `ImageCanvas` widget based on `QGraphicsView`:

**Features**:
- Load and display images
- Zoom in/out with mouse wheel
- Pan with click-and-drag
- Fit image to window
- Coordinate transformation (canvas ↔ image)

**See**: [ImageCanvas Documentation](./IMAGECANVAS.md)

### 4. Dock Widgets

Three dockable panels for project management:

#### File List Dock (Left)
- Lists all images in current project
- Displays thumbnails
- Click to switch active image
- Drag-and-drop to import

#### Class List Dock (Right)
- Shows annotation classes
- Add/remove/edit classes
- Color-coded class indicators
- Select class for annotation

#### Properties Dock (Right)
- Displays selected annotation properties
- Edit annotation attributes
- View/modify class assignment
- Adjust confidence scores

### 5. Status Bar

Bottom status bar for application feedback:
- Current status messages
- Progress indicators for long operations
- Image information (size, format)

## Code Organization

### Class Structure

```python
class MainWindow(QMainWindow):
    """
    Main application window.

    Attributes:
        image_canvas (ImageCanvas): Central image display widget
        file_dock (QDockWidget): File list panel
        class_dock (QDockWidget): Class list panel
        props_dock (QDockWidget): Properties panel

        # Actions (shared between menu and toolbar)
        new_action, open_action, save_action
        import_action, export_action, exit_action
        undo_action, redo_action, prefs_action
        zoom_in_action, zoom_out_action, fit_action
        prev_action, next_action
        auto_annotate_action, few_shot_action, train_action
        docs_action, shortcuts_action, about_action
    """
```

### Initialization Flow

```python
def __init__(self):
    1. super().__init__()
    2. Initialize instance variables (dock widgets)
    3. _init_actions()         # Create all QActions
    4. init_ui()               # Set up UI components

def init_ui(self):
    1. _setup_window()         # Window properties
    2. _create_dock_widgets()  # Create dock panels
    3. _create_menu_bar()      # Build menus
    4. _create_toolbar()       # Build toolbar
    5. _create_status_bar()    # Create status bar
    6. _create_central_widget() # Set up ImageCanvas
    7. _connect_view_actions() # Connect View menu to docks
```

### Action Management Pattern

All actions are created once in `_init_actions()` and reused across menus and toolbars:

```python
def _init_actions(self):
    """Create all actions as instance variables."""
    # File actions
    self.new_action = QAction("&New Project...", self)
    self.new_action.setShortcut("Ctrl+N")
    self.new_action.setStatusTip("Create a new project")
    # ... more actions

def _create_menu_bar(self):
    """Reuse actions in menus."""
    file_menu.addAction(self.new_action)

def _create_toolbar(self):
    """Reuse same actions in toolbar."""
    toolbar.addAction(self.new_action)
```

**Benefits**:
- ✅ Single source of truth for each action
- ✅ Consistent behavior across menu/toolbar
- ✅ Easy to modify shortcuts and tooltips
- ✅ Reduced code duplication

### Dock Widget Management

Dock widgets are stored as instance variables for programmatic access:

```python
# Created in _create_dock_widgets()
self.file_dock = QDockWidget("Files", self)
self.class_dock = QDockWidget("Classes", self)
self.props_dock = QDockWidget("Properties", self)

# Connected to View menu in _connect_view_actions()
view_menu.addAction(self.file_dock.toggleViewAction())
```

**Benefits**:
- ✅ Can show/hide docks programmatically
- ✅ Can check dock visibility state
- ✅ Can restore dock layout
- ✅ Automatic menu synchronization

## Design Patterns

### 1. **Action Reuse Pattern**

Actions are created once and shared between components:

```python
# Create once
self.zoom_in_action = QAction("Zoom In", self)

# Use in menu
view_menu.addAction(self.zoom_in_action)

# Use in toolbar
toolbar.addAction(self.zoom_in_action)

# Connect to canvas
self.zoom_in_action.triggered.connect(self.image_canvas.zoom_in)
```

### 2. **Dock Widget Toggle Pattern**

Use Qt's built-in `toggleViewAction()` for automatic menu synchronization:

```python
# View menu automatically stays in sync with dock visibility
view_menu.addAction(self.file_dock.toggleViewAction())
```

### 3. **Separation of Concerns**

Each UI component has its own creation method:

```python
_create_menu_bar()     # Menus only
_create_toolbar()      # Toolbar only
_create_dock_widgets() # Docks only
_create_central_widget() # Canvas only
```

**Benefits**:
- ✅ Easy to find and modify specific components
- ✅ Clear code organization
- ✅ Testable in isolation

## Extension Points

### Adding a New Action

1. **Create action in `_init_actions()`**:
```python
self.my_action = QAction("&My Feature", self)
self.my_action.setShortcut("Ctrl+M")
self.my_action.setStatusTip("Do something")
self.my_action.triggered.connect(self._on_my_action)
```

2. **Add to menu**:
```python
def _add_tools_menu_actions(self, tools_menu):
    tools_menu.addAction(self.my_action)
```

3. **Optionally add to toolbar**:
```python
def _create_toolbar(self):
    toolbar.addAction(self.my_action)
```

4. **Implement handler**:
```python
def _on_my_action(self):
    """Handle my action."""
    # Implementation
```

### Adding a New Dock Widget

1. **Declare instance variable in `__init__()`**:
```python
self.my_dock: Optional[QDockWidget] = None
```

2. **Create in `_create_dock_widgets()`**:
```python
self.my_dock = QDockWidget("My Panel", self)
# Configure and add widget
self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.my_dock)
```

3. **Add to View menu in `_connect_view_actions()`**:
```python
view_menu.addAction(self.my_dock.toggleViewAction())
```

## Integration with Other Components

### ImageCanvas Integration

```python
# In _create_central_widget()
self.image_canvas = ImageCanvas(self)
self.setCentralWidget(self.image_canvas)

# Connect actions
self.zoom_in_action.triggered.connect(self.image_canvas.zoom_in)
self.zoom_out_action.triggered.connect(self.image_canvas.zoom_out)
self.fit_action.triggered.connect(self.image_canvas.fit_to_window)
```

### Future: File List Widget

```python
# Will be added in dock widget implementation
from views.file_list_widget import FileListWidget

file_list = FileListWidget()
self.file_dock.setWidget(file_list)
```

## Testing

### Unit Tests

Located in `tests/unit/test_main_window.py`:
- Window initialization
- Component presence
- Basic properties

### Integration Tests

Located in `tests/integration/test_main_window_layout.py`:

**Test Categories**:
1. **Layout Tests**: All components present and positioned correctly
2. **Menu Tests**: All menus and actions present with shortcuts
3. **Dock Tests**: Dock widgets visible, toggleable, and in correct areas
4. **Action Tests**: All actions have shortcuts and status tips
5. **State Tests**: Instance variables initialized correctly

**Run Integration Tests**:
```bash
pytest tests/integration/test_main_window_layout.py -v
```

## Performance Considerations

### Current Implementation

- ✅ Actions created once and reused
- ✅ Dock widgets lightweight (placeholders)
- ✅ Menu/toolbar built once at startup
- ✅ ImageCanvas uses efficient QGraphicsView

### Future Optimizations

- [ ] Lazy load dock widget contents
- [ ] Cache menu actions
- [ ] Optimize image loading in FileListWidget
- [ ] Use QPixmapCache for thumbnails

## Known Limitations

1. **Placeholder Dock Contents**: File list, class list, and properties panels show placeholder labels (to be implemented in next tasks)

2. **Action Handlers**: Most actions don't have implementations yet (will be added in future milestones)

3. **No State Persistence**: Window layout and dock positions not saved between sessions (M7 feature)

## Future Enhancements (Post-M2)

- **M3**: Connect auto-annotate action to model inference
- **M4**: Add annotation drawing tools
- **M5**: Connect few-shot action to Gradio interface
- **M6**: Connect train action to YOLO training
- **M7**: Save/restore window layout and preferences
- **M8**: Add application icon and theming

## References

- **PyQt6 Documentation**: https://doc.qt.io/qtforpython-6/
- **QMainWindow**: https://doc.qt.io/qt-6/qmainwindow.html
- **QGraphicsView**: https://doc.qt.io/qt-6/qgraphicsview.html
- **TODO.md**: M2 Main Window Structure section

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-13 | Initial documentation for M2 completion |

---

**Author**: Claude (ALA-GUI Development)
**Status**: ✅ Complete (M2 Milestone)
