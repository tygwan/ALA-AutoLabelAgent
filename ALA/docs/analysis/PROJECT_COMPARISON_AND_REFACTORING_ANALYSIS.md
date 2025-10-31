# PROJECT-AGI vs X-AnyLabeling 비교 분석 및 리팩토링 검토

## 📊 Executive Summary

이 문서는 현재 PROJECT-AGI 라벨링 프로젝트와 X-AnyLabeling의 비교 분석 및 프로그램화(리팩토링) 가능성을 검토합니다.

**핵심 결론**: PROJECT-AGI는 X-AnyLabeling 스타일로 프로그램화 가능하며, 오히려 독자적인 강점을 더욱 발전시킬 수 있는 기회입니다.

---

## 🔍 프로젝트 비교 분석

### 1. 아키텍처 비교

| 측면 | PROJECT-AGI (현재) | X-AnyLabeling | 평가 |
|------|-------------------|---------------|------|
| **UI 프레임워크** | Gradio (웹 기반) | PyQt5/PySide (데스크톱) | 각각 장단점 존재 |
| **배포 방식** | 웹 서버 + 브라우저 | 독립 실행형 데스크톱 앱 | X-Any가 설치 편의성 우세 |
| **접근성** | 브라우저로 어디서나 접근 | 로컬 설치 필요 | AGI가 원격 작업에 유리 |
| **코드 구조** | 모듈화된 Phase별 스크립트 | 플러그인 기반 모델 시스템 | 둘 다 확장성 우수 |
| **통합성** | 파이프라인 중심 | 어노테이션 도구 중심 | 목적이 다름 |

### 2. 기능 비교

#### X-AnyLabeling의 강점 🌟

1. **포괄적인 어노테이션 도구**
   - 다양한 형태 지원: 폴리곤, 회전 박스, 원, 선, 점 등
   - 드래그 앤 드롭 인터페이스
   - 실시간 시각적 피드백

2. **광범위한 모델 라이브러리** (50+ 모델)
   - YOLOv5/6/7/8/9/10/11/12 시리즈
   - SAM 변형들 (SAM, SAM-HQ, MobileSAM, EfficientViT-SAM 등)
   - 전문 모델들 (OCR, Pose, Depth, Tracking 등)
   - VLM (Vision-Language Models)

3. **다양한 포맷 지원**
   - Import/Export: COCO, VOC, YOLO, DOTA, MOT, MASK 등
   - 산업 표준 호환성

4. **비디오 처리**
   - 프레임 단위 어노테이션
   - 트래킹 기능

#### PROJECT-AGI의 독특한 강점 💎

1. **완전한 End-to-End 파이프라인**
   ```
   원본 이미지 → 자동 객체 탐지 → Few-Shot Learning → Ground Truth → YOLO 학습
   ```
   - X-AnyLabeling은 어노테이션 도구이지만, AGI는 전체 ML 파이프라인

2. **Few-Shot Learning 통합**
   - 소량의 예시로 자동 분류
   - 코사인 유사도 기반 분류기
   - ResNet, DINO, CLIP 등 다양한 특징 추출기
   - 실험 자동화 (N-shot × threshold 조합)

3. **자동화된 초기 라벨링**
   - Autodistill + SAM2 통합
   - Florence-2 기반 객체 탐지
   - 사람의 개입 최소화

4. **실험 관리 시스템**
   - 다양한 조합으로 자동 실험
   - 성능 평가 및 비교
   - 결과 추적 및 시각화

5. **Ground Truth 최적화 워크플로우**
   - 자동 분류 결과를 기반으로 수동 검증
   - 통계 기반 의사결정 지원
   - 배치 처리 및 필터링

---

## 🎯 리팩토링 가능성 및 전략

### ✅ 결론: 리팩토링 가능하며 권장됨

PROJECT-AGI는 X-AnyLabeling 스타일로 프로그램화할 수 있으며, 다음 두 가지 전략 중 선택 가능합니다:

