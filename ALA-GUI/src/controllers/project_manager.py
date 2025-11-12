"""
ProjectManager - Manages project lifecycle and operations.

Handles creating, loading, saving projects and managing their images.
"""

import json
from pathlib import Path
from typing import Optional

from models import Image, Project


class ProjectManager:
    """
    ProjectManager handles project operations.

    Manages the current active project and provides methods for:
    - Creating new projects
    - Loading existing projects
    - Saving projects to disk
    - Adding images to projects
    - Managing project state

    Attributes:
        current_project: Currently active Project instance or None
    """

    def __init__(self) -> None:
        """Initialize ProjectManager with no active project."""
        self.current_project: Optional[Project] = None

    def has_project(self) -> bool:
        """
        Check if there is an active project.

        Returns:
            True if current_project is not None
        """
        return self.current_project is not None

    def create_project(self, name: str, path: Path, description: str = "") -> Project:
        """
        Create a new project.

        Args:
            name: Project name
            path: Project directory path
            description: Optional project description

        Returns:
            Created Project instance

        Side effects:
            - Creates project directory if it doesn't exist
            - Sets current_project to new project
        """
        # Ensure path is Path object
        if not isinstance(path, Path):
            path = Path(path)

        # Create project directory
        path.mkdir(parents=True, exist_ok=True)

        # Create project instance
        project = Project(name=name, path=path, description=description)

        # Set as current project
        self.current_project = project

        return project

    def save_project(self, save_path: Optional[Path] = None) -> Path:
        """
        Save current project to JSON file.

        Args:
            save_path: Optional custom save path, defaults to project_path/project.json

        Returns:
            Path where project was saved

        Raises:
            ValueError: If no active project exists
        """
        if not self.has_project():
            raise ValueError("No active project to save")

        # Use default path if not provided
        if save_path is None:
            save_path = self.current_project.path / "project.json"

        # Serialize project to JSON
        project_data = self.current_project.to_dict()

        # Write to file
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(project_data, f, indent=2, ensure_ascii=False)

        return save_path

    def load_project(self, load_path: Path) -> Project:
        """
        Load project from JSON file.

        Args:
            load_path: Path to project JSON file

        Returns:
            Loaded Project instance

        Raises:
            FileNotFoundError: If load_path doesn't exist

        Side effects:
            Sets current_project to loaded project
        """
        # Ensure path is Path object
        if not isinstance(load_path, Path):
            load_path = Path(load_path)

        # Check file exists
        if not load_path.exists():
            raise FileNotFoundError(f"Project file not found: {load_path}")

        # Load JSON data
        with open(load_path, "r", encoding="utf-8") as f:
            project_data = json.load(f)

        # Deserialize project
        project = Project.from_dict(project_data)

        # Set as current project
        self.current_project = project

        return project

    def add_image(self, path: Path, width: int, height: int, **kwargs) -> Image:
        """
        Add image to current project.

        Args:
            path: Image file path
            width: Image width in pixels
            height: Image height in pixels
            **kwargs: Additional Image parameters (metadata, etc.)

        Returns:
            Created Image instance

        Raises:
            ValueError: If no active project exists
            FileNotFoundError: If image file doesn't exist
        """
        if not self.has_project():
            raise ValueError("No active project - create or load project first")

        # Ensure path is Path object
        if not isinstance(path, Path):
            path = Path(path)

        # Check file exists
        if not path.exists():
            raise FileNotFoundError(f"Image file not found: {path}")

        # Create image instance
        image = Image(path=path, width=width, height=height, **kwargs)

        # Add to current project
        self.current_project.images.append(image)

        return image
