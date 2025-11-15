# Model UI Documentation

**M3: Model Integration - UI Components for AI-Powered Auto-Annotation**

## Overview

The Model UI provides a complete workflow for AI-powered auto-annotation using Florence-2 and SAM2 models. Users can:
- Run auto-annotation on single images
- Process multiple images in batch
- Review and accept/reject results
- Export annotations to COCO or YOLO formats

## Components

### 1. AutoAnnotateDialog

**Purpose**: Single image auto-annotation with AI models

**Location**: `src/views/auto_annotate_dialog.py`

**Features**:
- Model selection dropdown (Florence-2 + SAM2, Florence-2 Only, SAM2 Only)
- Text prompt input for object classes
- Progress tracking with QProgressBar
- Results preview with detection details
- Accept/Reject workflow
- Cancel support

**Usage**:
```python
from views.auto_annotate_dialog import AutoAnnotateDialog

# Create dialog
dialog = AutoAnnotateDialog(parent=main_window)

# Set image (numpy array in RGB format)
dialog.set_image(image_rgb)

# Set text prompt
dialog.set_text_prompt("person, car, dog")

# Connect signals
dialog.annotation_accepted.connect(handle_accepted)
dialog.annotation_rejected.connect(handle_rejected)

# Show dialog
dialog.exec()
```

**Signals**:
- `annotation_complete(dict)`: Emitted when annotation finishes
- `annotation_accepted(dict)`: Emitted when user accepts results
- `annotation_rejected()`: Emitted when user rejects results

**Workflow**:
1. User enters comma-separated object classes
2. Click "Run Auto-Annotation"
3. Progress bar shows processing status
4. Results preview displays detections
5. User reviews bounding boxes, labels, scores
6. Accept → annotations displayed on canvas, export dialog opens
7. Reject → clear results, allow retry with different prompt

### 2. BatchProcessDialog

**Purpose**: Process multiple images with auto-annotation

**Location**: `src/views/batch_process_dialog.py`

**Features**:
- File count display
- Overall progress bar (percentage completion)
- Per-file progress messages
- Success/error statistics tracking
- Detailed log output with status icons (✅/❌)
- Cancel functionality
- Thread-based processing for UI responsiveness

**Usage**:
```python
from views.batch_process_dialog import BatchProcessDialog

# Create dialog
dialog = BatchProcessDialog(parent=main_window)

# Set image paths
dialog.set_image_paths([
    "/path/to/image1.jpg",
    "/path/to/image2.jpg",
    "/path/to/image3.jpg"
])

# Set text prompt
dialog.set_text_prompt("person, car, dog")

# Show dialog
dialog.exec()
```

**Statistics**:
- Processed: Total images processed
- Success: Successfully annotated images
- Errors: Failed images with error messages

**Worker Thread**:
- `BatchProcessWorker` runs in QThread
- Emits progress signals for UI updates
- Supports cancellation mid-processing
- Handles per-file errors gracefully

### 3. ResultsPreviewWidget

**Purpose**: Preview annotation results before accepting

**Location**: `src/widgets/results_preview_widget.py`

**Features**:
- Detection count summary
- Scrollable detection list
- Per-detection details:
  - Detection number and class label
  - Bounding box coordinates (x1, y1) → (x2, y2)
  - Box dimensions (width × height)
  - Confidence score as percentage
- Styled detection cards with visual separation

**Usage**:
```python
from widgets.results_preview_widget import ResultsPreviewWidget

# Create widget
preview = ResultsPreviewWidget()

# Display results
preview.display_results(results_dict)

# Clear preview
preview.clear()
```

**Results Format**:
```python
results = {
    'boxes': [(x1, y1, x2, y2), ...],
    'labels': ['class1', 'class2', ...],
    'scores': [0.95, 0.87, ...],
    'metadata': {
        'num_detections': 3,
        'image_width': 640,
        'image_height': 480
    }
}
```

### 4. ExportDialog

**Purpose**: Export annotations to COCO or YOLO formats

**Location**: `src/views/export_dialog.py`

**Features**:
- Format selection: COCO JSON or YOLO TXT
- Format-specific file browsers
- Dataset name input (COCO only)
- Validation and error handling
- Success/error message boxes

**Usage**:
```python
from views.export_dialog import ExportDialog

# Create dialog
dialog = ExportDialog(parent=main_window)

# Set results and image path
dialog.set_results(results_dict)
dialog.set_image_path("/path/to/image.jpg")

# Show dialog
dialog.exec()
```

**Export Formats**:

**COCO JSON**:
- Single JSON file with MS COCO structure
- Bounding boxes in [x, y, width, height] format
- Category mapping with supercategory
- Image metadata (dimensions, filename)
- Confidence scores included

**YOLO TXT**:
- One .txt file per image
- Normalized coordinates (x_center, y_center, width, height)
- Class ID mapping from class names
- Auto-generated classes.txt file

## Integration with Main Window

### Menu Integration

**Tools Menu**:
- **Auto-Annotate... (Ctrl+A)**: Open auto-annotation dialog
- **Batch Process... (Ctrl+B)**: Open batch processing dialog

**File Menu**:
- **Export Annotations... (Ctrl+E)**: Open export dialog

### Toolbar Integration

