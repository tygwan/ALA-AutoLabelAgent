"""
Integration tests for ImageCanvas interactions.

M2: PyQt6 Image Display & Navigation - Canvas interaction testing.
"""

import pytest
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QColor, QImage

# Mark all tests in this module as GUI tests
pytestmark = pytest.mark.gui


@pytest.fixture
def image_canvas(qtbot):
    """
    Fixture to create ImageCanvas instance for integration testing.

    Args:
        qtbot: pytest-qt fixture for Qt widget testing

    Returns:
        ImageCanvas instance
    """
    from views.image_canvas import ImageCanvas

    canvas = ImageCanvas()
    qtbot.addWidget(canvas)
    return canvas


@pytest.fixture
def test_image(tmp_path):
    """
    Create a test image file.

    Args:
        tmp_path: pytest tmp_path fixture

    Returns:
        Path to test image
    """
    # Create a simple test image
    test_image = QImage(200, 150, QImage.Format.Format_RGB32)
    test_image.fill(QColor(100, 150, 200))  # Fill with blue

    # Add some variation for testing
    for y in range(50):
        for x in range(200):
            test_image.setPixel(x, y, QColor(255, 0, 0).rgb())  # Red stripe

    image_path = tmp_path / "test_image.png"
    test_image.save(str(image_path))

    return image_path


class TestImageCanvasImageLoading:
    """Integration tests for image loading functionality."""

    def test_load_valid_image(self, image_canvas, test_image, qtbot):
        """Test loading a valid image file."""
        # Capture signal
        with qtbot.waitSignal(image_canvas.imageLoaded, timeout=1000):
            result = image_canvas.load_image(str(test_image))

        assert result is True
        assert image_canvas.current_image == str(test_image)
        assert image_canvas.current_pixmap_item is not None
        assert image_canvas.get_image_size() == (200, 150)

    def test_load_nonexistent_image(self, image_canvas):
        """Test loading a nonexistent image returns False."""
        result = image_canvas.load_image("/nonexistent/path.png")
        assert result is False
        assert image_canvas.current_image is None
        assert image_canvas.get_image_size() is None

    def test_load_multiple_images_sequentially(
        self, image_canvas, test_image, tmp_path, qtbot
    ):
        """Test loading multiple images replaces previous image."""
        # Load first image
        image_canvas.load_image(str(test_image))

        # Create second image
        second_image = QImage(300, 200, QImage.Format.Format_RGB32)
        second_image.fill(QColor(0, 255, 0))
        second_path = tmp_path / "test_image2.png"
        second_image.save(str(second_path))

        # Load second image
        with qtbot.waitSignal(image_canvas.imageLoaded, timeout=1000):
            result = image_canvas.load_image(str(second_path))

        assert result is True
        assert image_canvas.current_image == str(second_path)
        assert image_canvas.get_image_size() == (300, 200)

    def test_scene_cleared_on_new_image(
        self, image_canvas, test_image, tmp_path, qtbot
    ):
        """Test that scene is cleared when loading new image."""
        # Load first image
        image_canvas.load_image(str(test_image))
        first_item_count = len(image_canvas.scene().items())

        # Load second image
        second_image = QImage(100, 100, QImage.Format.Format_RGB32)
        second_image.fill(QColor(255, 255, 0))
        second_path = tmp_path / "test_image3.png"
        second_image.save(str(second_path))

        image_canvas.load_image(str(second_path))

        # Should still have same number of items (just one pixmap)
        assert len(image_canvas.scene().items()) == first_item_count


