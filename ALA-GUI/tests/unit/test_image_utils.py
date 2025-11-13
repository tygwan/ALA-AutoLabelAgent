"""
Unit tests for Image Utilities.

Following TDD RED-GREEN-REFACTOR cycle.
"""

from pathlib import Path

import pytest

from utils.exceptions import ImageError
from utils.image_utils import ImageUtils


class TestImageValidation:
    """Test suite for image validation."""

    def test_is_valid_image_format_jpg(self):
        """Test JPG format validation."""
        # Arrange & Act
        result = ImageUtils.is_valid_format("test.jpg")

        # Assert
        assert result is True

    def test_is_valid_image_format_png(self):
        """Test PNG format validation."""
        # Arrange & Act
        result = ImageUtils.is_valid_format("test.png")

        # Assert
        assert result is True

    def test_is_valid_image_format_jpeg(self):
        """Test JPEG format validation."""
        # Arrange & Act
        result = ImageUtils.is_valid_format("test.jpeg")

        # Assert
        assert result is True

    def test_is_valid_image_format_bmp(self):
        """Test BMP format validation."""
        # Arrange & Act
        result = ImageUtils.is_valid_format("test.bmp")

        # Assert
        assert result is True

    def test_is_invalid_image_format(self):
        """Test invalid format returns False."""
        # Arrange & Act
        result = ImageUtils.is_valid_format("test.txt")

        # Assert
        assert result is False

    def test_is_valid_format_case_insensitive(self):
        """Test format validation is case insensitive."""
        # Arrange & Act
        result1 = ImageUtils.is_valid_format("test.JPG")
        result2 = ImageUtils.is_valid_format("test.PNG")

        # Assert
        assert result1 is True
        assert result2 is True

    def test_validate_path_exists(self, tmp_path):
        """Test path validation for existing file."""
        # Arrange
        image_file = tmp_path / "test.jpg"
        image_file.write_bytes(b"fake image data")

        # Act & Assert - should not raise
        ImageUtils.validate_path(image_file)

    def test_validate_path_not_exists_raises_error(self, tmp_path):
        """Test path validation raises error for non-existent file."""
        # Arrange
        image_file = tmp_path / "nonexistent.jpg"

        # Act & Assert
        with pytest.raises(ImageError, match="not found"):
            ImageUtils.validate_path(image_file)

    def test_validate_path_invalid_format_raises_error(self, tmp_path):
        """Test path validation raises error for invalid format."""
        # Arrange
        text_file = tmp_path / "test.txt"
        text_file.write_text("not an image")

        # Act & Assert
        with pytest.raises(ImageError, match="Invalid image format"):
            ImageUtils.validate_path(text_file)


class TestImageLoading:
    """Test suite for image loading operations."""

    def test_get_image_dimensions(self, sample_image_path):
        """Test getting image dimensions."""
        # Arrange & Act
        width, height = ImageUtils.get_dimensions(sample_image_path)

        # Assert
        assert isinstance(width, int)
        assert isinstance(height, int)
        assert width > 0
        assert height > 0

    def test_get_dimensions_invalid_file_raises_error(self, tmp_path):
        """Test get dimensions raises error for invalid file."""
        # Arrange
        invalid_file = tmp_path / "invalid.jpg"
        invalid_file.write_text("not an image")

        # Act & Assert
        with pytest.raises(ImageError, match="Cannot read image"):
            ImageUtils.get_dimensions(invalid_file)

    def test_get_image_size_bytes(self, sample_image_path):
        """Test getting image file size."""
        # Arrange & Act
        size = ImageUtils.get_file_size(sample_image_path)

        # Assert
        assert isinstance(size, int)
        assert size > 0

    def test_get_image_format(self, sample_image_path):
        """Test getting image format."""
        # Arrange & Act
        fmt = ImageUtils.get_format(sample_image_path)

        # Assert
        assert isinstance(fmt, str)
        assert fmt.lower() in ["jpg", "jpeg", "png", "bmp", "gif", "tiff"]


class TestImageMetadata:
    """Test suite for image metadata extraction."""

    def test_get_image_info(self, sample_image_path):
        """Test getting comprehensive image info."""
        # Arrange & Act
        info = ImageUtils.get_info(sample_image_path)

        # Assert
        assert isinstance(info, dict)
        assert "width" in info
        assert "height" in info
        assert "format" in info
        assert "size_bytes" in info
        assert "path" in info

    def test_image_info_has_correct_types(self, sample_image_path):
        """Test image info returns correct types."""
        # Arrange & Act
        info = ImageUtils.get_info(sample_image_path)

        # Assert
        assert isinstance(info["width"], int)
        assert isinstance(info["height"], int)
        assert isinstance(info["format"], str)
        assert isinstance(info["size_bytes"], int)
        assert isinstance(info["path"], str)

    def test_image_info_path_is_absolute(self, sample_image_path):
        """Test image info path is absolute."""
        # Arrange & Act
        info = ImageUtils.get_info(sample_image_path)

        # Assert
        path = Path(info["path"])
        assert path.is_absolute()


class TestImageAspectRatio:
    """Test suite for aspect ratio calculations."""

    def test_calculate_aspect_ratio(self):
        """Test aspect ratio calculation."""
        # Arrange & Act
        ratio = ImageUtils.calculate_aspect_ratio(1920, 1080)

        # Assert
        assert isinstance(ratio, float)
        assert ratio == pytest.approx(16 / 9, rel=0.01)

    def test_aspect_ratio_square(self):
        """Test aspect ratio for square image."""
        # Arrange & Act
        ratio = ImageUtils.calculate_aspect_ratio(100, 100)

        # Assert
        assert ratio == 1.0

    def test_aspect_ratio_zero_height_returns_zero(self):
        """Test aspect ratio returns 0 for zero height."""
        # Arrange & Act
        ratio = ImageUtils.calculate_aspect_ratio(100, 0)

        # Assert
        assert ratio == 0.0


class TestImageUtilsEdgeCases:
    """Test suite for edge cases."""

    def test_validate_path_with_spaces(self, tmp_path):
        """Test path validation with spaces in filename."""
        # Arrange
        image_file = tmp_path / "test image.jpg"
        image_file.write_bytes(b"fake image data")

        # Act & Assert - should not raise
        ImageUtils.validate_path(image_file)

    def test_validate_path_with_unicode(self, tmp_path):
        """Test path validation with unicode characters."""
        # Arrange
        image_file = tmp_path / "테스트_이미지.jpg"
        image_file.write_bytes(b"fake image data")

        # Act & Assert - should not raise
        ImageUtils.validate_path(image_file)
