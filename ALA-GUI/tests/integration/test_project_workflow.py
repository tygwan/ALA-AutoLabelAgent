"""
Integration tests for project workflow.

Tests complete workflows across multiple components.
"""

from pathlib import Path

import pytest

from controllers.project_manager import ProjectManager
from models import Image, Project
from utils import FileUtils, ImageUtils, Logger


class TestProjectCreationWorkflow:
    """Test suite for project creation workflow."""

    def test_create_and_save_project_workflow(self, tmp_path):
        """Test complete project creation and save workflow."""
        # Arrange
        project_dir = tmp_path / "test_project"
        manager = ProjectManager()

        # Act - Create project
        project = manager.create_project(
            name="Integration Test Project",
            path=project_dir,
            description="Testing integration",
        )

        # Act - Save project
        save_path = manager.save_project()

        # Assert - Verify project created
        assert project_dir.exists()
        assert save_path.exists()
        assert save_path == project_dir / "project.json"

        # Assert - Verify saved data
        saved_data = FileUtils.load_json(save_path)
        assert saved_data["name"] == "Integration Test Project"
        assert saved_data["description"] == "Testing integration"

    def test_create_save_and_load_project_workflow(self, tmp_path):
        """Test complete create, save, and load workflow."""
        # Arrange
        project_dir = tmp_path / "test_project"
        manager1 = ProjectManager()

        # Act - Create and save
        project1 = manager1.create_project(
            name="Test Project", path=project_dir, description="Test"
        )
        save_path = manager1.save_project()

        # Act - Load in new manager
        manager2 = ProjectManager()
        project2 = manager2.load_project(save_path)

        # Assert - Verify loaded project matches
        assert project2.name == project1.name
        assert project2.description == project1.description
        assert str(project2.path) == str(project1.path)


class TestImageIntegrationWorkflow:
    """Test suite for image integration workflow."""

    def test_add_image_to_project_workflow(self, tmp_path, sample_image_path):
        """Test adding image to project workflow."""
        # Arrange
        project_dir = tmp_path / "test_project"
        manager = ProjectManager()
        project = manager.create_project(name="Test", path=project_dir)

        # Act - Get image dimensions
        width, height = ImageUtils.get_dimensions(sample_image_path)

        # Act - Add image to project
        image = manager.add_image(sample_image_path, width, height)

        # Assert - Verify image added
        assert len(project.images) == 1
        assert image.path == sample_image_path
        assert image.width == width
        assert image.height == height

    def test_project_with_images_persistence_workflow(
        self, tmp_path, sample_image_path
    ):
        """Test project with images persists correctly."""
        # Arrange
        project_dir = tmp_path / "test_project"
        manager1 = ProjectManager()
        project1 = manager1.create_project(name="Test", path=project_dir)

        # Act - Add image and save
        width, height = ImageUtils.get_dimensions(sample_image_path)
        manager1.add_image(sample_image_path, width, height)
        save_path = manager1.save_project()

        # Act - Load in new manager
        manager2 = ProjectManager()
        project2 = manager2.load_project(save_path)

        # Assert - Verify images persisted
        assert len(project2.images) == 1
        assert project2.images[0].width == width
        assert project2.images[0].height == height


class TestLoggingIntegrationWorkflow:
    """Test suite for logging integration."""

    def test_log_project_operations_workflow(self, tmp_path):
        """Test logging project operations."""
        # Arrange
        log_dir = tmp_path / "logs"
        logger = Logger(name="project_test", log_dir=log_dir)
        project_dir = tmp_path / "test_project"
        manager = ProjectManager()

        # Act - Log project creation
        logger.info("Creating project", extra={"project_name": "Test Project"})
        project = manager.create_project(name="Test Project", path=project_dir)
        logger.info("Project created", extra={"project_id": str(project.id)})

        # Act - Log project save
        logger.info("Saving project")
        save_path = manager.save_project()
        logger.info("Project saved", extra={"path": str(save_path)})

        # Assert - Verify logs exist
        log_file = log_dir / "project_test.log"
        assert log_file.exists()

        # Assert - Verify log contents
        log_contents = log_file.read_text()
        assert "Creating project" in log_contents
        assert "Project created" in log_contents
        assert "Saving project" in log_contents
        assert "Project saved" in log_contents


