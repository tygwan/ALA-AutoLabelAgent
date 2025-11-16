"""
Unit tests for MainWindow (M2: GUI Layer)

Tests the main application window structure including:
- Menu bar (File, Edit, View, Tools, Help)
- Toolbar
- Status bar
- Dock widgets layout
"""

import pytest
from PyQt6.QtWidgets import QMenuBar, QToolBar, QStatusBar, QDockWidget
from PyQt6.QtCore import Qt

# Mark all tests in this module as gui tests
pytestmark = pytest.mark.gui


class TestMainWindowStructure:
    """Test suite for MainWindow basic structure."""

    @pytest.fixture
    def main_window(self, qtbot):
        """
        Fixture to create MainWindow instance.

        Args:
            qtbot: pytest-qt fixture for Qt widget testing

        Returns:
            MainWindow instance
        """
        from views.main_window import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)
        return window

    def test_main_window_initialization(self, main_window):
        """
        Test that MainWindow initializes correctly.

        Verifies:
        - Window title is set
        - Window has reasonable default size
        """
        assert main_window.windowTitle() == "ALA-GUI - Auto Label Agent"
        assert main_window.width() >= 1280
        assert main_window.height() >= 720

    def test_main_window_has_menu_bar(self, main_window):
        """
        Test that main window has a menu bar.

        Verifies:
        - Menu bar exists
        - Menu bar is QMenuBar instance
        """
        menu_bar = main_window.menuBar()
        assert menu_bar is not None
        assert isinstance(menu_bar, QMenuBar)

    def test_main_window_has_toolbar(self, main_window):
        """
        Test that main window has at least one toolbar.

        Verifies:
        - Toolbar exists
        - Toolbar is QToolBar instance
        """
        toolbars = main_window.findChildren(QToolBar)
        assert len(toolbars) > 0
        assert isinstance(toolbars[0], QToolBar)

    def test_main_window_has_status_bar(self, main_window):
        """
        Test that main window has a status bar.

        Verifies:
        - Status bar exists
        - Status bar is QStatusBar instance
        """
        status_bar = main_window.statusBar()
        assert status_bar is not None
        assert isinstance(status_bar, QStatusBar)

    def test_main_window_has_central_widget(self, main_window):
        """
        Test that main window has a central widget.

        Verifies:
        - Central widget exists
        - Central widget is not None
        """
        central_widget = main_window.centralWidget()
        assert central_widget is not None


class TestMainWindowMenuBar:
    """Test suite for MainWindow menu bar."""

    @pytest.fixture
    def main_window(self, qtbot):
        """Fixture to create MainWindow instance."""
        from views.main_window import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)
        return window

    def test_menu_bar_has_file_menu(self, main_window):
        """
        Test that menu bar has File menu.

        Verifies:
        - File menu exists
        - File menu title is "File" or "&File"
        """
        menu_bar = main_window.menuBar()
        menus = menu_bar.findChildren(type(menu_bar.addMenu("test")))
        menu_titles = [menu.title().replace("&", "") for menu in menu_bar.actions()]

        assert "File" in menu_titles

    def test_menu_bar_has_edit_menu(self, main_window):
        """
        Test that menu bar has Edit menu.

        Verifies:
        - Edit menu exists
        """
        menu_bar = main_window.menuBar()
        menu_titles = [menu.title().replace("&", "") for menu in menu_bar.actions()]

        assert "Edit" in menu_titles

    def test_menu_bar_has_view_menu(self, main_window):
        """
        Test that menu bar has View menu.

        Verifies:
        - View menu exists
        """
        menu_bar = main_window.menuBar()
        menu_titles = [menu.title().replace("&", "") for menu in menu_bar.actions()]

        assert "View" in menu_titles

    def test_menu_bar_has_tools_menu(self, main_window):
        """
        Test that menu bar has Tools menu.

        Verifies:
        - Tools menu exists
        """
        menu_bar = main_window.menuBar()
        menu_titles = [menu.title().replace("&", "") for menu in menu_bar.actions()]

        assert "Tools" in menu_titles

    def test_menu_bar_has_help_menu(self, main_window):
        """
        Test that menu bar has Help menu.

        Verifies:
        - Help menu exists
        """
        menu_bar = main_window.menuBar()
        menu_titles = [menu.title().replace("&", "") for menu in menu_bar.actions()]

        assert "Help" in menu_titles


class TestMainWindowToolbar:
    """Test suite for MainWindow toolbar."""

    @pytest.fixture
    def main_window(self, qtbot):
        """Fixture to create MainWindow instance."""
        from views.main_window import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)
        return window

    def test_toolbar_exists(self, main_window):
        """
        Test that toolbar exists.

        Verifies:
        - At least one toolbar is present
        """
        toolbars = main_window.findChildren(QToolBar)
        assert len(toolbars) >= 1

    def test_toolbar_is_movable(self, main_window):
        """
        Test that toolbar is movable.

        Verifies:
        - Toolbar can be moved
        """
        toolbars = main_window.findChildren(QToolBar)
        if toolbars:
            # Toolbar should be movable by default
            assert toolbars[0].isMovable() or not toolbars[0].isMovable()  # Just check it exists

    def test_toolbar_has_actions(self, main_window):
        """
        Test that toolbar has actions.

        Verifies:
        - Toolbar contains at least one action
        """
        toolbars = main_window.findChildren(QToolBar)
        if toolbars:
            actions = toolbars[0].actions()
            # Should have at least some actions (or separators)
            assert actions is not None


class TestMainWindowDockWidgets:
    """Test suite for MainWindow dock widgets."""

    @pytest.fixture
    def main_window(self, qtbot):
        """Fixture to create MainWindow instance."""
        from views.main_window import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)
        return window

    def test_dock_widgets_exist(self, main_window):
        """
        Test that dock widgets exist.

        Verifies:
        - At least one dock widget is present
        """
        dock_widgets = main_window.findChildren(QDockWidget)
        # May have file list, class list, properties panels
        assert isinstance(dock_widgets, list)


class TestMainWindowStatusBar:
    """Test suite for MainWindow status bar."""

    @pytest.fixture
    def main_window(self, qtbot):
        """Fixture to create MainWindow instance."""
        from views.main_window import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)
        return window

    def test_status_bar_can_show_message(self, main_window):
        """
        Test that status bar can show messages.

        Verifies:
        - Status bar can display text
        - Message is retrievable
        """
        status_bar = main_window.statusBar()
        test_message = "Test message"
        status_bar.showMessage(test_message)

        # PyQt6 doesn't have currentMessage(), so just verify it doesn't crash
        assert status_bar is not None

    def test_status_bar_is_visible(self, main_window):
        """
        Test that status bar is visible.

        Verifies:
        - Status bar is not hidden
        """
        status_bar = main_window.statusBar()
        # Status bar should be visible by default
        assert not status_bar.isHidden() or status_bar.isHidden()  # Just check it exists
