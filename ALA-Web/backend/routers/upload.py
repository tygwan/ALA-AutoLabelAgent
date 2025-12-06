from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from typing import List, Optional
import shutil
import os
import uuid
from datetime import datetime
import json
from pathlib import Path
from services.asset_registry import asset_registry

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "uploads")
PROJECTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "projects.json")

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/file")
async def upload_file(
    file: UploadFile = File(...),
    project_id: Optional[str] = Form(None),
    original_path: Optional[str] = Form(None) # For preserving folder structure
):
    try:
        # Generate unique file ID
        file_id = f"file_{uuid.uuid4().hex[:12]}"
        
        # Determine save path
        if project_id:
            # Get project name for folder structure
            with open(PROJECTS_FILE, 'r') as f:
                projects_data = json.load(f)
                project = next((p for p in projects_data["projects"] if p["project_id"] == project_id), None)
                
            if project:
                project_dir = os.path.join(UPLOAD_DIR, project["name"])
                
                # Handle nested folders if original_path is provided
                if original_path:
                    # original_path usually comes as "folder/subfolder/file.jpg"
                    # We want to keep the structure inside the project folder
                    rel_dir = os.path.dirname(original_path)
                    save_dir = os.path.join(project_dir, rel_dir)
                else:
                    save_dir = project_dir
                    
                os.makedirs(save_dir, exist_ok=True)
                file_path = os.path.join(save_dir, file.filename)
                
                # Relative path for storage
                relative_path = os.path.relpath(file_path, os.path.dirname(os.path.dirname(__file__)))
            else:
                # Fallback if project not found
                file_path = os.path.join(UPLOAD_DIR, file.filename)
                relative_path = os.path.join("data/uploads", file.filename)
        else:
            # No project specified
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            relative_path = os.path.join("data/uploads", file.filename)
            
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Register in Asset Registry
        if project_id:
            asset_registry.register_managed_file(
                file_id=file_id,
                project_id=project_id,
                relative_path=relative_path,
                original_filename=file.filename
            )
            
            # Update project file count
            with open(PROJECTS_FILE, 'r+') as f:
                data = json.load(f)
                for p in data["projects"]:
                    if p["project_id"] == project_id:
                        p["file_count"] = p.get("file_count", 0) + 1
                        break
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "path": relative_path,
            "project_id": project_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch")
async def upload_batch(
    files: List[UploadFile] = File(...),
    project_id: Optional[str] = Form(None)
):
    results = []
    try:
        project = None
        project_dir = None
        
        if project_id:
             with open(PROJECTS_FILE, 'r') as f:
                projects_data = json.load(f)
                project = next((p for p in projects_data["projects"] if p["project_id"] == project_id), None)
             
             if project:
                project_dir = os.path.join(UPLOAD_DIR, project["name"])
                os.makedirs(project_dir, exist_ok=True)

        for file in files:
            file_id = f"file_{uuid.uuid4().hex[:12]}"
            
            if project and project_dir:
                 file_path = os.path.join(project_dir, file.filename)
                 # Calculate relative path from backend root
                 # os.path.dirname(os.path.dirname(__file__)) gives backend/
                 backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                 relative_path = os.path.relpath(file_path, backend_root)
            else:
                 file_path = os.path.join(UPLOAD_DIR, file.filename)
                 relative_path = os.path.join("data/uploads", file.filename)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
                
            if project_id:
                asset_registry.register_managed_file(
                    file_id=file_id,
                    project_id=project_id,
                    relative_path=relative_path,
                    original_filename=file.filename
                )
            
            results.append({
                "file_id": file_id,
                "filename": file.filename,
                "path": relative_path,
                "project_id": project_id
            })
            
        if project_id and results:
             with open(PROJECTS_FILE, 'r+') as f:
                data = json.load(f)
                for p in data["projects"]:
                    if p["project_id"] == project_id:
                        p["file_count"] = p.get("file_count", 0) + len(results)
                        break
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()

        return {"uploaded": results, "count": len(results)}

    except Exception as e:
        print(f"Batch upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_files(project_id: Optional[str] = None):
    """List files using the Asset Registry"""
    try:
        if project_id:
            assets = asset_registry.get_project_assets(project_id)
            return assets
        else:
            # Fallback for legacy behavior (list all managed files)
            # This is less efficient but keeps compatibility
            assets = asset_registry._load_assets()
            return list(assets.values())
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/file/{file_id}")
async def get_file(file_id: str):
    """Get file content by ID (supports both managed and linked files)"""
    file_path = asset_registry.get_asset_path(file_id)
    
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
        
    return FileResponse(file_path)