### 전략 A: 통합 데스크톱 애플리케이션 (X-AnyLabeling 스타일)

**목표**: 전문가용 독립 실행형 데스크톱 애플리케이션

#### 아키텍처
```
PROJECT-AGI Desktop App
├── Main Application (PyQt6)
│   ├── Pipeline Manager
│   │   ├── Data Preparation Module
│   │   ├── Few-Shot Learning Module
│   │   ├── Ground Truth Module
│   │   └── YOLO Training Module
│   ├── Annotation Interface
│   │   ├── Image Viewer/Editor
│   │   ├── Shape Tools (Box, Polygon, Mask)
│   │   └── Class Management
│   ├── Model Manager
│   │   ├── Autodistill + SAM2
│   │   ├── Few-Shot Classifiers
│   │   └── YOLO Models
│   └── Experiment Dashboard
│       ├── Metrics Visualization
│       ├── Result Comparison
│       └── Export Tools
└── Backend Engine
    ├── Image Processing
    ├── Model Inference
    └── Data Management
```

#### 장점
- 설치 후 오프라인 작업 가능
- 빠른 응답성 (네트워크 레이턴시 없음)
- 파일 시스템 직접 접근
- 전문가 느낌의 UI

#### 단점
- 개발 시간이 더 오래 걸림
- 플랫폼별 빌드 필요 (Windows, Linux, macOS)
- 업데이트 배포가 복잡함

### 전략 B: 하이브리드 웹-데스크톱 앱 (권장 🌟)

**목표**: 웹 기술로 UI를 만들되, 데스크톱 앱처럼 배포

#### 아키텍처
```
PROJECT-AGI Hybrid App
├── Frontend (React/Vue.js + Electron/Tauri)
│   ├── Modern Web UI
│   ├── Responsive Design
│   └── Interactive Components
├── Backend (FastAPI/Flask)
│   ├── RESTful API
│   ├── WebSocket (실시간 업데이트)
│   └── Task Queue (Celery)
└── Packaging (Electron/Tauri)
    ├── Local Web Server Bundle
    ├── Desktop Integration
    └── Single Executable
```

#### 장점
- **최고의 두 세계**: 웹의 유연성 + 데스크톱의 편의성
- 기존 Gradio 코드 재사용 가능 (FastAPI로 전환)
- 크로스 플랫폼 빌드 자동화
- 자동 업데이트 쉬움
- 모던한 UI/UX
- Electron(더 무겁지만 성숙) 또는 Tauri(더 가볍지만 새로운 기술) 선택 가능

#### 단점
- 추가 레이어로 인한 약간의 오버헤드
- Electron의 경우 패키지 크기가 큼

---

## 📋 단계별 리팩토링 로드맵

### Phase 1: 아키텍처 설계 및 프로토타입 (2-3주)

#### 1.1 기술 스택 결정
- [ ] UI 프레임워크 선택
  - **Option A**: PyQt6 (X-AnyLabeling 스타일)
  - **Option B**: React + Electron/Tauri (권장)
  - **Option C**: Vue.js + Tauri (경량)

- [ ] 백엔드 프레임워크
  - **FastAPI** (권장) - 비동기, 빠름, 자동 문서화
  - Flask - 간단하지만 동기식

