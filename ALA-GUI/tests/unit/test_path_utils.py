"""
Unit tests for Path Utilities.

Following TDD RED-GREEN-REFACTOR cycle.
"""

from pathlib import Path

import pytest

from utils.exceptions import AlaGuiException
from utils.path_utils import PathUtils


class TestPathValidation:
    """Test suite for path validation."""

    def test_is_safe_path_valid(self, tmp_path):
        """Test safe path validation."""
        # Arrange
        safe_path = tmp_path / "subfolder" / "file.txt"

        # Act
        result = PathUtils.is_safe_path(safe_path, tmp_path)

        # Assert
        assert result is True

    def test_is_safe_path_traversal_attack(self, tmp_path):
        """Test path traversal detection."""
        # Arrange
        unsafe_path = tmp_path / ".." / ".." / "etc" / "passwd"

        # Act
        result = PathUtils.is_safe_path(unsafe_path, tmp_path)

        # Assert
        assert result is False

    def test_is_safe_path_absolute_outside_base(self, tmp_path):
        """Test absolute path outside base is unsafe."""
        # Arrange
        unsafe_path = Path("/etc/passwd")

        # Act
        result = PathUtils.is_safe_path(unsafe_path, tmp_path)

        # Assert
        assert result is False

    def test_validate_safe_path_valid(self, tmp_path):
        """Test validate_safe_path doesn't raise for valid path."""
        # Arrange
        safe_path = tmp_path / "file.txt"

        # Act & Assert - should not raise
        PathUtils.validate_safe_path(safe_path, tmp_path)

    def test_validate_safe_path_invalid_raises(self, tmp_path):
        """Test validate_safe_path raises for invalid path."""
        # Arrange
        unsafe_path = tmp_path / ".." / ".." / "etc"

        # Act & Assert
        with pytest.raises(AlaGuiException, match="Unsafe path"):
            PathUtils.validate_safe_path(unsafe_path, tmp_path)


class TestPathSanitization:
    """Test suite for path sanitization."""

    def test_sanitize_filename_removes_invalid_chars(self):
        """Test sanitizing filename removes invalid characters."""
        # Arrange
        filename = 'file<>:"|?*.txt'

        # Act
        sanitized = PathUtils.sanitize_filename(filename)

        # Assert
        assert "<" not in sanitized
        assert ">" not in sanitized
        assert ":" not in sanitized
        assert '"' not in sanitized
        assert "|" not in sanitized
        assert "?" not in sanitized
        assert "*" not in sanitized

    def test_sanitize_filename_preserves_valid_chars(self):
        """Test sanitizing filename preserves valid characters."""
        # Arrange
        filename = "valid_file-name.123.txt"

        # Act
        sanitized = PathUtils.sanitize_filename(filename)

        # Assert
        assert sanitized == filename

    def test_sanitize_filename_handles_unicode(self):
        """Test sanitizing filename handles unicode."""
        # Arrange
        filename = "테스트_파일.txt"

        # Act
        sanitized = PathUtils.sanitize_filename(filename)

        # Assert
        assert "테스트" in sanitized
        assert "파일" in sanitized

    def test_sanitize_filename_replaces_with_underscore(self):
        """Test invalid characters replaced with underscore."""
        # Arrange
        filename = "file:name.txt"

        # Act
        sanitized = PathUtils.sanitize_filename(filename)

        # Assert
        assert sanitized == "file_name.txt"


class TestPathNormalization:
    """Test suite for path normalization."""

    def test_normalize_path(self, tmp_path):
        """Test path normalization."""
        # Arrange
        path = tmp_path / "folder" / ".." / "file.txt"

        # Act
        normalized = PathUtils.normalize_path(path)

        # Assert
        assert ".." not in str(normalized)
        assert normalized == tmp_path / "file.txt"

    def test_normalize_path_removes_redundant_separators(self, tmp_path):
        """Test normalization removes redundant separators."""
        # Arrange
        path_str = str(tmp_path / "folder" / "" / "file.txt")

        # Act
        normalized = PathUtils.normalize_path(path_str)

        # Assert
        assert isinstance(normalized, Path)


class TestRelativePathOperations:
    """Test suite for relative path operations."""

    def test_make_relative_to(self, tmp_path):
        """Test making path relative to base."""
        # Arrange
        base = tmp_path
        target = tmp_path / "subfolder" / "file.txt"

        # Act
        relative = PathUtils.make_relative_to(target, base)

        # Assert
        assert not relative.is_absolute()
        assert str(relative) == str(Path("subfolder") / "file.txt")

    def test_make_relative_to_same_path(self, tmp_path):
        """Test making path relative to itself."""
        # Arrange
        path = tmp_path / "file.txt"

        # Act
        relative = PathUtils.make_relative_to(path, path)

        # Assert
        assert str(relative) == "."

    def test_resolve_relative_path(self, tmp_path):
        """Test resolving relative path."""
        # Arrange
        base = tmp_path
        relative = Path("subfolder") / "file.txt"

        # Act
        absolute = PathUtils.resolve_relative_path(relative, base)

        # Assert
        assert absolute.is_absolute()
        assert absolute == tmp_path / "subfolder" / "file.txt"


class TestPathComparison:
    """Test suite for path comparison."""

    def test_is_subpath_true(self, tmp_path):
        """Test subpath detection."""
        # Arrange
        parent = tmp_path
        child = tmp_path / "subfolder" / "file.txt"

        # Act
        result = PathUtils.is_subpath(child, parent)

        # Assert
        assert result is True

    def test_is_subpath_false(self, tmp_path):
        """Test non-subpath detection."""
        # Arrange
        path1 = tmp_path / "folder1"
        path2 = tmp_path / "folder2" / "file.txt"

        # Act
        result = PathUtils.is_subpath(path2, path1)

        # Assert
        assert result is False

    def test_is_subpath_same_path(self, tmp_path):
        """Test same path is considered subpath."""
        # Arrange
        path = tmp_path / "file.txt"

        # Act
        result = PathUtils.is_subpath(path, path)

        # Assert
        assert result is True


class TestPathInfo:
    """Test suite for path information extraction."""

    def test_get_extension(self):
        """Test getting file extension."""
        # Arrange
        path = Path("file.txt")

        # Act
        ext = PathUtils.get_extension(path)

        # Assert
        assert ext == ".txt"

    def test_get_extension_no_extension(self):
        """Test getting extension from file without extension."""
        # Arrange
        path = Path("file")

        # Act
        ext = PathUtils.get_extension(path)

        # Assert
        assert ext == ""

    def test_get_stem(self):
        """Test getting file stem."""
        # Arrange
        path = Path("folder") / "file.txt"

        # Act
        stem = PathUtils.get_stem(path)

        # Assert
        assert stem == "file"

    def test_change_extension(self):
        """Test changing file extension."""
        # Arrange
        path = Path("file.txt")

        # Act
        new_path = PathUtils.change_extension(path, ".json")

        # Assert
        assert new_path.suffix == ".json"
        assert new_path.stem == "file"
