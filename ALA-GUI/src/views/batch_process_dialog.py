"""
Batch Processing Dialog.

M3: UI Integration - Dialog for batch processing multiple images with AI models.
"""

from pathlib import Path
from typing import Optional

import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from models.model_controller import ModelController


class BatchProcessWorker(QThread):
    """
    Worker thread for batch processing images.

    Signals:
        progress: Emitted with (current, total, message) during processing
        file_complete: Emitted when file processed (file_path, success, message)
        batch_complete: Emitted when batch processing finishes
    """

    progress = pyqtSignal(int, int, str)
    file_complete = pyqtSignal(str, bool, str)
    batch_complete = pyqtSignal()

    def __init__(
        self,
        model_controller: ModelController,
        image_paths: list[str],
        text_prompt: str,
        parent: Optional[QThread] = None,
    ) -> None:
        """
        Initialize batch processing worker.

        Args:
            model_controller: Model controller for running inference
            image_paths: List of image file paths to process
            text_prompt: Text prompt for object detection
            parent: Parent QThread (optional)
        """
        super().__init__(parent)
        self.model_controller = model_controller
        self.image_paths = image_paths
        self.text_prompt = text_prompt
        self._is_cancelled = False

    def run(self) -> None:
        """Run batch processing on all images."""
        total = len(self.image_paths)

        for i, image_path in enumerate(self.image_paths):
            if self._is_cancelled:
                break

            # Emit progress
            self.progress.emit(i + 1, total, f"Processing {Path(image_path).name}...")

            try:
                # Load image
                from PIL import Image

                pil_image = Image.open(image_path)
                image = np.array(pil_image)

                # Run autodistill
                self.model_controller.run_autodistill(image, self.text_prompt)

                # Success
                self.file_complete.emit(
                    image_path, True, f"✅ Processed {Path(image_path).name}"
                )

            except Exception as e:
                # Error
                self.file_complete.emit(
                    image_path, False, f"❌ Failed {Path(image_path).name}: {str(e)}"
                )

        self.batch_complete.emit()

    def cancel(self) -> None:
        """Cancel batch processing."""
        self._is_cancelled = True


class BatchProcessDialog(QDialog):
    """
    Batch processing dialog for multiple images.

    Features:
        - Process multiple images with AI models
        - Progress tracking with file-level detail
        - Cancel support
        - Log output for each processed file
        - Success/failure statistics

    Usage:
        dialog = BatchProcessDialog()
        dialog.model_controller.load_models(florence_path, sam_path)
        dialog.set_image_paths(["/path/to/image1.jpg", "/path/to/image2.jpg"])
        dialog.set_text_prompt("person, car, dog")
        dialog.exec()
    """

    def __init__(self, parent: Optional[QDialog] = None) -> None:
        """
        Initialize BatchProcessDialog.

        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)

        self.setWindowTitle("Batch Process Images")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)

        # Initialize model controller
        self.model_controller = ModelController(parent=self)

        # State
        self._image_paths: list[str] = []
        self._text_prompt: str = ""
        self._worker: Optional[BatchProcessWorker] = None
        self._processed_count = 0
        self._success_count = 0
        self._error_count = 0

        # Create UI
        self._create_ui()

    def _create_ui(self) -> None:
        """Create dialog UI components."""
        layout = QVBoxLayout()

        # File info group
        file_group = QGroupBox("Files")
        file_layout = QVBoxLayout()

        self.file_count_label = QLabel("No files selected")
        self.file_count_label.setStyleSheet("font-weight: bold;")
        file_layout.addWidget(self.file_count_label)

        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        # Progress group
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout()

        # Overall progress
        overall_layout = QHBoxLayout()
        overall_layout.addWidget(QLabel("Overall:"))
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        overall_layout.addWidget(self.progress_bar)
        progress_layout.addLayout(overall_layout)

        # Current file
        self.current_file_label = QLabel("")
        progress_layout.addWidget(self.current_file_label)

        # Statistics
        stats_layout = QHBoxLayout()
        self.stats_label = QLabel("Processed: 0 | Success: 0 | Errors: 0")
        stats_layout.addWidget(self.stats_label)
        progress_layout.addLayout(stats_layout)

        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        # Log group
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout()

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        log_layout.addWidget(self.log_text)

        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        # Buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Batch Processing")
        self.start_button.clicked.connect(self.start_processing)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_processing)
        self.cancel_button.setEnabled(False)
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def set_image_paths(self, paths: list[str]) -> None:
        """
        Set image paths for batch processing.

        Args:
            paths: List of image file paths
        """
        self._image_paths = paths
        self.file_count_label.setText(f"{len(paths)} files ready for processing")

    def set_text_prompt(self, prompt: str) -> None:
        """
        Set text prompt for object detection.

        Args:
            prompt: Text prompt (comma-separated object classes)
        """
        self._text_prompt = prompt

    def start_processing(self) -> None:
        """Start batch processing."""
        if not self._image_paths:
            self.log_text.append("❌ No images selected")
            return

        if not self._text_prompt:
            self.log_text.append("❌ No text prompt provided")
            return

        # Reset statistics
        self._processed_count = 0
        self._success_count = 0
        self._error_count = 0
        self.log_text.clear()

        # Update UI
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.close_button.setEnabled(False)

        # Log start
        self.log_text.append(
            f"🚀 Starting batch processing of {len(self._image_paths)} images..."
        )
        self.log_text.append(f"📝 Text prompt: {self._text_prompt}")
        self.log_text.append("")

        # Create and start worker
        self._worker = BatchProcessWorker(
            self.model_controller, self._image_paths, self._text_prompt, self
        )
        self._worker.progress.connect(self._on_progress)
        self._worker.file_complete.connect(self._on_file_complete)
        self._worker.batch_complete.connect(self._on_batch_complete)
        self._worker.start()

    def cancel_processing(self) -> None:
        """Cancel batch processing."""
        if self._worker:
            self._worker.cancel()
            self.log_text.append("")
            self.log_text.append("⚠️ Cancelling batch processing...")

    def _on_progress(self, current: int, total: int, message: str) -> None:
        """
        Handle progress update.

        Args:
            current: Current file number
            total: Total number of files
            message: Progress message
        """
        progress_percent = int((current / total) * 100)
        self.progress_bar.setValue(progress_percent)
        self.current_file_label.setText(message)

    def _on_file_complete(self, file_path: str, success: bool, message: str) -> None:
        """
        Handle file completion.

        Args:
            file_path: Path to processed file
            success: Whether processing succeeded
            message: Result message
        """
        self._processed_count += 1

        if success:
            self._success_count += 1
        else:
            self._error_count += 1

        # Update statistics
        self.stats_label.setText(
            f"Processed: {self._processed_count} | "
            f"Success: {self._success_count} | "
            f"Errors: {self._error_count}"
        )

        # Log result
        self.log_text.append(message)

    def _on_batch_complete(self) -> None:
        """Handle batch completion."""
        self.log_text.append("")
        self.log_text.append("✅ Batch processing complete!")
        self.log_text.append(
            f"📊 Total: {self._processed_count} | "
            f"Success: {self._success_count} | "
            f"Errors: {self._error_count}"
        )

        # Update UI
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.close_button.setEnabled(True)
        self.current_file_label.setText("Batch processing finished")
        self.progress_bar.setValue(100)
