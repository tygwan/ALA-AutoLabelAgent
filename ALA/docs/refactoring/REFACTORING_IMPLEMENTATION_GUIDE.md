# PROJECT-AGI 리팩토링 실전 구현 가이드

## 📋 개요

이 문서는 PROJECT-AGI를 데스크톱 애플리케이션으로 리팩토링하기 위한 **실전 구현 가이드**입니다. 단계별 코드 예시와 함께 실제로 작업할 수 있는 내용을 담고 있습니다.

---

## 🎯 Phase 0: 사전 준비 및 프로토타입 (1-2주)

### 목표
- 기술 스택 검증
- 기존 코드와의 통합 가능성 확인
- MVP 범위 확정

### Step 1: 기본 프로젝트 구조 생성

```bash
# 새 디렉토리 생성
mkdir project-agi-desktop
cd project-agi-desktop

# Git 초기화
git init

# 기본 구조 생성
mkdir -p frontend/{src/{components,services,stores,utils},public}
mkdir -p backend/{api,core,models,services,utils}
mkdir -p desktop/{electron,tauri}
mkdir -p shared/{configs,assets}
mkdir -p tests/{frontend,backend,e2e}
mkdir -p docs

# README 파일들
touch README.md
touch frontend/README.md
touch backend/README.md
```

### Step 2: 프론트엔드 초기화 (React + Vite)

```bash
cd frontend

# Vite로 React + TypeScript 프로젝트 생성
npm create vite@latest . -- --template react-ts

# 필수 패키지 설치
npm install

# 추가 패키지 설치
npm install \
  @mui/material @emotion/react @emotion/styled \
  @mui/icons-material \
  react-router-dom \
  axios \
  zustand \
  konva react-konva \
  recharts \
  react-dropzone

# 개발 도구
npm install -D \
  @types/node \
  eslint \
  prettier

cd ..
```

### Step 3: 백엔드 초기화 (FastAPI)

```bash
cd backend

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 기본 패키지 설치
pip install \
  fastapi \
  uvicorn[standard] \
  pydantic \
  python-multipart \
  aiofiles \
  sqlalchemy \
  pillow

# 기존 프로젝트 의존성
pip install \
  torch torchvision \
  opencv-python \
  supervision \
  autodistill \
  numpy \
  tqdm

# requirements.txt 생성
pip freeze > requirements.txt

cd ..
```

### Step 4: 최소 기능 프로토타입 구현

#### 4.1 백엔드 API (backend/main.py)

