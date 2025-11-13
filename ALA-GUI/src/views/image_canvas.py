"""
Image Canvas Widget for ALA-GUI.

M2: PyQt6 Image Display & Navigation - Canvas for displaying and manipulating images.
"""

from pathlib import Path
from typing import Optional

from PyQt6.QtCore import QPoint, QPointF, Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QPixmap, QWheelEvent
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QWidget


class ImageCanvas(QGraphicsView):
    """
    Image canvas widget using QGraphicsView and QGraphicsScene.

    Features:
    - Display images with QPixmap
    - Zoom in/out with mouse wheel
    - Pan with mouse drag
    - Fit to window
    - Coordinate transformation between canvas and image space
    - Performance optimized rendering

    Signals:
        imageLoaded(str): Emitted when image is successfully loaded
        zoomChanged(float): Emitted when zoom level changes
    """

    # Signals
    imageLoaded = pyqtSignal(str)  # Emits image path
    zoomChanged = pyqtSignal(float)  # Emits current zoom scale

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the image canvas.

        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)

        # Current image state
        self.current_image: Optional[str] = None
        self.current_pixmap_item: Optional[QGraphicsPixmapItem] = None
        self._image_size: Optional[tuple[int, int]] = None

        # Zoom settings
        self.zoom_factor = 1.15
        self.min_zoom = 0.1
        self.max_zoom = 10.0

        # Setup the canvas
        self._setup_canvas()

    def _setup_canvas(self) -> None:
        """Configure the canvas view and scene for optimal performance."""
        # Create and set up the scene
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)

        # Configure view settings for quality
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # Configure interaction
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        # Performance optimization: Use minimal viewport update
        self.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.MinimalViewportUpdate
        )

        # Optimize for static content (no animations)
        self.setOptimizationFlag(
            QGraphicsView.OptimizationFlag.DontAdjustForAntialiasing, True
        )

        # Configure viewport
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setBackgroundBrush(Qt.GlobalColor.darkGray)

        # Disable frame for performance
        self.setFrameShape(QGraphicsView.Shape.NoFrame)

    def load_image(self, image_path: str) -> bool:
        """
        Load an image from file path with error handling.

        Args:
            image_path: Path to the image file

        Returns:
            True if image loaded successfully, False otherwise

        Emits:
            imageLoaded: When image is successfully loaded
        """
        path = Path(image_path)
        if not path.exists() or not path.is_file():
            return False

        # Load the image as QPixmap
        pixmap = QPixmap(str(path))
        if pixmap.isNull():
            return False

        # Store image size
        self._image_size = (pixmap.width(), pixmap.height())

        # Clear existing image
        self._scene.clear()
        self.current_pixmap_item = None

        # Add pixmap to scene with caching enabled
        self.current_pixmap_item = self._scene.addPixmap(pixmap)
        self.current_pixmap_item.setCacheMode(
            QGraphicsPixmapItem.CacheMode.DeviceCoordinateCache
        )
        self.current_image = str(path)

        # Reset view and optimize scene rect
        self.resetTransform()
        rect = self.current_pixmap_item.boundingRect()
        self.setSceneRect(rect)
        self._scene.setSceneRect(rect)

        # Emit signal
        self.imageLoaded.emit(str(path))

        return True

    def zoom_in(self) -> None:
        """
        Zoom in on the image.

        Emits:
            zoomChanged: When zoom level changes
        """
        current_scale = self.transform().m11()
        new_scale = current_scale * self.zoom_factor

        if new_scale < self.max_zoom:
            self.scale(self.zoom_factor, self.zoom_factor)
            self.zoomChanged.emit(new_scale)

    def zoom_out(self) -> None:
        """
        Zoom out on the image.

        Emits:
            zoomChanged: When zoom level changes
        """
        current_scale = self.transform().m11()
        new_scale = current_scale / self.zoom_factor

        if new_scale > self.min_zoom:
            self.scale(1 / self.zoom_factor, 1 / self.zoom_factor)
            self.zoomChanged.emit(new_scale)

    def reset_zoom(self) -> None:
        """
        Reset zoom to 100% (1:1 scale).

        Emits:
            zoomChanged: When zoom level changes
        """
        self.resetTransform()
        self.zoomChanged.emit(1.0)

    def get_zoom_level(self) -> float:
        """
        Get current zoom level.

        Returns:
            Current zoom scale (1.0 = 100%)
        """
        return self.transform().m11()

    def get_image_size(self) -> Optional[tuple[int, int]]:
        """
        Get loaded image dimensions.

        Returns:
            Tuple of (width, height) or None if no image loaded
        """
        return self._image_size

    def fit_to_window(self) -> None:
        """Fit the image to the viewport."""
        if self.current_pixmap_item:
            self.fitInView(
                self.current_pixmap_item.boundingRect(),
                Qt.AspectRatioMode.KeepAspectRatio,
            )

    def wheelEvent(self, event: QWheelEvent) -> None:
        """
        Handle mouse wheel events for zooming with smooth scrolling.

        Args:
            event: Wheel event
        """
        # Only zoom if we have an image
        if not self.current_pixmap_item:
            event.ignore()
            return

        # Determine zoom direction
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()

        event.accept()

    def map_to_image(self, canvas_point: QPoint) -> Optional[QPoint]:
        """
        Map a canvas coordinate to image coordinate.

        Args:
            canvas_point: Point in canvas (viewport) coordinates

        Returns:
            Point in image coordinates, or None if no image loaded
        """
        if not self.current_pixmap_item:
            return None

        # Convert viewport coordinate to scene coordinate
        scene_point = self.mapToScene(canvas_point)

        # Convert scene coordinate to item (image) coordinate
        item_point = self.current_pixmap_item.mapFromScene(scene_point)

        return QPoint(int(item_point.x()), int(item_point.y()))

    def map_to_canvas(self, image_point: QPoint) -> QPoint:
        """
        Map an image coordinate to canvas coordinate.

        Args:
            image_point: Point in image coordinates

        Returns:
            Point in canvas (viewport) coordinates
        """
        if not self.current_pixmap_item:
            return QPoint(0, 0)

        # Convert item (image) coordinate to scene coordinate
        scene_point = self.current_pixmap_item.mapToScene(
            QPointF(image_point.x(), image_point.y())
        )

        # Convert scene coordinate to viewport coordinate
        viewport_point = self.mapFromScene(scene_point)

        return viewport_point