class TestImageCanvasZoomInteractions:
    """Integration tests for zoom functionality."""

    def test_zoom_in_increases_scale(self, image_canvas, test_image, qtbot):
        """Test that zoom in increases scale factor."""
        image_canvas.load_image(str(test_image))

        initial_zoom = image_canvas.get_zoom_level()

        with qtbot.waitSignal(image_canvas.zoomChanged, timeout=1000):
            image_canvas.zoom_in()

        new_zoom = image_canvas.get_zoom_level()
        assert new_zoom > initial_zoom

    def test_zoom_out_decreases_scale(self, image_canvas, test_image, qtbot):
        """Test that zoom out decreases scale factor."""
        image_canvas.load_image(str(test_image))

        # Zoom in first so we can zoom out
        image_canvas.zoom_in()
        current_zoom = image_canvas.get_zoom_level()

        with qtbot.waitSignal(image_canvas.zoomChanged, timeout=1000):
            image_canvas.zoom_out()

        new_zoom = image_canvas.get_zoom_level()
        assert new_zoom < current_zoom

    def test_reset_zoom_returns_to_100_percent(self, image_canvas, test_image, qtbot):
        """Test that reset zoom returns to 1.0 scale."""
        image_canvas.load_image(str(test_image))

        # Zoom in multiple times
        image_canvas.zoom_in()
        image_canvas.zoom_in()
        image_canvas.zoom_in()

        with qtbot.waitSignal(image_canvas.zoomChanged, timeout=1000):
            image_canvas.reset_zoom()

        zoom = image_canvas.get_zoom_level()
        assert abs(zoom - 1.0) < 0.01  # Should be very close to 1.0

    def test_zoom_respects_max_limit(self, image_canvas, test_image):
        """Test that zoom cannot exceed maximum."""
        image_canvas.load_image(str(test_image))

        # Try to zoom beyond max
        for _ in range(50):
            image_canvas.zoom_in()

        zoom = image_canvas.get_zoom_level()
        assert zoom <= image_canvas.max_zoom

    def test_zoom_respects_min_limit(self, image_canvas, test_image):
        """Test that zoom cannot go below minimum."""
        image_canvas.load_image(str(test_image))

        # Try to zoom below min
        for _ in range(50):
            image_canvas.zoom_out()

        zoom = image_canvas.get_zoom_level()
        assert zoom >= image_canvas.min_zoom

    def test_zoom_signals_emitted(self, image_canvas, test_image, qtbot):
        """Test that zoom operations emit signals."""
        image_canvas.load_image(str(test_image))

        # Test zoom in signal
        with qtbot.waitSignal(image_canvas.zoomChanged, timeout=1000) as blocker:
            image_canvas.zoom_in()

        # Signal should contain new zoom level
        assert len(blocker.args) == 1
        assert isinstance(blocker.args[0], float)


class TestImageCanvasFitToWindow:
    """Integration tests for fit-to-window functionality."""

    def test_fit_to_window_scales_image(self, image_canvas, test_image):
        """Test that fit to window scales image appropriately."""
        image_canvas.load_image(str(test_image))

        # Set a specific viewport size
        image_canvas.resize(400, 300)

        # Zoom in first
        image_canvas.zoom_in()
        image_canvas.zoom_in()

        # Fit to window
        image_canvas.fit_to_window()

        # Zoom should have changed from the zoomed-in state
        zoom = image_canvas.get_zoom_level()
        # Should be less than 2.0 (which would be zoomed in)
        assert zoom < 2.0

    def test_fit_to_window_with_no_image(self, image_canvas):
        """Test that fit to window handles no image gracefully."""
        # Should not crash
        image_canvas.fit_to_window()
        assert image_canvas.current_pixmap_item is None


class TestImageCanvasCoordinateMapping:
    """Integration tests for coordinate transformation."""

    def test_map_to_image_coordinates(self, image_canvas, test_image):
        """Test mapping canvas to image coordinates."""
        image_canvas.load_image(str(test_image))
        image_canvas.reset_zoom()  # Ensure 1:1 scale

        # Map a point
        canvas_point = QPoint(50, 50)
        image_point = image_canvas.map_to_image(canvas_point)

        assert image_point is not None
        assert isinstance(image_point, QPoint)

    def test_map_to_canvas_coordinates(self, image_canvas, test_image):
        """Test mapping image to canvas coordinates."""
        image_canvas.load_image(str(test_image))
        image_canvas.reset_zoom()

        # Map a point
        image_point = QPoint(100, 75)
        canvas_point = image_canvas.map_to_canvas(image_point)

        assert canvas_point is not None
        assert isinstance(canvas_point, QPoint)

    def test_map_to_image_with_no_image(self, image_canvas):
        """Test coordinate mapping with no image returns None."""
        result = image_canvas.map_to_image(QPoint(50, 50))
        assert result is None

    def test_map_to_canvas_with_no_image(self, image_canvas):
        """Test reverse mapping with no image returns origin."""
        result = image_canvas.map_to_canvas(QPoint(100, 100))
        assert result == QPoint(0, 0)

    def test_coordinate_round_trip(self, image_canvas, test_image):
        """Test that coordinate mapping is consistent."""
        image_canvas.load_image(str(test_image))
        image_canvas.reset_zoom()

        # Original point
        original_image_point = QPoint(100, 75)

        # Map to canvas and back
        canvas_point = image_canvas.map_to_canvas(original_image_point)
        back_to_image = image_canvas.map_to_image(canvas_point)

        # Should be close to original (may have small rounding errors)
        assert back_to_image is not None
        assert abs(back_to_image.x() - original_image_point.x()) < 2
        assert abs(back_to_image.y() - original_image_point.y()) < 2


