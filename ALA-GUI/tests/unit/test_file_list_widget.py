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


class TestFileListWidgetSelection:
    """Tests for image selection functionality."""

    def test_get_current_image_path_returns_none_when_no_selection(
        self, file_list_widget
    ):
        """Test that get_current_image_path returns None with no selection."""
        result = file_list_widget.get_current_image_path()
        assert result is None

    def test_get_current_image_path_returns_path_when_selected(
        self, file_list_widget, test_image
    ):
        """Test that get_current_image_path returns path when image selected."""
        file_list_widget.add_image(str(test_image))
        file_list_widget.setCurrentRow(0)
        result = file_list_widget.get_current_image_path()
        assert result == str(test_image)

    def test_selection_changed_signal_emitted(
        self, file_list_widget, test_image, qtbot
    ):
        """Test that currentItemChanged signal is emitted on selection change."""
        file_list_widget.add_image(str(test_image))

        with qtbot.waitSignal(
            file_list_widget.currentItemChanged, timeout=1000
        ) as blocker:
            file_list_widget.setCurrentRow(0)

        # Signal should be emitted
        assert blocker.signal_triggered

    def test_selection_changed_with_multiple_images(
        self, file_list_widget, tmp_path, qtbot
    ):
        """Test selection changes correctly with multiple images."""
        from PyQt6.QtGui import QColor, QImage

        # Create and add multiple images
        images = []
        for i in range(3):
            img = QImage(100, 100, QImage.Format.Format_RGB32)
            img.fill(QColor(i * 50, i * 50, 255))
            path = tmp_path / f"image_{i}.png"
            img.save(str(path))
            file_list_widget.add_image(str(path))
            images.append(path)

        # Select first image
        file_list_widget.setCurrentRow(0)
        assert file_list_widget.get_current_image_path() == str(images[0])

        # Select second image
        file_list_widget.setCurrentRow(1)
        assert file_list_widget.get_current_image_path() == str(images[1])

        # Select third image
        file_list_widget.setCurrentRow(2)
        assert file_list_widget.get_current_image_path() == str(images[2])

    def test_clear_selection(self, file_list_widget, test_image):
        """Test clearing selection."""
        file_list_widget.add_image(str(test_image))
        file_list_widget.setCurrentRow(0)
        assert file_list_widget.get_current_image_path() is not None

        # Clear selection
        file_list_widget.clearSelection()
        assert file_list_widget.get_current_image_path() is None

    def test_get_current_image_path_after_removal(self, file_list_widget, tmp_path):
        """Test that selection updates correctly after removing image."""
        from PyQt6.QtGui import QColor, QImage

        # Create and add two images
        for i in range(2):
            img = QImage(100, 100, QImage.Format.Format_RGB32)
            img.fill(QColor(i * 50, i * 50, 255))
            path = tmp_path / f"image_{i}.png"
            img.save(str(path))
            file_list_widget.add_image(str(path))

        # Select first image
        file_list_widget.setCurrentRow(0)
        assert file_list_widget.item(0).text() == "image_0.png"

        # Remove first image
        file_list_widget.remove_image(0)

        # Selection should be cleared or moved
        # (behavior depends on Qt implementation)
        assert file_list_widget.count() == 1


class TestFileListWidgetDragDrop:
    """Tests for drag-and-drop functionality."""

    def test_widget_accepts_drops(self, file_list_widget):
        """Test that widget has drag-and-drop enabled."""
        assert file_list_widget.acceptDrops() is True

    def test_drop_single_image_file(self, file_list_widget, test_image, qtbot):
        """Test dropping a single image file."""
        from PyQt6.QtCore import QMimeData, QPoint, Qt, QUrl
        from PyQt6.QtGui import QDragEnterEvent, QDropEvent

        initial_count = file_list_widget.count()

        # Create mime data with file URL
        mime_data = QMimeData()
        mime_data.setUrls([QUrl.fromLocalFile(str(test_image))])

        # Simulate drag enter event
        drag_enter = QDragEnterEvent(
            QPoint(10, 10),
            Qt.DropAction.CopyAction,
            mime_data,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )
        file_list_widget.dragEnterEvent(drag_enter)

        # Event should be accepted
        assert drag_enter.isAccepted()

        # Simulate drop event
        drop_event = QDropEvent(
            QPoint(10, 10),
            Qt.DropAction.CopyAction,
            mime_data,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )
        file_list_widget.dropEvent(drop_event)

        # Image should be added
        assert file_list_widget.count() == initial_count + 1
        assert file_list_widget.item(0).text() == "test_image.png"

    def test_drop_multiple_image_files(self, file_list_widget, tmp_path, qtbot):
        """Test dropping multiple image files at once."""
        from PyQt6.QtCore import QMimeData, QPoint, Qt, QUrl
        from PyQt6.QtGui import QColor, QDropEvent, QImage

        # Create multiple test images
        image_paths = []
        for i in range(3):
            img = QImage(100, 100, QImage.Format.Format_RGB32)
            img.fill(QColor(i * 50, i * 50, 255))
            path = tmp_path / f"drop_image_{i}.png"
            img.save(str(path))
            image_paths.append(path)

        initial_count = file_list_widget.count()

        # Create mime data with multiple file URLs
        mime_data = QMimeData()
        urls = [QUrl.fromLocalFile(str(p)) for p in image_paths]
        mime_data.setUrls(urls)

        # Simulate drop event
        drop_event = QDropEvent(
            QPoint(10, 10),
            Qt.DropAction.CopyAction,
            mime_data,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )
        file_list_widget.dropEvent(drop_event)

        # All images should be added
        assert file_list_widget.count() == initial_count + 3
        for i in range(3):
            assert file_list_widget.item(i).text() == f"drop_image_{i}.png"

    def test_drop_non_image_file_ignored(self, file_list_widget, tmp_path):
        """Test that dropping non-image files is handled gracefully."""
        from PyQt6.QtCore import QMimeData, QPoint, Qt, QUrl
        from PyQt6.QtGui import QDropEvent

        # Create a non-image file
        text_file = tmp_path / "not_an_image.txt"
        text_file.write_text("This is not an image")

        initial_count = file_list_widget.count()

        # Create mime data with text file URL
        mime_data = QMimeData()
        mime_data.setUrls([QUrl.fromLocalFile(str(text_file))])

        # Simulate drop event
        drop_event = QDropEvent(
            QPoint(10, 10),
            Qt.DropAction.CopyAction,
            mime_data,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )
        file_list_widget.dropEvent(drop_event)

        # Invalid file should not be added
        assert file_list_widget.count() == initial_count

    def test_drop_mixed_valid_invalid_files(self, file_list_widget, tmp_path):
        """Test dropping a mix of valid and invalid files."""
        from PyQt6.QtCore import QMimeData, QPoint, Qt, QUrl
        from PyQt6.QtGui import QColor, QDropEvent, QImage

        # Create one valid image
        img = QImage(100, 100, QImage.Format.Format_RGB32)
        img.fill(QColor(100, 150, 200))
        image_path = tmp_path / "valid_image.png"
        img.save(str(image_path))

        # Create one invalid file
        text_file = tmp_path / "invalid.txt"
        text_file.write_text("Not an image")

        initial_count = file_list_widget.count()

        # Create mime data with both files
        mime_data = QMimeData()
        urls = [
            QUrl.fromLocalFile(str(image_path)),
            QUrl.fromLocalFile(str(text_file)),
        ]
        mime_data.setUrls(urls)

        # Simulate drop event
        drop_event = QDropEvent(
            QPoint(10, 10),
            Qt.DropAction.CopyAction,
            mime_data,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )
        file_list_widget.dropEvent(drop_event)

        # Only valid image should be added
        assert file_list_widget.count() == initial_count + 1
        assert file_list_widget.item(0).text() == "valid_image.png"


