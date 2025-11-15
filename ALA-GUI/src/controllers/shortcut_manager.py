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
