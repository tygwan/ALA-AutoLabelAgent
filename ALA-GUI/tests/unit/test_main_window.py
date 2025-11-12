"""
Unit tests for MainWindow

M0: Project Setup - Sample test to verify pytest-qt setup
"""

import pytest

# Mark test as gui test (requires PyQt6 installed)
pytestmark = pytest.mark.gui


@pytest.fixture
def main_window(qtbot):
    """
    Fixture to create MainWindow instance.

    Args:
        qtbot: pytest-qt fixture for Qt widget testing

    Returns:
        MainWindow instance
    """
    try:
        from main import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)
        return window
    except ImportError:
        pytest.skip("PyQt6 not installed")


def test_main_window_title(main_window):
    """
    Test that main window has correct title.

    RED phase: This test will fail until PyQt6 is installed
    and main.py is properly implemented.
    """
    assert main_window.windowTitle() == "ALA-GUI - Auto Label Agent"


def test_main_window_size(main_window):
    """
    Test that main window has correct initial size.
    """
    geometry = main_window.geometry()
    assert geometry.width() == 800
    assert geometry.height() == 600


def test_main_window_has_central_widget(main_window):
    """
    Test that main window has a central widget.
    """
    assert main_window.centralWidget() is not None


@pytest.mark.skip(reason="Will implement in M2: PyQt6 Image Display & Navigation")
def test_main_window_menu_bar():
    """
    Test that main window has menu bar.

    Placeholder test for M2 milestone.
    """
    pass


@pytest.mark.skip(reason="Will implement in M2: PyQt6 Image Display & Navigation")
def test_main_window_toolbar():
    """
    Test that main window has toolbar.

    Placeholder test for M2 milestone.
    """
    pass