#### 1.2 프로젝트 구조 재설계
```
project-agi-desktop/
├── frontend/                  # UI 코드
│   ├── src/
│   │   ├── components/       # React/Vue 컴포넌트
│   │   │   ├── Pipeline/     # 파이프라인 관리
│   │   │   ├── Annotation/   # 어노테이션 인터페이스
│   │   │   ├── Experiment/   # 실험 대시보드
│   │   │   └── Common/       # 공통 컴포넌트
│   │   ├── services/         # API 클라이언트
│   │   ├── stores/           # 상태 관리
│   │   └── utils/
│   └── package.json
│
├── backend/                   # Python 백엔드
│   ├── api/                  # FastAPI 라우터
│   │   ├── pipeline.py       # 파이프라인 API
│   │   ├── annotation.py     # 어노테이션 API
│   │   ├── models.py         # 모델 관리 API
│   │   └── experiments.py    # 실험 API
│   ├── core/                 # 핵심 로직 (기존 코드 재사용)
│   │   ├── data_preparation/
│   │   ├── few_shot/
│   │   ├── ground_truth/
│   │   └── yolo_training/
│   ├── models/               # 데이터 모델
│   ├── services/             # 비즈니스 로직
│   └── main.py               # FastAPI 앱
│
├── shared/                    # 공유 리소스
│   ├── models/               # ML 모델 파일
│   ├── configs/              # 설정 파일
│   └── assets/               # 아이콘, 이미지
│
├── desktop/                   # 데스크톱 패키징
│   ├── electron/             # Electron 설정
│   │   ├── main.js
│   │   └── preload.js
│   └── tauri/                # Tauri 설정 (대안)
│       └── tauri.conf.json
│
├── tests/                     # 테스트
├── docs/                      # 문서
└── scripts/                   # 빌드/배포 스크립트
```

#### 1.3 프로토타입 개발
- [ ] 기본 UI 레이아웃
- [ ] 이미지 뷰어 구현
- [ ] Backend API 엔드포인트 3-5개
- [ ] 데스크톱 패키징 테스트

### Phase 2: 핵심 기능 구현 (4-6주)

#### 2.1 파이프라인 매니저
- [ ] Phase별 워크플로우 UI
- [ ] 진행 상황 추적
- [ ] 설정 관리
- [ ] 로그 뷰어

#### 2.2 어노테이션 인터페이스
- [ ] 이미지 로딩 및 표시
- [ ] 확대/축소/패닝
- [ ] 바운딩 박스 그리기
- [ ] 폴리곤/마스크 편집
- [ ] 클래스 레이블 관리
- [ ] 키보드 단축키

#### 2.3 Few-Shot Learning 통합
- [ ] Support Set 관리 UI
- [ ] 모델 선택기
- [ ] 실험 설정 패널
- [ ] 결과 시각화

#### 2.4 Ground Truth 도구
- [ ] 배치 선택
- [ ] 클래스 필터링
- [ ] 통계 대시보드
- [ ] 검증 인터페이스

### Phase 3: 고급 기능 (3-4주)

#### 3.1 모델 관리자
- [ ] 모델 다운로드/설치
- [ ] 모델 버전 관리
- [ ] 커스텀 모델 임포트
- [ ] 모델 성능 모니터링

#### 3.2 실험 대시보드
- [ ] 메트릭 차트
- [ ] 결과 비교 테이블
- [ ] Confusion Matrix 시각화
- [ ] 실험 히스토리

#### 3.3 데이터 임포트/익스포트
- [ ] COCO 포맷
- [ ] YOLO 포맷
- [ ] VOC 포맷
- [ ] 커스텀 포맷 플러그인

### Phase 4: 최적화 및 배포 (2-3주)

#### 4.1 성능 최적화
- [ ] 이미지 로딩 최적화
- [ ] 모델 추론 캐싱
- [ ] 메모리 관리
- [ ] GPU 가속

#### 4.2 사용성 개선
- [ ] 온보딩 튜토리얼
- [ ] 상황별 도움말
- [ ] 에러 핸들링
- [ ] 자동 저장

#### 4.3 빌드 및 배포
- [ ] Windows 빌드
- [ ] Linux 빌드
- [ ] macOS 빌드
- [ ] 자동 업데이트 시스템
- [ ] 설치 프로그램

---

## 🛠️ 구체적인 구현 가이드

### 1. 기술 스택 추천 (하이브리드 접근)

