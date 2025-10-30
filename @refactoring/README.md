# @refactoring

리팩토링 산출물을 정리하는 디렉토리입니다. 기존 코드는 유지한 채, 구동 방식을 정확히 문서화하고 이후 단계적 리팩토링을 진행합니다.

## 문서 목록

- SAM2_RUNBOOK.md — SAM2 구동 방식 및 통합 포인트
- FLORENCE2_RUNBOOK.md — Florence-2 구동 방식 및 사용 패턴
- PROJECT_PIPELINE_RUNBOOK.md — 프로젝트 전체 구동 파이프라인 및 엔트리포인트

## 브랜치 전략 (권장)

- 작업 브랜치: `refactoring/runbooks`
- 커밋 단위: 문서 추가/갱신을 작은 단위로 빈번히 커밋

## 다음 단계

1) 세 러너블(runbook) 문서 검토 및 피드백 반영
2) FastAPI + Electron 프로토타입 분리 설계 문서화 (선택)
3) 점진적 모듈 경계 정의 및 인터페이스 고정