```python
"""
PROJECT-AGI Desktop - Backend API
최소 기능 프로토타입
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from pathlib import Path
import shutil
import uuid
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="PROJECT-AGI API",
    description="AI-powered image labeling platform",
    version="0.1.0"
)

# CORS 설정 (프론트엔드와 통신)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 개발 서버
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터 디렉토리 설정
DATA_DIR = Path("../data")
DATA_DIR.mkdir(exist_ok=True)

# Pydantic 모델들
class Project(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    category: str
    total_images: int = 0
    
class ImageInfo(BaseModel):
    id: str
    filename: str
    path: str
    width: Optional[int] = None
    height: Optional[int] = None

# ============================================
# 프로젝트 관리 API
# ============================================

@app.get("/")
async def root():
    """API 상태 확인"""
    return {
        "status": "ok",
        "message": "PROJECT-AGI API is running",
        "version": "0.1.0"
    }

@app.get("/api/v1/projects", response_model=List[Project])
async def list_projects():
    """프로젝트 목록 조회"""
    projects = []
    
    if DATA_DIR.exists():
        for item in DATA_DIR.iterdir():
            if item.is_dir():
                # 이미지 개수 카운트
                images_dir = item / "1.images"
                image_count = 0
                if images_dir.exists():
                    image_count = len(list(images_dir.glob("*.jpg"))) + \
                                 len(list(images_dir.glob("*.png")))
                
                projects.append(Project(
                    id=item.name,
                    name=item.name,
                    category=item.name,
                    total_images=image_count
                ))
    
    return projects

@app.post("/api/v1/projects", response_model=Project)
async def create_project(name: str, description: Optional[str] = None):
    """새 프로젝트 생성"""
    project_dir = DATA_DIR / name
    
    if project_dir.exists():
        raise HTTPException(status_code=400, detail="Project already exists")
    
    # 디렉토리 구조 생성
    dirs = [
        "1.images",
        "2.support-set",
        "3.box",
        "4.mask",
        "5.dataset",
        "6.preprocessed",
        "7.results",
        "8.ground_truth"
    ]
    
    for dir_name in dirs:
        (project_dir / dir_name).mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Created project: {name}")
    
    return Project(
        id=name,
        name=name,
        description=description,
        category=name,
        total_images=0
    )

@app.get("/api/v1/projects/{project_id}", response_model=Project)
async def get_project(project_id: str):
    """프로젝트 상세 정보"""
    project_dir = DATA_DIR / project_id
    
    if not project_dir.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    
    # 이미지 개수 카운트
    images_dir = project_dir / "1.images"
    image_count = 0
    if images_dir.exists():
        image_count = len(list(images_dir.glob("*.jpg"))) + \
                     len(list(images_dir.glob("*.png")))
    
    return Project(
        id=project_id,
        name=project_id,
        category=project_id,
        total_images=image_count
    )

# ============================================
# 이미지 관리 API
# ============================================

@app.post("/api/v1/projects/{project_id}/images/upload")
async def upload_images(
    project_id: str,
    files: List[UploadFile] = File(...)
):
    """이미지 업로드"""
    project_dir = DATA_DIR / project_id
    
    if not project_dir.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    
    images_dir = project_dir / "1.images"
    images_dir.mkdir(exist_ok=True)
    
    uploaded_files = []
    
    for file in files:
        # 파일 확장자 확인
        if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        
        # 고유 파일명 생성
        file_id = str(uuid.uuid4())
        ext = Path(file.filename).suffix
        new_filename = f"{file_id}{ext}"
        file_path = images_dir / new_filename
        
        # 파일 저장
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        uploaded_files.append({
            "id": file_id,
            "original_name": file.filename,
            "saved_name": new_filename,
            "path": str(file_path)
        })
        
        logger.info(f"Uploaded: {file.filename} -> {new_filename}")
    
    return {
        "project_id": project_id,
        "uploaded_count": len(uploaded_files),
        "files": uploaded_files
    }

@app.get("/api/v1/projects/{project_id}/images", response_model=List[ImageInfo])
async def list_images(
    project_id: str,
    skip: int = 0,
    limit: int = 100
):
    """이미지 목록 조회"""
    project_dir = DATA_DIR / project_id
    images_dir = project_dir / "1.images"
    
    if not images_dir.exists():
        return []
    
    images = []
    all_images = sorted(images_dir.glob("*.jpg")) + sorted(images_dir.glob("*.png"))
    
    for img_path in all_images[skip:skip+limit]:
        images.append(ImageInfo(
            id=img_path.stem,
            filename=img_path.name,
            path=str(img_path)
        ))
    
    return images

@app.get("/api/v1/images/{project_id}/{image_id}")
async def get_image(project_id: str, image_id: str):
    """이미지 파일 제공"""
    project_dir = DATA_DIR / project_id
    images_dir = project_dir / "1.images"
    
    # 이미지 파일 찾기
    for ext in ['.jpg', '.jpeg', '.png']:
        img_path = images_dir / f"{image_id}{ext}"
        if img_path.exists():
            return FileResponse(img_path)
    
    raise HTTPException(status_code=404, detail="Image not found")

# ============================================
# 파이프라인 API (Phase 1 통합)
# ============================================

@app.post("/api/v1/projects/{project_id}/pipeline/autodistill")
async def run_autodistill(project_id: str):
    """Autodistill + SAM2 파이프라인 실행"""
    project_dir = DATA_DIR / project_id
    
    if not project_dir.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    
    # TODO: 실제 파이프라인 실행 로직 통합
    # 현재는 더미 응답
    
    return {
        "status": "started",
        "project_id": project_id,
        "task_id": str(uuid.uuid4()),
        "message": "Autodistill pipeline started"
    }

# ============================================
# 개발 서버 실행
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
```

#### 4.2 프론트엔드 App (frontend/src/App.tsx)

