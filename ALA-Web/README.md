# ALA-Web - Modern Web Annotation Platform

**AI-Powered Image Annotation with React + FastAPI**

A modern web application for AI-powered image annotation, built with React and FastAPI. Features drag-and-drop uploads, structured caption ontology, and complete preprocessing pipeline.

---

## ✨ Features

### 🎯 Core Capabilities
- **Upload & Management**: Drag-and-drop interface for images and videos
- **Caption Ontology**: Structured class definitions with key-value format
- **AI Annotation**: Florence-2 VLM + SAM2 segmentation
- **Preprocessing Pipeline**: Crop, mask extraction, background removal, resizing
- **Modern UI**: Responsive React interface with TailwindCSS

### 🔧 Preprocessing Options
- **Output Sizes**: 640×480 (default), 224×224, or custom
- **Background Modes**: Black, White, Gray, Transparent, Blur, Mean color
- **Box Padding**: Adjustable 0-50 pixels
- **Batch Processing**: Process multiple images at once

---

## 🚀 Quick Start

### Prerequisites
- **Node.js**: 16+ (for frontend)
- **Python**: 3.10+ (for backend)
- **npm** or **yarn**

### Installation

#### 1. Backend Setup
```bash
cd ALA-Web/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload
```

Backend runs on: **http://localhost:8000**  
API docs: **http://localhost:8000/docs**

#### 2. Frontend Setup
```bash
cd ALA-Web/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs on: **http://localhost:5173**

---

## 📖 Usage Guide

### 1. Upload Assets
- Navigate to the **Annotate** page
- Drag and drop images/videos or click to browse
- Supported formats: JPG, PNG, WebP (images), MP4, AVI, MOV, MKV (videos)

### 2. Define Caption Ontology
- Click **Edit** next to "Caption Ontology"
- Add classes with descriptions:
  - Class: `cat`
  - Description: `a small feline animal`
- Import/export ontology as JSON

### 3. Run Annotation
- Select VLM model (Florence-2)
- Select segmentation model (SAM2)
- Click **Run Annotation**
- Review generated boxes and masks

### 4. Preprocess Results
- Navigate to **Preprocessing** page
- Configure options:
  - Output size (e.g., 640×480)
  - Background mode (e.g., transparent)
  - Box padding
- Click **Batch Process**

---

## 🏗️ Architecture

### Backend (FastAPI)
```
backend/
├── main.py              # FastAPI app entry point
├── routers/            # API endpoints
│   ├── upload.py       # File upload/delete/list
│   ├── images.py       # Image serving
│   ├── annotate.py     # Florence-2/SAM2 (mock)
│   ├── models.py       # Model status
│   └── preprocess.py   # Preprocessing pipeline
└── services/           # Business logic
    └── preprocessor.py # Image preprocessing
```

**API Endpoints** (13 total):
- Upload: `POST /api/upload/file`, `GET /api/upload/list`, `DELETE /api/upload/{id}`
- Images: `GET /api/images/`, `GET /api/images/file/{name}`
- Annotate: `POST /api/annotate/detect`, `POST /api/annotate/segment`
- Preprocess: `POST /api/preprocess/single`, `POST /api/preprocess/batch`
- Models: `GET /api/models/status`

### Frontend (React)
```
frontend/
├── src/
│   ├── components/         # Reusable UI components
│   │   ├── AssetGrid.tsx   # Upload grid with thumbnails
│   │   ├── OntologyEditor.tsx # Caption ontology modal
│   │   ├── AnnotationSidebar.tsx # Model selection  
│   │   └── Layout.tsx      # Main layout with sidebar
│   ├── pages/              # Page components
│   │   ├── Gallery.tsx     # Image gallery view
│   │   ├── Preprocessing.tsx # Preprocessing UI
│   │   └── Settings.tsx    # Settings page
│   └── hooks/              # Custom React hooks
│       ├── useUploads.ts   # Upload operations
│       └── useImages.ts    # Image fetching
└── package.json
```

---

## 🔌 API Documentation

Visit **http://localhost:8000/docs** (when backend is running) to see interactive Swagger UI documentation for all endpoints.

### Example: Upload File
```bash
curl -X POST "http://localhost:8000/api/upload/file" \
  -F "file=@image.jpg"
```

### Example: Preprocess Image
```bash
curl -X POST "http://localhost:8000/api/preprocess/single" \
  -H "Content-Type: application/json" \
  -d '{
    "image_data": "data:image/png;base64,...",
    "box": [100, 100, 400, 400],
    "bg_mode": "transparent",
    "target_size": [640, 480]
  }'
```

---

## 🧪 Development

### Run Tests
```bash
# Backend tests (if available)
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Build for Production
```bash
# Frontend build
cd frontend
npm run build

# Serve static build
npm run preview
```

---

## 📊 Technology Stack

| Layer | Technology | Purpose |
|:---|:---|:---|
| **Frontend** | React 18.2 | UI framework |
| | TypeScript | Type safety |
| | TailwindCSS 3.4 | Styling |
| | Axios | HTTP client |
| | Lucide React | Icons |
| **Backend** | FastAPI | Web framework |
| | Uvicorn | ASGI server |
| | Pydantic | Data validation |
| | OpenCV | Image processing |
| | Pillow | Image handling |
| **AI Models** | Florence-2 | Object detection |
| | SAM2 | Segmentation |

---

## 🗺️ Roadmap

### ✅ Completed
- Upload & asset management
- Caption ontology editor
- Preprocessing pipeline UI
- Backend API (13 endpoints)

### 🚧 In Progress
- Classification workflow
- Data flow tracking

### 📋 Planned
- Real-time collaboration
- User authentication
- Cloud deployment
- Mobile responsiveness

---

## 🐛 Known Issues

- Preprocessing backend requires `opencv-python` to be installed
- Classification and data tracking UIs are placeholders
- Annotation endpoints are currently mocked

---

## 📝 License

MIT License - see [LICENSE](../LICENSE) file for details.

---

## 🔗 Related

- **Desktop App**: [ALA-GUI](../ALA-GUI/)
- **Main Project**: [ALA-AutoLabelAgent](../)

---

**Version**: 0.1.0-beta  
**Last Updated**: 2025-01-19
