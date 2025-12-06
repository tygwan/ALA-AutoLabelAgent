"""
Simple test script to validate backend logic without running uvicorn.
This bypasses the typing_extensions issue in Python 3.10.
"""

import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def test_json_operations():
    """Test JSON file operations"""
    from routers.classification import load_json, save_json, EXPERIMENTS_FILE, SUPPORT_SETS_FILE
    
    print("Testing JSON operations...")
    
    # Test load/save
    test_data = {"test_id": {"name": "Test Experiment", "status": "created"}}
    save_json(EXPERIMENTS_FILE, test_data)
    loaded = load_json(EXPERIMENTS_FILE)
    
    assert "test_id" in loaded
    assert loaded["test_id"]["name"] == "Test Experiment"
    print("✓ JSON operations working")
    
def test_experiment_creation():
    """Test experiment creation logic"""
    print("\nTesting experiment creation...")
    
    # Simulate creating support set
    from routers.classification import save_json, SUPPORT_SETS_FILE, QUERY_SETS_FILE, EXPERIMENTS_FILE
    
    # Create test support set
    support_data = {
        "support_v1": {
            "support_set_id": "support_v1",
            "name": "Test Support Set",
            "classes": {
                "class_0": {
                    "class_name": "Cat",
                    "images": [{"image_id": "img1", "annotation_ref": "img1"}]
                }
            },
            "total_images": 1
        }
    }
    save_json(SUPPORT_SETS_FILE, support_data)
    print("✓ Support set created")
    
    # Create test query set
    query_data = {
        "query_001": {
            "query_set_id": "query_001",
            "name": "Test Query Set",
            "images": [{"image_id": "test1", "filename": "test1.jpg"}],
            "total_images": 1
        }
    }
    save_json(QUERY_SETS_FILE, query_data)
    print("✓ Query set created")
    
    # Create test experiment
    exp_data = {
        "exp_001": {
            "experiment_id": "exp_001",
            "name": "Test Experiment",
            "support_set_id": "support_v1",
            "query_set_id": "query_001",
            "status": "created",
            "created_at": "2025-11-22T19:00:00"
        }
    }
    save_json(EXPERIMENTS_FILE, exp_data)
    print("✓ Experiment created")
    
def test_tracking():
    """Test tracking operations"""
    from routers.tracking import load_tracking, save_tracking, TRACKING_FILE
    
    print("\nTesting tracking operations...")
    
    tracking_data = {
        "img001": {
            "filename": "test.jpg",
            "stages": {
                "uploaded": {"timestamp": "2025-11-22T19:00:00", "status": "complete"}
            },
            "current_stage": "uploaded",
            "errors": []
        }
    }
    save_tracking(tracking_data)
    loaded = load_tracking()
    
    assert "img001" in loaded
    print("✓ Tracking operations working")

def test_data_integrity():
    """Test that all data files exist and are readable"""
    from routers.classification import (
        EXPERIMENTS_FILE, SUPPORT_SETS_FILE, QUERY_SETS_FILE,
        EXPERIMENT_RESULTS_FILE, ANNOTATIONS_FILE
    )
    from routers.tracking import TRACKING_FILE
    
    print("\nTesting data file integrity...")
    
    files = [
        EXPERIMENTS_FILE,
        SUPPORT_SETS_FILE,
        QUERY_SETS_FILE,
        EXPERIMENT_RESULTS_FILE,
        ANNOTATIONS_FILE,
        TRACKING_FILE
    ]
    
    for file_path in files:
        assert file_path.exists(), f"{file_path} does not exist"
        print(f"✓ {file_path.name} exists")

if __name__ == "__main__":
    print("=" * 60)
    print("ALA-Web Backend Test Suite")
    print("=" * 60)
    
    try:
        test_json_operations()
        test_experiment_creation()
        test_tracking()
        test_data_integrity()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        
        print("\nData files created:")
        print("- data/experiments.json")
        print("- data/support_sets.json")
        print("- data/query_sets.json")
        print("- data/tracking.json")
        
        print("\nYou can now test the frontend by:")
        print("1. Starting the frontend: cd ../frontend && npm run dev")
        print("2. The frontend will load test data from JSON files")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
