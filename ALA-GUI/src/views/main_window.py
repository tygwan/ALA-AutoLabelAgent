"""
Main Window for ALA-GUI Application.

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

from views.image_canvas import ImageCanvas


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

        # Initialize dock widgets as instance variables
        self.file_dock: Optional[QDockWidget] = None
        self.class_dock: Optional[QDockWidget] = None
        self.props_dock: Optional[QDockWidget] = None

        # Initialize actions as instance variables
        self._init_actions()

        # Set up UI components
        self.init_ui()

    def init_ui(self) -> None:
        """Initialize the user interface components."""
        self._setup_window()
        self._create_dock_widgets()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_status_bar()
        self._create_central_widget()

        # Connect view menu actions to dock widgets
        self._connect_view_actions()

    def _init_actions(self) -> None:
        """Initialize all actions used in menus and toolbar."""
        # File actions
        self.new_action = QAction("&New Project...", self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.setStatusTip("Create a new project")

        self.open_action = QAction("&Open Project...", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.setStatusTip("Open an existing project")

        self.save_action = QAction("&Save Project", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.setStatusTip("Save the current project")

        self.import_action = QAction("&Import Images...", self)
        self.import_action.setShortcut("Ctrl+I")
        self.import_action.setStatusTip("Import images to the project")

        self.export_action = QAction("&Export Annotations...", self)
        self.export_action.setShortcut("Ctrl+E")
        self.export_action.setStatusTip("Export annotations to COCO/YOLO format")

        self.exit_action = QAction("E&xit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.setStatusTip("Exit the application")
        self.exit_action.triggered.connect(self.close)

        # Edit actions
        self.undo_action = QAction("&Undo", self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.setStatusTip("Undo last action")

        self.redo_action = QAction("&Redo", self)
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.setStatusTip("Redo last undone action")

        self.prefs_action = QAction("&Preferences...", self)
        self.prefs_action.setShortcut("Ctrl+,")
        self.prefs_action.setStatusTip("Open preferences dialog")

        # View actions
        self.zoom_in_action = QAction("Zoom &In", self)
        self.zoom_in_action.setShortcut("Ctrl++")
        self.zoom_in_action.setStatusTip("Zoom in on the image")

        self.zoom_out_action = QAction("Zoom &Out", self)
        self.zoom_out_action.setShortcut("Ctrl+-")
        self.zoom_out_action.setStatusTip("Zoom out on the image")

        self.fit_action = QAction("&Fit to Window", self)
        self.fit_action.setShortcut("Ctrl+0")
        self.fit_action.setStatusTip("Fit image to window")

        # Navigation actions
        self.prev_action = QAction("&Previous Image", self)
        self.prev_action.setShortcut("Left")
        self.prev_action.setStatusTip("Go to previous image")

        self.next_action = QAction("&Next Image", self)
        self.next_action.setShortcut("Right")
        self.next_action.setStatusTip("Go to next image")

        # Tools actions
        self.auto_annotate_action = QAction("&Auto-Annotate...", self)
        self.auto_annotate_action.setShortcut("Ctrl+A")
        self.auto_annotate_action.setStatusTip("Run auto-annotation with AI models")

        self.few_shot_action = QAction("&Few-Shot Classification...", self)
        self.few_shot_action.setShortcut("Ctrl+F")
        self.few_shot_action.setStatusTip("Run few-shot classification")

        self.train_action = QAction("&Train YOLO Model...", self)
        self.train_action.setStatusTip("Train a YOLO model on annotations")

        # Help actions
        self.docs_action = QAction("&Documentation", self)
        self.docs_action.setShortcut("F1")
        self.docs_action.setStatusTip("Open documentation")

        self.shortcuts_action = QAction("&Keyboard Shortcuts", self)
        self.shortcuts_action.setStatusTip("View keyboard shortcuts")

        self.about_action = QAction("&About ALA-GUI", self)
        self.about_action.setStatusTip("About this application")

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
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.import_action)
        file_menu.addAction(self.export_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

    def _add_edit_menu_actions(self, edit_menu: QMenu) -> None:
        """
        Add actions to Edit menu.

        Args:
            edit_menu: Edit menu to add actions to
        """
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.prefs_action)

    def _add_view_menu_actions(self, view_menu: QMenu) -> None:
        """
        Add actions to View menu.

        Args:
            view_menu: View menu to add actions to
        """
        # Zoom actions
        view_menu.addAction(self.zoom_in_action)
        view_menu.addAction(self.zoom_out_action)
        view_menu.addAction(self.fit_action)
        view_menu.addSeparator()

        # Dock widget toggle actions (will be added after dock widgets are created)
        # These will be set up in _connect_view_actions()

    def _add_tools_menu_actions(self, tools_menu: QMenu) -> None:
        """
        Add actions to Tools menu.

        Args:
            tools_menu: Tools menu to add actions to
        """
        tools_menu.addAction(self.auto_annotate_action)
        tools_menu.addAction(self.few_shot_action)
        tools_menu.addSeparator()
        tools_menu.addAction(self.train_action)

    def _add_help_menu_actions(self, help_menu: QMenu) -> None:
        """
        Add actions to Help menu.

        Args:
            help_menu: Help menu to add actions to
        """
        help_menu.addAction(self.docs_action)
        help_menu.addAction(self.shortcuts_action)
        help_menu.addSeparator()
        help_menu.addAction(self.about_action)

    def _create_toolbar(self) -> None:
        """Create the main toolbar with common actions (reusing menu actions)."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(True)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # File actions
        toolbar.addAction(self.new_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()

        # Navigation actions
        toolbar.addAction(self.prev_action)
        toolbar.addAction(self.next_action)
        toolbar.addSeparator()

        # Zoom actions
        toolbar.addAction(self.zoom_in_action)
        toolbar.addAction(self.zoom_out_action)
        toolbar.addAction(self.fit_action)

    def _create_status_bar(self) -> None:
        """Create the status bar for messages and progress."""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("Ready", 3000)

    def _create_dock_widgets(self) -> None:
        """Create dock widgets for file list, class list, and properties."""
        # File List Dock Widget
        self.file_dock = QDockWidget("Files", self)
        self.file_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        file_list_placeholder = QLabel("File List\n(To be implemented)")
        file_list_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_dock.setWidget(file_list_placeholder)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.file_dock)

        # Class List Dock Widget
        self.class_dock = QDockWidget("Classes", self)
        self.class_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        class_list_placeholder = QLabel("Class List\n(To be implemented)")
        class_list_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.class_dock.setWidget(class_list_placeholder)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.class_dock)

        # Properties Dock Widget
        self.props_dock = QDockWidget("Properties", self)
        self.props_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        props_placeholder = QLabel("Properties\n(To be implemented)")
        props_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.props_dock.setWidget(props_placeholder)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.props_dock)

    def _create_central_widget(self) -> None:
        """Create the central widget with ImageCanvas."""
        self.image_canvas = ImageCanvas(self)
        self.setCentralWidget(self.image_canvas)

        # Connect zoom actions to canvas
        self.zoom_in_action.triggered.connect(self.image_canvas.zoom_in)
        self.zoom_out_action.triggered.connect(self.image_canvas.zoom_out)
        self.fit_action.triggered.connect(self.image_canvas.fit_to_window)

    def _connect_view_actions(self) -> None:
        """Connect View menu actions to dock widget visibility toggles."""
        # Get the View menu
        view_menu = self.menuBar().findChild(QMenu, "&View")
        if view_menu is None:
            # Find by iterating through menus (fallback)
            for action in self.menuBar().actions():
                menu = action.menu()
                if menu and menu.title() == "&View":
                    view_menu = menu
                    break

        if view_menu:
            # Add dock widget toggle actions to View menu
            # These actions are automatically created by QDockWidget
            # and sync with the dock widget's visibility state
            assert self.file_dock is not None
            assert self.class_dock is not None
            assert self.props_dock is not None
            view_menu.addAction(self.file_dock.toggleViewAction())
            view_menu.addAction(self.class_dock.toggleViewAction())
            view_menu.addAction(self.props_dock.toggleViewAction())
