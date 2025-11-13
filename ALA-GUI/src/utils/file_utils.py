"""
File I/O Utilities - File and directory operations.

Provides utilities for file system operations.
"""

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List

from utils.exceptions import AlaGuiException


class FileUtils:
    """
    FileUtils provides file system operations.

    Provides:
    - JSON file operations (load/save)
    - Directory operations (create, list)
    - File operations (copy, move, delete)
    - Safe file operations with backups

    All methods are static for utility usage.
    """

    @staticmethod
    def save_json(path: Path, data: Dict[str, Any]) -> None:
        """
        Save dictionary to JSON file.

        Args:
            path: Path to JSON file
            data: Dictionary to save

        Raises:
            AlaGuiException: If save fails
        """
        try:
            # Ensure Path object
            if not isinstance(path, Path):
                path = Path(path)

            # Ensure parent directory exists
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write JSON
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            raise AlaGuiException(
                f"Failed to save JSON: {e}",
                details={"path": str(path), "error": str(e)},
            )

    @staticmethod
    def load_json(path: Path) -> Dict[str, Any]:
        """
        Load JSON file.

        Args:
            path: Path to JSON file

        Returns:
            Loaded dictionary

        Raises:
            AlaGuiException: If file not found or invalid JSON
        """
        try:
            # Ensure Path object
            if not isinstance(path, Path):
                path = Path(path)

            # Check file exists
            if not path.exists():
                raise AlaGuiException(
                    f"JSON file not found: {path}", details={"path": str(path)}
                )

            # Load JSON
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)

        except json.JSONDecodeError as e:
            raise AlaGuiException(
                f"Invalid JSON format: {e}",
                details={"path": str(path), "error": str(e)},
            )
        except AlaGuiException:
            raise
        except Exception as e:
            raise AlaGuiException(
                f"Failed to load JSON: {e}",
                details={"path": str(path), "error": str(e)},
            )

    @staticmethod
    def ensure_directory(path: Path) -> None:
        """
        Ensure directory exists, create if not.

        Args:
            path: Path to directory
        """
        # Ensure Path object
        if not isinstance(path, Path):
            path = Path(path)

        # Create directory with parents
        path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def list_files(directory: Path, pattern: str = "*") -> List[Path]:
        """
        List files in directory.

        Args:
            directory: Directory path
            pattern: Glob pattern for filtering (default: all files)

        Returns:
            List of file paths
        """
        # Ensure Path object
        if not isinstance(directory, Path):
            directory = Path(directory)

        # Get all matching files (not directories)
        return [f for f in directory.glob(pattern) if f.is_file()]

    @staticmethod
    def copy_file(source: Path, destination: Path) -> None:
        """
        Copy file from source to destination.

        Args:
            source: Source file path
            destination: Destination file path

        Raises:
            AlaGuiException: If source not found or copy fails
        """
        try:
            # Ensure Path objects
            if not isinstance(source, Path):
                source = Path(source)
            if not isinstance(destination, Path):
                destination = Path(destination)

            # Check source exists
            if not source.exists():
                raise AlaGuiException(
                    f"Source file not found: {source}", details={"path": str(source)}
                )

            # Ensure destination directory exists
            destination.parent.mkdir(parents=True, exist_ok=True)

            # Copy file
            shutil.copy2(source, destination)

        except AlaGuiException:
            raise
        except Exception as e:
            raise AlaGuiException(
                f"Failed to copy file: {e}",
                details={
                    "source": str(source),
                    "destination": str(destination),
                    "error": str(e),
                },
            )

    @staticmethod
    def move_file(source: Path, destination: Path) -> None:
        """
        Move file from source to destination.

        Args:
            source: Source file path
            destination: Destination file path

        Raises:
            AlaGuiException: If source not found or move fails
        """
        try:
            # Ensure Path objects
            if not isinstance(source, Path):
                source = Path(source)
            if not isinstance(destination, Path):
                destination = Path(destination)

            # Check source exists
            if not source.exists():
                raise AlaGuiException(
                    f"Source file not found: {source}", details={"path": str(source)}
                )

            # Ensure destination directory exists
            destination.parent.mkdir(parents=True, exist_ok=True)

            # Move file
            shutil.move(str(source), str(destination))

        except AlaGuiException:
            raise
        except Exception as e:
            raise AlaGuiException(
                f"Failed to move file: {e}",
                details={
                    "source": str(source),
                    "destination": str(destination),
                    "error": str(e),
                },
            )

    @staticmethod
    def delete_file(path: Path, missing_ok: bool = True) -> None:
        """
        Delete file.

        Args:
            path: File path
            missing_ok: If True, don't raise error if file doesn't exist

        Raises:
            AlaGuiException: If file not found (when missing_ok=False) or delete fails
        """
        try:
            # Ensure Path object
            if not isinstance(path, Path):
                path = Path(path)

            # Check if file exists
            if not path.exists():
                if not missing_ok:
                    raise AlaGuiException(
                        f"File not found: {path}", details={"path": str(path)}
                    )
                return

            # Delete file
            path.unlink()

        except AlaGuiException:
            raise
        except Exception as e:
            raise AlaGuiException(
                f"Failed to delete file: {e}",
                details={"path": str(path), "error": str(e)},
            )

    @staticmethod
    def safe_write(path: Path, content: str) -> None:
        """
        Safely write to file with backup.

        Creates backup of existing file before writing.

        Args:
            path: File path
            content: Content to write

        Raises:
            AlaGuiException: If write fails
        """
        try:
            # Ensure Path object
            if not isinstance(path, Path):
                path = Path(path)

            # Create backup if file exists
            if path.exists():
                backup_path = path.with_suffix(path.suffix + ".bak")
                shutil.copy2(path, backup_path)

            # Ensure directory exists
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write content
            path.write_text(content, encoding="utf-8")

        except Exception as e:
            raise AlaGuiException(
                f"Failed to write file: {e}",
                details={"path": str(path), "error": str(e)},
            )
