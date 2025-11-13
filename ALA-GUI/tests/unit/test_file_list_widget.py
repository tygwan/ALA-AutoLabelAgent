"""
Unit tests for FileListWidget.

M2: PyQt6 Image Display & Navigation - File list widget for managing images.
"""

import pytest

# Mark all tests in this module as GUI tests
pytestmark = pytest.mark.gui


@pytest.fixture
def file_list_widget(qtbot):
    """
    Fixture to create FileListWidget instance.

    Args:
        qtbot: pytest-qt fixture for Qt widget testing

    Returns:
        FileListWidget instance
    """
    from views.file_list_widget import FileListWidget

    widget = FileListWidget()
    qtbot.addWidget(widget)
    return widget


class TestFileListWidgetInitialization:
    """Tests for FileListWidget initialization."""

    def test_widget_is_qlistwidget(self, file_list_widget):
        """Test that FileListWidget is a QListWidget."""
        from PyQt6.QtWidgets import QListWidget

        assert isinstance(file_list_widget, QListWidget)

    def test_widget_initial_state(self, file_list_widget):
        """Test FileListWidget initial state."""
        # Should start with no items
        assert file_list_widget.count() == 0

    def test_widget_view_mode(self, file_list_widget):
        """Test that widget is in icon view mode for thumbnails."""
        from PyQt6.QtWidgets import QListWidget

        assert file_list_widget.viewMode() == QListWidget.ViewMode.IconMode

    def test_widget_icon_size(self, file_list_widget):
        """Test that widget has appropriate icon size for thumbnails."""
        # Should have icon size set for thumbnails (e.g., 128x128)
        icon_size = file_list_widget.iconSize()
        assert icon_size.width() > 0
        assert icon_size.height() > 0
        # Reasonable thumbnail size
        assert 64 <= icon_size.width() <= 256
        assert 64 <= icon_size.height() <= 256

    def test_widget_selection_mode(self, file_list_widget):
        """Test that widget allows single selection."""
        from PyQt6.QtWidgets import QAbstractItemView

        assert (
            file_list_widget.selectionMode()
            == QAbstractItemView.SelectionMode.SingleSelection
        )


@pytest.fixture
def test_image(tmp_path):
    """
    Create a test image file.

    Args:
        tmp_path: pytest tmp_path fixture

    Returns:
        Path to test image
    """
    from PyQt6.QtGui import QColor, QImage

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


class TestFileListWidgetAddImage:
    """Tests for add_image() functionality."""

    def test_add_image_returns_true_for_valid_image(self, file_list_widget, test_image):
        """Test that add_image returns True for valid image."""
        result = file_list_widget.add_image(str(test_image))
        assert result is True

    def test_add_image_increases_item_count(self, file_list_widget, test_image):
        """Test that add_image increases the item count."""
        initial_count = file_list_widget.count()
        file_list_widget.add_image(str(test_image))
        assert file_list_widget.count() == initial_count + 1

    def test_add_image_sets_item_text_to_filename(self, file_list_widget, test_image):
        """Test that added image item has filename as text."""
        file_list_widget.add_image(str(test_image))
        item = file_list_widget.item(0)
        assert item is not None
        assert item.text() == "test_image.png"

    def test_add_image_sets_thumbnail_icon(self, file_list_widget, test_image):
        """Test that added image item has a thumbnail icon."""
        file_list_widget.add_image(str(test_image))
        item = file_list_widget.item(0)
        assert item is not None
        assert not item.icon().isNull()

    def test_add_image_stores_full_path_in_data(self, file_list_widget, test_image):
        """Test that full image path is stored in item data."""
        from PyQt6.QtCore import Qt

        file_list_widget.add_image(str(test_image))
        item = file_list_widget.item(0)
        assert item is not None
        stored_path = item.data(Qt.ItemDataRole.UserRole)
        assert stored_path == str(test_image)

    def test_add_image_returns_false_for_nonexistent_file(self, file_list_widget):
        """Test that add_image returns False for nonexistent file."""
        result = file_list_widget.add_image("/nonexistent/path/image.png")
        assert result is False
        assert file_list_widget.count() == 0

    def test_add_image_returns_false_for_invalid_image(
        self, file_list_widget, tmp_path
    ):
        """Test that add_image returns False for invalid image file."""
        # Create a non-image file
        text_file = tmp_path / "not_an_image.txt"
        text_file.write_text("This is not an image")

        result = file_list_widget.add_image(str(text_file))
        assert result is False
        assert file_list_widget.count() == 0

    def test_add_multiple_images(self, file_list_widget, tmp_path):
        """Test adding multiple images."""
        from PyQt6.QtGui import QColor, QImage

        # Create multiple test images
        images = []
        for i in range(3):
            img = QImage(100, 100, QImage.Format.Format_RGB32)
            img.fill(QColor(i * 50, i * 50, 255))
            path = tmp_path / f"image_{i}.png"
            img.save(str(path))
            images.append(path)

        # Add all images
        for img_path in images:
            result = file_list_widget.add_image(str(img_path))
            assert result is True

        # Verify count
        assert file_list_widget.count() == 3

        # Verify each image has correct filename
        for i in range(3):
            item = file_list_widget.item(i)
            assert item.text() == f"image_{i}.png"


class TestFileListWidgetRemoveImage:
    """Tests for remove_image() functionality."""

    def test_remove_image_returns_true_for_valid_index(
        self, file_list_widget, test_image
    ):
        """Test that remove_image returns True for valid index."""
        file_list_widget.add_image(str(test_image))
        result = file_list_widget.remove_image(0)
        assert result is True

    def test_remove_image_decreases_item_count(self, file_list_widget, test_image):
        """Test that remove_image decreases the item count."""
        file_list_widget.add_image(str(test_image))
        initial_count = file_list_widget.count()
        file_list_widget.remove_image(0)
        assert file_list_widget.count() == initial_count - 1

    def test_remove_image_returns_false_for_invalid_index(self, file_list_widget):
        """Test that remove_image returns False for invalid index."""
        result = file_list_widget.remove_image(0)
        assert result is False

    def test_remove_image_returns_false_for_negative_index(
        self, file_list_widget, test_image
    ):
        """Test that remove_image returns False for negative index."""
        file_list_widget.add_image(str(test_image))
        result = file_list_widget.remove_image(-1)
        assert result is False

    def test_remove_image_returns_false_for_out_of_bounds_index(
        self, file_list_widget, test_image
    ):
        """Test that remove_image returns False for out of bounds index."""
        file_list_widget.add_image(str(test_image))
        result = file_list_widget.remove_image(10)
        assert result is False

    def test_remove_multiple_images(self, file_list_widget, tmp_path):
        """Test removing multiple images."""
        from PyQt6.QtGui import QColor, QImage

        # Create and add multiple images
        for i in range(3):
            img = QImage(100, 100, QImage.Format.Format_RGB32)
            img.fill(QColor(i * 50, i * 50, 255))
            path = tmp_path / f"image_{i}.png"
            img.save(str(path))
            file_list_widget.add_image(str(path))

        # Remove middle image
        result = file_list_widget.remove_image(1)
        assert result is True
        assert file_list_widget.count() == 2

        # Verify remaining images
        assert file_list_widget.item(0).text() == "image_0.png"
        assert file_list_widget.item(1).text() == "image_2.png"
