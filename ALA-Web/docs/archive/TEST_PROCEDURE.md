# ALA-Web 전체 테스트 절차 (First-Time User Test)

이 문서는 **처음 사용자**에게 발생 가능한 모든 문제를 사전에 발견하기 위한 완전한 테스트 절차입니다.

---

## 🎯 테스트 목표

1. ✅ 초기 설치 과정 검증
2. ✅ 백엔드/프론트엔드 실행 검증
3. ✅ UI/API 기능 검증
4. ✅ 에러 처리 검증

---

## 📋 사전 요구사항 체크

### 1. Python 설치 확인
```cmd
py --version
```
**예상 출력**: `Python 3.11.x` 또는 `Python 3.10.x`

**문제**: "py is not recognized"
**해결**: Python 3.11+ 설치 필요
- https://www.python.org/downloads/
- 설치 시 "Add Python to PATH" 체크 ✅

### 2. 디스크 공간 확인
**필요 공간**: 최소 500MB
- Python 가상환경: ~200MB
- Node.js 환경: ~150MB
- npm 패키지: ~150MB

---

## 🔧 Phase 1: 설치 테스트 (setup.bat)

### 1-1. 설치 스크립트 실행

**실행 방법**:
```cmd
cd C:\Users\user\Desktop\ALA-AutoLabelAgent\ALA-AutoLabelAgent\ALA-Web
setup.bat
```

또는 파일 탐색기에서 `setup.bat` 더블클릭

### 1-2. 예상 출력 및 체크포인트

```
========================================
ALA-Web Automated Setup
========================================

[1/5] Checking Python installation...
OK: Python found
```
✅ **체크**: "OK: Python found" 메시지 확인

```
[2/5] Setting up Backend...
Creating Python virtual environment...
Installing Python dependencies...
```
✅ **체크**: 
- `backend/ala` 폴더 생성됨
- 설치 진행 로그 표시됨 (1-2분 소요)

```
OK: Backend dependencies installed

[3/5] Setting up Frontend...
Creating Node.js environment...
Installing Node.js dependencies...
```
✅ **체크**:
- `frontend/nodeenv` 폴더 생성됨
- npm 패키지 다운로드 진행 (2-5분 소요)

```
OK: Frontend dependencies installed

[4/5] Setting up data directory...
OK: Data directory ready

[5/5] Setup Complete!
========================================

Next steps:
1. Run "start-backend.bat" to start backend server
2. Run "start-frontend.bat" to start frontend server
3. Or run "start-all.bat" to start both

Backend will be at: http://localhost:8000
Frontend will be at: http://localhost:5173
API Docs at: http://localhost:8000/docs

========================================

Setup complete! You can close this window.
```
✅ **체크**: 
- "Setup Complete!" 메시지 표시
- 창이 5초 후 자동 종료

### 1-3. 설치 결과 검증

**생성된 파일/폴더 확인**:
```
ALA-Web/
├── backend/
│   ├── ala/              ← Python 가상환경 (새로 생성)
│   └── data/             ← 데이터 폴더 (새로 생성)
│       ├── experiments.json
│       ├── support_sets.json
│       ├── query_sets.json
│       ├── tracking.json
│       ├── experiment_results.json
│       └── annotations.json
└── frontend/
    └── nodeenv/          ← Node.js 환경 (새로 생성)
```

**검증 명령**:
```cmd
dir backend\ala
dir backend\data
dir frontend\nodeenv
dir frontend\node_modules
```

✅ **모든 폴더가 존재해야 함**

### 1-4. 발생 가능한 문제

| 문제 | 원인 | 해결 |
|------|------|------|
| "Python not found" | Python 미설치 | Python 3.11+ 설치 |
| nodeenv 생성 실패 | 가상환경 미활성화 | setup.bat 재실행 |
| npm install 느림 | 네트워크 속도 | 정상, 기다리기 (최대 10분) |
| 권한 에러 | UAC 제한 | 관리자 권한으로 실행 |

---

## 🚀 Phase 2: 백엔드 실행 테스트

### 2-1. 백엔드 단독 실행

**실행**:
```cmd
start-backend.bat
```

### 2-2. 예상 출력