```yaml
Frontend:
  Framework: React 18 + TypeScript
  UI Library: Material-UI (MUI) 또는 Ant Design
  State Management: Zustand 또는 Redux Toolkit
  Canvas Library: Konva.js (어노테이션용) 또는 Fabric.js
  Charts: Recharts 또는 Chart.js
  Build Tool: Vite

Backend:
  Framework: FastAPI 0.104+
  Async: asyncio + uvicorn
  Task Queue: Celery + Redis (선택)
  ORM: SQLAlchemy (메타데이터용)
  Validation: Pydantic V2

Desktop Packaging:
  Primary: Electron 27+ (더 성숙함)
  Alternative: Tauri 1.5+ (더 가벼움)

ML/CV:
  Current Stack: (그대로 유지)
    - PyTorch
    - OpenCV
    - supervision
    - Autodistill
    - SAM2

Development:
  Code Quality: ESLint, Prettier, Black, mypy
  Testing: Jest (frontend), pytest (backend)
  Documentation: Storybook (컴포넌트), Swagger (API)
```

### 2. UI 설계 원칙

#### 2.1 레이아웃 구조
```
┌─────────────────────────────────────────────────────┐
│  Title Bar (앱 이름, 최소화, 최대화, 닫기)              │
├──────────┬──────────────────────────────────┬───────┤
│          │                                  │       │
│  Sidebar │      Main Canvas Area            │ Right │
│          │                                  │ Panel │
│  - Home  │   [이미지 뷰어 + 어노테이션 툴]      │       │
│  - Data  │                                  │ Props │
│  - FSL   │                                  │ Class │
│  - GT    │                                  │ Stats │
│  - Train │                                  │       │
│  - Exp.  │                                  │       │
│          │                                  │       │
├──────────┴──────────────────────────────────┴───────┤
│  Status Bar (진행 상황, 통계, 메시지)                  │
└─────────────────────────────────────────────────────┘
```

#### 2.2 핵심 화면 구성

**A. 홈 대시보드**
- 프로젝트 개요
- 최근 작업
- 빠른 시작 액션

**B. 데이터 준비 화면**
- 이미지 업로드/선택
- Support Set 구성
- Autodistill + SAM2 실행
- 결과 미리보기

**C. Few-Shot Learning 화면**
- 왼쪽: Support Set 갤러리
- 중앙: Query 이미지들
- 오른쪽: 설정 및 결과
- 하단: 실험 로그

**D. Ground Truth 화면**
- 이미지 그리드 뷰
- 필터 및 검색
- 배치 라벨링 툴
- 통계 패널

**E. 어노테이션 화면**
- 중앙: 큰 이미지 캔버스
- 왼쪽: 파일 브라우저
- 오른쪽: 도구 패널 + 오브젝트 리스트
- 하단: 썸네일 스트립

**F. 실험 대시보드**
- 실험 리스트
- 메트릭 비교 차트
- Confusion Matrix
- 상세 리포트

### 3. API 설계

#### 3.1 RESTful API 엔드포인트

