"""
Florence-2 Model Integration.

M3: Model Integration - Florence-2 for object detection and caption generation.
"""

from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor

from models.model_inference_engine import ModelInferenceEngine


class Florence2Model(ModelInferenceEngine):
    """
    Florence-2 model integration for object detection and vision-language tasks.

    Features:
    - Object detection with text prompts
    - Caption generation (brief and detailed)
    - Grounded detection with specific phrases
    - Batch processing for multiple images
    - Integration with SAM2 (bbox → mask conversion)
    - Progress tracking with signals

    Usage:
        model = Florence2Model()
        model.load_model("florence2_checkpoint", device="cuda")

        # Object detection
        result = model.detect_objects(image, "person, car, dog")

        # Caption generation
        caption = model.generate_caption(image)

        # Grounded detection
        result = model.grounded_detection(image, "red car")

        # Unified predict interface
        result = model.predict(image, task="detection", text_prompt="person")
    """

    def __init__(self, parent: Optional[Any] = None) -> None:
        """
        Initialize Florence-2 model.

        Args:
            parent: Parent QObject (optional)
        """
        super().__init__(parent)

        self.processor: Optional[Any] = None
        self.tokenizer: Optional[Any] = None

    def load_model(self, model_path: str, device: str = "cpu") -> None:
        """
        Load Florence-2 model from checkpoint.

        Args:
            model_path: Path to Florence-2 checkpoint or model name
                       (e.g., "microsoft/Florence-2-large" or local path)
            device: Device to load model on ("cpu", "cuda", "mps")

        Raises:
            RuntimeError: If model loading fails
        """
        self._emit_progress(10, "Loading Florence-2 model...")

        try:
            # Store device
            self.device = device

            # Use model_path or default to Florence-2-large
            if not model_path or model_path == "mock_checkpoint":
                model_path = "microsoft/Florence-2-large"

            self._emit_progress(30, f"Loading from {model_path}...")

            # Load processor
            self.processor = AutoProcessor.from_pretrained(
                model_path, trust_remote_code=True
            )

            self._emit_progress(60, "Loading model weights...")

            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path, trust_remote_code=True
            )

            # Move to device
            if device == "cuda" and torch.cuda.is_available():
                self.model = self.model.to("cuda")
            elif device == "mps" and torch.backends.mps.is_available():
                self.model = self.model.to("mps")
            else:
                self.model = self.model.to("cpu")
                if device != "cpu":
                    self._emit_progress(
                        80, f"Warning: {device} not available, using CPU"
                    )

            self.model.eval()
            self.model_path = model_path

            self._emit_progress(100, "Florence-2 model loaded")
            self.is_loaded = True
            self.model_loaded.emit()

        except Exception as e:
            error_msg = f"Failed to load Florence-2 model: {str(e)}"
            self._emit_error(error_msg)
            raise RuntimeError(error_msg) from e

    def predict(
        self,
        image: np.ndarray,
        task: str = "detection",
        text_prompt: Optional[str] = None,
        **kwargs,
    ) -> Union[Dict[str, Any], str]:
        """
        Run Florence-2 prediction (unified interface).

        Args:
            image: Input image as numpy array (H, W, 3) in RGB format
            task: Task type ("detection", "caption", "grounded")
            text_prompt: Text prompt for detection/grounding
            **kwargs: Additional task-specific arguments

        Returns:
            Task-dependent result:
                - detection: Dict with boxes, labels, scores
                - caption: String caption
                - grounded: Dict with boxes for specific phrases

        Raises:
            RuntimeError: If model is not loaded
            ValueError: If image or parameters are invalid
        """
        if not self.is_model_loaded():
            error_msg = "Model not loaded. Call load_model() first."
            self._emit_error(error_msg)
            raise RuntimeError(error_msg)

        if task == "detection":
            return self.detect_objects(image, text_prompt or "object", **kwargs)
        elif task == "caption":
            return {"caption": self.generate_caption(image, **kwargs)}
        elif task == "grounded":
            if not text_prompt:
                raise ValueError("text_prompt required for grounded detection")
            return self.grounded_detection(image, text_prompt, **kwargs)
        else:
            raise ValueError(f"Unknown task: {task}")

    def detect_objects(
        self, image: np.ndarray, text_prompt: str, confidence_threshold: float = 0.3
    ) -> Dict[str, Any]:
        """
        Detect objects in image based on text prompt.

        Args:
            image: Input image (H, W, 3) in RGB format
            text_prompt: Comma-separated list of object classes
                        e.g., "person, car, dog"
            confidence_threshold: Minimum confidence score (0.0-1.0)

        Returns:
            Dictionary containing:
                - boxes: List of bounding boxes [(x1, y1, x2, y2), ...]
                - labels: List of class labels for each box
                - scores: Confidence scores for each detection

        Raises:
            RuntimeError: If model is not loaded
            ValueError: If image is invalid
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
            # Convert numpy array to PIL Image
            if isinstance(image, np.ndarray):
                # Assume RGB format
                pil_image = Image.fromarray(image.astype("uint8"), "RGB")
            else:
                pil_image = image

            # Prepare Florence-2 prompt for caption to phrase grounding
            task_prompt = "<CAPTION_TO_PHRASE_GROUNDING>"
            prompt = task_prompt + text_prompt

            self._emit_progress(40, "Preparing inputs...")

            # Prepare inputs
            if self.processor is None:
                raise RuntimeError("Processor not initialized")

            inputs = self.processor(
                text=prompt, images=pil_image, return_tensors="pt"
            ).to(self.device)

            self._emit_progress(60, "Running object detection...")

            # Generate with Florence-2
            with torch.no_grad():
                generated_ids = self.model.generate(
                    input_ids=inputs["input_ids"],
                    pixel_values=inputs["pixel_values"],
                    max_new_tokens=1024,
                    early_stopping=False,
                    do_sample=False,
                    num_beams=3,
                )

            # Decode output
            generated_text = self.processor.batch_decode(
                generated_ids, skip_special_tokens=False
            )[0]

            self._emit_progress(80, "Post-processing...")

            # Parse results
            parsed_answer = self.processor.post_process_generation(
                generated_text,
                task=task_prompt,
                image_size=(pil_image.width, pil_image.height),
            )

            # Extract bounding boxes and labels
            boxes = []
            labels = []
            scores = []

            if "<CAPTION_TO_PHRASE_GROUNDING>" in parsed_answer:
                grounding_result = parsed_answer["<CAPTION_TO_PHRASE_GROUNDING>"]

                if "bboxes" in grounding_result and "labels" in grounding_result:
                    for bbox, label in zip(
                        grounding_result["bboxes"], grounding_result["labels"]
                    ):
                        # Convert bbox to (x1, y1, x2, y2) format
                        x1, y1, x2, y2 = bbox
                        boxes.append((int(x1), int(y1), int(x2), int(y2)))
                        labels.append(label)
                        # Florence-2 doesn't provide scores, use 1.0
                        scores.append(1.0)

            self._emit_progress(90, "Filtering results...")

            result = {
                "boxes": boxes,
                "labels": labels,
                "scores": scores,
            }

            self._emit_progress(100, "Detection complete")
            self.prediction_complete.emit(result)

            return result

        except Exception as e:
            error_msg = f"Detection failed: {str(e)}"
            self._emit_error(error_msg)
            raise RuntimeError(error_msg) from e

    def generate_caption(self, image: np.ndarray, detailed: bool = False) -> str:
        """
        Generate caption for image.

        Args:
            image: Input image (H, W, 3) in RGB format
            detailed: If True, generate detailed caption

        Returns:
            Generated caption as string

        Raises:
            RuntimeError: If model is not loaded
            ValueError: If image is invalid
        """
        if not self.is_model_loaded():
            error_msg = "Model not loaded. Call load_model() first."
            self._emit_error(error_msg)
            raise RuntimeError(error_msg)

        if image is None or image.size == 0:
            raise ValueError("Invalid image: image is None or empty")

        self._emit_progress(20, "Generating caption...")

        try:
            # Convert numpy array to PIL Image
            if isinstance(image, np.ndarray):
                pil_image = Image.fromarray(image.astype("uint8"), "RGB")
            else:
                pil_image = image

            # Choose task based on detailed flag
            task_prompt = "<DETAILED_CAPTION>" if detailed else "<CAPTION>"

            self._emit_progress(40, "Preparing inputs...")

            # Prepare inputs
            if self.processor is None:
                raise RuntimeError("Processor not initialized")

            inputs = self.processor(
                text=task_prompt, images=pil_image, return_tensors="pt"
            ).to(self.device)

            self._emit_progress(60, "Generating caption...")

            # Generate caption
            with torch.no_grad():
                generated_ids = self.model.generate(
                    input_ids=inputs["input_ids"],
                    pixel_values=inputs["pixel_values"],
                    max_new_tokens=1024,
                    early_stopping=False,
                    do_sample=False,
                    num_beams=3,
                )

            # Decode output
            generated_text = self.processor.batch_decode(
                generated_ids, skip_special_tokens=False
            )[0]

            self._emit_progress(80, "Processing caption...")

            # Parse results
            parsed_answer = self.processor.post_process_generation(
                generated_text,
                task=task_prompt,
                image_size=(pil_image.width, pil_image.height),
            )

            # Extract caption
            caption = parsed_answer.get(task_prompt, "")

            self._emit_progress(100, "Caption generated")
            self.prediction_complete.emit({"caption": caption})

            return caption

        except Exception as e:
            error_msg = f"Caption generation failed: {str(e)}"
            self._emit_error(error_msg)
            raise RuntimeError(error_msg) from e

    def grounded_detection(
        self, image: np.ndarray, phrase: str, confidence_threshold: float = 0.3
    ) -> Dict[str, Any]:
        """
        Detect objects based on specific phrase/description.

        Args:
            image: Input image (H, W, 3) in RGB format
            phrase: Specific phrase to ground (e.g., "red car", "person walking")
            confidence_threshold: Minimum confidence score

        Returns:
            Dictionary containing:
                - boxes: List of bounding boxes for phrase matches
                - scores: Confidence scores
                - phrase: The grounding phrase used

        Raises:
            RuntimeError: If model is not loaded
            ValueError: If image is invalid
        """
        if not self.is_model_loaded():
            error_msg = "Model not loaded. Call load_model() first."
            self._emit_error(error_msg)
            raise RuntimeError(error_msg)

        self._emit_progress(20, f"Grounding phrase: {phrase}...")

        try:
            # TODO: Replace with actual grounded detection
            # task = f"<GROUNDED_DETECTION>{phrase}"
            # Similar to detect_objects but with phrase grounding

            self._emit_progress(60, "Running grounded detection...")

            # Mock implementation
            h, w = image.shape[:2]
            num_matches = np.random.randint(1, 4)

            boxes = []
            scores = []

            for _ in range(num_matches):
                x1 = np.random.randint(0, w // 2)
                y1 = np.random.randint(0, h // 2)
                x2 = np.random.randint(x1 + 50, w)
                y2 = np.random.randint(y1 + 50, h)

                boxes.append((x1, y1, x2, y2))
                scores.append(np.random.uniform(confidence_threshold, 1.0))

            result = {
                "boxes": boxes,
                "scores": scores,
                "phrase": phrase,
            }

            self._emit_progress(100, "Grounding complete")
            self.prediction_complete.emit(result)

            return result

        except Exception as e:
            error_msg = f"Grounded detection failed: {str(e)}"
            self._emit_error(error_msg)
            raise RuntimeError(error_msg) from e

    def predict_batch(
        self,
        images: List[np.ndarray],
        text_prompt: str,
        task: str = "detection",
    ) -> List[Dict[str, Any]]:
        """
        Run batch prediction on multiple images.

        Args:
            images: List of input images
            text_prompt: Text prompt for detection/grounding
            task: Task type ("detection", "grounded")

        Returns:
            List of prediction results, one per image
        """
        results = []
        total = len(images)

        for i, image in enumerate(images):
            self._emit_progress(
                int((i / total) * 100), f"Processing image {i+1}/{total}..."
            )

            if task == "detection":
                result = self.detect_objects(image, text_prompt)
            elif task == "grounded":
                result = self.grounded_detection(image, text_prompt)
            else:
                raise ValueError(f"Unsupported batch task: {task}")

            results.append(result)

        return results

    def bbox_to_mask(
        self, boxes: List[Tuple[int, int, int, int]], image_shape: Tuple[int, int]
    ) -> List[np.ndarray]:
        """
        Convert bounding boxes to binary masks.

        This is a simple conversion for integration with SAM2.
        For better masks, use boxes as SAM2 prompts.

        Args:
            boxes: List of bounding boxes [(x1, y1, x2, y2), ...]
            image_shape: Image shape (height, width)

        Returns:
            List of binary masks, one per box
        """
        masks = []
        h, w = image_shape

        for box in boxes:
            x1, y1, x2, y2 = box

            # Create binary mask
            mask = np.zeros((h, w), dtype=np.uint8)
            mask[y1:y2, x1:x2] = 1

            masks.append(mask)

        return masks
