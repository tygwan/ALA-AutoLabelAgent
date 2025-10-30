# SAM2 Runbook (Segment Anything Model 2)

본 문서는 프로젝트 내 SAM2 구동 방식과 통합 포인트를 정리합니다. 모델 파일 위치, 코드 흐름, 실행 커맨드, 트러블슈팅을 포함합니다.

## 1) 핵심 개요

- 역할: Florence-2가 산출한 박스(xyxy)를 기반으로 픽셀 단위 마스크를 생성
- 사용 위치: 자동 라벨링/마스크 생성 파이프라인(데이터 준비 Phase)

## 2) 주요 구성 파일

- `modified_packages/autodistill_grounded_sam_2/helpers.py`
  - `load_SAM()`에서 SAM2 코드를 클론/로딩하고 체크포인트를 다운로드한 뒤 `SAM2ImagePredictor` 초기화
  - 기본 경로: `~/.cache/autodistill/segment_anything_2`
- `modified_packages/autodistill_grounded_sam_2/grounded_sam_2.py`
  - `GroundedSAM2`가 Florence-2 예측 박스를 받아 `predictor.predict(box=...)`로 마스크 생성 후 `sv.Detections.mask` 채움
- `scripts/01_data_preparation/custom_helpers.py`
  - `load_SAM_local()`, `patch_grounded_sam2()`로 SAM 로더를 프로젝트 로컬 디렉토리(`models/sam2/`) 사용으로 패치
- `scripts/01_data_preparation/main_launcher.py`
  - 런타임 초기에 `patch_grounded_sam2()` 호출(패치 실패 시 경고 로그)
- 설치 관련: `install_project.sh`, `models/README.md`

## 3) 구동 흐름

1. 런처 진입: `main_launcher.py` → `patch_grounded_sam2()`로 SAM 로더를 로컬 경로 사용으로 패치
2. 박스 획득: `GroundedSAM2` 내부에서 Florence-2로 박스 예측
3. 마스킹: `SAM2ImagePredictor.set_image(image)` → 각 박스에 대해 `predict(box=..., multimask_output=False)` → 최고 점수 마스크 선택
4. 반환: `sv.Detections`에 `.mask` 채워 후속 전처리/저장 단계로 전달

## 4) 모델/리소스 경로

- 로컬 경로(권장): `models/sam2/`
  - 코드: `models/sam2/segment-anything-2`
  - 체크포인트: `models/sam2/sam2_hiera_base_plus.pth`
- 캐시 경로(대체): `~/.cache/autodistill/segment_anything_2/`

## 5) 실행 방법 (대표)

```bash
# 전체 파이프라인(탐지+마스킹+전처리)
python scripts/01_data_preparation/main_launcher.py \
    --category <your_category> \
    --plot \
    --preprocess

# Autodistill 러너(Florence-2 + SAM2 조합)
python scripts/01_data_preparation/autodistill_runner.py \
    --category <your_category>
```

## 6) 체크리스트

- GPU(NVIDIA/CUDA) 정상 인식 여부
- `models/sam2/` 또는 캐시에 체크포인트 존재
- `segment-anything-2` 코드가 로드 가능 경로에 존재

## 7) 트러블슈팅

- SAM2 import 에러 → `models/sam2/segment-anything-2` 유무, `sys.path` 패치 로그 확인
- 체크포인트 없음 → `models/sam2/sam2_hiera_base_plus.pth` 존재 확인(설치 스크립트/수동 다운로드)
- 추론 느림 → `torch.cuda.is_available()` 체크, 드라이버/런타임 버전 확인
