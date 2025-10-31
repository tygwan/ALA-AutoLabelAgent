#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
순수한 AutoDistill 베이스라인 vs Ground Truth 분석으로 Table 4, 5, 6 생성
"""

import os
import re
import pandas as pd
import numpy as np
from collections import defaultdict, Counter
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.metrics import precision_recall_fscore_support
import argparse
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_frame_info_from_filename(filename):
    """파일명에서 프레임 정보 추출"""
    match = re.match(r'(.+?)_obj\d+', filename)
    if match:
        return match.group(1)
    return None

def extract_object_index_from_filename(filename):
    """파일명에서 객체 인덱스 추출"""
    match = re.search(r'_obj(\d+)_', filename)
    if match:
        return int(match.group(1))
    return None

def get_ground_truth_mapping(gt_dir):
    """Ground Truth 디렉토리에서 파일 매핑 생성"""
    logger.info("Ground Truth 매핑 생성 중...")
    
    gt_mapping = {}
    class_folders = {
        'Class_0': 'Class_0',
        'Class_1': 'Class_1', 
        'Class_2': 'Class_2',
        'Class_3': 'Class_3',
        'unknown_egifence': 'unknown_egifence',
        'unknown_human': 'unknown_human',
        'unknown_road': 'unknown_road',
        'unknown_none': 'unknown_none'
    }
    
    gt_stats = Counter()
    
    for folder_name, gt_class in class_folders.items():
        folder_path = os.path.join(gt_dir, folder_name)
        if not os.path.exists(folder_path):
            logger.warning(f"Ground Truth 폴더가 존재하지 않습니다: {folder_path}")
            continue
            
        for filename in os.listdir(folder_path):
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            frame_name = extract_frame_info_from_filename(filename)
            obj_index = extract_object_index_from_filename(filename)
            
            if frame_name and obj_index is not None:
                key = (frame_name, obj_index)
                gt_mapping[key] = gt_class
                gt_stats[gt_class] += 1
    
    logger.info("Ground Truth 통계:")
    for gt_class, count in sorted(gt_stats.items()):
        logger.info(f"  {gt_class}: {count}개")
    
    return gt_mapping

def get_autodistill_mapping(autodistill_dir):
    """Autodistill 디렉토리에서 파일 매핑 생성"""
    logger.info("Autodistill 매핑 생성 중...")
    
    autodistill_mapping = {}
    class_folders = {
        'Class_0': 'Class_0',
        'Class_1': 'Class_1',
        'Class_2': 'Class_2',
        'Class_3': 'Class_3',
        'unknown_egifence': 'unknown_egifence',
        'unknown_human': 'unknown_human',
        'unknown_road': 'unknown_road',
        'unknown_none': 'unknown_none'
    }
    
    autodistill_stats = Counter()
    
    for folder_name, auto_class in class_folders.items():
        folder_path = os.path.join(autodistill_dir, folder_name)
        if not os.path.exists(folder_path):
            logger.warning(f"Autodistill 폴더가 존재하지 않습니다: {folder_path}")
            continue
            
        for filename in os.listdir(folder_path):
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            frame_name = extract_frame_info_from_filename(filename)
            obj_index = extract_object_index_from_filename(filename)
            
            if frame_name and obj_index is not None:
                key = (frame_name, obj_index)
                autodistill_mapping[key] = auto_class
                autodistill_stats[auto_class] += 1
    
    logger.info("Autodistill 통계:")
    for auto_class, count in sorted(autodistill_stats.items()):
        logger.info(f"  {auto_class}: {count}개")
    
    return autodistill_mapping

def create_confusion_matrix_data(autodistill_mapping, gt_mapping):
    """Confusion matrix 데이터 생성"""
    y_pred = []
    y_true = []
    detailed_data = []
    
    # 공통 키 찾기
    common_keys = set(autodistill_mapping.keys()) & set(gt_mapping.keys())
    logger.info(f"매칭된 샘플 수: {len(common_keys)}")
    
    if not common_keys:
        logger.error("매칭되는 데이터가 없습니다!")
        return None, None, None
    
    for key in common_keys:
        autodistill_class = autodistill_mapping[key]
        gt_class = gt_mapping[key]
        
        y_pred.append(autodistill_class)
        y_true.append(gt_class)
        
        detailed_data.append({
            'frame_name': key[0],
            'obj_index': key[1],
            'predicted': autodistill_class,
            'ground_truth': gt_class,
            'correct': autodistill_class == gt_class
        })
    
    return y_pred, y_true, detailed_data

def calculate_metrics(y_true, y_pred, labels):
    """성능 메트릭 계산"""
    # 전체 정확도
    accuracy = accuracy_score(y_true, y_pred)
    
    # 클래스별 정밀도, 재현율, F1 점수
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, average=None, zero_division=0
    )
    
    # 매크로 평균
    macro_precision = np.mean(precision)
    macro_recall = np.mean(recall)
    macro_f1 = np.mean(f1)
    
    # 가중 평균
    weighted_precision, weighted_recall, weighted_f1, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, average='weighted', zero_division=0
    )
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'support': support,
        'macro_precision': macro_precision,
        'macro_recall': macro_recall,
        'macro_f1': macro_f1,
        'weighted_precision': weighted_precision,
        'weighted_recall': weighted_recall,
        'weighted_f1': weighted_f1
    }

def create_table_4(metrics, labels):
    """Table 4: Overall Performance Metrics 생성"""
    print("\n" + "="*50)
    print("TABLE 4: Overall Performance Metrics (AutoDistill Baseline)")
    print("="*50)
    
    print(f"Overall Accuracy: {metrics['accuracy']:.4f}")
    print(f"Macro Precision:  {metrics['macro_precision']:.4f}")
    print(f"Macro Recall:     {metrics['macro_recall']:.4f}")
    print(f"Macro F1-Score:   {metrics['macro_f1']:.4f}")
    print(f"Weighted Precision: {metrics['weighted_precision']:.4f}")
    print(f"Weighted Recall:    {metrics['weighted_recall']:.4f}")
    print(f"Weighted F1-Score:  {metrics['weighted_f1']:.4f}")

def create_table_5(metrics, labels):
    """Table 5: Class-wise Performance Metrics 생성"""
    print("\n" + "="*80)
    print("TABLE 5: Class-wise Performance Metrics (AutoDistill Baseline)")
    print("="*80)
    
    # 헤더
    print(f"{'Class':<20} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10}")
    print("-" * 80)
    
    # 각 클래스별 성능
    for i, label in enumerate(labels):
        precision = metrics['precision'][i]
        recall = metrics['recall'][i]
        f1 = metrics['f1'][i]
        support = metrics['support'][i]
        
        print(f"{label:<20} {precision:<12.4f} {recall:<12.4f} {f1:<12.4f} {support:<10}")
    
    # 평균 성능
    print("-" * 80)
    print(f"{'Macro Avg':<20} {metrics['macro_precision']:<12.4f} {metrics['macro_recall']:<12.4f} {metrics['macro_f1']:<12.4f} {sum(metrics['support']):<10}")
    print(f"{'Weighted Avg':<20} {metrics['weighted_precision']:<12.4f} {metrics['weighted_recall']:<12.4f} {metrics['weighted_f1']:<12.4f} {sum(metrics['support']):<10}")

def create_table_6(y_true, y_pred, labels):
    """Table 6: Confusion Matrix 생성"""
    print("\n" + "="*50)
    print("TABLE 6: Confusion Matrix (AutoDistill Baseline)")
    print("="*50)
    
    # Confusion matrix 계산
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    # 헤더 출력
    header = "Predicted →".ljust(20)
    for label in labels:
        header += f"{label[:8]:<10}"
    print(header)
    print("Actual ↓".ljust(20) + "-" * (10 * len(labels)))
    
    # 각 행 출력
    for i, label in enumerate(labels):
        row = f"{label[:15]:<20}"
        for j in range(len(labels)):
            row += f"{cm[i, j]:<10}"
        print(row)
    
    # 정확도 계산 (대각선 합 / 전체 합)
    accuracy = np.trace(cm) / np.sum(cm)
    print(f"\nAccuracy: {accuracy:.4f}")

def main():
    parser = argparse.ArgumentParser(description='AutoDistill 베이스라인 성능 분석 및 Table 4,5,6 생성')
    parser.add_argument('--category', default='test_category', help='카테고리명')
    args = parser.parse_args()
    
    # 경로 설정
    base_path = f"data/{args.category}"
    autodistill_dir = os.path.join(base_path, '6.preprocessed')
    gt_dir = os.path.join(base_path, '7.results', 'ground_truth')
    
    print(f"AutoDistill 디렉토리: {autodistill_dir}")
    print(f"Ground Truth 디렉토리: {gt_dir}")
    
    try:
        # 1. 매핑 생성
        autodistill_mapping = get_autodistill_mapping(autodistill_dir)
        gt_mapping = get_ground_truth_mapping(gt_dir)
        
        # 2. Confusion matrix 데이터 생성
        y_pred, y_true, detailed_data = create_confusion_matrix_data(autodistill_mapping, gt_mapping)
        
        if y_pred is None:
            logger.error("분석할 데이터가 없습니다.")
            return
        
        # 3. 라벨 정의
        all_labels = sorted(set(y_true + y_pred))
        
        # 4. 메트릭 계산
        metrics = calculate_metrics(y_true, y_pred, all_labels)
        
        # 5. Table 생성
        create_table_4(metrics, all_labels)
        create_table_5(metrics, all_labels)
        create_table_6(y_true, y_pred, all_labels)
        
        print(f"\n✅ 분석 완료!")
        print(f"총 분석된 샘플 수: {len(y_pred)}")
        
    except Exception as e:
        logger.error(f"분석 중 오류 발생: {e}")
        raise

if __name__ == "__main__":
    main() 