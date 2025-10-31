#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
데이터 유틸리티 함수들
"""

import os
import json
import logging

logger = logging.getLogger(__name__)

def get_category_path(category_name: str) -> str:
    """
    카테고리 경로 반환
    
    Args:
        category_name: 카테고리 이름
        
    Returns:
        카테고리 경로
    """
    return os.path.join("data", category_name)

def load_class_mapping(category_name: str) -> dict:
    """
    클래스 매핑 파일 로드
    
    Args:
        category_name: 카테고리 이름
        
    Returns:
        클래스 매핑 딕셔너리
    """
    mapping_file = os.path.join(get_category_path(category_name), "class_mapping.json")
    
    if os.path.exists(mapping_file):
        try:
            with open(mapping_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"클래스 매핑 파일 로드 실패: {e}")
    
    # 기본 매핑 반환
    return {
        "Class_0": "Class_0",
        "Class_1": "Class_1", 
        "Class_2": "Class_2",
        "Class_3": "Class_3",
        "unknown_egifence": "unknown_egifence",
        "unknown_human": "unknown_human", 
        "unknown_road": "unknown_road",
        "unknown_none": "unknown_none"
    }

def get_available_categories() -> list:
    """
    사용 가능한 카테고리 목록 반환
    
    Returns:
        카테고리 이름 리스트
    """
    data_dir = "data"
    if not os.path.exists(data_dir):
        return []
    
    categories = []
    for item in os.listdir(data_dir):
        item_path = os.path.join(data_dir, item)
        if os.path.isdir(item_path):
            # 기본 구조 확인
            required_dirs = ["1.images", "2.support-set", "6.preprocessed"]
            if all(os.path.exists(os.path.join(item_path, req_dir)) for req_dir in required_dirs):
                categories.append(item)
    
    return sorted(categories)

def validate_category_path(category_name: str) -> bool:
    """
    카테고리 경로 유효성 검사
    
    Args:
        category_name: 카테고리 이름
        
    Returns:
        유효한지 여부
    """
    category_path = get_category_path(category_name)
    
    if not os.path.exists(category_path):
        logger.error(f"카테고리 디렉토리가 없습니다: {category_path}")
        return False
    
    # 필수 디렉토리 확인
    required_dirs = ["1.images", "2.support-set", "6.preprocessed"]
    missing_dirs = []
    
    for req_dir in required_dirs:
        req_path = os.path.join(category_path, req_dir)
        if not os.path.exists(req_path):
            missing_dirs.append(req_dir)
    
    if missing_dirs:
        logger.error(f"필수 디렉토리가 없습니다: {missing_dirs}")
        return False
    
    logger.info(f"카테고리 경로 유효성 확인 완료: {category_path}")
    return True 