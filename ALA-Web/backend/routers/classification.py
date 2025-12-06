from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime
import json
import uuid

router = APIRouter()

# Data storage paths
DATA_DIR = Path("data")
EXPERIMENTS_FILE = DATA_DIR / "experiments.json"
SUPPORT_SETS_FILE = DATA_DIR / "support_sets.json"
QUERY_SETS_FILE = DATA_DIR / "query_sets.json"
EXPERIMENT_RESULTS_FILE = DATA_DIR / "experiment_results.json"
ANNOTATIONS_FILE = DATA_DIR / "annotations.json"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Initialize JSON files if they don't exist
for file_path in [EXPERIMENTS_FILE, SUPPORT_SETS_FILE, QUERY_SETS_FILE, 
                  EXPERIMENT_RESULTS_FILE, ANNOTATIONS_FILE]:
    if not file_path.exists():
        with open(file_path, 'w') as f:
            json.dump({}, f)


# ============================================================================
# Pydantic Models
# ============================================================================

class ExperimentCreate(BaseModel):
    name: str
    support_set_id: str
    query_set_id: str
    method: str = "cosine_similarity"
    threshold: Optional[float] = 0.7
    parent_experiment: Optional[str] = None
    notes: Optional[str] = None


class SupportSetCreate(BaseModel):
    name: str
    classes: Dict[str, List[str]]  # {class_id: [image_ids]}
    parent_version: Optional[str] = None


class QuerySetCreate(BaseModel):
    name: str
    image_ids: List[str]


class AnnotateRequest(BaseModel):
    image_ids: List[str]
    classes: List[str]


class ExportRequest(BaseModel):
    format: str = "folders"  # folders, csv, json


# ============================================================================
# Helper Functions
# ============================================================================