```
Starting ALA-Web Backend...

========================================
Backend Server Starting
========================================
URL: http://localhost:8000
API Docs: http://localhost:8000/docs
Press CTRL+C to stop
========================================

INFO:     Will watch for changes in these directories: ['C:\\...\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ **체크**: "Application startup complete." 메시지 확인

### 2-3. API 테스트

**브라우저에서 테스트**:

1. **Root API**
   - URL: http://localhost:8000/
   - 예상: `{"message":"ALA-Web API is running"}`

2. **Swagger UI**
   - URL: http://localhost:8000/docs
   - 예상: Interactive API 문서 표시

3. **Experiments API**
   - URL: http://localhost:8000/api/classification/experiment/list
   - 예상: 3개 실험 데이터 (`exp_001`, `exp_002`, `exp_003`)

4. **Support Sets API**
   - URL: http://localhost:8000/api/classification/support-set/list
   - 예상: 2개 support set (`support_v1`, `support_v2`)

5. **Tracking API**
   - URL: http://localhost:8000/api/tracking/status
   - 예상: 파이프라인 상태 (total_images: 3)

✅ **모든 엔드포인트에서 JSON 응답 반환**

### 2-4. 발생 가능한 문제

| 문제 | 원인 | 해결 |
|------|------|------|
| "No module named 'cv2'" | OpenCV 미설치 | `pip install opencv-python` |
| Port 8000 사용 중 | 다른 서버 실행 중 | 해당 프로세스 종료 |
| ImportError | 의존성 누락 | setup.bat 재실행 |

---

## 🎨 Phase 3: 프론트엔드 실행 테스트

### 3-1. 프론트엔드 단독 실행

**주의**: 백엔드가 실행 중이어야 API 호출 가능

**실행**:
```cmd
start-frontend.bat
```

### 3-2. 예상 출력

```
Starting ALA-Web Frontend...

========================================
Frontend Server Starting
========================================
URL: http://localhost:5173
Press CTRL+C to stop
========================================

  VITE v5.x.x  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

✅ **체크**: "ready in" 메시지와 URL 표시

### 3-3. UI 접근 테스트

**브라우저에서 접속**: http://localhost:5173

**예상 화면**:
1. 왼쪽 사이드바:
   - Annotate
   - Preprocessing
   - Classification ← **NEW**
   - Data Flow ← **NEW**
   - Gallery
   - Settings

2. 기본 페이지: Annotate 페이지 표시

✅ **체크**: 
- 사이드바 표시됨
- Classification, Data Flow 항목 보임
- 콘솔 에러 없음 (F12 개발자 도구)

### 3-4. 발생 가능한 문제

| 문제 | 원인 | 해결 |
|------|------|------|
| 빈 화면 | npm install 미완료 | setup.bat 재실행 |
| Port 5173 사용 중 | 다른 Vite 서버 | 해당 프로세스 종료 |
| 모듈 로드 실패 | 의존성 누락 | `npm install` 재실행 |

---

## 🔗 Phase 4: 통합 테스트 (start-all.bat)

### 4-1. 통합 실행

**실행**:
```cmd
start-all.bat
```

### 4-2. 예상 동작

1. **첫 번째 창 열림**: "ALA-Web Backend" 제목
   - 백엔드 서버 시작 로그

2. **3초 대기**

3. **두 번째 창 열림**: "ALA-Web Frontend" 제목
   - 프론트엔드 서버 시작 로그

4. **원본 창**: 3초 후 자동 종료

✅ **체크**: 2개의 서버 창이 유지됨

### 4-3. 서버 상태 확인

**백엔드**: http://localhost:8000/docs
**프론트엔드**: http://localhost:5173

✅ **둘 다 접속 가능해야 함**

---

## 🧪 Phase 5: 기능 테스트 (Classification Workflow)

### 5-1. Classification 페이지 접속

1. http://localhost:5173 열기
2. 왼쪽 사이드바에서 **"Classification"** 클릭

### 5-2. Experiments 탭 검증

**예상 화면**:
```
Classification Experiments    [+ New Experiment]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┌──────────────────────────────────────┐
│ exp_001: Cat vs Dog - Baseline [View]│
│ Support: support_v1 │ Query: batch_001│
│ Status: ✓ Completed │ Avg Conf: 0.82  │
│ Created: 2025-11-22 07:30            │
└──────────────────────────────────────┘
... (2 more experiments)
```

✅ **체크**:
- 3개 실험 표시됨
- 체크박스 작동
- [+ New Experiment] 버튼 보임

