#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoDistill 베이스라인과 Few-Shot Learning 결과의 파일 차이 찾기
"""

import os
import json
import pandas as pd
from collections import defaultdict, Counter

def get_autodistill_files():
    """AutoDistill 베이스라인에서 사용된 파일 목록 추출"""
    print("=== AutoDistill 베이스라인 파일 목록 추출 ===")
    
    # Ground Truth 디렉토리에서 직접 파일명 추출
    gt_dir = "data/test_category/7.results/ground_truth"
    
    autodistill_files = set()
    
    # 각 클래스 폴더에서 파일명 수집
    class_folders = ["Class_0", "Class_1", "Class_2", "Class_3", 
                    "unknown_egifence", "unknown_human", "unknown_none", "unknown_road"]
    
    for class_folder in class_folders:
        class_path = os.path.join(gt_dir, class_folder)
        if os.path.exists(class_path):
            for filename in os.listdir(class_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    autodistill_files.add(filename)
            print(f"  {class_folder}: {len([f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])}개")
    
    print(f"AutoDistill 총 파일 수: {len(autodistill_files)}")
    return autodistill_files

def get_few_shot_files():
    """기존 Few-Shot Learning 결과에서 사용된 파일 목록 추출"""
    print("\n=== Few-Shot Learning 파일 목록 추출 ===")
    
    # 기존 Few-Shot 결과에서 파일 목록 추출
    # shot_1/threshold_0.50 결과를 참조
    few_shot_dir = "data/test_category/7.results/resnet/shot_1/threshold_0.50"
    
    few_shot_files = set()
    
    if os.path.exists(few_shot_dir):
        # 분류 결과 폴더들에서 파일명 수집
        for item in os.listdir(few_shot_dir):
            item_path = os.path.join(few_shot_dir, item)
            if os.path.isdir(item_path):
                for filename in os.listdir(item_path):
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                        few_shot_files.add(filename)
                print(f"  {item}: {len([f for f in os.listdir(item_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])}개")
    
    print(f"Few-Shot 총 파일 수: {len(few_shot_files)}")
    return few_shot_files

def find_differences(autodistill_files, few_shot_files):
    """두 파일 목록의 차이점 찾기"""
    print("\n=== 파일 차이점 분석 ===")
    
    # Few-Shot에만 있는 파일들 (제거해야 할 파일들)
    only_in_few_shot = few_shot_files - autodistill_files
    
    # AutoDistill에만 있는 파일들
    only_in_autodistill = autodistill_files - few_shot_files
    
    # 공통 파일들
    common_files = autodistill_files & few_shot_files
    
    print(f"공통 파일 수: {len(common_files)}")
    print(f"Few-Shot에만 있는 파일 수: {len(only_in_few_shot)}")
    print(f"AutoDistill에만 있는 파일 수: {len(only_in_autodistill)}")
    
    if only_in_few_shot:
        print(f"\n📝 제거해야 할 파일들 ({len(only_in_few_shot)}개):")
        for i, filename in enumerate(sorted(only_in_few_shot)):
            print(f"  {i+1:2d}. {filename}")
    
    if only_in_autodistill:
        print(f"\n⚠️  AutoDistill에만 있는 파일들 ({len(only_in_autodistill)}개):")
        for i, filename in enumerate(sorted(only_in_autodistill)[:10]):  # 처음 10개만
            print(f"  {i+1:2d}. {filename}")
        if len(only_in_autodistill) > 10:
            print(f"  ... 및 {len(only_in_autodistill) - 10}개 더")
    
    return only_in_few_shot, only_in_autodistill, common_files

def analyze_file_patterns(files_to_remove):
    """제거할 파일들의 패턴 분석"""
    if not files_to_remove:
        return
    
    print(f"\n=== 제거할 파일들의 패턴 분석 ===")
    
    # 파일명에서 클래스 정보 추출
    class_pattern = defaultdict(list)
    
    for filename in files_to_remove:
        # 파일명에서 클래스 정보 추출 시도
        if "unknown_egifence" in filename:
            class_pattern["unknown_egifence"].append(filename)
        elif "unknown_human" in filename:
            class_pattern["unknown_human"].append(filename)
        elif "unknown_none" in filename:
            class_pattern["unknown_none"].append(filename)
        elif "unknown_road" in filename:
            class_pattern["unknown_road"].append(filename)
        elif any(f"cls{i}" in filename for i in range(4)):
            # cls0, cls1, cls2, cls3 패턴
            for i in range(4):
                if f"cls{i}" in filename:
                    class_pattern[f"Class_{i}"].append(filename)
                    break
        else:
            class_pattern["기타"].append(filename)
    
    for class_name, files in class_pattern.items():
        if files:
            print(f"  {class_name}: {len(files)}개")
            for file in files:
                print(f"    - {file}")

def main():
    """메인 함수"""
    print("8개 누락 파일 찾기 및 분석")
    print("=" * 50)
    
    # 1. AutoDistill 베이스라인 파일 목록
    autodistill_files = get_autodistill_files()
    
    # 2. Few-Shot Learning 파일 목록  
    few_shot_files = get_few_shot_files()
    
    # 3. 차이점 분석
    files_to_remove, files_missing, common_files = find_differences(autodistill_files, few_shot_files)
    
    # 4. 제거할 파일 패턴 분석
    analyze_file_patterns(files_to_remove)
    
    # 5. 결과 저장
    result = {
        "autodistill_total": len(autodistill_files),
        "few_shot_total": len(few_shot_files), 
        "common_files": len(common_files),
        "files_to_remove": list(files_to_remove),
        "files_missing_in_few_shot": list(files_missing)
    }
    
    with open("file_difference_analysis.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 결과가 file_difference_analysis.json에 저장되었습니다.")
    
    return result

if __name__ == "__main__":
    result = main() 