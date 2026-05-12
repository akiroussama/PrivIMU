"""Random Forest identity classifier."""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from privimu.config import RANDOM_SEED


def build_random_forest(n_estimators: int = 200, random_state: int = RANDOM_SEED) -> RandomForestClassifier:
    """Build the default RF baseline."""

    return RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
        class_weight="balanced_subsample",
        max_features="sqrt",
    )


def train_random_forest(X: np.ndarray, y: np.ndarray, n_estimators: int = 200) -> RandomForestClassifier:
    """Train a Random Forest classifier."""

    model = build_random_forest(n_estimators=n_estimators)
    model.fit(X, y)
    return model


def save_model(model: RandomForestClassifier, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)


def load_model(path: Path) -> RandomForestClassifier:
    return joblib.load(path)
