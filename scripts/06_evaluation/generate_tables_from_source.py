#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Few-Shot Learning 결과 분석: Table 7, 8 생성 (최종 요구사항 반영)

- **핵심 수정**: 폴더/파일을 직접 세는 대신, 각 실험 폴더의 결과 원본 파일
  (예: comparison/comparison.csv)을 직접 읽어와 데이터 누락 없이 16,061개를 처리합니다.

- Table 7: 예측-실제 클래스 간의 Confusion Matrix (GT Unknown 제외)
- Table 8: 각 예측이 'Target' vs 'Unknown' 중 어디서 왔는지 분석
"""

import os
import json
import pandas as pd
from collections import defaultdict

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
    for class_folder in class_folders:
        class_path = os.path.join(gt_dir, class_folder)
        if os.path.exists(class_path):
            for filename in os.listdir(class_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    gt_mapping[filename] = class_folder
    return gt_mapping

def get_predictions_from_source_file(shot, threshold):
    """
    [수정된 핵심 로직]
    각 실험 폴더의 predictions.csv 파일을 직접 읽어서 예측 맵을 생성합니다.
    """
    base_dir = os.path.join(PROJECT_ROOT, "data", "test_category", "7.results", "resnet",
                            f"shot_{shot}", f"threshold_{threshold:.2f}")

    # 1. annotation_summary.json에서 기대값 확인
    summary_path = os.path.join(base_dir, "annotation_summary.json")
    expected_total = 0
    if os.path.exists(summary_path):
        with open(summary_path, 'r') as f:
            summary_data = json.load(f)
            expected_total = summary_data.get("total_annotations", 0)

    # 2. predictions.csv 파일 경로 (comparison 폴더가 아니라 바로 여기에 있음)
    predictions_csv = os.path.join(base_dir, "predictions.csv")
    
    if not os.path.exists(predictions_csv):
        print(f"  [!] 경고: Shot={shot}, Threshold={threshold:.2f} 에서 predictions.csv 파일을 찾을 수 없습니다.")
        return {}

    # 3. CSV에서 데이터 로드 및 예측 맵 생성
    try:
        df = pd.read_csv(predictions_csv)
        
        # 정확한 열 이름 사용
        filename_col = 'image_filename'
        pred_col = 'predicted_class'
        
        if filename_col not in df.columns or pred_col not in df.columns:
            print(f"  [!] 오류: 필요한 열({filename_col}, {pred_col})이 CSV에 없습니다.")
            print(f"      실제 열들: {list(df.columns)}")
            return {}
        
        pred_mapping = pd.Series(df[pred_col].values, index=df[filename_col]).to_dict()

        # 4. 최종 검증
        if expected_total > 0 and len(pred_mapping) != expected_total:
             print(f"  [!] 경고: 로드된 예측 수({len(pred_mapping)})가 summary({expected_total})와 일치하지 않습니다.")
        elif expected_total > 0:
             print(f"  ✅ 확인: 로드된 예측 수({len(pred_mapping)})가 summary의 총계와 정확히 일치합니다.")

        return pred_mapping
    except Exception as e:
        print(f"  [!] 오류: CSV 파일 '{predictions_csv}' 처리 중 오류: {e}")
        return {}

def normalize_class_name(class_name):
    """클래스명 정규화 (e.g., 'unknown_road' -> 'Unknown')"""
    if class_name is None or not isinstance(class_name, str): return None
    return "Unknown" if "unknown" in class_name.lower() else class_name

# --- Table 7 & 8 계산 로직 (사용자님 최종 요구사항 반영) ---

def calculate_table7_data(gt_mapping, pred_mapping):
    """Table 7: 실제-예측 클래스 간 Confusion Matrix 데이터 계산 (행:실제, 열:예측)"""
    known_classes = ["Class_0", "Class_1", "Class_2", "Class_3"]
    confusion_matrix = defaultdict(lambda: defaultdict(int))
    
    for filename, actual_raw in gt_mapping.items():
        actual_class = normalize_class_name(actual_raw)
        if actual_class in known_classes:
            pred_raw = pred_mapping.get(filename)
            pred_class = normalize_class_name(pred_raw)
            if pred_class in known_classes:
                confusion_matrix[actual_class][pred_class] += 1
    return confusion_matrix

def get_autodistill_predictions():
    """AutoDistill의 실제 예측 결과 로드 (6.preprocessed 폴더 기준)"""
    autodistill_mapping = {}
    autodistill_dir = os.path.join(PROJECT_ROOT, "data", "test_category", "6.preprocessed")
    
    # AutoDistill이 실제로 분류한 결과 폴더들
    for class_id in [0, 1, 2, 3]:
        class_folder = f"Class_{class_id}"
        class_path = os.path.join(autodistill_dir, class_folder)
        
        if os.path.exists(class_path):
            for filename in os.listdir(class_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    autodistill_mapping[filename] = class_folder
    
    print(f"AutoDistill 예측 결과 로드 완료: {len(autodistill_mapping)}개 파일")
    
    # 클래스별 통계 출력
    from collections import Counter
    class_counts = Counter(autodistill_mapping.values())
    for class_name, count in sorted(class_counts.items()):
        print(f"  {class_name}: {count}개")
    
    return autodistill_mapping

def calculate_table8_data(gt_mapping, pred_mapping, autodistill_mapping):
    """Table 8: AutoDistill 예측 기준 FSL 재분류 성능 분석"""
    autodistill_classes = ["Class_0", "Class_1", "Class_2", "Class_3"]
    analysis = defaultdict(lambda: defaultdict(int))

    for filename, autodistill_class in autodistill_mapping.items():
        if autodistill_class in autodistill_classes:
            fsl_pred_raw = pred_mapping.get(filename)
            fsl_pred = normalize_class_name(fsl_pred_raw)
            
            # AutoDistill이 해당 클래스로 예측한 것을 FSL이 어떻게 재분류했는지 분석
            if fsl_pred in ["Class_0", "Class_1", "Class_2", "Class_3"]:
                # FSL이 어떤 타겟 클래스로든 예측한 경우
                analysis[autodistill_class]['within_target'] += 1
            elif fsl_pred == "Unknown":
                # FSL이 Unknown으로 예측한 경우
                analysis[autodistill_class]['marked_as_others'] += 1
    
    return analysis

# --- 메인 실행 로직 ---

def main():
    """메인 실행 함수"""
    print("최종 요구사항 기반 Table 7, 8 생성 시작")
    print("AutoDistill 실제 예측 결과 기준 FSL 재분류 성능 분석")
    print("=" * 60)

    experiments = get_available_experiments()
    gt_mapping = get_ground_truth_mapping()
    
    # AutoDistill 예측 결과를 한 번만 로드 (효율성 개선)
    print("\n--- AutoDistill 실제 예측 결과 로딩 ---")
    autodistill_mapping = get_autodistill_predictions()
    
    if not experiments or not gt_mapping or not autodistill_mapping:
        print("분석에 필요한 데이터가 부족합니다.")
        return

    print(f"\n📊 분석 시작: {len(experiments)}개 실험 조합 처리")
    
    table7_all_results = []
    table8_all_results = []
    processed_count = 0

    for shot, threshold in experiments:
        processed_count += 1
        print(f"\n[{processed_count:2d}/{len(experiments)}] Shot={shot}, Threshold={threshold:.2f} 처리 중...")
        
        pred_mapping = get_predictions_from_source_file(shot, threshold)
        if not pred_mapping:
            print("  ⚠️  예측 데이터 없음. 건너뜁니다.")
            continue

        # Table 7 데이터 생성 (Ground Truth 기준 Confusion Matrix)
        t7_data = calculate_table7_data(gt_mapping, pred_mapping)
        for actual_class in ["Class_0", "Class_1", "Class_2", "Class_3"]:
            row = {
                "Shot": shot, "Threshold": threshold, "Actual_Class": actual_class,
                "Pred_Class_0": t7_data[actual_class].get("Class_0", 0),
                "Pred_Class_1": t7_data[actual_class].get("Class_1", 0),
                "Pred_Class_2": t7_data[actual_class].get("Class_2", 0),
                "Pred_Class_3": t7_data[actual_class].get("Class_3", 0),
            }
            table7_all_results.append(row)

        # Table 8 데이터 생성 (AutoDistill 예측 기준 FSL 재분류 성능)
        t8_data = calculate_table8_data(gt_mapping, pred_mapping, autodistill_mapping)
        true_class_map = {
            "Class_0": "Fence (C1)", "Class_1": "Sidewalk (C2)", 
            "Class_2": "Parked car (C3)", "Class_3": "Traffic cone (C4)"
        }
        for autodistill_class in ["Class_0", "Class_1", "Class_2", "Class_3"]:
            within = t8_data[autodistill_class].get('within_target', 0)
            others = t8_data[autodistill_class].get('marked_as_others', 0)
            row = {
                "Shot": shot, "Threshold": threshold, "Class": autodistill_class,
                "True class": true_class_map.get(autodistill_class, autodistill_class),
                "Within target classes": within,
                "Manually marked as others": others,
                "Total": within + others
            }
            table8_all_results.append(row)
        
        print(f"  ✅ 완료 (Table 7: {len(['Class_0', 'Class_1', 'Class_2', 'Class_3'])}행, Table 8: {len(['Class_0', 'Class_1', 'Class_2', 'Class_3'])}행 추가)")

    # DataFrame 생성 및 저장
    print(f"\n📁 결과 파일 저장 중...")
    
    if table7_all_results:
        df7 = pd.DataFrame(table7_all_results)
        df7_path = os.path.join(PROJECT_ROOT, "final_table7_actual_vs_predicted.csv")
        df7.to_csv(df7_path, index=False)
        print(f"✅ Table 7 저장 완료: {df7_path}")
        print(f"   📈 총 {len(df7)} 행 (실제 클래스별 예측 분포 - Ground Truth 기준)")
        print("--- Table 7 샘플 (처음 5행) ---")
        print(df7.head())

    if table8_all_results:
        df8 = pd.DataFrame(table8_all_results)
        df8_path = os.path.join(PROJECT_ROOT, "final_table8_prediction_source.csv")
        df8.to_csv(df8_path, index=False)
        print(f"\n✅ Table 8 저장 완료: {df8_path}")
        print(f"   📈 총 {len(df8)} 행 (AutoDistill 예측별 FSL 재분류 성능)")
        
        # 검증: 각 조합별 Total 합계 확인
        total_sum = df8.groupby(['Shot', 'Threshold'])['Total'].sum()
        unique_totals = total_sum.unique()
        print(f"   🔍 검증: 각 조합별 Total 합계 = {unique_totals} (모두 16061이어야 함)")
        
        print("--- Table 8 샘플 (처음 5행) ---")
        print(df8.head())
        print("\n--- Table 8 조합별 Total 합계 (처음 10개) ---")
        print(total_sum.head(10))

    print(f"\n🎉 모든 작업 완료!")
    print(f"📊 처리된 실험 조합: {processed_count}개")
    print(f"📁 생성된 파일:")
    print(f"   - final_table7_actual_vs_predicted.csv (Ground Truth 기준 Confusion Matrix)")
    print(f"   - final_table8_prediction_source.csv (AutoDistill 예측 기준 FSL 재분류 성능)")

if __name__ == "__main__":
    main() 