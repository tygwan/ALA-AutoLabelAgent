"""
Unit tests for ModelInferenceEngine.

Tests the base model inference engine following TDD methodology.
"""

import pytest
from PyQt6.QtCore import QObject, pyqtSignal

# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit


class TestModelInferenceEngineInitialization:
    """Tests for ModelInferenceEngine initialization."""

    def test_model_inference_engine_creation(self):
        """Test that ModelInferenceEngine can be created."""
        from models.model_inference_engine import ModelInferenceEngine

        class TestModel(ModelInferenceEngine):
            """Test implementation of ModelInferenceEngine."""

            def load_model(self, model_path: str, device: str = "cpu"):
                """Test implementation of load_model."""
                pass

            def predict(self, image, **kwargs):
                """Test implementation of predict."""
                pass

        engine = TestModel()
        assert engine is not None

    def test_engine_is_qobject(self):
        """Test that ModelInferenceEngine inherits from QObject for signals."""
        from models.model_inference_engine import ModelInferenceEngine

        class TestModel(ModelInferenceEngine):
            """Test implementation of ModelInferenceEngine."""

            def load_model(self, model_path: str, device: str = "cpu"):
                """Test implementation."""
                pass

            def predict(self, image, **kwargs):
                """Test implementation."""
                pass

        engine = TestModel()
        assert isinstance(engine, QObject)

    def test_engine_has_model_loaded_signal(self):
        """Test that engine has model_loaded signal."""
        from models.model_inference_engine import ModelInferenceEngine

        class TestModel(ModelInferenceEngine):
            """Test implementation."""

            def load_model(self, model_path: str, device: str = "cpu"):
                """Test implementation."""
                pass

            def predict(self, image, **kwargs):
                """Test implementation."""
                pass

        engine = TestModel()
        assert hasattr(engine, "model_loaded")
        assert isinstance(engine.model_loaded, pyqtSignal)

    def test_engine_has_progress_signal(self):
        """Test that engine has progress signal."""
        from models.model_inference_engine import ModelInferenceEngine

        class TestModel(ModelInferenceEngine):
            """Test implementation."""

            def load_model(self, model_path: str, device: str = "cpu"):
                """Test implementation."""
                pass

            def predict(self, image, **kwargs):
                """Test implementation."""
                pass

        engine = TestModel()
        assert hasattr(engine, "progress")

    def test_engine_has_error_signal(self):
        """Test that engine has error signal."""
        from models.model_inference_engine import ModelInferenceEngine

        class TestModel(ModelInferenceEngine):
            """Test implementation."""

            def load_model(self, model_path: str, device: str = "cpu"):
                """Test implementation."""
                pass

            def predict(self, image, **kwargs):
                """Test implementation."""
                pass

        engine = TestModel()
        assert hasattr(engine, "error")


class TestModelInferenceEngineAbstractMethods:
    """Tests for abstract methods that must be implemented."""

    def test_load_model_is_abstract(self):
        """Test that load_model must be implemented by subclasses."""
        from models.model_inference_engine import ModelInferenceEngine

        with pytest.raises(TypeError):
            # Cannot instantiate abstract class
            ModelInferenceEngine()

    def test_predict_is_abstract(self):
        """Test that predict must be implemented by subclasses."""
        from models.model_inference_engine import ModelInferenceEngine

        class IncompleteModel(ModelInferenceEngine):
            """Incomplete implementation missing predict."""

            def load_model(self, model_path: str, device: str = "cpu"):
                """Load model from checkpoint."""
                pass

        with pytest.raises(TypeError):
            # Missing predict method
            IncompleteModel()


class TestDeviceSelection:
    """Tests for device selection (CPU/GPU)."""

    def test_default_device_is_cpu(self):
        """Test that default device is CPU."""
        from models.model_inference_engine import ModelInferenceEngine

        class TestModel(ModelInferenceEngine):
            """Test implementation."""

            def load_model(self, model_path: str, device: str = "cpu"):
                """Test implementation."""
                self.device = device

            def predict(self, image, **kwargs):
                """Test implementation."""
                pass

        engine = TestModel()
        engine.load_model("test.pth")
        assert engine.device == "cpu"

    def test_can_set_cuda_device(self):
        """Test that CUDA device can be set."""
        from models.model_inference_engine import ModelInferenceEngine

        class TestModel(ModelInferenceEngine):
            """Test implementation."""

            def load_model(self, model_path: str, device: str = "cpu"):
                """Test implementation."""
                self.device = device

            def predict(self, image, **kwargs):
                """Test implementation."""
                pass

        engine = TestModel()
        engine.load_model("test.pth", device="cuda")
        assert engine.device == "cuda"

    def test_can_set_mps_device(self):
        """Test that MPS device (Apple Silicon) can be set."""
        from models.model_inference_engine import ModelInferenceEngine

        class TestModel(ModelInferenceEngine):
            """Test implementation."""

            def load_model(self, model_path: str, device: str = "cpu"):
                """Test implementation."""
                self.device = device

            def predict(self, image, **kwargs):
                """Test implementation."""
                pass

        engine = TestModel()
        engine.load_model("test.pth", device="mps")
        assert engine.device == "mps"


