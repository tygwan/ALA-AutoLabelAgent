#!/usr/bin/env python3
"""
Analyze Calculation Source and Differences

This script examines the original JSON data to understand where the calculation differences come from.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path

def load_original_json():
    """Load the original JSON data for shot=1, threshold=0.3"""
    json_file = Path("/home/ml/project-agi/data/test_category/7.results/resnet/shot_1/threshold_0.30/comparison/comparison_summary.json")
    
    print(f"📂 Loading original JSON: {json_file}")
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    print(f"✅ JSON loaded successfully")
    return data

def analyze_json_structure(data):
    """Analyze the structure of the JSON data"""
    
    print("\n" + "="*60)
    print("📊 JSON DATA STRUCTURE ANALYSIS")
    print("="*60)
    
    print(f"📋 Top-level keys: {list(data.keys())}")
    print(f"📋 Experiment ID: {data.get('experiment_id', 'N/A')}")
    print(f"📋 Total predictions: {data.get('total_predictions', 'N/A')}")
    print(f"📋 Accuracy: {data.get('accuracy', 'N/A')}")
    
    class_stats = data.get("class_stats", {})
    print(f"\n📊 Class statistics available for: {list(class_stats.keys())}")
    
    return class_stats

def analyze_class_details(class_stats):
    """Analyze detailed class statistics"""
    
    print("\n" + "="*60)
    print("🔍 DETAILED CLASS ANALYSIS")
    print("="*60)
    
    target_classes = ["Class_0", "Class_1", "Class_2", "Class_3"]
    
    for class_id in target_classes:
        if class_id not in class_stats:
            print(f"❌ {class_id} not found in class_stats")
            continue
        
        stats = class_stats[class_id]
        print(f"\n📋 {class_id} detailed breakdown:")
        print(f"   📊 Keys available: {list(stats.keys())}")
        
        correct = stats.get("correct", 0)
        incorrect = stats.get("incorrect", 0)  
        predicted_as = stats.get("predicted_as", {})
        
        print(f"   ✅ Correct predictions: {correct}")
        print(f"   ❌ Incorrect predictions: {incorrect}")
        print(f"   🔄 Predicted as breakdown: {predicted_as}")
        
        # Calculate totals
        total_predicted_as_others = sum(predicted_as.values())
        total_samples = correct + total_predicted_as_others
        
        print(f"   📈 Total predicted as others: {total_predicted_as_others}")
        print(f"   📈 Total samples for this class: {total_samples}")
        
        # Verify: incorrect should equal sum of predicted_as (excluding self-prediction)
        other_predictions = sum(count for pred_class, count in predicted_as.items() if pred_class != class_id)
        print(f"   🔍 Verification: incorrect ({incorrect}) vs other predictions ({other_predictions})")

def explain_binary_metric_calculation_differences(class_stats):
    """Explain why binary metrics differ between the two files"""
    
    print("\n" + "="*80)
    print("💡 EXPLANATION OF CALCULATION DIFFERENCES")
    print("="*80)
    
    print("\n🎯 KEY INSIGHT: Different scopes for binary classification metrics")
    print("\n1️⃣ COMPREHENSIVE FILE APPROACH:")
    print("   - Treats each class vs ALL OTHER CLASSES (including Unknown)")
    print("   - TN includes Unknown class samples not predicted as target")
    print("   - FP includes Unknown class samples predicted as target")
    
    print("\n2️⃣ UNIFIED FILE APPROACH:")
    print("   - Only considers the 4 target classes (Class_0, Class_1, Class_2, Class_3)")
    print("   - TN only includes target classes not predicted as target")
    print("   - FP only includes target classes predicted as target")
    print("   - Unknown class is completely excluded from binary metrics")
    
    target_classes = ["Class_0", "Class_1", "Class_2", "Class_3"]
    
    for class_id in target_classes:
        if class_id not in class_stats:
            continue
        
        stats = class_stats[class_id]
        class_name = {
            "Class_0": "Fence (C1)",
            "Class_1": "Sidewalk (C2)",
            "Class_2": "Parked car (C3)",
            "Class_3": "Traffic cone (C4)"
        }[class_id]
        
        print(f"\n📋 {class_name} ({class_id}) calculation breakdown:")
        
        correct = stats.get("correct", 0)
        predicted_as = stats.get("predicted_as", {})
        
        # TP is the same in both approaches
        tp = correct
        print(f"   TP (True Positive): {tp} ✅ SAME in both files")
        
        # FN calculation
        fn_target_only = sum(predicted_as.get(other_class, 0) for other_class in target_classes if other_class != class_id)
        fn_with_unknown = fn_target_only + predicted_as.get("Unknown", 0)
        
        print(f"   FN (False Negative):")
        print(f"      - Target classes only: {fn_target_only}")
        print(f"      - Including Unknown: {fn_with_unknown}")
        print(f"      - Unknown contribution: {predicted_as.get('Unknown', 0)}")
        
        # FP calculation (would need data from other classes)
        print(f"   FP (False Positive): Requires analyzing other classes predicting as {class_id}")
        
        # The key difference is inclusion/exclusion of Unknown class
        unknown_impact = predicted_as.get("Unknown", 0)
        print(f"   🎯 Unknown class impact on {class_name}: {unknown_impact} samples")

def show_table7_vs_table8_relationship(class_stats):
    """Show how Table 7 and Table 8 data relate to the source JSON"""
    
    print("\n" + "="*60)
    print("📊 TABLE 7 & 8 DATA SOURCE EXPLANATION")
    print("="*60)
    
    print("\nTable 7 (Within Target Classes vs Manually Marked Others):")
    print("- Shows distribution between target classes and Unknown")
    print("- 'Within Target Classes' = correct + predictions within target classes")
    print("- 'Manually Marked Others' = predictions as Unknown")
    
    print("\nTable 8 (4x4 Confusion Matrix):")
    print("- Shows only the 4x4 matrix within target classes")
    print("- Excludes Unknown class completely")
    print("- Each cell shows cross-predictions between target classes")
    
    target_classes = ["Class_0", "Class_1", "Class_2", "Class_3"]
    
    for class_id in target_classes:
        if class_id not in class_stats:
            continue
        
        stats = class_stats[class_id]
        class_name = {
            "Class_0": "Fence (C1)",
            "Class_1": "Sidewalk (C2)",
            "Class_2": "Parked car (C3)",
            "Class_3": "Traffic cone (C4)"
        }[class_id]
        
        correct = stats.get("correct", 0)
        predicted_as = stats.get("predicted_as", {})
        
        # Table 7 calculations
        within_target = correct + sum(predicted_as.get(other_class, 0) for other_class in target_classes if other_class != class_id)
        others = predicted_as.get("Unknown", 0)
        total = within_target + others
        
        print(f"\n📋 {class_name} source breakdown:")
        print(f"   JSON 'correct': {correct}")
        print(f"   JSON 'predicted_as': {predicted_as}")
        print(f"   → Table 7 'Within Target': {within_target}")
        print(f"   → Table 7 'Others': {others}")
        print(f"   → Table 7 'Total': {total}")

def main():
    """Main analysis function"""
    print("🚀 Analyzing Calculation Source and Differences...")
    
    # Load original JSON data
    data = load_original_json()
    
    # Analyze JSON structure
    class_stats = analyze_json_structure(data)
    
    # Analyze class details
    analyze_class_details(class_stats)
    
    # Explain calculation differences
    explain_binary_metric_calculation_differences(class_stats)
    
    # Show Table 7 & 8 relationship
    show_table7_vs_table8_relationship(class_stats)
    
    print("\n" + "="*80)
    print("🎯 CONCLUSION")
    print("="*80)
    print("\n✅ COMPREHENSIVE FILE:")
    print("   - Uses traditional binary classification approach")
    print("   - Includes Unknown class in TN and FP calculations")
    print("   - More conservative precision due to Unknown class FP")
    
    print("\n✅ UNIFIED FILE:")
    print("   - Uses target-class-only approach")
    print("   - Excludes Unknown class from binary metrics")
    print("   - Higher precision due to Unknown class exclusion")
    print("   - Focuses on performance within the defined target classes")
    
    print("\n💡 BOTH APPROACHES ARE VALID:")
    print("   - Comprehensive: Traditional multi-class vs rest approach")
    print("   - Unified: Target-specific performance evaluation")
    print("   - Choice depends on evaluation purpose")

if __name__ == "__main__":
    main() 