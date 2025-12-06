# Development Guide

## 🏗️ Project Structure

```
ALA-Web/
├── backend/                 # FastAPI Application
│   ├── main.py              # Entry point
│   ├── routers/             # API Endpoints
│   ├── services/            # Business Logic
│   └── lib/                 # Local AI Libraries
│
├── frontend/                # React Application
│   ├── src/
│   │   ├── components/      # Reusable UI Components
│   │   ├── pages/           # Page Views
│   │   └── hooks/           # Custom React Hooks
│   └── ...
│
├── scripts/                 # Utility Scripts
└── docs/                    # Documentation
```

---

## 🐍 Backend Development

### Setup
1. Activate virtual environment: `.venv\Scripts\activate`
2. Install dev dependencies: `pip install pytest black flake8`

### Running Dev Server
```bash
cd backend
uvicorn main:app --reload
```
- API Docs: http://localhost:8000/docs

### Adding New Endpoints
1. Create router in `backend/routers/`
2. Register router in `backend/main.py`

---

## ⚛️ Frontend Development

### Setup
1. `cd frontend`
2. `npm install`

### Running Dev Server
```bash
npm run dev
```
- URL: http://localhost:5173

### Component Guidelines
- Use Functional Components with Hooks.
- Use TailwindCSS for styling.
- Place reusable components in `src/components/common`.

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
*Not configured yet*
