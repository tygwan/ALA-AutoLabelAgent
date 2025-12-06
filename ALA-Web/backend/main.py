import sys
import os

# Add local lib directory to sys.path
# This allows importing packages from the local 'lib' folder
# mirroring the structure of project-agi
lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
cache_path = os.path.join(lib_path, 'cache')

# Set cache directories to ensure models are downloaded locally
os.environ['XDG_CACHE_HOME'] = cache_path
os.environ['TORCH_HOME'] = cache_path
os.environ['HF_HOME'] = os.path.join(cache_path, 'huggingface')

if os.path.exists(lib_path) and lib_path not in sys.path:
    sys.path.insert(0, lib_path)
    print(f"Added local lib path: {lib_path}")
    print(f"Set cache path: {cache_path}")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import classification, tracking, upload, annotate, projects, ontology
import uvicorn

app = FastAPI(title="ALA AutoLabelAgent API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploaded images
# Ensure the directory exists
os.makedirs("data/uploads", exist_ok=True)
app.mount("/data/uploads", StaticFiles(directory="data/uploads"), name="uploads")

# Include routers
app.include_router(classification.router, prefix="/api/classification", tags=["classification"])
app.include_router(tracking.router, prefix="/api/tracking", tags=["tracking"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(annotate.router, prefix="/api/annotate", tags=["annotate"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(ontology.router, prefix="/api/ontology", tags=["ontology"])

@app.get("/")
async def root():
    return {"message": "ALA AutoLabelAgent API is running (v2)"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
