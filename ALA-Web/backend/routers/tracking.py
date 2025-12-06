from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime
import json

router = APIRouter()

# Data storage path
DATA_DIR = Path("data")
TRACKING_FILE = DATA_DIR / "tracking.json"

# Ensure data directory and file exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
if not TRACKING_FILE.exists():
    with open(TRACKING_FILE, 'w') as f:
        json.dump({}, f)


# ============================================================================
# Pydantic Models
# ============================================================================

class StageUpdate(BaseModel):
    image_id: str
    stage: str  # uploaded, annotated, preprocessed, classified
    status: str  # pending, processing, complete, error
    metadata: Optional[Dict[str, Any]] = None


# ============================================================================
# Helper Functions
# ============================================================================

def load_tracking() -> Dict:
    """Load tracking data"""
    try:
        with open(TRACKING_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_tracking(data: Dict):
    """Save tracking data"""
    with open(TRACKING_FILE, 'w') as f:
        json.dump(data, f, indent=2)


# ============================================================================
# Tracking Endpoints
# ============================================================================

@router.get("/status")
async def get_pipeline_status():
    """Get overall pipeline status"""
    tracking = load_tracking()
    
    stages = {
        "uploaded": 0,
        "annotated": 0,
        "preprocessed": 0,
        "classified": 0
    }
    
    for image_id, data in tracking.items():
        current_stage = data.get("current_stage", "uploaded")
        if current_stage in stages:
            stages[current_stage] += 1
    
    return {
        "stages": stages,
        "total_images": len(tracking)
    }


@router.get("/image/{image_id}")
async def get_image_history(image_id: str):
    """Get detailed history for single image"""
    tracking = load_tracking()
    
    if image_id not in tracking:
        raise HTTPException(status_code=404, detail=f"Image {image_id} not found in tracking")
    
    image_data = tracking[image_id]
    
    # Convert stages to history list
    history = []
    stages = image_data.get("stages", {})
    for stage_name, stage_data in stages.items():
        if stage_data:
            history.append({
                "stage": stage_name,
                "timestamp": stage_data.get("timestamp"),
                "status": stage_data.get("status"),
                "metadata": stage_data.get("metadata", {})
            })
    
    return {
        "image_id": image_id,
        "filename": image_data.get("filename"),
        "current_stage": image_data.get("current_stage"),
        "history": history,
        "errors": image_data.get("errors", [])
    }


@router.post("/update")
async def update_tracking(update: StageUpdate):
    """Update image status (called internally by other routers)"""
    tracking = load_tracking()
    
    # Initialize image tracking if not exists
    if update.image_id not in tracking:
        tracking[update.image_id] = {
            "filename": f"{update.image_id}.jpg",
            "stages": {},
            "current_stage": update.stage,
            "errors": []
        }
    
    # Update stage
    tracking[update.image_id]["stages"][update.stage] = {
        "timestamp": datetime.now().isoformat(),
        "status": update.status,
        "metadata": update.metadata or {}
    }
    
    # Update current stage if status is complete
    if update.status == "complete":
        tracking[update.image_id]["current_stage"] = update.stage
    
    # Add error if status is error
    if update.status == "error":
        error_entry = {
            "stage": update.stage,
            "error": update.metadata.get("error", "Unknown error") if update.metadata else "Unknown error",
            "timestamp": datetime.now().isoformat()
        }
        tracking[update.image_id]["errors"].append(error_entry)
    
    save_tracking(tracking)
    
    return {
        "message": f"Tracking updated for {update.image_id}",
        "image_id": update.image_id,
        "stage": update.stage,
        "status": update.status
    }


@router.get("/errors")
async def get_errors():
    """Get images with errors/failures"""
    tracking = load_tracking()
    
    errors = []
    for image_id, data in tracking.items():
        if data.get("errors"):
            errors.append({
                "image_id": image_id,
                "filename": data.get("filename"),
                "errors": data.get("errors"),
                "current_stage": data.get("current_stage")
            })
    
    return {
        "errors": errors,
        "total": len(errors)
    }


@router.post("/retry/{image_id}")
async def retry_failed(image_id: str):
    """Retry processing for a failed image"""
    tracking = load_tracking()
    
    if image_id not in tracking:
        raise HTTPException(status_code=404, detail=f"Image {image_id} not found in tracking")
    
    # Clear errors
    tracking[image_id]["errors"] = []
    
    # Reset current stage status to pending
    current_stage = tracking[image_id].get("current_stage", "uploaded")
    if current_stage in tracking[image_id].get("stages", {}):
        tracking[image_id]["stages"][current_stage]["status"] = "pending"
    
    save_tracking(tracking)
    
    return {
        "message": f"Retry initiated for {image_id}",
        "image_id": image_id,
        "stage": current_stage
    }
