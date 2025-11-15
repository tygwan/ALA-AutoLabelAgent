"""
Model Controller.

M3: Model Integration - Coordinates Florence-2 and SAM2 models for auto-annotation.
"""

import hashlib
from typing import Any, Dict, Optional

import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal

from models.florence2_model import Florence2Model
from models.sam2_model import SAM2Model


class ModelController(QObject):
    """
    Model controller that coordinates Florence-2 and SAM2 for auto-annotation.

    Workflow:
        1. Florence-2 detects objects with text prompt
        2. SAM2 refines detections into pixel-accurate masks
        3. Results cached and returned with progress updates

    Usage:
        controller = ModelController()
        controller.load_models(florence_path, sam_path)

        # Auto-annotate with text prompt
        results = controller.run_autodistill(image, "person, car, dog")

        # Monitor progress
        controller.progress.connect(update_progress_bar)
        controller.error.connect(show_error_dialog)
    """

    # Signals
    progress = pyqtSignal(int, str)  # (percentage, message)
    error = pyqtSignal(str)  # error message
    autodistill_complete = pyqtSignal(object)  # results
    cancelled = pyqtSignal()  # cancellation notification

    def __init__(self, parent: Optional[QObject] = None) -> None:
        """
        Initialize ModelController.

        Args:
            parent: Parent QObject (optional)
        """
        super().__init__(parent)

        # Initialize models
        self.florence2_model = Florence2Model(parent=self)
        self.sam2_model = SAM2Model(parent=self)

        # Connect model signals to controller signals
        self.florence2_model.progress.connect(self._forward_progress)
        self.florence2_model.error.connect(self._forward_error)
        self.sam2_model.progress.connect(self._forward_progress)
        self.sam2_model.error.connect(self._forward_error)

        # State
        self._is_cancelled = False
        self._cache: Dict[str, Any] = {}

    def load_models(
        self,
        florence_path: str,
        sam_path: str,
        device: str = "cpu",
    ) -> None:
        """
        Load both Florence-2 and SAM2 models.

        Args:
            florence_path: Path to Florence-2 checkpoint
            sam_path: Path to SAM2 checkpoint
            device: Device to load models on ("cpu", "cuda", "mps")

        Raises:
            RuntimeError: If model loading fails
        """
        self.progress.emit(0, "Loading models...")

        try:
            # Load Florence-2
            self.progress.emit(10, "Loading Florence-2...")
            self.florence2_model.load_model(florence_path, device=device)

            # Load SAM2
            self.progress.emit(50, "Loading SAM2...")
            self.sam2_model.load_model(sam_path, device=device)

            self.progress.emit(100, "Models loaded successfully")

        except Exception as e:
            error_msg = f"Failed to load models: {str(e)}"
            self.error.emit(error_msg)
            raise RuntimeError(error_msg) from e

    def run_autodistill(
        self,
        image: np.ndarray,
        text_prompt: str,
        confidence_threshold: float = 0.3,
        use_cache: bool = True,
    ) -> Optional[Dict[str, Any]]:
        """
        Run auto-annotation workflow: Florence-2 detection → SAM2 segmentation.

        Args:
            image: Input image (H, W, 3) in RGB format
            text_prompt: Text prompt for object detection (e.g., "person, car")
            confidence_threshold: Minimum confidence for detections
            use_cache: Whether to use cached results

        Returns:
            Dictionary containing:
                - detections: Florence-2 detection results (boxes, labels, scores)
                - masks: SAM2 segmentation masks for each detection
                - metadata: Additional information (prompt, confidence, etc.)

        Raises:
            RuntimeError: If models are not loaded or inference fails
        """
        # Check if cancelled
        if self._is_cancelled:
            self.progress.emit(0, "Operation cancelled")
            return None

        # Check if models are loaded
        if not self.florence2_model.is_model_loaded():
            error_msg = "Florence-2 model not loaded. Call load_models() first."
            self.error.emit(error_msg)
            raise RuntimeError(error_msg)

        if not self.sam2_model.is_model_loaded():
            error_msg = "SAM2 model not loaded. Call load_models() first."
            self.error.emit(error_msg)
            raise RuntimeError(error_msg)

        # Check cache
        if use_cache:
            cache_key = self._generate_cache_key(image, text_prompt)
            if cache_key in self._cache:
                self.progress.emit(100, "Retrieved from cache")
                cached_result = self._cache[cache_key]
                self.autodistill_complete.emit(cached_result)
                return cached_result

        try:
            self.progress.emit(10, "Starting auto-annotation...")

            # Step 1: Florence-2 object detection
            self.progress.emit(20, "Detecting objects with Florence-2...")
            detections = self.florence2_model.detect_objects(
                image, text_prompt, confidence_threshold
            )

            if self._is_cancelled:
                return None

            # Step 2: SAM2 segmentation for each detection
            self.progress.emit(50, "Refining masks with SAM2...")
            masks = []

            boxes = detections["boxes"]
            for i, box in enumerate(boxes):
                if self._is_cancelled:
                    return None

                # Update progress
                progress_pct = 50 + int((i / len(boxes)) * 40)
                self.progress.emit(
                    progress_pct, f"Segmenting object {i+1}/{len(boxes)}..."
                )

                # Run SAM2 with box prompt
                sam_result = self.sam2_model.predict(image, box=box)
                masks.append(sam_result["masks"][0])

            # Combine results
            result = {
                "detections": detections,
                "masks": masks,
                "metadata": {
                    "text_prompt": text_prompt,
                    "confidence_threshold": confidence_threshold,
                    "num_detections": len(boxes),
                },
            }

            # Cache result
            if use_cache:
                cache_key = self._generate_cache_key(image, text_prompt)
                self._cache[cache_key] = result

            self.progress.emit(100, "Auto-annotation complete")
            self.autodistill_complete.emit(result)

            return result

        except Exception as e:
            error_msg = f"Auto-annotation failed: {str(e)}"
            self.error.emit(error_msg)
            raise RuntimeError(error_msg) from e

    def cancel_inference(self) -> None:
        """
        Cancel ongoing inference operation.

        Sets cancellation flag and emits cancelled signal.
        """
        self._is_cancelled = True
        self.cancelled.emit()

    def clear_cache(self) -> None:
        """Clear the result cache."""
        self._cache.clear()

    def _generate_cache_key(self, image: np.ndarray, text_prompt: str) -> str:
        """
        Generate cache key from image and prompt.

        Args:
            image: Input image
            text_prompt: Text prompt

        Returns:
            Hash string for cache key
        """
        # Hash image data + prompt
        image_hash = hashlib.md5(image.tobytes()).hexdigest()
        prompt_hash = hashlib.md5(text_prompt.encode()).hexdigest()
        return f"{image_hash}_{prompt_hash}"

    def _forward_progress(self, percentage: int, message: str) -> None:
        """Forward progress signal from models."""
        self.progress.emit(percentage, message)

    def _forward_error(self, error_msg: str) -> None:
        """Forward error signal from models."""
        self.error.emit(error_msg)
