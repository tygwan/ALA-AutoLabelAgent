"""
Shortcut Manager for ALA-GUI.

M2: PyQt6 Image Display & Navigation - Keyboard shortcut management system.
"""

from typing import Callable, Dict

from PyQt6.QtCore import QObject
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import QWidget


class ShortcutManager(QObject):
    """
    Keyboard shortcut management system.

    Features:
    - Register and manage keyboard shortcuts
    - Associate shortcuts with actions and callbacks
    - Prevent duplicate key bindings
    - Support for standard and custom shortcuts
    - Context-aware shortcut handling

    Attributes:
        _shortcuts: Dictionary of action_name -> QAction mappings
        _key_bindings: Dictionary of key_sequence -> action_name mappings
    """

    def __init__(self, parent: QWidget) -> None:
        """
        Initialize the shortcut manager.

        Args:
            parent: Parent widget (typically MainWindow)
        """
        super().__init__(parent)

        # Storage for shortcuts
        self._shortcuts: Dict[str, QAction] = {}
        self._key_bindings: Dict[str, str] = {}

    def register_shortcut(
        self,
        action_name: str,
        key_sequence: str,
        callback: Callable[[], None],
        description: str = "",
    ) -> bool:
        """
        Register a keyboard shortcut with an action.

        Args:
            action_name: Unique identifier for the action
            key_sequence: Key sequence string (e.g., "Ctrl+S")
            callback: Function to call when shortcut triggered
            description: Human-readable description of the action

        Returns:
            True if registered successfully, False if key already bound
        """
        # Check if key sequence already bound to different action
        if key_sequence in self._key_bindings:
            existing_action = self._key_bindings[key_sequence]
            if existing_action != action_name:
                return False

        # If action name already exists, remove old binding
        if action_name in self._shortcuts:
            old_action = self._shortcuts[action_name]
            old_key = old_action.shortcut().toString()
            if old_key in self._key_bindings:
                del self._key_bindings[old_key]

        # Create QAction for the shortcut
        action = QAction(description or action_name, self.parent())
        action.setShortcut(QKeySequence(key_sequence))
        action.triggered.connect(callback)

        # Add to parent widget so it's active
        parent_widget = self.parent()
        if isinstance(parent_widget, QWidget):
            parent_widget.addAction(action)

        # Store the shortcut
        self._shortcuts[action_name] = action
        self._key_bindings[key_sequence] = action_name

        return True

    def get_all_shortcuts(self) -> Dict[str, str]:
        """
        Get all registered shortcuts.

        Returns:
            Dictionary mapping action_name to key_sequence
        """
        result = {}
        for action_name, action in self._shortcuts.items():
            result[action_name] = action.shortcut().toString()
        return result

    def setup_default_shortcuts(self) -> None:
        """
        Register all default keyboard shortcuts for the application.

        This method sets up shortcuts for:
        - Navigation (arrow keys, home, end)
        - Zoom (Ctrl+/-, Ctrl+0, Ctrl+F)
        - File operations (Ctrl+O, Ctrl+S, etc.)
        - Annotation tools (R, P, Del)
        - Undo/Redo (Ctrl+Z, Ctrl+Y)

        Note: Callbacks need to be connected by the parent window.
        """
        # Get parent window
        window = self.parent()

        # Navigation shortcuts
        self.register_shortcut(
            "next_image",
            "Right",
            lambda: self._safe_call(window, "next_image"),
            "Next image",
        )
        self.register_shortcut(
            "prev_image",
            "Left",
            lambda: self._safe_call(window, "previous_image"),
            "Previous image",
        )
        self.register_shortcut(
            "first_image",
            "Home",
            lambda: self._safe_call(window, "first_image"),
            "First image",
        )
        self.register_shortcut(
            "last_image",
            "End",
            lambda: self._safe_call(window, "last_image"),
            "Last image",
        )

        # Zoom shortcuts
        self.register_shortcut(
            "zoom_in",
            "Ctrl++",
            lambda: self._safe_call(window, "zoom_in"),
            "Zoom in",
        )
        self.register_shortcut(
            "zoom_out",
            "Ctrl+-",
            lambda: self._safe_call(window, "zoom_out"),
            "Zoom out",
        )
        self.register_shortcut(
            "zoom_reset",
            "Ctrl+0",
            lambda: self._safe_call(window, "zoom_reset"),
            "Reset zoom",
        )
        self.register_shortcut(
            "zoom_fit",
            "Ctrl+F",
            lambda: self._safe_call(window, "zoom_fit"),
            "Fit to window",
        )

        # File operation shortcuts
        self.register_shortcut(
            "open_file",
            "Ctrl+O",
            lambda: self._safe_call(window, "open_file"),
            "Open file",
        )
        self.register_shortcut(
            "save", "Ctrl+S", lambda: self._safe_call(window, "save"), "Save"
        )
        self.register_shortcut(
            "save_as",
            "Ctrl+Shift+S",
            lambda: self._safe_call(window, "save_as"),
            "Save as",
        )
        self.register_shortcut(
            "quit", "Ctrl+Q", lambda: self._safe_call(window, "quit"), "Quit"
        )

        # Tool shortcuts
        self.register_shortcut(
            "tool_rectangle",
            "R",
            lambda: self._safe_call(window, "select_rectangle_tool"),
            "Rectangle tool",
        )
        self.register_shortcut(
            "tool_polygon",
            "P",
            lambda: self._safe_call(window, "select_polygon_tool"),
            "Polygon tool",
        )
        self.register_shortcut(
            "delete_annotation",
            "Del",
            lambda: self._safe_call(window, "delete_annotation"),
            "Delete annotation",
        )

        # Undo/Redo shortcuts
        self.register_shortcut(
            "undo", "Ctrl+Z", lambda: self._safe_call(window, "undo"), "Undo"
        )
        self.register_shortcut(
            "redo", "Ctrl+Y", lambda: self._safe_call(window, "redo"), "Redo"
        )

    def _safe_call(self, window: QWidget, method_name: str) -> None:
        """
        Safely call a method on the window if it exists.

        Args:
            window: The window object
            method_name: Name of the method to call
        """
        if hasattr(window, method_name):
            method = getattr(window, method_name)
            if callable(method):
                method()
