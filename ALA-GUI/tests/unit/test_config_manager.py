"""
Unit tests for ConfigManager.

Following TDD RED-GREEN-REFACTOR cycle.
"""

import pytest

from utils.config_manager import ConfigManager
from utils.exceptions import ConfigError


class TestConfigManagerInitialization:
    """Test suite for ConfigManager initialization."""

    def test_config_manager_initialization(self):
        """Test ConfigManager creates without errors."""
        # Arrange & Act
        config = ConfigManager()

        # Assert
        assert config is not None

    def test_config_manager_has_default_values(self):
        """Test ConfigManager loads default configuration."""
        # Arrange & Act
        config = ConfigManager()

        # Assert
        assert config.get("app_name") == "ALA-GUI"
        assert config.get("version") is not None


class TestConfigManagerGetSet:
    """Test suite for get/set operations."""

    def test_get_existing_key(self):
        """Test getting existing configuration value."""
        # Arrange
        config = ConfigManager()

        # Act
        value = config.get("app_name")

        # Assert
        assert value == "ALA-GUI"

    def test_get_nonexistent_key_returns_default(self):
        """Test getting non-existent key returns default."""
        # Arrange
        config = ConfigManager()

        # Act
        value = config.get("nonexistent_key", default="default_value")

        # Assert
        assert value == "default_value"

    def test_get_nonexistent_key_without_default_returns_none(self):
        """Test getting non-existent key without default returns None."""
        # Arrange
        config = ConfigManager()

        # Act
        value = config.get("nonexistent_key")

        # Assert
        assert value is None

    def test_set_new_value(self):
        """Test setting new configuration value."""
        # Arrange
        config = ConfigManager()

        # Act
        config.set("test_key", "test_value")
        value = config.get("test_key")

        # Assert
        assert value == "test_value"

    def test_set_updates_existing_value(self):
        """Test setting updates existing value."""
        # Arrange
        config = ConfigManager()
        config.set("test_key", "original")

        # Act
        config.set("test_key", "updated")
        value = config.get("test_key")

        # Assert
        assert value == "updated"


class TestConfigManagerDefaultValues:
    """Test suite for default configuration."""

    def test_default_config_keys_exist(self):
        """Test all expected default keys exist."""
        # Arrange
        config = ConfigManager()

        # Act & Assert
        assert config.get("app_name") is not None
        assert config.get("version") is not None
        assert config.get("window_width") is not None
        assert config.get("window_height") is not None

    def test_default_config_types(self):
        """Test default config values have correct types."""
        # Arrange
        config = ConfigManager()

        # Act & Assert
        assert isinstance(config.get("app_name"), str)
        assert isinstance(config.get("version"), str)
        assert isinstance(config.get("window_width"), int)
        assert isinstance(config.get("window_height"), int)


class TestConfigManagerValidation:
    """Test suite for configuration validation."""

    def test_validate_integer_value(self):
        """Test validating integer configuration."""
        # Arrange
        config = ConfigManager()

        # Act & Assert - should not raise
        config.set("window_width", 1920)

    def test_validate_integer_rejects_string(self):
        """Test integer validation rejects string."""
        # Arrange
        config = ConfigManager()

        # Act & Assert
        with pytest.raises(ConfigError, match="Invalid type"):
            config.set("window_width", "not_an_int", validate=True)

    def test_validate_positive_integer(self):
        """Test validating integer minimum value."""
        # Arrange
        config = ConfigManager()

        # Act & Assert
        with pytest.raises(ConfigError, match="must be >= 800"):
            config.set("window_width", -100, validate=True)

    def test_skip_validation_when_disabled(self):
        """Test validation can be skipped."""
        # Arrange
        config = ConfigManager()

        # Act & Assert - should not raise
        config.set("window_width", "invalid", validate=False)


class TestConfigManagerPersistence:
    """Test suite for configuration persistence."""

    def test_config_persists_between_instances(self):
        """Test configuration persists to storage."""
        # Arrange
        config1 = ConfigManager()
        config1.set("test_persist", "persisted_value")

        # Act
        config2 = ConfigManager()
        value = config2.get("test_persist")

        # Assert
        assert value == "persisted_value"

    def test_reset_to_defaults(self):
        """Test resetting configuration to defaults."""
        # Arrange
        config = ConfigManager()
        config.set("test_key", "test_value")

        # Act
        config.reset_to_defaults()
        value = config.get("test_key")

        # Assert
        assert value is None
        assert config.get("app_name") == "ALA-GUI"


class TestConfigManagerTypeSafety:
    """Test suite for type-safe configuration access."""

    def test_get_int(self):
        """Test type-safe integer getter."""
        # Arrange
        config = ConfigManager()

        # Act
        value = config.get_int("window_width")

        # Assert
        assert isinstance(value, int)
        assert value > 0

    def test_get_int_with_invalid_value_raises_error(self):
        """Test get_int raises error for non-integer value."""
        # Arrange
        config = ConfigManager()
        config.set("test_key", "not_an_int", validate=False)

        # Act & Assert
        with pytest.raises(ConfigError, match="not an integer"):
            config.get_int("test_key")

    def test_get_str(self):
        """Test type-safe string getter."""
        # Arrange
        config = ConfigManager()

        # Act
        value = config.get_str("app_name")

        # Assert
        assert isinstance(value, str)
        assert len(value) > 0

    def test_get_bool(self):
        """Test type-safe boolean getter."""
        # Arrange
        config = ConfigManager()
        config.set("test_bool", True)

        # Act
        value = config.get_bool("test_bool")

        # Assert
        assert isinstance(value, bool)
        assert value is True