Auto-annotation and batch processing buttons are available in the main toolbar for quick access.

### Workflow Integration

**Complete Auto-Annotation Workflow**:
1. User loads image in main window
2. Clicks "Auto-Annotate" (Ctrl+A)
3. Dialog validates image is loaded
4. User enters object classes
5. Clicks "Run Auto-Annotation"
6. Reviews results in preview widget
7. Clicks "Accept Results"
8. Annotations display on canvas
9. Export dialog opens automatically
10. User selects format and exports

**Batch Processing Workflow**:
1. User adds multiple images to file list
2. Clicks "Batch Process" (Ctrl+B)
3. Dialog shows file count
4. User enters object classes
5. Clicks "Start Batch Processing"
6. Monitors progress and log
7. Reviews statistics when complete

## Model Integration

### ModelController

**Location**: `src/models/model_controller.py`

**Purpose**: Orchestrate Florence-2 and SAM2 models

**Key Methods**:
- `load_models(florence_path, sam_path)`: Load model checkpoints
- `run_autodistill(image, text_prompt)`: Run Florence-2 + SAM2 pipeline
- `cancel_inference()`: Cancel ongoing inference

**Signals**:
- `progress(int, str)`: Progress updates (percentage, message)
- `autodistill_complete(dict)`: Results ready
- `error(str)`: Error occurred

### Florence2Model

**Location**: `src/models/florence2_model.py`

**Capabilities**:
- Object detection with text prompts
- Caption generation (brief and detailed)
- Grounded detection with phrases
- Batch processing

**Tasks**:
- `<CAPTION_TO_PHRASE_GROUNDING>`: Object detection
- `<CAPTION>`: Brief caption
- `<DETAILED_CAPTION>`: Detailed caption

### SAM2Model

**Location**: `src/models/sam2_model.py`

**Capabilities**:
- Point-based prompting (foreground/background)
- Bounding box prompting
- Multiple prompt refinement
- Mask post-processing

**Input Prompts**:
- Points: `[(x, y, label), ...]` where label=1 (foreground), 0 (background)
- Box: `(x1, y1, x2, y2)`

## Configuration

### Model Settings

Models are automatically downloaded on first use:
- **Florence-2**: `microsoft/Florence-2-large` from HuggingFace
- **SAM2**: `sam2_hiera_base_plus.pth` from Facebook AI

**Cache Location**: `~/.cache/autodistill/`

### Device Selection

Supports CPU, CUDA (NVIDIA GPU), and MPS (Apple Silicon):
```python
model.load_model(checkpoint_path, device="cuda")  # or "cpu", "mps"
```

Auto-fallback to CPU if requested device unavailable.

## Performance Considerations

### Optimization Tips

1. **Use GPU**: Significantly faster than CPU (10-100x speedup)
2. **Batch Processing**: More efficient for multiple images
3. **Model Caching**: Models loaded once, reused for all images
4. **Image Resizing**: Resize large images before processing

### Expected Performance

**With GPU (CUDA)**:
- Florence-2: ~2-5 seconds per image
- SAM2: ~1-3 seconds per image
- Total: ~3-8 seconds per image

**With CPU**:
- Florence-2: ~20-60 seconds per image
- SAM2: ~10-30 seconds per image
- Total: ~30-90 seconds per image

## Error Handling

### Common Issues

**No Models Loaded**:
- Error: "Model not loaded. Call load_model() first."
- Solution: Models auto-download on first use

**No Image Set**:
- Error: "No image set. Call set_image() first."
- Solution: Load image before opening auto-annotate dialog

**Empty Text Prompt**:
- Error: "Please enter object classes to detect."
- Solution: Enter comma-separated class names

**Invalid Image Format**:
- Error: "Invalid image shape. Expected (H, W, 3)"
- Solution: Ensure image is RGB format

### Recovery Strategies

**Model Loading Fails**:
- Check internet connection (for auto-download)
- Verify disk space for model cache
- Check PyTorch installation

**Inference Fails**:
- Reduce image size
- Simplify text prompt
- Check available memory

**Export Fails**:
- Verify output directory exists
- Check write permissions
- Ensure valid filename

## Testing

### Manual Testing

Run E2E test:
```bash
python src/test_e2e_auto_annotation.py
```

### Test Dialogs Individually

**Auto-Annotate**:
```bash
python src/test_main_window.py  # Then click Auto-Annotate
```

**Batch Process**:
```bash
python src/test_batch_process_dialog.py
```

**Export**:
```bash
python src/test_export_dialog.py
```

## Future Enhancements

### Planned Features

- [ ] Few-shot classification support
- [ ] Custom model loading
- [ ] Advanced prompt engineering
- [ ] Annotation editing tools
- [ ] Model performance monitoring
- [ ] Result comparison view
- [ ] Batch export to multiple formats

### Under Consideration

- Real-time annotation preview during processing
- Confidence threshold adjustment
- IoU threshold tuning
- Active learning integration
- Model fine-tuning UI

## References

- [Florence-2 Paper](https://arxiv.org/abs/2311.06242)
- [SAM2 Paper](https://arxiv.org/abs/2408.00714)
- [MS COCO Format](https://cocodataset.org/#format-data)
- [YOLO Format](https://docs.ultralytics.com/datasets/detect/)
