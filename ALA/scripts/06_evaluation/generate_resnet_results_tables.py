#!/usr/bin/env python3
"""
ResNet Results Table Generator

This script generates comprehensive ResNet classification results in the format specified:
- Table 4: Ground truth distribution (excluding unknown)
- Table 5: Data composition (within target classes / manually marked as "others" / total)
- Table 6: Performance metrics (Precision, Recall, Macro balanced accuracy, Macro F1-score, Macro MCC, Macro Fall-out)
- Binary Confusion Matrix: TP, TN, FP, FN for each class with specified column names

Usage:
  python generate_resnet_results_tables.py --category=test_category --output=7.results
"""

import os
import sys
import json
import argparse
import logging
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("resnet_results_tables.log")
    ]
)
logger = logging.getLogger(__name__)

# Add project directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
if project_dir not in sys.path:
    sys.path.append(project_dir)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Generate ResNet Results Tables')
    parser.add_argument('--category', type=str, required=True, help='Category name')
    parser.add_argument('--output', type=str, default='7.results', help='Output directory within category')
    parser.add_argument('--model', type=str, default='resnet', help='Model name (default: resnet)')
    return parser.parse_args()

class ResNetResultsGenerator:
    """ResNet 결과 테이블 생성기"""
    
    def __init__(self, category: str, output_dir: str = "7.results", model: str = "resnet"):
        self.category = category
        self.model = model
        self.project_dir = Path(project_dir)
        self.data_dir = self.project_dir / "data" / category
        self.results_dir = self.data_dir / output_dir
        self.model_dir = self.results_dir / model
        self.output_dir = self.results_dir
        
        # Class names (excluding unknown)
        self.target_classes = ["class_0", "class_1", "class_2", "class_3"]
        self.all_classes = self.target_classes + ["unknown"]
        
        # Results storage
        self.experiment_results = {}
        self.ground_truth_data = {}
        
    def load_experiment_results(self) -> bool:
        """Load all experiment results for the model"""
        if not self.model_dir.exists():
            logger.error(f"Model directory not found: {self.model_dir}")
            return False
        
        logger.info(f"Loading results from {self.model_dir}")
        
        # Load all shot/threshold combinations
        for shot_dir in self.model_dir.glob("shot_*"):
            if not shot_dir.is_dir():
                continue
            
            shot = int(shot_dir.name.split("_")[1])
            
            for threshold_dir in shot_dir.glob("threshold_*"):
                if not threshold_dir.is_dir():
                    continue
                
                threshold = float(threshold_dir.name.split("_")[1])
                
                # Load comparison results
                comparison_file = threshold_dir / "comparison" / "comparison_summary.json"
                if not comparison_file.exists():
                    logger.warning(f"Comparison file not found: {comparison_file}")
                    continue
                
                try:
                    with open(comparison_file, 'r') as f:
                        comparison_data = json.load(f)
                    
                    exp_id = f"shot_{shot}_threshold_{threshold:.2f}"
                    self.experiment_results[exp_id] = {
                        "shot": shot,
                        "threshold": threshold,
                        "data": comparison_data
                    }
                    
                    logger.info(f"Loaded experiment: {exp_id}")
                    
                except Exception as e:
                    logger.error(f"Error loading {comparison_file}: {e}")
                    continue
        
        logger.info(f"Loaded {len(self.experiment_results)} experiments")
        return len(self.experiment_results) > 0
    
    def load_ground_truth_data(self) -> bool:
        """Load ground truth data"""
        gt_dir = self.results_dir / "ground_truth"
        if not gt_dir.exists():
            logger.error(f"Ground truth directory not found: {gt_dir}")
            return False
        
        for class_name in self.all_classes:
            class_dir = gt_dir / class_name
            if class_dir.exists():
                image_files = list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.png"))
                self.ground_truth_data[class_name] = len(image_files)
                logger.info(f"Ground truth {class_name}: {len(image_files)} images")
        
        return len(self.ground_truth_data) > 0
    
    def calculate_confusion_matrix(self, class_stats: Dict, target_class: str) -> Dict:
        """Calculate binary confusion matrix for a specific class"""
        # Initialize counts
        tp = fp = fn = tn = 0
        
        # True Positives: correctly predicted as target class
        if target_class in class_stats:
            tp = class_stats[target_class].get("correct", 0)
        
        # False Negatives: target class predicted as other classes
        if target_class in class_stats:
            fn = class_stats[target_class].get("incorrect", 0)
        
        # False Positives: other classes predicted as target class
        for other_class, other_stats in class_stats.items():
            if other_class == target_class:
                continue
            
            predicted_as = other_stats.get("predicted_as", {})
            if target_class in predicted_as:
                fp += predicted_as[target_class]
        
        # True Negatives: other classes correctly not predicted as target class
        for other_class, other_stats in class_stats.items():
            if other_class == target_class:
                continue
            
            # Other class correctly predicted as itself
            tn += other_stats.get("correct", 0)
            
            # Other class incorrectly predicted as non-target classes
            predicted_as = other_stats.get("predicted_as", {})
            for pred_class, count in predicted_as.items():
                if pred_class != target_class:
                    tn += count
        
        # Calculate metrics
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        fallout = fp / (fp + tn) if (fp + tn) > 0 else 0
        
        return {
            "TP": tp,
            "TN": tn,
            "FP": fp,
            "FN": fn,
            "precision": precision * 100,  # Convert to percentage
            "recall": recall * 100,
            "specificity": specificity * 100,
            "f1_score": f1 * 100,
            "fallout": fallout * 100
        }
    
    def calculate_macro_metrics(self, class_metrics: Dict) -> Dict:
        """Calculate macro-averaged metrics"""
        if not class_metrics:
            return {}
        
        total_metrics = defaultdict(float)
        count = len(class_metrics)
        
        for class_name, metrics in class_metrics.items():
            if class_name == "unknown":  # Skip unknown for macro calculations
                count -= 1
                continue
            
            total_metrics["precision"] += metrics["precision"]
            total_metrics["recall"] += metrics["recall"]
            total_metrics["f1_score"] += metrics["f1_score"]
            total_metrics["fallout"] += metrics["fallout"]
        
        if count == 0:
            return {}
        
        # Calculate macro averages
        macro_metrics = {
            "macro_precision": total_metrics["precision"] / count,
            "macro_recall": total_metrics["recall"] / count,
            "macro_f1": total_metrics["f1_score"] / count,
            "macro_fallout": total_metrics["fallout"] / count
        }
        
        # Calculate macro balanced accuracy (average of recalls)
        macro_metrics["macro_balanced_accuracy"] = macro_metrics["macro_recall"]
        
        # Calculate MCC (Matthews Correlation Coefficient)
        # For macro MCC, we'll use the average of individual MCCs
        total_mcc = 0
        mcc_count = 0
        
        for class_name, metrics in class_metrics.items():
            if class_name == "unknown":
                continue
            
            tp = metrics["TP"]
            tn = metrics["TN"]
            fp = metrics["FP"]
            fn = metrics["FN"]
            
            # Calculate MCC for this class
            denominator = np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
            if denominator != 0:
                mcc = (tp * tn - fp * fn) / denominator
                total_mcc += mcc
                mcc_count += 1
        
        macro_metrics["macro_mcc"] = (total_mcc / mcc_count * 100) if mcc_count > 0 else 0
        
        return macro_metrics
    
    def generate_table_4_ground_truth(self) -> pd.DataFrame:
        """Generate Table 4: Ground truth distribution (excluding unknown)"""
        data = []
        
        for class_name in self.target_classes:
            if class_name in self.ground_truth_data:
                data.append({
                    "Class": class_name,
                    "Ground_Truth_Count": self.ground_truth_data[class_name]
                })
        
        df = pd.DataFrame(data)
        logger.info("Generated Table 4: Ground truth distribution")
        return df
    
    def generate_table_5_data_composition(self) -> pd.DataFrame:
        """Generate Table 5: Data composition for each class"""
        data = []
        
        # Calculate totals across all experiments (use first experiment as representative)
        if self.experiment_results:
            first_exp = list(self.experiment_results.values())[0]
            class_stats = first_exp["data"].get("class_stats", {})
            
            for class_name in self.target_classes:
                if class_name in class_stats:
                    # For now, we'll use the ground truth data as "within target classes"
                    # and calculate "others" based on the difference
                    within_target = self.ground_truth_data.get(class_name, 0)
                    manually_marked_others = 0  # This would need to be calculated from actual data
                    total = within_target + manually_marked_others
                    
                    data.append({
                        "Class": class_name,
                        "Within_Target_Classes": within_target,
                        "Manually_Marked_Others": manually_marked_others,
                        "Total": total
                    })
        
        df = pd.DataFrame(data)
        logger.info("Generated Table 5: Data composition")
        return df
    
    def generate_table_6_performance_metrics(self) -> pd.DataFrame:
        """Generate Table 6: Performance metrics for each shot/threshold combination"""
        data = []
        
        for exp_id, exp_data in self.experiment_results.items():
            shot = exp_data["shot"]
            threshold = exp_data["threshold"]
            class_stats = exp_data["data"].get("class_stats", {})
            
            # Calculate per-class metrics
            class_metrics = {}
            for class_name in self.target_classes:
                class_metrics[class_name] = self.calculate_confusion_matrix(class_stats, class_name)
            
            # Calculate macro metrics
            macro_metrics = self.calculate_macro_metrics(class_metrics)
            
            data.append({
                "Shot": shot,
                "Threshold": threshold,
                "Macro_Precision": macro_metrics.get("macro_precision", 0),
                "Macro_Recall": macro_metrics.get("macro_recall", 0),
                "Macro_Balanced_Accuracy": macro_metrics.get("macro_balanced_accuracy", 0),
                "Macro_F1_Score": macro_metrics.get("macro_f1", 0),
                "Macro_MCC": macro_metrics.get("macro_mcc", 0),
                "Macro_Fallout": macro_metrics.get("macro_fallout", 0)
            })
        
        df = pd.DataFrame(data)
        df = df.sort_values(by=["Shot", "Threshold"])
        logger.info("Generated Table 6: Performance metrics")
        return df
    
    def generate_binary_confusion_matrices(self) -> pd.DataFrame:
        """Generate binary confusion matrices for each class and experiment"""
        data = []
        
        for exp_id, exp_data in self.experiment_results.items():
            shot = exp_data["shot"]
            threshold = exp_data["threshold"]
            class_stats = exp_data["data"].get("class_stats", {})
            
            for class_name in self.target_classes:
                metrics = self.calculate_confusion_matrix(class_stats, class_name)
                
                data.append({
                    "Shot": shot,
                    "Threshold": threshold,
                    "Class": class_name,
                    "PREDICTED_CLASS": metrics["TP"],
                    "PREDICTED_NOT_CLASS": metrics["FN"],
                    "GT_CLASS": metrics["TP"] + metrics["FN"],
                    "GT_NOT_CLASS": metrics["TN"] + metrics["FP"],
                    "TP": metrics["TP"],
                    "TN": metrics["TN"],
                    "FP": metrics["FP"],
                    "FN": metrics["FN"],
                    "Precision": metrics["precision"],
                    "Recall": metrics["recall"],
                    "F1_Score": metrics["f1_score"],
                    "Specificity": metrics["specificity"],
                    "Fallout": metrics["fallout"]
                })
        
        df = pd.DataFrame(data)
        df = df.sort_values(by=["Shot", "Threshold", "Class"])
        logger.info("Generated Binary Confusion Matrices")
        return df
    
    def save_all_tables(self):
        """Save all tables to CSV files"""
        if not self.load_experiment_results():
            logger.error("Failed to load experiment results")
            return False
        
        if not self.load_ground_truth_data():
            logger.error("Failed to load ground truth data")
            return False
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        try:
            # Generate and save Table 4
            table4 = self.generate_table_4_ground_truth()
            table4_path = self.output_dir / f"{self.model}_table4_ground_truth.csv"
            table4.to_csv(table4_path, index=False)
            logger.info(f"Saved Table 4 to {table4_path}")
            
            # Generate and save Table 5
            table5 = self.generate_table_5_data_composition()
            table5_path = self.output_dir / f"{self.model}_table5_data_composition.csv"
            table5.to_csv(table5_path, index=False)
            logger.info(f"Saved Table 5 to {table5_path}")
            
            # Generate and save Table 6
            table6 = self.generate_table_6_performance_metrics()
            table6_path = self.output_dir / f"{self.model}_table6_performance_metrics.csv"
            table6.to_csv(table6_path, index=False)
            logger.info(f"Saved Table 6 to {table6_path}")
            
            # Generate and save Binary Confusion Matrices
            binary_cm = self.generate_binary_confusion_matrices()
            binary_cm_path = self.output_dir / f"{self.model}_binary_confusion_matrices.csv"
            binary_cm.to_csv(binary_cm_path, index=False)
            logger.info(f"Saved Binary Confusion Matrices to {binary_cm_path}")
            
            # Generate comprehensive combined table
            combined_data = []
            
            for exp_id, exp_data in self.experiment_results.items():
                shot = exp_data["shot"]
                threshold = exp_data["threshold"]
                class_stats = exp_data["data"].get("class_stats", {})
                
                # Calculate per-class metrics
                class_metrics = {}
                for class_name in self.target_classes:
                    class_metrics[class_name] = self.calculate_confusion_matrix(class_stats, class_name)
                
                # Calculate macro metrics
                macro_metrics = self.calculate_macro_metrics(class_metrics)
                
                # Add row for each class
                for class_name in self.target_classes:
                    metrics = class_metrics[class_name]
                    
                    combined_data.append({
                        "Model": self.model,
                        "Shot": shot,
                        "Threshold": threshold,
                        "Class": class_name,
                        "TP": metrics["TP"],
                        "TN": metrics["TN"],
                        "FP": metrics["FP"],
                        "FN": metrics["FN"],
                        "Precision": metrics["precision"],
                        "Recall": metrics["recall"],
                        "F1_Score": metrics["f1_score"],
                        "Specificity": metrics["specificity"],
                        "Fallout": metrics["fallout"],
                        "Macro_Precision": macro_metrics.get("macro_precision", 0),
                        "Macro_Recall": macro_metrics.get("macro_recall", 0),
                        "Macro_Balanced_Accuracy": macro_metrics.get("macro_balanced_accuracy", 0),
                        "Macro_F1_Score": macro_metrics.get("macro_f1", 0),
                        "Macro_MCC": macro_metrics.get("macro_mcc", 0),
                        "Macro_Fallout": macro_metrics.get("macro_fallout", 0)
                    })
            
            # Save comprehensive table
            combined_df = pd.DataFrame(combined_data)
            combined_df = combined_df.sort_values(by=["Shot", "Threshold", "Class"])
            combined_path = self.output_dir / f"{self.model}_comprehensive_results.csv"
            combined_df.to_csv(combined_path, index=False)
            logger.info(f"Saved Comprehensive Results to {combined_path}")
            
            logger.info("All tables generated successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error generating tables: {e}")
            return False

def main():
    """Main function"""
    args = parse_args()
    
    generator = ResNetResultsGenerator(
        category=args.category,
        output_dir=args.output,
        model=args.model
    )
    
    success = generator.save_all_tables()
    
    if success:
        logger.info("ResNet results tables generated successfully!")
    else:
        logger.error("Failed to generate ResNet results tables")
        sys.exit(1)

if __name__ == "__main__":
    main() 