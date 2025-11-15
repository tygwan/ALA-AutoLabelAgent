"""
Results Preview Widget.

M3: UI Integration - Widget for previewing annotation results before accepting.
"""

from typing import Optional

from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class ResultsPreviewWidget(QWidget):
    """
    Widget for previewing annotation results.

    Features:
        - Display detection count and summary statistics
        - Show bounding box coordinates for each detection
        - Display confidence scores and labels
        - Scrollable list for many detections
        - Clear visual separation of each detection

    Usage:
        widget = ResultsPreviewWidget()
        widget.display_results(results_dict)
        widget.clear()
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialize ResultsPreviewWidget.

        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        self._create_ui()

    def _create_ui(self) -> None:
        """Create widget UI components."""
        layout = QVBoxLayout()

        # Summary group
        self.summary_group = QGroupBox("Detection Summary")
        summary_layout = QVBoxLayout()

        self.count_label = QLabel("No results")
        self.count_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        summary_layout.addWidget(self.count_label)

        self.summary_group.setLayout(summary_layout)
        layout.addWidget(self.summary_group)

        # Details group with scroll area
        self.details_group = QGroupBox("Detection Details")
        details_layout = QVBoxLayout()

        # Scroll area for detections
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(300)

        self.details_widget = QWidget()
        self.details_layout = QVBoxLayout()
        self.details_widget.setLayout(self.details_layout)
        scroll.setWidget(self.details_widget)

        details_layout.addWidget(scroll)
        self.details_group.setLayout(details_layout)
        layout.addWidget(self.details_group)

        self.setLayout(layout)

    def display_results(self, results: dict) -> None:
        """
        Display annotation results.

        Args:
            results: Results dictionary with format:
                {
                    'boxes': [(x1, y1, x2, y2), ...],
                    'labels': ['class1', 'class2', ...],
                    'scores': [0.95, 0.87, ...],
                    'metadata': {'num_detections': N, ...}
                }
        """
        # Clear previous results
        self.clear()

        # Update summary
        num_detections = results.get("metadata", {}).get("num_detections", 0)
        self.count_label.setText(f"Total Detections: {num_detections}")

        # Display each detection
        boxes = results.get("boxes", [])
        labels = results.get("labels", [])
        scores = results.get("scores", [])

        for i, (box, label) in enumerate(zip(boxes, labels)):
            detection_widget = self._create_detection_widget(
                i + 1, box, label, scores[i] if i < len(scores) else None
            )
            self.details_layout.addWidget(detection_widget)

        # Add stretch at the end
        self.details_layout.addStretch()

    def _create_detection_widget(
        self,
        index: int,
        box: tuple[int, int, int, int],
        label: str,
        score: Optional[float] = None,
    ) -> QWidget:
        """
        Create widget for single detection.

        Args:
            index: Detection number (1-based)
            box: Bounding box (x1, y1, x2, y2)
            label: Class label
            score: Confidence score (optional)

        Returns:
            Widget displaying detection info
        """
        widget = QWidget()
        widget.setStyleSheet(
            "background-color: #f5f5f5; border: 1px solid #ddd; "
            "border-radius: 4px; padding: 8px; margin: 4px;"
        )

        layout = QVBoxLayout()
        layout.setSpacing(4)

        # Header with index and label
        header_layout = QHBoxLayout()
        index_label = QLabel(f"#{index}")
        index_label.setStyleSheet("font-weight: bold; color: #2196F3;")

        label_text = QLabel(f"Label: {label}")
        label_text.setStyleSheet("font-weight: bold;")

        header_layout.addWidget(index_label)
        header_layout.addWidget(label_text)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Bounding box coordinates
        x1, y1, x2, y2 = box
        width = x2 - x1
        height = y2 - y1

        bbox_label = QLabel(
            f"Box: ({x1}, {y1}) → ({x2}, {y2}) | Size: {width}×{height}px"
        )
        bbox_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(bbox_label)

        # Confidence score if available
        if score is not None:
            score_label = QLabel(f"Confidence: {score:.2%}")
            score_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
            layout.addWidget(score_label)

        widget.setLayout(layout)
        return widget

    def clear(self) -> None:
        """Clear all preview content."""
        # Clear details layout
        while self.details_layout.count():
            item = self.details_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Reset summary
        self.count_label.setText("No results")
