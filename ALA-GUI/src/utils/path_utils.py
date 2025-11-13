"""
Path Utilities - Path validation and manipulation.

Provides utilities for safe path operations.
"""

import re
from pathlib import Path

from utils.exceptions import AlaGuiException


class PathUtils:
    """
    PathUtils provides path manipulation utilities.

    Provides:
    - Path validation (security checks)
    - Path sanitization (remove invalid characters)
    - Path normalization
    - Relative/absolute path operations
    - Path comparison

    All methods are static for utility usage.
    """

    # Invalid filename characters (Windows + Unix)
    INVALID_CHARS = r'<>:"|?*'

    @staticmethod
    def is_safe_path(path: Path, base_path: Path) -> bool:
        """
        Check if path is safe (no directory traversal).

        Args:
            path: Path to check
            base_path: Base directory path

        Returns:
            True if path is safe, False otherwise
        """
        try:
            # Ensure Path objects
            if not isinstance(path, Path):
                path = Path(path)
            if not isinstance(base_path, Path):
                base_path = Path(base_path)

            # Resolve to absolute paths
            abs_path = path.resolve()
            abs_base = base_path.resolve()

            # Check if path is under base
            try:
                abs_path.relative_to(abs_base)
                return True
            except ValueError:
                return False

        except Exception:
            return False

    @staticmethod
    def validate_safe_path(path: Path, base_path: Path) -> None:
        """
        Validate path is safe, raise if not.

        Args:
            path: Path to validate
            base_path: Base directory path

        Raises:
            AlaGuiException: If path is unsafe
        """
        if not PathUtils.is_safe_path(path, base_path):
            raise AlaGuiException(
                f"Unsafe path detected: {path}",
                details={"path": str(path), "base": str(base_path)},
            )

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename by removing invalid characters.

        Args:
            filename: Filename to sanitize

        Returns:
            Sanitized filename
        """
        # Replace invalid characters with underscore
        pattern = f"[{re.escape(PathUtils.INVALID_CHARS)}]"
        sanitized = re.sub(pattern, "_", filename)

        return sanitized

    @staticmethod
    def normalize_path(path: Path) -> Path:
        """
        Normalize path (resolve .., ., redundant separators).

        Args:
            path: Path to normalize

        Returns:
            Normalized path
        """
        # Ensure Path object
        if not isinstance(path, Path):
            path = Path(path)

        # Normalize using resolve
        return path.resolve()

    @staticmethod
    def make_relative_to(path: Path, base: Path) -> Path:
        """
        Make path relative to base.

        Args:
            path: Target path
            base: Base path

        Returns:
            Relative path
        """
        # Ensure Path objects
        if not isinstance(path, Path):
            path = Path(path)
        if not isinstance(base, Path):
            base = Path(base)

        # Make relative
        try:
            return path.relative_to(base)
        except ValueError:
            # If not relative, return absolute
            return path

    @staticmethod
    def resolve_relative_path(relative_path: Path, base: Path) -> Path:
        """
        Resolve relative path against base.

        Args:
            relative_path: Relative path
            base: Base path

        Returns:
            Absolute path
        """
        # Ensure Path objects
        if not isinstance(relative_path, Path):
            relative_path = Path(relative_path)
        if not isinstance(base, Path):
            base = Path(base)

        # Resolve relative path
        return (base / relative_path).resolve()

    @staticmethod
    def is_subpath(path: Path, parent: Path) -> bool:
        """
        Check if path is subpath of parent.

        Args:
            path: Path to check
            parent: Parent path

        Returns:
            True if path is under parent, False otherwise
        """
        try:
            # Ensure Path objects
            if not isinstance(path, Path):
                path = Path(path)
            if not isinstance(parent, Path):
                parent = Path(parent)

            # Resolve to absolute
            abs_path = path.resolve()
            abs_parent = parent.resolve()

            # Check if path is under parent
            try:
                abs_path.relative_to(abs_parent)
                return True
            except ValueError:
                return False

        except Exception:
            return False

    @staticmethod
    def get_extension(path: Path) -> str:
        """
        Get file extension.

        Args:
            path: File path

        Returns:
            Extension (e.g., '.txt'), empty string if no extension
        """
        # Ensure Path object
        if not isinstance(path, Path):
            path = Path(path)

        return path.suffix

    @staticmethod
    def get_stem(path: Path) -> str:
        """
        Get file stem (filename without extension).

        Args:
            path: File path

        Returns:
            Filename stem
        """
        # Ensure Path object
        if not isinstance(path, Path):
            path = Path(path)

        return path.stem

    @staticmethod
    def change_extension(path: Path, new_extension: str) -> Path:
        """
        Change file extension.

        Args:
            path: File path
            new_extension: New extension (with or without dot)

        Returns:
            Path with new extension
        """
        # Ensure Path object
        if not isinstance(path, Path):
            path = Path(path)

        # Ensure extension starts with dot
        if not new_extension.startswith("."):
            new_extension = "." + new_extension

        # Change extension
        return path.with_suffix(new_extension)