```typescript
import React, { useState, useEffect } from 'react';
import {
  Container,
  AppBar,
  Toolbar,
  Typography,
  Box,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  List,
  ListItem,
  ListItemText,
  CircularProgress
} from '@mui/material';
import axios from 'axios';

// API 기본 URL
const API_BASE_URL = 'http://localhost:8000/api/v1';

// 프로젝트 타입 정의
interface Project {
  id: string;
  name: string;
  description?: string;
  category: string;
  total_images: number;
}

interface ImageInfo {
  id: string;
  filename: string;
  path: string;
}

function App() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [images, setImages] = useState<ImageInfo[]>([]);
  const [loading, setLoading] = useState(false);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [newProjectName, setNewProjectName] = useState('');

  // 프로젝트 목록 로드
  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    setLoading(true);
    try {
      const response = await axios.get<Project[]>(`${API_BASE_URL}/projects`);
      setProjects(response.data);
    } catch (error) {
      console.error('Failed to load projects:', error);
    } finally {
      setLoading(false);
    }
  };

  // 프로젝트 생성
  const handleCreateProject = async () => {
    if (!newProjectName.trim()) return;

    try {
      await axios.post(`${API_BASE_URL}/projects`, null, {
        params: { name: newProjectName }
      });
      setCreateDialogOpen(false);
      setNewProjectName('');
      loadProjects();
    } catch (error) {
      console.error('Failed to create project:', error);
      alert('프로젝트 생성 실패');
    }
  };

  // 프로젝트 선택
  const handleSelectProject = async (project: Project) => {
    setSelectedProject(project);
    setLoading(true);
    
    try {
      const response = await axios.get<ImageInfo[]>(
        `${API_BASE_URL}/projects/${project.id}/images`
      );
      setImages(response.data);
    } catch (error) {
      console.error('Failed to load images:', error);
    } finally {
      setLoading(false);
    }
  };

  // 이미지 업로드
  const handleUploadImages = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!selectedProject || !event.target.files) return;

    const formData = new FormData();
    Array.from(event.target.files).forEach(file => {
      formData.append('files', file);
    });

    setLoading(true);
    try {
      await axios.post(
        `${API_BASE_URL}/projects/${selectedProject.id}/images/upload`,
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' }
        }
      );
      
      // 이미지 목록 새로고침
      handleSelectProject(selectedProject);
    } catch (error) {
      console.error('Failed to upload images:', error);
      alert('이미지 업로드 실패');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* 앱바 */}
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            PROJECT-AGI Desktop (Prototype)
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 4 }}>
        <Grid container spacing={3}>
          {/* 좌측: 프로젝트 목록 */}
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  프로젝트
                </Typography>
                <Button
                  variant="contained"
                  fullWidth
                  onClick={() => setCreateDialogOpen(true)}
                  sx={{ mb: 2 }}
                >
                  새 프로젝트
                </Button>

                {loading && !selectedProject ? (
                  <Box display="flex" justifyContent="center">
                    <CircularProgress />
                  </Box>
                ) : (
                  <List>
                    {projects.map(project => (
                      <ListItem
                        key={project.id}
                        button
                        selected={selectedProject?.id === project.id}
                        onClick={() => handleSelectProject(project)}
                      >
                        <ListItemText
                          primary={project.name}
                          secondary={`${project.total_images} 이미지`}
                        />
                      </ListItem>
                    ))}
                  </List>
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* 우측: 이미지 목록 */}
          <Grid item xs={12} md={9}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                  <Typography variant="h6">
                    {selectedProject ? selectedProject.name : '프로젝트를 선택하세요'}
                  </Typography>
                  
                  {selectedProject && (
                    <Button
                      variant="contained"
                      component="label"
                    >
                      이미지 업로드
                      <input
                        type="file"
                        hidden
                        multiple
                        accept="image/*"
                        onChange={handleUploadImages}
                      />
                    </Button>
                  )}
                </Box>

                {loading && selectedProject ? (
                  <Box display="flex" justifyContent="center" p={4}>
                    <CircularProgress />
                  </Box>
                ) : images.length > 0 ? (
                  <Grid container spacing={2}>
                    {images.map(image => (
                      <Grid item xs={6} sm={4} md={3} key={image.id}>
                        <Card>
                          <Box
                            component="img"
                            src={`http://localhost:8000/api/v1/images/${selectedProject?.id}/${image.id}`}
                            alt={image.filename}
                            sx={{
                              width: '100%',
                              height: 150,
                              objectFit: 'cover'
                            }}
                          />
                          <CardContent>
                            <Typography variant="caption" noWrap>
                              {image.filename}
                            </Typography>
                          </CardContent>
                        </Card>
                      </Grid>
                    ))}
                  </Grid>
                ) : selectedProject ? (
                  <Typography variant="body2" color="text.secondary" align="center">
                    이미지가 없습니다. 이미지를 업로드하세요.
                  </Typography>
                ) : (
                  <Typography variant="body2" color="text.secondary" align="center">
                    좌측에서 프로젝트를 선택하세요.
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>

      {/* 프로젝트 생성 다이얼로그 */}
      <Dialog open={createDialogOpen} onClose={() => setCreateDialogOpen(false)}>
        <DialogTitle>새 프로젝트 생성</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="프로젝트 이름"
            fullWidth
            value={newProjectName}
            onChange={(e) => setNewProjectName(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)}>취소</Button>
          <Button onClick={handleCreateProject} variant="contained">
            생성
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default App;
```

#### 4.3 프론트엔드 메인 진입점 (frontend/src/main.tsx)

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import App from './App.tsx'

// 다크 테마 생성
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </React.StrictMode>,
)
```

### Step 5: 프로토타입 실행 및 테스트

```bash
# 터미널 1: 백엔드 실행
cd backend
source venv/bin/activate
python main.py

# 터미널 2: 프론트엔드 실행
cd frontend
npm run dev

# 브라우저에서 http://localhost:5173 접속
```

**테스트 시나리오:**
1. ✅ 프로젝트 생성
2. ✅ 이미지 업로드
3. ✅ 이미지 목록 표시

---

## 🚀 Phase 1: Electron 통합 (1주)

### Step 1: Electron 설치 및 설정

```bash
# 루트 디렉토리에서
npm init -y

# Electron 설치
npm install --save-dev electron electron-builder concurrently wait-on

# package.json 업데이트
```

#### package.json 수정

```json
{
  "name": "project-agi-desktop",
  "version": "0.1.0",
  "description": "AI-powered image labeling platform",
  "main": "desktop/electron/main.js",
  "scripts": {
    "dev:frontend": "cd frontend && npm run dev",
    "dev:backend": "cd backend && python main.py",
    "dev": "concurrently \"npm run dev:backend\" \"npm run dev:frontend\" \"wait-on http://localhost:5173 && electron .\"",
    "build:frontend": "cd frontend && npm run build",
    "build": "npm run build:frontend && electron-builder",
    "electron": "electron .",
    "postinstall": "electron-builder install-app-deps"
  },
  "build": {
    "appId": "com.yourcompany.project-agi",
    "productName": "PROJECT-AGI",
    "directories": {
      "output": "dist-electron"
    },
    "files": [
      "frontend/dist/**/*",
      "desktop/electron/**/*"
    ],
    "win": {
      "target": "nsis",
      "icon": "shared/assets/icon.ico"
    },
    "linux": {
      "target": "AppImage",
      "icon": "shared/assets/icon.png"
    },
    "mac": {
      "target": "dmg",
      "icon": "shared/assets/icon.icns"
    }
  },
  "devDependencies": {
    "concurrently": "^8.0.0",
    "electron": "^27.0.0",
    "electron-builder": "^24.0.0",
    "wait-on": "^7.0.0"
  }
}
```

### Step 2: Electron Main Process

#### desktop/electron/main.js

```javascript
const { app, BrowserWindow, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

let mainWindow;
let backendProcess;

// 개발 모드 확인
const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;

// Python 실행 파일 경로 찾기
function getPythonPath() {
  if (isDev) {
    // 개발 모드: 시스템 Python
    return process.platform === 'win32' ? 'python' : 'python3';
  } else {
    // 프로덕션: 번들된 Python
    const resourcesPath = process.resourcesPath;
    if (process.platform === 'win32') {
      return path.join(resourcesPath, 'python', 'python.exe');
    } else {
      return path.join(resourcesPath, 'python', 'bin', 'python3');
    }
  }
}

// 백엔드 서버 시작
function startBackend() {
  const pythonPath = getPythonPath();
  const backendScript = isDev
    ? path.join(__dirname, '../../backend/main.py')
    : path.join(process.resourcesPath, 'backend/main.py');

  console.log('Starting backend...');
  console.log('Python path:', pythonPath);
  console.log('Backend script:', backendScript);

  backendProcess = spawn(pythonPath, [backendScript], {
    env: {
      ...process.env,
      PYTHONUNBUFFERED: '1'
    }
  });

  backendProcess.stdout.on('data', (data) => {
    console.log(`[Backend] ${data.toString()}`);
  });

  backendProcess.stderr.on('data', (data) => {
    console.error(`[Backend Error] ${data.toString()}`);
  });

  backendProcess.on('close', (code) => {
    console.log(`Backend process exited with code ${code}`);
  });
}

// 메인 윈도우 생성
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1600,
    height: 1000,
    minWidth: 1200,
    minHeight: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, '../../shared/assets/icon.png'),
    show: false  // 로딩 완료 후 표시
  });

  // 개발 모드
  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    // 프로덕션 모드
    mainWindow.loadFile(path.join(__dirname, '../../frontend/dist/index.html'));
  }

  // 윈도우 준비 완료
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // 윈도우 닫힘
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// 앱 준비 완료
app.whenReady().then(() => {
  // 백엔드 먼저 시작
  startBackend();

  // 백엔드가 준비될 때까지 대기 (2초)
  setTimeout(() => {
    createWindow();
  }, 2000);

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// 모든 윈도우 닫힘
app.on('window-all-closed', () => {
  // 백엔드 프로세스 종료
  if (backendProcess) {
    backendProcess.kill();
  }

  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// 앱 종료 전
app.on('before-quit', () => {
  if (backendProcess) {
    backendProcess.kill();
  }
});

// 예외 처리
process.on('uncaughtException', (error) => {
  console.error('Uncaught exception:', error);
  
  dialog.showErrorBox(
    'Error',
    `An unexpected error occurred: ${error.message}`
  );
});
```

#### desktop/electron/preload.js

```javascript
const { contextBridge, ipcRenderer } = require('electron');

// 프론트엔드에 안전한 API 노출
contextBridge.exposeInMainWorld('electronAPI', {
  // 여기에 필요한 IPC 통신 함수 추가
  platform: process.platform,
  versions: {
    node: process.versions.node,
    chrome: process.versions.chrome,
    electron: process.versions.electron
  }
});
```

### Step 3: Electron에서 실행

```bash
# 개발 모드 실행
npm run dev

# 또는 각각 실행
npm run dev:backend    # 터미널 1
npm run dev:frontend   # 터미널 2
npm run electron       # 터미널 3
```

---

## 📦 Phase 2: 기존 파이프라인 통합 (2주)

### 목표
- Autodistill + SAM2 파이프라인을 API로 통합
- 진행 상황을 WebSocket으로 실시간 업데이트
- 결과 시각화

### Step 1: 백엔드에 기존 코드 통합

#### backend/core/pipeline.py

```python
"""
기존 파이프라인 래퍼
"""

import sys
from pathlib import Path
import logging

# 기존 프로젝트 경로 추가
ORIGINAL_PROJECT_PATH = Path(__file__).parent.parent.parent.parent / "project-agi"
sys.path.insert(0, str(ORIGINAL_PROJECT_PATH))

# 기존 스크립트 임포트
try:
    from scripts.01_data_preparation.main_launcher import run_pipeline
    from scripts.01_data_preparation.autodistill_runner import AutodistillRunner
except ImportError as e:
    logging.error(f"Failed to import original scripts: {e}")
    run_pipeline = None
    AutodistillRunner = None

class PipelineManager:
    """파이프라인 실행 관리자"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.logger = logging.getLogger(__name__)
    
    async def run_autodistill(
        self,
        category: str,
        progress_callback=None
    ):
        """
        Autodistill + SAM2 실행
        
        Args:
            category: 프로젝트 카테고리
            progress_callback: 진행 상황 콜백 함수
        """
        if run_pipeline is None:
            raise RuntimeError("Original pipeline scripts not available")
        
        try:
            # 진행 상황 업데이트
            if progress_callback:
                await progress_callback({
                    "status": "running",
                    "message": "Starting Autodistill...",
                    "progress": 10
                })
            
            # 실제 파이프라인 실행
            result = run_pipeline(
                category=category,
                data_dir=str(self.data_dir),
                plot=False,
                preprocess=True
            )
            
            if progress_callback:
                await progress_callback({
                    "status": "completed",
                    "message": "Pipeline completed successfully",
                    "progress": 100,
                    "result": result
                })
            
            return result
            
        except Exception as e:
            self.logger.error(f"Pipeline error: {e}")
            if progress_callback:
                await progress_callback({
                    "status": "error",
                    "message": str(e),
                    "progress": 0
                })
            raise
```

### Step 2: WebSocket 진행 상황 업데이트

#### backend/main.py에 추가

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict
import asyncio

# WebSocket 연결 관리
active_connections: Dict[str, WebSocket] = {}

@app.websocket("/ws/progress/{task_id}")
async def websocket_progress(websocket: WebSocket, task_id: str):
    """실시간 진행 상황 업데이트"""
    await websocket.accept()
    active_connections[task_id] = websocket
    
    try:
        while True:
            # 클라이언트로부터 메시지 수신 (keep-alive)
            await websocket.receive_text()
    except WebSocketDisconnect:
        del active_connections[task_id]
        logger.info(f"WebSocket disconnected: {task_id}")

async def send_progress(task_id: str, data: dict):
    """특정 태스크의 진행 상황 전송"""
    if task_id in active_connections:
        await active_connections[task_id].send_json(data)

# 파이프라인 실행 API 수정
from backend.core.pipeline import PipelineManager

pipeline_manager = PipelineManager(DATA_DIR)

@app.post("/api/v1/projects/{project_id}/pipeline/autodistill")
async def run_autodistill(project_id: str):
    """Autodistill + SAM2 파이프라인 실행 (실제 통합)"""
    task_id = str(uuid.uuid4())
    
    # 백그라운드 태스크로 실행
    asyncio.create_task(
        pipeline_manager.run_autodistill(
            category=project_id,
            progress_callback=lambda data: send_progress(task_id, data)
        )
    )
    
    return {
        "status": "started",
        "project_id": project_id,
        "task_id": task_id
    }
```

### Step 3: 프론트엔드 WebSocket 연결

#### frontend/src/services/websocket.ts

```typescript
export class ProgressWebSocket {
  private ws: WebSocket | null = null;
  private taskId: string;
  private onProgress: (data: any) => void;

  constructor(taskId: string, onProgress: (data: any) => void) {
    this.taskId = taskId;
    this.onProgress = onProgress;
  }

  connect() {
    this.ws = new WebSocket(`ws://localhost:8000/ws/progress/${this.taskId}`);

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.onProgress(data);
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.ws.onclose = () => {
      console.log('WebSocket closed');
    };

    // Keep-alive
    setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send('ping');
      }
    }, 30000);
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}
```

---

## ✅ 체크리스트

### 프로토타입 완료 기준
- [ ] 프로젝트 생성/조회 가능
- [ ] 이미지 업로드 및 표시 가능
- [ ] Electron 앱으로 실행 가능
- [ ] 백엔드-프론트엔드 통신 정상 작동

### MVP 완료 기준
- [ ] Autodistill + SAM2 파이프라인 통합
- [ ] 실시간 진행 상황 표시
- [ ] 결과 시각화
- [ ] 기본 어노테이션 기능

### V1.0 완료 기준
- [ ] Few-Shot Learning 통합
- [ ] Ground Truth 관리 UI
- [ ] 실험 대시보드
- [ ] 크로스 플랫폼 빌드

---

## 🔧 문제 해결

### 문제: Electron에서 Python 실행 안 됨
**해결**: PyInstaller로 Python을 단일 실행 파일로 패키징

```bash
# backend/build.spec 생성 후
pyinstaller backend/build.spec
```

### 문제: CORS 에러
**해결**: FastAPI CORS 미들웨어 설정 확인

### 문제: 이미지 로딩 느림
**해결**: 썸네일 생성 및 지연 로딩 구현

---

**다음 단계**: 이 가이드를 따라 프로토타입을 완성한 후, 더 상세한 기능 구현으로 진행하세요.

