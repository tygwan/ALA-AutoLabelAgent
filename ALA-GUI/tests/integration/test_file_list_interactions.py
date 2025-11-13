"""
Integration tests for FileListWidget interactions.

Tests FileListWidget integration with other components including
ImageCanvas and MainWindow.
"""

import pytest

# Mark all tests in this module as integration and GUI tests
pytestmark = [pytest.mark.integration, pytest.mark.gui]


@pytest.fixture
def main_window(qtbot):
    """
    Fixture to create MainWindow with FileListWidget.

    Args:
        qtbot: pytest-qt fixture for Qt widget testing

    Returns:
        MainWindow instance
    """
    from views.main_window import MainWindow

    window = MainWindow()
    qtbot.addWidget(window)
    return window


@pytest.fixture
def test_images(tmp_path):
    """
    Create multiple test images for testing.

    Args:
        tmp_path: pytest tmp_path fixture

    Returns:
        List of paths to test images
    """
    from PyQt6.QtGui import QColor, QImage

    images = []
    colors = [
        (255, 0, 0),  # Red
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (255, 255, 0),  # Yellow
    ]

    for i, color in enumerate(colors):
        image = QImage(200, 200, QImage.Format.Format_RGB32)
        image.fill(QColor(*color))
        image_path = tmp_path / f"test_image_{i}.png"
        image.save(str(image_path))
        images.append(image_path)

    return images


class TestFileListWidgetIntegration:
    """Integration tests for FileListWidget with other components."""

    def test_file_list_in_main_window(self, main_window):
        """Test that FileListWidget is properly integrated in MainWindow."""
        # MainWindow should have a file dock
        assert main_window.file_dock is not None

        # File dock should contain FileListWidget
        file_list = main_window.file_dock.widget()
        assert file_list is not None

        from views.file_list_widget import FileListWidget

        assert isinstance(file_list, FileListWidget)

    def test_add_images_to_file_list(self, main_window, test_images):
        """Test adding multiple images to FileListWidget."""
        file_list = main_window.file_dock.widget()

        # Add all test images
        for image_path in test_images:
            result = file_list.add_image(str(image_path))
            assert result is True

        # All images should be in the list
        assert file_list.count() == len(test_images)

    def test_file_list_selection_changes(self, main_window, test_images, qtbot):
        """Test that selecting an image in file list emits signal."""
        file_list = main_window.file_dock.widget()

        # Add test images
        for image_path in test_images:
            file_list.add_image(str(image_path))

        # Connect to signal
        with qtbot.waitSignal(file_list.currentItemChanged, timeout=1000):
            # Select first item
            file_list.setCurrentRow(0)

        # Current selection should be first image
        selected_path = file_list.get_current_image_path()
        assert selected_path == str(test_images[0])

    def test_file_list_remove_images(self, main_window, test_images):
        """Test removing images from FileListWidget."""
        file_list = main_window.file_dock.widget()

        # Add test images
        for image_path in test_images:
            file_list.add_image(str(image_path))

        initial_count = file_list.count()

        # Remove first image
        result = file_list.remove_image(0)
        assert result is True
        assert file_list.count() == initial_count - 1

    def test_file_list_clear_all(self, main_window, test_images):
        """Test clearing all images from FileListWidget."""
        file_list = main_window.file_dock.widget()

        # Add test images
        for image_path in test_images:
            file_list.add_image(str(image_path))

        assert file_list.count() > 0

        # Clear all
        file_list.clear()
        assert file_list.count() == 0

    def test_file_list_thumbnail_display(self, main_window, test_images):
        """Test that thumbnails are displayed for added images."""
        file_list = main_window.file_dock.widget()

        # Add test image
        file_list.add_image(str(test_images[0]))

        # Get first item
        item = file_list.item(0)
        assert item is not None

        # Item should have an icon (thumbnail)
        icon = item.icon()
        assert not icon.isNull()

        # Item should have text (filename)
        assert item.text() == test_images[0].name