class TestErrorHandlingIntegration:
    """Test suite for error handling integration."""

    def test_invalid_image_path_error_workflow(self, tmp_path):
        """Test error handling for invalid image path."""
        # Arrange
        project_dir = tmp_path / "test_project"
        manager = ProjectManager()
        project = manager.create_project(name="Test", path=project_dir)
        invalid_path = tmp_path / "nonexistent.jpg"

        # Act & Assert - Verify error raised
        with pytest.raises(FileNotFoundError, match="not found"):
            manager.add_image(invalid_path, 100, 100)

    def test_load_nonexistent_project_error_workflow(self, tmp_path):
        """Test error handling for non-existent project."""
        # Arrange
        manager = ProjectManager()
        nonexistent_path = tmp_path / "nonexistent" / "project.json"

        # Act & Assert - Verify error raised
        with pytest.raises(FileNotFoundError, match="not found"):
            manager.load_project(nonexistent_path)


class TestFileUtilsIntegration:
    """Test suite for file utilities integration."""

    def test_safe_project_save_with_backup_workflow(self, tmp_path):
        """Test safe project save creates backup."""
        # Arrange
        project_dir = tmp_path / "test_project"
        manager = ProjectManager()
        project = manager.create_project(name="Test V1", path=project_dir)

        # Act - Save initial version
        save_path = manager.save_project()
        initial_content = save_path.read_text()

        # Act - Modify and save again
        project.name = "Test V2"
        FileUtils.safe_write(save_path, FileUtils.load_json(save_path).__str__())

        # Assert - Verify backup created
        backup_path = save_path.with_suffix(".json.bak")
        assert backup_path.exists()

    def test_project_directory_creation_workflow(self, tmp_path):
        """Test project directory creation with nested paths."""
        # Arrange
        project_dir = tmp_path / "parent" / "child" / "project"
        assert not project_dir.exists()

        # Act - Create project (should create nested directories)
        manager = ProjectManager()
        project = manager.create_project(name="Nested", path=project_dir)

        # Assert - Verify all directories created
        assert project_dir.exists()
        assert project_dir.parent.exists()
        assert project_dir.parent.parent.exists()


class TestCompleteWorkflow:
    """Test suite for complete end-to-end workflows."""

    def test_complete_project_lifecycle(self, tmp_path, sample_image_path):
        """Test complete project lifecycle workflow."""
        # Arrange
        project_dir = tmp_path / "complete_test"
        log_dir = tmp_path / "logs"
        logger = Logger(name="lifecycle_test", log_dir=log_dir)

        # Act 1 - Create project
        logger.info("Starting project lifecycle test")
        manager = ProjectManager()
        project = manager.create_project(
            name="Complete Test", path=project_dir, description="Full workflow test"
        )
        logger.info(f"Project created: {project.id}")

        # Act 2 - Add images
        width, height = ImageUtils.get_dimensions(sample_image_path)
        image = manager.add_image(sample_image_path, width, height)
        logger.info(f"Image added: {image.id}")

        # Act 3 - Save project
        save_path = manager.save_project()
        logger.info(f"Project saved: {save_path}")

        # Act 4 - Verify saved files
        assert save_path.exists()
        saved_data = FileUtils.load_json(save_path)
        assert saved_data["name"] == "Complete Test"
        assert len(saved_data["images"]) == 1

        # Act 5 - Load project in new manager
        new_manager = ProjectManager()
        loaded_project = new_manager.load_project(save_path)
        logger.info(f"Project loaded: {loaded_project.id}")

        # Assert - Verify complete workflow
        assert loaded_project.name == project.name
        assert len(loaded_project.images) == 1
        assert loaded_project.images[0].width == width

        # Assert - Verify logs
        log_file = log_dir / "lifecycle_test.log"
        assert log_file.exists()
        log_contents = log_file.read_text()
        assert "Starting project lifecycle test" in log_contents
        assert "Project created" in log_contents
        assert "Image added" in log_contents
        assert "Project saved" in log_contents
        assert "Project loaded" in log_contents
