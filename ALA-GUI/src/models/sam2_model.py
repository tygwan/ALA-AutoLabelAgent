"""
SAM2 Model Integration.

M3: Model Integration - SAM2 for instance segmentation with point/box prompts.
"""

import os
import subprocess
import sys
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
import torch

from models.model_inference_engine import ModelInferenceEngine


class SAM2Model(ModelInferenceEngine):
    """
    SAM2 (Segment Anything Model 2) integration.

    Features:
    - Point-based prompting (foreground/background points)
    - Bounding box prompting
    - Multiple prompt refinement
    - Batch processing for multiple images
    - Mask post-processing (smoothing, polygon conversion)
    - Progress tracking with signals

    Usage:
        model = SAM2Model()
        model.load_model("sam2_checkpoint.pth", device="cuda")

        # Point prompts
        result = model.predict(image, points=[(x, y, 1)])

        # Box prompt
        result = model.predict(image, box=(x1, y1, x2, y2))

        # Multiple prompts for refinement
        result = model.predict(
            image,
            points=[(x1, y1, 1), (x2, y2, 1), (x3, y3, 0)]
        )
    """

    def __init__(self, parent: Optional[Any] = None) -> None:
        """
        Initialize SAM2 model.

        Args:
            parent: Parent QObject (optional)
        """
        super().__init__(parent)

        self.predictor: Optional[Any] = None
        self.image_embedding: Optional[np.ndarray] = None

    def load_model(self, model_path: str, device: str = "cpu") -> None:
        """
        Load SAM2 model from checkpoint.

        Args:
            model_path: Path to SAM2 checkpoint file or "auto" for auto-download
            device: Device to load model on ("cpu", "cuda", "mps")

        Raises:
            RuntimeError: If model loading fails
        """
        self._emit_progress(10, "Loading SAM2 model...")

        try:
            # Store device
            self.device = device

            # Auto-download SAM2 if needed
            if not model_path or model_path == "mock_checkpoint.pth":
                model_path = self._download_sam2_model()

            self._emit_progress(30, "Initializing SAM2...")

            # Add SAM2 to Python path
            self._setup_sam2_path()

            # Import SAM2 components
            from sam2.build_sam import build_sam2
            from sam2.sam2_image_predictor import SAM2ImagePredictor

            self._emit_progress(60, "Loading model weights...")

            # Build SAM2 model
            model_cfg = "sam2_hiera_b+.yaml"
            sam2_model = build_sam2(model_cfg, model_path)

            # Create predictor
            self.predictor = SAM2ImagePredictor(sam2_model)

            # Move to device
            if device == "cuda" and torch.cuda.is_available():
                self.predictor.model.to("cuda")
            elif device == "mps" and torch.backends.mps.is_available():
                self.predictor.model.to("mps")
            else:
                self.predictor.model.to("cpu")
                if device != "cpu":
                    self._emit_progress(
                        80, f"Warning: {device} not available, using CPU"
                    )

            self.model = self.predictor.model
            self.model_path = model_path

            self._emit_progress(100, "SAM2 model loaded")
            self.is_loaded = True
            self.model_loaded.emit()

        except Exception as e:
            error_msg = f"Failed to load SAM2 model: {str(e)}"
            self._emit_error(error_msg)
            raise RuntimeError(error_msg) from e

    def _download_sam2_model(self) -> str:
        """
        Download SAM2 model checkpoint if not exists.

        Returns:
            Path to SAM2 checkpoint
        """
        cache_dir = os.path.expanduser("~/.cache/autodistill")
        sam_cache_dir = os.path.join(cache_dir, "segment_anything_2")
        checkpoint_path = os.path.join(sam_cache_dir, "sam2_hiera_base_plus.pth")

        # Create directory
        os.makedirs(sam_cache_dir, exist_ok=True)

        # Download if not exists
        if not os.path.isfile(checkpoint_path):
            url = (
                "https://dl.fbaipublicfiles.com/segment_anything_2/"
                "072824/sam2_hiera_base_plus.pt"
            )
            self._emit_progress(20, "Downloading SAM2 checkpoint...")
            urllib.request.urlretrieve(url, checkpoint_path)

        return checkpoint_path

    def _setup_sam2_path(self) -> None:
        """Set up SAM2 repository path."""
        cache_dir = os.path.expanduser("~/.cache/autodistill")
        sam_cache_dir = os.path.join(cache_dir, "segment_anything_2")
        sam_repo_dir = os.path.join(sam_cache_dir, "segment-anything-2")

        # Clone SAM2 repository if not exists
        if not os.path.isdir(sam_repo_dir):
            self._emit_progress(15, "Cloning SAM2 repository...")
            os.makedirs(sam_cache_dir, exist_ok=True)

            cur_dir = os.getcwd()
            os.chdir(sam_cache_dir)

            subprocess.run(
                [
                    "git",
                    "clone",
                    "https://github.com/facebookresearch/segment-anything-2.git",
                ],
                check=True,
            )

            os.chdir(sam_repo_dir)
            subprocess.run(["pip", "install", "-e", "."], check=True)
            os.chdir(cur_dir)

        # Add to Python path
        if sam_repo_dir not in sys.path:
            sys.path.insert(0, sam_repo_dir)

    def predict(
        self,
        image: np.ndarray,
        points: Optional[List[Tuple[int, int, int]]] = None,
        box: Optional[Tuple[int, int, int, int]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Run SAM2 segmentation on image.

        Args:
            image: Input image as numpy array (H, W, 3) in RGB format
            points: List of point prompts [(x, y, label), ...]
                   where label=1 for foreground, label=0 for background
            box: Bounding box prompt (x1, y1, x2, y2)
            **kwargs: Additional arguments (multimask_output, etc.)

        Returns:
            Dictionary containing:
                - masks: List of binary masks (H, W) as numpy arrays
                - scores: Confidence scores for each mask
                - logits: Raw mask logits (optional)

        Raises:
            RuntimeError: If model is not loaded
            ValueError: If image or prompts are invalid
        """
        if not self.is_model_loaded():
            error_msg = "Model not loaded. Call load_model() first."
            self._emit_error(error_msg)
            raise RuntimeError(error_msg)

        if image is None or image.size == 0:
            raise ValueError("Invalid image: image is None or empty")

        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError(f"Invalid image shape: {image.shape}. Expected (H, W, 3)")

        self._emit_progress(20, "Preprocessing image...")

        try:
            # Ensure image is in RGB format
            if image.ndim == 3 and image.shape[2] == 3:
                # Convert RGB to BGR for SAM2 (expects BGR)
                image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            else:
                image_bgr = image

            # Set image for predictor
            self._emit_progress(40, "Generating image embeddings...")

            if self.predictor is None:
                raise RuntimeError("SAM2 predictor not initialized")

            self.predictor.set_image(image_bgr)

            # Prepare point prompts
            point_coords = None
            point_labels = None
            if points:
                point_coords = np.array([[p[0], p[1]] for p in points])
                point_labels = np.array([p[2] for p in points])

            # Prepare box prompt
            box_coords = None
            if box:
                box_coords = np.array(box)

            self._emit_progress(60, "Running SAM2 segmentation...")

            # Run SAM2 prediction
            with torch.inference_mode():
                if torch.cuda.is_available() and self.device == "cuda":
                    with torch.autocast("cuda", dtype=torch.bfloat16):
                        masks, scores, logits = self.predictor.predict(
                            point_coords=point_coords,
                            point_labels=point_labels,
                            box=box_coords,
                            multimask_output=kwargs.get("multimask_output", False),
                        )
                else:
                    masks, scores, logits = self.predictor.predict(
                        point_coords=point_coords,
                        point_labels=point_labels,
                        box=box_coords,
                        multimask_output=kwargs.get("multimask_output", False),
                    )

            self._emit_progress(80, "Post-processing masks...")

            # Convert to boolean masks
            masks = masks.astype(bool)

            # Select best mask if multiple
            if len(masks) > 1 and not kwargs.get("multimask_output", False):
                best_idx = np.argmax(scores)
                masks = [masks[best_idx]]
                scores = [scores[best_idx]]
            else:
                masks = list(masks)
                scores = list(scores)

            self._emit_progress(90, "Finalizing results...")

            result = {
                "masks": masks,
                "scores": scores,
            }

            self._emit_progress(100, "Segmentation complete")
            self.prediction_complete.emit(result)

            return result

        except Exception as e:
            error_msg = f"Prediction failed: {str(e)}"
            self._emit_error(error_msg)
            raise RuntimeError(error_msg) from e

    def predict_batch(
        self,
        images: List[np.ndarray],
        points: Optional[List[Tuple[int, int, int]]] = None,
        box: Optional[Tuple[int, int, int, int]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Run batch prediction on multiple images.

        Args:
            images: List of input images
            points: Point prompts (same for all images)
            box: Box prompt (same for all images)

        Returns:
            List of prediction results, one per image
        """
        results = []
        total = len(images)

        for i, image in enumerate(images):
            self._emit_progress(
                int((i / total) * 100), f"Processing image {i+1}/{total}..."
            )

            result = self.predict(image, points=points, box=box)
            results.append(result)

        return results

    def smooth_mask(
        self, mask: np.ndarray, kernel_size: int = 5, iterations: int = 2
    ) -> np.ndarray:
        """
        Smooth binary mask using morphological operations.

        Args:
            mask: Binary mask (H, W)
            kernel_size: Size of morphological kernel
            iterations: Number of iterations

        Returns:
            Smoothed binary mask
        """
        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (kernel_size, kernel_size)
        )

        # Close small holes
        closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=iterations)

        # Open to smooth boundaries
        opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel, iterations=iterations)

        return opened

    def mask_to_polygon(
        self, mask: np.ndarray, epsilon_factor: float = 0.001
    ) -> List[np.ndarray]:
        """
        Convert binary mask to polygon contours.

        Args:
            mask: Binary mask (H, W)
            epsilon_factor: Contour approximation factor (relative to perimeter)

        Returns:
            List of polygon contours as numpy arrays of shape (N, 2)
        """
        # Find contours
        contours, _ = cv2.findContours(
            mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        polygons = []
        for contour in contours:
            # Approximate contour
            epsilon = epsilon_factor * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Convert to (N, 2) format
            polygon = approx.reshape(-1, 2)

            # Keep only polygons with at least 3 points
            if len(polygon) >= 3:
                polygons.append(polygon)

        return polygons

    def refine_mask(
        self,
        image: np.ndarray,
        initial_mask: np.ndarray,
        positive_points: Optional[List[Tuple[int, int]]] = None,
        negative_points: Optional[List[Tuple[int, int]]] = None,
    ) -> Dict[str, Any]:
        """
        Refine existing mask with additional point prompts.

        Args:
            image: Input image
            initial_mask: Initial mask to refine
            positive_points: Additional foreground points
            negative_points: Additional background points

        Returns:
            Refined segmentation result
        """
        # Combine points
        points = []

        if positive_points:
            points.extend([(x, y, 1) for x, y in positive_points])

        if negative_points:
            points.extend([(x, y, 0) for x, y in negative_points])

        # Run prediction with combined prompts
        return self.predict(image, points=points)
