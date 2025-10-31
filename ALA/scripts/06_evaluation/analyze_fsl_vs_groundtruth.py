#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Few-Shot Learning vs Ground Truth 직접 대조 분석

- FSL 결과를 Ground Truth와 직접 비교하여 성능 분석
- Threshold 증가에 따른 보수적 예측 경향 분석
- Table 8 Total 값의 감소 패턴 확인 (이상적인 경우)
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

def analyze_fsl_vs_groundtruth(gt_mapping, fsl_mapping):
    """FSL vs Ground Truth 직접 대조 분석"""
    
    # 매칭되는 파일들만 분석
    common_files = set(gt_mapping.keys()) & set(fsl_mapping.keys())
    
    analysis = {
        'total_files': len(common_files),
        'gt_distribution': Counter(),
        'fsl_distribution': Counter(),
        'confusion_matrix': defaultdict(lambda: defaultdict(int)),
        'gt_class_performance': defaultdict(lambda: defaultdict(int)),
        'accuracy_by_gt_class': {},
        'overall_accuracy': 0
    }
    
    correct_predictions = 0
    
    for filename in common_files:
        gt_raw = gt_mapping[filename]
        fsl_raw = fsl_mapping[filename]
        
        gt_class = normalize_class_name(gt_raw)
        fsl_class = normalize_class_name(fsl_raw)
        
        # 통계 수집
        analysis['gt_distribution'][gt_class] += 1
        analysis['fsl_distribution'][fsl_class] += 1
        analysis['confusion_matrix'][gt_class][fsl_class] += 1
        
        # Ground Truth 클래스별 성능 분석
        if gt_class in ["Class_0", "Class_1", "Class_2", "Class_3"]:
            analysis['gt_class_performance'][gt_class]['total'] += 1
            
            if gt_class == fsl_class:
                analysis['gt_class_performance'][gt_class]['correct'] += 1
                correct_predictions += 1
            elif fsl_class in ["Class_0", "Class_1", "Class_2", "Class_3"]:
                analysis['gt_class_performance'][gt_class]['wrong_class'] += 1
            elif fsl_class == "Unknown":
                analysis['gt_class_performance'][gt_class]['predicted_unknown'] += 1
        elif gt_class == "Unknown":
            if fsl_class == "Unknown":
                correct_predictions += 1
    
    # 클래스별 정확도 계산
    for gt_class in ["Class_0", "Class_1", "Class_2", "Class_3"]:
        perf = analysis['gt_class_performance'][gt_class]
        if perf['total'] > 0:
            analysis['accuracy_by_gt_class'][gt_class] = perf['correct'] / perf['total']
        else:
            analysis['accuracy_by_gt_class'][gt_class] = 0.0
    
    # 전체 정확도
    analysis['overall_accuracy'] = correct_predictions / len(common_files) if common_files else 0.0
    
    return analysis

def create_table8_style_analysis(gt_mapping, fsl_mapping):
    """Table 8 스타일 분석: GT 클래스별 FSL 예측 분포"""
    
    common_files = set(gt_mapping.keys()) & set(fsl_mapping.keys())
    
    # GT 클래스별로 FSL이 어떻게 예측했는지 분석
    gt_class_analysis = defaultdict(lambda: defaultdict(int))
    
    for filename in common_files:
        gt_raw = gt_mapping[filename]
        fsl_raw = fsl_mapping[filename]
        
        gt_class = normalize_class_name(gt_raw)
        fsl_class = normalize_class_name(fsl_raw)
        
        if gt_class in ["Class_0", "Class_1", "Class_2", "Class_3"]:
            if fsl_class in ["Class_0", "Class_1", "Class_2", "Class_3"]:
                gt_class_analysis[gt_class]['within_target'] += 1
            elif fsl_class == "Unknown":
                gt_class_analysis[gt_class]['marked_as_others'] += 1
    
    return gt_class_analysis

# --- 메인 실행 로직 ---

