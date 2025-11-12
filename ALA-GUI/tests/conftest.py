"""
Pytest configuration and shared fixtures for ALA-GUI tests
"""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture(scope="session")
def qapp_cls():
    """
    Configure QApplication for pytest-qt.

    This fixture ensures QApplication is properly configured
    for all GUI tests.
    """
    try:
        from PyQt6.QtWidgets import QApplication

        return QApplication
    except ImportError:
        pytest.skip("PyQt6 not installed")


@pytest.fixture
def sample_image_path(tmp_path):
    """
    Create a sample image file for testing.

    Args:
        tmp_path: pytest temporary directory fixture

    Returns:
        Path to sample image file
    """
    import numpy as np

    try:
        from PIL import Image

        # Create a simple 100x100 RGB image
        img_array = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)

        img_path = tmp_path / "test_image.jpg"
        img.save(img_path)

        return img_path
    except ImportError:
        pytest.skip("PIL/Pillow not installed")


@pytest.fixture
def sample_annotation():
    """
    Create sample annotation data for testing.

    Returns:
        Dictionary with sample annotation data
    """
    return {
        "id": "test-annotation-1",
        "image_id": "test-image-1",
        "class_id": 0,
        "type": "polygon",
        "geometry": {"points": [[10, 10], [50, 10], [50, 50], [10, 50]]},
        "confidence": 0.95,
    }


@pytest.fixture
def sample_project(tmp_path):
    """
    Create sample project data for testing.

    Args:
        tmp_path: pytest temporary directory fixture

    Returns:
        Dictionary with sample project data
    """
    return {
        "name": "Test Project",
        "path": str(tmp_path / "test_project.alagui"),
        "classes": [
            {"id": 0, "name": "class_0", "color": "#FF0000"},
            {"id": 1, "name": "class_1", "color": "#00FF00"},
        ],
    }
