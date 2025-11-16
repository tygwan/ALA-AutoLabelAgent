"""
Model Inference Engine Base Class.

M3: Model Integration - Abstract base for SAM2, Florence-2, and other models.
"""

from abc import ABCMeta, abstractmethod
from typing import Any, Optional

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.sip import wrappertype


# Create a compatible metaclass that combines QObject and ABC
class QABCMeta(wrappertype, ABCMeta):
    """Metaclass that combines Qt's wrappertype with ABCMeta."""

    pass


class ModelInferenceEngine(QObject, metaclass=QABCMeta):
    """
    Abstract base class for model inference engines.

    Features:
    - PyQt6 signals for progress and error reporting
    - Abstract methods for model loading and prediction
    - Device selection (CPU, CUDA, MPS)
    - Model caching and lifecycle management
    - Thread-safe operation with QThread integration

    Signals:
        model_loaded: Emitted when model is successfully loaded
        progress: Emitted during operations (value: int 0-100, message: str)
        error: Emitted when an error occurs (error_message: str)
        prediction_complete: Emitted when prediction is done (result: Any)

    Subclasses must implement:
        - load_model(model_path, device): Load model from checkpoint
        - predict(image, **kwargs): Run inference on image
    """

    # Signals
    model_loaded = pyqtSignal()
    progress = pyqtSignal(int, str)  # (percentage, message)
    error = pyqtSignal(str)  # (error_message)
    prediction_complete = pyqtSignal(object)  # (result)

    def __init__(self, parent: Optional[QObject] = None) -> None:
        """
        Initialize the model inference engine.

        Args:
            parent: Parent QObject (optional)
        """
        super().__init__(parent)

        self.model: Optional[Any] = None
        self.device: str = "cpu"
        self.is_loaded: bool = False
        self.model_path: Optional[str] = None

    @abstractmethod
    def load_model(self, model_path: str, device: str = "cpu") -> None:
        """
        Load model from checkpoint.

        Args:
            model_path: Path to model checkpoint file
            device: Device to load model on ("cpu", "cuda", "mps")

        Raises:
            FileNotFoundError: If model file doesn't exist
            RuntimeError: If model loading fails
        """
        pass

    @abstractmethod
    def predict(self, image: Any, **kwargs) -> Any:
        """
        Run inference on an image.

        Args:
            image: Input image (format depends on model)
            **kwargs: Additional model-specific parameters

        Returns:
            Prediction result (format depends on model)

        Raises:
            RuntimeError: If model is not loaded
            ValueError: If input is invalid
        """
        pass

    def unload_model(self) -> None:
        """
        Unload the model to free memory.

        This method clears the model from memory and resets the engine state.
        Useful for switching between models or freeing resources.
        """
        self.model = None
        self.is_loaded = False
        self.model_path = None
        self.progress.emit(100, "Model unloaded")

    def is_model_loaded(self) -> bool:
        """
        Check if model is loaded and ready for inference.

        Returns:
            True if model is loaded, False otherwise
        """
        return self.is_loaded and self.model is not None

    def get_device(self) -> str:
        """
        Get the current device being used.

        Returns:
            Device string ("cpu", "cuda", "mps")
        """
        return self.device

    def _emit_progress(self, percentage: int, message: str) -> None:
        """
        Emit progress signal with percentage and message.

        Args:
            percentage: Progress percentage (0-100)
            message: Progress message
        """
        # Clamp percentage to valid range
        percentage = max(0, min(100, percentage))
        self.progress.emit(percentage, message)

    def _emit_error(self, error_message: str) -> None:
        """
        Emit error signal with error message.

        Args:
            error_message: Error description
        """
        self.error.emit(error_message)
        self.is_loaded = False
