from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from pathlib import Path

try:
    from services.auto_annotator import auto_annotator
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    auto_annotator = None

from services.asset_registry import asset_registry

router = APIRouter()

class AnnotationRequest(BaseModel):
    file_id: str
    ontology: Dict[str, str]  # {"prompt": "class_name"}
    save_visualization: bool = False

class AnnotationResponse(BaseModel):
    file_id: str
    boxes: List[List[float]]
    masks: List[List[List[bool]]]
    classes: List[str]
    scores: List[float]
    count: int

@router.post("/auto-annotate", response_model=AnnotationResponse)
async def auto_annotate(request: AnnotationRequest):
    """
    Automatic annotation using Florence-2 + SAM2
    
    Example request:
    {
        "file_id": "abc123",
        "ontology": {
            "person": "person",
            "car": "vehicle",
            "dog": "animal"
        },
        "save_visualization": true
    }
    """
    if not AI_AVAILABLE:
        raise HTTPException(
            503,
            "AI models not available. Please run 'backend/setup_ai_env.bat' to install dependencies."
        )
    
    try:
        # Get image path
        image_path = asset_registry.get_asset_path(request.file_id)
        
        if not image_path or not Path(image_path).exists():
            raise HTTPException(404, f"Image not found: {request.file_id}")
        
        # Run annotation
        result = auto_annotator.annotate(
            image_path=image_path,
            ontology=request.ontology,
            save_visualization=request.save_visualization
        )
        
        return AnnotationResponse(
            file_id=request.file_id,
            boxes=result["boxes"],
            masks=result["masks"],
            classes=result["classes"],
            scores=result["scores"],
            count=len(result["boxes"])
        )
        
    except Exception as e:
        raise HTTPException(500, f"Annotation failed: {str(e)}")

@router.get("/models/status")
async def get_model_status():
    """Check if models are loaded"""
    from services.model_loader import model_loader
    from config.model_config import SAM2_CHECKPOINT
    
    return {
        "florence2_loaded": model_loader.florence2_model is not None,
        "sam2_loaded": model_loader.sam2_predictor is not None,
        "device": model_loader.device,
        "sam2_checkpoint_exists": SAM2_CHECKPOINT.exists()
    }

@router.post("/models/unload")
async def unload_models():
    """Free up GPU/RAM"""
    from services.model_loader import model_loader
    model_loader.unload_models()
    return {"status": "models unloaded"}

# Keep old detect/segment endpoints for compatibility
class BoundingBox(BaseModel):
    x: float
    y: float
    width: float
    height: float
    label: str
    score: float

class DetectionRequest(BaseModel):
    image_name: str
    prompt: str

class SegmentationRequest(BaseModel):
    image_name: str
    box: Optional[BoundingBox] = None
    point: Optional[List[float]] = None  # [x, y]

@router.post("/detect", response_model=List[BoundingBox])
async def detect_objects(request: DetectionRequest):
    """Legacy endpoint - use /auto-annotate instead"""
    # Mock response for now
    return [
        BoundingBox(x=100, y=100, width=200, height=200, label=request.prompt, score=0.95)
    ]

@router.post("/segment", response_model=Dict[str, Any])
async def segment_object(request: SegmentationRequest):
    """Legacy endpoint - use /auto-annotate instead"""
    # Mock response
    return {"mask": "mock_rle_data"}
