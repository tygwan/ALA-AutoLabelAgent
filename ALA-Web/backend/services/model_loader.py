"""
Simplified Model Loader using autodistill-grounded-sam-2
This eliminates the need for manual SAM2 installation!
"""

from __future__ import annotations

from typing import Optional, Dict

# Optional AI imports
try:
    from autodistill_grounded_sam_2 import GroundedSAM2
    from autodistill.detection import CaptionOntology
    import torch
    AI_AVAILABLE = True
except ImportError as e:
    AI_AVAILABLE = False
    _import_error = str(e)
    GroundedSAM2 = None
    CaptionOntology = None
    torch = None

class ModelLoader:
    """
    Simplified model loader using GroundedSAM2
    No need to separately load Florence-2 and SAM2!
    """
    
    def __init__(self):
        self.model = None
        self._ontology = None
        if AI_AVAILABLE:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"[ModelLoader] Initialized on device: {self.device}")
        else:
            self.device = "cpu"
            print(f"[ModelLoader] AI libraries not available: {_import_error}")
    
    def load_model(self, ontology: Dict[str, str]) -> Optional[GroundedSAM2]:
        """
        Load GroundedSAM2 model with ontology
        
        Args:
            ontology: Dict mapping prompts to class names
                Example: {"person": "person", "car": "car"}
        
        Returns:
            GroundedSAM2 model instance
        """
        if not AI_AVAILABLE:
            raise ImportError(
                f"AI libraries not available: {_import_error}\n"
                "Install with: pip install -r requirements_ai.txt"
            )
        
        # Reload if ontology changed
        if self.model is None or self._ontology != ontology:
            print(f"[GroundedSAM2] Loading model with ontology...")
            print(f"[GroundedSAM2] Classes: {list(ontology.keys())}")
            
            caption_ontology = CaptionOntology(ontology)
            self.model = GroundedSAM2(ontology=caption_ontology)
            self._ontology = ontology
            
            print("[GroundedSAM2] Model loaded successfully!")
        else:
            print("[GroundedSAM2] Using cached model")
        
        return self.model
    
    def unload_model(self):
        """Free up memory"""
        print("[ModelLoader] Unloading model...")
        self.model = None
        self._ontology = None
        
        if AI_AVAILABLE and torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("[ModelLoader] CUDA cache cleared")
        
        print("[ModelLoader] Model unloaded")

# Global instance
model_loader = ModelLoader()
