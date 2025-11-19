import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

router = APIRouter()

# TODO: Make this configurable
IMAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../testimage"))

class ImageInfo(BaseModel):
    filename: str
    path: str

@router.get("/", response_model=List[ImageInfo])
async def list_images():
    if not os.path.exists(IMAGE_DIR):
        return []
    
    images = []
    for filename in os.listdir(IMAGE_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            images.append(ImageInfo(
                filename=filename,
                path=f"/api/images/file/{filename}"
            ))
    return images

@router.get("/file/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(IMAGE_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)
