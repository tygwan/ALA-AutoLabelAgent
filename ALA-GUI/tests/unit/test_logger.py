"""
Unit tests for Logger.

Following TDD RED-GREEN-REFACTOR cycle.
"""

import logging
from pathlib import Path

import pytest

from utils.logger import Logger


class TestLoggerInitialization:
    """Test suite for Logger initialization."""

    def test_logger_initialization(self, tmp_path):
        """Test Logger creates without errors."""
        # Arrange & Act
        logger = Logger(name="test_logger", log_dir=tmp_path)

        # Assert
        assert logger is not None
        assert logger.name == "test_logger"

    def test_logger_creates_log_directory(self, tmp_path):
        """Test Logger creates log directory if not exists."""
        # Arrange
        log_dir = tmp_path / "logs"
        assert not log_dir.exists()

        # Act
        Logger(name="test_logger", log_dir=log_dir)

        # Assert
        assert log_dir.exists()

    def test_logger_default_level_is_info(self, tmp_path):
        """Test Logger default level is INFO."""
        # Arrange & Act
        logger = Logger(name="test_logger", log_dir=tmp_path)

        # Assert
        assert logger.level == logging.INFO


class TestLoggerLevels:
    """Test suite for log level operations."""

    def test_set_debug_level(self, tmp_path):
        """Test setting DEBUG log level."""
        # Arrange
        logger = Logger(name="test_logger", log_dir=tmp_path)

        # Act
        logger.set_level(logging.DEBUG)

        # Assert
        assert logger.level == logging.DEBUG

    def test_set_warning_level(self, tmp_path):
        """Test setting WARNING log level."""
        # Arrange
        logger = Logger(name="test_logger", log_dir=tmp_path)

        # Act
        logger.set_level(logging.WARNING)

        # Assert
        assert logger.level == logging.WARNING

    def test_set_error_level(self, tmp_path):
        """Test setting ERROR log level."""
        # Arrange
        logger = Logger(name="test_logger", log_dir=tmp_path)

        # Act
        logger.set_level(logging.ERROR)

        # Assert
        assert logger.level == logging.ERROR


class TestLoggerOutputs:
    """Test suite for logging outputs."""

    def test_log_to_file(self, tmp_path):
        """Test logging to file."""
        # Arrange
        logger = Logger(name="test_logger", log_dir=tmp_path)
        log_file = tmp_path / "test_logger.log"

        # Act
        logger.info("Test message")

        # Assert
        assert log_file.exists()
        content = log_file.read_text()
        assert "Test message" in content

    def test_debug_message(self, tmp_path):
        """Test DEBUG level logging."""
        # Arrange
        logger = Logger(name="test_logger", log_dir=tmp_path, level=logging.DEBUG)
        log_file = tmp_path / "test_logger.log"

        # Act
        logger.debug("Debug message")

        # Assert
        content = log_file.read_text()
        assert "Debug message" in content
        assert "DEBUG" in content

    def test_info_message(self, tmp_path):
        """Test INFO level logging."""
        # Arrange
        logger = Logger(name="test_logger", log_dir=tmp_path)
        log_file = tmp_path / "test_logger.log"

        # Act
        logger.info("Info message")

        # Assert
        content = log_file.read_text()
        assert "Info message" in content
        assert "INFO" in content

    def test_warning_message(self, tmp_path):
        """Test WARNING level logging."""
        # Arrange
        logger = Logger(name="test_logger", log_dir=tmp_path)
        log_file = tmp_path / "test_logger.log"

        # Act
        logger.warning("Warning message")

        # Assert
        content = log_file.read_text()
        assert "Warning message" in content
        assert "WARNING" in content

    def test_error_message(self, tmp_path):
        """Test ERROR level logging."""
        # Arrange
        logger = Logger(name="test_logger", log_dir=tmp_path)
        log_file = tmp_path / "test_logger.log"

        # Act
        logger.error("Error message")

        # Assert
        content = log_file.read_text()
        assert "Error message" in content
        assert "ERROR" in content

    def test_critical_message(self, tmp_path):
        """Test CRITICAL level logging."""
        # Arrange
        logger = Logger(name="test_logger", log_dir=tmp_path)
        log_file = tmp_path / "test_logger.log"

        # Act
        logger.critical("Critical message")

        # Assert
        content = log_file.read_text()
        assert "Critical message" in content
        assert "CRITICAL" in content


class TestLoggerFormatting:
    """Test suite for log formatting."""

    def test_log_contains_timestamp(self, tmp_path):
        """Test log messages contain timestamp."""
        # Arrange
        logger = Logger(name="test_logger", log_dir=tmp_path)
        log_file = tmp_path / "test_logger.log"

        # Act
        logger.info("Test message")

        # Assert
        content = log_file.read_text()
        # Check for timestamp pattern (YYYY-MM-DD HH:MM:SS)
        assert content[0].isdigit()  # Starts with year

    def test_log_contains_logger_name(self, tmp_path):
        """Test log messages contain logger name."""
        # Arrange
        logger = Logger(name="test_logger", log_dir=tmp_path)
        log_file = tmp_path / "test_logger.log"

        # Act
        logger.info("Test message")

        # Assert
        content = log_file.read_text()
        assert "test_logger" in content


class TestLoggerContext:
    """Test suite for contextual logging."""

    def test_log_with_extra_context(self, tmp_path):
        """Test logging with extra context information."""
        # Arrange
        logger = Logger(name="test_logger", log_dir=tmp_path)
        log_file = tmp_path / "test_logger.log"

        # Act
        logger.info("User action", extra={"user_id": "123", "action": "save"})

        # Assert
        content = log_file.read_text()
        assert "User action" in content

    def test_log_exception(self, tmp_path):
        """Test logging exception with traceback."""
        # Arrange
        logger = Logger(name="test_logger", log_dir=tmp_path)
        log_file = tmp_path / "test_logger.log"

        # Act
        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.exception("Exception occurred")

        # Assert
        content = log_file.read_text()
        assert "Exception occurred" in content
        assert "ValueError: Test exception" in content
        assert "Traceback" in content


class TestLoggerLevelFiltering:
    """Test suite for log level filtering."""

    def test_debug_not_logged_at_info_level(self, tmp_path):
        """Test DEBUG messages not logged when level is INFO."""
        # Arrange
        logger = Logger(name="test_logger", log_dir=tmp_path, level=logging.INFO)
        log_file = tmp_path / "test_logger.log"

        # Act
        logger.debug("Debug message")
        logger.info("Info message")

        # Assert
        content = log_file.read_text()
        assert "Debug message" not in content
        assert "Info message" in content

    def test_info_not_logged_at_warning_level(self, tmp_path):
        """Test INFO messages not logged when level is WARNING."""
        # Arrange
        logger = Logger(name="test_logger", log_dir=tmp_path, level=logging.WARNING)
        log_file = tmp_path / "test_logger.log"

        # Act
        logger.info("Info message")
        logger.warning("Warning message")

        # Assert
        content = log_file.read_text()
        assert "Info message" not in content
        assert "Warning message" in content
