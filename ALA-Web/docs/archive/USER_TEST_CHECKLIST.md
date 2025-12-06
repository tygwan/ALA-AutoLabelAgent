# 🧪 ALA-Web 테스트 체크리스트 (직접 실행용)

**소요 시간**: 약 10-15분
**목표**: 모든 기능이 정상 작동하는지 확인

---

## ✅ 체크리스트

복사해서 결과를 기록하세요:
```
[ ] 1. 사전 확인
[ ] 2. 백엔드 서버 시작
[ ] 3. 백엔드 API 테스트
[ ] 4. 프론트엔드 설치 (최초 1회)
[ ] 5. 프론트엔드 서버 시작
[ ] 6. UI 접속 확인
[ ] 7. Classification 페이지 테스트
[ ] 8. Data Flow 페이지 테스트
```

---

## 1️⃣ 사전 확인

### Python 버전 확인
```cmd
py --version
```
**예상**: `Python 3.11.x` 또는 `Python 3.10.x`

✅ PASS: ___________  
❌ FAIL: ___________

---

## 2️⃣ 백엔드 서버 시작

### 새 터미널 열기 (터미널 #1)

```cmd
cd C:\Users\user\Desktop\ALA-AutoLabelAgent\ALA-AutoLabelAgent\ALA-Web\backend
.\ala\Scripts\activate.bat
python -m uvicorn main:app --reload --port 8000
```

### 예상 출력
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**✅ 체크**: "Application startup complete." 메시지 확인

✅ PASS: ___________  
❌ FAIL: ___________

**이 터미널은 열어두기** (서버 실행 중)

---

## 3️⃣ 백엔드 API 테스트

### 브라우저에서 테스트

#### 3-1. Root API
- URL: http://localhost:8000/
- **예상**: `{"message":"ALA-Web API is running"}`

✅ PASS: ___________  
❌ FAIL: ___________

#### 3-2. Swagger UI
- URL: http://localhost:8000/docs
- **예상**: API 문서 페이지 표시

✅ PASS: ___________  
❌ FAIL: ___________

#### 3-3. Experiments API
- URL: http://localhost:8000/api/classification/experiment/list
- **예상**: JSON with 3 experiments (exp_001, exp_002, exp_003)

✅ PASS: ___________  
❌ FAIL: ___________

#### 3-4. Tracking API
- URL: http://localhost:8000/api/tracking/status
- **예상**: `{"stages":{...},"total_images":3}`

✅ PASS: ___________  
❌ FAIL: ___________

---

## 4️⃣ 프론트엔드 설치 (최초 1회만)

### 새 터미널 열기 (터미널 #2)

```cmd
cd C:\Users\user\Desktop\ALA-AutoLabelAgent\ALA-AutoLabelAgent\ALA-Web\backend
.\ala\Scripts\activate.bat
cd ..\frontend
nodeenv --python-virtualenv nodeenv
```

**대기**: Node.js 다운로드 및 설치 (2-3분)

### 예상 출력 (마지막 줄)
```
Done.
```

✅ PASS: ___________  
❌ FAIL: ___________

### Node.js 환경 활성화 및 패키지 설치

```cmd
nodeenv\Scripts\activate.bat
npm install
```

**대기**: npm 패키지 설치 (3-5분)

### 예상 출력 (마지막 부분)
```
added xxx packages, and audited xxx packages in xxs
```

✅ PASS: ___________  
❌ FAIL: ___________

---

## 5️⃣ 프론트엔드 서버 시작

### 같은 터미널 (터미널 #2)에서

```cmd
npm run dev
```

