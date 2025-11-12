"""
Image data model.

Represents an image file with dimensions and metadata.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Tuple
from uuid import UUID, uuid4


@dataclass
class Image:
    """
    Image data model.

    Attributes:
        path: Image file path
        width: Image width in pixels
        height: Image height in pixels
        id: Unique identifier (auto-generated)
        filename: Extracted from path (auto-generated)
        annotations: List of annotations for this image
        metadata: Optional metadata dictionary
    """

    path: Path
    width: int
    height: int
    id: UUID = field(default_factory=uuid4)
    filename: str = field(init=False)
    annotations: List[Any] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Extract filename from path after initialization."""
        self.filename = self.path.name

    @property
    def aspect_ratio(self) -> float:
        """
        Calculate aspect ratio (width / height).

        Returns:
            Aspect ratio as float
        """
        return self.width / self.height if self.height > 0 else 0.0

    @property
    def size(self) -> Tuple[int, int]:
        """
        Get image size as tuple.

        Returns:
            (width, height) tuple
        """
        return (self.width, self.height)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize Image to dictionary.

        Returns:
            Dictionary representation of Image
        """
        return {
            "id": str(self.id),
            "path": self.path.as_posix(),
            "filename": self.filename,
            "width": self.width,
            "height": self.height,
            "annotations": [
                ann if isinstance(ann, dict) else str(ann) for ann in self.annotations
            ],
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Image":
        """
        Deserialize Image from dictionary.

        Args:
            data: Dictionary with image data

        Returns:
            Image instance
        """
        # Convert path string to Path object
        if "path" in data:
            data["path"] = Path(data["path"])

        # Convert UUID string to UUID object if present
        if "id" in data and isinstance(data["id"], str):
            data["id"] = UUID(data["id"])

        # Remove filename as it's auto-generated
        data.pop("filename", None)

        # Filter valid fields
        valid_fields = {"path", "width", "height", "id", "annotations", "metadata"}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}

        return cls(**filtered_data)
