"""
Exception classes for ALA-GUI.

Provides a hierarchy of custom exceptions for different error scenarios.
"""

from typing import Any, Dict, Optional


class AlaGuiException(Exception):
    """
    Base exception for all ALA-GUI errors.

    Attributes:
        message: Error message
        details: Optional dictionary with additional error context
    """

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize exception.

        Args:
            message: Error message
            details: Optional dictionary with error context
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        """Return error message."""
        return self.message


class ProjectError(AlaGuiException):
    """
    Exception raised for project-related errors.

    Examples:
        - Project not found
        - Project load/save failure
        - Invalid project structure
    """

    pass


class ImageError(AlaGuiException):
    """
    Exception raised for image-related errors.

    Examples:
        - Image file not found
        - Invalid image format
        - Image load failure
        - Corrupted image data
    """

    pass


class ModelError(AlaGuiException):
    """
    Exception raised for model-related errors.

    Examples:
        - Model not found
        - Model load failure
        - Inference error
        - Invalid model format
    """

    pass


class ConfigError(AlaGuiException):
    """
    Exception raised for configuration errors.

    Examples:
        - Missing configuration key
        - Invalid configuration value
        - Configuration file not found
        - Configuration parsing error
    """

    pass