class TestModelCaching:
    """Tests for model instance caching."""

    def test_model_is_cached_after_load(self):
        """Test that model is cached after loading."""
        from models.model_inference_engine import ModelInferenceEngine

        class TestModel(ModelInferenceEngine):
            """Test implementation."""

            def load_model(self, model_path: str, device: str = "cpu"):
                """Test implementation."""
                self.model = "mock_model"
                self.is_loaded = True

            def predict(self, image, **kwargs):
                """Test implementation."""
                pass

        engine = TestModel()
        engine.load_model("test.pth")
        assert engine.is_loaded is True
        assert engine.model is not None

    def test_model_can_be_unloaded(self):
        """Test that model can be unloaded to free memory."""
        from models.model_inference_engine import ModelInferenceEngine

        class TestModel(ModelInferenceEngine):
            """Test implementation."""

            def load_model(self, model_path: str, device: str = "cpu"):
                """Test implementation."""
                self.model = "mock_model"
                self.is_loaded = True

            def predict(self, image, **kwargs):
                """Test implementation."""
                pass

            def unload_model(self):
                """Unload the model."""
                self.model = None
                self.is_loaded = False

        engine = TestModel()
        engine.load_model("test.pth")
        assert engine.is_loaded is True

        engine.unload_model()
        assert engine.is_loaded is False
        assert engine.model is None


class TestErrorHandling:
    """Tests for error handling."""

    def test_error_signal_emitted_on_load_failure(self, qtbot):
        """Test that error signal is emitted when model fails to load."""
        from models.model_inference_engine import ModelInferenceEngine

        class TestModel(ModelInferenceEngine):
            """Test implementation."""

            def load_model(self, model_path: str, device: str = "cpu"):
                """Test implementation that fails."""
                self.error.emit("Failed to load model")

            def predict(self, image, **kwargs):
                """Test implementation."""
                pass

        engine = TestModel()

        with qtbot.waitSignal(engine.error, timeout=1000) as blocker:
            engine.load_model("invalid.pth")

        assert blocker.args[0] == "Failed to load model"

    def test_error_signal_emitted_on_predict_failure(self, qtbot):
        """Test that error signal is emitted when prediction fails."""
        from models.model_inference_engine import ModelInferenceEngine

        class TestModel(ModelInferenceEngine):
            """Test implementation."""

            def load_model(self, model_path: str, device: str = "cpu"):
                """Test implementation."""
                pass

            def predict(self, image, **kwargs):
                """Test implementation that fails."""
                self.error.emit("Prediction failed")

        engine = TestModel()

        with qtbot.waitSignal(engine.error, timeout=1000) as blocker:
            engine.predict(None)

        assert blocker.args[0] == "Prediction failed"


class TestProgressSignals:
    """Tests for progress signals."""

    def test_progress_signal_during_loading(self, qtbot):
        """Test that progress signal is emitted during model loading."""
        from models.model_inference_engine import ModelInferenceEngine

        class TestModel(ModelInferenceEngine):
            """Test implementation."""

            def load_model(self, model_path: str, device: str = "cpu"):
                """Test implementation with progress."""
                self.progress.emit(50, "Loading model...")
                self.progress.emit(100, "Model loaded")

            def predict(self, image, **kwargs):
                """Test implementation."""
                pass

        engine = TestModel()

        with qtbot.waitSignal(engine.progress, timeout=1000) as blocker:
            engine.load_model("test.pth")

        # Should receive progress signals
        assert blocker.args[0] >= 0
        assert blocker.args[0] <= 100

    def test_progress_signal_during_prediction(self, qtbot):
        """Test that progress signal is emitted during prediction."""
        from models.model_inference_engine import ModelInferenceEngine

        class TestModel(ModelInferenceEngine):
            """Test implementation."""

            def load_model(self, model_path: str, device: str = "cpu"):
                """Test implementation."""
                pass

            def predict(self, image, **kwargs):
                """Test implementation with progress."""
                self.progress.emit(25, "Preprocessing...")
                self.progress.emit(75, "Inferring...")
                self.progress.emit(100, "Done")

        engine = TestModel()

        with qtbot.waitSignal(engine.progress, timeout=1000) as blocker:
            engine.predict(None)

        assert blocker.args[0] >= 0
        assert blocker.args[0] <= 100
