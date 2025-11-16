"""
Unit tests for ClassListWidget.

Tests the class list widget component following TDD methodology.
"""

import pytest
from PyQt6.QtWidgets import QAbstractItemView, QListWidget

# Mark all tests in this module as unit tests and GUI tests
pytestmark = [pytest.mark.unit, pytest.mark.gui]


@pytest.fixture
def class_list_widget(qtbot):
    """
    Fixture to create a ClassListWidget for testing.

    Args:
        qtbot: pytest-qt fixture for Qt widget testing

    Returns:
        ClassListWidget instance
    """
    from views.class_list_widget import ClassListWidget

    widget = ClassListWidget()
    qtbot.addWidget(widget)
    return widget


class TestClassListWidgetInitialization:
    """Tests for ClassListWidget initialization."""

    def test_widget_creation(self, class_list_widget):
        """Test that ClassListWidget can be created."""
        assert class_list_widget is not None
        from views.class_list_widget import ClassListWidget

        assert isinstance(class_list_widget, ClassListWidget)
        assert isinstance(class_list_widget, QListWidget)

    def test_widget_starts_empty(self, class_list_widget):
        """Test that widget starts with no items."""
        assert class_list_widget.count() == 0

    def test_view_mode_is_list(self, class_list_widget):
        """Test that view mode is set to list mode."""
        assert class_list_widget.viewMode() == QListWidget.ViewMode.ListMode

    def test_selection_mode_is_single(self, class_list_widget):
        """Test that selection mode is single selection."""
        assert (
            class_list_widget.selectionMode()
            == QAbstractItemView.SelectionMode.SingleSelection
        )

    def test_widget_has_context_menu(self, class_list_widget):
        """Test that widget has context menu enabled."""
        from PyQt6.QtCore import Qt

        assert (
            class_list_widget.contextMenuPolicy()
            == Qt.ContextMenuPolicy.CustomContextMenu
        )

    def test_widget_is_sortable(self, class_list_widget):
        """Test that widget has sorting enabled."""
        assert class_list_widget.isSortingEnabled() is True


class TestClassListWidgetAddClass:
    """Tests for adding classes to the widget."""

    def test_add_class_with_name_and_color(self, class_list_widget):
        """Test adding a class with name and color."""
        from PyQt6.QtGui import QColor

        result = class_list_widget.add_class("Person", QColor(255, 0, 0))
        assert result is True
        assert class_list_widget.count() == 1

    def test_add_class_item_has_correct_text(self, class_list_widget):
        """Test that added class item has correct text."""
        from PyQt6.QtGui import QColor

        class_list_widget.add_class("Car", QColor(0, 255, 0))
        item = class_list_widget.item(0)
        assert item.text() == "Car"

    def test_add_class_stores_color_in_data(self, class_list_widget):
        """Test that class color is stored in item data."""
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QColor

        color = QColor(0, 0, 255)
        class_list_widget.add_class("Building", color)
        item = class_list_widget.item(0)
        stored_color = item.data(Qt.ItemDataRole.UserRole)
        assert stored_color == color

    def test_add_multiple_classes(self, class_list_widget):
        """Test adding multiple classes."""
        from PyQt6.QtGui import QColor

        class_list_widget.add_class("Person", QColor(255, 0, 0))
        class_list_widget.add_class("Car", QColor(0, 255, 0))
        class_list_widget.add_class("Building", QColor(0, 0, 255))
        assert class_list_widget.count() == 3

    def test_add_class_with_empty_name_fails(self, class_list_widget):
        """Test that adding class with empty name fails."""
        from PyQt6.QtGui import QColor

        result = class_list_widget.add_class("", QColor(255, 0, 0))
        assert result is False
        assert class_list_widget.count() == 0

    def test_add_duplicate_class_name_fails(self, class_list_widget):
        """Test that adding duplicate class name fails."""
        from PyQt6.QtGui import QColor

        class_list_widget.add_class("Person", QColor(255, 0, 0))
        result = class_list_widget.add_class("Person", QColor(0, 255, 0))
        assert result is False
        assert class_list_widget.count() == 1

    def test_add_class_with_default_color(self, class_list_widget):
        """Test adding class with default color."""
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QColor

        result = class_list_widget.add_class("Person")
        assert result is True
        item = class_list_widget.item(0)
        stored_color = item.data(Qt.ItemDataRole.UserRole)
        assert isinstance(stored_color, QColor)

    def test_add_class_displays_color_badge(self, class_list_widget):
        """Test that added class displays color badge icon."""
        from PyQt6.QtGui import QColor

        class_list_widget.add_class("Person", QColor(255, 0, 0))
        item = class_list_widget.item(0)
        icon = item.icon()
        assert not icon.isNull()


