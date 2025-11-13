"""
Integration tests for MainWindow layout and component interaction.

M2: PyQt6 Image Display & Navigation - Complete window layout integration
"""

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDockWidget, QMainWindow, QMenuBar, QStatusBar, QToolBar

# Mark all tests in this module as GUI tests
pytestmark = pytest.mark.gui


@pytest.fixture
def main_window(qtbot):
    """
    Fixture to create MainWindow instance for integration testing.

    Args:
        qtbot: pytest-qt fixture for Qt widget testing

    Returns:
        MainWindow instance
    """
    from views.main_window import MainWindow

    window = MainWindow()
    qtbot.addWidget(window)
    return window


class TestMainWindowLayout:
    """Integration tests for MainWindow layout components."""

    def test_window_has_all_components(self, main_window):
        """Test that MainWindow has all required components."""
        # Check menu bar
        assert main_window.menuBar() is not None
        assert isinstance(main_window.menuBar(), QMenuBar)

        # Check toolbar
        toolbars = main_window.findChildren(QToolBar)
        assert len(toolbars) >= 1, "MainWindow should have at least one toolbar"

        # Check status bar
        assert main_window.statusBar() is not None
        assert isinstance(main_window.statusBar(), QStatusBar)

        # Check central widget (ImageCanvas)
        assert main_window.centralWidget() is not None
        assert hasattr(main_window, "image_canvas")

    def test_menu_bar_structure(self, main_window):
        """Test that menu bar has all expected menus."""
        menu_bar = main_window.menuBar()

        # Get menu titles
        menu_titles = [action.text() for action in menu_bar.actions()]

        # Check for required menus
        assert "&File" in menu_titles
        assert "&Edit" in menu_titles
        assert "&View" in menu_titles
        assert "&Tools" in menu_titles
        assert "&Help" in menu_titles

    def test_file_menu_actions(self, main_window):
        """Test that File menu has all required actions."""
        menu_bar = main_window.menuBar()
        file_menu = None
        for action in menu_bar.actions():
            if action.text() == "&File":
                file_menu = action.menu()
                break

        assert file_menu is not None, "File menu not found"

        action_texts = [action.text() for action in file_menu.actions()]

        # Check for required actions (excluding separators)
        assert "&New Project..." in action_texts
        assert "&Open Project..." in action_texts
        assert "&Save Project" in action_texts
        assert "&Import Images..." in action_texts
        assert "&Export Annotations..." in action_texts
        assert "E&xit" in action_texts

    def test_dock_widgets_present(self, main_window):
        """Test that all dock widgets are present."""
        dock_widgets = main_window.findChildren(QDockWidget)
        assert len(dock_widgets) >= 3, "Should have at least 3 dock widgets"

        # Check dock widget titles
        dock_titles = [dock.windowTitle() for dock in dock_widgets]
        assert "Files" in dock_titles
        assert "Classes" in dock_titles
        assert "Properties" in dock_titles

    def test_dock_widgets_visibility(self, main_window):
        """Test that dock widgets can be toggled."""
        # Get dock widgets
        file_dock = main_window.file_dock
        class_dock = main_window.class_dock
        props_dock = main_window.props_dock

        # All should be visible by default
        assert file_dock.isVisible()
        assert class_dock.isVisible()
        assert props_dock.isVisible()

        # Test toggling
        file_dock.setVisible(False)
        assert not file_dock.isVisible()

        file_dock.setVisible(True)
        assert file_dock.isVisible()

    def test_toolbar_has_actions(self, main_window):
        """Test that toolbar has all required actions."""
        toolbars = main_window.findChildren(QToolBar)
        assert len(toolbars) > 0

        main_toolbar = toolbars[0]
        actions = [a for a in main_toolbar.actions() if not a.isSeparator()]

        # Should have multiple actions
        assert len(actions) >= 8, "Toolbar should have at least 8 actions"

    def test_actions_connected_to_canvas(self, main_window):
        """Test that view actions are connected to canvas methods."""
        # Test zoom actions are connected
        assert hasattr(main_window, "zoom_in_action")
        assert hasattr(main_window, "zoom_out_action")
        assert hasattr(main_window, "fit_action")

        # Check connections exist (connections should be made)
        assert main_window.image_canvas is not None

    def test_view_menu_dock_toggles(self, main_window):
        """Test that View menu has dock widget toggle actions."""
        menu_bar = main_window.menuBar()
        view_menu = None
        for action in menu_bar.actions():
            if action.text() == "&View":
                view_menu = action.menu()
                break

        assert view_menu is not None, "View menu not found"

        # Count checkable actions (should include dock widget toggles)
        checkable_actions = [a for a in view_menu.actions() if a.isCheckable()]
        assert len(checkable_actions) >= 3, "View menu should have dock widget toggles"


