"""
Unit tests for Project data model.

Following TDD RED-GREEN-REFACTOR cycle.
"""

from datetime import datetime
from pathlib import Path
from uuid import UUID

import pytest

from models.project import Project


class TestProjectDataclass:
    """Test suite for Project dataclass."""

    def test_project_initialization(self):
        """Test Project creates with required fields."""
        # Arrange
        name = "Test Project"
        path = Path("/tmp/test_project")

        # Act
        project = Project(name=name, path=path)

        # Assert
        assert project.name == name
        assert project.path == path
        assert isinstance(project.id, UUID)
        assert isinstance(project.created_at, datetime)
        assert isinstance(project.updated_at, datetime)
        assert project.images == []
        assert project.classes == []

    def test_project_uuid_uniqueness(self):
        """Test each Project gets unique UUID."""
        # Arrange & Act
        project1 = Project(name="Project 1", path=Path("/tmp/p1"))
        project2 = Project(name="Project 2", path=Path("/tmp/p2"))

        # Assert
        assert project1.id != project2.id

    def test_project_with_optional_fields(self):
        """Test Project with description."""
        # Arrange
        name = "Test Project"
        path = Path("/tmp/test")
        description = "Test description"

        # Act
        project = Project(name=name, path=path, description=description)

        # Assert
        assert project.description == description

    def test_project_name_required(self):
        """Test Project requires name."""
        # Arrange & Act & Assert
        with pytest.raises(TypeError):
            Project(path=Path("/tmp/test"))

    def test_project_path_required(self):
        """Test Project requires path."""
        # Arrange & Act & Assert
        with pytest.raises(TypeError):
            Project(name="Test")

    def test_project_timestamps_auto_set(self):
        """Test created_at and updated_at are automatically set."""
        # Arrange & Act
        before = datetime.now()
        project = Project(name="Test", path=Path("/tmp/test"))
        after = datetime.now()

        # Assert
        assert before <= project.created_at <= after
        assert before <= project.updated_at <= after

    def test_project_to_dict(self):
        """Test Project serialization to dict."""
        # Arrange
        project = Project(name="Test", path=Path("/tmp/test"))

        # Act
        data = project.to_dict()

        # Assert
        assert isinstance(data, dict)
        assert data["name"] == "Test"
        assert data["path"] == "/tmp/test"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_project_from_dict(self):
        """Test Project deserialization from dict."""
        # Arrange
        data = {
            "name": "Test",
            "path": "/tmp/test",
            "description": "Test description",
        }

        # Act
        project = Project.from_dict(data)

        # Assert
        assert project.name == "Test"
        assert project.path == Path("/tmp/test")
        assert project.description == "Test description"
