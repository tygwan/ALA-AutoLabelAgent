"""
Unit tests for Image data model.

Following TDD RED-GREEN-REFACTOR cycle.
"""

from datetime import datetime
from pathlib import Path
from uuid import UUID

import pytest

from models.image import Image


class TestImageDataclass:
    """Test suite for Image dataclass."""

    def test_image_initialization(self):
        """Test Image creates with required fields."""
        # Arrange
        path = Path("/tmp/test.jpg")
        width = 1920
        height = 1080

        # Act
        image = Image(path=path, width=width, height=height)

        # Assert
        assert image.path == path
        assert image.filename == "test.jpg"
        assert image.width == width
        assert image.height == height
        assert isinstance(image.id, UUID)
        assert image.annotations == []
        assert isinstance(image.metadata, dict)

    def test_image_filename_auto_extracted(self):
        """Test filename is automatically extracted from path."""
        # Arrange & Act
        image = Image(path=Path("/folder/subfolder/image.png"), width=100, height=100)

        # Assert
        assert image.filename == "image.png"

    def test_image_uuid_uniqueness(self):
        """Test each Image gets unique UUID."""
        # Arrange & Act
        image1 = Image(path=Path("/tmp/img1.jpg"), width=100, height=100)
        image2 = Image(path=Path("/tmp/img2.jpg"), width=100, height=100)

        # Assert
        assert image1.id != image2.id

    def test_image_with_metadata(self):
        """Test Image with metadata."""
        # Arrange
        path = Path("/tmp/test.jpg")
        metadata = {"camera": "Canon EOS", "iso": 400}

        # Act
        image = Image(path=path, width=100, height=100, metadata=metadata)

        # Assert
        assert image.metadata == metadata

    def test_image_path_required(self):
        """Test Image requires path."""
        # Arrange & Act & Assert
        with pytest.raises(TypeError):
            Image(width=100, height=100)

    def test_image_dimensions_required(self):
        """Test Image requires width and height."""
        # Arrange & Act & Assert
        with pytest.raises(TypeError):
            Image(path=Path("/tmp/test.jpg"))

    def test_image_dimensions_positive(self):
        """Test Image dimensions must be positive."""
        # Arrange & Act
        image = Image(path=Path("/tmp/test.jpg"), width=1920, height=1080)

        # Assert
        assert image.width > 0
        assert image.height > 0

    def test_image_to_dict(self):
        """Test Image serialization to dict."""
        # Arrange
        image = Image(
            path=Path("/tmp/test.jpg"),
            width=1920,
            height=1080,
            metadata={"format": "JPEG"},
        )

        # Act
        data = image.to_dict()

        # Assert
        assert isinstance(data, dict)
        assert data["path"] == "/tmp/test.jpg"
        assert data["filename"] == "test.jpg"
        assert data["width"] == 1920
        assert data["height"] == 1080
        assert "id" in data
        assert data["metadata"] == {"format": "JPEG"}

    def test_image_from_dict(self):
        """Test Image deserialization from dict."""
        # Arrange
        data = {
            "path": "/tmp/test.jpg",
            "width": 1920,
            "height": 1080,
            "metadata": {"format": "JPEG"},
        }

        # Act
        image = Image.from_dict(data)

        # Assert
        assert image.path == Path("/tmp/test.jpg")
        assert image.filename == "test.jpg"
        assert image.width == 1920
        assert image.height == 1080
        assert image.metadata == {"format": "JPEG"}

    def test_image_aspect_ratio(self):
        """Test Image aspect ratio calculation."""
        # Arrange
        image = Image(path=Path("/tmp/test.jpg"), width=1920, height=1080)

        # Act
        aspect_ratio = image.aspect_ratio

        # Assert
        assert aspect_ratio == pytest.approx(16 / 9)

    def test_image_size_property(self):
        """Test Image size property returns (width, height)."""
        # Arrange
        image = Image(path=Path("/tmp/test.jpg"), width=1920, height=1080)

        # Act
        size = image.size

        # Assert
        assert size == (1920, 1080)
