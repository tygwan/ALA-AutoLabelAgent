"""
ALA-GUI Main Entry Point

This is the main entry point for the ALA-GUI application.
Currently displays a basic PyQt6 window to verify installation.
"""

import sys

try:
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow

    PYQT6_AVAILABLE = True
except ImportError:
    PYQT6_AVAILABLE = False
    print("PyQt6 not installed. Please run: pip install -r requirements.txt")


class MainWindow(QMainWindow):
    """
    Main application window.

    This is a placeholder implementation for M0: Project Setup.
    Full implementation will be added in M2: PyQt6 Image Display & Navigation.
    """

    def __init__(self) -> None:
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        """Initialize the user interface."""
        self.setWindowTitle("ALA-GUI - Auto Label Agent")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget with welcome message
        label = QLabel("Welcome to ALA-GUI!\n\nProject Setup Complete ✅", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            """
            QLabel {
                font-size: 24px;
                padding: 20px;
            }
        """
        )

        self.setCentralWidget(label)


def main() -> int:
    """
    Main application function.

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    if not PYQT6_AVAILABLE:
        return 1

    app = QApplication(sys.argv)
    app.setApplicationName("ALA-GUI")
    app.setOrganizationName("ALA")

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
