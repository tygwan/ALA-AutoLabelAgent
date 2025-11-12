"""Basic tests to verify pytest setup without GUI dependencies."""

import pytest


def test_python_version():
    """Test that Python version is 3.9+."""
    import sys

    assert sys.version_info >= (3, 9)


def test_basic_math():
    """Basic sanity check test."""
    assert 1 + 1 == 2


def test_imports():
    """Test that basic imports work."""
    import pathlib
    import sys
    from typing import Dict, List

    assert pathlib is not None
    assert sys is not None


@pytest.mark.unit
def test_with_marker():
    """Test with unit marker."""
    assert True
