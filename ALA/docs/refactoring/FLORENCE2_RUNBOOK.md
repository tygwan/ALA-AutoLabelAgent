# Florence-2 Runbook (VLM)

본 문서는 프로젝트 내 Florence-2 사용 방식과 실행 패턴을 정리합니다. Detection/Classification 사용 지점, 온톨로지 구성, 출력 아티팩트, 실행 커맨드를 포함합니다.

## 1) 핵심 개요

- 역할: 제로샷 텍스트-비전 기반 분류/탐지(프레이즈 그라우딩)로 클래스 후보 탐색 및 박스 생성
- 사용 위치: 데이터 준비(박스 생성), VLM 기반 분류 실험

## 2) 주요 구성 파일

- `modified_packages/autodistill_florence_2/model.py`
  - `class Florence2(DetectionBaseModel)`
  - HF 모델/프로세서 로드(예: `microsoft/Florence-2-large`), 프레이즈 그라우딩 결과를 `sv.Detections`로 변환
- `scripts/01_data_preparation/autodistill_runner.py`
  - `run_florence2_classification(...)`에서 `CaptionOntology` 구성 후 후보 클래스에 대한 신뢰도 산출 → `florence2_classification.json` 저장
- `scripts/03_classification/classifier_vlm.py`
  - `Florence2Classifier`로 VLM 기반 이미지 분류 실행(`microsoft/florence-2-base`)
- `scripts/03_classification/main_webapp.py`
  - 설정에서 Florence-2 사용 가능 토글
- 의존성: `requirements.txt` 내 `autodistill-florence-2`

## 3) 구동 흐름

1. 온톨로지 구성: `CaptionOntology`에 "무엇?" 형태의 프롬프트/레이블 매핑 생성
2. 모델 로드: `AutoProcessor`, `AutoModelFor...` 계열로 Florence-2 로드(CUDA 사용 권장)
3. 추론: 입력 이미지 → 캡션/프레이즈 그라우딩 → 박스/라벨/신뢰도 산출
4. 결과 저장: 분류 결과는 JSON, 탐지 결과는 `sv.Detections`로 후속 단계 전달

## 4) 실행 방법 (대표)

```bash
# 데이터 준비 단계에서의 분류(JSON 산출)
python scripts/01_data_preparation/autodistill_runner.py \
    --category <your_category>

# VLM 기반 분류 단독 실행(웹/CLI 모두 가능)
python scripts/03_classification/classifier_vlm.py \
    --category <your_category> \
    --classes "class_0,class_1,class_2" \
    --output-dir data/<your_category>/7.results/vlm
```

## 5) 출력 아티팩트

- `data/<category>/7.results/.../florence2_classification.json` (분류 스코어)
- 파이프라인 내 `sv.Detections` 객체(박스/신뢰도/마스크 연계용)

## 6) 주의사항

- VRAM 사용량이 크므로 GPU 메모리 여유 필요
- 반복 추론 시 메모리 누수 방지(세션/캐시 정리) 유의
- 클래스 설명(프롬프트) 문구 개선이 성능에 영향
