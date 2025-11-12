"""
ConfigManager - Configuration management system.

Provides centralized configuration storage with type-safe access.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

from utils.exceptions import ConfigError


class ConfigManager:
    """
    ConfigManager handles application configuration.

    Provides:
    - Default configuration values
    - Type-safe getters (get_int, get_str, get_bool)
    - Configuration validation
    - Persistence to JSON file

    Attributes:
        _config: Internal configuration dictionary
        _config_file: Path to configuration file
    """

    # Default configuration
    DEFAULTS: Dict[str, Any] = {
        "app_name": "ALA-GUI",
        "version": "0.1.0",
        "window_width": 1280,
        "window_height": 720,
        "window_x": 100,
        "window_y": 100,
        "recent_projects": [],
        "max_recent_projects": 10,
        "auto_save": True,
        "auto_save_interval": 300,  # seconds
        "theme": "light",
        "language": "en",
    }

    # Validation rules for specific keys
    VALIDATION_RULES: Dict[str, Dict[str, Any]] = {
        "window_width": {"type": int, "min": 800, "max": 7680},
        "window_height": {"type": int, "min": 600, "max": 4320},
        "window_x": {"type": int, "min": 0},
        "window_y": {"type": int, "min": 0},
        "max_recent_projects": {"type": int, "min": 1, "max": 50},
        "auto_save_interval": {"type": int, "min": 60, "max": 3600},
    }

    def __init__(self, config_file: Optional[Path] = None) -> None:
        """
        Initialize ConfigManager.

        Args:
            config_file: Optional path to config file, defaults to ~/.ala-gui/config.json
        """
        if config_file is None:
            config_dir = Path.home() / ".ala-gui"
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / "config.json"

        self._config_file = config_file
        self._config: Dict[str, Any] = {}

        # Load configuration (defaults + saved)
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from file, merging with defaults."""
        # Start with defaults
        self._config = self.DEFAULTS.copy()

        # Load from file if exists
        if self._config_file.exists():
            try:
                with open(self._config_file, "r", encoding="utf-8") as f:
                    saved_config = json.load(f)
                    # Merge saved config with defaults
                    self._config.update(saved_config)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted, use defaults
                pass

    def _save_config(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self._config_file, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise ConfigError(f"Failed to save configuration: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any, validate: bool = False) -> None:
        """
        Set configuration value.

        Args:
            key: Configuration key
            value: Configuration value
            validate: Whether to validate the value

        Raises:
            ConfigError: If validation fails
        """
        if validate and key in self.VALIDATION_RULES:
            self._validate_value(key, value)

        self._config[key] = value
        self._save_config()

    def _validate_value(self, key: str, value: Any) -> None:
        """
        Validate configuration value against rules.

        Args:
            key: Configuration key
            value: Value to validate

        Raises:
            ConfigError: If validation fails
        """
        rules = self.VALIDATION_RULES[key]

        # Type validation
        expected_type = rules["type"]
        if not isinstance(value, expected_type):
            raise ConfigError(
                f"Invalid type for '{key}': expected {expected_type.__name__}, got {type(value).__name__}",
                details={"key": key, "value": value},
            )

        # Range validation for integers
        if expected_type == int:
            if "min" in rules and value < rules["min"]:
                raise ConfigError(
                    f"Value for '{key}' must be >= {rules['min']}, got {value}",
                    details={"key": key, "value": value, "min": rules["min"]},
                )
            if "max" in rules and value > rules["max"]:
                raise ConfigError(
                    f"Value for '{key}' must be <= {rules['max']}, got {value}",
                    details={"key": key, "value": value, "max": rules["max"]},
                )

    def get_int(self, key: str, default: Optional[int] = None) -> int:
        """
        Get integer configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Integer value

        Raises:
            ConfigError: If value is not an integer
        """
        value = self.get(key, default)
        if value is None:
            raise ConfigError(
                f"Configuration key '{key}' not found", details={"key": key}
            )
        if not isinstance(value, int):
            raise ConfigError(
                f"Configuration '{key}' is not an integer: {value}",
                details={"key": key, "value": value},
            )
        return value

    def get_str(self, key: str, default: Optional[str] = None) -> str:
        """
        Get string configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            String value

        Raises:
            ConfigError: If value is not a string
        """
        value = self.get(key, default)
        if value is None:
            raise ConfigError(
                f"Configuration key '{key}' not found", details={"key": key}
            )
        if not isinstance(value, str):
            raise ConfigError(
                f"Configuration '{key}' is not a string: {value}",
                details={"key": key, "value": value},
            )
        return value

    def get_bool(self, key: str, default: Optional[bool] = None) -> bool:
        """
        Get boolean configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Boolean value

        Raises:
            ConfigError: If value is not a boolean
        """
        value = self.get(key, default)
        if value is None:
            raise ConfigError(
                f"Configuration key '{key}' not found", details={"key": key}
            )
        if not isinstance(value, bool):
            raise ConfigError(
                f"Configuration '{key}' is not a boolean: {value}",
                details={"key": key, "value": value},
            )
        return value

    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self._config = self.DEFAULTS.copy()
        self._save_config()
