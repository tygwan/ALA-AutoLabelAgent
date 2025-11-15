"""
End-to-End Test for Auto-Annotation Workflow.

M3: Model Integration - Complete workflow test from image load to export.

This test validates the entire auto-annotation workflow:
1. Load image into main window
2. Open auto-annotate dialog
3. Configure model and text prompt
4. Run auto-annotation
5. Review results
6. Accept results
7. Export to COCO/YOLO

Note: This is an integration test that requires manual interaction.
For automated E2E testing, use pytest-qt with QTest.
"""

import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image
from PyQt6.QtWidgets import QApplication

from views.main_window import MainWindow


def create_test_image(path: str, width: int = 640, height: int = 480) -> None:
    """
    Create a test image file with random content.

    Args:
        path: Output file path
        width: Image width
        height: Image height
    """
    # Create random RGB image
    image_array = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    image = Image.fromarray(image_array, "RGB")
    image.save(path)


def main() -> None:
    """Run E2E test for auto-annotation workflow."""
    app = QApplication(sys.argv)

    # Create temporary test directory
    temp_dir = Path(tempfile.mkdtemp())
    print(f"📁 Created temp directory: {temp_dir}")

    # Create test images
    test_images = []
    for i in range(3):
        image_path = temp_dir / f"test_image_{i}.jpg"
        create_test_image(str(image_path))
        test_images.append(str(image_path))
        print(f"✅ Created test image: {image_path.name}")

    # Create main window
    window = MainWindow()
    window.show()

    print("\n🚀 Starting E2E Auto-Annotation Workflow Test")
    print("=" * 70)

    # Test Steps
    print("\n📋 TEST WORKFLOW:")
    print("1. Add Test Images to File List")
    print("   - Use file list widget to add images")
    print("   - Or drag and drop images into file list")
    print("   - Verify thumbnails are generated")

    for img_path in test_images:
        window.file_list_widget.add_image(img_path)
        print(f"   ✓ Added: {Path(img_path).name}")

    print("\n2. Load First Image")
    print("   - Click on first image in file list")
    print("   - Verify image displays in canvas")
    print("   - Try zoom in/out and pan")

    # Simulate loading first image
    if test_images:
        window.file_list_widget.list_widget.setCurrentRow(0)
        print("   ✓ Loaded first image")

    print("\n3. Open Auto-Annotate Dialog")
    print("   - Click 'Auto-Annotate' in Tools menu (Ctrl+A)")
    print("   - Or click Auto-Annotate button in toolbar")
    print("   - Verify dialog opens with current image")
    print("   ⚠️  Note: Models not loaded - will show mock results")

    print("\n4. Configure Auto-Annotation")
    print("   - Select model: Florence-2 + SAM2 (Best Quality)")
    print("   - Enter text prompt: 'person, car, dog, cat, bicycle'")
    print("   - Verify progress bar is at 0%")

    print("\n5. Run Auto-Annotation")
    print("   - Click 'Run Auto-Annotation' button")
    print("   - Monitor progress bar (mock: instant completion)")
    print("   - Wait for completion message")
    print("   - Verify detection count displayed")

    print("\n6. Review Results")
    print("   - Check results preview widget")
    print("   - Review detection details:")
    print("     • Detection count summary")
    print("     • Bounding box coordinates")
    print("     • Class labels")
    print("     • Confidence scores")
    print("   - Verify Accept/Reject buttons appear")

    print("\n7. Accept or Reject Results")
    print("   Option A - ACCEPT:")
    print("   - Click '✓ Accept Results' button")
    print("   - Verify annotations overlay on canvas")
    print("   - Export dialog should open automatically")
    print("   - Verify results are pre-filled")
    print("")
    print("   Option B - REJECT:")
    print("   - Click '✗ Reject & Retry' button")
    print("   - Verify preview clears")
    print("   - Verify can retry with different prompt")

    print("\n8. Export Annotations (if accepted)")
    print("   - Select export format:")
    print("     • COCO JSON: Single JSON file")
    print("     • YOLO TXT: One .txt per image + classes.txt")
    print("   - For COCO:")
    print("     • Set dataset name")
    print("     • Browse for output file (.json)")
    print("     • Click Export")
    print("   - For YOLO:")
    print("     • Browse for output directory")
    print("     • Click Export")
    print("     • Verify .txt and classes.txt created")

    print("\n9. Batch Processing Test")
    print("   - Click 'Batch Process' in Tools menu (Ctrl+B)")
    print("   - Verify all 3 images are listed")
    print("   - Enter same text prompt")
    print("   - Click 'Start Batch Processing'")
    print("   - Monitor progress for all images")
    print("   - Check success/error statistics")
    print("   - Review log output")

    print("\n10. Manual Export Test")
    print("   - With annotations visible on canvas")
    print("   - Click 'Export Annotations' (Ctrl+E)")
    print("   - Verify current image path is set")
    print("   - Test both COCO and YOLO export")

    print("\n" + "=" * 70)
    print("🔍 VALIDATION CHECKLIST:")
    print("=" * 70)

    validation_items = [
        "[ ] Images load correctly in file list",
        "[ ] Thumbnails are generated and displayed",
        "[ ] Image canvas displays selected image",
        "[ ] Zoom and pan work correctly",
        "[ ] Auto-annotate dialog opens with image",
        "[ ] Model selection dropdown works",
        "[ ] Text prompt input accepts comma-separated classes",
        "[ ] Progress bar updates during processing",
        "[ ] Results preview shows detection details",
        "[ ] Bounding boxes display on canvas after accept",
        "[ ] Accept/Reject buttons function correctly",
        "[ ] Export dialog pre-fills results",
        "[ ] COCO export creates valid JSON",
        "[ ] YOLO export creates .txt and classes.txt",
        "[ ] Batch processing handles multiple images",
        "[ ] Statistics update correctly during batch",
        "[ ] Error handling works (try empty prompt)",
        "[ ] Cancel functionality works",
        "[ ] Status bar shows appropriate messages",
        "[ ] Keyboard shortcuts work (Ctrl+A, Ctrl+B, Ctrl+E)",
    ]

    for item in validation_items:
        print(f"  {item}")

    print("\n" + "=" * 70)
    print("📝 TEST NOTES:")
    print("=" * 70)
    print("• Models are not loaded - results will be mock/empty")
    print("• To test with real models, install torch and transformers:")
    print("  pip install torch transformers")
    print("• Real model test will download Florence-2 and SAM2 checkpoints")
    print("• First run with real models may take several minutes")
    print("• Subsequent runs will use cached models")
    print("")
    print("🎯 Expected Behavior:")
    print("• Auto-annotate dialog should open without errors")
    print("• UI controls should be responsive")
    print("• Export should create valid format files")
    print("• No crashes or exceptions in console")
    print("")
    print("⚠️  Known Limitations:")
    print("• Mock results have no actual detections")
    print("• Real models require GPU for good performance")
    print("• Large images may take time to process")

    print("\n" + "=" * 70)
    print("🚀 E2E Test Ready - Interact with UI to validate workflow")
    print("=" * 70)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
