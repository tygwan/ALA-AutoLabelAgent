#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
직접적인 Few-Shot Learning 실행 스크립트
"""

import os
import sys
import subprocess
import time

def run_direct_fsl():
    """직접적인 Few-Shot Learning 실행"""
    
    # 실험 설정
    category = "test_category"
    model = "resnet"
    shots = [1, 5, 10, 30]
    thresholds = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8]
    
    print(f"=== Few-Shot Learning 실험 시작 ===")
    print(f"카테고리: {category}")
    print(f"모델: {model}")
    print(f"Shots: {shots}")
    print(f"Thresholds: {thresholds}")
    print(f"총 실험 수: {len(shots) * len(thresholds)}")
    print()
    
    # 기본 경로 확인
    support_set_path = f"data/{category}/2.support-set"
    preprocessed_path = f"data/{category}/6.preprocessed"
    
    if not os.path.exists(support_set_path):
        print(f"❌ Support set이 없습니다: {support_set_path}")
        return False
        
    if not os.path.exists(preprocessed_path):
        print(f"❌ Preprocessed 데이터가 없습니다: {preprocessed_path}")
        return False
    
    print(f"✓ Support set 확인: {support_set_path}")
    print(f"✓ Preprocessed 확인: {preprocessed_path}")
    print()
    
    # 실험별 실행
    experiment_count = 0
    total_experiments = len(shots) * len(thresholds)
    
    for shot in shots:
        for threshold in thresholds:
            experiment_count += 1
            print(f"[{experiment_count}/{total_experiments}] Shot: {shot}, Threshold: {threshold}")
            
            try:
                # classifier_cosine_experiment.py 직접 실행
                cmd = [
                    "python3", 
                    "scripts/03_classification/classifier_cosine_experiment.py",
                    "--category", category,
                    "--model", model,
                    "--shots", str(shot),
                    "--thresholds", str(threshold),
                    "--input-dir", preprocessed_path
                ]
                
                print(f"   실행 중: {' '.join(cmd)}")
                
                # 실행
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=1800  # 30분 타임아웃
                )
                
                if result.returncode == 0:
                    print(f"   ✓ 성공")
                else:
                    print(f"   ❌ 실패: {result.stderr[:200]}")
                    
            except subprocess.TimeoutExpired:
                print(f"   ⏰ 타임아웃 (30분 초과)")
            except Exception as e:
                print(f"   ❌ 오류: {e}")
            
            print()
    
    print("=== 모든 실험 완료 ===")
    return True

if __name__ == "__main__":
    # 작업 디렉토리 확인
    if not os.path.exists("data/test_category"):
        print("❌ data/test_category 디렉토리가 없습니다.")
        print("현재 위치:", os.getcwd())
        sys.exit(1)
    
    # 실험 실행
    success = run_direct_fsl()
    
    if success:
        print("실험 완료!")
        # 결과 확인
        results_dir = "data/test_category/7.results/resnet"
        if os.path.exists(results_dir):
            print(f"결과 위치: {results_dir}")
            print("생성된 파일들:")
            for root, dirs, files in os.walk(results_dir):
                for file in files[:5]:  # 처음 5개만 표시
                    print(f"  - {os.path.join(root, file)}")
    else:
        print("실험 실행 실패")
        sys.exit(1) 