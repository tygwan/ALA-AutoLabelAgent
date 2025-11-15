"""
Annotation Exporter.

M3: UI Integration - Export annotations to COCO and YOLO formats.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


class AnnotationExporter:
    """
    Export annotations to various formats.

    Supported formats:
        - COCO: MS COCO JSON format
        - YOLO: YOLO txt format (one file per image)

    Usage:
        exporter = AnnotationExporter()
        exporter.export_coco(results, image_path, output_path)
        exporter.export_yolo(results, image_path, output_dir)
    """

    def export_coco(
        self,
        results: dict,
        image_path: str,
        output_path: str,
        dataset_name: str = "ALA Dataset",
    ) -> None:
        """
        Export annotations to COCO JSON format.

        COCO format structure:
        {
            "info": {...},
            "images": [...],
            "annotations": [...],
            "categories": [...]
        }

        Args:
            results: Annotation results dictionary with boxes, labels, scores
            image_path: Path to source image
            output_path: Path to output COCO JSON file
            dataset_name: Name of the dataset
        """
        image_path_obj = Path(image_path)

        # Get image dimensions from results metadata
        metadata = results.get("metadata", {})
        image_width = metadata.get("image_width", 0)
        image_height = metadata.get("image_height", 0)

        # Create COCO structure
        coco_data: dict[str, Any] = {
            "info": {
                "description": dataset_name,
                "version": "1.0",
                "year": datetime.now().year,
                "contributor": "ALA-AutoLabelAgent",
                "date_created": datetime.now().isoformat(),
            },
            "images": [
                {
                    "id": 1,
                    "file_name": image_path_obj.name,
                    "width": image_width,
                    "height": image_height,
                }
            ],
            "annotations": [],
            "categories": [],
        }

        # Extract unique categories
        labels = results.get("labels", [])
        unique_labels = sorted(set(labels))
        category_map = {}

        for idx, label in enumerate(unique_labels, start=1):
            category_map[label] = idx
            coco_data["categories"].append(
                {
                    "id": idx,
                    "name": label,
                    "supercategory": "object",
                }
            )

        # Add annotations
        boxes = results.get("boxes", [])
        scores = results.get("scores", [])

        for ann_id, (box, label) in enumerate(zip(boxes, labels), start=1):
            x1, y1, x2, y2 = box
            width = x2 - x1
            height = y2 - y1
            area = width * height

            annotation = {
                "id": ann_id,
                "image_id": 1,
                "category_id": category_map[label],
                "bbox": [x1, y1, width, height],  # COCO format: [x, y, width, height]
                "area": area,
                "iscrowd": 0,
            }

            # Add score if available
            if ann_id - 1 < len(scores):
                annotation["score"] = float(scores[ann_id - 1])

            coco_data["annotations"].append(annotation)

        # Write to file
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path_obj, "w", encoding="utf-8") as f:
            json.dump(coco_data, f, indent=2, ensure_ascii=False)

    def export_yolo(
        self,
        results: dict,
        image_path: str,
        output_dir: str,
        class_names: Optional[list[str]] = None,
    ) -> None:
        """
        Export annotations to YOLO txt format.

        YOLO format (one line per object):
        <class_id> <x_center> <y_center> <width> <height>

        All coordinates are normalized to [0, 1].

        Args:
            results: Annotation results dictionary with boxes, labels
            image_path: Path to source image
            output_dir: Directory to save YOLO txt files
            class_names: Optional list of class names for mapping
        """
        image_path_obj = Path(image_path)
        output_dir_obj = Path(output_dir)
        output_dir_obj.mkdir(parents=True, exist_ok=True)

        # Get image dimensions
        metadata = results.get("metadata", {})
        image_width = metadata.get("image_width", 1)
        image_height = metadata.get("image_height", 1)

        # Create class mapping
        labels = results.get("labels", [])
        if class_names is None:
            unique_labels = sorted(set(labels))
            class_names = unique_labels

        class_map = {name: idx for idx, name in enumerate(class_names)}

        # Convert annotations to YOLO format
        boxes = results.get("boxes", [])
        yolo_lines = []

        for box, label in zip(boxes, labels):
            if label not in class_map:
                continue

            class_id = class_map[label]
            x1, y1, x2, y2 = box

            # Convert to YOLO format (normalized center coordinates)
            x_center = ((x1 + x2) / 2) / image_width
            y_center = ((y1 + y2) / 2) / image_height
            width = (x2 - x1) / image_width
            height = (y2 - y1) / image_height

            yolo_lines.append(f"{class_id} {x_center} {y_center} {width} {height}")

        # Write to file (same name as image but .txt extension)
        output_file = output_dir_obj / f"{image_path_obj.stem}.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(yolo_lines))

        # Also create classes.txt file
        classes_file = output_dir_obj / "classes.txt"
        if not classes_file.exists():
            with open(classes_file, "w", encoding="utf-8") as f:
                f.write("\n".join(class_names))

    def export_batch_coco(
        self,
        batch_results: list[dict],
        image_paths: list[str],
        output_path: str,
        dataset_name: str = "ALA Dataset",
    ) -> None:
        """
        Export batch annotations to single COCO JSON file.

        Args:
            batch_results: List of annotation results dictionaries
            image_paths: List of image paths
            output_path: Path to output COCO JSON file
            dataset_name: Name of the dataset
        """
        # Create COCO structure
        coco_data: dict[str, Any] = {
            "info": {
                "description": dataset_name,
                "version": "1.0",
                "year": datetime.now().year,
                "contributor": "ALA-AutoLabelAgent",
                "date_created": datetime.now().isoformat(),
            },
            "images": [],
            "annotations": [],
            "categories": [],
        }

        # Collect all unique categories
        all_labels = set()
        for results in batch_results:
            labels = results.get("labels", [])
            all_labels.update(labels)

        unique_labels = sorted(all_labels)
        category_map = {}

        for idx, label in enumerate(unique_labels, start=1):
            category_map[label] = idx
            coco_data["categories"].append(
                {
                    "id": idx,
                    "name": label,
                    "supercategory": "object",
                }
            )

        # Process each image
        annotation_id = 1
        for image_id, (results, image_path) in enumerate(
            zip(batch_results, image_paths), start=1
        ):
            image_path_obj = Path(image_path)
            metadata = results.get("metadata", {})

            # Add image info
            coco_data["images"].append(
                {
                    "id": image_id,
                    "file_name": image_path_obj.name,
                    "width": metadata.get("image_width", 0),
                    "height": metadata.get("image_height", 0),
                }
            )

            # Add annotations for this image
            boxes = results.get("boxes", [])
            labels = results.get("labels", [])
            scores = results.get("scores", [])

            for idx, (box, label) in enumerate(zip(boxes, labels)):
                x1, y1, x2, y2 = box
                width = x2 - x1
                height = y2 - y1
                area = width * height

                annotation = {
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": category_map[label],
                    "bbox": [x1, y1, width, height],
                    "area": area,
                    "iscrowd": 0,
                }

                if idx < len(scores):
                    annotation["score"] = float(scores[idx])

                coco_data["annotations"].append(annotation)
                annotation_id += 1

        # Write to file
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path_obj, "w", encoding="utf-8") as f:
            json.dump(coco_data, f, indent=2, ensure_ascii=False)