class TestClassListWidgetRemoveClass:
    """Tests for removing classes from the widget."""

    def test_remove_class_by_index(self, class_list_widget):
        """Test removing a class by index."""
        from PyQt6.QtGui import QColor

        class_list_widget.add_class("Person", QColor(255, 0, 0))
        class_list_widget.add_class("Car", QColor(0, 255, 0))

        result = class_list_widget.remove_class(0)
        assert result is True
        assert class_list_widget.count() == 1

    def test_remove_class_by_name(self, class_list_widget):
        """Test removing a class by name."""
        from PyQt6.QtGui import QColor

        class_list_widget.add_class("Person", QColor(255, 0, 0))
        class_list_widget.add_class("Car", QColor(0, 255, 0))

        result = class_list_widget.remove_class_by_name("Person")
        assert result is True
        assert class_list_widget.count() == 1
        assert class_list_widget.item(0).text() == "Car"

    def test_remove_invalid_index_fails(self, class_list_widget):
        """Test that removing invalid index fails."""
        from PyQt6.QtGui import QColor

        class_list_widget.add_class("Person", QColor(255, 0, 0))

        result = class_list_widget.remove_class(5)
        assert result is False
        assert class_list_widget.count() == 1

    def test_remove_negative_index_fails(self, class_list_widget):
        """Test that removing negative index fails."""
        from PyQt6.QtGui import QColor

        class_list_widget.add_class("Person", QColor(255, 0, 0))

        result = class_list_widget.remove_class(-1)
        assert result is False
        assert class_list_widget.count() == 1

    def test_remove_nonexistent_name_fails(self, class_list_widget):
        """Test that removing nonexistent name fails."""
        from PyQt6.QtGui import QColor

        class_list_widget.add_class("Person", QColor(255, 0, 0))

        result = class_list_widget.remove_class_by_name("NonExistent")
        assert result is False
        assert class_list_widget.count() == 1

    def test_remove_all_classes(self, class_list_widget):
        """Test removing all classes one by one."""
        from PyQt6.QtGui import QColor

        class_list_widget.add_class("Person", QColor(255, 0, 0))
        class_list_widget.add_class("Car", QColor(0, 255, 0))
        class_list_widget.add_class("Building", QColor(0, 0, 255))

        class_list_widget.remove_class(0)
        class_list_widget.remove_class(0)
        class_list_widget.remove_class(0)

        assert class_list_widget.count() == 0


class TestClassListWidgetGetters:
    """Tests for getter methods."""

    def test_get_current_class(self, class_list_widget):
        """Test getting the currently selected class name."""
        from PyQt6.QtGui import QColor

        class_list_widget.add_class("Person", QColor(255, 0, 0))
        class_list_widget.add_class("Car", QColor(0, 255, 0))

        class_list_widget.setCurrentRow(0)
        assert class_list_widget.get_current_class() == "Person"

        class_list_widget.setCurrentRow(1)
        assert class_list_widget.get_current_class() == "Car"

    def test_get_current_class_no_selection(self, class_list_widget):
        """Test getting current class with no selection."""
        from PyQt6.QtGui import QColor

        class_list_widget.add_class("Person", QColor(255, 0, 0))
        assert class_list_widget.get_current_class() is None

    def test_get_class_color(self, class_list_widget):
        """Test getting a class color by name."""
        from PyQt6.QtGui import QColor

        red = QColor(255, 0, 0)
        class_list_widget.add_class("Person", red)

        color = class_list_widget.get_class_color("Person")
        assert color == red

    def test_get_class_color_nonexistent(self, class_list_widget):
        """Test getting color for nonexistent class."""
        color = class_list_widget.get_class_color("NonExistent")
        assert color is None

    def test_get_all_classes(self, class_list_widget):
        """Test getting all class names."""
        from PyQt6.QtGui import QColor

        class_list_widget.add_class("Person", QColor(255, 0, 0))
        class_list_widget.add_class("Car", QColor(0, 255, 0))
        class_list_widget.add_class("Building", QColor(0, 0, 255))

        classes = class_list_widget.get_all_classes()
        assert len(classes) == 3
        assert "Person" in classes
        assert "Car" in classes
        assert "Building" in classes
