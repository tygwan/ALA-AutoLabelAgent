"""
Unit tests for ProjectManager.

Following TDD RED-GREEN-REFACTOR cycle.
"""

from pathlib import Path
from uuid import UUID

import pytest

from controllers.project_manager import ProjectManager
from models import Image, Project


class TestProjectManagerInitialization:
    """Test suite for ProjectManager initialization."""

    def test_project_manager_initialization(self):
        """Test ProjectManager creates without errors."""
        # Arrange & Act
        manager = ProjectManager()

        # Assert
        assert manager is not None
        assert manager.current_project is None

    def test_project_manager_has_no_project_initially(self):
        """Test ProjectManager starts with no active project."""
        # Arrange & Act
        manager = ProjectManager()

        # Assert
        assert manager.current_project is None
        assert not manager.has_project()


class TestProjectManagerCreateProject:
    """Test suite for create_project() method."""

    def test_create_project_with_name_and_path(self, tmp_path):
        """Test creating a new project."""
        # Arrange
        manager = ProjectManager()
        name = "Test Project"
        path = tmp_path / "test_project"

        # Act
        project = manager.create_project(name=name, path=path)

        # Assert
        assert isinstance(project, Project)
        assert project.name == name
        assert project.path == path
        assert manager.current_project == project
        assert manager.has_project()

    def test_create_project_initializes_directory(self, tmp_path):
        """Test project directory is created."""
        # Arrange
        manager = ProjectManager()
        path = tmp_path / "test_project"

        # Act
        project = manager.create_project(name="Test", path=path)

        # Assert
        assert path.exists()
        assert path.is_dir()

    def test_create_project_with_description(self, tmp_path):
        """Test creating project with description."""
        # Arrange
        manager = ProjectManager()
        description = "Test project description"

        # Act
        project = manager.create_project(
            name="Test", path=tmp_path / "test", description=description
        )

        # Assert
        assert project.description == description

    def test_create_project_replaces_current_project(self, tmp_path):
        """Test creating new project replaces current one."""
        # Arrange
        manager = ProjectManager()
        project1 = manager.create_project(name="Project 1", path=tmp_path / "p1")

        # Act
        project2 = manager.create_project(name="Project 2", path=tmp_path / "p2")

        # Assert
        assert manager.current_project == project2
        assert manager.current_project != project1


class TestProjectManagerSaveProject:
    """Test suite for save_project() method."""

    def test_save_project_to_json(self, tmp_path):
        """Test saving project to JSON file."""
        # Arrange
        manager = ProjectManager()
        project = manager.create_project(name="Test", path=tmp_path / "test")

        # Act
        save_path = manager.save_project()

        # Assert
        assert save_path.exists()
        assert save_path.suffix == ".json"
        assert "project.json" in save_path.name

    def test_save_project_without_active_project_raises_error(self):
        """Test saving without active project raises error."""
        # Arrange
        manager = ProjectManager()

        # Act & Assert
        with pytest.raises(ValueError, match="No active project"):
            manager.save_project()

    def test_save_project_preserves_data(self, tmp_path):
        """Test saved project can be loaded back."""
        # Arrange
        manager = ProjectManager()
        project = manager.create_project(
            name="Test", path=tmp_path / "test", description="Test description"
        )

        # Act
        save_path = manager.save_project()

        # Assert
        import json

        with open(save_path, "r") as f:
            data = json.load(f)

        assert data["name"] == "Test"
        assert data["description"] == "Test description"


class TestProjectManagerLoadProject:
    """Test suite for load_project() method."""

    def test_load_project_from_json(self, tmp_path):
        """Test loading project from JSON file."""
        # Arrange
        manager = ProjectManager()
        original = manager.create_project(name="Test", path=tmp_path / "test")
        save_path = manager.save_project()

        # Create new manager and load
        new_manager = ProjectManager()

        # Act
        loaded = new_manager.load_project(save_path)

        # Assert
        assert isinstance(loaded, Project)
        assert loaded.name == original.name
        assert loaded.path == original.path
        assert new_manager.current_project == loaded

    def test_load_project_from_nonexistent_file_raises_error(self, tmp_path):
        """Test loading from non-existent file raises error."""
        # Arrange
        manager = ProjectManager()
        fake_path = tmp_path / "nonexistent.json"

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            manager.load_project(fake_path)


class TestProjectManagerAddImage:
    """Test suite for add_image() method."""

    def test_add_image_to_project(self, tmp_path):
        """Test adding image to current project."""
        # Arrange
        manager = ProjectManager()
        manager.create_project(name="Test", path=tmp_path / "test")
        image_path = tmp_path / "test.jpg"
        image_path.touch()  # Create dummy file

        # Act
        image = manager.add_image(path=image_path, width=1920, height=1080)

        # Assert
        assert isinstance(image, Image)
        assert image in manager.current_project.images
        assert len(manager.current_project.images) == 1

    def test_add_image_without_active_project_raises_error(self, tmp_path):
        """Test adding image without active project raises error."""
        # Arrange
        manager = ProjectManager()
        image_path = tmp_path / "test.jpg"

        # Act & Assert
        with pytest.raises(ValueError, match="No active project"):
            manager.add_image(path=image_path, width=1920, height=1080)

    def test_add_image_validates_file_exists(self, tmp_path):
        """Test adding non-existent image raises error."""
        # Arrange
        manager = ProjectManager()
        manager.create_project(name="Test", path=tmp_path / "test")
        fake_image = tmp_path / "nonexistent.jpg"

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            manager.add_image(path=fake_image, width=1920, height=1080)

    def test_add_multiple_images(self, tmp_path):
        """Test adding multiple images."""
        # Arrange
        manager = ProjectManager()
        manager.create_project(name="Test", path=tmp_path / "test")

        # Create dummy images
        img1 = tmp_path / "img1.jpg"
        img2 = tmp_path / "img2.jpg"
        img1.touch()
        img2.touch()

        # Act
        image1 = manager.add_image(path=img1, width=1920, height=1080)
        image2 = manager.add_image(path=img2, width=1280, height=720)

        # Assert
        assert len(manager.current_project.images) == 2
        assert image1 in manager.current_project.images
        assert image2 in manager.current_project.images
