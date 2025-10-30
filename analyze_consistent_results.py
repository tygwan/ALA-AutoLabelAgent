#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
동일 데이터셋 기준 AutoDistill vs Few-Shot Learning 성능 비교
"""

import os
import json
import pandas as pd
import numpy as np
from collections import defaultdict, Counter
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.metrics import precision_recall_fscore_support

def get_ground_truth_mapping():
    """Ground Truth 매핑 생성"""
    print("=== Ground Truth 매핑 생성 ===")
    
    gt_dir = "data/test_category/7.results/ground_truth"
    gt_mapping = {}
    gt_stats = Counter()
    
    class_folders = ["Class_0", "Class_1", "Class_2", "Class_3", 
                    "unknown_egifence", "unknown_human", "unknown_none", "unknown_road"]
    
    for class_folder in class_folders:
        class_path = os.path.join(gt_dir, class_folder)
        if os.path.exists(class_path):
            files = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            for filename in files:
                gt_mapping[filename] = class_folder
                gt_stats[class_folder] += 1
            print(f"  {class_folder}: {len(files)}개")
    
    print(f"Ground Truth 총 파일 수: {len(gt_mapping)}")
    return gt_mapping, gt_stats

def get_autodistill_predictions():
    """AutoDistill 베이스라인 예측 결과 매핑 생성"""
    print("\n=== AutoDistill 베이스라인 예측 결과 ===")
    
    # 6.preprocessed 디렉토리에서 AutoDistill 분류 결과 수집
    preprocessed_dir = "data/test_category/6.preprocessed"
    autodistill_mapping = {}
    autodistill_stats = Counter()
    
    class_folders = ["Class_0", "Class_1", "Class_2", "Class_3", 
                    "unknown_egifence", "unknown_human", "unknown_none", "unknown_road"]
    
    for class_folder in class_folders:
        class_path = os.path.join(preprocessed_dir, class_folder)
        if os.path.exists(class_path):
            files = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            for filename in files:
                autodistill_mapping[filename] = class_folder
                autodistill_stats[class_folder] += 1
            print(f"  {class_folder}: {len(files)}개")
    
    print(f"AutoDistill 총 파일 수: {len(autodistill_mapping)}")
    return autodistill_mapping, autodistill_stats

def get_few_shot_predictions(shot=1, threshold=0.5):
    """Few-Shot Learning 예측 결과 매핑 생성"""
    print(f"\n=== Few-Shot Learning 예측 결과 (Shot: {shot}, Threshold: {threshold}) ===")
    
    few_shot_dir = f"data/test_category/7.results/resnet/shot_{shot}/threshold_{threshold:.2f}"
    few_shot_mapping = {}
    few_shot_stats = Counter()
    
    if os.path.exists(few_shot_dir):
        for item in os.listdir(few_shot_dir):
            item_path = os.path.join(few_shot_dir, item)
            if os.path.isdir(item_path) and item not in ["annotations_by_class", "comparison"]:
                files = [f for f in os.listdir(item_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                for filename in files:
                    few_shot_mapping[filename] = item
                    few_shot_stats[item] += 1
                print(f"  {item}: {len(files)}개")
    
    print(f"Few-Shot 총 파일 수: {len(few_shot_mapping)}")
    return few_shot_mapping, few_shot_stats

def normalize_class_names(class_name):
    """클래스명 정규화"""
    if class_name == "Unknown":
        return "Unknown"
    elif class_name.startswith("Class_"):
        return class_name
    elif class_name.startswith("unknown_"):
        return "Unknown"
    else:
        return class_name

def create_comparison_data(gt_mapping, autodistill_mapping, few_shot_mapping):
    """비교 데이터 생성"""
    print("\n=== 비교 데이터 생성 ===")
    
    # 공통 파일들만 사용
    common_files = set(gt_mapping.keys()) & set(autodistill_mapping.keys()) & set(few_shot_mapping.keys())
    print(f"공통 파일 수: {len(common_files)}")
    
    comparison_data = []
    
    for filename in common_files:
        gt_class = gt_mapping[filename]
        autodistill_class = autodistill_mapping[filename]
        few_shot_class = few_shot_mapping[filename]
        
        # 클래스명 정규화
        gt_normalized = normalize_class_names(gt_class)
        autodistill_normalized = normalize_class_names(autodistill_class)
        few_shot_normalized = normalize_class_names(few_shot_class)
        
        comparison_data.append({
            'filename': filename,
            'ground_truth': gt_normalized,
            'autodistill_pred': autodistill_normalized,
            'few_shot_pred': few_shot_normalized,
            'autodistill_correct': gt_normalized == autodistill_normalized,
            'few_shot_correct': gt_normalized == few_shot_normalized
        })
    
    return pd.DataFrame(comparison_data)

def calculate_performance_metrics(df):
    """성능 메트릭 계산"""
    print("\n=== 성능 메트릭 계산 ===")
    
    # 전체 정확도
    autodistill_accuracy = df['autodistill_correct'].mean()
    few_shot_accuracy = df['few_shot_correct'].mean()
    
    print(f"AutoDistill 정확도: {autodistill_accuracy:.4f} ({autodistill_accuracy*100:.2f}%)")
    print(f"Few-Shot 정확도: {few_shot_accuracy:.4f} ({few_shot_accuracy*100:.2f}%)")
    print(f"성능 개선: {few_shot_accuracy - autodistill_accuracy:.4f} ({(few_shot_accuracy - autodistill_accuracy)*100:.2f}%p)")
    
    # 클래스별 정확도
    print("\n클래스별 정확도:")
    for class_name in sorted(df['ground_truth'].unique()):
        class_df = df[df['ground_truth'] == class_name]
        auto_acc = class_df['autodistill_correct'].mean()
        fs_acc = class_df['few_shot_correct'].mean()
        print(f"  {class_name}: AutoDistill {auto_acc:.4f} vs Few-Shot {fs_acc:.4f} (개선: {fs_acc-auto_acc:.4f})")
    
    return {
        'autodistill_accuracy': autodistill_accuracy,
        'few_shot_accuracy': few_shot_accuracy,
        'improvement': few_shot_accuracy - autodistill_accuracy
    }

def create_confusion_matrices(df):
    """Confusion Matrix 생성"""
    print("\n=== Confusion Matrix 생성 ===")
    
    labels = sorted(df['ground_truth'].unique())
    
    # AutoDistill Confusion Matrix
    cm_auto = confusion_matrix(df['ground_truth'], df['autodistill_pred'], labels=labels)
    
    # Few-Shot Confusion Matrix  
    cm_fs = confusion_matrix(df['ground_truth'], df['few_shot_pred'], labels=labels)
    
    return cm_auto, cm_fs, labels

def save_results(df, metrics, cm_auto, cm_fs, labels):
    """결과 저장"""
    print("\n=== 결과 저장 ===")
    
    # 1. 상세 비교 데이터
    df.to_csv("autodistill_vs_few_shot_comparison.csv", index=False)
    print("✓ autodistill_vs_few_shot_comparison.csv")
    
    # 2. 성능 요약
    summary = {
        "total_files": len(df),
        "autodistill_accuracy": metrics['autodistill_accuracy'],
        "few_shot_accuracy": metrics['few_shot_accuracy'], 
        "performance_improvement": metrics['improvement'],
        "confusion_matrix_autodistill": cm_auto.tolist(),
        "confusion_matrix_few_shot": cm_fs.tolist(),
        "class_labels": labels
    }
    
    with open("performance_comparison_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print("✓ performance_comparison_summary.json")
    
    # 3. Confusion Matrix CSV
    cm_auto_df = pd.DataFrame(cm_auto, index=labels, columns=labels)
    cm_fs_df = pd.DataFrame(cm_fs, index=labels, columns=labels)
    
    cm_auto_df.to_csv("autodistill_confusion_matrix.csv")
    cm_fs_df.to_csv("few_shot_confusion_matrix.csv")
    print("✓ confusion matrix CSV 파일들")

def main():
    """메인 함수"""
    print("AutoDistill vs Few-Shot Learning 성능 비교 분석")
    print("=" * 60)
    
    # 1. Ground Truth 매핑
    gt_mapping, gt_stats = get_ground_truth_mapping()
    
    # 2. AutoDistill 예측 결과
    autodistill_mapping, autodistill_stats = get_autodistill_predictions()
    
    # 3. Few-Shot Learning 예측 결과 (Shot 1, Threshold 0.5)
    few_shot_mapping, few_shot_stats = get_few_shot_predictions(shot=1, threshold=0.5)
    
    # 4. 비교 데이터 생성
    df = create_comparison_data(gt_mapping, autodistill_mapping, few_shot_mapping)
    
    # 5. 성능 메트릭 계산
    metrics = calculate_performance_metrics(df)
    
    # 6. Confusion Matrix 생성
    cm_auto, cm_fs, labels = create_confusion_matrices(df)
    
    # 7. 결과 저장
    save_results(df, metrics, cm_auto, cm_fs, labels)
    
    print(f"\n🎉 분석 완료! 총 {len(df)}개 파일 분석됨")
    
    return df, metrics

if __name__ == "__main__":
    df, metrics = main() 