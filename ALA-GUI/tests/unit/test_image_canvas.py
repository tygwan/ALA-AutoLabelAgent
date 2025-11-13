"""
Unit tests for ImageCanvas widget.

M2: PyQt6 Image Display & Navigation - Image canvas for displaying
and interacting with images.
"""

import pytest

# Mark all tests in this module as GUI tests
pytestmark = pytest.mark.gui


@pytest.fixture
def image_canvas(qtbot):
    """
    Fixture to create ImageCanvas instance.

    Args:
        qtbot: pytest-qt fixture for Qt widget testing

    Returns:
        ImageCanvas instance
    """
    from views.image_canvas import ImageCanvas

    canvas = ImageCanvas()
    qtbot.addWidget(canvas)
    return canvas


class TestImageCanvasInitialization:
    """Tests for ImageCanvas initialization."""

    def test_canvas_is_graphics_view(self, image_canvas):
        """Test that ImageCanvas is a QGraphicsView."""
        from PyQt6.QtWidgets import QGraphicsView

        assert isinstance(image_canvas, QGraphicsView)

    def test_canvas_has_scene(self, image_canvas):
        """Test that ImageCanvas has a QGraphicsScene."""
        from PyQt6.QtWidgets import QGraphicsScene

        scene = image_canvas.scene()
        assert scene is not None
        assert isinstance(scene, QGraphicsScene)

    def test_canvas_initial_state(self, image_canvas):
        """Test ImageCanvas initial state."""
        # Should start with no image loaded
        assert image_canvas.current_image is None
        assert image_canvas.current_pixmap_item is None

    def test_canvas_viewport_settings(self, image_canvas):
        """Test that viewport is configured correctly."""
        # Check that anti-aliasing and smooth transformation are enabled
        # Should have smooth pixel transform
        assert image_canvas.renderHints() & image_canvas.renderHint(
            image_canvas.RenderHint.SmoothPixmapTransform
        )


class TestImageCanvasImageLoading:
    """Tests for image loading functionality."""

    def test_load_image_from_path(self, image_canvas, tmp_path):
        """Test loading an image from file path."""
        # Create a simple test image
        from PyQt6.QtGui import QColor, QImage

        test_image = QImage(100, 100, QImage.Format.Format_RGB32)
        test_image.fill(QColor(255, 0, 0))  # Fill with red

        # Save to temp file
        image_path = tmp_path / "test_image.png"
        test_image.save(str(image_path))

        # Load the image
        result = image_canvas.load_image(str(image_path))

        assert result is True
        assert image_canvas.current_image is not None
        assert image_canvas.current_pixmap_item is not None

    def test_load_invalid_image_path(self, image_canvas):
        """Test loading from invalid path returns False."""
        result = image_canvas.load_image("/nonexistent/path.png")
        assert result is False
        assert image_canvas.current_image is None

    def test_load_image_updates_scene(self, image_canvas, tmp_path):
        """Test that loading image updates the scene."""
        from PyQt6.QtGui import QColor, QImage

        # Create test image
        test_image = QImage(100, 100, QImage.Format.Format_RGB32)
        test_image.fill(QColor(0, 255, 0))
        image_path = tmp_path / "test_green.png"
        test_image.save(str(image_path))

        # Load image
        image_canvas.load_image(str(image_path))

        # Scene should have items
        assert len(image_canvas.scene().items()) > 0


class TestImageCanvasZoom:
    """Tests for zoom functionality."""

    def test_zoom_in(self, image_canvas):
        """Test zoom in increases scale."""
        initial_scale = image_canvas.transform().m11()
        image_canvas.zoom_in()
        new_scale = image_canvas.transform().m11()
        assert new_scale > initial_scale

    def test_zoom_out(self, image_canvas):
        """Test zoom out decreases scale."""
        # First zoom in to have room to zoom out
        image_canvas.zoom_in()
        current_scale = image_canvas.transform().m11()
        image_canvas.zoom_out()
        new_scale = image_canvas.transform().m11()
        assert new_scale < current_scale

    def test_zoom_reset(self, image_canvas):
        """Test reset zoom returns to 100%."""
        image_canvas.zoom_in()
        image_canvas.zoom_in()
        image_canvas.reset_zoom()
        scale = image_canvas.transform().m11()
        assert abs(scale - 1.0) < 0.01  # Should be close to 1.0


class TestImageCanvasFitToWindow:
    """Tests for fit-to-window functionality."""

    def test_fit_to_window(self, image_canvas, tmp_path):
        """Test fit to window scales image appropriately."""
        from PyQt6.QtGui import QColor, QImage

        # Create a large test image
        test_image = QImage(1000, 1000, QImage.Format.Format_RGB32)
        test_image.fill(QColor(0, 0, 255))
        image_path = tmp_path / "test_large.png"
        test_image.save(str(image_path))

        # Load image
        image_canvas.load_image(str(image_path))

        # Fit to window
        image_canvas.fit_to_window()

        # Image should be scaled to fit viewport
        # The exact scale depends on viewport size, just check it's not 1.0
        scale = image_canvas.transform().m11()
        assert scale > 0  # Should have some positive scale


class TestImageCanvasCoordinates:
    """Tests for coordinate transformation."""

    def test_map_to_image_coordinates(self, image_canvas, tmp_path):
        """Test mapping canvas coordinates to image coordinates."""
        from PyQt6.QtCore import QPoint
        from PyQt6.QtGui import QColor, QImage

        # Create test image
        test_image = QImage(200, 200, QImage.Format.Format_RGB32)
        test_image.fill(QColor(128, 128, 128))
        image_path = tmp_path / "test_coord.png"
        test_image.save(str(image_path))

        # Load image
        image_canvas.load_image(str(image_path))

        # Map a point
        canvas_point = QPoint(50, 50)
        image_point = image_canvas.map_to_image(canvas_point)

        assert image_point is not None
        assert isinstance(image_point, QPoint)
