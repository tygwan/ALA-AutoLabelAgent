"""
Class definition data model.

Represents an object class/category with name and color.
"""

import re
from dataclasses import dataclass, field
from typing import Any, Dict, Tuple
from uuid import UUID, uuid4


@dataclass
class ClassDefinition:
    """
    Class definition data model.

    Attributes:
        name: Class name (e.g., "person", "car")
        color: Hex color code for visualization (e.g., "#FF0000")
        id: Unique identifier (auto-generated)
        description: Optional class description
    """

    name: str
    color: str
    id: UUID = field(default_factory=uuid4)
    description: str = ""

    def is_valid_color(self) -> bool:
        """
        Validate hex color format.

        Returns:
            True if color is valid hex format (#RRGGBB or #RGB)
        """
        # Match #RGB or #RRGGBB format
        hex_pattern = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
        return bool(re.match(hex_pattern, self.color))

    @property
    def rgb_tuple(self) -> Tuple[int, int, int]:
        """
        Convert hex color to RGB tuple.

        Returns:
            (R, G, B) tuple with values 0-255
        """
        # Remove # prefix
        hex_color = self.color.lstrip("#")

        # Handle short format (#RGB -> #RRGGBB)
        if len(hex_color) == 3:
            hex_color = "".join([c * 2 for c in hex_color])

        # Convert to RGB
        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return (r, g, b)
        except ValueError:
            return (0, 0, 0)  # Default to black if invalid

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize ClassDefinition to dictionary.

        Returns:
            Dictionary representation of ClassDefinition
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "color": self.color,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClassDefinition":
        """
        Deserialize ClassDefinition from dictionary.

        Args:
            data: Dictionary with class data

        Returns:
            ClassDefinition instance
        """
        # Convert UUID string to UUID object if present
        if "id" in data and isinstance(data["id"], str):
            data["id"] = UUID(data["id"])

        # Filter valid fields
        valid_fields = {"name", "color", "id", "description"}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}

        return cls(**filtered_data)

    def __str__(self) -> str:
        """String representation of ClassDefinition."""
        return f"ClassDefinition(name='{self.name}', color='{self.color}')"

    def __repr__(self) -> str:
        """Detailed representation of ClassDefinition."""
        return (
            f"ClassDefinition(id={self.id}, name='{self.name}', "
            f"color='{self.color}', description='{self.description}')"
        )
