#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Few-Shot Learning vs Ground Truth 분석 (수정된 논리)

Table 8: FSL 예측 기준 분석
- FSL이 C1으로 예측한 것 중 실제 GT가 C1인 것 → Within
- FSL이 C1으로 예측한 것 중 실제 GT가 Unknown인 것 → Marked as Others
- Threshold 증가 → FSL 예측 수 감소 → Total 합계 감소

Table 7: 클래스별 혼동행렬 (Accuracy 제거)
"""

import os
import json
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
    raise FileNotFoundError("프로젝트 루트를 찾을 수 없습니다. 'data/test_category' 폴더를 확인하세요.")

PROJECT_ROOT = find_project_root()
print(f"🎯 프로젝트 루트: {PROJECT_ROOT}")

def get_available_experiments():
    """사용 가능한 Few-Shot Learning 실험 조합 찾기"""
    base_dir = os.path.join(PROJECT_ROOT, "data", "test_category", "7.results", "resnet")
    experiments = []
    if os.path.exists(base_dir):
        for shot_dir in sorted(os.listdir(base_dir)):
            if shot_dir.startswith("shot_"):
                shot = int(shot_dir.split("_")[1])
                shot_path = os.path.join(base_dir, shot_dir)
                for threshold_dir in sorted(os.listdir(shot_path)):
                    if threshold_dir.startswith("threshold_"):
                        threshold = float(threshold_dir.split("_")[1])
                        experiments.append((shot, threshold))
    print(f"발견된 실험 조합: {len(experiments)}개")
    return experiments

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
        return pred_mapping
    except Exception as e:
        print(f"  [!] 오류: {e}")
        return {}

def normalize_class_name(class_name):
    """클래스명 정규화"""
    if class_name is None or not isinstance(class_name, str):
        return None
    return "Unknown" if "unknown" in class_name.lower() else class_name

# --- 분석 함수 ---

def create_table7_confusion_matrix(gt_mapping, fsl_mapping):
    """Table 7: 클래스별 혼동행렬 (GT vs FSL 예측)"""
    
    common_files = set(gt_mapping.keys()) & set(fsl_mapping.keys())
    
    # 혼동행렬 생성 (GT 클래스별로 FSL이 어떻게 예측했는지)
    confusion_matrix = defaultdict(lambda: defaultdict(int))
    
    for filename in common_files:
        gt_raw = gt_mapping[filename]
        fsl_raw = fsl_mapping[filename]
        
        gt_class = normalize_class_name(gt_raw)
        fsl_class = normalize_class_name(fsl_raw)
        
        # GT 클래스가 Class_0~3인 경우만 분석 (Unknown 제외)
        if gt_class in ["Class_0", "Class_1", "Class_2", "Class_3"]:
            confusion_matrix[gt_class][fsl_class] += 1
    
    return confusion_matrix

def create_table8_fsl_based_analysis(gt_mapping, fsl_mapping):
    """Table 8: FSL 예측 기준 분석 (수정된 논리)"""
    
    common_files = set(gt_mapping.keys()) & set(fsl_mapping.keys())
    
    # FSL 예측 클래스별로 분석
    fsl_class_analysis = defaultdict(lambda: defaultdict(int))
    
    for filename in common_files:
        gt_raw = gt_mapping[filename]
        fsl_raw = fsl_mapping[filename]
        
        gt_class = normalize_class_name(gt_raw)
        fsl_class = normalize_class_name(fsl_raw)
        
        # FSL이 특정 클래스로 예측한 경우
        if fsl_class in ["Class_0", "Class_1", "Class_2", "Class_3"]:
            if gt_class == fsl_class:
                # FSL 예측과 GT가 일치 → Within
                fsl_class_analysis[fsl_class]['within'] += 1
            elif gt_class == "Unknown":
                # FSL은 클래스로 예측했지만 GT는 Unknown → Marked as Others
                fsl_class_analysis[fsl_class]['marked_as_others'] += 1
            else:
                # FSL은 클래스로 예측했지만 GT는 다른 클래스 → 오분류 (Within에 포함하지 않음)
                pass
    
    return fsl_class_analysis

# --- 메인 실행 로직 ---

def main():
    """메인 실행 함수"""
    print("Few-Shot Learning vs Ground Truth 분석 (수정된 논리)")
    print("=" * 65)
    
    experiments = get_available_experiments()
    gt_mapping = get_ground_truth_mapping()
    
    if not experiments or not gt_mapping:
        print("분석에 필요한 데이터가 부족합니다.")
        return
    
    print(f"\n📊 분석 시작: {len(experiments)}개 실험 조합 처리")
    
    table7_results = []  # 클래스별 혼동행렬
    table8_results = []  # FSL 예측 기준 분석
    
    for i, (shot, threshold) in enumerate(experiments, 1):
        print(f"\n[{i:2d}/{len(experiments)}] Shot={shot}, Threshold={threshold:.2f} 분석 중...")
        
        fsl_mapping = get_fsl_predictions(shot, threshold)
        if not fsl_mapping:
            print("  ⚠️  FSL 예측 데이터 없음. 건너뜁니다.")
            continue
        
        # Table 7: 클래스별 혼동행렬
        confusion_matrix = create_table7_confusion_matrix(gt_mapping, fsl_mapping)
        
        for gt_class in ["Class_0", "Class_1", "Class_2", "Class_3"]:
            table7_row = {
                'Shot': shot,
                'Threshold': threshold,
                'GT_Class': gt_class,
                'FSL_Class_0': confusion_matrix[gt_class]['Class_0'],
                'FSL_Class_1': confusion_matrix[gt_class]['Class_1'],
                'FSL_Class_2': confusion_matrix[gt_class]['Class_2'],
                'FSL_Class_3': confusion_matrix[gt_class]['Class_3'],
                'FSL_Unknown': confusion_matrix[gt_class]['Unknown'],
                'GT_Total': sum(confusion_matrix[gt_class].values())
            }
            table7_results.append(table7_row)
        
        # Table 8: FSL 예측 기준 분석
        fsl_analysis = create_table8_fsl_based_analysis(gt_mapping, fsl_mapping)
        
        true_class_map = {
            "Class_0": "Fence (C1)", "Class_1": "Sidewalk (C2)", 
            "Class_2": "Parked car (C3)", "Class_3": "Traffic cone (C4)"
        }
        
        for fsl_class in ["Class_0", "Class_1", "Class_2", "Class_3"]:
            within = fsl_analysis[fsl_class]['within']
            others = fsl_analysis[fsl_class]['marked_as_others']
            
            table8_row = {
                'Shot': shot,
                'Threshold': threshold,
                'Class': fsl_class,
                'True_Class': true_class_map[fsl_class],
                'Within_Target_Classes': within,
                'Manually_Marked_As_Others': others,
                'Total': within + others
            }
            table8_results.append(table8_row)
        
        # 진행 상황 출력 (Table 8 Total 합계)
        total_fsl_predictions = sum([fsl_analysis[cls]['within'] + fsl_analysis[cls]['marked_as_others'] 
                                   for cls in ["Class_0", "Class_1", "Class_2", "Class_3"]])
        print(f"  ✅ 완료 - FSL 클래스 예측 총계: {total_fsl_predictions}개")
    
    # 결과 저장
    print(f"\n📁 결과 파일 저장 중...")
    
    if table7_results:
        df_table7 = pd.DataFrame(table7_results)
        table7_path = os.path.join(PROJECT_ROOT, "final_table7_confusion_matrix.csv")
        df_table7.to_csv(table7_path, index=False)
        print(f"✅ Table 7 (혼동행렬) 저장: {table7_path}")
        print(f"   📈 총 {len(df_table7)} 행")
    
    if table8_results:
        df_table8 = pd.DataFrame(table8_results)
        table8_path = os.path.join(PROJECT_ROOT, "final_table8_fsl_based_analysis.csv")
        df_table8.to_csv(table8_path, index=False)
        print(f"✅ Table 8 (FSL 예측 기준) 저장: {table8_path}")
        print(f"   📈 총 {len(df_table8)} 행")
        
        # Threshold별 Total 감소 패턴 확인 (Shot=1 예시)
        print(f"\n--- Table 8 Total 감소 패턴 확인 (Shot=1) ---")
        shot1_table8 = df_table8[df_table8['Shot'] == 1].groupby('Threshold')['Total'].sum().sort_index()
        for threshold, total in shot1_table8.items():
            print(f"Threshold {threshold:.2f}: {int(total):5d}개")
    
    print(f"\n🎉 모든 작업 완료!")
    print(f"📊 처리된 실험 조합: {len(experiments)}개")
    print(f"📁 생성된 파일:")
    print(f"   - final_table7_confusion_matrix.csv (GT vs FSL 혼동행렬)")
    print(f"   - final_table8_fsl_based_analysis.csv (FSL 예측 기준 분석)")
    
    # 논리 검증 샘플 출력
    if table8_results:
        print(f"\n🔍 논리 검증 샘플 (Shot=1, Threshold=0.50):")
        sample = df_table8[(df_table8['Shot'] == 1) & (df_table8['Threshold'] == 0.50)]
        for _, row in sample.iterrows():
            print(f"  {row['Class']}: FSL이 {row['Class']}로 예측한 것 중")
            print(f"    - 실제로 {row['Class']}인 것: {row['Within_Target_Classes']}개")
            print(f"    - 실제로 Unknown인 것: {row['Manually_Marked_As_Others']}개")
            print(f"    - 총계: {row['Total']}개")

if __name__ == "__main__":
    main() 