### 예상 출력
```
  VITE v5.x.x  ready in xxxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**✅ 체크**: "ready in" 메시지와 URL 확인

✅ PASS: ___________  
❌ FAIL: ___________

**이 터미널도 열어두기** (서버 실행 중)

---

## 6️⃣ UI 접속 확인

### 브라우저에서 접속
```
http://localhost:5173
```

### 예상 화면
- 왼쪽 사이드바 보임:
  - Annotate
  - Preprocessing  
  - **Classification** ← 새로 추가
  - **Data Flow** ← 새로 추가
  - Gallery
  - Settings

✅ PASS: ___________  
❌ FAIL: ___________

### F12 개발자 도구 → Console 탭
- 에러 메시지 없어야 함 (경고는 무시)

✅ PASS (콘솔 에러 없음): ___________  
❌ FAIL (에러 있음): ___________

---

## 7️⃣ Classification 페이지 테스트

### 7-1. 페이지 접속
1. 왼쪽 사이드바에서 **"Classification"** 클릭

### 7-2. Experiments 탭 확인

**예상**:
- 3개 실험 카드 표시됨:
  - exp_001: Cat vs Dog - Baseline
  - exp_002: Cat vs Dog - More Support Images  
  - exp_003: Testing New Query Set
- 각 카드에 체크박스, 상태, 버튼 있음

✅ PASS: ___________  
❌ FAIL: ___________

### 7-3. New Experiment 생성 테스트

1. **"+ New Experiment"** 버튼 클릭
2. 모달 창 열림
3. 입력:
   - Experiment Name: `My Test Experiment`
   - Support Set: `support_v1` 선택
   - Query Set: `query_batch_001` 선택
4. **"Create Experiment"** 버튼 클릭
5. 모달 닫힘
6. 새 실험이 목록 맨 위에 추가됨 (Status: created)

✅ PASS: ___________  
❌ FAIL: ___________

### 7-4. Support Sets 탭 확인

1. **"Support Sets"** 탭 클릭
2. **예상**: "2 support set(s) available" 메시지

✅ PASS: ___________  
❌ FAIL: ___________

### 7-5. Comparison 탭 확인

1. **"Experiments"** 탭으로 돌아가기
2. 2개 실험 체크박스 선택
3. **"Comparison"** 탭 클릭
4. **예상**: "Comparing 2 experiments" 메시지

✅ PASS: ___________  
❌ FAIL: ___________

---

## 8️⃣ Data Flow 페이지 테스트

### 8-1. 페이지 접속
1. 왼쪽 사이드바에서 **"Data Flow"** 클릭

### 8-2. 파이프라인 상태 확인

**예상**:
- "Pipeline Overview" 섹션
- 4개 스테이지 카드:
  - Uploaded: 0
  - Annotated: 2
  - Preprocessed: 1
  - Classified: 0
- Total Images: 3

✅ PASS: ___________  
❌ FAIL: ___________

### 8-3. 에러 섹션 확인

**예상**:
- "Errors (1)" 표시
- 1개 에러 카드:
  - test_003.jpg
  - Stage: annotated
  - Error: Model initialization failed
  - [Retry] 버튼 있음

✅ PASS: ___________  
❌ FAIL: ___________

---

## 📊 최종 점수

총 항목: **18개**

통과: _____ / 18  
실패: _____ / 18

---

## 🎉 모두 통과했다면

축하합니다! ALA-Web이 정상적으로 작동합니다.

**다음 단계**:
- 실제 이미지로 실험 생성
- Florence-2 + SAM2 모델 통합
- 분류 알고리즘 구현

---

## ❌ 실패한 항목이 있다면

### 일반적인 문제 해결

**백엔드 시작 실패**:
```cmd
cd backend
.\ala\Scripts\activate.bat
pip install fastapi uvicorn pydantic python-multipart opencv-python pillow numpy
python -m uvicorn main:app --reload --port 8000
```

**프론트엔드 npm install 실패**:
```cmd
cd frontend
nodeenv\Scripts\activate.bat
npm cache clean --force
npm install
```

**Port 이미 사용 중**:
- 8000 포트: 다른 백엔드 서버 종료
- 5173 포트: 다른 Vite 서버 종료

**그래도 안 되면 처음부터**:
```cmd
cd ALA-Web
setup.bat
```

---

## 💡 팁

1. **터미널 2개 유지**: 백엔드 + 프론트엔드 각각 실행
2. **자동 새로고침**: 코드 수정 시 자동 반영됨
3. **서버 중지**: CTRL+C
4. **로그 확인**: 터미널에서 에러 메시지 확인

---

**테스트 날짜**: _______________  
**테스터**: _______________  
**환경**: Windows _____, Python _____
