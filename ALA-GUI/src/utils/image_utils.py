"""
Image Utilities - Image loading and validation.

Provides utilities for working with image files.
"""

from pathlib import Path
from typing import Dict, Tuple

from PIL import Image

from utils.exceptions import ImageError


class ImageUtils:
    """
    ImageUtils provides image file operations.

    Provides:
    - Image format validation
    - Dimension extraction
    - File size calculation
    - Metadata extraction
    - Aspect ratio calculation

    All methods are static for utility usage.
    """

    # Supported image formats
    SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".tif"}

    @staticmethod
    def is_valid_format(filename: str) -> bool:
        """
        Check if filename has valid image format.

        Args:
            filename: Image filename or path

        Returns:
            True if format is supported, False otherwise
        """
        path = Path(filename)
        extension = path.suffix.lower()
        return extension in ImageUtils.SUPPORTED_FORMATS

    @staticmethod
    def validate_path(path: Path) -> None:
        """
        Validate image file path.

        Args:
            path: Path to image file

        Raises:
            ImageError: If file doesn't exist or has invalid format
        """
        # Ensure Path object
        if not isinstance(path, Path):
            path = Path(path)

        # Check file exists
        if not path.exists():
            raise ImageError(
                f"Image file not found: {path}", details={"path": str(path)}
            )

        # Check format
        if not ImageUtils.is_valid_format(str(path)):
            raise ImageError(
                f"Invalid image format: {path.suffix}",
                details={"path": str(path), "format": path.suffix},
            )

    @staticmethod
    def get_dimensions(path: Path) -> Tuple[int, int]:
        """
        Get image dimensions.

        Args:
            path: Path to image file

        Returns:
            Tuple of (width, height)

        Raises:
            ImageError: If image cannot be read
        """
        try:
            # Ensure Path object
            if not isinstance(path, Path):
                path = Path(path)

            with Image.open(path) as img:
                width, height = img.size
                return width, height

        except Exception as e:
            raise ImageError(
                f"Cannot read image: {e}", details={"path": str(path), "error": str(e)}
            )

    @staticmethod
    def get_file_size(path: Path) -> int:
        """
        Get image file size in bytes.

        Args:
            path: Path to image file

        Returns:
            File size in bytes
        """
        # Ensure Path object
        if not isinstance(path, Path):
            path = Path(path)

        return path.stat().st_size

    @staticmethod
    def get_format(path: Path) -> str:
        """
        Get image format.

        Args:
            path: Path to image file

        Returns:
            Image format (e.g., 'JPEG', 'PNG')

        Raises:
            ImageError: If image cannot be read
        """
        try:
            # Ensure Path object
            if not isinstance(path, Path):
                path = Path(path)

            with Image.open(path) as img:
                return img.format or path.suffix.lstrip(".").upper()

        except Exception as e:
            raise ImageError(
                f"Cannot read image format: {e}",
                details={"path": str(path), "error": str(e)},
            )

    @staticmethod
    def get_info(path: Path) -> Dict[str, any]:
        """
        Get comprehensive image information.

        Args:
            path: Path to image file

        Returns:
            Dictionary with image metadata:
            - width: Image width in pixels
            - height: Image height in pixels
            - format: Image format
            - size_bytes: File size in bytes
            - path: Absolute path to file

        Raises:
            ImageError: If image cannot be read
        """
        # Ensure Path object
        if not isinstance(path, Path):
            path = Path(path)

        # Get dimensions
        width, height = ImageUtils.get_dimensions(path)

        # Get format
        fmt = ImageUtils.get_format(path)

        # Get file size
        size_bytes = ImageUtils.get_file_size(path)

        return {
            "width": width,
            "height": height,
            "format": fmt,
            "size_bytes": size_bytes,
            "path": str(path.absolute()),
        }

    @staticmethod
    def calculate_aspect_ratio(width: int, height: int) -> float:
        """
        Calculate aspect ratio.

        Args:
            width: Image width
            height: Image height

        Returns:
            Aspect ratio (width/height), 0.0 if height is 0
        """
        if height == 0:
            return 0.0
        return width / height
