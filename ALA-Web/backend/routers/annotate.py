from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

router = APIRouter()

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
    point: Optional[List[float]] = None # [x, y]

@router.post("/detect", response_model=List[BoundingBox])
async def detect_objects(request: DetectionRequest):
    # TODO: Integrate Florence-2
    # Mock response
    return [
        BoundingBox(x=100, y=100, width=200, height=200, label=request.prompt, score=0.95)
    ]

@router.post("/segment", response_model=Dict[str, Any])
async def segment_object(request: SegmentationRequest):
    # TODO: Integrate SAM2
    # Mock response (RLE or Polygon)
    return {"mask": "mock_rle_data"}
