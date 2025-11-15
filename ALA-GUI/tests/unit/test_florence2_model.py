"""
Unit tests for Florence2Model.

Tests the Florence-2 model integration following TDD methodology.
"""

import numpy as np
import pytest

# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit


class TestFlorence2ModelInitialization:
    """Tests for Florence2Model initialization."""

    def test_florence2_model_creation(self):
        """Test that Florence2Model can be created."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        assert model is not None

    def test_florence2_inherits_from_inference_engine(self):
        """Test that Florence2Model inherits from ModelInferenceEngine."""
        from models.florence2_model import Florence2Model
        from models.model_inference_engine import ModelInferenceEngine

        model = Florence2Model()
        assert isinstance(model, ModelInferenceEngine)

    def test_florence2_has_required_methods(self):
        """Test that Florence2Model implements required abstract methods."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        assert hasattr(model, "load_model")
        assert hasattr(model, "predict")
        assert hasattr(model, "detect_objects")
        assert hasattr(model, "generate_caption")


class TestFlorence2ModelLoading:
    """Tests for Florence-2 model loading."""

    def test_load_model_sets_device(self):
        """Test that load_model sets the device correctly."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        model.load_model("mock_checkpoint", device="cpu")
        assert model.device == "cpu"

    def test_load_model_with_cuda(self):
        """Test that CUDA device can be specified."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        model.load_model("mock_checkpoint", device="cuda")
        assert model.device == "cuda"

    def test_load_model_emits_signal(self, qtbot):
        """Test that model_loaded signal is emitted."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()

        with qtbot.waitSignal(model.model_loaded, timeout=2000):
            model.load_model("mock_checkpoint")

    def test_load_model_sets_is_loaded_flag(self):
        """Test that is_loaded flag is set after loading."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        assert model.is_loaded is False

        model.load_model("mock_checkpoint")
        assert model.is_loaded is True


class TestFlorence2ObjectDetection:
    """Tests for object detection functionality."""

    def test_detect_objects_with_text_prompt(self):
        """Test object detection with text prompt."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        model.load_model("mock_checkpoint")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        text_prompt = "person, car, dog"

        result = model.detect_objects(image, text_prompt)
        assert result is not None
        assert "boxes" in result
        assert "labels" in result
        assert "scores" in result

    def test_detect_objects_returns_bounding_boxes(self):
        """Test that detection returns bounding boxes in correct format."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        model.load_model("mock_checkpoint")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        result = model.detect_objects(image, "person")

        boxes = result["boxes"]
        assert isinstance(boxes, (list, np.ndarray))

        # Check box format (x1, y1, x2, y2)
        if len(boxes) > 0:
            box = boxes[0]
            assert len(box) == 4

    def test_detect_objects_multiple_classes(self):
        """Test detection with multiple object classes."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        model.load_model("mock_checkpoint")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        text_prompt = "person, car, bicycle"

        result = model.detect_objects(image, text_prompt)
        labels = result["labels"]

        # Should potentially detect multiple classes
        assert isinstance(labels, list)

    def test_detect_objects_emits_progress(self, qtbot):
        """Test that progress signals are emitted during detection."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        model.load_model("mock_checkpoint")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        with qtbot.waitSignal(model.progress, timeout=2000):
            model.detect_objects(image, "person")


