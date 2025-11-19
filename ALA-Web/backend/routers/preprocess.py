from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Tuple
import sys
import os

# Add services to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.preprocessor import (
    decode_base64_image,
    encode_image_to_base64,
    create_mask_from_polygon,
    preprocess_image
)

router = APIRouter()


class PreprocessRequest(BaseModel):
    image_data: str  # Base64 encoded image
    box: Optional[Tuple[int, int, int, int]] = None
    polygon_coords: Optional[List[float]] = None  # Normalized polygon coordinates
    bg_mode: str = "black"  # black, white, gray, transparent, blur, mean
    target_size: Tuple[int, int] = (640, 480)  # (width, height)
    padding: int = 0


class PreprocessResponse(BaseModel):
    processed_image: str  # Base64 encoded
    metadata: dict


@router.post("/single", response_model=PreprocessResponse)
async def preprocess_single(request: PreprocessRequest):
    """
    Preprocess a single image with optional box cropping and mask application
    """
    try:
        # Decode input image
        image = decode_base64_image(request.image_data)
        
        # Create mask from polygon if provided
        mask = None
        if request.polygon_coords:
            mask = create_mask_from_polygon(
                image.shape[:2],
                request.polygon_coords
            )
        
        # Preprocess
        processed = preprocess_image(
            image,
            box=request.box,
            mask=mask,
            bg_mode=request.bg_mode,
            target_size=request.target_size,
            padding=request.padding
        )
        
        # Encode output
        output_data = encode_image_to_base64(processed)
        
        return PreprocessResponse(
            processed_image=f"data:image/png;base64,{output_data}",
            metadata={
                "input_size": image.shape[:2],
                "output_size": processed.shape[:2],
                "bg_mode": request.bg_mode,
                "has_mask": mask is not None,
                "has_box": request.box is not None
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preprocessing failed: {str(e)}")


class BatchPreprocessRequest(BaseModel):
    images: List[PreprocessRequest]


@router.post("/batch")
async def preprocess_batch(request: BatchPreprocessRequest):
    """
    Preprocess multiple images
    """
    results = []
    errors = []
    
    for idx, img_request in enumerate(request.images):
        try:
            result = await preprocess_single(img_request)
            results.append(result)
        except Exception as e:
            errors.append({
                "index": idx,
                "error": str(e)
            })
    
    return {
        "results": results,
        "errors": errors,
        "total": len(request.images),
        "successful": len(results),
        "failed": len(errors)
    }
