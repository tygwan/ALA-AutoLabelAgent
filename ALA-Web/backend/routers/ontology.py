from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import os
import uuid
from datetime import datetime
from pathlib import Path

router = APIRouter()

# Path to ontologies database
ONTOLOGIES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ontologies.json")

class OntologyCreate(BaseModel):
    name: str
    description: str = ""
    classes: Dict[str, str]  # {"prompt": "class_name"}

class OntologyResponse(BaseModel):
    ontology_id: str
    name: str
    description: str
    classes: Dict[str, str]
    created_at: str
    class_count: int

class OntologyListItem(BaseModel):
    ontology_id: str
    name: str
    description: str
    class_count: int
    created_at: str

def _load_ontologies() -> Dict:
    """Load ontologies from JSON file"""
    if not os.path.exists(ONTOLOGIES_FILE):
        # Create file if it doesn't exist
        os.makedirs(os.path.dirname(ONTOLOGIES_FILE), exist_ok=True)
        with open(ONTOLOGIES_FILE, 'w') as f:
            json.dump({"ontologies": []}, f, indent=2)
        return {"ontologies": []}
    
    try:
        with open(ONTOLOGIES_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"ontologies": []}

def _save_ontologies(data: Dict):
    """Save ontologies to JSON file"""
    with open(ONTOLOGIES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@router.post("/save", response_model=Dict[str, str])
async def save_ontology(ontology: OntologyCreate):
    """Save a new ontology"""
    try:
        data = _load_ontologies()
        
        ontology_id = f"ont_{uuid.uuid4().hex[:12]}"
        
        new_ontology = {
            "ontology_id": ontology_id,
            "name": ontology.name,
            "description": ontology.description,
            "classes": ontology.classes,
            "created_at": datetime.now().isoformat(),
            "class_count": len(ontology.classes)
        }
        
        data["ontologies"].append(new_ontology)
        _save_ontologies(data)
        
        return {
            "ontology_id": ontology_id,
            "message": "Ontology saved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list", response_model=Dict[str, List[OntologyListItem]])
async def list_ontologies():
    """List all saved ontologies"""
    try:
        data = _load_ontologies()
        
        ontologies = [
            OntologyListItem(
                ontology_id=ont["ontology_id"],
                name=ont["name"],
                description=ont.get("description", ""),
                class_count=ont.get("class_count", len(ont.get("classes", {}))),
                created_at=ont["created_at"]
            )
            for ont in data["ontologies"]
        ]
        
        return {"ontologies": ontologies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{ontology_id}", response_model=OntologyResponse)
async def get_ontology(ontology_id: str):
    """Get a specific ontology by ID"""
    try:
        data = _load_ontologies()
        
        ontology = next(
            (ont for ont in data["ontologies"] if ont["ontology_id"] == ontology_id),
            None
        )
        
        if not ontology:
            raise HTTPException(status_code=404, detail="Ontology not found")
        
        return OntologyResponse(
            ontology_id=ontology["ontology_id"],
            name=ontology["name"],
            description=ontology.get("description", ""),
            classes=ontology["classes"],
            created_at=ontology["created_at"],
            class_count=len(ontology["classes"])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{ontology_id}", response_model=Dict[str, str])
async def delete_ontology(ontology_id: str):
    """Delete an ontology"""
    try:
        data = _load_ontologies()
        
        original_count = len(data["ontologies"])
        data["ontologies"] = [
            ont for ont in data["ontologies"]
            if ont["ontology_id"] != ontology_id
        ]
        
        if len(data["ontologies"]) == original_count:
            raise HTTPException(status_code=404, detail="Ontology not found")
        
        _save_ontologies(data)
        
        return {"message": "Ontology deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
