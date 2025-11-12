"""
Test utilities for ALA-GUI testing

Provides helper functions for testing PyQt6 widgets and image operations.
"""

from typing import Optional

import numpy as np

try:
    from PyQt6.QtCore import QSize
    from PyQt6.QtGui import QImage, QPixmap

    PYQT6_AVAILABLE = True
except ImportError:
    PYQT6_AVAILABLE = False


def pixmaps_equal(pixmap1: QPixmap, pixmap2: QPixmap, tolerance: int = 0) -> bool:
    """
    Compare two QPixmap objects for equality.

    Args:
        pixmap1: First QPixmap
        pixmap2: Second QPixmap
        tolerance: Maximum allowed difference per pixel (0-255)

    Returns:
        True if pixmaps are equal within tolerance
    """
    if not PYQT6_AVAILABLE:
        return False

    # Check if both are null
    if pixmap1.isNull() and pixmap2.isNull():
        return True

    # Check if one is null
    if pixmap1.isNull() or pixmap2.isNull():
        return False

    # Check dimensions
    if pixmap1.size() != pixmap2.size():
        return False

    # Convert to QImage for pixel comparison
    img1 = pixmap1.toImage()
    img2 = pixmap2.toImage()

    # Convert to numpy arrays
    width = img1.width()
    height = img1.height()

    # Compare pixel by pixel
    for y in range(height):
        for x in range(width):
            pixel1 = img1.pixel(x, y)
            pixel2 = img2.pixel(x, y)

            # Extract RGB values
            r1 = (pixel1 >> 16) & 0xFF
            g1 = (pixel1 >> 8) & 0xFF
            b1 = pixel1 & 0xFF

            r2 = (pixel2 >> 16) & 0xFF
            g2 = (pixel2 >> 8) & 0xFF
            b2 = pixel2 & 0xFF

            # Check difference
            if (
                abs(r1 - r2) > tolerance
                or abs(g1 - g2) > tolerance
                or abs(b1 - b2) > tolerance
            ):
                return False

    return True


def create_test_pixmap(
    width: int = 100, height: int = 100, color: tuple = (255, 0, 0)
) -> Optional[QPixmap]:
    """
    Create a test QPixmap with specified dimensions and color.

    Args:
        width: Image width in pixels
        height: Image height in pixels
        color: RGB color tuple (0-255)

    Returns:
        QPixmap filled with specified color
    """
    if not PYQT6_AVAILABLE:
        return None

    # Create numpy array
    r, g, b = color
    img_array = np.full((height, width, 3), [r, g, b], dtype=np.uint8)

    # Convert to QImage
    bytes_per_line = 3 * width
    qimage = QImage(
        img_array.data, width, height, bytes_per_line, QImage.Format.Format_RGB888
    )

    # Convert to QPixmap
    return QPixmap.fromImage(qimage)


def pixmap_to_numpy(pixmap: QPixmap) -> Optional[np.ndarray]:
    """
    Convert QPixmap to numpy array.

    Args:
        pixmap: Input QPixmap

    Returns:
        Numpy array in RGB format (H, W, 3)
    """
    if not PYQT6_AVAILABLE or pixmap.isNull():
        return None

    # Convert to QImage
    image = pixmap.toImage()
    image = image.convertToFormat(QImage.Format.Format_RGB888)

    width = image.width()
    height = image.height()
    bytes_per_line = image.bytesPerLine()

    # Get pointer to image data
    ptr = image.bits()
    ptr.setsize(height * bytes_per_line)

    # Convert to numpy array
    arr = np.frombuffer(ptr, np.uint8).reshape((height, bytes_per_line))

    # Extract RGB channels (ignore padding)
    return arr[:, : width * 3].reshape((height, width, 3))


def assert_pixmap_size(
    pixmap: QPixmap, expected_width: int, expected_height: int
) -> None:
    """
    Assert that QPixmap has expected dimensions.

    Args:
        pixmap: QPixmap to check
        expected_width: Expected width in pixels
        expected_height: Expected height in pixels

    Raises:
        AssertionError: If dimensions don't match
    """
    if not PYQT6_AVAILABLE:
        return

    actual_size = pixmap.size()
    expected_size = QSize(expected_width, expected_height)

    assert actual_size == expected_size, (
        f"Pixmap size mismatch: expected {expected_size.width()}x{expected_size.height()}, "
        f"got {actual_size.width()}x{actual_size.height()}"
    )


def assert_pixmap_not_null(pixmap: QPixmap) -> None:
    """
    Assert that QPixmap is not null.

    Args:
        pixmap: QPixmap to check

    Raises:
        AssertionError: If pixmap is null
    """
    if not PYQT6_AVAILABLE:
        return

    assert not pixmap.isNull(), "Pixmap should not be null"
