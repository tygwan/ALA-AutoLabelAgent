#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 Few-Shot Learning 실행 스크립트
현재 Ground Truth 데이터 기준으로 resnet 모델 실험 실행
"""

import os
import sys
import json
import time
import logging
from pathlib import Path

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("few_shot_simple")

def run_simple_few_shot_experiment():
    """
    간단한 Few-Shot Learning 실험 실행
    - 모델: resnet
    - Shot: 1, 5, 10, 30
    - Threshold: 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8
    """
    category = "test_category"
    model_name = "resnet"
    
    # 실험 설정
    shots = [1, 5, 10, 30]
    thresholds = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8]
    
    # 경로 설정
    category_path = f"data/{category}"
    support_dir = os.path.join(category_path, "2.support-set")
    preprocessed_dir = os.path.join(category_path, "6.preprocessed")
    results_base_dir = os.path.join(category_path, "7.results")
    results_dir = os.path.join(results_base_dir, model_name)
    
    logger.info(f"카테고리: {category}")
    logger.info(f"모델: {model_name}")
    logger.info(f"Shots: {shots}")
    logger.info(f"Thresholds: {thresholds}")
    logger.info(f"Support set: {support_dir}")
    logger.info(f"Preprocessed: {preprocessed_dir}")
    logger.info(f"Results: {results_dir}")
    
    # 디렉토리 확인
    if not os.path.exists(support_dir):
        logger.error(f"Support set 디렉토리가 없습니다: {support_dir}")
        return False
    
    if not os.path.exists(preprocessed_dir):
        logger.error(f"Preprocessed 디렉토리가 없습니다: {preprocessed_dir}")
        return False
    
    # 결과 디렉토리 생성
    os.makedirs(results_dir, exist_ok=True)
    
    try:
        # classifier_cosine 모듈 import
        sys.path.append("scripts/03_classification")
        from classifier_cosine_experiment import FewShotExperiment
        
        logger.info("FewShotExperiment 클래스 로드 성공")
        
        # 실험 객체 생성
        experiment = FewShotExperiment(
            category_name=category,
            model_name=model_name,
            save_images=True,
            group_unknown=True
        )
        
        # 실험 설정 업데이트
        experiment.n_shots = shots
        experiment.thresholds = thresholds
        
        logger.info(f"총 {len(shots) * len(thresholds)}개 실험 조합 시작")
        
        # 실험 실행
        experiment.run_all_experiments(preprocessed_dir)
        
        logger.info("모든 실험 완료!")
        logger.info(f"결과 저장 위치: {results_dir}")
        
        return True
        
    except ImportError as e:
        logger.error(f"모듈 import 실패: {e}")
        logger.error("필요한 패키지를 설치하세요:")
        logger.error("pip install torch torchvision clip-by-openai")
        return False
        
    except Exception as e:
        logger.error(f"실험 실행 중 오류: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def check_dependencies():
    """필요한 의존성 확인"""
    logger.info("의존성 확인 중...")
    
    required_modules = [
        'torch', 'torchvision', 'numpy', 'pandas', 
        'PIL', 'sklearn', 'matplotlib', 'seaborn'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            logger.info(f"✓ {module}")
        except ImportError:
            logger.warning(f"✗ {module} - 설치 필요")
            missing_modules.append(module)
    
    if missing_modules:
        logger.error(f"누락된 모듈: {missing_modules}")
        logger.error("다음 명령으로 설치하세요:")
        logger.error(f"pip install {' '.join(missing_modules)}")
        return False
    
    logger.info("모든 의존성 확인 완료!")
    return True

def main():
    """메인 함수"""
    logger.info("=== 간단한 Few-Shot Learning 실험 시작 ===")
    
    # 의존성 확인
    if not check_dependencies():
        logger.error("의존성 확인 실패")
        return 1
    
    # 실험 실행
    success = run_simple_few_shot_experiment()
    
    if success:
        logger.info("=== 실험 성공적으로 완료 ===")
        return 0
    else:
        logger.error("=== 실험 실행 실패 ===")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 