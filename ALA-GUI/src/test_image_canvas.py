"""
Manual test script for ImageCanvas.

Run this to visually verify the ImageCanvas implementation.
"""

import sys
from pathlib import Path

from PyQt6.QtGui import QColor, QImage
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from views.image_canvas import ImageCanvas


class ImageCanvasTestWindow(QMainWindow):
    """Test window for ImageCanvas."""

    def __init__(self):
        """Initialize the test window."""
        super().__init__()
        self.setWindowTitle("ImageCanvas Test")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create layout
        layout = QVBoxLayout(central_widget)

        # Create image canvas
        self.canvas = ImageCanvas()
        layout.addWidget(self.canvas)

        # Create button panel
        button_layout = QHBoxLayout()

        load_btn = QPushButton("Load Test Image")
        load_btn.clicked.connect(self.load_test_image)
        button_layout.addWidget(load_btn)

        load_file_btn = QPushButton("Load from File...")
        load_file_btn.clicked.connect(self.load_from_file)
        button_layout.addWidget(load_file_btn)

        zoom_in_btn = QPushButton("Zoom In")
        zoom_in_btn.clicked.connect(self.canvas.zoom_in)
        button_layout.addWidget(zoom_in_btn)

        zoom_out_btn = QPushButton("Zoom Out")
        zoom_out_btn.clicked.connect(self.canvas.zoom_out)
        button_layout.addWidget(zoom_out_btn)

        reset_btn = QPushButton("Reset Zoom")
        reset_btn.clicked.connect(self.canvas.reset_zoom)
        button_layout.addWidget(reset_btn)

        fit_btn = QPushButton("Fit to Window")
        fit_btn.clicked.connect(self.canvas.fit_to_window)
        button_layout.addWidget(fit_btn)

        layout.addLayout(button_layout)

        # Create a test image on startup
        self.create_test_image()

    def create_test_image(self):
        """Create a test image file."""
        # Create a colorful test image
        test_image = QImage(400, 300, QImage.Format.Format_RGB32)

        # Fill with gradient
        for y in range(300):
            for x in range(400):
                r = int((x / 400) * 255)
                g = int((y / 300) * 255)
                b = 128
                test_image.setPixel(x, y, QColor(r, g, b).rgb())

        # Save to temp file
        self.test_image_path = Path.cwd() / "test_canvas_image.png"
        test_image.save(str(self.test_image_path))

    def load_test_image(self):
        """Load the test image."""
        if self.test_image_path.exists():
            result = self.canvas.load_image(str(self.test_image_path))
            if result:
                print(f"[OK] Loaded test image: {self.test_image_path}")
            else:
                print("[ERROR] Failed to load test image")
        else:
            print("[ERROR] Test image not found")

    def load_from_file(self):
        """Load image from file dialog."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)",
        )

        if file_path:
            result = self.canvas.load_image(file_path)
            if result:
                print(f"[OK] Loaded image: {file_path}")
            else:
                print(f"[ERROR] Failed to load image: {file_path}")

    def closeEvent(self, event):
        """Clean up test image on close."""
        if hasattr(self, "test_image_path") and self.test_image_path.exists():
            self.test_image_path.unlink()
        event.accept()


def main():
    """Run the ImageCanvas test window."""
    app = QApplication(sys.argv)
    app.setApplicationName("ImageCanvas Test")

    window = ImageCanvasTestWindow()
    window.show()

    print("ImageCanvas Test Window is running.")
    print("")
    print("Test the following features:")
    print("[OK] Click 'Load Test Image' to load a gradient test image")
    print("[OK] Use mouse wheel to zoom in/out")
    print("[OK] Click and drag to pan the image")
    print("[OK] Click 'Zoom In' / 'Zoom Out' buttons")
    print("[OK] Click 'Reset Zoom' to return to 100%")
    print("[OK] Click 'Fit to Window' to fit image in viewport")
    print("[OK] Load your own image with 'Load from File...'")
    print("")
    print("Close the window to exit.")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
