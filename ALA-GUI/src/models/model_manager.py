"""
Model Manager.

M3: Model Integration - Manages model discovery and loading.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class ModelInfo:
    """Information about a discovered model."""

    name: str  # Display name
    type: str  # "vlm" or "segmentation"
    path: str  # Full path to model checkpoint
    framework: str  # "florence2", "sam2", etc.
    size_mb: Optional[float] = None  # Model size in MB


class ModelManager:
    """
    Manages model discovery and organization.

    Scans model directories for available models and provides
    information for UI selection.

    Usage:
        manager = ModelManager()
        manager.set_model_directory("path/to/models")

        vlm_models = manager.get_vlm_models()
        seg_models = manager.get_segmentation_models()
    """

    def __init__(self) -> None:
        """Initialize ModelManager."""
        self.model_dir: Optional[str] = None
        self.vlm_models: List[ModelInfo] = []
        self.segmentation_models: List[ModelInfo] = []

        # Default model directory
        default_dir = os.path.expanduser("~/.cache/ala-gui/models")
        self.set_model_directory(default_dir)

    def set_model_directory(self, directory: str) -> None:
        """
        Set model directory and scan for models.

        Args:
            directory: Path to model directory
        """
        self.model_dir = directory
        os.makedirs(directory, exist_ok=True)
        self.scan_models()

    def scan_models(self) -> None:
        """Scan model directory for available models."""
        if not self.model_dir:
            return

        self.vlm_models = []
        self.segmentation_models = []

        model_path = Path(self.model_dir)

        # Scan for Florence-2 models
        self._scan_florence2_models(model_path)

        # Scan for SAM2 models
        self._scan_sam2_models(model_path)

        # Add HuggingFace hub models as option
        self._add_huggingface_models()

    def _scan_florence2_models(self, model_path: Path) -> None:
        """Scan for Florence-2 models."""
        florence_dir = model_path / "florence2"
        if florence_dir.exists():
            for model_dir in florence_dir.iterdir():
                if model_dir.is_dir() and (model_dir / "config.json").exists():
                    size_mb = self._get_directory_size_mb(model_dir)
                    self.vlm_models.append(
                        ModelInfo(
                            name=f"Florence-2 ({model_dir.name})",
                            type="vlm",
                            path=str(model_dir),
                            framework="florence2",
                            size_mb=size_mb,
                        )
                    )

    def _scan_sam2_models(self, model_path: Path) -> None:
        """Scan for SAM2 models."""
        sam2_dir = model_path / "sam2"
        if sam2_dir.exists():
            for checkpoint in sam2_dir.glob("*.pth"):
                size_mb = checkpoint.stat().st_size / (1024 * 1024)
                self.segmentation_models.append(
                    ModelInfo(
                        name=f"SAM2 ({checkpoint.stem})",
                        type="segmentation",
                        path=str(checkpoint),
                        framework="sam2",
                        size_mb=size_mb,
                    )
                )

    def _add_huggingface_models(self) -> None:
        """Add HuggingFace Hub models as download options."""
        # Florence-2 models from HuggingFace
        hf_florence_models = [
            ("Florence-2-large (HF)", "microsoft/Florence-2-large"),
            ("Florence-2-base (HF)", "microsoft/Florence-2-base"),
        ]

        for name, hf_id in hf_florence_models:
            self.vlm_models.append(
                ModelInfo(
                    name=name,
                    type="vlm",
                    path=hf_id,  # HuggingFace model ID
                    framework="florence2",
                    size_mb=None,  # Will download on demand
                )
            )

        # SAM2 models - add download option
        sam2_url = (
            "https://dl.fbaipublicfiles.com/segment_anything_2/"
            "072824/sam2_hiera_base_plus.pt"
        )
        self.segmentation_models.append(
            ModelInfo(
                name="SAM2 Base+ (Auto-download)",
                type="segmentation",
                path=sam2_url,
                framework="sam2",
                size_mb=300.0,
            )
        )

    def _get_directory_size_mb(self, directory: Path) -> float:
        """Get total size of directory in MB."""
        total_size = sum(f.stat().st_size for f in directory.rglob("*") if f.is_file())
        return total_size / (1024 * 1024)

    def get_vlm_models(self) -> List[ModelInfo]:
        """
        Get list of available VLM models.

        Returns:
            List of VLM model information
        """
        return self.vlm_models

    def get_segmentation_models(self) -> List[ModelInfo]:
        """
        Get list of available segmentation models.

        Returns:
            List of segmentation model information
        """
        return self.segmentation_models

    def get_model_info(self, model_path: str) -> Optional[ModelInfo]:
        """
        Get information about a specific model.

        Args:
            model_path: Path to model

        Returns:
            ModelInfo if found, None otherwise
        """
        all_models = self.vlm_models + self.segmentation_models
        for model in all_models:
            if model.path == model_path:
                return model
        return None

    def get_model_directory(self) -> str:
        """
        Get current model directory.

        Returns:
            Path to model directory
        """
        return self.model_dir or os.path.expanduser("~/.cache/ala-gui/models")

    def create_directory_structure(self) -> Dict[str, str]:
        """
        Create recommended directory structure for models.

        Returns:
            Dictionary of created directories
        """
        base_dir = self.get_model_directory()
        dirs = {
            "base": base_dir,
            "florence2": os.path.join(base_dir, "florence2"),
            "sam2": os.path.join(base_dir, "sam2"),
            "custom": os.path.join(base_dir, "custom"),
        }

        for path in dirs.values():
            os.makedirs(path, exist_ok=True)

        return dirs
