"""
Integration tests for Export Dialog.

Tests COCO and YOLO export functionality.
"""

import sys

from PyQt6.QtWidgets import QApplication

from views.export_dialog import ExportDialog


def main() -> None:
    """Run export dialog integration test."""
    app = QApplication(sys.argv)  # noqa: F841

    # Create test results
    test_results = {
        "boxes": [
            (100, 100, 200, 200),
            (300, 150, 450, 300),
            (50, 400, 150, 500),
        ],
        "labels": ["person", "car", "dog"],
        "scores": [0.95, 0.87, 0.92],
        "metadata": {
            "num_detections": 3,
            "image_width": 640,
            "image_height": 480,
        },
    }

    # Create export dialog
    dialog = ExportDialog()

    # Set test data
    dialog.set_results(test_results)
    dialog.set_image_path("test_image.jpg")

    print("✅ Created Export Dialog with test results")
    metadata = test_results["metadata"]
    labels = test_results["labels"]
    print(f"   - {metadata['num_detections']} detections")  # type: ignore
    print(f"   - Labels: {', '.join(labels)}")  # type: ignore
    print(
        f"   - Image size: {metadata['image_width']}x"  # type: ignore
        f"{metadata['image_height']}"  # type: ignore
    )

    # Show dialog
    print("\n🚀 Showing Export Dialog...")
    print("   Test Cases:")
    print("   1. Select COCO JSON format")
    print("      - Browse for output location")
    print("      - Set dataset name")
    print("      - Click Export")
    print("   2. Select YOLO TXT format")
    print("      - Browse for output directory")
    print("      - Click Export")
    print("      - Verify .txt and classes.txt created")

    result = dialog.exec()

    if result == ExportDialog.DialogCode.Accepted:
        print("✅ Export completed successfully")
    else:
        print("❌ Export cancelled")

    sys.exit(0)


if __name__ == "__main__":
    main()
