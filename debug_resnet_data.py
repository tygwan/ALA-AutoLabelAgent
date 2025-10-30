#!/usr/bin/env python3
"""Debug ResNet data loading"""

import os
import json
from pathlib import Path

def check_resnet_data():
    project_dir = Path("/home/ml/project-agi")
    data_dir = project_dir / "data" / "test_category"
    results_dir = data_dir / "7.results"
    model_dir = results_dir / "resnet"
    
    print(f"Checking ResNet data in: {model_dir}")
    
    if not model_dir.exists():
        print(f"❌ Model directory not found: {model_dir}")
        return
    
    print(f"✅ Model directory found: {model_dir}")
    
    # Check shot directories
    shot_dirs = list(model_dir.glob("shot_*"))
    print(f"Found {len(shot_dirs)} shot directories:")
    
    experiment_count = 0
    
    for shot_dir in sorted(shot_dirs):
        if not shot_dir.is_dir():
            continue
        
        shot = int(shot_dir.name.split("_")[1])
        print(f"  📁 {shot_dir.name}")
        
        # Check threshold directories
        threshold_dirs = list(shot_dir.glob("threshold_*"))
        print(f"    Found {len(threshold_dirs)} threshold directories")
        
        for threshold_dir in sorted(threshold_dirs)[:3]:  # Just check first 3
            if not threshold_dir.is_dir():
                continue
            
            threshold = float(threshold_dir.name.split("_")[1])
            comparison_file = threshold_dir / "comparison" / "comparison_summary.json"
            
            if comparison_file.exists():
                try:
                    with open(comparison_file, 'r') as f:
                        data = json.load(f)
                    
                    print(f"    ✅ {threshold_dir.name}: {comparison_file.stat().st_size} bytes")
                    print(f"       Keys: {list(data.keys())}")
                    
                    if "class_stats" in data:
                        classes = list(data["class_stats"].keys())
                        print(f"       Classes: {classes}")
                    
                    experiment_count += 1
                    
                except Exception as e:
                    print(f"    ❌ {threshold_dir.name}: Error loading {e}")
            else:
                print(f"    ❌ {threshold_dir.name}: comparison_summary.json not found")
    
    print(f"\nTotal valid experiments found: {experiment_count}")
    
    # Check ground truth data
    gt_dir = results_dir / "ground_truth"
    if gt_dir.exists():
        print(f"\n✅ Ground truth directory found: {gt_dir}")
        for class_dir in gt_dir.iterdir():
            if class_dir.is_dir():
                image_count = len(list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.png")))
                print(f"  📁 {class_dir.name}: {image_count} images")
    else:
        print(f"\n❌ Ground truth directory not found: {gt_dir}")

if __name__ == "__main__":
    check_resnet_data() 