"""
Logger - Structured logging system.

Provides centralized logging with file and console outputs.
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional


class Logger:
    """
    Logger handles application logging.

    Provides:
    - Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - File and console output
    - Structured logging with context
    - Configurable formatting

    Attributes:
        name: Logger name
        level: Current log level
        _logger: Internal Python logger instance
    """

    def __init__(
        self,
        name: str,
        log_dir: Optional[Path] = None,
        level: int = logging.INFO,
        console: bool = True,
    ) -> None:
        """
        Initialize Logger.

        Args:
            name: Logger name
            log_dir: Directory for log files, defaults to ./logs
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            console: Whether to output to console
        """
        self.name = name
        self.level = level

        # Create logger instance
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        self._logger.propagate = False

        # Clear any existing handlers
        self._logger.handlers.clear()

        # Set up log directory
        if log_dir is None:
            log_dir = Path("logs")
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Create formatters
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Add file handler
        log_file = self.log_dir / f"{name}.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(self.formatter)
        self._logger.addHandler(file_handler)

        # Add console handler if requested
        if console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(self.formatter)
            self._logger.addHandler(console_handler)

    def set_level(self, level: int) -> None:
        """
        Set logging level.

        Args:
            level: New logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.level = level
        self._logger.setLevel(level)
        for handler in self._logger.handlers:
            handler.setLevel(level)

    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Log debug message.

        Args:
            message: Log message
            extra: Additional context information
        """
        self._logger.debug(message, extra=extra or {})

    def info(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Log info message.

        Args:
            message: Log message
            extra: Additional context information
        """
        self._logger.info(message, extra=extra or {})

    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Log warning message.

        Args:
            message: Log message
            extra: Additional context information
        """
        self._logger.warning(message, extra=extra or {})

    def error(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Log error message.

        Args:
            message: Log message
            extra: Additional context information
        """
        self._logger.error(message, extra=extra or {})

    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Log critical message.

        Args:
            message: Log message
            extra: Additional context information
        """
        self._logger.critical(message, extra=extra or {})

    def exception(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Log exception with traceback.

        Args:
            message: Log message
            extra: Additional context information
        """
        self._logger.exception(message, extra=extra or {})
