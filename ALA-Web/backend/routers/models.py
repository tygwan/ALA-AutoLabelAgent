from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

# Import from ALA-GUI
try:
    from models.model_manager import ModelManager
except ImportError:
    # Mock for now if import fails during dev
    class ModelManager:
        def __init__(self): pass
        def check_model_status(self): return {"florence2": False, "sam2": False}

router = APIRouter()
model_manager = ModelManager()

class ModelStatus(BaseModel):
    florence2: bool
    sam2: bool

@router.get("/status", response_model=ModelStatus)
async def get_model_status():
    status = model_manager.check_model_status()
    # Adapt the return format if necessary, assuming the method returns a dict
    return ModelStatus(
        florence2=status.get("florence2", False),
        sam2=status.get("sam2", False)
    )

@router.post("/download/{model_name}")
async def download_model(model_name: str):
    # TODO: Implement async download task
    return {"message": f"Download started for {model_name}"}