```python
# FastAPI 예시

from fastapi import FastAPI, UploadFile, WebSocket
from pydantic import BaseModel

app = FastAPI()

# Project Management
@app.get("/api/v1/projects")
async def list_projects():
    """프로젝트 목록 조회"""
    pass

@app.post("/api/v1/projects")
async def create_project(name: str, description: str):
    """새 프로젝트 생성"""
    pass

@app.get("/api/v1/projects/{project_id}")
async def get_project(project_id: str):
    """프로젝트 상세 정보"""
    pass

# Data Preparation
@app.post("/api/v1/data/upload")
async def upload_images(files: list[UploadFile]):
    """이미지 업로드"""
    pass

@app.post("/api/v1/data/autodistill")
async def run_autodistill(project_id: str, config: dict):
    """Autodistill + SAM2 실행"""
    pass

@app.get("/api/v1/data/status/{task_id}")
async def get_task_status(task_id: str):
    """작업 진행 상황 조회"""
    pass

# Few-Shot Learning
@app.post("/api/v1/fsl/support-set")
async def create_support_set(project_id: str, images: list[str]):
    """Support Set 생성"""
    pass

@app.post("/api/v1/fsl/classify")
async def run_few_shot(
    project_id: str,
    model: str,
    n_shots: int,
    threshold: float
):
    """Few-Shot 분류 실행"""
    pass

@app.get("/api/v1/fsl/results/{experiment_id}")
async def get_fsl_results(experiment_id: str):
    """분류 결과 조회"""
    pass

# Ground Truth
@app.get("/api/v1/gt/images")
async def list_gt_images(
    project_id: str,
    class_filter: str = None,
    skip: int = 0,
    limit: int = 100
):
    """GT 이미지 목록 (페이지네이션)"""
    pass

@app.post("/api/v1/gt/label")
async def set_ground_truth(image_ids: list[str], label: str):
    """Ground Truth 라벨 설정"""
    pass

@app.get("/api/v1/gt/statistics")
async def get_gt_statistics(project_id: str):
    """GT 통계"""
    pass

# Annotation
@app.get("/api/v1/annotations/{image_id}")
async def get_annotations(image_id: str):
    """이미지의 어노테이션 조회"""
    pass

@app.post("/api/v1/annotations")
async def save_annotation(image_id: str, annotations: list[dict]):
    """어노테이션 저장"""
    pass

# Export
@app.post("/api/v1/export/coco")
async def export_coco(project_id: str):
    """COCO 포맷으로 익스포트"""
    pass

@app.post("/api/v1/export/yolo")
async def export_yolo(project_id: str):
    """YOLO 포맷으로 익스포트"""
    pass

# WebSocket for real-time updates
@app.websocket("/ws/progress/{task_id}")
async def websocket_progress(websocket: WebSocket, task_id: str):
    """실시간 진행 상황 업데이트"""
    await websocket.accept()
    # ... streaming progress updates
```

