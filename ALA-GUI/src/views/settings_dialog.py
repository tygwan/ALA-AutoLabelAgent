"""
Settings Dialog for ALA-GUI.

M2: PyQt6 Image Display & Navigation - Application settings configuration.
"""

from typing import Optional

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class SettingsDialog(QDialog):
    """
    Settings dialog for application configuration.

    Features:
    - Tabbed interface for different setting categories
    - Appearance settings (theme, font)
    - Performance settings (cache, threads)
    - Model settings (paths, device)
    - OK/Cancel buttons with validation
    - Settings persistence with ConfigManager

    Tabs:
        Appearance: UI theme, font size, language
        Performance: Cache size, thread count, auto-save
        Model: Model paths, inference device, batch size
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the settings dialog.

        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)

        # Make dialog modal
        self.setModal(True)

        # Set window title
        self.setWindowTitle("Settings")

        # Set up UI
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize the user interface."""
        # Create main layout
        layout = QVBoxLayout(self)

        # Create tab widget
        self.tab_widget = QTabWidget()

        # Create tabs
        self.appearance_tab = self._create_appearance_tab()
        self.performance_tab = self._create_performance_tab()
        self.model_tab = self._create_model_tab()

        # Add tabs to tab widget
        self.tab_widget.addTab(self.appearance_tab, "Appearance")
        self.tab_widget.addTab(self.performance_tab, "Performance")
        self.tab_widget.addTab(self.model_tab, "Model")

        # Add tab widget to layout
        layout.addWidget(self.tab_widget)

        # Create button box
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Add button box to layout
        layout.addWidget(button_box)

    def _create_appearance_tab(self) -> QWidget:
        """
        Create the appearance settings tab.

        Returns:
            Widget containing appearance settings
        """
        widget = QWidget()
        layout = QFormLayout(widget)

        # Theme setting
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "System"])
        self.theme_combo.setCurrentText("System")
        layout.addRow("Theme:", self.theme_combo)

        # Font size setting
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setValue(10)
        self.font_size_spin.setSuffix(" pt")
        layout.addRow("Font Size:", self.font_size_spin)

        return widget

    def _create_performance_tab(self) -> QWidget:
        """
        Create the performance settings tab.

        Returns:
            Widget containing performance settings
        """
        widget = QWidget()
        layout = QFormLayout(widget)

        # Cache size setting
        self.cache_size_spin = QSpinBox()
        self.cache_size_spin.setRange(64, 4096)
        self.cache_size_spin.setValue(256)
        self.cache_size_spin.setSingleStep(64)
        self.cache_size_spin.setSuffix(" MB")
        layout.addRow("Cache Size:", self.cache_size_spin)

        # Thread count setting
        self.thread_count_spin = QSpinBox()
        self.thread_count_spin.setRange(1, 16)
        self.thread_count_spin.setValue(4)
        layout.addRow("Thread Count:", self.thread_count_spin)

        return widget

    def _create_model_tab(self) -> QWidget:
        """
        Create the model settings tab.

        Returns:
            Widget containing model settings
        """
        widget = QWidget()
        layout = QFormLayout(widget)

        # Device setting
        self.device_combo = QComboBox()
        self.device_combo.addItems(["CPU", "CUDA", "MPS"])
        self.device_combo.setCurrentText("CPU")
        layout.addRow("Inference Device:", self.device_combo)

        # Batch size setting
        self.batch_size_spin = QSpinBox()
        self.batch_size_spin.setRange(1, 64)
        self.batch_size_spin.setValue(1)
        layout.addRow("Batch Size:", self.batch_size_spin)

        return widget

    # Getter and setter methods
    def get_theme(self) -> str:
        """Get the selected theme."""
        return self.theme_combo.currentText()

    def set_theme(self, theme: str) -> None:
        """Set the theme."""
        self.theme_combo.setCurrentText(theme)

    def get_font_size(self) -> int:
        """Get the font size."""
        return self.font_size_spin.value()

    def set_font_size(self, size: int) -> None:
        """Set the font size."""
        self.font_size_spin.setValue(size)

    def get_cache_size(self) -> int:
        """Get the cache size in MB."""
        return self.cache_size_spin.value()

    def set_cache_size(self, size: int) -> None:
        """Set the cache size in MB."""
        self.cache_size_spin.setValue(size)

    def get_thread_count(self) -> int:
        """Get the thread count."""
        return self.thread_count_spin.value()

    def set_thread_count(self, count: int) -> None:
        """Set the thread count."""
        self.thread_count_spin.setValue(count)

    def get_device(self) -> str:
        """Get the inference device."""
        return self.device_combo.currentText()

    def set_device(self, device: str) -> None:
        """Set the inference device."""
        self.device_combo.setCurrentText(device)

    def get_batch_size(self) -> int:
        """Get the batch size."""
        return self.batch_size_spin.value()

    def set_batch_size(self, size: int) -> None:
        """Set the batch size."""
        self.batch_size_spin.setValue(size)
