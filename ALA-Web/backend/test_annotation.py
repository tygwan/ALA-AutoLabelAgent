"""
Test script for Florence-2 + SAM2 annotation
Run this to verify models are working
"""

from services.auto_annotator import auto_annotator
from pathlib import Path

def test_annotation():
    """Test annotation pipeline"""
    # Test image (place a test image in backend/)
    test_image = Path("test_image.jpg")
    
    if not test_image.exists():
        print("=" * 50)
        print("ERROR: test_image.jpg not found")
        print("Please add a test_image.jpg to backend/")
        print("=" * 50)
        return
    
    # Define what to detect
    ontology = {
        "person": "person",
        "car": "car",
        "dog": "dog",
        "cat": "cat"
    }
    
    print("=" * 50)
    print("ALA-Web Auto-Annotation Test")
    print("=" * 50)
    print(f"Test image: {test_image}")
    print(f"Ontology: {ontology}")
    print("=" * 50)
    print()
    
    try:
        result = auto_annotator.annotate(
            image_path=str(test_image),
            ontology=ontology,
            save_visualization=True
        )
        
        print()
        print("=" * 50)
        print("RESULTS")
        print("=" * 50)
        print(f"Detected Objects: {len(result['boxes'])}")
        print(f"Classes: {result['classes']}")
        print(f"Scores: {[f'{s:.2f}' for s in result['scores']]}")
        print()
        print("Visualization saved to: test_image_annotated.jpg")
        print("=" * 50)
        print("TEST PASSED ✓")
        print("=" * 50)
        
    except Exception as e:
        print()
        print("=" * 50)
        print("TEST FAILED ✗")
        print("=" * 50)
        print(f"Error: {e}")
        print()
        import traceback
        traceback.print_exc()
        print("=" * 50)

if __name__ == "__main__":
    test_annotation()
