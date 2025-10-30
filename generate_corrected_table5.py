#!/usr/bin/env python3
"""
Generate Corrected Table 5 with 4x4 Confusion Matrix

This script generates the corrected Table 5 based on the actual confusion matrix results:
- Within Target Classes: Number classified into target classes (4x4 confusion matrix)
- Manually Marked as Others: Number classified as "Unknown"
- Total: Sum of both
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path

def load_experiment_data(category="test_category", model="resnet", shot=1, threshold=0.70):
    """Load a specific experiment to analyze confusion matrix"""
    project_dir = Path("/home/ml/project-agi")
    comparison_file = project_dir / "data" / category / "7.results" / model / f"shot_{shot}" / f"threshold_{threshold:.2f}" / "comparison" / "comparison_summary.json"
    
    print(f"Loading experiment: shot_{shot}_threshold_{threshold}")
    print(f"File: {comparison_file}")
    
    try:
        with open(comparison_file, 'r') as f:
            data = json.load(f)
        
        print("✅ Data loaded successfully")
        return data
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def analyze_confusion_matrix(class_stats):
    """Analyze the full confusion matrix including Unknown classifications"""
    target_classes = ["Class_0", "Class_1", "Class_2", "Class_3"]
    
    print("\n📊 Analyzing Confusion Matrix...")
    
    # Create 4x4 confusion matrix for target classes
    confusion_4x4 = {}
    others_count = {}
    within_target_count = {}
    
    for true_class in target_classes:
        if true_class not in class_stats:
            continue
        
        stats = class_stats[true_class]
        total_class = stats.get("total", 0)
        correct = stats.get("correct", 0)  # Correctly classified as itself
        predicted_as = stats.get("predicted_as", {})
        
        print(f"\n🔍 {true_class}:")
        print(f"   Total: {total_class}")
        print(f"   Correctly predicted as {true_class}: {correct}")
        
        # Count predictions to other target classes
        within_target = correct  # Start with correct predictions
        others = 0
        
        for pred_class, count in predicted_as.items():
            print(f"   Predicted as {pred_class}: {count}")
            if pred_class in target_classes:
                within_target += count
            elif pred_class == "Unknown":
                others += count
        
        within_target_count[true_class] = within_target
        others_count[true_class] = others
        
        print(f"   📈 Within Target Classes: {within_target}")
        print(f"   📈 Marked as Others (Unknown): {others}")
        print(f"   📈 Total: {within_target + others}")
    
    return within_target_count, others_count

def generate_table5_corrected(within_target_count, others_count):
    """Generate corrected Table 5"""
    target_classes = ["Class_0", "Class_1", "Class_2", "Class_3"]
    data = []
    
    for class_name in target_classes:
        within_target = within_target_count.get(class_name, 0)
        manually_marked_others = others_count.get(class_name, 0)
        total = within_target + manually_marked_others
        
        data.append({
            "Class": class_name,
            "Within_Target_Classes": within_target,
            "Manually_Marked_Others": manually_marked_others,
            "Total": total
        })
    
    return pd.DataFrame(data)

def generate_detailed_confusion_matrix(class_stats):
    """Generate detailed 4x4 confusion matrix"""
    target_classes = ["Class_0", "Class_1", "Class_2", "Class_3"]
    
    # Initialize confusion matrix
    cm_data = []
    
    for true_class in target_classes:
        if true_class not in class_stats:
            continue
        
        stats = class_stats[true_class]
        correct = stats.get("correct", 0)
        predicted_as = stats.get("predicted_as", {})
        
        row = {"True_Class": true_class}
        
        # Add predictions for each target class
        for pred_class in target_classes:
            if pred_class == true_class:
                row[f"Predicted_{pred_class}"] = correct
            else:
                row[f"Predicted_{pred_class}"] = predicted_as.get(pred_class, 0)
        
        # Add Unknown predictions
        row["Predicted_Unknown"] = predicted_as.get("Unknown", 0)
        
        cm_data.append(row)
    
    return pd.DataFrame(cm_data)

def main():
    """Main function"""
    print("🚀 Generating Corrected Table 5...")
    
    # Load experiment data (using shot=1, threshold=0.70 as example)
    data = load_experiment_data(shot=1, threshold=0.70)
    
    if not data:
        print("❌ Failed to load experiment data")
        return
    
    class_stats = data.get("class_stats", {})
    
    # Analyze confusion matrix
    within_target_count, others_count = analyze_confusion_matrix(class_stats)
    
    # Generate corrected Table 5
    print("\n📊 Generating Corrected Table 5...")
    table5_corrected = generate_table5_corrected(within_target_count, others_count)
    
    # Generate detailed confusion matrix
    print("\n📊 Generating Detailed 4x4+1 Confusion Matrix...")
    detailed_cm = generate_detailed_confusion_matrix(class_stats)
    
    # Save results
    output_dir = Path("/home/ml/project-agi/data/test_category/7.results")
    
    # Save corrected Table 5
    table5_path = output_dir / "resnet_table5_corrected.csv"
    table5_corrected.to_csv(table5_path, index=False)
    print(f"✅ Saved Corrected Table 5 to {table5_path}")
    
    # Save detailed confusion matrix
    cm_path = output_dir / "resnet_detailed_confusion_matrix.csv"
    detailed_cm.to_csv(cm_path, index=False)
    print(f"✅ Saved Detailed Confusion Matrix to {cm_path}")
    
    # Display results
    print("\n📋 Corrected Table 5:")
    print(table5_corrected.to_string(index=False))
    
    print("\n📋 Detailed 4x4+1 Confusion Matrix:")
    print(detailed_cm.to_string(index=False))
    
    print(f"\n🎉 Corrected tables generated successfully!")
    print(f"📁 Files saved in: {output_dir}")

if __name__ == "__main__":
    main() 