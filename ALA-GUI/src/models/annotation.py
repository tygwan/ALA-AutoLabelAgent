"""
Annotation data model.

Represents an object annotation with bounding box and/or segmentation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4


class AnnotationType(str, Enum):
    """Annotation type enumeration."""

    BBOX = "bbox"
    POLYGON = "polygon"
    MASK = "mask"


@dataclass
class Annotation:
    """
    Annotation data model.

    Attributes:
        class_id: Reference to class definition
        bbox: Bounding box [x, y, width, height]
        id: Unique identifier (auto-generated)
        segmentation: Optional polygon/mask segmentation
        type: Annotation type (auto-detected)
        confidence: Confidence score (0.0-1.0)
    """

    class_id: str
    bbox: List[float]
    id: UUID = field(default_factory=uuid4)
    segmentation: Optional[List[List[float]]] = None
    type: AnnotationType = field(init=False)
    confidence: float = 1.0

    def __post_init__(self) -> None:
        """Auto-detect annotation type after initialization."""
        if self.segmentation is not None:
            self.type = AnnotationType.POLYGON
        else:
            self.type = AnnotationType.BBOX

    @property
    def area(self) -> float:
        """
        Calculate bounding box area.

        Returns:
            Area in square pixels
        """
        if len(self.bbox) >= 4:
            return self.bbox[2] * self.bbox[3]  # width * height
        return 0.0

    def to_coco(self) -> Dict[str, Any]:
        """
        Convert to COCO format.

        Returns:
            Dictionary in COCO annotation format
        """
        coco_data = {
            "id": str(self.id),
            "category_id": self.class_id,
            "bbox": self.bbox,
            "area": self.area,
            "score": self.confidence,
        }

        if self.segmentation is not None:
            coco_data["segmentation"] = self.segmentation

        return coco_data

    def to_yolo(self, image_width: int, image_height: int) -> Dict[str, float]:
        """
        Convert to YOLO format (normalized coordinates).

        Args:
            image_width: Image width in pixels
            image_height: Image height in pixels

        Returns:
            Dictionary with YOLO format (class, x_center, y_center, width, height)
        """
        x, y, w, h = self.bbox

        # Convert to center coordinates and normalize
        x_center = (x + w / 2) / image_width
        y_center = (y + h / 2) / image_height
        width_norm = w / image_width
        height_norm = h / image_height

        return {
            "class_id": self.class_id,
            "x_center": x_center,
            "y_center": y_center,
            "width": width_norm,
            "height": height_norm,
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize Annotation to dictionary.

        Returns:
            Dictionary representation of Annotation
        """
        data = {
            "id": str(self.id),
            "class_id": self.class_id,
            "bbox": self.bbox,
            "type": self.type.value,
            "confidence": self.confidence,
        }

        if self.segmentation is not None:
            data["segmentation"] = self.segmentation

        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Annotation":
        """
        Deserialize Annotation from dictionary.

        Args:
            data: Dictionary with annotation data

        Returns:
            Annotation instance
        """
        # Convert UUID string to UUID object if present
        if "id" in data and isinstance(data["id"], str):
            data["id"] = UUID(data["id"])

        # Remove type as it's auto-detected
        data.pop("type", None)

        # Filter valid fields
        valid_fields = {"class_id", "bbox", "id", "segmentation", "confidence"}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}

        return cls(**filtered_data)
