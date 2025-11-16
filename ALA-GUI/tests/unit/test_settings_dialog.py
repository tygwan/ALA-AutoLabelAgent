"""
Unit tests for SettingsDialog.

Tests the settings dialog component following TDD methodology.
"""

import pytest
from PyQt6.QtWidgets import QDialogButtonBox, QTabWidget

# Mark all tests in this module as unit tests and GUI tests
pytestmark = [pytest.mark.unit, pytest.mark.gui]


@pytest.fixture
def settings_dialog(qtbot):
    """
    Fixture to create a SettingsDialog for testing.

    Args:
        qtbot: pytest-qt fixture for Qt widget testing

    Returns:
        SettingsDialog instance
    """
    from views.settings_dialog import SettingsDialog

    dialog = SettingsDialog()
    qtbot.addWidget(dialog)
    return dialog


class TestSettingsDialogInitialization:
    """Tests for SettingsDialog initialization."""

    def test_dialog_creation(self, settings_dialog):
        """Test that SettingsDialog can be created."""
        assert settings_dialog is not None
        from views.settings_dialog import SettingsDialog

        assert isinstance(settings_dialog, SettingsDialog)

    def test_dialog_is_modal(self, settings_dialog):
        """Test that dialog is modal."""
        assert settings_dialog.isModal() is True

    def test_dialog_has_title(self, settings_dialog):
        """Test that dialog has a title."""
        assert settings_dialog.windowTitle() == "Settings"

    def test_dialog_has_tab_widget(self, settings_dialog):
        """Test that dialog contains a tab widget."""
        tab_widget = settings_dialog.findChild(QTabWidget)
        assert tab_widget is not None

    def test_dialog_has_button_box(self, settings_dialog):
        """Test that dialog has OK/Cancel buttons."""
        button_box = settings_dialog.findChild(QDialogButtonBox)
        assert button_box is not None

    def test_button_box_has_ok_cancel(self, settings_dialog):
        """Test that button box has OK and Cancel buttons."""
        button_box = settings_dialog.findChild(QDialogButtonBox)
        assert button_box is not None

        buttons = button_box.standardButtons()
        assert QDialogButtonBox.StandardButton.Ok in buttons
        assert QDialogButtonBox.StandardButton.Cancel in buttons

    def test_dialog_has_three_tabs(self, settings_dialog):
        """Test that dialog has three tabs (Appearance, Performance, Model)."""
        tab_widget = settings_dialog.findChild(QTabWidget)
        assert tab_widget is not None
        assert tab_widget.count() == 3


class TestAppearanceTab:
    """Tests for appearance settings tab."""

    def test_appearance_tab_exists(self, settings_dialog):
        """Test that appearance tab exists."""
        tab_widget = settings_dialog.findChild(QTabWidget)
        assert tab_widget.tabText(0) == "Appearance"

    def test_appearance_has_theme_setting(self, settings_dialog):
        """Test that appearance tab has theme setting."""
        assert hasattr(settings_dialog, "theme_combo")
        assert settings_dialog.theme_combo is not None

    def test_appearance_has_font_size_setting(self, settings_dialog):
        """Test that appearance tab has font size setting."""
        assert hasattr(settings_dialog, "font_size_spin")
        assert settings_dialog.font_size_spin is not None


class TestPerformanceTab:
    """Tests for performance settings tab."""

    def test_performance_tab_exists(self, settings_dialog):
        """Test that performance tab exists."""
        tab_widget = settings_dialog.findChild(QTabWidget)
        assert tab_widget.tabText(1) == "Performance"

    def test_performance_has_cache_setting(self, settings_dialog):
        """Test that performance tab has cache size setting."""
        assert hasattr(settings_dialog, "cache_size_spin")
        assert settings_dialog.cache_size_spin is not None

    def test_performance_has_threads_setting(self, settings_dialog):
        """Test that performance tab has thread count setting."""
        assert hasattr(settings_dialog, "thread_count_spin")
        assert settings_dialog.thread_count_spin is not None


class TestModelTab:
    """Tests for model settings tab."""

    def test_model_tab_exists(self, settings_dialog):
        """Test that model tab exists."""
        tab_widget = settings_dialog.findChild(QTabWidget)
        assert tab_widget.tabText(2) == "Model"

    def test_model_has_device_setting(self, settings_dialog):
        """Test that model tab has device setting."""
        assert hasattr(settings_dialog, "device_combo")
        assert settings_dialog.device_combo is not None

    def test_model_has_batch_size_setting(self, settings_dialog):
        """Test that model tab has batch size setting."""
        assert hasattr(settings_dialog, "batch_size_spin")
        assert settings_dialog.batch_size_spin is not None


class TestSettingsGettersSetters:
    """Tests for settings getter and setter methods."""

    def test_get_theme(self, settings_dialog):
        """Test getting theme setting."""
        theme = settings_dialog.get_theme()
        assert theme in ["Light", "Dark", "System"]

    def test_set_theme(self, settings_dialog):
        """Test setting theme."""
        settings_dialog.set_theme("Dark")
        assert settings_dialog.get_theme() == "Dark"

    def test_get_font_size(self, settings_dialog):
        """Test getting font size."""
        size = settings_dialog.get_font_size()
        assert isinstance(size, int)
        assert 8 <= size <= 24

    def test_set_font_size(self, settings_dialog):
        """Test setting font size."""
        settings_dialog.set_font_size(14)
        assert settings_dialog.get_font_size() == 14

    def test_get_cache_size(self, settings_dialog):
        """Test getting cache size."""
        size = settings_dialog.get_cache_size()
        assert isinstance(size, int)
        assert size > 0

    def test_set_cache_size(self, settings_dialog):
        """Test setting cache size."""
        settings_dialog.set_cache_size(512)
        assert settings_dialog.get_cache_size() == 512

    def test_get_thread_count(self, settings_dialog):
        """Test getting thread count."""
        count = settings_dialog.get_thread_count()
        assert isinstance(count, int)
        assert 1 <= count <= 16

    def test_set_thread_count(self, settings_dialog):
        """Test setting thread count."""
        settings_dialog.set_thread_count(4)
        assert settings_dialog.get_thread_count() == 4

    def test_get_device(self, settings_dialog):
        """Test getting inference device."""
        device = settings_dialog.get_device()
        assert device in ["CPU", "CUDA", "MPS"]

    def test_set_device(self, settings_dialog):
        """Test setting inference device."""
        settings_dialog.set_device("CPU")
        assert settings_dialog.get_device() == "CPU"

    def test_get_batch_size(self, settings_dialog):
        """Test getting batch size."""
        size = settings_dialog.get_batch_size()
        assert isinstance(size, int)
        assert 1 <= size <= 64

    def test_set_batch_size(self, settings_dialog):
        """Test setting batch size."""
        settings_dialog.set_batch_size(8)
        assert settings_dialog.get_batch_size() == 8