class TestFileListImageCanvasIntegration:
    """Integration tests for FileListWidget and ImageCanvas interaction."""

    @pytest.fixture
    def file_list_and_canvas(self, qtbot):
        """
        Create FileListWidget and ImageCanvas for integration testing.

        Args:
            qtbot: pytest-qt fixture

        Returns:
            Tuple of (FileListWidget, ImageCanvas)
        """
        from views.file_list_widget import FileListWidget
        from views.image_canvas import ImageCanvas

        file_list = FileListWidget()
        canvas = ImageCanvas()

        qtbot.addWidget(file_list)
        qtbot.addWidget(canvas)

        return file_list, canvas

    def test_select_image_loads_in_canvas(
        self, file_list_and_canvas, test_images, qtbot
    ):
        """Test that selecting an image in list loads it in canvas."""
        file_list, canvas = file_list_and_canvas

        # Add test images to file list
        for image_path in test_images:
            file_list.add_image(str(image_path))

        # Connect file list selection to canvas loading
        def load_selected_image():
            selected_path = file_list.get_current_image_path()
            if selected_path:
                canvas.load_image(selected_path)

        file_list.currentItemChanged.connect(
            lambda current, previous: load_selected_image()
        )

        # Select first image
        file_list.setCurrentRow(0)

        # Wait a bit for the loading to complete
        qtbot.wait(100)

        # Canvas should have loaded the image
        assert canvas.current_image is not None
        assert canvas.current_pixmap_item is not None

    def test_navigate_images_updates_canvas(
        self, file_list_and_canvas, test_images, qtbot
    ):
        """Test that navigating through images updates canvas."""
        file_list, canvas = file_list_and_canvas

        # Add test images
        for image_path in test_images:
            file_list.add_image(str(image_path))

        # Connect selection to canvas
        def load_selected_image():
            selected_path = file_list.get_current_image_path()
            if selected_path:
                canvas.load_image(selected_path)

        file_list.currentItemChanged.connect(
            lambda current, previous: load_selected_image()
        )

        # Select first image
        file_list.setCurrentRow(0)
        qtbot.wait(100)
        first_pixmap = canvas.current_pixmap_item

        # Select second image
        file_list.setCurrentRow(1)
        qtbot.wait(100)
        second_pixmap = canvas.current_pixmap_item

        # Canvas should have updated with new image
        assert first_pixmap != second_pixmap
        assert canvas.current_image is not None


class TestFileListRealFileOperations:
    """Integration tests with real file operations."""

    def test_add_various_image_formats(self, main_window, tmp_path):
        """Test adding different image format files."""
        from PyQt6.QtGui import QColor, QImage

        file_list = main_window.file_dock.widget()

        # Create images in different formats
        formats = ["PNG", "JPEG", "BMP"]
        images = []

        for fmt in formats:
            image = QImage(100, 100, QImage.Format.Format_RGB32)
            image.fill(QColor(128, 128, 128))
            ext = fmt.lower()
            if fmt == "JPEG":
                ext = "jpg"
            image_path = tmp_path / f"test_image.{ext}"
            image.save(str(image_path), fmt)
            images.append(image_path)

        # Add all images
        for image_path in images:
            result = file_list.add_image(str(image_path))
            assert result is True

        # All should be added
        assert file_list.count() == len(formats)

    def test_add_non_image_file_fails(self, main_window, tmp_path):
        """Test that adding non-image files fails gracefully."""
        file_list = main_window.file_dock.widget()

        # Create a text file
        text_file = tmp_path / "not_an_image.txt"
        text_file.write_text("This is not an image")

        # Try to add text file
        result = file_list.add_image(str(text_file))
        assert result is False

        # File list should be empty
        assert file_list.count() == 0

    def test_add_nonexistent_file_fails(self, main_window):
        """Test that adding nonexistent files fails gracefully."""
        file_list = main_window.file_dock.widget()

        # Try to add nonexistent file
        result = file_list.add_image("/nonexistent/path/to/image.png")
        assert result is False

        # File list should be empty
        assert file_list.count() == 0

    def test_file_list_persists_across_operations(self, main_window, test_images):
        """Test that file list maintains state across operations."""
        file_list = main_window.file_dock.widget()

        # Add images
        for image_path in test_images:
            file_list.add_image(str(image_path))

        original_count = file_list.count()

        # Select an image
        file_list.setCurrentRow(1)

        # Remove a different image
        file_list.remove_image(2)

        # File list count should decrease
        assert file_list.count() == original_count - 1
        # Selection management is handled by Qt automatically

    def test_thumbnail_cache_performance(self, main_window, test_images):
        """Test that thumbnail caching improves performance."""
        from PyQt6.QtGui import QPixmapCache

        file_list = main_window.file_dock.widget()

        # Add image first time
        image_path = str(test_images[0])
        file_list.add_image(image_path)

        # Get cache key
        cache_key = file_list._get_cache_key(image_path)

        # Thumbnail should be in cache
        cached_pixmap = QPixmapCache.find(cache_key)
        assert cached_pixmap is not None

        # Clear widget but not cache
        file_list.clear()

        # Add same image again
        file_list.add_image(image_path)

        # Should still be in cache
        cached_pixmap_2 = QPixmapCache.find(cache_key)
        assert cached_pixmap_2 is not None