#### 3.2 데이터 모델 (Pydantic)

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Project(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    category: str
    total_images: int
    labeled_images: int
    
class Annotation(BaseModel):
    id: str
    image_id: str
    type: str  # "box", "polygon", "mask"
    label: str
    confidence: Optional[float]
    coordinates: dict
    metadata: Optional[dict]
    
class FewShotExperiment(BaseModel):
    id: str
    project_id: str
    model_name: str
    n_shots: int
    threshold: float
    accuracy: Optional[float]
    created_at: datetime
    status: str  # "pending", "running", "completed", "failed"
    results: Optional[dict]
    
class GroundTruthImage(BaseModel):
    id: str
    filename: str
    path: str
    predicted_class: Optional[str]
    ground_truth_class: Optional[str]
    confidence: Optional[float]
    is_verified: bool
```

### 4. 어노테이션 캔버스 구현

#### 4.1 Konva.js 기반 구현 (React 예시)

```typescript
// components/AnnotationCanvas.tsx

import React, { useEffect, useRef, useState } from 'react';
import { Stage, Layer, Image, Rect, Line } from 'react-konva';
import useImage from 'use-image';

interface Annotation {
  id: string;
  type: 'box' | 'polygon';
  points: number[];
  label: string;
  color: string;
}

interface AnnotationCanvasProps {
  imageUrl: string;
  annotations: Annotation[];
  selectedTool: 'box' | 'polygon' | 'select';
  onAnnotationsChange: (annotations: Annotation[]) => void;
}

export const AnnotationCanvas: React.FC<AnnotationCanvasProps> = ({
  imageUrl,
  annotations,
  selectedTool,
  onAnnotationsChange
}) => {
  const [image] = useImage(imageUrl);
  const [isDrawing, setIsDrawing] = useState(false);
  const [currentAnnotation, setCurrentAnnotation] = useState<Annotation | null>(null);
  const stageRef = useRef<any>(null);
  
  const handleMouseDown = (e: any) => {
    if (selectedTool === 'select') return;
    
    const pos = e.target.getStage().getPointerPosition();
    setIsDrawing(true);
    
    if (selectedTool === 'box') {
      setCurrentAnnotation({
        id: `temp-${Date.now()}`,
        type: 'box',
        points: [pos.x, pos.y, pos.x, pos.y],
        label: 'unknown',
        color: '#00ff00'
      });
    }
  };
  
  const handleMouseMove = (e: any) => {
    if (!isDrawing || !currentAnnotation) return;
    
    const pos = e.target.getStage().getPointerPosition();
    
    if (selectedTool === 'box') {
      setCurrentAnnotation({
        ...currentAnnotation,
        points: [
          currentAnnotation.points[0],
          currentAnnotation.points[1],
          pos.x,
          pos.y
        ]
      });
    }
  };
  
  const handleMouseUp = () => {
    if (!isDrawing || !currentAnnotation) return;
    
    setIsDrawing(false);
    onAnnotationsChange([...annotations, currentAnnotation]);
    setCurrentAnnotation(null);
  };
  
  return (
    <Stage
      ref={stageRef}
      width={window.innerWidth * 0.7}
      height={window.innerHeight * 0.8}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
    >
      <Layer>
        {image && <Image image={image} />}
        
        {annotations.map(ann => {
          if (ann.type === 'box') {
            const [x1, y1, x2, y2] = ann.points;
            return (
              <Rect
                key={ann.id}
                x={Math.min(x1, x2)}
                y={Math.min(y1, y2)}
                width={Math.abs(x2 - x1)}
                height={Math.abs(y2 - y1)}
                stroke={ann.color}
                strokeWidth={2}
                draggable
              />
            );
          }
          return null;
        })}
        
        {currentAnnotation && currentAnnotation.type === 'box' && (
          <Rect
            x={Math.min(currentAnnotation.points[0], currentAnnotation.points[2])}
            y={Math.min(currentAnnotation.points[1], currentAnnotation.points[3])}
            width={Math.abs(currentAnnotation.points[2] - currentAnnotation.points[0])}
            height={Math.abs(currentAnnotation.points[3] - currentAnnotation.points[1])}
            stroke="#00ff00"
            strokeWidth={2}
            dash={[4, 4]}
          />
        )}
      </Layer>
    </Stage>
  );
};
```

### 5. 데스크톱 패키징

#### 5.1 Electron 설정

```javascript
// desktop/electron/main.js

const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let backendProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1600,
    height: 1000,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, '../../assets/icon.png')
  });

  // Development: 개발 서버로 로드
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    // Production: 빌드된 파일 로드
    mainWindow.loadFile(path.join(__dirname, '../../frontend/dist/index.html'));
  }
}

function startBackend() {
  // Python 백엔드 서버 시작
  const pythonPath = process.env.NODE_ENV === 'development'
    ? 'python'
    : path.join(process.resourcesPath, 'python/python');
  
  const backendPath = process.env.NODE_ENV === 'development'
    ? path.join(__dirname, '../../backend/main.py')
    : path.join(process.resourcesPath, 'backend/main.py');
  
  backendProcess = spawn(pythonPath, [backendPath], {
    env: { ...process.env, PYTHONUNBUFFERED: '1' }
  });
  
  backendProcess.stdout.on('data', (data) => {
    console.log(`Backend: ${data}`);
  });
  
  backendProcess.stderr.on('data', (data) => {
    console.error(`Backend Error: ${data}`);
  });
}