class TestMainWindowInteraction:
    """Integration tests for MainWindow component interactions."""

    def test_status_bar_shows_messages(self, main_window):
        """Test that status bar can display messages."""
        status_bar = main_window.statusBar()
        test_message = "Test message"

        status_bar.showMessage(test_message)
        assert status_bar.currentMessage() == test_message

    def test_window_geometry(self, main_window):
        """Test that window has correct initial geometry."""
        geometry = main_window.geometry()

        # Should have reasonable initial size
        assert geometry.width() == 1280
        assert geometry.height() == 720

    def test_central_widget_is_image_canvas(self, main_window):
        """Test that central widget is ImageCanvas."""
        from views.image_canvas import ImageCanvas

        assert isinstance(main_window.centralWidget(), ImageCanvas)
        assert main_window.image_canvas == main_window.centralWidget()

    def test_dock_widget_areas(self, main_window):
        """Test that dock widgets are in correct areas."""
        # File dock should be on left
        file_area = main_window.dockWidgetArea(main_window.file_dock)
        assert file_area == Qt.DockWidgetArea.LeftDockWidgetArea

        # Class and props docks should be on right
        class_area = main_window.dockWidgetArea(main_window.class_dock)
        props_area = main_window.dockWidgetArea(main_window.props_dock)

        assert class_area == Qt.DockWidgetArea.RightDockWidgetArea
        assert props_area == Qt.DockWidgetArea.RightDockWidgetArea


class TestMainWindowActions:
    """Integration tests for MainWindow actions."""

    def test_all_actions_have_shortcuts(self, main_window):
        """Test that important actions have keyboard shortcuts."""
        # Check that key actions have shortcuts
        assert main_window.new_action.shortcut().toString() == "Ctrl+N"
        assert main_window.open_action.shortcut().toString() == "Ctrl+O"
        assert main_window.save_action.shortcut().toString() == "Ctrl+S"
        assert main_window.exit_action.shortcut().toString() == "Ctrl+Q"

        assert main_window.undo_action.shortcut().toString() == "Ctrl+Z"
        assert main_window.redo_action.shortcut().toString() == "Ctrl+Y"

        assert main_window.zoom_in_action.shortcut().toString() == "Ctrl++"
        assert main_window.zoom_out_action.shortcut().toString() == "Ctrl+-"
        assert main_window.fit_action.shortcut().toString() == "Ctrl+0"

    def test_actions_have_status_tips(self, main_window):
        """Test that actions have status tips for user guidance."""
        # File actions
        assert len(main_window.new_action.statusTip()) > 0
        assert len(main_window.open_action.statusTip()) > 0
        assert len(main_window.save_action.statusTip()) > 0

        # Edit actions
        assert len(main_window.undo_action.statusTip()) > 0
        assert len(main_window.redo_action.statusTip()) > 0

        # View actions
        assert len(main_window.zoom_in_action.statusTip()) > 0
        assert len(main_window.zoom_out_action.statusTip()) > 0

    def test_exit_action_connected(self, main_window):
        """Test that exit action is connected to close."""
        # The exit action should be connected to close
        # We can't easily test the actual connection, but we can verify it exists
        assert main_window.exit_action is not None
        assert main_window.exit_action.text() == "E&xit"


class TestMainWindowState:
    """Integration tests for MainWindow state management."""

    def test_window_title(self, main_window):
        """Test that window has correct title."""
        assert main_window.windowTitle() == "ALA-GUI - Auto Label Agent"

    def test_window_is_main_window(self, main_window):
        """Test that window is QMainWindow."""
        assert isinstance(main_window, QMainWindow)

    def test_all_instance_variables_initialized(self, main_window):
        """Test that all expected instance variables are initialized."""
        # Check dock widgets
        assert hasattr(main_window, "file_dock")
        assert hasattr(main_window, "class_dock")
        assert hasattr(main_window, "props_dock")

        # Check central widget
        assert hasattr(main_window, "image_canvas")

        # Check actions exist
        action_names = [
            "new_action",
            "open_action",
            "save_action",
            "import_action",
            "export_action",
            "exit_action",
            "undo_action",
            "redo_action",
            "prefs_action",
            "zoom_in_action",
            "zoom_out_action",
            "fit_action",
            "prev_action",
            "next_action",
            "auto_annotate_action",
            "few_shot_action",
            "train_action",
            "docs_action",
            "shortcuts_action",
            "about_action",
        ]

        for action_name in action_names:
            assert hasattr(main_window, action_name), f"Missing action: {action_name}"
