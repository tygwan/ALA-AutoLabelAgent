from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from typing import List
import os
import shutil
from pathlib import Path
import uuid
from datetime import datetime

router = APIRouter()

# Configuration
UPLOAD_DIR = Path("data/uploads")
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_VIDEO_EXTENSIONS

# Ensure upload directory exists
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/file")
async def upload_file(file: UploadFile = File(...)):
    """Upload a single image or video file"""
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    safe_filename = f"{file_id}{file_ext}"
    file_path = UPLOAD_DIR / safe_filename
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Determine file type
    file_type = "image" if file_ext in ALLOWED_IMAGE_EXTENSIONS else "video"
    
    return {
        "file_id": file_id,
        "filename": file.filename,
        "stored_filename": safe_filename,
        "file_type": file_type,
        "size": file_path.stat().st_size,
        "uploaded_at": datetime.now().isoformat()
    }

@router.post("/batch")
async def upload_batch(files: List[UploadFile] = File(...)):
    """Upload multiple files at once"""
    results = []
    errors = []
    
    for file in files:
        try:
            result = await upload_file(file)
            results.append(result)
        except Exception as e:
            errors.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {
        "uploaded": results,
        "errors": errors,
        "total": len(files),
        "successful": len(results),
        "failed": len(errors)
    }

@router.get("/list")
async def list_uploads():
    """List all uploaded files"""
    files = []
    
    for file_path in UPLOAD_DIR.iterdir():
        if file_path.is_file():
            file_ext = file_path.suffix.lower()
            file_type = "image" if file_ext in ALLOWED_IMAGE_EXTENSIONS else "video"
            
            files.append({
                "file_id": file_path.stem,
                "filename": file_path.name,
                "file_type": file_type,
                "size": file_path.stat().st_size,
                "uploaded_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            })
    
    return {"files": files, "total": len(files)}

@router.delete("/{file_id}")
async def delete_file(file_id: str):
    """Delete an uploaded file"""
    # Find file with matching ID (any extension)
    deleted = False
    for file_path in UPLOAD_DIR.iterdir():
        if file_path.stem == file_id:
            try:
                file_path.unlink()
                deleted = True
                break
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")
    
    if not deleted:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {"message": "File deleted successfully", "file_id": file_id}

@router.get("/file/{file_id}")
async def get_file(file_id: str):
    """Get a specific uploaded file"""
    for file_path in UPLOAD_DIR.iterdir():
        if file_path.stem == file_id:
            return FileResponse(file_path)
    
    raise HTTPException(status_code=404, detail="File not found")
