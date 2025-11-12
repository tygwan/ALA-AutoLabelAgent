"""
Project data model.

Represents a labeling project with images, annotations, and classes.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4


@dataclass
class Project:
    """
    Project data model.

    Attributes:
        name: Project name
        path: Project directory path
        id: Unique identifier (auto-generated)
        description: Optional project description
        created_at: Creation timestamp (auto-generated)
        updated_at: Last update timestamp (auto-generated)
        images: List of image references
        classes: List of class definitions
    """

    name: str
    path: Path
    id: UUID = field(default_factory=uuid4)
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    images: List[Any] = field(default_factory=list)
    classes: List[Any] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize Project to dictionary.

        Returns:
            Dictionary representation of Project
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "path": self.path.as_posix(),  # Platform-independent path representation
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "images": [
                img if isinstance(img, dict) else str(img) for img in self.images
            ],
            "classes": [
                cls if isinstance(cls, dict) else str(cls) for cls in self.classes
            ],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        """
        Deserialize Project from dictionary.

        Args:
            data: Dictionary with project data

        Returns:
            Project instance
        """
        # Convert path string to Path object
        if "path" in data:
            data["path"] = Path(data["path"])

        # Convert UUID string to UUID object if present
        if "id" in data and isinstance(data["id"], str):
            data["id"] = UUID(data["id"])

        # Convert datetime strings to datetime objects if present
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])

        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])

        # Remove fields that aren't in the dataclass
        valid_fields = {
            "name",
            "path",
            "id",
            "description",
            "created_at",
            "updated_at",
            "images",
            "classes",
        }
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}

        return cls(**filtered_data)