app.whenReady().then(() => {
  startBackend();
  
  // 백엔드가 준비될 때까지 대기
  setTimeout(() => {
    createWindow();
  }, 2000);
  
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (backendProcess) {
    backendProcess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  if (backendProcess) {
    backendProcess.kill();
  }
});
```

#### 5.2 빌드 설정 (package.json)

```json
{
  "name": "project-agi-desktop",
  "version": "1.0.0",
  "main": "desktop/electron/main.js",
  "scripts": {
    "dev": "concurrently \"npm run dev:frontend\" \"npm run dev:backend\"",
    "dev:frontend": "cd frontend && vite",
    "dev:backend": "cd backend && uvicorn main:app --reload --port 8000",
    "build": "npm run build:frontend && npm run build:backend && npm run build:electron",
    "build:frontend": "cd frontend && vite build",
    "build:backend": "pyinstaller backend/main.spec",
    "build:electron": "electron-builder",
    "electron": "electron ."
  },
  "build": {
    "appId": "com.yourcompany.project-agi",
    "productName": "PROJECT-AGI",
    "directories": {
      "output": "dist-electron"
    },
    "files": [
      "frontend/dist/**/*",
      "desktop/electron/**/*",
      "assets/**/*"
    ],
    "extraResources": [
      {
        "from": "backend/dist",
        "to": "backend"
      },
      {
        "from": "backend/models",
        "to": "models"
      }
    ],
    "win": {
      "target": "nsis",
      "icon": "assets/icon.ico"
    },
    "linux": {
      "target": "AppImage",
      "icon": "assets/icon.png",
      "category": "Graphics"
    },
    "mac": {
      "target": "dmg",
      "icon": "assets/icon.icns"
    }
  },
  "devDependencies": {
    "electron": "^27.0.0",
    "electron-builder": "^24.0.0",
    "concurrently": "^8.0.0"
  }
}
```

---

## 🚀 빠른 시작 가이드 (리팩토링 버전)

### 개발 환경 설정

```bash
# 1. 저장소 클론
git clone https://github.com/yourusername/project-agi-desktop.git
cd project-agi-desktop

# 2. 프론트엔드 의존성 설치
cd frontend
npm install
cd ..

# 3. 백엔드 의존성 설치
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..

# 4. 개발 서버 실행
npm run dev

# 5. Electron 앱 실행
npm run electron
```

### 프로덕션 빌드

```bash
# 전체 빌드 (Frontend + Backend + Electron)
npm run build

# 플랫폼별 빌드
npm run build:win     # Windows
npm run build:linux   # Linux
npm run build:mac     # macOS
```

---

## 📊 예상 개발 일정 및 리소스

### 인력 구성 (최소)
- **풀스택 개발자** 1명 (React + Python)
- **ML 엔지니어** 1명 (파트타임, 모델 통합)
- **UI/UX 디자이너** 1명 (파트타임, 초기 설계)

### 일정
- **Phase 1** (아키텍처): 2-3주
- **Phase 2** (핵심 기능): 4-6주
- **Phase 3** (고급 기능): 3-4주
- **Phase 4** (최적화/배포): 2-3주
- **총 기간**: 11-16주 (약 3-4개월)

### 우선순위별 개발 전략

#### MVP (Minimum Viable Product) - 6주
1. 이미지 로딩 및 표시
2. 기본 어노테이션 (바운딩 박스)
3. Autodistill + SAM2 통합
4. 결과 익스포트 (YOLO)

#### V1.0 - 12주
- MVP +
5. Few-Shot Learning 기능
6. Ground Truth 관리
7. 실험 대시보드
8. 데스크톱 패키징

#### V1.5 - 16주
- V1.0 +
9. 고급 어노테이션 (폴리곤, 마스크)
10. 추가 모델 지원
11. 플러그인 시스템
12. 성능 최적화

---

## 🎨 X-AnyLabeling과의 차별화 포인트

PROJECT-AGI는 X-AnyLabeling을 따라하는 것이 아니라, **고유한 가치 제안**을 가져야 합니다:

### 1. **Few-Shot Learning 중심 워크플로우** 🎯
- X-Any: 수동 어노테이션 → 모델 학습
- AGI: 소량 예시 → 자동 분류 → 검증 → 모델 학습

### 2. **완전 자동화 파이프라인** 🤖
- 원본 이미지만 있으면 최종 YOLO 모델까지 자동 생성
- 사람의 개입은 검증 단계에만 필요

### 3. **실험 중심 접근** 🔬
- 다양한 조합 자동 실험
- 성능 비교 및 최적 설정 추천
- 재현 가능한 실험 관리

### 4. **연구자 친화적** 📚
- Jupyter 노트북 통합
- 실험 로그 및 메트릭 추적
- 논문용 차트 및 표 생성

### 5. **도메인 특화 최적화** 🏭
- 특정 산업(예: 자율주행, 의료, 제조)에 특화된 프리셋
- 도메인별 모델 추천
- 맞춤형 평가 지표

---

## ⚠️ 리스크 및 대응 방안

### 리스크 1: 개발 범위 과다
**대응**: MVP 중심 개발, 단계적 기능 추가

### 리스크 2: 성능 이슈 (Electron)
**대응**: Tauri로 전환 가능하도록 설계

### 리스크 3: 크로스 플랫폼 호환성
**대응**: CI/CD에서 모든 플랫폼 자동 테스트

### 리스크 4: 모델 파일 크기
**대응**: 
- 모델 온디맨드 다운로드
- 경량 모델 우선 제공
- 클라우드 저장소 활용

### 리스크 5: Python 백엔드 패키징
**대응**:
- PyInstaller로 단일 실행 파일 생성
- 또는 Conda 환경 번들링

---

## 🎓 학습 리소스

### Electron + React
- Electron 공식 문서: https://www.electronjs.org/docs
- Electron React Boilerplate: https://electron-react-boilerplate.js.org/

### Tauri (경량 대안)
- Tauri 공식 문서: https://tauri.app/
- Tauri + React 가이드: https://tauri.app/v1/guides/getting-started/setup/react

### FastAPI
- FastAPI 공식 문서: https://fastapi.tiangolo.com/
- FastAPI WebSocket: https://fastapi.tiangolo.com/advanced/websockets/

### Canvas 라이브러리
- Konva.js: https://konvajs.org/
- Fabric.js: http://fabricjs.com/
- Paper.js: http://paperjs.org/

### 참고 프로젝트
- X-AnyLabeling: https://github.com/CVHub520/X-AnyLabeling
- LabelImg: https://github.com/heartexlabs/labelImg
- CVAT: https://github.com/opencv/cvat
- Label Studio: https://github.com/heartexlabs/label-studio

---

## 📝 결론 및 권장 사항

### ✅ 리팩토링 권장 이유

1. **사용자 경험 향상**: 브라우저 없이 독립 앱으로 실행
2. **배포 편의성**: 설치 프로그램으로 간편한 배포
3. **전문성**: 산업 표준 도구로서의 신뢰성
4. **확장성**: 모듈화된 아키텍처로 기능 추가 용이
5. **유지보수성**: 명확한 프론트엔드-백엔드 분리

### 🎯 추천 접근 방식

**하이브리드 웹-데스크톱 앱 (Electron/Tauri + React + FastAPI)**

이 방식은:
- 기존 코드를 최대한 재사용
- 모던한 웹 기술로 빠른 개발
- 데스크톱 앱의 편의성 제공
- 크로스 플랫폼 지원 용이

### 🚀 시작 단계

1. **프로토타입 개발** (2주)
   - 간단한 Electron + React + FastAPI 조합 테스트
   - 이미지 로딩 및 기본 UI
   - 기존 파이프라인 하나 통합

2. **피드백 수집**
   - 내부 사용자 테스트
   - 성능 및 UX 평가

3. **본격 개발 여부 결정**
   - 프로토타입 성공 시 전체 리팩토링 진행
   - 문제 발견 시 대안 검토

### 📞 Next Steps

이 분석 결과를 바탕으로:

1. **기술 스택 최종 확정**
2. **프로토타입 개발 시작**
3. **상세 기능 명세 작성**
4. **개발 일정 수립**

---

**작성일**: 2025-10-20
**버전**: 1.0
**작성자**: AI Assistant (Claude Sonnet 4.5)

