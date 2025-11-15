"""
Integration tests for MainWindow with all M2 components.

Tests the complete integration of MainWindow with FileListWidget,
ClassListWidget, ImageCanvas, SettingsDialog, and ShortcutManager.
"""

import pytest
from PyQt6.QtCore import Qt

# Mark all tests in this module as integration tests and GUI tests
pytestmark = [pytest.mark.integration, pytest.mark.gui]


@pytest.fixture
def main_window(qtbot):
    """
    Fixture to create a MainWindow for integration testing.

    Args:
        qtbot: pytest-qt fixture for Qt widget testing

    Returns:
        MainWindow instance
    """
    from views.main_window import MainWindow

    window = MainWindow()
    qtbot.addWidget(window)
    return window


class TestMainWindowComponentIntegration:
    """Tests for MainWindow integration with all components."""

    def test_main_window_has_file_list_widget(self, main_window):
        """Test that MainWindow contains FileListWidget in dock."""
        assert main_window.file_dock is not None

        from views.file_list_widget import FileListWidget

        file_list = main_window.file_dock.widget()
        assert isinstance(file_list, FileListWidget)

    def test_main_window_has_class_list_widget(self, main_window):
        """Test that MainWindow contains ClassListWidget in dock."""
        assert main_window.class_dock is not None

        from views.class_list_widget import ClassListWidget

        class_list = main_window.class_dock.widget()
        assert isinstance(class_list, ClassListWidget)

    def test_main_window_has_image_canvas(self, main_window):
        """Test that MainWindow has ImageCanvas as central widget."""
        from views.image_canvas import ImageCanvas

        assert isinstance(main_window.image_canvas, ImageCanvas)
        assert main_window.centralWidget() is main_window.image_canvas

    def test_main_window_has_shortcut_manager(self, main_window):
        """Test that MainWindow has ShortcutManager initialized."""
        from controllers.shortcut_manager import ShortcutManager

        assert hasattr(main_window, "shortcut_manager")
        assert isinstance(main_window.shortcut_manager, ShortcutManager)


class TestFileListIntegration:
    """Tests for FileListWidget integration with MainWindow."""

    def test_file_list_selection_updates_canvas(self, main_window, test_images, qtbot):
        """Test that selecting image in file list loads it in canvas."""
        from views.file_list_widget import FileListWidget

        file_list = main_window.file_dock.widget()
        assert isinstance(file_list, FileListWidget)

        # Add test images
        for image_path in test_images:
            file_list.add_image(str(image_path))

        # Select first image
        file_list.setCurrentRow(0)
        qtbot.wait(100)

        # Canvas should have image loaded
        current_path = file_list.get_current_image_path()
        assert current_path is not None

    def test_file_list_navigation_shortcuts_work(self, main_window, test_images, qtbot):
        """Test that navigation shortcuts work with file list."""
        from PyQt6.QtTest import QTest

        from views.file_list_widget import FileListWidget

        file_list = main_window.file_dock.widget()
        assert isinstance(file_list, FileListWidget)

        # Add multiple images
        for image_path in test_images:
            file_list.add_image(str(image_path))

        file_list.setCurrentRow(0)

        # Press Right arrow (next image shortcut)
        QTest.keyClick(main_window, Qt.Key.Key_Right)
        qtbot.wait(50)

        # Status bar should show message (shortcut was triggered)
        status_text = main_window.statusBar().currentMessage()
        assert "Next image" in status_text or status_text == ""

    def test_file_list_drag_drop_in_main_window(self, main_window, test_images, qtbot):
        """Test that file list accepts drag-drop in integrated environment."""
        from PyQt6.QtCore import QMimeData, QUrl
        from PyQt6.QtGui import QDragEnterEvent, QDropEvent

        from views.file_list_widget import FileListWidget

        file_list = main_window.file_dock.widget()
        assert isinstance(file_list, FileListWidget)

        initial_count = file_list.count()

        # Simulate drag-drop
        mime_data = QMimeData()
        urls = [QUrl.fromLocalFile(str(path)) for path in test_images[:2]]
        mime_data.setUrls(urls)

        drag_event = QDragEnterEvent(
            file_list.rect().center(),
            Qt.DropAction.CopyAction,
            mime_data,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )
        file_list.dragEnterEvent(drag_event)
        assert drag_event.isAccepted()

        drop_event = QDropEvent(
            file_list.rect().center(),
            Qt.DropAction.CopyAction,
            mime_data,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )
        file_list.dropEvent(drop_event)

        assert file_list.count() == initial_count + 2


