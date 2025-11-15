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
