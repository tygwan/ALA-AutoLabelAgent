"""
File List Widget for ALA-GUI.

M2: PyQt6 Image Display & Navigation - File list widget for managing images.
"""

from pathlib import Path
from typing import Optional

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QIcon, QPixmap, QPixmapCache
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

        # Enable drag-and-drop for importing images
        self.setAcceptDrops(True)

    def add_image(self, image_path: str) -> bool:
        """
        Add an image to the file list with thumbnail.

        Uses QPixmapCache to cache thumbnails for improved performance.

        Args:
            image_path: Path to the image file

        Returns:
            True if image added successfully, False otherwise
        """
        # Validate file exists
        path = Path(image_path)
        if not path.exists() or not path.is_file():
            return False

        # Generate cache key for this image
        cache_key = self._get_cache_key(str(path))

        # Try to get thumbnail from cache
        thumbnail = QPixmapCache.find(cache_key)

        if thumbnail is None:
            # Not in cache - load image and generate thumbnail
            pixmap = QPixmap(str(path))
            if pixmap.isNull():
                # Not a valid image file
                return False

            # Generate thumbnail
            thumbnail = self._generate_thumbnail(pixmap)

            # Store thumbnail in cache
            QPixmapCache.insert(cache_key, thumbnail)

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

    def get_current_image_path(self) -> Optional[str]:
        """
        Get the full path of the currently selected image.

        Returns:
            Full path to the selected image, or None if no selection
        """
        current_item = self.currentItem()
        if current_item is None:
            return None

        # Retrieve full path from item data
        path = current_item.data(Qt.ItemDataRole.UserRole)
        return path

    def select_previous_image(self) -> bool:
        """
        Select the previous image in the list.

        Returns:
            True if selection changed, False if already at first image
        """
        current_row = self.currentRow()
        if current_row > 0:
            self.setCurrentRow(current_row - 1)
            return True
        return False

    def select_next_image(self) -> bool:
        """
        Select the next image in the list.

        Returns:
            True if selection changed, False if already at last image
        """
        current_row = self.currentRow()
        if current_row < self.count() - 1:
            self.setCurrentRow(current_row + 1)
            return True
        return False

    def _get_cache_key(self, image_path: str) -> str:
        """
        Generate a cache key for an image path.

        Args:
            image_path: Path to the image file

        Returns:
            Cache key string
        """
        # Use the absolute path as cache key for consistency
        return f"thumbnail_{Path(image_path).resolve()}"

    def _generate_thumbnail(self, pixmap: QPixmap) -> QPixmap:
        """
        Generate a thumbnail from a pixmap.

        Args:
            pixmap: Source pixmap

        Returns:
            Thumbnail pixmap scaled to icon size
        """
        icon_size = self.iconSize()
        return pixmap.scaled(
            icon_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """
        Handle drag enter events to accept file drops.

        Args:
            event: The drag enter event
        """
        # Accept event if it contains URLs (file paths)
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        """
        Handle drop events to add dropped image files.

        Args:
            event: The drop event
        """
        # Get URLs from mime data
        mime_data = event.mimeData()
        if not mime_data.hasUrls():
            event.ignore()
            return

        # Process each dropped file
        for url in mime_data.urls():
            # Convert URL to local file path
            file_path = url.toLocalFile()
            if file_path:
                # Try to add the image (will validate if it's a valid image)
                self.add_image(file_path)

        # Accept the drop event
        event.acceptProposedAction()

    def get_all_image_paths(self) -> list[str]:
        """
        Get all image paths in the list.

        Returns:
            List of all image file paths
        """
        image_paths = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item:
                path_str = item.data(Qt.ItemDataRole.UserRole)
                if path_str:
                    image_paths.append(str(path_str))
        return image_paths