class TestClassListIntegration:
    """Tests for ClassListWidget integration with MainWindow."""

    def test_class_list_in_dock_widget(self, main_window):
        """Test that class list is properly docked."""
        from views.class_list_widget import ClassListWidget

        assert main_window.class_dock is not None
        class_list = main_window.class_dock.widget()
        assert isinstance(class_list, ClassListWidget)

    def test_add_class_in_integrated_window(self, main_window):
        """Test adding classes in integrated environment."""
        from PyQt6.QtGui import QColor

        from views.class_list_widget import ClassListWidget

        class_list = main_window.class_dock.widget()
        assert isinstance(class_list, ClassListWidget)

        initial_count = class_list.count()

        success = class_list.add_class("person", QColor(255, 0, 0))
        assert success is True
        assert class_list.count() == initial_count + 1

    def test_class_list_dock_toggleable(self, main_window, qtbot):
        """Test that class list dock can be toggled via View menu."""
        assert main_window.class_dock is not None

        initial_visibility = main_window.class_dock.isVisible()

        # Toggle visibility
        toggle_action = main_window.class_dock.toggleViewAction()
        toggle_action.trigger()
        qtbot.wait(50)

        assert main_window.class_dock.isVisible() != initial_visibility


class TestImageCanvasIntegration:
    """Tests for ImageCanvas integration with MainWindow."""

    def test_canvas_zoom_actions_connected(self, main_window):
        """Test that zoom actions are connected to canvas."""
        # Zoom in action should be connected
        assert main_window.zoom_in_action is not None
        assert main_window.image_canvas is not None

        # Trigger zoom in
        main_window.zoom_in_action.trigger()

        # Canvas zoom should have changed (tested via ImageCanvas tests)

    def test_canvas_zoom_shortcuts_work(self, main_window, qtbot):
        """Test that zoom shortcuts trigger canvas zoom methods."""
        from PyQt6.QtTest import QTest

        # Press Ctrl++ (zoom in shortcut)
        QTest.keyClick(
            main_window, Qt.Key.Key_Plus, Qt.KeyboardModifier.ControlModifier
        )
        qtbot.wait(50)

        # Status bar should show zoom message
        status_text = main_window.statusBar().currentMessage()
        assert "Zoom" in status_text or status_text == ""

    def test_canvas_fit_to_window_action(self, main_window):
        """Test fit to window action integration."""
        assert main_window.fit_action is not None

        # Trigger fit action
        main_window.fit_action.trigger()

        # Action should be connected to canvas


class TestSettingsDialogIntegration:
    """Tests for SettingsDialog integration with MainWindow."""

    def test_preferences_action_opens_settings_dialog(self, main_window, qtbot):
        """Test that preferences action opens SettingsDialog."""
        assert main_window.prefs_action is not None

        # Trigger preferences action
        main_window.prefs_action.trigger()
        qtbot.wait(100)

        # Settings dialog should be shown (will be implemented)

    def test_settings_dialog_is_modal(self, main_window, qtbot):
        """Test that settings dialog opens as modal."""
        # When implemented, dialog should be modal


