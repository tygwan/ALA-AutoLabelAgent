import json
import os
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Union
from pathlib import Path

# Path to the assets registry file
ASSETS_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "assets.json")
PROJECTS_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "projects.json")

class AssetRegistry:
    def __init__(self):
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        if not os.path.exists(ASSETS_DB_PATH):
            with open(ASSETS_DB_PATH, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(PROJECTS_DB_PATH):
            # Projects DB should already exist, but just in case
            with open(PROJECTS_DB_PATH, 'w') as f:
                json.dump({"projects": []}, f)

    def _load_assets(self) -> Dict:
        try:
            with open(ASSETS_DB_PATH, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _save_assets(self, assets: Dict):
        with open(ASSETS_DB_PATH, 'w') as f:
            json.dump(assets, f, indent=2)

    def _load_projects(self) -> Dict:
        try:
            with open(PROJECTS_DB_PATH, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"projects": []}
            
    def _save_projects(self, data: Dict):
        with open(PROJECTS_DB_PATH, 'w') as f:
            json.dump(data, f, indent=2)

    def register_managed_file(self, file_id: str, project_id: str, relative_path: str, original_filename: str) -> Dict:
        """Register a file that is managed by the system (uploaded/copied to data/uploads)"""
        assets = self._load_assets()
        
        asset_record = {
            "type": "managed",
            "file_id": file_id,
            "project_id": project_id,
            "path": relative_path,  # Relative to backend root
            "original_filename": original_filename,
            "registered_at": datetime.now().isoformat()
        }
        
        assets[file_id] = asset_record
        self._save_assets(assets)
        return asset_record

    def register_linked_file(self, file_id: str, project_id: str, absolute_path: str, root_id: str) -> Dict:
        """Register a file that is linked from an external location"""
        assets = self._load_assets()
        
        # Calculate relative path from the linked root
        # This is useful if we want to reconstruct the path later using the root
        # For now, we'll store the absolute path for simplicity in retrieval, 
        # but the root_id allows us to update it if the root moves
        
        asset_record = {
            "type": "linked",
            "file_id": file_id,
            "project_id": project_id,
            "path": absolute_path,  # Absolute path
            "root_id": root_id,
            "original_filename": os.path.basename(absolute_path),
            "registered_at": datetime.now().isoformat()
        }
        
        assets[file_id] = asset_record
        self._save_assets(assets)
        return asset_record

    def get_asset_path(self, file_id: str) -> Optional[str]:
        """Get the absolute filesystem path for an asset"""
        assets = self._load_assets()
        if file_id not in assets:
            return None
            
        asset = assets[file_id]
        
        if asset["type"] == "managed":
            # Managed files are relative to backend root
            backend_root = os.path.dirname(os.path.dirname(__file__))
            return os.path.join(backend_root, asset["path"])
        elif asset["type"] == "linked":
            # Linked files have absolute paths
            # In a more advanced version, we would look up the root_id and reconstruct
            return asset["path"]
            
        return None

    def get_project_assets(self, project_id: str) -> List[Dict]:
        """Get all assets for a specific project"""
        assets = self._load_assets()
        return [asset for asset in assets.values() if asset.get("project_id") == project_id]

    def link_external_folder(self, project_id: str, folder_path: str) -> Dict:
        """
        Link an external folder to a project.
        Recursively finds images and registers them.
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")
            
        # 1. Register the linked root in projects.json
        projects_data = self._load_projects()
        project = next((p for p in projects_data["projects"] if p["project_id"] == project_id), None)
        
        if not project:
            raise ValueError(f"Project not found: {project_id}")
            
        import uuid
        root_id = f"root_{uuid.uuid4().hex[:8]}"
        
        if "linked_roots" not in project:
            project["linked_roots"] = []
            
        project["linked_roots"].append({
            "root_id": root_id,
            "path": folder_path,
            "linked_at": datetime.now().isoformat()
        })
        
        self._save_projects(projects_data)
        
        # 2. Scan for images and register them
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff'}
        added_count = 0
        
        for root, _, files in os.walk(folder_path):
            for file in files:
                if os.path.splitext(file)[1].lower() in image_extensions:
                    absolute_path = os.path.join(root, file)
                    file_id = f"file_{uuid.uuid4().hex[:12]}"
                    
                    self.register_linked_file(
                        file_id=file_id,
                        project_id=project_id,
                        absolute_path=absolute_path,
                        root_id=root_id
                    )
                    added_count += 1
                    
        # Update project file count
        project["file_count"] = project.get("file_count", 0) + added_count
        self._save_projects(projects_data)
        
        return {
            "root_id": root_id,
            "added_count": added_count,
            "folder_path": folder_path
        }

# Global instance
asset_registry = AssetRegistry()
