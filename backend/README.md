# Placement ML API (FastAPI)

Toy example that trains a logistic regression model on two features (`cgpa`, `iq`) to predict a binary placement outcome. Exposes a small HTTP API for training and prediction.

## Requirements

- Python 3.x

## Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
```

CORS is enabled for `http://localhost:3000` by default.

## Endpoints

- `GET /health` → `{ "status": "ok" }`
- `POST /train` → trains a model and returns metrics
  - If no file is uploaded, it will load the first existing file from:
    1. `backend/data/placement-dataset.csv`
    2. `backend/data/placement.csv`
  - CSV is expected to contain columns:
    - features: `cgpa`, `iq`
    - target: one of `placement`, `placed`, `target`, `label`
  - Any auto-generated index columns like `Unnamed:*` are dropped.
  - Response: `{ "message": "Model trained", "metrics": { "test_accuracy": number, "best_params": {...} } }`
  - Optional upload: send a CSV file as `multipart/form-data` with field name `file`.
- `POST /predict` → body `{ "cgpa": number, "iq": number }` → `{ "prediction": 0 | 1 }`

## Model

- Persisted to `backend/models/model.joblib` after successful training.

## Notes

- This is a simple teaching/demo app; the ML pipeline is a basic `StandardScaler` + `LogisticRegression` with a small grid search.