class TestFileListWidgetThumbnailCache:
    """Tests for thumbnail caching functionality."""

    def test_thumbnail_cached_after_add(self, file_list_widget, test_image):
        """Test that thumbnails are cached after being generated."""
        from PyQt6.QtGui import QPixmapCache

        # Get cache key for the image
        cache_key = f"thumbnail_{test_image}"

        # Initially, cache should not contain the thumbnail
        cached_pixmap = QPixmapCache.find(cache_key)
        assert cached_pixmap is None

        # Add image - should generate and cache thumbnail
        result = file_list_widget.add_image(str(test_image))
        assert result is True

        # Now cache should contain the thumbnail
        cached_pixmap = QPixmapCache.find(cache_key)
        assert cached_pixmap is not None

    def test_cached_thumbnail_reused(self, file_list_widget, test_image, mocker):
        """Test that cached thumbnails are reused instead of regenerating."""
        # Add image first time
        file_list_widget.add_image(str(test_image))

        # Spy on _generate_thumbnail to verify caching works
        spy_generate = mocker.spy(file_list_widget, "_generate_thumbnail")

        # Clear the widget (but cache remains)
        file_list_widget.clear()

        # Add same image again - should use cached thumbnail
        file_list_widget.add_image(str(test_image))

        # _generate_thumbnail should not be called (thumbnail retrieved from cache)
        spy_generate.assert_not_called()

    def test_cache_key_consistency(self, file_list_widget, test_image):
        """Test that cache keys are consistent for the same image."""
        # Generate cache key twice for same image
        key1 = file_list_widget._get_cache_key(str(test_image))
        key2 = file_list_widget._get_cache_key(str(test_image))

        # Keys should be identical
        assert key1 == key2
        assert isinstance(key1, str)
        assert len(key1) > 0

    def test_different_images_different_cache_keys(
        self, file_list_widget, test_image, tmp_path
    ):
        """Test that different images get different cache keys."""
        from PyQt6.QtGui import QColor, QImage

        # Create second test image
        test_image2 = QImage(150, 150, QImage.Format.Format_RGB32)
        test_image2.fill(QColor(0, 255, 0))
        image_path2 = tmp_path / "test_image2.png"
        test_image2.save(str(image_path2))

        # Get cache keys for both images
        key1 = file_list_widget._get_cache_key(str(test_image))
        key2 = file_list_widget._get_cache_key(str(image_path2))

        # Keys should be different
        assert key1 != key2

    def test_cache_limits_memory_usage(self, file_list_widget, tmp_path):
        """Test that cache respects memory limits."""
        from PyQt6.QtGui import QColor, QImage, QPixmapCache

        # Set a small cache limit (in KB)
        original_limit = QPixmapCache.cacheLimit()
        QPixmapCache.setCacheLimit(1024)  # 1 MB

        try:
            # Create and add multiple large images
            for i in range(10):
                large_image = QImage(500, 500, QImage.Format.Format_RGB32)
                large_image.fill(QColor(i * 25, 100, 200))
                image_path = tmp_path / f"large_image_{i}.png"
                large_image.save(str(image_path))
                file_list_widget.add_image(str(image_path))

            # All images should be added successfully
            assert file_list_widget.count() == 10

            # Cache should not exceed limit (though some may be evicted)
            # This is more of a sanity check that caching doesn't break
            assert QPixmapCache.cacheLimit() == 1024

        finally:
            # Restore original cache limit
            QPixmapCache.setCacheLimit(original_limit)
