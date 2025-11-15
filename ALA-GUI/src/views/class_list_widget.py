"""
Class List Widget for ALA-GUI.

M2: PyQt6 Image Display & Navigation - Class list widget for managing
annotation classes.
"""

from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem, QWidget


class ClassListWidget(QListWidget):
    """
    Class list widget for managing annotation classes.

    Features:
    - Display annotation classes with color badges
    - Add/edit/remove classes
    - Color picker integration
    - Context menu for class operations
    - Class selection for annotation

    Signals:
        currentItemChanged: Emitted when selected class changes
        customContextMenuRequested: Emitted when context menu requested
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the class list widget.

        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)

        # Configure view settings
        self._setup_view()

    def _setup_view(self) -> None:
        """Configure the list widget view settings."""
        # Set view mode to list view for class names
        self.setViewMode(QListWidget.ViewMode.ListMode)

        # Set selection mode to single selection
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        # Enable context menu for right-click operations
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        # Enable sorting for alphabetical organization
        self.setSortingEnabled(True)

    def _create_color_badge(self, color: QColor, size: int = 16) -> QIcon:
        """
        Create a color badge icon for a class.

        Args:
            color: The color for the badge
            size: Size of the badge in pixels (default: 16)

        Returns:
            QIcon with colored badge
        """
        # Create a pixmap for the badge
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        # Paint the colored circle
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Fill with color
        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, size, size)

        painter.end()

        return QIcon(pixmap)

    def _class_exists(self, class_name: str) -> bool:
        """
        Check if a class with the given name already exists.

        Args:
            class_name: Name of the class to check

        Returns:
            True if class exists, False otherwise
        """
        for i in range(self.count()):
            if self.item(i).text() == class_name:
                return True
        return False

    def add_class(self, class_name: str, color: Optional[QColor] = None) -> bool:
        """
        Add a new annotation class to the list.

        Args:
            class_name: Name of the annotation class
            color: Color for the class (optional, defaults to random)

        Returns:
            True if class added successfully, False otherwise
        """
        # Validate class name is not empty
        if not class_name or not class_name.strip():
            return False

        # Check for duplicate class names
        if self._class_exists(class_name):
            return False

        # Use default color if none provided
        if color is None:
            # Generate a default color (can be made more sophisticated)
            import random

            color = QColor(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )

        # Create list item
        item = QListWidgetItem(class_name)

        # Create and set color badge icon
        badge_icon = self._create_color_badge(color)
        item.setIcon(badge_icon)

        # Store color in item data for later retrieval
        item.setData(Qt.ItemDataRole.UserRole, color)

        # Add item to list
        self.addItem(item)

        return True

    def remove_class(self, index: int) -> bool:
        """
        Remove a class from the list by index.

        Args:
            index: Index of the class to remove

        Returns:
            True if class removed successfully, False otherwise
        """
        # Validate index
        if index < 0 or index >= self.count():
            return False

        # Remove item at index
        item = self.takeItem(index)
        if item is None:
            return False

        # Item successfully removed
        return True

    def remove_class_by_name(self, class_name: str) -> bool:
        """
        Remove a class from the list by name.

        Args:
            class_name: Name of the class to remove

        Returns:
            True if class removed successfully, False otherwise
        """
        # Find item with matching name
        for i in range(self.count()):
            if self.item(i).text() == class_name:
                return self.remove_class(i)

        # Class not found
        return False
