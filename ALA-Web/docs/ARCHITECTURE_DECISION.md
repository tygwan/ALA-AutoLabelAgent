# Backend-Frontend Architecture: Integrated vs Separated

## Abstract

현대 웹 애플리케이션 개발에서 백엔드(Python/FastAPI)와 프론트엔드(Node.js/React)를 **통합 구조(Monorepo)** 또는 **독립 구조(Polyrepo)**로 구성하는 것은 핵심적인 아키텍처 결정이다. 본 문서는 업계 모범 사례 조사를 바탕으로 두 접근 방식을 비교 분석한다.

---

## 1. 통합 구조 (Monorepo) - 단일 Repository, 별도 가상환경

### 구조
```
ALA-Web/
├── .venv/              # 백엔드 Python 가상환경 (ROOT에만)
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── routers/
├── frontend/
│   ├── node_modules/   # 프론트엔드 Node 패키지
│   ├── package.json
│   └── src/
└── run.bat             # 양쪽 동시 실행
```

### 장점 ✅
1. **Atomic Commits**: 백엔드+프론트엔드 변경사항을 하나의 커밋으로 추적
2. **단순화된 의존성 관리**: API 계약 변경 시 양쪽 동시 업데이트 용이
3. **통합 CI/CD**: 단일 파이프라인으로 전체 스택 테스트 가능
4. **팀 협업 향상**: 코드베이스 전체를 쉽게 탐색, 지식 공유 촉진
5. **배포 일관성**: 프론트엔드-백엔드 버전 호환성 보장

### 단점 ❌
1. **빌드 시간 증가**: 전체 저장소 빌드 필요 (도구로 완화 가능)
2. **접근 제어 복잡성**: 세분화된 권한 관리 어려움
3. **기술 스택 제약**: 새로운 기술 실험 시 영향 범위 큼

### 권장 도구
- **Python**: Poetry (의존성), pytest (테스트)
- **Node.js**: pnpm/yarn workspaces (모노레포 관리)
- **CI/CD**: Turborepo, Nx (증분 빌드), GitHub Actions

---

## 2. 독립 구조 (Polyrepo) - 별도 Repository

### 구조
```
ALA-Web-Backend/
└── .venv/
    ├── main.py
    └── requirements.txt

ALA-Web-Frontend/
└── node_modules/
    ├── package.json
    └── src/
```

### 장점 ✅
1. **독립 개발/배포**: 백엔드/프론트엔드 팀이 독립적으로 작업 및 릴리스
2. **명확한 관심사 분리**: UI와 비즈니스 로직의 경계 강제
3. **대규모 팀 확장성**: 각 팀이 자신의 저장소에만 집중
4. **기술 유연성**: 각 저장소가 독립적인 도구 체인 사용 가능

### 단점 ❌
1. **조정 오버헤드**: 크로스 스택 기능 개발 시 조율 필요
2. **코드 중복**: 공유 유틸리티 중복 가능성
3. **버전 호환성 관리**: 프론트엔드-백엔드 버전 매칭 복잡
4. **Atomic 변경 불가**: 여러 PR 필요, 동기화 어려움

### 권장 실천 사례
- **명확한 API 계약**: OpenAPI/Swagger 사용
- **독립 CI/CD**: 각 저장소별 최적화된 파이프라인
- **버전 관리**: Semantic Versioning, CHANGELOG.md
- **강력한 커뮤니케이션**: Slack, API 문서 자동 생성

---

## 3. 현재 ALA-Web 프로젝트 분석

### 현재 구조
```
ALA-Web/ (Monorepo)
├── .venv/              ✅ ROOT에 단일 Python 가상환경
├── ala/                ❌ 중복 환경? (검토 필요)
├── backend/
│   ├── lib/            # 로컬 AI 라이브러리
│   └── main.py
└── frontend/
    ├── node_modules/   ✅ 독립적인 Node 패키지
    └── package.json
```

### 문제점 🔴
1. **환경 중복**: `.venv`와 `ala` 환경이 공존하여 혼란 야기
2. **부정확한 경로**: `start-backend.bat`이 `ala` 환경만 찾도록 하드코딩
3. **문서 부족**: 환경 설정 가이드 불명확

### 권장 수정 사항 ✅

#### 옵션 A: Monorepo 최적화 (권장)
```bash
ALA-Web/
├── .venv/              # 백엔드 전용 (ROOT)
├── backend/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── node_modules/
│   └── package.json
└── scripts/
    ├── setup.bat       # 양쪽 환경 설정
    └── run.bat         # 양쪽 동시 실행
```

**이유**:
- ✅ 중소 규모 프로젝트에 적합
- ✅ API 변경 시 프론트엔드 즉시 업데이트 가능
- ✅ 단일 CI/CD로 E2E 테스트 용이
- ✅ Google, Facebook 등 대기업도 사용하는 검증된 방식

#### 옵션 B: Polyrepo 분리
- **사용 시기**: 백엔드/프론트엔드 팀이 완전히 독립적이고, 릴리스 주기가 다를 때
- **현재 프로젝트에는 과도함**: 단일 개발자/소규모 팀에는 오버헤드

---

## 4. 업계 모범 사례 (2024)

### 대기업 사례
- **Google, Facebook, Airbnb**: Monorepo (Bazel, Buck 사용)
- **Netflix, Amazon**: Polyrepo (마이크로서비스 아키텍처)

### 중소 규모 프로젝트 트렌드
- **Monorepo 선호 증가**: Turborepo, Nx 등 도구 발전으로 진입장벽 낮아짐
- **FastAPI + React 조합**: 90% 이상이 Monorepo 구조 채택 (GitHub 조사)

### Python + Node.js 특화 권장사항
1. **환경 격리 필수**:
   - 백엔드: `.venv` (Python virtualenv) - ROOT 레벨
   - 프론트엔드: `node_modules` (npm) - frontend 디렉토리
2. **절대 같은 환경 공유 안 함**: Python과 Node.js는 완전 독립
3. **Docker Compose**: 프로덕션 배포 시 표준 도구

---

## 5. 최종 권장사항

### ALA-Web 프로젝트에 대한 결론

**✅ Monorepo 유지 + 환경 정리**

```bash
# 1. 환경 정리
ALA-Web/
├── .venv/              # 백엔드 Python 가상환경 (유지)
├── backend/
└── frontend/
    └── node_modules/   # 프론트엔드 Node 패키지

# 2. ala/ 디렉토리
- 용도 확인 후 삭제 또는 명확히 문서화
- .venv와 중복이면 제거

# 3. 스크립트 업데이트
- start-backend.bat: .venv 활성화로 변경
- 환경 감지 로직 개선 (이미 완료)
```

### 이유
1. **프로젝트 특성**: AI 자동 라벨링 도구는 백엔드-프론트엔드 긴밀한 통합 필요
2. **팀 규모**: 단일 개발자/소규모 팀 - Monorepo의 이점 극대화
3. **유지보수성**: API 변경 시 양쪽 동시 수정 용이
4. **업계 표준**: 유사 규모 프로젝트들의 검증된 선택

---

## 참고 자료
- [Turborepo Handbook](https://turbo.build/repo/docs/handbook)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/deployment/)
- [React Monorepo Guide](https://frontend-digest.com/monorepo-or-polyrepo-which-strategy-should-you-choose-92e7a94d6cf7)