def load_json(file_path: Path) -> Dict:
    """Load JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_json(file_path: Path, data: Dict):
    """Save JSON file"""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


# ============================================================================
# Experiment Management Endpoints
# ============================================================================

@router.post("/experiment/create")
async def create_experiment(experiment: ExperimentCreate):
    """Create a new classification experiment"""
    experiments = load_json(EXPERIMENTS_FILE)
    
    # Generate experiment ID
    exp_id = f"exp_{str(uuid.uuid4())[:8]}"
    
    # Verify support set and query set exist
    support_sets = load_json(SUPPORT_SETS_FILE)
    query_sets = load_json(QUERY_SETS_FILE)
    
    if experiment.support_set_id not in support_sets:
        raise HTTPException(status_code=404, detail=f"Support set {experiment.support_set_id} not found")
    
    if experiment.query_set_id not in query_sets:
        raise HTTPException(status_code=404, detail=f"Query set {experiment.query_set_id} not found")
    
    # Create experiment entry
    experiments[exp_id] = {
        "experiment_id": exp_id,
        "name": experiment.name,
        "created_at": datetime.now().isoformat(),
        "support_set_id": experiment.support_set_id,
        "query_set_id": experiment.query_set_id,
        "status": "created",
        "results_ref": f"{exp_id}_results",
        "metadata": {
            "method": experiment.method,
            "threshold": experiment.threshold,
            "notes": experiment.notes
        }
    }
    
    if experiment.parent_experiment:
        experiments[exp_id]["parent_experiment"] = experiment.parent_experiment
    
    save_json(EXPERIMENTS_FILE, experiments)
    
    return {
        "experiment_id": exp_id,
        "status": "created",
        "message": f"Experiment {exp_id} created successfully"
    }


@router.get("/experiment/list")
async def list_experiments(
    support_set: Optional[str] = None,
    query_set: Optional[str] = None,
    status: Optional[str] = None
):
    """List all experiments with optional filtering"""
    experiments = load_json(EXPERIMENTS_FILE)
    
    filtered = []
    for exp_id, exp in experiments.items():
        # Apply filters
        if support_set and exp.get("support_set_id") != support_set:
            continue
        if query_set and exp.get("query_set_id") != query_set:
            continue
        if status and exp.get("status") != status:
            continue
        
        filtered.append(exp)
    
    return {
        "experiments": filtered,
        "total": len(filtered)
    }


@router.get("/experiment/{exp_id}")
async def get_experiment(exp_id: str):
    """Get experiment details and results"""
    experiments = load_json(EXPERIMENTS_FILE)
    
    if exp_id not in experiments:
        raise HTTPException(status_code=404, detail=f"Experiment {exp_id} not found")
    
    experiment = experiments[exp_id]
    
    # Load results if available
    results = None
    results_ref = experiment.get("results_ref")
    if results_ref:
        experiment_results = load_json(EXPERIMENT_RESULTS_FILE)
        results = experiment_results.get(results_ref)
    
    return {
        "experiment": experiment,
        "results": results,
        "statistics": results.get("statistics") if results else None
    }


@router.post("/experiment/{exp_id}/run")
async def run_experiment(exp_id: str):
    """Execute classification for experiment"""
    experiments = load_json(EXPERIMENTS_FILE)
    
    if exp_id not in experiments:
        raise HTTPException(status_code=404, detail=f"Experiment {exp_id} not found")
    
    # Update status to running
    experiments[exp_id]["status"] = "running"
    save_json(EXPERIMENTS_FILE, experiments)
    
    # TODO: Implement actual classification logic
    # For now, return a job_id
    job_id = str(uuid.uuid4())
    
    return {
        "status": "running",
        "job_id": job_id,
        "message": "Classification job started. This will be implemented in Phase 3."
    }


@router.get("/experiment/compare")
async def compare_experiments(exp_ids: str):
    """Compare multiple experiments"""
    exp_id_list = exp_ids.split(",")
    
    if len(exp_id_list) < 2:
        raise HTTPException(status_code=400, detail="At least 2 experiments required for comparison")
    
    experiments = load_json(EXPERIMENTS_FILE)
    experiment_results = load_json(EXPERIMENT_RESULTS_FILE)
    
    comparison = {
        "experiments": [],
        "comparison": {},
        "diff": []
    }
    
    for exp_id in exp_id_list:
        if exp_id not in experiments:
            raise HTTPException(status_code=404, detail=f"Experiment {exp_id} not found")
        
        exp = experiments[exp_id]
        results_ref = exp.get("results_ref")
        results = experiment_results.get(results_ref) if results_ref else None
        
        comparison["experiments"].append({
            "experiment_id": exp_id,
            "name": exp.get("name"),
            "results": results
        })
    
    # TODO: Implement detailed comparison logic in Phase 6
    comparison["comparison"] = {
        "message": "Detailed comparison will be implemented in Phase 6"
    }
    
    return comparison


@router.delete("/experiment/{exp_id}")
async def delete_experiment(exp_id: str):
    """Delete experiment and its results"""
    experiments = load_json(EXPERIMENTS_FILE)
    
    if exp_id not in experiments:
        raise HTTPException(status_code=404, detail=f"Experiment {exp_id} not found")
    
    # Delete results
    results_ref = experiments[exp_id].get("results_ref")
    if results_ref:
        experiment_results = load_json(EXPERIMENT_RESULTS_FILE)
        if results_ref in experiment_results:
            del experiment_results[results_ref]
            save_json(EXPERIMENT_RESULTS_FILE, experiment_results)
    
    # Delete experiment
    del experiments[exp_id]
    save_json(EXPERIMENTS_FILE, experiments)
    
    return {"message": f"Experiment {exp_id} deleted successfully"}


# ============================================================================
# Support Set Management Endpoints
# ============================================================================

@router.post("/support-set/create")
async def create_support_set(support_set: SupportSetCreate):
    """Create a new support set version"""
    support_sets = load_json(SUPPORT_SETS_FILE)
    annotations = load_json(ANNOTATIONS_FILE)
    
    # Generate support set ID
    version_num = len([k for k in support_sets.keys() if k.startswith("support_v")]) + 1
    support_set_id = f"support_v{version_num}"
    
    # Build classes structure
    classes = {}
    total_images = 0
    
    for class_id, image_ids in support_set.classes.items():
        images = []
        for img_id in image_ids:
            # Verify annotation exists
            if img_id not in annotations:
                raise HTTPException(status_code=404, detail=f"Annotation for image {img_id} not found")
            
            images.append({
                "image_id": img_id,
                "annotation_ref": img_id,
                "added_at": datetime.now().isoformat()
            })
            total_images += 1
        
        classes[class_id] = {
            "class_name": class_id,  # Can be customized later
            "images": images
        }
    
    # Create support set entry
    support_sets[support_set_id] = {
        "support_set_id": support_set_id,
        "name": support_set.name,
        "created_at": datetime.now().isoformat(),
        "classes": classes,
        "total_images": total_images
    }
    
    if support_set.parent_version:
        support_sets[support_set_id]["parent_version"] = support_set.parent_version
    
    save_json(SUPPORT_SETS_FILE, support_sets)
    
    return {
        "support_set_id": support_set_id,
        "version": support_set_id,
        "total_images": total_images
    }


@router.get("/support-set/list")
async def list_support_sets():
    """List all support set versions"""
    support_sets = load_json(SUPPORT_SETS_FILE)
    
    sets_list = []
    for set_id, set_data in support_sets.items():
        sets_list.append({
            "id": set_id,
            "name": set_data.get("name"),
            "version": set_id,
            "images_count": set_data.get("total_images", 0),
            "created_at": set_data.get("created_at")
        })
    
    return {"support_sets": sets_list}


@router.get("/support-set/{support_set_id}")
async def get_support_set(support_set_id: str):
    """Get support set details"""
    support_sets = load_json(SUPPORT_SETS_FILE)
    
    if support_set_id not in support_sets:
        raise HTTPException(status_code=404, detail=f"Support set {support_set_id} not found")
    
    return {
        "support_set": support_sets[support_set_id],
        "classes": support_sets[support_set_id].get("classes", {})
    }


@router.post("/support-set/{support_set_id}/clone")
async def clone_support_set(support_set_id: str):
    """Clone support set for modification"""
    support_sets = load_json(SUPPORT_SETS_FILE)
    
    if support_set_id not in support_sets:
        raise HTTPException(status_code=404, detail=f"Support set {support_set_id} not found")
    
    # Generate new ID
    version_num = len([k for k in support_sets.keys() if k.startswith("support_v")]) + 1
    new_support_set_id = f"support_v{version_num}"
    
    # Clone data
    original = support_sets[support_set_id]
    support_sets[new_support_set_id] = {
        **original,
        "support_set_id": new_support_set_id,
        "name": f"{original.get('name')} (Clone)",
        "created_at": datetime.now().isoformat(),
        "parent_version": support_set_id
    }
    
    save_json(SUPPORT_SETS_FILE, support_sets)
    
    return {
        "new_support_set_id": new_support_set_id,
        "message": f"Cloned {support_set_id} to {new_support_set_id}"
    }


@router.post("/support-set/annotate")
async def annotate_support_images(request: AnnotateRequest):
    """Run Florence-2 + SAM2 on support images"""
    # TODO: Implement in Phase 2
    # This will integrate with existing annotation endpoints
    
    return {
        "processed": len(request.image_ids),
        "annotations": [],
        "message": "Annotation integration will be implemented in Phase 2"
    }


# ============================================================================
# Query Set Management Endpoints
# ============================================================================

@router.post("/query-set/create")
async def create_query_set(query_set: QuerySetCreate):
    """Create query set from uploaded images"""
    query_sets = load_json(QUERY_SETS_FILE)
    
    # Generate query set ID
    query_set_id = f"query_{str(uuid.uuid4())[:8]}"
    
    images = []
    for img_id in query_set.image_ids:
        images.append({
            "image_id": img_id,
            "filename": f"{img_id}.jpg"  # Will be populated from upload metadata
        })
    
    query_sets[query_set_id] = {
        "query_set_id": query_set_id,
        "name": query_set.name,
        "created_at": datetime.now().isoformat(),
        "images": images,
        "total_images": len(images)
    }
    
    save_json(QUERY_SETS_FILE, query_sets)
    
    return {
        "query_set_id": query_set_id,
        "total_images": len(images)
    }


@router.get("/query-set/list")
async def list_query_sets():
    """List all query sets"""
    query_sets = load_json(QUERY_SETS_FILE)
    
    sets_list = []
    for set_id, set_data in query_sets.items():
        sets_list.append({
            "id": set_id,
            "name": set_data.get("name"),
            "images_count": set_data.get("total_images", 0),
            "created_at": set_data.get("created_at")
        })
    
    return {"query_sets": sets_list}


@router.get("/query-set/{query_set_id}")
async def get_query_set(query_set_id: str):
    """Get query set details"""
    query_sets = load_json(QUERY_SETS_FILE)
    
    if query_set_id not in query_sets:
        raise HTTPException(status_code=404, detail=f"Query set {query_set_id} not found")
    
    return {
        "query_set": query_sets[query_set_id],
        "images": query_sets[query_set_id].get("images", [])
    }


# ============================================================================
# Results & Export Endpoints
# ============================================================================

@router.get("/results/{exp_id}")
async def get_results(
    exp_id: str,
    sort_by: str = "confidence",
    order: str = "desc",
    page: int = 1,
    limit: int = 50
):
    """Get classification results for experiment with sorting and pagination"""
    experiments = load_json(EXPERIMENTS_FILE)
    
    if exp_id not in experiments:
        raise HTTPException(status_code=404, detail=f"Experiment {exp_id} not found")
    
    results_ref = experiments[exp_id].get("results_ref")
    if not results_ref:
        raise HTTPException(status_code=404, detail=f"No results found for experiment {exp_id}")
    
    experiment_results = load_json(EXPERIMENT_RESULTS_FILE)
    results = experiment_results.get(results_ref)
    
    if not results:
        return {"results": [], "statistics": {}, "pagination": {}}
    
    # TODO: Implement sorting and pagination in Phase 4
    
    return {
        "results": results.get("classifications", {}),
        "statistics": results.get("statistics", {}),
        "pagination": {
            "page": page,
            "limit": limit,
            "total": results.get("statistics", {}).get("total_classified", 0)
        }
    }


@router.post("/results/{exp_id}/export")
async def export_results(exp_id: str, request: ExportRequest):
    """Export experiment results"""
    experiments = load_json(EXPERIMENTS_FILE)
    
    if exp_id not in experiments:
        raise HTTPException(status_code=404, detail=f"Experiment {exp_id} not found")
    
    # TODO: Implement export logic in Phase 6
    
    return {
        "export_path": f"data/exports/{exp_id}",
        "format": request.format,
        "message": "Export functionality will be implemented in Phase 6"
    }