def main():
    """메인 실행 함수"""
    print("Few-Shot Learning vs Ground Truth 직접 대조 분석")
    print("=" * 60)
    
    experiments = get_available_experiments()
    gt_mapping = get_ground_truth_mapping()
    
    if not experiments or not gt_mapping:
        print("분석에 필요한 데이터가 부족합니다.")
        return
    
    print(f"\n📊 분석 시작: {len(experiments)}개 실험 조합 처리")
    
    all_results = []
    table8_results = []
    
    for i, (shot, threshold) in enumerate(experiments, 1):
        print(f"\n[{i:2d}/{len(experiments)}] Shot={shot}, Threshold={threshold:.2f} 분석 중...")
        
        fsl_mapping = get_fsl_predictions(shot, threshold)
        if not fsl_mapping:
            print("  ⚠️  FSL 예측 데이터 없음. 건너뜁니다.")
            continue
        
        # 직접 대조 분석
        analysis = analyze_fsl_vs_groundtruth(gt_mapping, fsl_mapping)
        
        # 전체 성능 결과 저장
        result_row = {
            'Shot': shot,
            'Threshold': threshold,
            'Total_Files': analysis['total_files'],
            'Overall_Accuracy': analysis['overall_accuracy'],
            'FSL_Class_0': analysis['fsl_distribution'].get('Class_0', 0),
            'FSL_Class_1': analysis['fsl_distribution'].get('Class_1', 0),
            'FSL_Class_2': analysis['fsl_distribution'].get('Class_2', 0),
            'FSL_Class_3': analysis['fsl_distribution'].get('Class_3', 0),
            'FSL_Unknown': analysis['fsl_distribution'].get('Unknown', 0),
            'FSL_Target_Total': (analysis['fsl_distribution'].get('Class_0', 0) + 
                               analysis['fsl_distribution'].get('Class_1', 0) + 
                               analysis['fsl_distribution'].get('Class_2', 0) + 
                               analysis['fsl_distribution'].get('Class_3', 0))
        }
        
        # 클래스별 정확도 추가
        for gt_class in ["Class_0", "Class_1", "Class_2", "Class_3"]:
            result_row[f'Accuracy_{gt_class}'] = analysis['accuracy_by_gt_class'][gt_class]
        
        all_results.append(result_row)
        
        # Table 8 스타일 분석
        table8_analysis = create_table8_style_analysis(gt_mapping, fsl_mapping)
        
        true_class_map = {
            "Class_0": "Fence (C1)", "Class_1": "Sidewalk (C2)", 
            "Class_2": "Parked car (C3)", "Class_3": "Traffic cone (C4)"
        }
        
        for gt_class in ["Class_0", "Class_1", "Class_2", "Class_3"]:
            within = table8_analysis[gt_class]['within_target']
            others = table8_analysis[gt_class]['marked_as_others']
            
            table8_row = {
                'Shot': shot,
                'Threshold': threshold,
                'GT_Class': gt_class,
                'True_Class': true_class_map[gt_class],
                'Within_Target_Classes': within,
                'Manually_Marked_As_Others': others,
                'Total': within + others
            }
            table8_results.append(table8_row)
        
        # 진행 상황 출력
        fsl_target_total = result_row['FSL_Target_Total']
        print(f"  ✅ 완료 - 전체 정확도: {analysis['overall_accuracy']:.3f}, FSL 타겟 예측: {fsl_target_total}개")
    
    # 결과 저장
    print(f"\n📁 결과 파일 저장 중...")
    
    if all_results:
        df_main = pd.DataFrame(all_results)
        main_path = os.path.join(PROJECT_ROOT, "fsl_vs_groundtruth_analysis.csv")
        df_main.to_csv(main_path, index=False)
        print(f"✅ 메인 분석 결과 저장: {main_path}")
        print(f"   📈 총 {len(df_main)} 행")
        
        # Threshold별 FSL Target Total 감소 패턴 확인
        print("\n--- Threshold별 FSL Target Total 변화 (Shot=1 예시) ---")
        shot1_data = df_main[df_main['Shot'] == 1].sort_values('Threshold')
        for _, row in shot1_data.iterrows():
            print(f"Threshold {row['Threshold']:.2f}: {int(row['FSL_Target_Total']):5d}개 (정확도: {row['Overall_Accuracy']:.3f})")
    
    if table8_results:
        df_table8 = pd.DataFrame(table8_results)
        table8_path = os.path.join(PROJECT_ROOT, "fsl_vs_groundtruth_table8.csv")
        df_table8.to_csv(table8_path, index=False)
        print(f"\n✅ Table 8 스타일 분석 저장: {table8_path}")
        print(f"   📈 총 {len(df_table8)} 행")
        
        # Table 8 Total 감소 패턴 확인
        print("\n--- Table 8 Total 합계 변화 (Shot=1 예시) ---")
        shot1_table8 = df_table8[df_table8['Shot'] == 1].groupby('Threshold')['Total'].sum().sort_index()
        for threshold, total in shot1_table8.items():
            print(f"Threshold {threshold:.2f}: {int(total):5d}개")
    
    print(f"\n🎉 모든 작업 완료!")
    print(f"📊 처리된 실험 조합: {len(all_results)}개")
    print(f"📁 생성된 파일:")
    print(f"   - fsl_vs_groundtruth_analysis.csv (전체 성능 분석)")
    print(f"   - fsl_vs_groundtruth_table8.csv (GT 클래스별 FSL 예측 분포)")

if __name__ == "__main__":
    main() 