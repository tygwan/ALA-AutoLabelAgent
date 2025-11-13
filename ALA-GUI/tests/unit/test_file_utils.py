"""
Unit tests for File I/O Utilities.

Following TDD RED-GREEN-REFACTOR cycle.
"""

import json
from pathlib import Path

import pytest

from utils.exceptions import AlaGuiException
from utils.file_utils import FileUtils


class TestJSONOperations:
    """Test suite for JSON file operations."""

    def test_save_json(self, tmp_path):
        """Test saving dictionary to JSON file."""
        # Arrange
        data = {"name": "test", "value": 123}
        json_file = tmp_path / "test.json"

        # Act
        FileUtils.save_json(json_file, data)

        # Assert
        assert json_file.exists()
        loaded = json.loads(json_file.read_text())
        assert loaded == data

    def test_load_json(self, tmp_path):
        """Test loading JSON file."""
        # Arrange
        data = {"name": "test", "value": 123}
        json_file = tmp_path / "test.json"
        json_file.write_text(json.dumps(data))

        # Act
        loaded = FileUtils.load_json(json_file)

        # Assert
        assert loaded == data

    def test_load_json_nonexistent_raises_error(self, tmp_path):
        """Test loading non-existent JSON raises error."""
        # Arrange
        json_file = tmp_path / "nonexistent.json"

        # Act & Assert
        with pytest.raises(AlaGuiException, match="not found"):
            FileUtils.load_json(json_file)

    def test_load_json_invalid_format_raises_error(self, tmp_path):
        """Test loading invalid JSON raises error."""
        # Arrange
        json_file = tmp_path / "invalid.json"
        json_file.write_text("not valid json {")

        # Act & Assert
        with pytest.raises(AlaGuiException, match="Invalid JSON"):
            FileUtils.load_json(json_file)

    def test_save_json_with_encoding(self, tmp_path):
        """Test saving JSON with unicode characters."""
        # Arrange
        data = {"name": "테스트", "value": "한글"}
        json_file = tmp_path / "test.json"

        # Act
        FileUtils.save_json(json_file, data)

        # Assert
        loaded = FileUtils.load_json(json_file)
        assert loaded == data


class TestDirectoryOperations:
    """Test suite for directory operations."""

    def test_ensure_directory_creates_dir(self, tmp_path):
        """Test ensure_directory creates directory."""
        # Arrange
        new_dir = tmp_path / "new_directory"
        assert not new_dir.exists()

        # Act
        FileUtils.ensure_directory(new_dir)

        # Assert
        assert new_dir.exists()
        assert new_dir.is_dir()

    def test_ensure_directory_existing_dir(self, tmp_path):
        """Test ensure_directory with existing directory."""
        # Arrange
        existing_dir = tmp_path / "existing"
        existing_dir.mkdir()

        # Act & Assert - should not raise
        FileUtils.ensure_directory(existing_dir)

    def test_ensure_directory_creates_parents(self, tmp_path):
        """Test ensure_directory creates parent directories."""
        # Arrange
        nested_dir = tmp_path / "parent" / "child" / "grandchild"
        assert not nested_dir.exists()

        # Act
        FileUtils.ensure_directory(nested_dir)

        # Assert
        assert nested_dir.exists()
        assert nested_dir.is_dir()

    def test_list_files_in_directory(self, tmp_path):
        """Test listing files in directory."""
        # Arrange
        (tmp_path / "file1.txt").write_text("content1")
        (tmp_path / "file2.txt").write_text("content2")
        (tmp_path / "subdir").mkdir()

        # Act
        files = FileUtils.list_files(tmp_path)

        # Assert
        assert len(files) == 2
        assert all(f.suffix == ".txt" for f in files)

    def test_list_files_with_pattern(self, tmp_path):
        """Test listing files with pattern."""
        # Arrange
        (tmp_path / "image1.jpg").write_bytes(b"img1")
        (tmp_path / "image2.png").write_bytes(b"img2")
        (tmp_path / "data.txt").write_text("text")

        # Act
        jpg_files = FileUtils.list_files(tmp_path, pattern="*.jpg")

        # Assert
        assert len(jpg_files) == 1
        assert jpg_files[0].suffix == ".jpg"


