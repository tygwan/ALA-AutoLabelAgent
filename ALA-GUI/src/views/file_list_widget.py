"""
File List Widget for ALA-GUI.

M2: PyQt6 Image Display & Navigation - File list widget for managing images.
"""

from pathlib import Path
from typing import Optional

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem, QWidget


class FileListWidget(QListWidget):
    """
    File list widget for displaying image thumbnails.

    Features:
    - Display images as thumbnails in icon view
    - Single selection mode
    - Add/remove images
    - Thumbnail caching with QPixmapCache
    - Drag-and-drop support for importing images

    Signals:
        currentItemChanged: Emitted when selected image changes
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the file list widget.

        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)

        # Configure view settings
        self._setup_view()

    def _setup_view(self) -> None:
        """Configure the list widget view settings."""
        # Set view mode to icon view for thumbnails
        self.setViewMode(QListWidget.ViewMode.IconMode)

        # Set icon size for thumbnails (128x128)
        self.setIconSize(QSize(128, 128))

        # Set selection mode to single selection
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        # Set spacing between items
        self.setSpacing(10)

        # Enable word wrap for item text
        self.setWordWrap(True)

        # Set resize mode to adjust items automatically
        self.setResizeMode(QListWidget.ResizeMode.Adjust)

        # Set movement to static (items don't move)
        self.setMovement(QListWidget.Movement.Static)

    def add_image(self, image_path: str) -> bool:
        """
        Add an image to the file list with thumbnail.

        Args:
            image_path: Path to the image file

        Returns:
            True if image added successfully, False otherwise
        """
        # Validate file exists
        path = Path(image_path)
        if not path.exists() or not path.is_file():
            return False

        # Try to load image as QPixmap
        pixmap = QPixmap(str(path))
        if pixmap.isNull():
            # Not a valid image file
            return False

        # Create thumbnail - scale to icon size while maintaining aspect ratio
        icon_size = self.iconSize()
        thumbnail = pixmap.scaled(
            icon_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        # Create list item with filename as text
        item = QListWidgetItem(path.name)

        # Set thumbnail as icon
        item.setIcon(QIcon(thumbnail))

        # Store full path in item data for later retrieval
        item.setData(Qt.ItemDataRole.UserRole, str(path))

        # Add item to list
        self.addItem(item)

        return True

    def remove_image(self, index: int) -> bool:
        """
        Remove an image from the file list.

        Args:
            index: Index of the image to remove

        Returns:
            True if image removed successfully, False otherwise
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