class TestFlorence2CaptionGeneration:
    """Tests for caption generation functionality."""

    def test_generate_caption_returns_string(self):
        """Test that caption generation returns a string."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        model.load_model("mock_checkpoint")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        caption = model.generate_caption(image)

        assert isinstance(caption, str)
        assert len(caption) > 0

    def test_generate_caption_with_detailed_mode(self):
        """Test detailed caption generation."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        model.load_model("mock_checkpoint")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        caption = model.generate_caption(image, detailed=True)

        assert isinstance(caption, str)

    def test_generate_caption_emits_progress(self, qtbot):
        """Test that progress signals are emitted during captioning."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        model.load_model("mock_checkpoint")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        with qtbot.waitSignal(model.progress, timeout=2000):
            model.generate_caption(image)


class TestFlorence2GroundedDetection:
    """Tests for grounded detection with phrases."""

    def test_grounded_detection_with_phrase(self):
        """Test grounded detection with specific phrase."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        model.load_model("mock_checkpoint")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        phrase = "red car"

        result = model.grounded_detection(image, phrase)
        assert result is not None
        assert "boxes" in result

    def test_grounded_detection_multiple_phrases(self):
        """Test grounded detection with multiple phrases."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        model.load_model("mock_checkpoint")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        phrases = ["person walking", "blue car", "traffic light"]

        results = []
        for phrase in phrases:
            result = model.grounded_detection(image, phrase)
            results.append(result)

        assert len(results) == 3


class TestFlorence2Predict:
    """Tests for the unified predict method."""

    def test_predict_calls_detect_objects(self):
        """Test that predict method calls detect_objects."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        model.load_model("mock_checkpoint")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        # predict should default to object detection
        result = model.predict(image, text_prompt="person, car")
        assert "boxes" in result

    def test_predict_with_task_parameter(self):
        """Test predict with different task modes."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        model.load_model("mock_checkpoint")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        # Detection task
        result_det = model.predict(image, task="detection", text_prompt="person")
        assert "boxes" in result_det

        # Caption task
        result_cap = model.predict(image, task="caption")
        assert "caption" in result_cap or isinstance(result_cap, str)


class TestFlorence2BboxToMask:
    """Tests for bbox to mask conversion (integration with SAM2)."""

    def test_bbox_to_mask_conversion(self):
        """Test converting bounding boxes to masks."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        model.load_model("mock_checkpoint")

        # Sample bounding boxes (x1, y1, x2, y2)
        boxes = [(100, 100, 200, 200), (300, 300, 400, 400)]
        image_shape = (512, 512)

        if hasattr(model, "bbox_to_mask"):
            masks = model.bbox_to_mask(boxes, image_shape)
            assert isinstance(masks, (list, np.ndarray))
            if isinstance(masks, list):
                assert len(masks) == len(boxes)


class TestFlorence2BatchProcessing:
    """Tests for batch processing capabilities."""

    def test_predict_batch_multiple_images(self):
        """Test batch prediction on multiple images."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        model.load_model("mock_checkpoint")

        # Create batch of images
        images = [
            np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8) for _ in range(3)
        ]

        text_prompt = "person, car"

        if hasattr(model, "predict_batch"):
            results = model.predict_batch(images, text_prompt=text_prompt)
            assert len(results) == 3
            for result in results:
                assert "boxes" in result


class TestFlorence2ErrorHandling:
    """Tests for error handling in Florence2Model."""

    def test_predict_without_loading_model(self):
        """Test that prediction fails gracefully when model not loaded."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        with pytest.raises((RuntimeError, ValueError)):
            model.detect_objects(image, "person")

    def test_predict_with_invalid_image(self):
        """Test that prediction handles invalid image gracefully."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        model.load_model("mock_checkpoint")

        # Invalid image shape
        invalid_image = np.random.randint(0, 255, (10, 10), dtype=np.uint8)

        with pytest.raises((ValueError, RuntimeError)):
            model.detect_objects(invalid_image, "person")

    def test_error_signal_on_prediction_failure(self, qtbot):
        """Test that error signal is emitted on prediction failure."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        try:
            with qtbot.waitSignal(model.error, timeout=1000):
                model.detect_objects(image, "person")
        except (RuntimeError, ValueError):
            # Either exception or signal is acceptable
            pass


class TestFlorence2Integration:
    """Integration tests for Florence2Model."""

    def test_full_workflow(self):
        """Test complete workflow: load → detect → caption → unload."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()

        # Load model
        model.load_model("mock_checkpoint", device="cpu")
        assert model.is_model_loaded()

        # Detect objects
        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        detection_result = model.detect_objects(image, "person, car")
        assert detection_result is not None

        # Generate caption
        caption = model.generate_caption(image)
        assert isinstance(caption, str)

        # Unload
        model.unload_model()
        assert not model.is_model_loaded()

    def test_detection_to_sam2_integration(self):
        """Test that detection results are compatible with SAM2 input."""
        from models.florence2_model import Florence2Model

        model = Florence2Model()
        model.load_model("mock_checkpoint")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        result = model.detect_objects(image, "person")

        boxes = result["boxes"]

        # Check that boxes can be used as SAM2 prompts
        if len(boxes) > 0:
            box = boxes[0]
            assert len(box) == 4  # (x1, y1, x2, y2)
            assert all(isinstance(coord, (int, float, np.integer)) for coord in box)
