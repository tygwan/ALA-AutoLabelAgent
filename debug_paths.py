#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Few-Shot Learning 경로 문제 디버깅
"""

import os
import sys
from pathlib import Path

def debug_current_directory():
    """현재 디렉토리 확인"""
    print("=== 현재 디렉토리 정보 ===")
    print(f"현재 작업 디렉토리: {os.getcwd()}")
    print(f"스크립트 위치: {os.path.abspath(__file__)}")
    print(f"Python 경로: {sys.executable}")
    
def check_data_paths():
    """데이터 경로 확인"""
    print("\n=== 데이터 경로 확인 ===")
    
    # 가능한 기본 경로들
    possible_roots = [
        ".",  # 현재 디렉토리
        "..",  # 상위 디렉토리
        "../..",  # 두 단계 상위
        "/home/ml/project-agi",  # 절대 경로
    ]
    
    for root in possible_roots:
        data_path = os.path.join(root, "data", "test_category")
        abs_path = os.path.abspath(data_path)
        exists = os.path.exists(data_path)
        print(f"  {root}/data/test_category -> {abs_path} [{'✓' if exists else '✗'}]")
        
        if exists:
            print(f"    └─ 발견! 이 경로를 사용해야 합니다: {abs_path}")
            return root
    
    return None

def check_ground_truth(base_path):
    """Ground Truth 경로 확인"""
    if base_path is None:
        print("\n❌ 기본 경로를 찾을 수 없습니다.")
        return
    
    print(f"\n=== Ground Truth 확인 (기준: {base_path}) ===")
    
    gt_path = os.path.join(base_path, "data", "test_category", "7.results", "ground_truth")
    abs_gt_path = os.path.abspath(gt_path)
    
    print(f"Ground Truth 경로: {abs_gt_path}")
    print(f"존재 여부: {'✓' if os.path.exists(gt_path) else '✗'}")
    
    if os.path.exists(gt_path):
        print("  하위 디렉토리:")
        for item in os.listdir(gt_path):
            item_path = os.path.join(gt_path, item)
            if os.path.isdir(item_path):
                file_count = len([f for f in os.listdir(item_path) 
                                if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
                print(f"    {item}: {file_count}개 파일")

def check_few_shot_results(base_path):
    """Few-Shot Learning 결과 확인"""
    if base_path is None:
        return
    
    print(f"\n=== Few-Shot Learning 결과 확인 (기준: {base_path}) ===")
    
    results_path = os.path.join(base_path, "data", "test_category", "7.results", "resnet")
    abs_results_path = os.path.abspath(results_path)
    
    print(f"Results 경로: {abs_results_path}")
    print(f"존재 여부: {'✓' if os.path.exists(results_path) else '✗'}")
    
    if os.path.exists(results_path):
        shot_dirs = [d for d in os.listdir(results_path) if d.startswith("shot_")]
        print(f"  발견된 shot 디렉토리: {len(shot_dirs)}개")
        
        for shot_dir in sorted(shot_dirs)[:5]:  # 처음 5개만
            shot_path = os.path.join(results_path, shot_dir)
            threshold_dirs = [d for d in os.listdir(shot_path) if d.startswith("threshold_")]
            print(f"    {shot_dir}: {len(threshold_dirs)}개 threshold")
            
            # 첫 번째 threshold 내용 확인
            if threshold_dirs:
                first_threshold = sorted(threshold_dirs)[0]
                threshold_path = os.path.join(shot_path, first_threshold)
                class_dirs = [d for d in os.listdir(threshold_path) 
                            if os.path.isdir(os.path.join(threshold_path, d)) 
                            and d not in ["annotations_by_class", "comparison"]]
                print(f"      └─ {first_threshold}: {class_dirs}")

def suggest_fix(base_path):
    """해결 방법 제안"""
    print(f"\n=== 해결 방법 제안 ===")
    
    if base_path is None:
        print("❌ 데이터 디렉토리를 찾을 수 없습니다.")
        print("📍 다음을 확인해주세요:")
        print("  1. 프로젝트 루트 디렉토리에서 실행하고 있는지")
        print("  2. data/test_category/ 디렉토리가 존재하는지")
        return
    
    print(f"✅ 올바른 기본 경로: {os.path.abspath(base_path)}")
    
    if base_path != ".":
        print(f"💡 해결 방법 1: 올바른 디렉토리에서 실행")
        print(f"   cd {os.path.abspath(base_path)}")
        print(f"   python3 generate_few_shot_tables_789.py")
        
        print(f"\n💡 해결 방법 2: 스크립트 내 경로 수정")
        print(f"   base_path = '{base_path}' 를 스크립트에 추가")

def main():
    """메인 함수"""
    print("Few-Shot Learning 경로 디버깅")
    print("=" * 50)
    
    # 1. 현재 디렉토리 확인
    debug_current_directory()
    
    # 2. 데이터 경로 찾기
    base_path = check_data_paths()
    
    # 3. Ground Truth 확인
    check_ground_truth(base_path)
    
    # 4. Few-Shot 결과 확인
    check_few_shot_results(base_path)
    
    # 5. 해결 방법 제안
    suggest_fix(base_path)

if __name__ == "__main__":
    main() 