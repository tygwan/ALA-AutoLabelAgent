# ALA-Web Scripts

이 폴더에는 ALA-Web 프로젝트의 설치 및 실행 스크립트가 포함되어 있습니다.

## 📂 스크립트 구조

### 🔧 [setup/](setup/) - 설치 스크립트

프로젝트 설치 및 초기 설정:

- **[setup_all.bat](setup/setup_all.bat)** - 🌟 **전체 자동 설치** (권장)
  - Python 가상환경 생성
  - 백엔드 의존성 설치
  - 프론트엔드 의존성 설치
  - AI 모델 설치 (선택)
  
- **[setup_local_lib.bat](setup/setup_local_lib.bat)** - AI 모델만 설치
  - SAM2 git clone 및 설치
  - Florence-2 설치
  - 체크포인트 다운로드

---

### ▶️ [start/](start/) - 실행 스크립트

애플리케이션 실행:

- **[start_all.bat](start/start_all.bat)** - 🌟 **통합 실행** (권장)
  - 백엔드 서버 시작 (새 창)
  - 프론트엔드 서버 시작 (새 창)
  - 자동으로 브라우저 오픈
  
- **[start_backend.bat](start/start_backend.bat)** - 백엔드만 실행
  - FastAPI 서버: http://localhost:8000
  - API 문서: http://localhost:8000/docs
  
- **[start_frontend.bat](start/start_frontend.bat)** - 프론트엔드만 실행
  - Vite 개발 서버: http://localhost:5173

---

## 🚀 사용법

### 최초 설치 (딱 한 번만)

```bash
# 프로젝트 루트에서
scripts\setup\setup_all.bat
```

이 스크립트는:
1. ✅ Python 환경 확인 및 생성
2. ✅ 모든 의존성 설치
3. ✅ 데이터 폴더 생성
4. ⚡ AI 모델 설치 (사용자 선택)

### 애플리케이션 실행 (매번)

```bash
# 프로젝트 루트에서
scripts\start\start_all.bat
```

이 스크립트는:
1. 🚀 백엔드 서버 시작
2. 🎨 프론트엔드 서버 시작
3. 🌐 브라우저 자동 오픈

**접속**: http://localhost:5173

### 개별 실행 (개발 시)

**백엔드 개발**:
```bash
scripts\start\start_backend.bat
```

**프론트엔드 개발**:
```bash
scripts\start\start_frontend.bat
```

---

## 📝 스크립트 상세 정보

### setup_all.bat

**실행 전 준비사항**:
- Git 설치
- Python 3.11+ 설치
- Node.js 18+ 설치

**실행 시간**: 
- 기본 설치: ~5분
- AI 모델 포함: ~10-15분

**실행 내용**:
```
1. Python 가상환경 생성 (conda 또는 venv)
2. backend/requirements.txt 설치
3. frontend/package.json 설치
4. (선택) AI 모델 설치
```

**참고**: AI 모델 설치는 ~2GB 디스크 공간 필요

---

### start_all.bat

**실행 전 확인**:
- `setup_all.bat` 완료 여부
- 가상환경 활성화 (자동)

**포트**:
- Backend: 8000
- Frontend: 5173

**종료 방법**:
1. 각 터미널 창에서 `Ctrl+C`
2. 또는 터미널 창 닫기

---

## ⚠️ 문제 해결

### "가상환경을 찾을 수 없습니다"

**해결**:
```bash
# 가상환경 활성화
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS
```

### "포트가 이미 사용 중입니다"

**해결**:
```bash
# 포트 사용 프로세스 확인
netstat -ano | findstr :8000
netstat -ano | findstr :5173

# 프로세스 종료
taskkill /PID <PID> /F
```

### "npm install 실패"

**해결**:
```bash
cd frontend
npm cache clean --force
npm install --legacy-peer-deps
```

---

## 🔗 관련 문서

- 📖 [설치 가이드](../docs/installation/INSTALLATION.md)
- 🔧 [백엔드 개발 가이드](../docs/development/BACKEND_DEVELOPMENT_GUIDE.md)
- 🎨 [프론트엔드 개발 가이드](../docs/development/FRONTEND_SETUP.md)
- 🆘 [문제 해결](../docs/installation/troubleshooting/)

---

<div align="center">

[⬆ 프로젝트 루트로](../README.md)

</div>
