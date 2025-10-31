#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoDistill 베이스라인 결과를 포맷팅된 테이블로 생성
"""

def create_formatted_tables():
    """AutoDistill 베이스라인 결과 테이블들 생성"""
    
    print("="*80)
    print("AUTODISTILL BASELINE PERFORMANCE ANALYSIS")
    print("="*80)
    print()
    
    # ==================== TABLE 4 ====================
    print("TABLE 4: Overall Performance Metrics (AutoDistill Baseline)")
    print("-" * 60)
    print(f"{'Metric':<25} {'Value':<15} {'Percentage':<15}")
    print("-" * 60)
    print(f"{'Overall Accuracy':<25} {0.5353:<15.4f} {'53.53%':<15}")
    print(f"{'Macro Precision':<25} {0.2114:<15.4f} {'21.14%':<15}")
    print(f"{'Macro Recall':<25} {0.3740:<15.4f} {'37.40%':<15}")
    print(f"{'Macro F1-Score':<25} {0.2628:<15.4f} {'26.28%':<15}")
    print(f"{'Weighted Precision':<25} {0.3474:<15.4f} {'34.74%':<15}")
    print(f"{'Weighted Recall':<25} {0.5353:<15.4f} {'53.53%':<15}")
    print(f"{'Weighted F1-Score':<25} {0.4156:<15.4f} {'41.56%':<15}")
    print()
    
    # ==================== TABLE 5 ====================
    print("TABLE 5: Class-wise Performance Metrics (AutoDistill Baseline)")
    print("-" * 90)
    print(f"{'Class':<20} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10} {'Accuracy':<12}")
    print("-" * 90)
    
    # 클래스별 데이터
    classes_data = [
        ("Class_0", 0.0414, 0.1230, 0.0619, 366),
        ("Class_1", 0.6005, 0.8729, 0.7115, 3762),
        ("Class_2", 0.7250, 0.9960, 0.8392, 3971),
        ("Class_3", 0.3242, 1.0000, 0.4897, 1313),
        ("unknown_egifence", 0.0000, 0.0000, 0.0000, 2),
        ("unknown_human", 0.0000, 0.0000, 0.0000, 235),
        ("unknown_none", 0.0000, 0.0000, 0.0000, 4310),
        ("unknown_road", 0.0000, 0.0000, 0.0000, 2102)
    ]
    
    # Confusion matrix 데이터 (대각선 값들)
    correct_predictions = [45, 3284, 3955, 1313, 0, 0, 0, 0]
    
    for i, (class_name, precision, recall, f1, support) in enumerate(classes_data):
        accuracy = correct_predictions[i] / support if support > 0 else 0.0
        print(f"{class_name:<20} {precision:<12.4f} {recall:<12.4f} {f1:<12.4f} {support:<10} {accuracy:<12.4f}")
    
    print("-" * 90)
    print(f"{'Macro Average':<20} {0.2114:<12.4f} {0.3740:<12.4f} {0.2628:<12.4f} {16061:<10} {0.5353:<12.4f}")
    print(f"{'Weighted Average':<20} {0.3474:<12.4f} {0.5353:<12.4f} {0.4156:<12.4f} {16061:<10} {0.5353:<12.4f}")
    print()
    
    # ==================== TABLE 6 ====================
    print("TABLE 6: Confusion Matrix (AutoDistill Baseline)")
    print("-" * 120)
    
    # 헤더
    classes = ["Class_0", "Class_1", "Class_2", "Class_3", "unknown_egifence", "unknown_human", "unknown_none", "unknown_road"]
    print(f"{'Actual \\ Predicted':<20}", end="")
    for cls in classes:
        print(f"{cls[:10]:<12}", end="")
    print()
    print("-" * 120)
    
    # Confusion matrix 데이터
    confusion_matrix = [
        [45, 1, 259, 61, 0, 0, 0, 0],      # Class_0
        [478, 3284, 0, 0, 0, 0, 0, 0],     # Class_1
        [11, 1, 3955, 4, 0, 0, 0, 0],      # Class_2
        [0, 0, 0, 1313, 0, 0, 0, 0],       # Class_3
        [2, 0, 0, 0, 0, 0, 0, 0],          # unknown_egifence
        [227, 0, 8, 0, 0, 0, 0, 0],        # unknown_human
        [141, 268, 1231, 2670, 0, 0, 0, 0], # unknown_none
        [183, 1915, 2, 2, 0, 0, 0, 0]      # unknown_road
    ]
    
    for i, cls in enumerate(classes):
        print(f"{cls:<20}", end="")
        for j in range(len(classes)):
            print(f"{confusion_matrix[i][j]:<12}", end="")
        print()
    
    print()
    print(f"Overall Accuracy: {0.5353:.4f} (53.53%)")
    print()
    
    # ==================== BINARY TABLE ====================
    print("TABLE 7: Binary Classification Performance (Known vs Unknown Classes)")
    print("-" * 80)
    
    # Known classes: Class_0, Class_1, Class_2, Class_3
    # Unknown classes: unknown_egifence, unknown_human, unknown_none, unknown_road
    
    # Binary confusion matrix 계산
    # Known classes 예측 결과
    known_correct = 45 + 3284 + 3955 + 1313  # 8597
    known_total = 366 + 3762 + 3971 + 1313   # 9412
    known_as_unknown = known_total - known_correct  # 815
    
    # Unknown classes 예측 결과  
    unknown_total = 2 + 235 + 4310 + 2102  # 6649
    unknown_as_known = 2 + 227 + 141 + 183 + 0 + 0 + 268 + 1915 + 0 + 8 + 1231 + 2 + 0 + 0 + 2670 + 2  # 모두 known으로 잘못 분류
    unknown_as_known = 6649  # 모든 unknown이 known으로 분류됨
    unknown_correct = 0  # unknown으로 정확히 분류된 것은 0개
    
    print(f"{'Actual \\ Predicted':<20} {'Known':<15} {'Unknown':<15} {'Total':<15}")
    print("-" * 80)
    print(f"{'Known':<20} {known_correct:<15} {known_as_unknown:<15} {known_total:<15}")
    print(f"{'Unknown':<20} {unknown_as_known:<15} {unknown_correct:<15} {unknown_total:<15}")
    print("-" * 80)
    print(f"{'Total':<20} {known_correct + unknown_as_known:<15} {known_as_unknown + unknown_correct:<15} {known_total + unknown_total:<15}")
    print()
    
    # Binary 성능 메트릭 계산
    binary_accuracy = (known_correct + unknown_correct) / (known_total + unknown_total)
    known_precision = known_correct / (known_correct + unknown_as_known) if (known_correct + unknown_as_known) > 0 else 0
    known_recall = known_correct / known_total if known_total > 0 else 0
    known_f1 = 2 * (known_precision * known_recall) / (known_precision + known_recall) if (known_precision + known_recall) > 0 else 0
    
    unknown_precision = unknown_correct / (unknown_correct + known_as_unknown) if (unknown_correct + known_as_unknown) > 0 else 0
    unknown_recall = unknown_correct / unknown_total if unknown_total > 0 else 0
    unknown_f1 = 2 * (unknown_precision * unknown_recall) / (unknown_precision + unknown_recall) if (unknown_precision + unknown_recall) > 0 else 0
    
    print("Binary Classification Metrics:")
    print("-" * 60)
    print(f"{'Metric':<25} {'Known Classes':<15} {'Unknown Classes':<15}")
    print("-" * 60)
    print(f"{'Precision':<25} {known_precision:<15.4f} {unknown_precision:<15.4f}")
    print(f"{'Recall':<25} {known_recall:<15.4f} {unknown_recall:<15.4f}")
    print(f"{'F1-Score':<25} {known_f1:<15.4f} {unknown_f1:<15.4f}")
    print("-" * 60)
    print(f"{'Binary Accuracy':<25} {binary_accuracy:<15.4f} ({binary_accuracy*100:.2f}%)")
    print()
    
    # ==================== 주요 인사이트 ====================
    print("KEY INSIGHTS:")
    print("-" * 40)
    print("1. AutoDistill 베이스라인 모델의 전체 정확도는 53.53%")
    print("2. Known classes (Class_1, Class_2, Class_3)에서는 상대적으로 높은 성능")
    print("3. Class_0과 모든 Unknown classes에서 매우 낮은 성능")
    print("4. Unknown classes는 전혀 인식되지 않고 모두 Known classes로 오분류")
    print("5. 이는 AutoDistill 모델이 Unknown 객체 탐지에 한계가 있음을 시사")
    print()

if __name__ == "__main__":
    create_formatted_tables() 