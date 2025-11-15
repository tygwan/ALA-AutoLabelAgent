"""
Manual test script for MainWindow.

Run this to visually verify the MainWindow implementation.
"""

import sys

from PyQt6.QtWidgets import QApplication

from views.main_window import MainWindow


def main():
    """Run the MainWindow for manual testing."""
    app = QApplication(sys.argv)
    app.setApplicationName("ALA-GUI")
    app.setOrganizationName("ALA")

    window = MainWindow()
    window.show()

    print("MainWindow is running. Check the following:")
    print("[OK] Window title: 'ALA-GUI - Auto Label Agent'")
    print("[OK] Window size: 1280x720")
    print("[OK] Menu bar: File, Edit, View, Tools, Help")
    print("[OK] Toolbar: New, Open, Save, Previous, Next, Zoom In/Out, Fit")
    print("[OK] Status bar: Shows 'Ready' message")
    print("[OK] Dock widgets: Files (left), Classes (right), Properties (right)")
    print("[OK] Central widget: Placeholder for image canvas")
    print("")
    print("Close the window to exit.")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
