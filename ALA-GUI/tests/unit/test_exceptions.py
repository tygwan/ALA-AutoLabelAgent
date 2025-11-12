"""
Unit tests for exception handling.

Following TDD RED-GREEN-REFACTOR cycle.
"""

import pytest

from utils.exceptions import (
    AlaGuiException,
    ConfigError,
    ImageError,
    ModelError,
    ProjectError,
)


class TestAlaGuiException:
    """Test suite for base AlaGuiException."""

    def test_base_exception_creation(self):
        """Test creating base exception."""
        # Arrange & Act
        exc = AlaGuiException("Test error")

        # Assert
        assert str(exc) == "Test error"
        assert isinstance(exc, Exception)

    def test_base_exception_with_details(self):
        """Test exception with additional details."""
        # Arrange & Act
        exc = AlaGuiException("Test error", details={"key": "value"})

        # Assert
        assert exc.details == {"key": "value"}

    def test_base_exception_inheritance(self):
        """Test all exceptions inherit from base."""
        # Arrange & Act & Assert
        assert issubclass(ProjectError, AlaGuiException)
        assert issubclass(ImageError, AlaGuiException)
        assert issubclass(ModelError, AlaGuiException)
        assert issubclass(ConfigError, AlaGuiException)


class TestProjectError:
    """Test suite for ProjectError."""

    def test_project_error_creation(self):
        """Test creating ProjectError."""
        # Arrange & Act
        exc = ProjectError("Project not found")

        # Assert
        assert str(exc) == "Project not found"
        assert isinstance(exc, AlaGuiException)

    def test_project_error_with_project_name(self):
        """Test ProjectError with project name in details."""
        # Arrange & Act
        exc = ProjectError("Load failed", details={"project": "test_project"})

        # Assert
        assert exc.details["project"] == "test_project"


class TestImageError:
    """Test suite for ImageError."""

    def test_image_error_creation(self):
        """Test creating ImageError."""
        # Arrange & Act
        exc = ImageError("Invalid image format")

        # Assert
        assert str(exc) == "Invalid image format"
        assert isinstance(exc, AlaGuiException)

    def test_image_error_with_path(self):
        """Test ImageError with image path."""
        # Arrange & Act
        exc = ImageError("Cannot load image", details={"path": "/tmp/test.jpg"})

        # Assert
        assert exc.details["path"] == "/tmp/test.jpg"


class TestModelError:
    """Test suite for ModelError."""

    def test_model_error_creation(self):
        """Test creating ModelError."""
        # Arrange & Act
        exc = ModelError("Model inference failed")

        # Assert
        assert str(exc) == "Model inference failed"
        assert isinstance(exc, AlaGuiException)

    def test_model_error_with_model_name(self):
        """Test ModelError with model name."""
        # Arrange & Act
        exc = ModelError("Load failed", details={"model": "florence-2"})

        # Assert
        assert exc.details["model"] == "florence-2"


class TestConfigError:
    """Test suite for ConfigError."""

    def test_config_error_creation(self):
        """Test creating ConfigError."""
        # Arrange & Act
        exc = ConfigError("Invalid configuration")

        # Assert
        assert str(exc) == "Invalid configuration"
        assert isinstance(exc, AlaGuiException)

    def test_config_error_with_key(self):
        """Test ConfigError with config key."""
        # Arrange & Act
        exc = ConfigError("Missing key", details={"key": "model_path"})

        # Assert
        assert exc.details["key"] == "model_path"


class TestExceptionContext:
    """Test exception context and chaining."""

    def test_exception_chaining(self):
        """Test exception chaining with from clause."""
        # Arrange
        original = ValueError("Original error")

        # Act
        try:
            try:
                raise original
            except ValueError as e:
                raise ProjectError("Wrapped error") from e
        except ProjectError as exc:
            # Assert
            assert exc.__cause__ == original
            assert str(exc) == "Wrapped error"

    def test_exception_details_serialization(self):
        """Test exception details can be serialized."""
        # Arrange & Act
        exc = ProjectError(
            "Test error", details={"project": "test", "path": "/tmp/test"}
        )

        # Assert
        assert isinstance(exc.details, dict)
        assert exc.details["project"] == "test"
        assert exc.details["path"] == "/tmp/test"