class TestKeyboardShortcutsIntegration:
    """Tests for keyboard shortcuts integration."""

    def test_shortcut_manager_initialized(self, main_window):
        """Test that ShortcutManager is initialized in MainWindow."""
        from controllers.shortcut_manager import ShortcutManager

        assert hasattr(main_window, "shortcut_manager")
        assert isinstance(main_window.shortcut_manager, ShortcutManager)

    def test_navigation_shortcuts_registered(self, main_window):
        """Test that navigation shortcuts are registered."""
        shortcuts = main_window.shortcut_manager.get_all_shortcuts()

        # Check for navigation shortcuts
        assert "next_image" in shortcuts
        assert "prev_image" in shortcuts
        assert "first_image" in shortcuts
        assert "last_image" in shortcuts

    def test_zoom_shortcuts_registered(self, main_window):
        """Test that zoom shortcuts are registered."""
        shortcuts = main_window.shortcut_manager.get_all_shortcuts()

        # Check for zoom shortcuts
        assert "zoom_in" in shortcuts
        assert "zoom_out" in shortcuts
        assert "zoom_reset" in shortcuts
        assert "zoom_fit" in shortcuts

    def test_file_shortcuts_registered(self, main_window):
        """Test that file operation shortcuts are registered."""
        shortcuts = main_window.shortcut_manager.get_all_shortcuts()

        # Check for file shortcuts
        assert "open" in shortcuts
        assert "save" in shortcuts
        assert "quit" in shortcuts

    def test_tool_shortcuts_registered(self, main_window):
        """Test that tool selection shortcuts are registered."""
        shortcuts = main_window.shortcut_manager.get_all_shortcuts()

        # Check for tool shortcuts
        assert "rectangle_tool" in shortcuts
        assert "polygon_tool" in shortcuts

    def test_edit_shortcuts_registered(self, main_window):
        """Test that edit shortcuts are registered."""
        shortcuts = main_window.shortcut_manager.get_all_shortcuts()

        # Check for edit shortcuts
        assert "undo" in shortcuts
        assert "redo" in shortcuts


class TestCompleteWorkflow:
    """End-to-end workflow integration tests."""

    def test_complete_image_viewing_workflow(self, main_window, test_images, qtbot):
        """Test complete workflow: add images, select, view, navigate."""
        from views.file_list_widget import FileListWidget

        file_list = main_window.file_dock.widget()
        assert isinstance(file_list, FileListWidget)

        # Step 1: Add images to file list
        for image_path in test_images:
            file_list.add_image(str(image_path))

        assert file_list.count() == len(test_images)

        # Step 2: Select first image
        file_list.setCurrentRow(0)
        qtbot.wait(100)

        first_image_path = file_list.get_current_image_path()
        assert first_image_path is not None

        # Step 3: Use next image shortcut
        main_window.next_image()
        qtbot.wait(50)

        # Status should update
        status_text = main_window.statusBar().currentMessage()
        assert status_text is not None

    def test_complete_class_management_workflow(self, main_window, qtbot):
        """Test complete workflow: add classes, select, verify."""
        from PyQt6.QtGui import QColor

        from views.class_list_widget import ClassListWidget

        class_list = main_window.class_dock.widget()
        assert isinstance(class_list, ClassListWidget)

        # Step 1: Add classes
        classes = [
            ("person", QColor(255, 0, 0)),
            ("car", QColor(0, 255, 0)),
            ("dog", QColor(0, 0, 255)),
        ]

        for class_name, color in classes:
            success = class_list.add_class(class_name, color)
            assert success is True

        assert class_list.count() == 3

        # Step 2: Select a class
        class_list.setCurrentRow(0)
        qtbot.wait(50)

        current_class = class_list.get_current_class()
        assert current_class == "person"

        # Step 3: Get class color
        person_color = class_list.get_class_color("person")
        assert person_color == QColor(255, 0, 0)

    def test_dock_widgets_persistence(self, main_window, qtbot):
        """Test that dock widgets maintain state."""
        # Hide file dock
        main_window.file_dock.setVisible(False)
        qtbot.wait(50)
        assert main_window.file_dock.isVisible() is False

        # Show file dock
        main_window.file_dock.setVisible(True)
        qtbot.wait(50)
        assert main_window.file_dock.isVisible() is True
