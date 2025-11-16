"""
Integration tests for keyboard shortcuts.

Tests ShortcutManager integration with MainWindow and widget interactions.
"""

import pytest

# Mark all tests in this module as integration and GUI tests
pytestmark = [pytest.mark.integration, pytest.mark.gui]


@pytest.fixture
def main_window(qtbot):
    """
    Fixture to create MainWindow for testing.

    Args:
        qtbot: pytest-qt fixture

    Returns:
        MainWindow instance with shortcuts configured
    """
    from views.main_window import MainWindow

    window = MainWindow()
    qtbot.addWidget(window)
    return window


class TestShortcutIntegration:
    """Tests for shortcut integration with MainWindow."""

    def test_shortcut_manager_created(self, main_window):
        """Test that ShortcutManager is created and initialized."""
        assert hasattr(main_window, "shortcut_manager")
        assert main_window.shortcut_manager is not None

    def test_default_shortcuts_registered(self, main_window):
        """Test that default shortcuts are registered."""
        shortcuts = main_window.shortcut_manager.get_all_shortcuts()

        # Check that we have multiple shortcuts registered
        assert len(shortcuts) > 0

        # Check for key shortcut categories
        navigation_shortcuts = [
            k for k in shortcuts.keys() if "image" in k or "prev" in k
        ]
        assert len(navigation_shortcuts) > 0

        zoom_shortcuts = [k for k in shortcuts.keys() if "zoom" in k]
        assert len(zoom_shortcuts) > 0

    def test_navigation_shortcuts_exist(self, main_window):
        """Test that navigation shortcuts are registered."""
        shortcuts = main_window.shortcut_manager.get_all_shortcuts()

        assert "next_image" in shortcuts
        assert "prev_image" in shortcuts
        assert "first_image" in shortcuts
        assert "last_image" in shortcuts

    def test_zoom_shortcuts_exist(self, main_window):
        """Test that zoom shortcuts are registered."""
        shortcuts = main_window.shortcut_manager.get_all_shortcuts()

        assert "zoom_in" in shortcuts
        assert "zoom_out" in shortcuts
        assert "zoom_reset" in shortcuts
        assert "zoom_fit" in shortcuts

    def test_file_operation_shortcuts_exist(self, main_window):
        """Test that file operation shortcuts are registered."""
        shortcuts = main_window.shortcut_manager.get_all_shortcuts()

        assert "open_file" in shortcuts
        assert "save" in shortcuts
        assert "save_as" in shortcuts
        assert "quit" in shortcuts

    def test_tool_shortcuts_exist(self, main_window):
        """Test that tool shortcuts are registered."""
        shortcuts = main_window.shortcut_manager.get_all_shortcuts()

        assert "tool_rectangle" in shortcuts
        assert "tool_polygon" in shortcuts
        assert "delete_annotation" in shortcuts

    def test_undo_redo_shortcuts_exist(self, main_window):
        """Test that undo/redo shortcuts are registered."""
        shortcuts = main_window.shortcut_manager.get_all_shortcuts()

        assert "undo" in shortcuts
        assert "redo" in shortcuts


class TestShortcutHandlers:
    """Tests for shortcut handler methods in MainWindow."""

    def test_navigation_handlers_exist(self, main_window):
        """Test that navigation handler methods exist."""
        assert hasattr(main_window, "next_image")
        assert callable(main_window.next_image)
        assert hasattr(main_window, "previous_image")
        assert callable(main_window.previous_image)
        assert hasattr(main_window, "first_image")
        assert callable(main_window.first_image)
        assert hasattr(main_window, "last_image")
        assert callable(main_window.last_image)

    def test_zoom_handlers_exist(self, main_window):
        """Test that zoom handler methods exist."""
        assert hasattr(main_window, "zoom_in")
        assert callable(main_window.zoom_in)
        assert hasattr(main_window, "zoom_out")
        assert callable(main_window.zoom_out)
        assert hasattr(main_window, "zoom_reset")
        assert callable(main_window.zoom_reset)
        assert hasattr(main_window, "zoom_fit")
        assert callable(main_window.zoom_fit)

    def test_file_operation_handlers_exist(self, main_window):
        """Test that file operation handler methods exist."""
        assert hasattr(main_window, "open_file")
        assert callable(main_window.open_file)
        assert hasattr(main_window, "save")
        assert callable(main_window.save)
        assert hasattr(main_window, "save_as")
        assert callable(main_window.save_as)
        assert hasattr(main_window, "quit")
        assert callable(main_window.quit)

    def test_tool_handlers_exist(self, main_window):
        """Test that tool handler methods exist."""
        assert hasattr(main_window, "select_rectangle_tool")
        assert callable(main_window.select_rectangle_tool)
        assert hasattr(main_window, "select_polygon_tool")
        assert callable(main_window.select_polygon_tool)
        assert hasattr(main_window, "delete_annotation")
        assert callable(main_window.delete_annotation)

    def test_undo_redo_handlers_exist(self, main_window):
        """Test that undo/redo handler methods exist."""
        assert hasattr(main_window, "undo")
        assert callable(main_window.undo)
        assert hasattr(main_window, "redo")
        assert callable(main_window.redo)

    def test_handlers_can_be_called(self, main_window):
        """Test that handler methods can be called without errors."""
        # Test navigation handlers
        main_window.next_image()
        main_window.previous_image()
        main_window.first_image()
        main_window.last_image()

        # Test zoom handlers
        main_window.zoom_in()
        main_window.zoom_out()
        main_window.zoom_reset()
        main_window.zoom_fit()

        # Test file operation handlers
        main_window.open_file()
        main_window.save()
        main_window.save_as()

        # Test tool handlers
        main_window.select_rectangle_tool()
        main_window.select_polygon_tool()
        main_window.delete_annotation()

        # Test undo/redo handlers
        main_window.undo()
        main_window.redo()

        # Note: quit handler will close the window, so we don't test it
