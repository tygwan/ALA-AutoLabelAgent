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
from models.model_manager import ModelManager
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
        self.setMinimumWidth(600)

        # Initialize model manager
        self.model_manager = ModelManager()

        # Create UI first (so progress bar exists)
        self._create_ui()

        # Initialize model controller (without auto-loading)
        self.model_controller = ModelController(parent=self, auto_load=False)

        # Connect model signals
        self.model_controller.progress.connect(self.update_progress)
        self.model_controller.autodistill_complete.connect(self._on_annotation_complete)
        self.model_controller.error.connect(self._on_error)

        # State
        self._current_image: Optional[np.ndarray] = None
        self._current_results: Optional[dict] = None
        self._models_loaded = False

        # Populate model lists
        self._populate_model_lists()

    def _create_ui(self) -> None:
        """Create dialog UI components."""
        layout = QVBoxLayout()

        # VLM Model selection
        vlm_layout = QHBoxLayout()
        vlm_label = QLabel("VLM Model:")
        self.vlm_selector = QComboBox()
        self.vlm_selector.setToolTip(
            "Visual Language Model for object detection (e.g., Florence-2)"
        )
        vlm_layout.addWidget(vlm_label)
        vlm_layout.addWidget(self.vlm_selector, 1)
        layout.addLayout(vlm_layout)

        # Segmentation Model selection
        seg_layout = QHBoxLayout()
        seg_label = QLabel("Seg Model:")
        self.seg_selector = QComboBox()
        self.seg_selector.setToolTip(
            "Segmentation Model for refining masks (e.g., SAM2)"
        )
        seg_layout.addWidget(seg_label)
        seg_layout.addWidget(self.seg_selector, 1)
        layout.addLayout(seg_layout)

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

        # Get selected models
        vlm_path = self.vlm_selector.currentData()
        seg_path = self.seg_selector.currentData()

        if vlm_path is None:
            self._on_error("Please select a valid VLM model.")
            return

        # Disable run button, enable cancel
        self.run_button.setEnabled(False)
        self.cancel_button.setEnabled(True)

        # Reset progress
        self.progress_bar.setValue(0)
        self.progress_label.setText("Loading models...")

        # Load models if not already loaded
        if not self._models_loaded:
            try:
                # Auto-detect device
                import torch

                device = (
                    "cuda"
                    if torch.cuda.is_available()
                    else "mps" if torch.backends.mps.is_available() else "cpu"
                )

                # Load models
                self.model_controller.load_models(
                    florence_path=vlm_path,
                    sam_path=seg_path if seg_path else "",
                    device=device,
                )
                self._models_loaded = True
            except Exception as e:
                self._on_error(f"Failed to load models: {str(e)}")
                self._reset_buttons()
                return

        # Run autodistill
        self.progress_label.setText("Running inference...")
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
        from PyQt6.QtWidgets import QMessageBox

        self.progress_label.setText(f"Error: {error_msg}")
        self._reset_buttons()

        # Show error dialog for model loading errors
        if "Failed to load models" in error_msg:
            QMessageBox.critical(
                self,
                "Model Loading Failed",
                f"Failed to load AI models:\n\n{error_msg}\n\n"
                "This may be due to:\n"
                "- Invalid model path\n"
                "- Network connection issues (for HuggingFace models)\n"
                "- Insufficient disk space (~2-5GB required)\n"
                "- Missing dependencies (PyTorch, transformers)\n\n"
                "Please check your model directory and setup.",
            )

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

    def _populate_model_lists(self) -> None:
        """Populate VLM and Segmentation model dropdown lists."""
        # Clear existing items
        self.vlm_selector.clear()
        self.seg_selector.clear()

        # Get available models
        vlm_models = self.model_manager.get_vlm_models()
        seg_models = self.model_manager.get_segmentation_models()

        # Populate VLM models
        if vlm_models:
            for model in vlm_models:
                size_info = f" (~{model.size_mb:.0f}MB)" if model.size_mb else ""
                self.vlm_selector.addItem(f"{model.name}{size_info}", model.path)
        else:
            self.vlm_selector.addItem("No VLM models found", None)
            self.progress_label.setText(
                f"⚠️ No models found in {self.model_manager.get_model_directory()}"
            )

        # Populate Segmentation models
        if seg_models:
            for model in seg_models:
                size_info = f" (~{model.size_mb:.0f}MB)" if model.size_mb else ""
                self.seg_selector.addItem(f"{model.name}{size_info}", model.path)
            # Add "None" option for Florence-2 only mode
            self.seg_selector.addItem("None (VLM only)", None)
        else:
            self.seg_selector.addItem("No segmentation models found", None)

        # Show model directory path
        model_dir = self.model_manager.get_model_directory()
        self.progress_label.setText(f"Models directory: {model_dir}\nReady to annotate")
