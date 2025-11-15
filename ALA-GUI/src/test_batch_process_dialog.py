"""
Integration tests for Batch Processing Dialog.

Tests the batch processing workflow with multiple images.
"""

import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image
from PyQt6.QtWidgets import QApplication

from views.batch_process_dialog import BatchProcessDialog


def create_test_image(path: str, width: int = 640, height: int = 480) -> None:
    """Create a test image file."""
    # Create random RGB image
    image_array = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    image = Image.fromarray(image_array, "RGB")
    image.save(path)


def main() -> None:
    """Run batch process dialog integration test."""
    app = QApplication(sys.argv)

    # Create temporary test images
    temp_dir = tempfile.mkdtemp()
    test_images = []

    for i in range(3):
        image_path = Path(temp_dir) / f"test_image_{i}.jpg"
        create_test_image(str(image_path))
        test_images.append(str(image_path))
        print(f"✅ Created test image: {image_path}")

    # Create batch process dialog
    dialog = BatchProcessDialog()

    # Set image paths
    dialog.set_image_paths(test_images)
    print(f"✅ Set {len(test_images)} image paths")

    # Set text prompt
    dialog.set_text_prompt("person, car, dog")
    print("✅ Set text prompt: 'person, car, dog'")

    # Show dialog
    print("\n🚀 Showing Batch Process Dialog...")
    print("   - Check file count display")
    print("   - Click 'Start Batch Processing' to begin")
    print("   - Monitor progress bar and log output")
    print("   - Test cancel functionality")
    print("   - Check statistics display")

    dialog.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
