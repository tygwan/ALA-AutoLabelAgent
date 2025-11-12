"""
Unit tests for Class data model.

Following TDD RED-GREEN-REFACTOR cycle.
"""

from uuid import UUID

import pytest

from models.class_definition import ClassDefinition


class TestClassDefinition:
    """Test suite for ClassDefinition dataclass."""

    def test_class_initialization(self):
        """Test ClassDefinition creates with required fields."""
        # Arrange
        name = "person"
        color = "#FF0000"

        # Act
        class_def = ClassDefinition(name=name, color=color)

        # Assert
        assert class_def.name == name
        assert class_def.color == color
        assert isinstance(class_def.id, UUID)
        assert class_def.description == ""

    def test_class_with_description(self):
        """Test ClassDefinition with description."""
        # Arrange
        name = "person"
        color = "#FF0000"
        description = "Human person"

        # Act
        class_def = ClassDefinition(name=name, color=color, description=description)

        # Assert
        assert class_def.description == description

    def test_class_uuid_uniqueness(self):
        """Test each ClassDefinition gets unique UUID."""
        # Arrange & Act
        class1 = ClassDefinition(name="person", color="#FF0000")
        class2 = ClassDefinition(name="car", color="#00FF00")

        # Assert
        assert class1.id != class2.id

    def test_class_name_required(self):
        """Test ClassDefinition requires name."""
        # Arrange & Act & Assert
        with pytest.raises(TypeError):
            ClassDefinition(color="#FF0000")

    def test_class_color_required(self):
        """Test ClassDefinition requires color."""
        # Arrange & Act & Assert
        with pytest.raises(TypeError):
            ClassDefinition(name="person")

    def test_class_color_validation(self):
        """Test ClassDefinition validates color format."""
        # Arrange & Act
        class_def = ClassDefinition(name="person", color="#FF0000")

        # Assert
        assert class_def.is_valid_color()

    def test_class_color_invalid_format(self):
        """Test ClassDefinition detects invalid color."""
        # Arrange & Act
        class_def = ClassDefinition(name="person", color="red")

        # Assert
        assert not class_def.is_valid_color()

    def test_class_rgb_tuple(self):
        """Test ClassDefinition converts hex to RGB tuple."""
        # Arrange
        class_def = ClassDefinition(name="person", color="#FF0000")

        # Act
        rgb = class_def.rgb_tuple

        # Assert
        assert rgb == (255, 0, 0)

    def test_class_to_dict(self):
        """Test ClassDefinition serialization to dict."""
        # Arrange
        class_def = ClassDefinition(
            name="person", color="#FF0000", description="Human person"
        )

        # Act
        data = class_def.to_dict()

        # Assert
        assert isinstance(data, dict)
        assert data["name"] == "person"
        assert data["color"] == "#FF0000"
        assert data["description"] == "Human person"
        assert "id" in data

    def test_class_from_dict(self):
        """Test ClassDefinition deserialization from dict."""
        # Arrange
        data = {
            "name": "person",
            "color": "#FF0000",
            "description": "Human person",
        }

        # Act
        class_def = ClassDefinition.from_dict(data)

        # Assert
        assert class_def.name == "person"
        assert class_def.color == "#FF0000"
        assert class_def.description == "Human person"

    def test_class_equality(self):
        """Test ClassDefinition equality by ID."""
        # Arrange
        class1 = ClassDefinition(name="person", color="#FF0000")
        class2 = ClassDefinition(name="person", color="#FF0000")

        # Assert
        assert class1 != class2  # Different IDs

    def test_class_str_representation(self):
        """Test ClassDefinition string representation."""
        # Arrange
        class_def = ClassDefinition(name="person", color="#FF0000")

        # Act
        str_repr = str(class_def)

        # Assert
        assert "person" in str_repr
        assert "#FF0000" in str_repr
