from __future__ import annotations
from pathlib import Path
from typing import Optional, Tuple, Dict

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

FEATURE_COLUMNS = ["cgpa", "iq"]
TARGET_CANDIDATES = ["placement", "placed", "target", "label"]
MODEL_FILENAME = "model.joblib"


def _select_target_column(df: pd.DataFrame) -> str:
    for candidate in TARGET_CANDIDATES:
        if candidate in df.columns:
            return candidate
    # fallback: last column
    return df.columns[-1]


def _prepare_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    missing = [col for col in FEATURE_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required feature columns: {missing}")
    target_col = _select_target_column(df)
    X = df[FEATURE_COLUMNS].copy()
    y = df[target_col].astype(int).copy()
    return X, y


def _build_pipeline() -> Pipeline:
    numeric_transformer = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, FEATURE_COLUMNS),
        ],
        remainder="drop",
    )
    clf = LogisticRegression(max_iter=1000)
    pipeline = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("clf", clf),
        ]
    )
    return pipeline


def train_from_dataframe(df: pd.DataFrame, model_dir: Path) -> Dict[str, float]:
    X, y = _prepare_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y if len(np.unique(y)) > 1 else None
    )

    pipeline = _build_pipeline()

    param_grid = {
        "clf__C": [0.1, 1.0, 10.0],
        "clf__solver": ["lbfgs", "liblinear"],
    }

    search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        scoring="accuracy",
        n_jobs=-1,
        cv=5 if len(y_train) >= 5 else 3,
    )
    search.fit(X_train, y_train)

    best_model: Pipeline = search.best_estimator_

    y_pred = best_model.predict(X_test)
    test_accuracy = float(accuracy_score(y_test, y_pred))

    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, model_dir / MODEL_FILENAME)

    return {
        "test_accuracy": test_accuracy,
        "best_params": {k: str(v) for k, v in search.best_params_.items()},
    }


def load_model(model_dir: Path) -> Optional[Pipeline]:
    model_path = model_dir / MODEL_FILENAME
    if not model_path.exists():
        return None
    return joblib.load(model_path)


def predict_with_model(model: Pipeline, cgpa: float, iq: float) -> int:
    input_array = np.array([[cgpa, iq]])
    prediction = model.predict(pd.DataFrame(input_array, columns=FEATURE_COLUMNS))
    return int(prediction[0])