### 5-3. New Experiment 생성 테스트

1. **"+ New Experiment"** 클릭
2. 모달 창 열림
3. 입력:
   - Name: "Test Experiment"
   - Support Set: support_v1 선택
   - Query Set: query_batch_001 선택
4. **"Create Experiment"** 클릭

**예상 결과**:
- 모달 닫힘
- 새 실험이 목록에 추가됨
- Status: "created"

✅ **체크**: 새 실험이 보임

### 5-4. Support Sets 탭 검증

1. **"Support Sets"** 탭 클릭

**예상 화면**:
```
Support Set Management    [+ Create New]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2 support set(s) available
Support set management UI coming in Phase 5...
```

✅ **체크**: Placeholder 메시지 표시

### 5-5. Comparison 탭 검증

1. Experiments 탭으로 돌아가기
2. 2개 실험 체크박스 선택
3. **"Comparison"** 탭 클릭

**예상 화면**:
```
Comparing 2 experiments
Comparison UI coming in Phase 6...
```

✅ **체크**: 선택된 개수 표시

---

## 📊 Phase 6: Data Tracking 테스트

### 6-1. Data Flow 페이지 접속

1. 왼쪽 사이드바에서 **"Data Flow"** 클릭

### 6-2. 파이프라인 상태 검증

**예상 화면**:
```
Data Flow Tracking
Monitor images through the processing pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pipeline Overview
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│Uploaded │ →  │Annotated │ →  │Preprocessed│ → │Classified│
│  0      │    │  2       │    │  1       │    │  0       │
└─────────┘    └──────────┘    └──────────┘    └──────────┘

Total Images: 3
```

✅ **체크**:
- 4개 스테이지 카드 표시
- 숫자 데이터 로드됨

### 6-3. 에러 섹션 검증

**예상 화면**:
```
⚠ Errors (1)                    [Retry All]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┌──────────────────────────────────────┐
│ test_003.jpg                         │
│ Stage: annotated                     │
│ Model initialization failed   [Retry]│
└──────────────────────────────────────┘
```

✅ **체크**:
- 1개 에러 표시
- [Retry] 버튼 보임

---

## ✅ 전체 테스트 체크리스트

### 설치
- [ ] setup.bat 성공적으로 완료
- [ ] backend/ala 폴더 생성됨
- [ ] frontend/nodeenv 폴더 생성됨
- [ ] data/ 폴더 및 JSON 파일 생성됨

### 백엔드
- [ ] start-backend.bat 실행 성공
- [ ] http://localhost:8000 접속 가능
- [ ] http://localhost:8000/docs Swagger UI 표시
- [ ] /api/classification/experiment/list → 3개 실험
- [ ] /api/classification/support-set/list → 2개 support set
- [ ] /api/tracking/status → 3개 이미지

### 프론트엔드
- [ ] start-frontend.bat 실행 성공
- [ ] http://localhost:5173 접속 가능
- [ ] 사이드바에 "Classification", "Data Flow" 표시
- [ ] 콘솔 에러 없음

### 통합
- [ ] start-all.bat로 2개 서버 동시 실행
- [ ] 백엔드+프론트엔드 모두 작동

### 기능
- [ ] Classification 페이지 → 3개 실험 표시
- [ ] New Experiment 생성 가능
- [ ] Support Sets 탭 접근 가능
- [ ] Comparison 탭 접근 가능
- [ ] Data Flow 페이지 → 파이프라인 표시
- [ ] 에러 1개 표시됨

---

## 🐛 발견된 문제 기록

문제를 발견하면 여기에 기록하세요:

| # | 증상 | 재현 방법 | 우선순위 |
|---|------|-----------|----------|
| 1 | setup.bat pause 문제 | ~~setup.bat 실행~~ **수정 완료** | - |
| 2 |  |  |  |
| 3 |  |  |  |

---

## 📋 테스트 완료 후 보고

**형식**:
```
테스트 날짜: YYYY-MM-DD
테스터: [이름]
환경: Windows [버전], Python [버전]

✅ 통과한 항목: [개수]/[전체]
❌ 실패한 항목: [개수]

주요 발견 사항:
1. ...
2. ...

권장 사항:
1. ...
2. ...
```

---

**이 테스트를 완료하면 신규 사용자도 문제없이 사용 가능합니다!** 🎉
