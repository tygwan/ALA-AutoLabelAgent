#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table 7, 8 데이터 일관성 검증

- Few-Shot Learning 결과: 16,061장
- Ground Truth 결과: 16,061장
- Table 7, 8에서 실제 사용된 데이터 수량 검증
"""

import os
import pandas as pd
from collections import defaultdict, Counter

# --- 유틸리티 함수 ---

def find_project_root():
    """프로젝트 루트 디렉토리 찾기"""
    current_dir = os.getcwd()
    for i in range(4):
        path = os.path.join(current_dir, "data", "test_category")
        if os.path.exists(path):
            return os.path.abspath(current_dir)
        current_dir = os.path.dirname(current_dir)
    raise FileNotFoundError("프로젝트 루트를 찾을 수 없습니다.")

PROJECT_ROOT = find_project_root()
print(f"🎯 프로젝트 루트: {PROJECT_ROOT}")

def get_ground_truth_mapping():
    """Ground Truth 매핑 생성"""
    gt_dir = os.path.join(PROJECT_ROOT, "data", "test_category", "7.results", "ground_truth")
    gt_mapping = {}
    class_folders = ["Class_0", "Class_1", "Class_2", "Class_3", 
                    "unknown_egifence", "unknown_human", "unknown_none", "unknown_road"]
    
    gt_stats = Counter()
    for class_folder in class_folders:
        class_path = os.path.join(gt_dir, class_folder)
        if os.path.exists(class_path):
            for filename in os.listdir(class_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    gt_mapping[filename] = class_folder
                    gt_stats[class_folder] += 1
    
    print("Ground Truth 통계:")
    for class_name, count in sorted(gt_stats.items()):
        print(f"  {class_name}: {count}개")
    print(f"  총계: {sum(gt_stats.values())}개")
    
    return gt_mapping

def get_fsl_predictions(shot, threshold):
    """FSL 예측 결과 로드"""
    base_dir = os.path.join(PROJECT_ROOT, "data", "test_category", "7.results", "resnet",
                            f"shot_{shot}", f"threshold_{threshold:.2f}")
    
    predictions_csv = os.path.join(base_dir, "predictions.csv")
    if not os.path.exists(predictions_csv):
        return {}
    
    try:
        df = pd.read_csv(predictions_csv)
        pred_mapping = pd.Series(df['predicted_class'].values, index=df['image_filename']).to_dict()
        print(f"FSL 예측 결과 로드: {len(pred_mapping)}개 파일")
        return pred_mapping
    except Exception as e:
        print(f"  [!] 오류: {e}")
        return {}

def normalize_class_name(class_name):
    """클래스명 정규화"""
    if class_name is None or not isinstance(class_name, str):
        return None
    return "Unknown" if "unknown" in class_name.lower() else class_name

def verify_table_data_consistency(gt_mapping, fsl_mapping):
    """Table 데이터 일관성 검증"""
    
    print("\n=== 데이터 일관성 검증 ===")
    
    # 1. 기본 통계
    gt_files = set(gt_mapping.keys())
    fsl_files = set(fsl_mapping.keys())
    common_files = gt_files & fsl_files
    
    print(f"Ground Truth 파일 수: {len(gt_files)}개")
    print(f"FSL 예측 파일 수: {len(fsl_files)}개")
    print(f"공통 파일 수: {len(common_files)}개")
    
    # 2. 누락된 파일 확인
    gt_only = gt_files - fsl_files
    fsl_only = fsl_files - gt_files
    
    if gt_only:
        print(f"\n⚠️  GT에만 있는 파일: {len(gt_only)}개")
        if len(gt_only) <= 10:
            for f in list(gt_only)[:10]:
                print(f"    {f}")
    
    if fsl_only:
        print(f"\n⚠️  FSL에만 있는 파일: {len(fsl_only)}개")
        if len(fsl_only) <= 10:
            for f in list(fsl_only)[:10]:
                print(f"    {f}")
    
    # 3. Table 7 검증 (GT 클래스별 분석)
    print(f"\n=== Table 7 검증 (GT 기준) ===")
    gt_class_counts = Counter()
    table7_total = 0
    
    for filename in common_files:
        gt_raw = gt_mapping[filename]
        gt_class = normalize_class_name(gt_raw)
        
        # Table 7은 GT 클래스가 Class_0~3인 경우만 포함
        if gt_class in ["Class_0", "Class_1", "Class_2", "Class_3"]:
            gt_class_counts[gt_class] += 1
            table7_total += 1
    
    print("Table 7에 포함되는 파일 (GT 기준):")
    for gt_class in ["Class_0", "Class_1", "Class_2", "Class_3"]:
        print(f"  {gt_class}: {gt_class_counts[gt_class]}개")
    print(f"  Table 7 총계: {table7_total}개")
    
    # 4. Table 8 검증 (FSL 예측 기준)
    print(f"\n=== Table 8 검증 (FSL 예측 기준) ===")
    fsl_class_counts = Counter()
    table8_total = 0
    
    for filename in common_files:
        fsl_raw = fsl_mapping[filename]
        fsl_class = normalize_class_name(fsl_raw)
        
        # Table 8은 FSL이 Class_0~3으로 예측한 경우만 포함
        if fsl_class in ["Class_0", "Class_1", "Class_2", "Class_3"]:
            fsl_class_counts[fsl_class] += 1
            table8_total += 1
    
    print("Table 8에 포함되는 파일 (FSL 예측 기준):")
    for fsl_class in ["Class_0", "Class_1", "Class_2", "Class_3"]:
        print(f"  {fsl_class}: {fsl_class_counts[fsl_class]}개")
    print(f"  Table 8 총계: {table8_total}개")
    
    # 5. 전체 데이터 검증
    print(f"\n=== 전체 데이터 검증 ===")
    print(f"예상 총 파일 수: 16,061개")
    print(f"실제 공통 파일 수: {len(common_files)}개")
    print(f"일치 여부: {'✅ 일치' if len(common_files) == 16061 else '❌ 불일치'}")
    
    # 6. Unknown 클래스 분석
    print(f"\n=== Unknown 클래스 분석 ===")
    gt_unknown_count = 0
    fsl_unknown_count = 0
    
    for filename in common_files:
        gt_raw = gt_mapping[filename]
        fsl_raw = fsl_mapping[filename]
        
        gt_class = normalize_class_name(gt_raw)
        fsl_class = normalize_class_name(fsl_raw)
        
        if gt_class == "Unknown":
            gt_unknown_count += 1
        if fsl_class == "Unknown":
            fsl_unknown_count += 1
    
    print(f"GT Unknown: {gt_unknown_count}개")
    print(f"FSL Unknown: {fsl_unknown_count}개")
    print(f"GT Known: {len(common_files) - gt_unknown_count}개")
    print(f"FSL Known: {len(common_files) - fsl_unknown_count}개")
    
    return {
        'total_files': len(common_files),
        'table7_files': table7_total,
        'table8_files': table8_total,
        'gt_unknown': gt_unknown_count,
        'fsl_unknown': fsl_unknown_count,
        'is_16061': len(common_files) == 16061
    }

def main():
    """메인 실행 함수"""
    print("Table 7, 8 데이터 일관성 검증")
    print("=" * 50)
    
    # Ground Truth 로드
    gt_mapping = get_ground_truth_mapping()
    
    # 샘플 FSL 결과 로드 (Shot=1, Threshold=0.50)
    print(f"\n샘플 FSL 결과 로드 (Shot=1, Threshold=0.50):")
    fsl_mapping = get_fsl_predictions(1, 0.50)
    
    if not gt_mapping or not fsl_mapping:
        print("❌ 데이터 로드 실패")
        return
    
    # 데이터 일관성 검증
    result = verify_table_data_consistency(gt_mapping, fsl_mapping)
    
    # 결과 요약
    print(f"\n🎯 최종 검증 결과:")
    print(f"총 데이터 파일: {result['total_files']}개")
    print(f"Table 7 대상: {result['table7_files']}개 (GT Known 클래스)")
    print(f"Table 8 대상: {result['table8_files']}개 (FSL 클래스 예측)")
    print(f"16,061개 일치: {'✅ 예' if result['is_16061'] else '❌ 아니오'}")
    
    # 추가 실험 몇 개 더 확인
    print(f"\n=== 다른 실험 조합 검증 ===")
    test_experiments = [(1, 0.30), (10, 0.50), (30, 0.75)]
    
    for shot, threshold in test_experiments:
        fsl_test = get_fsl_predictions(shot, threshold)
        if fsl_test:
            common_test = set(gt_mapping.keys()) & set(fsl_test.keys())
            print(f"Shot={shot}, Threshold={threshold}: {len(common_test)}개 파일")
        else:
            print(f"Shot={shot}, Threshold={threshold}: 데이터 없음")

if __name__ == "__main__":
    main() 