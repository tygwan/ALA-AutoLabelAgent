#!/usr/bin/env python3
"""
Generate Complete Corrected Tables for All Experiments

This script generates corrected tables for all shot/threshold combinations:
- Table 5 corrected: Based on actual confusion matrix results
- 4x4 Confusion Matrix: Detailed classification results
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path

def load_all_experiments(category="test_category", model="resnet"):
    """Load all experiment results"""
    project_dir = Path("/home/ml/project-agi")
    model_dir = project_dir / "data" / category / "7.results" / model
    
    experiments = {}
    
    print(f"Loading experiments from {model_dir}")
    
    for shot_dir in model_dir.glob("shot_*"):
        if not shot_dir.is_dir():
            continue
        
        shot = int(shot_dir.name.split("_")[1])
        
        for threshold_dir in shot_dir.glob("threshold_*"):
            if not threshold_dir.is_dir():
                continue
            
            threshold = float(threshold_dir.name.split("_")[1])
            comparison_file = threshold_dir / "comparison" / "comparison_summary.json"
            
            if comparison_file.exists():
                try:
                    with open(comparison_file, 'r') as f:
                        data = json.load(f)
                    
                    exp_id = f"shot_{shot}_threshold_{threshold:.2f}"
                    experiments[exp_id] = {
                        "shot": shot,
                        "threshold": threshold,
                        "data": data
                    }
                    
                except Exception as e:
                    print(f"Error loading {comparison_file}: {e}")
    
    print(f"Loaded {len(experiments)} experiments")
    return experiments

def analyze_confusion_matrix_for_experiment(class_stats):
    """Analyze confusion matrix for a single experiment"""
    target_classes = ["Class_0", "Class_1", "Class_2", "Class_3"]
    
    within_target_count = {}
    others_count = {}
    confusion_matrix = {}
    
    for true_class in target_classes:
        if true_class not in class_stats:
            within_target_count[true_class] = 0
            others_count[true_class] = 0
            continue
        
        stats = class_stats[true_class]
        correct = stats.get("correct", 0)
        predicted_as = stats.get("predicted_as", {})
        
        # Count predictions to target classes (including correct)
        within_target = correct
        for pred_class, count in predicted_as.items():
            if pred_class in target_classes:
                within_target += count
        
        # Count predictions to Unknown
        others = predicted_as.get("Unknown", 0)
        
        within_target_count[true_class] = within_target
        others_count[true_class] = others
        
        # Store confusion matrix row
        confusion_row = {"True_Class": true_class}
        for pred_class in target_classes:
            if pred_class == true_class:
                confusion_row[f"Predicted_{pred_class}"] = correct
            else:
                confusion_row[f"Predicted_{pred_class}"] = predicted_as.get(pred_class, 0)
        confusion_row["Predicted_Unknown"] = others
        confusion_matrix[true_class] = confusion_row
    
    return within_target_count, others_count, confusion_matrix

def generate_table5_for_all_experiments(experiments):
    """Generate Table 5 for all experiments"""
    data = []
    target_classes = ["Class_0", "Class_1", "Class_2", "Class_3"]
    
    print("Generating corrected Table 5 for all experiments...")
    
    for exp_id, exp_data in experiments.items():
        shot = exp_data["shot"]
        threshold = exp_data["threshold"]
        class_stats = exp_data["data"].get("class_stats", {})
        
        within_target_count, others_count, _ = analyze_confusion_matrix_for_experiment(class_stats)
        
        # Add row for each class
        for class_name in target_classes:
            within_target = within_target_count.get(class_name, 0)
            manually_marked_others = others_count.get(class_name, 0)
            total = within_target + manually_marked_others
            
            data.append({
                "Shot": shot,
                "Threshold": threshold,
                "Class": class_name,
                "Within_Target_Classes": within_target,
                "Manually_Marked_Others": manually_marked_others,
                "Total": total
            })
    
    df = pd.DataFrame(data)
    df = df.sort_values(by=["Shot", "Threshold", "Class"])
    
    print(f"Generated Table 5 with {len(df)} rows")
    return df

def generate_confusion_matrices_for_all_experiments(experiments):
    """Generate detailed confusion matrices for all experiments"""
    all_cm_data = []
    target_classes = ["Class_0", "Class_1", "Class_2", "Class_3"]
    
    print("Generating confusion matrices for all experiments...")
    
    for exp_id, exp_data in experiments.items():
        shot = exp_data["shot"]
        threshold = exp_data["threshold"]
        class_stats = exp_data["data"].get("class_stats", {})
        
        _, _, confusion_matrix = analyze_confusion_matrix_for_experiment(class_stats)
        
        # Add shot and threshold to each row
        for true_class in target_classes:
            if true_class in confusion_matrix:
                row = {
                    "Shot": shot,
                    "Threshold": threshold,
                    **confusion_matrix[true_class]
                }
                all_cm_data.append(row)
    
    df = pd.DataFrame(all_cm_data)
    df = df.sort_values(by=["Shot", "Threshold", "True_Class"])
    
    print(f"Generated confusion matrices with {len(df)} rows")
    return df

def main():
    """Main function"""
    print("🚀 Starting Complete Corrected Tables Generation...")
    
    # Load all experiments
    experiments = load_all_experiments()
    
    if not experiments:
        print("❌ No experiments found!")
        return
    
    # Define output directory
    output_dir = Path("/home/ml/project-agi/data/test_category/7.results")
    
    # Generate corrected Table 5 for all experiments
    print("\n📊 Generating corrected Table 5 for all experiments...")
    table5_all = generate_table5_for_all_experiments(experiments)
    table5_all_path = output_dir / "resnet_table5_corrected_all_experiments.csv"
    table5_all.to_csv(table5_all_path, index=False)
    print(f"✅ Saved Table 5 (All Experiments) to {table5_all_path}")
    
    # Generate confusion matrices for all experiments
    print("\n📊 Generating confusion matrices for all experiments...")
    cm_all = generate_confusion_matrices_for_all_experiments(experiments)
    cm_all_path = output_dir / "resnet_confusion_matrices_all_experiments.csv"
    cm_all.to_csv(cm_all_path, index=False)
    print(f"✅ Saved Confusion Matrices (All Experiments) to {cm_all_path}")
    
    # Generate summary statistics
    print("\n📊 Generating summary statistics...")
    
    # Summary by Shot/Threshold
    summary_data = []
    for exp_id, exp_data in experiments.items():
        shot = exp_data["shot"]
        threshold = exp_data["threshold"]
        class_stats = exp_data["data"].get("class_stats", {})
        
        within_target_count, others_count, _ = analyze_confusion_matrix_for_experiment(class_stats)
        
        total_within_target = sum(within_target_count.values())
        total_others = sum(others_count.values())
        total_all = total_within_target + total_others
        
        summary_data.append({
            "Shot": shot,
            "Threshold": threshold,
            "Total_Within_Target_Classes": total_within_target,
            "Total_Marked_As_Others": total_others,
            "Total_Classified": total_all,
            "Within_Target_Percentage": round(total_within_target / total_all * 100, 2) if total_all > 0 else 0,
            "Others_Percentage": round(total_others / total_all * 100, 2) if total_all > 0 else 0
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_df = summary_df.sort_values(by=["Shot", "Threshold"])
    summary_path = output_dir / "resnet_classification_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    print(f"✅ Saved Classification Summary to {summary_path}")
    
    print(f"\n🎉 All corrected tables generated successfully!")
    print(f"📁 Output directory: {output_dir}")
    print(f"📄 Files created:")
    print(f"   - resnet_table5_corrected_all_experiments.csv ({len(table5_all)} rows)")
    print(f"   - resnet_confusion_matrices_all_experiments.csv ({len(cm_all)} rows)")
    print(f"   - resnet_classification_summary.csv ({len(summary_df)} rows)")
    
    # Display sample results
    print(f"\n📋 Sample Table 5 (first 10 rows):")
    print(table5_all.head(10).to_string(index=False))
    
    print(f"\n📋 Classification Summary (first 10 rows):")
    print(summary_df.head(10).to_string(index=False))

if __name__ == "__main__":
    main() 