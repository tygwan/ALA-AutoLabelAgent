"""ALA-GUI Main Entry Point.

This is the main entry point for the ALA-GUI application.
Launches the full MainWindow with all M1-M3 features:
- File list and image navigation (M2)
- Auto-annotation with Florence-2 + SAM2 (M3)
- Batch processing and export (M3)
"""

import sys

try:
    from PyQt6.QtWidgets import QApplication

    PYQT6_AVAILABLE = True
except ImportError:
    PYQT6_AVAILABLE = False
    print("PyQt6 not installed. Please run: pip install -r requirements.txt")

from views.main_window import MainWindow


def main() -> int:
    """Run the main application.

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
