#!/usr/bin/env python3
"""
ResNet Results Table Generator (Fixed Version)

This script generates comprehensive ResNet classification results in the format specified:
- Table 4: Ground truth distribution (excluding unknown)
- Table 5: Data composition (within target classes / manually marked as "others" / total)
- Table 6: Performance metrics (Precision, Recall, Macro balanced accuracy, Macro F1-score, Macro MCC, Macro Fall-out)
- Binary Confusion Matrix: TP, TN, FP, FN for each class with specified column names

Usage:
  python3 generate_resnet_results_tables_v2.py --category=test_category
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Generate ResNet Results Tables')
    parser.add_argument('--category', type=str, required=True, help='Category name')
    parser.add_argument('--output', type=str, default='7.results', help='Output directory within category')
    parser.add_argument('--model', type=str, default='resnet', help='Model name (default: resnet)')
    return parser.parse_args()

class ResNetResultsGenerator:
    """ResNet 결과 테이블 생성기 (간소화 버전)"""
    
    def __init__(self, category: str, output_dir: str = "7.results", model: str = "resnet"):
        self.category = category
        self.model = model
        self.project_dir = Path("/home/ml/project-agi")
        self.data_dir = self.project_dir / "data" / category
        self.results_dir = self.data_dir / output_dir
        self.model_dir = self.results_dir / model
        self.output_dir = self.results_dir
        
        # Class names (based on actual data)
        self.target_classes = ["Class_0", "Class_1", "Class_2", "Class_3"]
        self.all_classes = self.target_classes + ["Unknown"]
        
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
            logger.info(f"Processing shot {shot}")
            
            for threshold_dir in shot_dir.glob("threshold_*"):
                if not threshold_dir.is_dir():
                    continue
                
                threshold = float(threshold_dir.name.split("_")[1])
                
                # Load comparison results
                comparison_file = threshold_dir / "comparison" / "comparison_summary.json"
                if not comparison_file.exists():
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
        count = 0
        
        for class_name, metrics in class_metrics.items():
            if class_name == "Unknown":  # Skip unknown for macro calculations
                continue
            
            total_metrics["precision"] += metrics["precision"]
            total_metrics["recall"] += metrics["recall"]
            total_metrics["f1_score"] += metrics["f1_score"]
            total_metrics["fallout"] += metrics["fallout"]
            count += 1
        
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
            if class_name == "Unknown":
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
    
    def generate_comprehensive_table(self) -> pd.DataFrame:
        """Generate comprehensive table with all data"""
        data = []
        
        logger.info("Generating comprehensive results table...")
        
        for exp_id, exp_data in self.experiment_results.items():
            shot = exp_data["shot"]
            threshold = exp_data["threshold"]
            class_stats = exp_data["data"].get("class_stats", {})
            
            logger.info(f"Processing {exp_id}")
            
            # Calculate per-class metrics
            class_metrics = {}
            for class_name in self.target_classes:
                class_metrics[class_name] = self.calculate_confusion_matrix(class_stats, class_name)
            
            # Calculate macro metrics
            macro_metrics = self.calculate_macro_metrics(class_metrics)
            
            # Add row for each class
            for class_name in self.target_classes:
                metrics = class_metrics[class_name]
                
                data.append({
                    "Model": self.model,
                    "Shot": shot,
                    "Threshold": threshold,
                    "Class": class_name,
                    "TP": metrics["TP"],
                    "TN": metrics["TN"],
                    "FP": metrics["FP"],
                    "FN": metrics["FN"],
                    "PREDICTED_CLASS": metrics["TP"],
                    "PREDICTED_NOT_CLASS": metrics["FN"],
                    "GT_CLASS": metrics["TP"] + metrics["FN"],
                    "GT_NOT_CLASS": metrics["TN"] + metrics["FP"],
                    "Precision": round(metrics["precision"], 2),
                    "Recall": round(metrics["recall"], 2),
                    "F1_Score": round(metrics["f1_score"], 2),
                    "Specificity": round(metrics["specificity"], 2),
                    "Fallout": round(metrics["fallout"], 2),
                    "Macro_Precision": round(macro_metrics.get("macro_precision", 0), 2),
                    "Macro_Recall": round(macro_metrics.get("macro_recall", 0), 2),
                    "Macro_Balanced_Accuracy": round(macro_metrics.get("macro_balanced_accuracy", 0), 2),
                    "Macro_F1_Score": round(macro_metrics.get("macro_f1", 0), 2),
                    "Macro_MCC": round(macro_metrics.get("macro_mcc", 0), 2),
                    "Macro_Fallout": round(macro_metrics.get("macro_fallout", 0), 2)
                })
        
        df = pd.DataFrame(data)
        df = df.sort_values(by=["Shot", "Threshold", "Class"])
        logger.info(f"Generated table with {len(df)} rows")
        return df
    
    def generate_ground_truth_table(self) -> pd.DataFrame:
        """Generate Table 4: Ground truth distribution"""
        data = []
        
        for class_name in self.target_classes:
            if class_name in self.ground_truth_data:
                data.append({
                    "Class": class_name,
                    "Ground_Truth_Count": self.ground_truth_data[class_name]
                })
        
        return pd.DataFrame(data)
    
    def save_all_tables(self):
        """Save all tables to CSV files"""
        logger.info("Starting table generation...")
        
        if not self.load_experiment_results():
            logger.error("Failed to load experiment results")
            return False
        
        if not self.load_ground_truth_data():
            logger.error("Failed to load ground truth data")
            return False
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        try:
            # Generate and save comprehensive table
            logger.info("Generating comprehensive table...")
            comprehensive_df = self.generate_comprehensive_table()
            comprehensive_path = self.output_dir / f"{self.model}_comprehensive_results.csv"
            comprehensive_df.to_csv(comprehensive_path, index=False)
            logger.info(f"✅ Saved Comprehensive Results to {comprehensive_path}")
            
            # Generate and save ground truth table
            logger.info("Generating ground truth table...")
            gt_df = self.generate_ground_truth_table()
            gt_path = self.output_dir / f"{self.model}_table4_ground_truth.csv"
            gt_df.to_csv(gt_path, index=False)
            logger.info(f"✅ Saved Table 4 (Ground Truth) to {gt_path}")
            
            # Generate performance metrics summary (aggregated by shot/threshold)
            logger.info("Generating performance summary...")
            summary_data = []
            
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
                
                summary_data.append({
                    "Model": self.model,
                    "Shot": shot,
                    "Threshold": threshold,
                    "Macro_Precision": round(macro_metrics.get("macro_precision", 0), 2),
                    "Macro_Recall": round(macro_metrics.get("macro_recall", 0), 2),
                    "Macro_Balanced_Accuracy": round(macro_metrics.get("macro_balanced_accuracy", 0), 2),
                    "Macro_F1_Score": round(macro_metrics.get("macro_f1", 0), 2),
                    "Macro_MCC": round(macro_metrics.get("macro_mcc", 0), 2),
                    "Macro_Fallout": round(macro_metrics.get("macro_fallout", 0), 2)
                })
            
            summary_df = pd.DataFrame(summary_data)
            summary_df = summary_df.sort_values(by=["Shot", "Threshold"])
            summary_path = self.output_dir / f"{self.model}_table6_performance_metrics.csv"
            summary_df.to_csv(summary_path, index=False)
            logger.info(f"✅ Saved Table 6 (Performance Metrics) to {summary_path}")
            
            logger.info("🎉 All tables generated successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error generating tables: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main function"""
    args = parse_args()
    
    logger.info(f"Starting ResNet results generation for category: {args.category}")
    
    generator = ResNetResultsGenerator(
        category=args.category,
        output_dir=args.output,
        model=args.model
    )
    
    success = generator.save_all_tables()
    
    if success:
        logger.info("✅ ResNet results tables generated successfully!")
    else:
        logger.error("❌ Failed to generate ResNet results tables")
        sys.exit(1)

if __name__ == "__main__":
    main() 