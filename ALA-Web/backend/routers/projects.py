from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Optional
from pydantic import BaseModel
import json
import os
import uuid
from datetime import datetime
from services.asset_registry import asset_registry

router = APIRouter()

PROJECTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "projects.json")

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    ontology: Optional[Dict[str, str]] = {}

class Project(BaseModel):
    project_id: str
    name: str
    display_name: str
    description: Optional[str] = None
    created_at: str
    file_count: int = 0
    ontology: Dict[str, str] = {}
    linked_roots: Optional[List[Dict]] = []

class LinkFolderRequest(BaseModel):
    folder_path: str

def load_projects():
    if not os.path.exists(PROJECTS_FILE):
        return []
    try:
        with open(PROJECTS_FILE, 'r') as f:
            data = json.load(f)
            return data.get("projects", [])
    except json.JSONDecodeError:
        return []

def save_projects(projects):
    with open(PROJECTS_FILE, 'w') as f:
        json.dump({"projects": projects}, f, indent=2)

@router.get("/list", response_model=List[Project])
async def list_projects():
    return load_projects()

@router.post("/create", response_model=Project)
async def create_project(project: ProjectCreate):
    projects = load_projects()
    
    # Check for duplicates
    if any(p["name"] == project.name for p in projects):
        raise HTTPException(status_code=400, detail="Project with this name already exists")
    
    new_project = {
        "project_id": f"proj_{uuid.uuid4().hex[:8]}",
        "name": project.name,
        "display_name": project.name, # Can be different in future
        "description": project.description,
        "created_at": datetime.now().isoformat(),
        "file_count": 0,
        "ontology": project.ontology or {},
        "linked_roots": []
    }
    
    projects.append(new_project)
    save_projects(projects)
    return new_project

@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: str):
    projects = load_projects()
    project = next((p for p in projects if p["project_id"] == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}/ontology")
async def update_ontology(project_id: str, ontology: Dict[str, str] = Body(...)):
    projects = load_projects()
    project = next((p for p in projects if p["project_id"] == project_id), None)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    project["ontology"] = ontology
    save_projects(projects)
    
    return {"status": "success", "ontology": ontology}

@router.post("/{project_id}/link-folder")
async def link_folder(project_id: str, request: LinkFolderRequest):
    """Link an external folder to the project"""
    try:
        result = asset_registry.link_external_folder(project_id, request.folder_path)
        return {
            "status": "success",
            "message": f"Successfully linked folder. Added {result['added_count']} files.",
            "details": result
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Folder not found: {request.folder_path}")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to link folder: {str(e)}")

@router.delete("/{project_id}")
async def delete_project(project_id: str, delete_files: bool = False):
    projects = load_projects()
    project = next((p for p in projects if p["project_id"] == project_id), None)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Remove from list
    projects = [p for p in projects if p["project_id"] != project_id]
    save_projects(projects)
    
    # Optional: Delete files (not implemented fully here, but placeholder)
    if delete_files:
        # Logic to delete files from disk/registry would go here
        pass
        
    return {"status": "success", "message": f"Project {project_id} deleted"}
