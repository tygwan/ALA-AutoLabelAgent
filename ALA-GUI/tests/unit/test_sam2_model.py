"""
Unit tests for SAM2Model.

Tests the SAM2 model integration following TDD methodology.
"""

import numpy as np
import pytest

# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit


class TestSAM2ModelInitialization:
    """Tests for SAM2Model initialization."""

    def test_sam2_model_creation(self):
        """Test that SAM2Model can be created."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()
        assert model is not None

    def test_sam2_inherits_from_inference_engine(self):
        """Test that SAM2Model inherits from ModelInferenceEngine."""
        from models.model_inference_engine import ModelInferenceEngine
        from models.sam2_model import SAM2Model

        model = SAM2Model()
        assert isinstance(model, ModelInferenceEngine)

    def test_sam2_has_required_methods(self):
        """Test that SAM2Model implements required abstract methods."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()
        assert hasattr(model, "load_model")
        assert hasattr(model, "predict")
        assert callable(model.load_model)
        assert callable(model.predict)


class TestSAM2ModelLoading:
    """Tests for SAM2 model loading."""

    def test_load_model_sets_device(self):
        """Test that load_model sets the device correctly."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()
        # Mock implementation should accept any path for testing
        model.load_model("mock_checkpoint.pth", device="cpu")
        assert model.device == "cpu"

    def test_load_model_with_cuda(self):
        """Test that CUDA device can be specified."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()
        model.load_model("mock_checkpoint.pth", device="cuda")
        assert model.device == "cuda"

    def test_load_model_emits_signal(self, qtbot):
        """Test that model_loaded signal is emitted."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()

        with qtbot.waitSignal(model.model_loaded, timeout=2000):
            model.load_model("mock_checkpoint.pth")

    def test_load_model_sets_is_loaded_flag(self):
        """Test that is_loaded flag is set after loading."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()
        assert model.is_loaded is False

        model.load_model("mock_checkpoint.pth")
        assert model.is_loaded is True


class TestSAM2Prediction:
    """Tests for SAM2 prediction methods."""

    def test_predict_with_point_prompt(self):
        """Test prediction with point prompts."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()
        model.load_model("mock_checkpoint.pth")

        # Mock image (H, W, 3)
        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        # Point prompt: (x, y, label) where label=1 for foreground
        points = [(256, 256, 1)]

        result = model.predict(image, points=points)
        assert result is not None
        assert "masks" in result
        assert "scores" in result

    def test_predict_with_box_prompt(self):
        """Test prediction with bounding box prompt."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()
        model.load_model("mock_checkpoint.pth")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        # Box prompt: (x1, y1, x2, y2)
        box = (100, 100, 400, 400)

        result = model.predict(image, box=box)
        assert result is not None
        assert "masks" in result

    def test_predict_with_multiple_points(self):
        """Test prediction with multiple point prompts."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()
        model.load_model("mock_checkpoint.pth")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        # Multiple points: foreground (label=1) and background (label=0)
        points = [(200, 200, 1), (300, 300, 1), (450, 450, 0)]

        result = model.predict(image, points=points)
        assert result is not None
        assert len(result["masks"]) > 0

    def test_predict_returns_mask_array(self):
        """Test that prediction returns numpy array masks."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()
        model.load_model("mock_checkpoint.pth")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        points = [(256, 256, 1)]

        result = model.predict(image, points=points)
        masks = result["masks"]

        assert isinstance(masks, (list, np.ndarray))
        if isinstance(masks, list):
            assert len(masks) > 0
            assert isinstance(masks[0], np.ndarray)

    def test_predict_emits_progress_signal(self, qtbot):
        """Test that progress signals are emitted during prediction."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()
        model.load_model("mock_checkpoint.pth")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        points = [(256, 256, 1)]

        with qtbot.waitSignal(model.progress, timeout=2000):
            model.predict(image, points=points)


class TestSAM2BatchProcessing:
    """Tests for batch processing capabilities."""

    def test_predict_batch_multiple_images(self):
        """Test batch prediction on multiple images."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()
        model.load_model("mock_checkpoint.pth")

        # Create batch of images
        images = [
            np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8) for _ in range(3)
        ]

        # Same prompt for all images
        points = [(256, 256, 1)]

        if hasattr(model, "predict_batch"):
            results = model.predict_batch(images, points=points)
            assert len(results) == 3
            for result in results:
                assert "masks" in result


class TestSAM2MaskPostProcessing:
    """Tests for mask post-processing."""

    def test_mask_smoothing(self):
        """Test mask smoothing functionality."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()

        # Create a rough binary mask
        mask = np.random.randint(0, 2, (512, 512), dtype=np.uint8)

        if hasattr(model, "smooth_mask"):
            smoothed = model.smooth_mask(mask)
            assert smoothed.shape == mask.shape
            assert smoothed.dtype == mask.dtype

    def test_mask_to_polygon(self):
        """Test converting mask to polygon contours."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()

        # Create a simple circular mask
        mask = np.zeros((512, 512), dtype=np.uint8)
        y, x = np.ogrid[:512, :512]
        circle = (x - 256) ** 2 + (y - 256) ** 2 <= 100**2
        mask[circle] = 1

        if hasattr(model, "mask_to_polygon"):
            polygons = model.mask_to_polygon(mask)
            assert isinstance(polygons, list)
            if len(polygons) > 0:
                assert isinstance(polygons[0], np.ndarray)


class TestSAM2ErrorHandling:
    """Tests for error handling in SAM2Model."""

    def test_predict_without_loading_model(self):
        """Test that prediction fails gracefully when model not loaded."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()
        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        # Should raise error or emit error signal
        with pytest.raises((RuntimeError, ValueError)):
            model.predict(image, points=[(256, 256, 1)])

    def test_predict_with_invalid_image(self):
        """Test that prediction handles invalid image gracefully."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()
        model.load_model("mock_checkpoint.pth")

        # Invalid image shape
        invalid_image = np.random.randint(0, 255, (10, 10), dtype=np.uint8)

        with pytest.raises((ValueError, RuntimeError)):
            model.predict(invalid_image, points=[(5, 5, 1)])

    def test_error_signal_on_prediction_failure(self, qtbot):
        """Test that error signal is emitted on prediction failure."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()

        # Try to predict without loading model
        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        # This should emit error signal instead of raising exception
        try:
            with qtbot.waitSignal(model.error, timeout=1000):
                model.predict(image, points=[(256, 256, 1)])
        except (RuntimeError, ValueError):
            # Either exception or signal is acceptable
            pass


class TestSAM2Integration:
    """Integration tests for SAM2Model."""

    def test_full_workflow(self):
        """Test complete workflow: load → predict → unload."""
        from models.sam2_model import SAM2Model

        model = SAM2Model()

        # Load model
        model.load_model("mock_checkpoint.pth", device="cpu")
        assert model.is_model_loaded()

        # Predict
        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        result = model.predict(image, points=[(256, 256, 1)])
        assert result is not None

        # Unload
        model.unload_model()
        assert not model.is_model_loaded()
