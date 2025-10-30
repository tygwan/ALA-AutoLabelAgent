#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 Few-Shot Learning 테스트 스크립트
"""

import os
import sys
import json
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """필요한 모듈들 import 테스트"""
    try:
        # 기본 라이브러리 테스트
        import torch
        import numpy as np
        import pandas as pd
        from PIL import Image
        from sklearn.metrics import accuracy_score
        logger.info("✓ 기본 라이브러리 import 성공")
        
        # 프로젝트 모듈 테스트
        sys.path.append("scripts/03_classification")
        
        from data_utils import get_category_path, load_class_mapping
        logger.info("✓ data_utils import 성공")
        
        from classifier_cosine import CosineSimilarityClassifier, FeatureExtractor
        logger.info("✓ classifier_cosine import 성공")
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ Import 실패: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ 기타 오류: {e}")
        return False

def test_data_paths():
    """데이터 경로 확인"""
    category = "test_category"
    
    # 필요한 경로들
    paths = {
        "category": f"data/{category}",
        "support_set": f"data/{category}/2.support-set",
        "preprocessed": f"data/{category}/6.preprocessed",
        "results": f"data/{category}/7.results"
    }
    
    all_exist = True
    for name, path in paths.items():
        if os.path.exists(path):
            logger.info(f"✓ {name}: {path}")
        else:
            logger.error(f"❌ {name} 없음: {path}")
            all_exist = False
    
    return all_exist

def run_simple_classification():
    """간단한 분류 테스트"""
    try:
        sys.path.append("scripts/03_classification")
        from data_utils import get_category_path
        from classifier_cosine import CosineSimilarityClassifier
        
        category = "test_category"
        model_name = "resnet"
        
        logger.info(f"분류기 초기화: {category}, {model_name}")
        
        # 분류기 생성
        classifier = CosineSimilarityClassifier(
            category_name=category,
            model_name=model_name,
            k_shot=1,
            threshold=0.5
        )
        
        logger.info("✓ 분류기 생성 성공")
        
        # Support set 로드
        support_dir = f"data/{category}/2.support-set"
        if os.path.exists(support_dir):
            classifier.load_support_set(category)
            logger.info("✓ Support set 로드 성공")
        else:
            logger.error("❌ Support set 디렉토리 없음")
            return False
        
        # 테스트 이미지로 예측 테스트
        preprocessed_dir = f"data/{category}/6.preprocessed"
        if os.path.exists(preprocessed_dir):
            # Class_0 폴더에서 첫 번째 이미지 가져오기
            class_0_dir = os.path.join(preprocessed_dir, "Class_0")
            if os.path.exists(class_0_dir):
                images = [f for f in os.listdir(class_0_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                if images:
                    test_image = os.path.join(class_0_dir, images[0])
                    logger.info(f"테스트 이미지: {test_image}")
                    
                    # 예측 수행
                    result = classifier.predict_single(test_image)
                    logger.info(f"✓ 예측 결과: {result}")
                    return True
                else:
                    logger.error("❌ 테스트 이미지 없음")
            else:
                logger.error("❌ Class_0 디렉토리 없음")
        else:
            logger.error("❌ Preprocessed 디렉토리 없음")
        
        return False
        
    except Exception as e:
        logger.error(f"❌ 분류 테스트 실패: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def main():
    """메인 함수"""
    logger.info("=== Few-Shot Learning 진단 시작 ===")
    
    # 1. Import 테스트
    logger.info("1. Import 테스트...")
    if not test_imports():
        logger.error("Import 테스트 실패")
        return 1
    
    # 2. 데이터 경로 테스트
    logger.info("\n2. 데이터 경로 테스트...")
    if not test_data_paths():
        logger.error("데이터 경로 테스트 실패")
        return 1
    
    # 3. 간단한 분류 테스트
    logger.info("\n3. 분류 테스트...")
    if not run_simple_classification():
        logger.error("분류 테스트 실패")
        return 1
    
    logger.info("\n=== 모든 테스트 성공! ===")
    logger.info("Few-Shot Learning 환경이 정상적으로 설정되었습니다.")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 