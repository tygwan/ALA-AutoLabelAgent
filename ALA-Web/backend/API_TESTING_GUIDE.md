# Backend API Testing Guide

## Setup

1. **Install Dependencies**
```bash
cd ALA-Web/backend
pip install fastapi uvicorn pydantic
```

2. **Start Server**
```bash
uvicorn main:app --reload --port 8000
```

3. **Access API Documentation**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints Summary

### Classification Router (`/api/classification`)

#### Experiment Management
- **POST** `/experiment/create` - Create new experiment
- **GET** `/experiment/list` - List all experiments (with filters)
- **GET** `/experiment/{exp_id}` - Get experiment details
- **POST** `/experiment/{exp_id}/run` - Execute classification
- **GET** `/experiment/compare?exp_ids=exp1,exp2` - Compare experiments
- **DELETE** `/experiment/{exp_id}` - Delete experiment

#### Support Set Management  
- **POST** `/support-set/create` - Create support set version
- **GET** `/support-set/list` - List all support sets
- **GET** `/support-set/{support_set_id}` - Get support set details
- **POST** `/support-set/{support_set_id}/clone` - Clone support set
- **POST** `/support-set/annotate` - Annotate support images

#### Query Set Management
- **POST** `/query-set/create` - Create query set
- **GET** `/query-set/list` - List all query sets
- **GET** `/query-set/{query_set_id}` - Get query set details

#### Results & Export
- **GET** `/results/{exp_id}` - Get classification results (sorted/paginated)
- **POST** `/results/{exp_id}/export` - Export results

### Tracking Router (`/api/tracking`)

- **GET** `/status` - Get overall pipeline status
- **GET** `/image/{image_id}` - Get image history
- **POST** `/update` - Update image tracking
- **GET** `/errors` - Get images with errors
- **POST** `/retry/{image_id}` - Retry failed image

## Example Usage

### 1. Create Support Set

```bash
curl -X POST "http://localhost:8000/api/classification/support-set/create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cat-Dog Baseline",
    "classes": {
      "class_0": ["img001", "img002"],
      "class_1": ["img003"]
    }
  }'
```

**Response:**
```json
{
  "support_set_id": "support_v1",
  "version": "support_v1",
  "total_images": 3
}
```

### 2. Create Query Set

```bash
curl -X POST "http://localhost:8000/api/classification/query-set/create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Batch 1",
    "image_ids": ["test001", "test002", "test003"]
  }'
```

**Response:**
```json
{
  "query_set_id": "query_a1b2c3d4",
  "total_images": 3
}
```

### 3. Create Experiment

```bash
curl -X POST "http://localhost:8000/api/classification/experiment/create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cat vs Dog Baseline",
    "support_set_id": "support_v1",
    "query_set_id": "query_a1b2c3d4",
    "method": "cosine_similarity",
    "threshold": 0.7
  }'
```

**Response:**
```json
{
  "experiment_id": "exp_12345678",
  "status": "created",
  "message": "Experiment exp_12345678 created successfully"
}
```

### 4. List Experiments

```bash
curl -X GET "http://localhost:8000/api/classification/experiment/list"
```

**Response:**
```json
{
  "experiments": [
    {
      "experiment_id": "exp_12345678",
      "name": "Cat vs Dog Baseline",
      "support_set_id": "support_v1",
      "query_set_id": "query_a1b2c3d4",
      "status": "created",
      "created_at": "2025-11-22T08:10:00"
    }
  ],
  "total": 1
}
```

### 5. Clone Support Set

```bash
curl -X POST "http://localhost:8000/api/classification/support-set/support_v1/clone"
```

**Response:**
```json
{
  "new_support_set_id": "support_v2",
  "message": "Cloned support_v1 to support_v2"
}
```

### 6. Create Revision Experiment

```bash
curl -X POST "http://localhost:8000/api/classification/experiment/create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cat vs Dog - Improved Support",
    "support_set_id": "support_v2",
    "query_set_id": "query_a1b2c3d4",
    "method": "cosine_similarity",
    "parent_experiment": "exp_12345678"
  }'
```

### 7. Compare Experiments

```bash
curl -X GET "http://localhost:8000/api/classification/experiment/compare?exp_ids=exp_12345678,exp_87654321"
```

### 8. Update Tracking

```bash
curl -X POST "http://localhost:8000/api/tracking/update" \
  -H "Content-Type: application/json" \
  -d '{
    "image_id": "test001",
    "stage": "uploaded",
    "status": "complete"
  }'
```

### 9. Get Pipeline Status

```bash
curl -X GET "http://localhost:8000/api/tracking/status"
```

**Response:**
```json
{
  "stages": {
    "uploaded": 10,
    "annotated": 8,
    "preprocessed": 5,
    "classified": 0
  },
  "total_images": 10
}
```

## Data Files Created

After using the API, the following JSON files will be created in `data/`:

- `experiments.json` - Experiment metadata
- `support_sets.json` - Support set versions
- `query_sets.json` - Query set definitions
- `experiment_results.json` - Classification results per experiment
- `annotations.json` - Annotation data (boxes, masks)
- `tracking.json` - Pipeline tracking data

## Next Steps

**Phase 2-3** (To be implemented):
- Annotation service integration (Florence-2 + SAM2)
- Classification algorithm (cosine similarity)
- Experiment execution engine
- Result statistics calculation

**Phase 4-6** (Frontend):
- Classification page with 3 tabs (Experiments, Support Sets, Comparison)
- Data Tracking dashboard
- UI integration with backend APIs

## Notes

- All endpoints return JSON responses
- IDs are auto-generated (UUID-based)
- JSON files are used for storage (can migrate to DB later)
- Error handling included for invalid IDs and missing data
