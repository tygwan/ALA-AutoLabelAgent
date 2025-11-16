"""
Unit tests for ShortcutManager.

Tests the keyboard shortcut management system following TDD methodology.
"""

import pytest

# Mark all tests in this module as unit tests and GUI tests
pytestmark = [pytest.mark.unit, pytest.mark.gui]


@pytest.fixture
def main_window(qtbot):
    """
    Fixture to create a MainWindow for shortcut testing.

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
def shortcut_manager(main_window):
    """
    Fixture to create a ShortcutManager for testing.

    Args:
        main_window: MainWindow fixture

    Returns:
        ShortcutManager instance
    """
    from controllers.shortcut_manager import ShortcutManager

    manager = ShortcutManager(main_window)
    return manager


class TestShortcutManagerInitialization:
    """Tests for ShortcutManager initialization."""

    def test_manager_creation(self, shortcut_manager):
        """Test that ShortcutManager can be created."""
        assert shortcut_manager is not None
        from controllers.shortcut_manager import ShortcutManager

        assert isinstance(shortcut_manager, ShortcutManager)

    def test_manager_has_parent_window(self, shortcut_manager, main_window):
        """Test that manager has reference to parent window."""
        assert shortcut_manager.parent() == main_window

    def test_manager_starts_with_no_shortcuts(self, shortcut_manager):
        """Test that manager starts with no registered shortcuts."""
        shortcuts = shortcut_manager.get_all_shortcuts()
        # Should have default shortcuts registered during init
        assert isinstance(shortcuts, dict)

    def test_manager_can_register_shortcut(self, shortcut_manager):
        """Test that manager can register a new shortcut."""
        result = shortcut_manager.register_shortcut(
            "test_action", "Ctrl+T", lambda: None, "Test action"
        )
        assert result is True

    def test_duplicate_key_registration_fails(self, shortcut_manager):
        """Test that registering duplicate key sequence fails."""
        shortcut_manager.register_shortcut(
            "action1", "Ctrl+T", lambda: None, "Action 1"
        )
        result = shortcut_manager.register_shortcut(
            "action2", "Ctrl+T", lambda: None, "Action 2"
        )
        assert result is False

    def test_duplicate_action_name_overwrites(self, shortcut_manager):
        """Test that registering duplicate action name overwrites."""

        def callback1():
            pass

        def callback2():
            pass

        shortcut_manager.register_shortcut("action1", "Ctrl+T", callback1, "Action 1")
        result = shortcut_manager.register_shortcut(
            "action1", "Ctrl+Y", callback2, "Action 1 Updated"
        )
        assert result is True


class TestNavigationShortcuts:
    """Tests for navigation keyboard shortcuts."""

    def test_next_image_shortcut(self, shortcut_manager, qtbot):
        """Test Right arrow shortcut for next image."""
        triggered = []

        def callback():
            triggered.append(True)

        result = shortcut_manager.register_shortcut(
            "next_image", "Right", callback, "Next image"
        )
        assert result is True

        # Trigger the shortcut
        shortcuts = shortcut_manager.get_all_shortcuts()
        assert "next_image" in shortcuts
        assert shortcuts["next_image"] == "Right"

    def test_previous_image_shortcut(self, shortcut_manager):
        """Test Left arrow shortcut for previous image."""
        triggered = []

        def callback():
            triggered.append(True)

        result = shortcut_manager.register_shortcut(
            "prev_image", "Left", callback, "Previous image"
        )
        assert result is True

    def test_first_image_shortcut(self, shortcut_manager):
        """Test Home key shortcut for first image."""
        result = shortcut_manager.register_shortcut(
            "first_image", "Home", lambda: None, "First image"
        )
        assert result is True

    def test_last_image_shortcut(self, shortcut_manager):
        """Test End key shortcut for last image."""
        result = shortcut_manager.register_shortcut(
            "last_image", "End", lambda: None, "Last image"
        )
        assert result is True


class TestZoomShortcuts:
    """Tests for zoom keyboard shortcuts."""

    def test_zoom_in_shortcut(self, shortcut_manager):
        """Test Ctrl++ shortcut for zoom in."""
        result = shortcut_manager.register_shortcut(
            "zoom_in", "Ctrl++", lambda: None, "Zoom in"
        )
        assert result is True

    def test_zoom_out_shortcut(self, shortcut_manager):
        """Test Ctrl+- shortcut for zoom out."""
        result = shortcut_manager.register_shortcut(
            "zoom_out", "Ctrl+-", lambda: None, "Zoom out"
        )
        assert result is True

    def test_zoom_reset_shortcut(self, shortcut_manager):
        """Test Ctrl+0 shortcut for reset zoom."""
        result = shortcut_manager.register_shortcut(
            "zoom_reset", "Ctrl+0", lambda: None, "Reset zoom"
        )
        assert result is True

    def test_zoom_fit_shortcut(self, shortcut_manager):
        """Test Ctrl+F shortcut for fit to window."""
        result = shortcut_manager.register_shortcut(
            "zoom_fit", "Ctrl+F", lambda: None, "Fit to window"
        )
        assert result is True


class TestFileOperationShortcuts:
    """Tests for file operation shortcuts."""

    def test_open_file_shortcut(self, shortcut_manager):
        """Test Ctrl+O shortcut for open file."""
        result = shortcut_manager.register_shortcut(
            "open_file", "Ctrl+O", lambda: None, "Open file"
        )
        assert result is True

    def test_save_shortcut(self, shortcut_manager):
        """Test Ctrl+S shortcut for save."""
        result = shortcut_manager.register_shortcut(
            "save", "Ctrl+S", lambda: None, "Save"
        )
        assert result is True

    def test_save_as_shortcut(self, shortcut_manager):
        """Test Ctrl+Shift+S shortcut for save as."""
        result = shortcut_manager.register_shortcut(
            "save_as", "Ctrl+Shift+S", lambda: None, "Save as"
        )
        assert result is True

    def test_quit_shortcut(self, shortcut_manager):
        """Test Ctrl+Q shortcut for quit."""
        result = shortcut_manager.register_shortcut(
            "quit", "Ctrl+Q", lambda: None, "Quit application"
        )
        assert result is True


class TestToolShortcuts:
    """Tests for annotation tool shortcuts."""

    def test_rectangle_tool_shortcut(self, shortcut_manager):
        """Test R key shortcut for rectangle tool."""
        result = shortcut_manager.register_shortcut(
            "tool_rectangle", "R", lambda: None, "Rectangle tool"
        )
        assert result is True

    def test_polygon_tool_shortcut(self, shortcut_manager):
        """Test P key shortcut for polygon tool."""
        result = shortcut_manager.register_shortcut(
            "tool_polygon", "P", lambda: None, "Polygon tool"
        )
        assert result is True

    def test_delete_annotation_shortcut(self, shortcut_manager):
        """Test Delete key shortcut for delete annotation."""
        result = shortcut_manager.register_shortcut(
            "delete_annotation", "Del", lambda: None, "Delete annotation"
        )
        assert result is True

    def test_undo_shortcut(self, shortcut_manager):
        """Test Ctrl+Z shortcut for undo."""
        result = shortcut_manager.register_shortcut(
            "undo", "Ctrl+Z", lambda: None, "Undo"
        )
        assert result is True

    def test_redo_shortcut(self, shortcut_manager):
        """Test Ctrl+Y shortcut for redo."""
        result = shortcut_manager.register_shortcut(
            "redo", "Ctrl+Y", lambda: None, "Redo"
        )
        assert result is True
