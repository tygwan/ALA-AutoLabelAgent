"""
Main Window for ALA-GUI Application

M2: GUI Layer - Main application window with menu bar, toolbar, and dock widgets.
"""

from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QDockWidget,
    QLabel,
    QMainWindow,
    QMenu,
    QStatusBar,
    QToolBar,
    QWidget,
)


class MainWindow(QMainWindow):
    """
    Main application window for ALA-GUI.

    Features:
    - Menu bar (File, Edit, View, Tools, Help)
    - Toolbar with common actions
    - Status bar for messages and progress
    - Dock widgets for file list, class list, properties
    - Central widget for image canvas (to be implemented)
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the main window.

        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        self.init_ui()

    def init_ui(self) -> None:
        """Initialize the user interface components."""
        self._setup_window()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_status_bar()
        self._create_dock_widgets()
        self._create_central_widget()

    def _setup_window(self) -> None:
        """Set up the main window properties."""
        self.setWindowTitle("ALA-GUI - Auto Label Agent")
        self.setGeometry(100, 100, 1280, 720)

    def _create_menu_bar(self) -> None:
        """Create the menu bar with File, Edit, View, Tools, Help menus."""
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("&File")
        self._add_file_menu_actions(file_menu)

        # Edit Menu
        edit_menu = menu_bar.addMenu("&Edit")
        self._add_edit_menu_actions(edit_menu)

        # View Menu
        view_menu = menu_bar.addMenu("&View")
        self._add_view_menu_actions(view_menu)

        # Tools Menu
        tools_menu = menu_bar.addMenu("&Tools")
        self._add_tools_menu_actions(tools_menu)

        # Help Menu
        help_menu = menu_bar.addMenu("&Help")
        self._add_help_menu_actions(help_menu)

    def _add_file_menu_actions(self, file_menu: QMenu) -> None:
        """
        Add actions to File menu.

        Args:
            file_menu: File menu to add actions to
        """
        # New Project
        new_action = QAction("&New Project...", self)
        new_action.setShortcut("Ctrl+N")
        new_action.setStatusTip("Create a new project")
        file_menu.addAction(new_action)

        # Open Project
        open_action = QAction("&Open Project...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Open an existing project")
        file_menu.addAction(open_action)

        # Save Project
        save_action = QAction("&Save Project", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip("Save the current project")
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        # Import Images
        import_action = QAction("&Import Images...", self)
        import_action.setShortcut("Ctrl+I")
        import_action.setStatusTip("Import images to the project")
        file_menu.addAction(import_action)

        # Export Annotations
        export_action = QAction("&Export Annotations...", self)
        export_action.setShortcut("Ctrl+E")
        export_action.setStatusTip("Export annotations to COCO/YOLO format")
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        # Exit
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def _add_edit_menu_actions(self, edit_menu: QMenu) -> None:
        """
        Add actions to Edit menu.

        Args:
            edit_menu: Edit menu to add actions to
        """
        # Undo
        undo_action = QAction("&Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.setStatusTip("Undo last action")
        edit_menu.addAction(undo_action)

        # Redo
        redo_action = QAction("&Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.setStatusTip("Redo last undone action")
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        # Preferences
        prefs_action = QAction("&Preferences...", self)
        prefs_action.setShortcut("Ctrl+,")
        prefs_action.setStatusTip("Open preferences dialog")
        edit_menu.addAction(prefs_action)

    def _add_view_menu_actions(self, view_menu: QMenu) -> None:
        """
        Add actions to View menu.

        Args:
            view_menu: View menu to add actions to
        """
        # Zoom In
        zoom_in_action = QAction("Zoom &In", self)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.setStatusTip("Zoom in on the image")
        view_menu.addAction(zoom_in_action)

        # Zoom Out
        zoom_out_action = QAction("Zoom &Out", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.setStatusTip("Zoom out on the image")
        view_menu.addAction(zoom_out_action)

        # Fit to Window
        fit_action = QAction("&Fit to Window", self)
        fit_action.setShortcut("Ctrl+0")
        fit_action.setStatusTip("Fit image to window")
        view_menu.addAction(fit_action)

        view_menu.addSeparator()

        # Toggle File List
        toggle_files_action = QAction("&File List", self)
        toggle_files_action.setCheckable(True)
        toggle_files_action.setChecked(True)
        toggle_files_action.setStatusTip("Show/hide file list panel")
        view_menu.addAction(toggle_files_action)

        # Toggle Class List
        toggle_classes_action = QAction("&Class List", self)
        toggle_classes_action.setCheckable(True)
        toggle_classes_action.setChecked(True)
        toggle_classes_action.setStatusTip("Show/hide class list panel")
        view_menu.addAction(toggle_classes_action)

    def _add_tools_menu_actions(self, tools_menu: QMenu) -> None:
        """
        Add actions to Tools menu.

        Args:
            tools_menu: Tools menu to add actions to
        """
        # Auto-Annotate
        auto_annotate_action = QAction("&Auto-Annotate...", self)
        auto_annotate_action.setShortcut("Ctrl+A")
        auto_annotate_action.setStatusTip("Run auto-annotation with AI models")
        tools_menu.addAction(auto_annotate_action)

        # Few-Shot Classification
        few_shot_action = QAction("&Few-Shot Classification...", self)
        few_shot_action.setShortcut("Ctrl+F")
        few_shot_action.setStatusTip("Run few-shot classification")
        tools_menu.addAction(few_shot_action)

        tools_menu.addSeparator()

        # Train YOLO Model
        train_action = QAction("&Train YOLO Model...", self)
        train_action.setStatusTip("Train a YOLO model on annotations")
        tools_menu.addAction(train_action)

    def _add_help_menu_actions(self, help_menu: QMenu) -> None:
        """
        Add actions to Help menu.

        Args:
            help_menu: Help menu to add actions to
        """
        # Documentation
        docs_action = QAction("&Documentation", self)
        docs_action.setShortcut("F1")
        docs_action.setStatusTip("Open documentation")
        help_menu.addAction(docs_action)

        # Keyboard Shortcuts
        shortcuts_action = QAction("&Keyboard Shortcuts", self)
        shortcuts_action.setStatusTip("View keyboard shortcuts")
        help_menu.addAction(shortcuts_action)

        help_menu.addSeparator()

        # About
        about_action = QAction("&About ALA-GUI", self)
        about_action.setStatusTip("About this application")
        help_menu.addAction(about_action)

    def _create_toolbar(self) -> None:
        """Create the main toolbar with common actions."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(True)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # Add placeholder actions (icons will be added later)
        new_action = QAction("New", self)
        new_action.setStatusTip("Create a new project")
        toolbar.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.setStatusTip("Open an existing project")
        toolbar.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setStatusTip("Save the current project")
        toolbar.addAction(save_action)

        toolbar.addSeparator()

        # Navigation actions
        prev_action = QAction("Previous", self)
        prev_action.setStatusTip("Go to previous image")
        toolbar.addAction(prev_action)

        next_action = QAction("Next", self)
        next_action.setStatusTip("Go to next image")
        toolbar.addAction(next_action)

        toolbar.addSeparator()

        # Zoom actions
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setStatusTip("Zoom in on the image")
        toolbar.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setStatusTip("Zoom out on the image")
        toolbar.addAction(zoom_out_action)

        fit_action = QAction("Fit", self)
        fit_action.setStatusTip("Fit image to window")
        toolbar.addAction(fit_action)

    def _create_status_bar(self) -> None:
        """Create the status bar for messages and progress."""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("Ready", 3000)

    def _create_dock_widgets(self) -> None:
        """Create dock widgets for file list, class list, and properties."""
        # File List Dock Widget
        file_dock = QDockWidget("Files", self)
        file_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        file_list_placeholder = QLabel("File List\n(To be implemented)")
        file_list_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_dock.setWidget(file_list_placeholder)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, file_dock)

        # Class List Dock Widget
        class_dock = QDockWidget("Classes", self)
        class_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        class_list_placeholder = QLabel("Class List\n(To be implemented)")
        class_list_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        class_dock.setWidget(class_list_placeholder)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, class_dock)

        # Properties Dock Widget
        props_dock = QDockWidget("Properties", self)
        props_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        props_placeholder = QLabel("Properties\n(To be implemented)")
        props_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        props_dock.setWidget(props_placeholder)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, props_dock)

    def _create_central_widget(self) -> None:
        """Create the central widget (placeholder for image canvas)."""
        central_widget = QLabel("Image Canvas\n(To be implemented in next step)")
        central_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        central_widget.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
                color: #666;
                background-color: #f0f0f0;
                border: 2px dashed #ccc;
            }
            """
        )
        self.setCentralWidget(central_widget)
