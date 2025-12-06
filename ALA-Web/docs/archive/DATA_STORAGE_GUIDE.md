# ALA-Web Data Storage Guide

## 📁 Current Data Folder Structure

```
ALA-Web/
└── backend/
    └── data/
        ├── uploads/              # User uploaded images/videos
        │   ├── abc123.jpg        # Uploaded images (UUID named)
        │   ├── def456.mp4        # Uploaded videos
        │   └── ...
        │
        ├── experiments.json      # Experiment definitions
        ├── support_sets.json     # Support set metadata
        ├── query_sets.json       # Query set metadata
        ├── tracking.json         # Pipeline tracking data
        ├── experiment_results.json  # Classification results
        └── annotations.json      # Annotation data (masks, boxes)
```

---

## 🎯 User Data Storage Location

### **Primary Data Folder**: 
```
backend/data/uploads/
```

**Absolute Path** (on your system):
```
C:\Users\user\Desktop\ALA-AutoLabelAgent\ALA-AutoLabelAgent\ALA-Web\backend\data\uploads\
```

### What Gets Stored Here:
- ✅ All user uploaded images (.jpg, .png, .bmp, .webp)
- ✅ All user uploaded videos (.mp4, .avi, .mov, .mkv)
- ✅ Files are renamed with UUID (e.g., `a1b2c3d4.jpg`)

---

## 🔧 How It Works

### 1. File Upload Process

```
User uploads "cat.jpg"
    ↓
Backend generates UUID: "a1b2c3d4-e5f6-..."
    ↓
File saved as: data/uploads/a1b2c3d4.jpg
    ↓
Metadata stored in tracking.json
```

### 2. Code Implementation

**File**: `backend/routers/upload.py` (Line 13)

```python
UPLOAD_DIR = Path("data/uploads")  # Relative to backend/
```

**Auto-creation**: Folder is created automatically on first upload.

---

## 📝 Recommended Folder Organization (Optional)

### Option 1: Keep Default (Simple)
```
data/uploads/          # All files together
```
✅ Simple  
✅ Works out of the box  
❌ Can get messy with many files

### Option 2: Organize by Date (Advanced)

Modify `upload.py`:
```python
from datetime import datetime

# Change UPLOAD_DIR dynamically
date_folder = datetime.now().strftime("%Y-%m-%d")
UPLOAD_DIR = Path(f"data/uploads/{date_folder}")
```

Result:
```
data/uploads/
├── 2025-11-23/
│   ├── abc123.jpg
│   └── def456.jpg
├── 2025-11-24/
│   └── ghi789.jpg
```

### Option 3: Organize by Type

```python
# In upload.py, organize by file type
if file_type == "image":
    UPLOAD_DIR = Path("data/uploads/images")
else:
    UPLOAD_DIR = Path("data/uploads/videos")
```

Result:
```
data/uploads/
├── images/
│   ├── abc123.jpg
│   └── def456.png
└── videos/
    ├── ghi789.mp4
    └── jkl012.avi
```

---

## 💾 Storage Considerations

### Disk Space Requirements

**Typical Usage**:
- 100 images (~200KB each) = ~20MB
- 10 videos (~50MB each) = ~500MB
- Models (Florence-2 + SAM2) = ~5GB

**Recommendation**: Reserve at least **10GB** for active use.

### Cleanup

**Manual Cleanup**:
```cmd
# Delete all uploaded files
cd backend
rmdir /S data\uploads
mkdir data\uploads
```

**Programmatic Cleanup** (Add to backend):
```python
@router.delete("/cleanup/old")
async def cleanup_old_files(days: int = 30):
    """Delete files older than X days"""
    cutoff = datetime.now() - timedelta(days=days)
    deleted = 0
    
    for file_path in UPLOAD_DIR.iterdir():
        if file_path.stat().st_mtime < cutoff.timestamp():
            file_path.unlink()
            deleted += 1
    
    return {"deleted": deleted}
```

---

## 🗄️ Metadata Storage

### JSON Files (Lightweight)

**Current Approach** (Phase 1-7):
- `data/*.json` files
- Simple, human-readable
- Good for <10,000 files

**Limitations**:
- No indexing
- Slower with large datasets
- No concurrent write safety

### Future: Database Migration

**For Production** (Phase 8+):
```
Replace JSON with PostgreSQL/SQLite
├── Tables: files, annotations, experiments
├── Indexed queries
└── Transaction safety
```

---

## 🔐 Security Considerations

### Current (Development):
- ❌ No file size limits
- ❌ No virus scanning
- ❌ Public file access (anyone with file_id)

### Production Recommendations:
```python
# Add to upload.py
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# Add to upload endpoint
if file.size > MAX_FILE_SIZE:
    raise HTTPException(413, "File too large")
```

---

## 📊 Monitoring Storage

### Check Disk Usage

**Windows**:
```cmd
cd backend\data\uploads
dir /s
```

**Python Script** (`check_storage.py`):
```python
from pathlib import Path

upload_dir = Path("data/uploads")
total_size = sum(f.stat().st_size for f in upload_dir.rglob("*") if f.is_file())

print(f"Total uploads: {total_size / (1024**3):.2f} GB")
print(f"File count: {len(list(upload_dir.rglob('*')))}")
```

---

## ✅ Summary

| Aspect | Value |
|--------|-------|
| **Default Location** | `backend/data/uploads/` |
| **Absolute Path** | `C:\...\ALA-Web\backend\data\uploads\` |
| **Naming** | UUID-based (e.g., `a1b2c3d4.jpg`) |
| **Organization** | Flat (all files together) |
| **Auto-creation** | Yes (on first upload) |
| **Backup** | Manual (copy `data/` folder) |

---

## 🔄 Changing Data Location

If you want to use a different folder (e.g., external drive):

**Step 1**: Edit `backend/routers/upload.py`

```python
# Change line 13 to absolute path
UPLOAD_DIR = Path("D:/MyData/ALA-Uploads")  # Example
```

**Step 2**: Restart backend

```cmd
# Backend will use new location
```

**Step 3**: Update permissions (if needed)

Ensure the Python process has write access to the new folder.

---

**Default location works for most users!** Only change if you have specific needs (external storage, NAS, etc.).