class TestImageCanvasWheelZoom:
    """Integration tests for mouse wheel zoom."""

    def test_wheel_event_without_image(self, image_canvas, qtbot):
        """Test that wheel events are ignored without an image."""
        from PyQt6.QtCore import QPointF
        from PyQt6.QtGui import QWheelEvent

        # Create a wheel event
        event = QWheelEvent(
            QPointF(100, 100),  # position
            QPointF(100, 100),  # global position
            QPoint(0, 120),  # pixel delta
            QPoint(0, 120),  # angle delta
            Qt.MouseButton.NoButton,
            Qt.KeyboardModifier.NoModifier,
            Qt.ScrollPhase.ScrollUpdate,
            False,  # inverted
        )

        # Should not crash
        image_canvas.wheelEvent(event)
        assert image_canvas.current_pixmap_item is None


class TestImageCanvasPerformance:
    """Integration tests for performance optimizations."""

    def test_viewport_update_mode_is_minimal(self, image_canvas):
        """Test that viewport uses minimal update mode."""
        from PyQt6.QtWidgets import QGraphicsView

        assert (
            image_canvas.viewportUpdateMode()
            == QGraphicsView.ViewportUpdateMode.MinimalViewportUpdate
        )

    def test_pixmap_item_has_caching(self, image_canvas, test_image):
        """Test that loaded pixmap item uses caching."""
        from PyQt6.QtWidgets import QGraphicsPixmapItem

        image_canvas.load_image(str(test_image))

        assert image_canvas.current_pixmap_item is not None
        assert (
            image_canvas.current_pixmap_item.cacheMode()
            == QGraphicsPixmapItem.CacheMode.DeviceCoordinateCache
        )

    def test_optimization_flags_set(self, image_canvas):
        """Test that optimization flags are configured."""
        from PyQt6.QtWidgets import QGraphicsView

        # Check that DontAdjustForAntialiasing is enabled
        flags = image_canvas.optimizationFlags()
        assert flags & QGraphicsView.OptimizationFlag.DontAdjustForAntialiasing


class TestImageCanvasState:
    """Integration tests for canvas state management."""

    def test_initial_state(self, image_canvas):
        """Test that canvas starts in correct initial state."""
        assert image_canvas.current_image is None
        assert image_canvas.current_pixmap_item is None
        assert image_canvas.get_image_size() is None
        assert image_canvas.get_zoom_level() == 1.0

    def test_state_after_image_load(self, image_canvas, test_image):
        """Test that state is correct after loading image."""
        image_canvas.load_image(str(test_image))

        assert image_canvas.current_image == str(test_image)
        assert image_canvas.current_pixmap_item is not None
        assert image_canvas.get_image_size() == (200, 150)
        assert image_canvas.get_zoom_level() == 1.0  # Reset to 1.0 on load

    def test_state_after_zoom_operations(self, image_canvas, test_image):
        """Test that state tracks zoom level correctly."""
        image_canvas.load_image(str(test_image))

        initial_zoom = image_canvas.get_zoom_level()
        image_canvas.zoom_in()
        zoomed_in = image_canvas.get_zoom_level()
        image_canvas.reset_zoom()
        reset_zoom = image_canvas.get_zoom_level()

        assert zoomed_in > initial_zoom
        assert abs(reset_zoom - 1.0) < 0.01
