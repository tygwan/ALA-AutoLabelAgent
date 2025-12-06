from __future__ import annotations
import os
import sys
import json
from typing import Dict, List, Optional, Any
from pathlib import Path

# Add local lib directory to sys.path
lib_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'lib'))
if os.path.exists(lib_path) and lib_path not in sys.path:
    sys.path.insert(0, lib_path)
    print(f"Added local lib to path: {lib_path}")

# Try to import AI libraries
AI_LIBS_AVAILABLE = False
_import_error = None

try:
    import cv2
    import numpy as np
    import torch
    import supervision as sv
    from autodistill.detection import CaptionOntology
    
    # Import our custom SAM2 loader
    from services.sam2_loader import get_sam2_predictor
    
    # Import Florence2 from autodistill
    from autodistill_florence_2 import Florence2
    
    AI_LIBS_AVAILABLE = True
    print("[OK] AI libraries loaded successfully from local lib")
except ImportError as e:
    _import_error = str(e)
    print(f"[WARN] AI libraries not available: {e}")
    # Continue without AI libs - will raise error when annotate is called

class AutoAnnotator:
    def __init__(self):
        self.florence2_model = None
        self.sam2_predictor = None
        self.current_ontology = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") if AI_LIBS_AVAILABLE else None

    def _ensure_models(self, ontology: Dict[str, str]):
        """
        Initialize or update models with new ontology.
        ontology format: { "prompt": "class_name" }
        Example: { "What blue fence?": "fence" }
        """
        if not AI_LIBS_AVAILABLE:
            raise ImportError(f"AI libraries not installed. Error: {_import_error}")

        # Check if ontology changed
        if self.florence2_model is None or self.current_ontology != ontology:
            print(f"Initializing models with ontology: {ontology}")
            
            # Create Caption Ontology for Florence2
            caption_ontology = CaptionOntology(ontology)
            
            # Initialize Florence2 for grounding
            self.florence2_model = Florence2(ontology=caption_ontology)
            
            # Load SAM2 predictor from local lib
            self.sam2_predictor = get_sam2_predictor()
            
            self.current_ontology = ontology
            print("✓ Models initialized successfully")

    def annotate(self, image_path: str, ontology: Dict[str, str], save_visualization: bool = False) -> Dict[str, Any]:
        """
        Run annotation on a single image.
        Uses Florence2 for object detection and SAM2 for segmentation.
        """
        if not AI_LIBS_AVAILABLE:
            raise ImportError(f"AI libraries not installed. Error: {_import_error}")

        self._ensure_models(ontology)
        
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")
        
        # Step 1: Use Florence2 to detect objects
        print(f"Running Florence2 detection on {image_path}")
        florence_detections = self.florence2_model.predict(image)
        
        # Step 2: Use SAM2 to refine segmentation
        print(f"Running SAM2 segmentation")
        with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
            self.sam2_predictor.set_image(image)
            
            result_masks = []
            for box in florence_detections.xyxy:
                masks, scores, _ = self.sam2_predictor.predict(
                    box=box,
                    multimask_output=False
                )
                index = np.argmax(scores)
                masks = masks.astype(bool)
                result_masks.append(masks[index])
        
        # Combine detections with refined masks
        florence_detections.mask = np.array(result_masks) if result_masks else None
        
        # Convert to serializable format
        boxes = florence_detections.xyxy.tolist() if hasattr(florence_detections.xyxy, 'tolist') else []
        masks = []
        
        if florence_detections.mask is not None:
            masks = [{"shape": list(m.shape)} for m in florence_detections.mask]

        classes = []
        if florence_detections.class_id is not None:
            caption_ontology = CaptionOntology(ontology)
            class_names = caption_ontology.classes()
            classes = [class_names[cid] for cid in florence_detections.class_id]

        scores = florence_detections.confidence.tolist() if florence_detections.confidence is not None else []

        # Save visualization if requested
        if save_visualization:
            self._save_visualization(image_path, florence_detections, classes)

        return {
            "boxes": boxes,
            "masks": masks,
            "classes": classes,
            "scores": scores,
            "count": len(boxes)
        }

    def _save_visualization(self, image_path: str, detections: sv.Detections, classes: List[str]):
        """Save annotated image for debugging/visualization"""
        try:
            image = cv2.imread(image_path)
            
            # Create annotators
            box_annotator = sv.BoxAnnotator()
            mask_annotator = sv.MaskAnnotator()
            label_annotator = sv.LabelAnnotator()

            # Generate labels
            labels = [
                f"{class_name} {confidence:.2f}"
                for class_name, confidence
                in zip(classes, detections.confidence)
            ] if detections.confidence is not None else classes

            # Annotate
            annotated_image = image.copy()
            if detections.mask is not None:
                annotated_image = mask_annotator.annotate(scene=annotated_image, detections=detections)
            annotated_image = box_annotator.annotate(scene=annotated_image, detections=detections)
            annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections, labels=labels)

            # Save
            output_path = image_path.replace(".", "_annotated.")
            cv2.imwrite(output_path, annotated_image)
            print(f"✓ Saved visualization to {output_path}")
            
        except Exception as e:
            print(f"✗ Failed to save visualization: {e}")

# Global instance
auto_annotator = AutoAnnotator()
