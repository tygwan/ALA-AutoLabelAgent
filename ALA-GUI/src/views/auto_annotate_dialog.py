"""
Auto-Annotate Dialog.

M3: UI Integration - Dialog for auto-annotation with Florence-2 + SAM2.
"""

from typing import Optional

import numpy as np
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
)

from models.model_controller import ModelController
from widgets.results_preview_widget import ResultsPreviewWidget


class AutoAnnotateDialog(QDialog):
    """
    Auto-annotation dialog with text prompt input and progress tracking.

    Features:
        - Text prompt input for object classes
        - Progress bar for visual feedback
        - Model controller integration
        - Cancel support
        - Result signals

    Usage:
        dialog = AutoAnnotateDialog()
        dialog.model_controller.load_models(florence_path, sam_path)
        dialog.set_text_prompt("person, car, dog")

        # Connect signal
        dialog.annotation_complete.connect(handle_results)

        # Run
        dialog.run_annotation()
    """

    # Signals
    annotation_complete = pyqtSignal(object)  # results dictionary
    annotation_accepted = pyqtSignal(object)  # results accepted by user
    annotation_rejected = pyqtSignal()  # results rejected by user

    def __init__(self, parent: Optional[QDialog] = None) -> None:
        """
        Initialize AutoAnnotateDialog.

        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)

        self.setWindowTitle("Auto-Annotate with AI Models")
        self.setMinimumWidth(500)

        # Initialize model controller
        self.model_controller = ModelController(parent=self)

        # Connect model signals
        self.model_controller.progress.connect(self.update_progress)
        self.model_controller.autodistill_complete.connect(self._on_annotation_complete)
        self.model_controller.error.connect(self._on_error)

        # Create UI
        self._create_ui()

        # State
        self._current_image: Optional[np.ndarray] = None
        self._current_results: Optional[dict] = None

    def _create_ui(self) -> None:
        """Create dialog UI components."""
        layout = QVBoxLayout()

        # Model selection dropdown
        model_layout = QHBoxLayout()
        model_label = QLabel("Model:")
        self.model_selector = QComboBox()
        self.model_selector.addItems(
            [
                "Florence-2 + SAM2 (Best Quality)",
                "Florence-2 Only (Fast)",
                "SAM2 Only (Manual Prompts)",
            ]
        )
        self.model_selector.setCurrentIndex(0)
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_selector)
        layout.addLayout(model_layout)

        # Text prompt input
        prompt_layout = QHBoxLayout()
        prompt_label = QLabel("Object Classes:")
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText(
            "Enter comma-separated classes (e.g., person, car, dog)"
        )
        prompt_layout.addWidget(prompt_label)
        prompt_layout.addWidget(self.prompt_input)
        layout.addLayout(prompt_layout)

        # Progress bar
        progress_layout = QVBoxLayout()
        progress_label = QLabel("Progress:")
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_label = QLabel("")
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        layout.addLayout(progress_layout)

        # Results preview (initially hidden)
        self.results_preview = ResultsPreviewWidget()
        self.results_preview.hide()
        layout.addWidget(self.results_preview)

        # Buttons
        button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run Auto-Annotation")
        self.run_button.clicked.connect(self.run_annotation)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_annotation)
        self.cancel_button.setEnabled(False)
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        # Accept/Reject buttons (initially hidden)
        accept_reject_layout = QHBoxLayout()
        self.accept_button = QPushButton("✓ Accept Results")
        self.accept_button.clicked.connect(self.accept_results)
        self.accept_button.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold;"
        )
        self.reject_button = QPushButton("✗ Reject & Retry")
        self.reject_button.clicked.connect(self.reject_results)
        self.reject_button.setStyleSheet(
            "background-color: #f44336; color: white; font-weight: bold;"
        )
        accept_reject_layout.addWidget(self.accept_button)
        accept_reject_layout.addWidget(self.reject_button)
        layout.addLayout(accept_reject_layout)

        # Hide accept/reject initially
        self.accept_button.hide()
        self.reject_button.hide()

        self.setLayout(layout)

    def get_text_prompt(self) -> str:
        """
        Get current text prompt.

        Returns:
            Text prompt string
        """
        return self.prompt_input.text()

    def set_text_prompt(self, prompt: str) -> None:
        """
        Set text prompt.

        Args:
            prompt: Text prompt to set
        """
        self.prompt_input.setText(prompt)

    def set_image(self, image: np.ndarray) -> None:
        """
        Set image for annotation.

        Args:
            image: Input image (H, W, 3) in RGB format
        """
        self._current_image = image

    def update_progress(self, percentage: int, message: str) -> None:
        """
        Update progress bar and message.

        Args:
            percentage: Progress percentage (0-100)
            message: Progress message
        """
        self.progress_bar.setValue(percentage)
        self.progress_label.setText(message)

    def run_annotation(self) -> None:
        """
        Run auto-annotation on current image.

        Raises:
            RuntimeError: If no image is set or models not loaded
        """
        if self._current_image is None:
            self._on_error("No image set. Call set_image() first.")
            return

        text_prompt = self.get_text_prompt()
        if not text_prompt:
            self._on_error("Please enter object classes to detect.")
            return

        # Disable run button, enable cancel
        self.run_button.setEnabled(False)
        self.cancel_button.setEnabled(True)

        # Reset progress
        self.progress_bar.setValue(0)
        self.progress_label.setText("Starting...")

        # Run autodistill
        try:
            self.model_controller.run_autodistill(
                self._current_image,
                text_prompt,
            )
        except Exception as e:
            self._on_error(str(e))
            self._reset_buttons()

    def cancel_annotation(self) -> None:
        """Cancel ongoing annotation."""
        self.model_controller.cancel_inference()
        self.progress_label.setText("Cancelled")
        self._reset_buttons()

    def _on_annotation_complete(self, results: dict) -> None:
        """
        Handle annotation completion.

        Args:
            results: Annotation results from model controller
        """
        # Store results for accept/reject
        self._current_results = results

        num_detections = results["metadata"]["num_detections"]
        self.progress_label.setText(
            f"Complete! Found {num_detections} objects - Review and Accept/Reject"
        )
        self._reset_buttons()

        # Show results preview
        self.results_preview.display_results(results)
        self.results_preview.show()

        # Show accept/reject buttons
        self.accept_button.show()
        self.reject_button.show()

        # Emit signal
        self.annotation_complete.emit(results)

    def _on_error(self, error_msg: str) -> None:
        """
        Handle error.

        Args:
            error_msg: Error message
        """
        self.progress_label.setText(f"Error: {error_msg}")
        self._reset_buttons()

    def accept_results(self) -> None:
        """Accept annotation results and close dialog."""
        if self._current_results is None:
            return

        num_detections = self._current_results["metadata"]["num_detections"]
        self.progress_label.setText(f"✅ Accepted {num_detections} detections")

        # Hide accept/reject buttons
        self.accept_button.hide()
        self.reject_button.hide()

        # Emit accepted signal
        self.annotation_accepted.emit(self._current_results)

        # Close dialog
        self.accept()

    def reject_results(self) -> None:
        """Reject annotation results and allow retry."""
        self.progress_label.setText("❌ Results rejected - Ready to retry")

        # Hide accept/reject buttons
        self.accept_button.hide()
        self.reject_button.hide()

        # Hide and clear results preview
        self.results_preview.clear()
        self.results_preview.hide()

        # Clear current results
        self._current_results = None

        # Emit rejected signal
        self.annotation_rejected.emit()

        # Reset UI for retry
        self.run_button.setEnabled(True)
        self.progress_bar.setValue(0)

    def _reset_buttons(self) -> None:
        """Reset button states."""
        self.run_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
