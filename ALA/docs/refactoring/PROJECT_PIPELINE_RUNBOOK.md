# Project Pipeline Runbook

본 문서는 프로젝트의 전체 구동 파이프라인과 주요 엔트리포인트(스크립트, 옵션, 출력 경로)를 요약합니다.

## 1) 데이터 디렉토리 구조(요지)

```
data/<category>/
  1.images/          # 원본 이미지
  2.support-set/     # Few-Shot 지원 세트
  3.box/             # 박스 좌표 결과
  4.mask/            # 마스크 이미지/좌표
  5.dataset/         # 학습용 데이터셋
  6.preprocessed/    # 전처리 산출물
  7.results/         # 실험/분석 결과
  8.ground_truth/    # 확정 GT
```

## 2) Phase별 엔트리포인트

### Phase 1: 데이터 준비(탐지/마스크/전처리)

- 메인 런처: `scripts/01_data_preparation/main_launcher.py`
  - 대표 옵션: `--category`, `--plot`, `--preprocess`, `--save-npy`, `--target-size`
  - 내부에서 SAM2 로더 패치 시도(`custom_helpers.patch_grounded_sam2()`)
- Autodistill 러너: `scripts/01_data_preparation/autodistill_runner.py`
  - Florence-2 분류(JSON) + GroundedSAM2 탐지/마스크

### Phase 2: Few-Shot 분류/분석

- 웹 플랫폼: `scripts/03_classification/run_few_shot_platform.py --webapp`
- CLI 실험: `scripts/03_classification/run_shot_threshold_experiments.py`
- 분석: `scripts/03_classification/analyze_experiment_metrics.py`, `run_model_comparison.py`

### Phase 3: Ground Truth 생성/검증

- 폴더 기반 라벨러: `scripts/04_ground_truth/folder_based_labeler.py`
- 대화형 라벨러: `scripts/04_ground_truth/ground_truth_labeler.py`
- 평가: `scripts/04_ground_truth/evaluate_ground_truth.py`

### Phase 4: 최종 모델 학습(YOLO 등)

- `scripts/05_yolo_training/...` (데이터셋 생성, 학습 스크립트)

## 3) 대표 실행 커맨드

```bash
# A. 전체 파이프라인(탐지+시각화+전처리)
python scripts/01_data_preparation/main_launcher.py \
  --category <your_category> \
  --plot \
  --preprocess

# B. Florence-2 + SAM2 자동 라벨링
python scripts/01_data_preparation/autodistill_runner.py \
  --category <your_category>

# C. Few-Shot 웹 플랫폼
python scripts/03_classification/run_few_shot_platform.py --webapp

# D. Ground Truth 라벨러(폴더 기반)
python scripts/04_ground_truth/folder_based_labeler.py
```

## 4) 데이터 흐름(요약)

1. 원본 → Florence-2(박스/분류) → GroundedSAM2(마스크)
2. 전처리(`6.preprocessed/`) 및 결과(`7.results/`) 생성
3. Few-Shot 결과 정리/검토 → GT 확정(`8.ground_truth/`)
4. 최종 학습용 데이터셋(`5.dataset/`) 생성 및 학습

## 5) 설정/환경

- `requirements.txt`의 핵심 의존성: `autodistill-florence-2`, SAM2 관련 의존성
- GPU 가용 시 CUDA 사용 권장
- 대용량 모델/체크포인트는 `models/` 또는 캐시 디렉토리에 배치
