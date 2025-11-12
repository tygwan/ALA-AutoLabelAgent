"""
Unit tests for Annotation data model.

Following TDD RED-GREEN-REFACTOR cycle.
"""

from uuid import UUID

import pytest

from models.annotation import Annotation, AnnotationType


class TestAnnotationDataclass:
    """Test suite for Annotation dataclass."""

    def test_annotation_initialization(self):
        """Test Annotation creates with required fields."""
        # Arrange
        class_id = "class-123"
        bbox = [10, 20, 100, 200]

        # Act
        annotation = Annotation(class_id=class_id, bbox=bbox)

        # Assert
        assert annotation.class_id == class_id
        assert annotation.bbox == bbox
        assert isinstance(annotation.id, UUID)
        assert annotation.type == AnnotationType.BBOX
        assert annotation.segmentation is None
        assert annotation.confidence == 1.0

    def test_annotation_with_segmentation(self):
        """Test Annotation with segmentation."""
        # Arrange
        class_id = "class-123"
        bbox = [10, 20, 100, 200]
        segmentation = [[10, 20, 110, 20, 110, 220, 10, 220]]

        # Act
        annotation = Annotation(class_id=class_id, bbox=bbox, segmentation=segmentation)

        # Assert
        assert annotation.segmentation == segmentation
        assert annotation.type == AnnotationType.POLYGON

    def test_annotation_with_confidence(self):
        """Test Annotation with confidence score."""
        # Arrange
        annotation = Annotation(
            class_id="class-123", bbox=[10, 20, 100, 200], confidence=0.95
        )

        # Assert
        assert annotation.confidence == 0.95

    def test_annotation_uuid_uniqueness(self):
        """Test each Annotation gets unique UUID."""
        # Arrange & Act
        ann1 = Annotation(class_id="class-123", bbox=[10, 20, 100, 200])
        ann2 = Annotation(class_id="class-123", bbox=[10, 20, 100, 200])

        # Assert
        assert ann1.id != ann2.id

    def test_annotation_to_coco(self):
        """Test Annotation conversion to COCO format."""
        # Arrange
        annotation = Annotation(
            class_id="class-123", bbox=[10, 20, 100, 200], confidence=0.95
        )

        # Act
        coco_data = annotation.to_coco()

        # Assert
        assert isinstance(coco_data, dict)
        assert coco_data["bbox"] == [10, 20, 100, 200]
        assert coco_data["category_id"] == "class-123"
        assert coco_data["score"] == 0.95

    def test_annotation_to_yolo(self):
        """Test Annotation conversion to YOLO format."""
        # Arrange
        annotation = Annotation(class_id="class-123", bbox=[10, 20, 100, 200])
        image_width = 640
        image_height = 480

        # Act
        yolo_data = annotation.to_yolo(image_width, image_height)

        # Assert
        assert isinstance(yolo_data, dict)
        assert "class_id" in yolo_data
        assert "x_center" in yolo_data
        assert "y_center" in yolo_data
        assert "width" in yolo_data
        assert "height" in yolo_data

    def test_annotation_area(self):
        """Test Annotation area calculation."""
        # Arrange
        annotation = Annotation(class_id="class-123", bbox=[10, 20, 100, 200])

        # Act
        area = annotation.area

        # Assert
        assert area == 100 * 200  # width * height

    def test_annotation_to_dict(self):
        """Test Annotation serialization to dict."""
        # Arrange
        annotation = Annotation(
            class_id="class-123",
            bbox=[10, 20, 100, 200],
            confidence=0.95,
            segmentation=[[10, 20, 110, 20, 110, 220, 10, 220]],
        )

        # Act
        data = annotation.to_dict()

        # Assert
        assert isinstance(data, dict)
        assert data["class_id"] == "class-123"
        assert data["bbox"] == [10, 20, 100, 200]
        assert data["confidence"] == 0.95
        assert "id" in data
        assert "type" in data

    def test_annotation_from_dict(self):
        """Test Annotation deserialization from dict."""
        # Arrange
        data = {
            "class_id": "class-123",
            "bbox": [10, 20, 100, 200],
            "confidence": 0.95,
        }

        # Act
        annotation = Annotation.from_dict(data)

        # Assert
        assert annotation.class_id == "class-123"
        assert annotation.bbox == [10, 20, 100, 200]
        assert annotation.confidence == 0.95


class TestAnnotationType:
    """Test AnnotationType enum."""

    def test_annotation_type_values(self):
        """Test AnnotationType enum values."""
        assert AnnotationType.BBOX == "bbox"
        assert AnnotationType.POLYGON == "polygon"
        assert AnnotationType.MASK == "mask"
