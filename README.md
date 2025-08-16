# Placement Toy App

A small example ML app consisting of:

- FastAPI backend that trains a logistic regression model on `cgpa` and `iq` to predict placement (0/1)
- Next.js App Router (TypeScript) frontend with a minimal UI to trigger training and request predictions

This is a toy example for learning purposes, not a production ML system.

## Project structure

```
fullml1stproject/
  backend/        # FastAPI API + simple sklearn pipeline
  frontend/       # Next.js App Router UI
  project1(toy_example) (1).ipynb  # original notebook (reference only)
```

## Quickstart

### 1) Backend (API)

Requirements: Python 3.x

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Endpoints:

- `GET /health` → `{ "status": "ok" }`
- `POST /train` → trains a model and returns metrics
  - Defaults to the first existing CSV among:
    - `backend/data/placement-dataset.csv`
    - `backend/data/placement.csv`
  - Expected columns: features `cgpa`, `iq`; target in one of `placement`, `placed`, `target`, `label`
  - Auto-generated index columns like `Unnamed:*` are dropped
- `POST /predict` → body `{ "cgpa": number, "iq": number }` → `{ "prediction": 0 | 1 }`

Trained model is saved to `backend/models/model.joblib`.

### 2) Frontend (UI)

Requirements: Node.js and npm

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

Configuration: the UI uses `NEXT_PUBLIC_API_BASE` (default `http://localhost:8000`).

UI notes:

- Headings use the Bricolage Grotesque font; body text uses Geist
- Simple form for `cgpa` and `iq`, a Train button, and a metrics display panel

## Notes

- The ML pipeline is a simple `StandardScaler` + `LogisticRegression` with a small grid search; suitable for demonstration only
- No license included; this is a minimal educational example
