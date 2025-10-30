#!/usr/bin/env python3
import pandas as pd
import os

# CSV 파일 경로
csv_path = "data/test_category/7.results/resnet/shot_10/threshold_0.50/predictions.csv"

if os.path.exists(csv_path):
    print(f"파일 발견: {csv_path}")
    
    # CSV 파일 읽기 (처음 5줄만)
    df = pd.read_csv(csv_path, nrows=5)
    
    print(f"총 열 개수: {len(df.columns)}")
    print(f"열 이름들: {list(df.columns)}")
    print("\n--- 첫 5줄 샘플 ---")
    print(df)
    
    # 전체 파일 크기도 확인
    df_full = pd.read_csv(csv_path)
    print(f"\n총 행 개수: {len(df_full)}")
    
else:
    print(f"파일 없음: {csv_path}") 