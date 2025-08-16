from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from .ml.model_service import train_from_dataframe, load_model, predict_with_model

BASE_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

class PredictRequest(BaseModel):
    cgpa: float
    iq: float

app = FastAPI(title="Placement ML API", version="1.0.0")

# CORS for local Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/train")
async def train(file: UploadFile | None = File(default=None)) -> dict:
    try:
        if file is not None:
            if not file.filename.lower().endswith(".csv"):
                raise HTTPException(status_code=400, detail="Please upload a CSV file.")
            content = await file.read()
            df = pd.read_csv(pd.io.common.BytesIO(content))
        else:
            default_candidates = [
                DATA_DIR / "placement-dataset.csv",
                DATA_DIR / "placement.csv",
            ]
            default_csv = next((p for p in default_candidates if p.exists()), None)
            if default_csv is None:
                raise HTTPException(status_code=400, detail="No file uploaded and no default dataset found in data/.")
            df = pd.read_csv(default_csv)
        # drop auto-generated index columns if present
        df = df.loc[:, ~df.columns.str.contains(r"^Unnamed")]
        metrics = train_from_dataframe(df, model_dir=MODELS_DIR)
        return {"message": "Model trained", "metrics": metrics}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/predict")
def predict(payload: PredictRequest) -> dict:
    model = load_model(model_dir=MODELS_DIR)
    if model is None:
        raise HTTPException(status_code=503, detail="Model not trained yet. Call /train first.")
    prediction = predict_with_model(model, cgpa=payload.cgpa, iq=payload.iq)
    return {"prediction": int(prediction)}
