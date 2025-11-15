"""
Export Dialog.

M3: UI Integration - Dialog for exporting annotations to COCO/YOLO formats.
"""

from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from utils.annotation_exporter import AnnotationExporter


class ExportDialog(QDialog):
    """
    Dialog for exporting annotations.

    Features:
        - Select export format (COCO, YOLO)
        - Choose output path with file browser
        - Dataset name input for COCO format
        - Export validation and error handling

    Usage:
        dialog = ExportDialog()
        dialog.set_results(results_dict)
        dialog.set_image_path("/path/to/image.jpg")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Export completed
    """

    def __init__(self, parent: Optional[QDialog] = None) -> None:
        """
        Initialize ExportDialog.

        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)

        self.setWindowTitle("Export Annotations")
        self.setMinimumWidth(500)

        # State
        self._results: Optional[dict] = None
        self._image_path: Optional[str] = None
        self._exporter = AnnotationExporter()

        # Create UI
        self._create_ui()

    def _create_ui(self) -> None:
        """Create dialog UI components."""
        layout = QVBoxLayout()

        # Format selection
        format_group = QGroupBox("Export Format")
        format_layout = QVBoxLayout()

        format_select_layout = QHBoxLayout()
        format_label = QLabel("Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["COCO JSON", "YOLO TXT"])
        self.format_combo.currentIndexChanged.connect(self._on_format_changed)
        format_select_layout.addWidget(format_label)
        format_select_layout.addWidget(self.format_combo)
        format_layout.addLayout(format_select_layout)

        # Format description
        self.format_description = QLabel(
            "COCO JSON: Single JSON file with all annotations in MS COCO format"
        )
        self.format_description.setWordWrap(True)
        self.format_description.setStyleSheet("color: #666; font-size: 11px;")
        format_layout.addWidget(self.format_description)

        format_group.setLayout(format_layout)
        layout.addWidget(format_group)

        # Dataset name (COCO only)
        self.dataset_group = QGroupBox("Dataset Information")
        dataset_layout = QHBoxLayout()

        dataset_label = QLabel("Dataset Name:")
        self.dataset_name_input = QLineEdit()
        self.dataset_name_input.setText("ALA Dataset")
        dataset_layout.addWidget(dataset_label)
        dataset_layout.addWidget(self.dataset_name_input)

        self.dataset_group.setLayout(dataset_layout)
        layout.addWidget(self.dataset_group)

        # Output path selection
        output_group = QGroupBox("Output Location")
        output_layout = QVBoxLayout()

        path_layout = QHBoxLayout()
        path_label = QLabel("Output:")
        self.output_path_input = QLineEdit()
        self.output_path_input.setPlaceholderText("Select output location...")
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self._browse_output)

        path_layout.addWidget(path_label)
        path_layout.addWidget(self.output_path_input)
        path_layout.addWidget(self.browse_button)
        output_layout.addLayout(path_layout)

        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # Buttons
        button_layout = QHBoxLayout()
        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self._export)
        self.export_button.setStyleSheet(
            "background-color: #2196F3; color: white; font-weight: bold;"
        )
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def set_results(self, results: dict) -> None:
        """
        Set annotation results to export.

        Args:
            results: Annotation results dictionary
        """
        self._results = results

    def set_image_path(self, image_path: str) -> None:
        """
        Set source image path.

        Args:
            image_path: Path to source image
        """
        self._image_path = image_path

    def _on_format_changed(self, index: int) -> None:
        """
        Handle format selection change.

        Args:
            index: Selected format index
        """
        if index == 0:  # COCO
            self.format_description.setText(
                "COCO JSON: Single JSON file with all annotations in MS COCO format"
            )
            self.dataset_group.show()
        else:  # YOLO
            self.format_description.setText(
                "YOLO TXT: One .txt file per image with normalized coordinates"
            )
            self.dataset_group.hide()

    def _browse_output(self) -> None:
        """Open file browser to select output location."""
        format_index = self.format_combo.currentIndex()

        if format_index == 0:  # COCO
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save COCO Annotations",
                "annotations.json",
                "JSON Files (*.json);;All Files (*)",
            )
            if file_path:
                self.output_path_input.setText(file_path)
        else:  # YOLO
            dir_path = QFileDialog.getExistingDirectory(
                self,
                "Select YOLO Output Directory",
            )
            if dir_path:
                self.output_path_input.setText(dir_path)

    def _export(self) -> None:
        """Execute export operation."""
        # Validate inputs
        if self._results is None:
            QMessageBox.warning(self, "Export Error", "No annotation results to export")
            return

        if self._image_path is None:
            QMessageBox.warning(self, "Export Error", "No source image specified")
            return

        output_path = self.output_path_input.text()
        if not output_path:
            QMessageBox.warning(self, "Export Error", "Please select output location")
            return

        try:
            format_index = self.format_combo.currentIndex()

            if format_index == 0:  # COCO
                dataset_name = self.dataset_name_input.text()
                self._exporter.export_coco(
                    self._results, self._image_path, output_path, dataset_name
                )
                QMessageBox.information(
                    self,
                    "Export Successful",
                    f"Annotations exported to:\n{output_path}",
                )
            else:  # YOLO
                self._exporter.export_yolo(self._results, self._image_path, output_path)

                # Show exported files
                output_dir = Path(output_path)
                image_name = Path(self._image_path).stem
                txt_file = output_dir / f"{image_name}.txt"

                QMessageBox.information(
                    self,
                    "Export Successful",
                    f"Annotations exported to:\n{txt_file}\n\n"
                    f"Classes saved to:\n{output_dir / 'classes.txt'}",
                )

            # Close dialog on success
            self.accept()

        except Exception as e:
            QMessageBox.critical(
                self, "Export Error", f"Failed to export annotations:\n{str(e)}"
            )
