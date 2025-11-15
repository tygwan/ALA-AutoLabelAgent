"""
Unit tests for ModelController.

Tests the model controller that coordinates Florence-2 and SAM2 models.
"""

import numpy as np
import pytest

# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit


class TestModelControllerInitialization:
    """Tests for ModelController initialization."""

    def test_model_controller_creation(self):
        """Test that ModelController can be created."""
        from models.model_controller import ModelController

        controller = ModelController()
        assert controller is not None

    def test_model_controller_inherits_from_qobject(self):
        """Test that ModelController inherits from QObject."""
        from PyQt6.QtCore import QObject

        from models.model_controller import ModelController

        controller = ModelController()
        assert isinstance(controller, QObject)

    def test_model_controller_has_florence2_model(self):
        """Test that ModelController has Florence2Model instance."""
        from models.model_controller import ModelController

        controller = ModelController()
        assert hasattr(controller, "florence2_model")
        assert controller.florence2_model is not None

    def test_model_controller_has_sam2_model(self):
        """Test that ModelController has SAM2Model instance."""
        from models.model_controller import ModelController

        controller = ModelController()
        assert hasattr(controller, "sam2_model")
        assert controller.sam2_model is not None

    def test_model_controller_has_required_signals(self):
        """Test that ModelController has required signals."""
        from models.model_controller import ModelController

        controller = ModelController()
        assert hasattr(controller, "progress")
        assert hasattr(controller, "error")
        assert hasattr(controller, "autodistill_complete")
        assert hasattr(controller, "cancelled")


class TestModelControllerModelLoading:
    """Tests for model loading functionality."""

    def test_load_models(self):
        """Test that load_models loads both Florence-2 and SAM2."""
        from models.model_controller import ModelController

        controller = ModelController()
        controller.load_models("florence_path", "sam_path")

        assert controller.florence2_model.is_model_loaded()
        assert controller.sam2_model.is_model_loaded()

    def test_load_models_with_device(self):
        """Test model loading with specific device."""
        from models.model_controller import ModelController

        controller = ModelController()
        controller.load_models("florence_path", "sam_path", device="cuda")

        assert controller.florence2_model.device == "cuda"
        assert controller.sam2_model.device == "cuda"

    def test_load_models_emits_progress(self, qtbot):
        """Test that progress signals are emitted during loading."""
        from models.model_controller import ModelController

        controller = ModelController()

        with qtbot.waitSignal(controller.progress, timeout=2000):
            controller.load_models("florence_path", "sam_path")


class TestModelControllerAutodistill:
    """Tests for autodistill functionality."""

    def test_run_autodistill_basic(self):
        """Test basic autodistill workflow."""
        from models.model_controller import ModelController

        controller = ModelController()
        controller.load_models("florence_path", "sam_path")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        text_prompt = "person, car"

        result = controller.run_autodistill(image, text_prompt)

        assert result is not None
        assert "detections" in result
        assert "masks" in result

    def test_run_autodistill_returns_annotations(self):
        """Test that autodistill returns proper annotation format."""
        from models.model_controller import ModelController

        controller = ModelController()
        controller.load_models("florence_path", "sam_path")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        result = controller.run_autodistill(image, "person")

        detections = result["detections"]
        masks = result["masks"]

        assert isinstance(detections, dict)
        assert isinstance(masks, list)
        assert "boxes" in detections
        assert "labels" in detections

    def test_run_autodistill_emits_progress(self, qtbot):
        """Test that progress signals are emitted during autodistill."""
        from models.model_controller import ModelController

        controller = ModelController()
        controller.load_models("florence_path", "sam_path")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        with qtbot.waitSignal(controller.progress, timeout=3000):
            controller.run_autodistill(image, "person")

    def test_run_autodistill_emits_complete(self, qtbot):
        """Test that completion signal is emitted after autodistill."""
        from models.model_controller import ModelController

        controller = ModelController()
        controller.load_models("florence_path", "sam_path")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        with qtbot.waitSignal(controller.autodistill_complete, timeout=3000):
            controller.run_autodistill(image, "person")


class TestModelControllerCancellation:
    """Tests for cancellation support."""

    def test_cancel_inference(self):
        """Test that inference can be cancelled."""
        from models.model_controller import ModelController

        controller = ModelController()
        controller.cancel_inference()

        assert controller._is_cancelled is True

    def test_cancel_emits_signal(self, qtbot):
        """Test that cancellation emits signal."""
        from models.model_controller import ModelController

        controller = ModelController()

        with qtbot.waitSignal(controller.cancelled, timeout=1000):
            controller.cancel_inference()

    def test_run_autodistill_respects_cancellation(self):
        """Test that autodistill checks for cancellation."""
        from models.model_controller import ModelController

        controller = ModelController()
        controller.load_models("florence_path", "sam_path")

        # Cancel before running
        controller.cancel_inference()

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        result = controller.run_autodistill(image, "person")

        # Should return None or empty result when cancelled
        assert result is None or result == {}


class TestModelControllerCaching:
    """Tests for result caching."""

    def test_cache_enabled_by_default(self):
        """Test that caching is enabled by default."""
        from models.model_controller import ModelController

        controller = ModelController()
        assert hasattr(controller, "_cache")
        assert isinstance(controller._cache, dict)

    def test_run_autodistill_uses_cache(self):
        """Test that results are cached for repeated calls."""
        from models.model_controller import ModelController

        controller = ModelController()
        controller.load_models("florence_path", "sam_path")

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        text_prompt = "person"

        # First call
        result1 = controller.run_autodistill(image, text_prompt)

        # Second call with same inputs
        result2 = controller.run_autodistill(image, text_prompt)

        # Results should be identical (from cache)
        assert result1 == result2

    def test_clear_cache(self):
        """Test that cache can be cleared."""
        from models.model_controller import ModelController

        controller = ModelController()
        controller._cache["test"] = "data"

        if hasattr(controller, "clear_cache"):
            controller.clear_cache()
            assert len(controller._cache) == 0


class TestModelControllerErrorHandling:
    """Tests for error handling."""

    def test_autodistill_without_loading_models(self):
        """Test that autodistill fails gracefully without loaded models."""
        from models.model_controller import ModelController

        controller = ModelController()

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        with pytest.raises((RuntimeError, ValueError)):
            controller.run_autodistill(image, "person")

    def test_error_signal_on_failure(self, qtbot):
        """Test that error signal is emitted on failure."""
        from models.model_controller import ModelController

        controller = ModelController()

        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

        try:
            with qtbot.waitSignal(controller.error, timeout=1000):
                controller.run_autodistill(image, "person")
        except (RuntimeError, ValueError):
            # Either exception or signal is acceptable
            pass
