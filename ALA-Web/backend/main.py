import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add ALA-GUI/src to sys.path to allow importing existing modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
gui_src_path = os.path.join(project_root, "ALA-GUI", "src")
sys.path.append(gui_src_path)

from routers import images, annotate, models, upload, preprocess

app = FastAPI(title="ALA-Web API", version="0.1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(images.router, prefix="/api/images", tags=["images"])
app.include_router(annotate.router, prefix="/api/annotate", tags=["annotate"])
app.include_router(models.router, prefix="/api/models", tags=["models"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(preprocess.router, prefix="/api/preprocess", tags=["preprocess"])

@app.get("/")
async def root():
    return {"message": "ALA-Web API is running"}