class TestFileCopy:
    """Test suite for file copy operations."""

    def test_copy_file(self, tmp_path):
        """Test copying file."""
        # Arrange
        source = tmp_path / "source.txt"
        source.write_text("test content")
        dest = tmp_path / "destination.txt"

        # Act
        FileUtils.copy_file(source, dest)

        # Assert
        assert dest.exists()
        assert dest.read_text() == "test content"

    def test_copy_file_to_existing_overwrites(self, tmp_path):
        """Test copying to existing file overwrites."""
        # Arrange
        source = tmp_path / "source.txt"
        source.write_text("new content")
        dest = tmp_path / "dest.txt"
        dest.write_text("old content")

        # Act
        FileUtils.copy_file(source, dest)

        # Assert
        assert dest.read_text() == "new content"

    def test_copy_file_nonexistent_raises_error(self, tmp_path):
        """Test copying non-existent file raises error."""
        # Arrange
        source = tmp_path / "nonexistent.txt"
        dest = tmp_path / "dest.txt"

        # Act & Assert
        with pytest.raises(AlaGuiException, match="not found"):
            FileUtils.copy_file(source, dest)


class TestFileMove:
    """Test suite for file move operations."""

    def test_move_file(self, tmp_path):
        """Test moving file."""
        # Arrange
        source = tmp_path / "source.txt"
        source.write_text("test content")
        dest = tmp_path / "destination.txt"

        # Act
        FileUtils.move_file(source, dest)

        # Assert
        assert not source.exists()
        assert dest.exists()
        assert dest.read_text() == "test content"

    def test_move_file_nonexistent_raises_error(self, tmp_path):
        """Test moving non-existent file raises error."""
        # Arrange
        source = tmp_path / "nonexistent.txt"
        dest = tmp_path / "dest.txt"

        # Act & Assert
        with pytest.raises(AlaGuiException, match="not found"):
            FileUtils.move_file(source, dest)


class TestFileDelete:
    """Test suite for file deletion."""

    def test_delete_file(self, tmp_path):
        """Test deleting file."""
        # Arrange
        file = tmp_path / "test.txt"
        file.write_text("content")
        assert file.exists()

        # Act
        FileUtils.delete_file(file)

        # Assert
        assert not file.exists()

    def test_delete_nonexistent_file_silent(self, tmp_path):
        """Test deleting non-existent file doesn't raise."""
        # Arrange
        file = tmp_path / "nonexistent.txt"

        # Act & Assert - should not raise
        FileUtils.delete_file(file, missing_ok=True)

    def test_delete_nonexistent_file_raises(self, tmp_path):
        """Test deleting non-existent file raises error."""
        # Arrange
        file = tmp_path / "nonexistent.txt"

        # Act & Assert
        with pytest.raises(AlaGuiException, match="not found"):
            FileUtils.delete_file(file, missing_ok=False)


class TestSafeFileOperations:
    """Test suite for safe file operations."""

    def test_safe_write_creates_backup(self, tmp_path):
        """Test safe write creates backup of existing file."""
        # Arrange
        file = tmp_path / "test.txt"
        file.write_text("original content")
        backup_file = tmp_path / "test.txt.bak"

        # Act
        FileUtils.safe_write(file, "new content")

        # Assert
        assert file.read_text() == "new content"
        assert backup_file.exists()
        assert backup_file.read_text() == "original content"

    def test_safe_write_new_file_no_backup(self, tmp_path):
        """Test safe write of new file doesn't create backup."""
        # Arrange
        file = tmp_path / "new.txt"
        backup_file = tmp_path / "new.txt.bak"

        # Act
        FileUtils.safe_write(file, "content")

        # Assert
        assert file.read_text() == "content"
        assert not backup_file.exists()
