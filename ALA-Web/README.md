# ALA-Web: Auto Label Agent

**AI-powered Image Annotation Tool** leveraging SAM2 and Florence-2 for automated labeling.

---

## 🚀 Quick Start

### Windows
1. **Clone**: `git clone <repository-url>`
2. **Setup**: Double-click `setup.bat` (Install logic & dependencies)
3. **Run**: Double-click `run.bat` (Starts Backend & Frontend)

### Linux/macOS
1. **Clone**: `git clone <repository-url>`
2. **Setup**: `./setup.sh`
3. **Run**: `./run.sh`

> **Note**: The application will automatically open in your browser at http://localhost:5173

---

## 📁 Project Structure

```
ALA-Web/
├── .venv/              # Python virtual environment (CANONICAL)
├── backend/            # FastAPI backend
│   ├── lib/            # Local AI libraries
│   ├── main.py         # Entry point
│   └── requirements.txt
├── frontend/           # React frontend
│   ├── node_modules/   # Frontend dependencies
│   └── package.json
└── scripts/            # Setup utilities
```

**Important**: This project uses **`.venv`** in the root directory as the single Python virtual environment.

---

## 📚 Documentation

- **[Installation Guide](INSTALL.md)**: Detailed installation instructions and manual setup.
- **[User Guide](USER_GUIDE.md)**: How to use the tool for annotation.
- **[Development Guide](docs/development.md)**: For contributors and developers.
- **[Troubleshooting](docs/troubleshooting.md)**: Solutions for common issues.
- **[Architecture](docs/architecture.md)**: System design and component overview.

---

## ✨ Features

- **Auto Annotation**: Automatically label images using text prompts (Grounding DINO + SAM).
- **Smart Segmentation**: Click-to-segment using Segment Anything Model (SAM).
- **Project Management**: Organize datasets into projects.
- **Export**: Export annotations in standard formats (COCO, YOLO).

---

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, PyTorch
- **Frontend**: React, TypeScript, Vite, TailwindCSS
- **AI Models**: SAM2, Florence-2, Grounding DINO

---

## 🤝 Contributing

See [docs/development.md](docs/development.md) for setting up your development environment.

## 📄 License

MIT License
