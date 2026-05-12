"""Evaluation metrics for PrivIMU."""

from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
from sklearn.metrics import accuracy_score, f1_score

EPS = 1e-12


@dataclass(frozen=True)
class ClassificationSummary:
    top1_accuracy: float
    top3_accuracy: float
    f1_macro: float
    privacy_entropy_leakage_bits_mean: float
    posterior_entropy_bits_mean: float


def align_probabilities(
    observed_proba: np.ndarray,
    observed_classes: np.ndarray,
    all_classes: np.ndarray,
) -> np.ndarray:
    """Align class-probability columns to a fixed class order."""

    aligned = np.zeros((observed_proba.shape[0], len(all_classes)), dtype=float)
    class_to_col = {int(cls): idx for idx, cls in enumerate(all_classes)}
    for local_idx, cls in enumerate(observed_classes):
        global_idx = class_to_col[int(cls)]
        aligned[:, global_idx] = observed_proba[:, local_idx]
    row_sums = aligned.sum(axis=1, keepdims=True)
    row_sums = np.where(row_sums < EPS, 1.0, row_sums)
    return aligned / row_sums


def top_k_accuracy(y_true: np.ndarray, proba: np.ndarray, classes: np.ndarray, k: int) -> float:
    """Compute top-k accuracy for arbitrary class labels."""

    y = np.asarray(y_true)
    p = np.asarray(proba, dtype=float)
    class_order = np.asarray(classes)
    if p.ndim != 2:
        raise ValueError("proba must be 2D")
    if len(class_order) != p.shape[1]:
        raise ValueError("classes length must match proba columns")
    k = min(k, p.shape[1])
    top_indices = np.argsort(p, axis=1)[:, -k:]
    top_labels = class_order[top_indices]
    return float(np.mean([label in row for label, row in zip(y, top_labels, strict=True)]))


def entropy_bits(proba: np.ndarray) -> np.ndarray:
    """Shannon entropy in bits for each posterior distribution."""

    p = np.asarray(proba, dtype=float)
    p = np.clip(p, EPS, 1.0)
    p = p / p.sum(axis=1, keepdims=True)
    return -np.sum(p * np.log2(p), axis=1)


def privacy_entropy_leakage(proba: np.ndarray) -> np.ndarray:
    """Return ΔH = log2(N) − H(posterior), in bits, per sample."""

    p = np.asarray(proba, dtype=float)
    prior_entropy = np.log2(p.shape[1])
    return prior_entropy - entropy_bits(p)


def summarize_classification(
    y_true: np.ndarray,
    proba: np.ndarray,
    classes: np.ndarray,
) -> ClassificationSummary:
    """Summarize identity-classification performance."""

    y_pred = classes[np.argmax(proba, axis=1)]
    posterior_entropy = entropy_bits(proba)
    leakage = privacy_entropy_leakage(proba)
    return ClassificationSummary(
        top1_accuracy=float(accuracy_score(y_true, y_pred)),
        top3_accuracy=top_k_accuracy(y_true, proba, classes, k=3),
        f1_macro=float(f1_score(y_true, y_pred, labels=classes, average="macro", zero_division=0)),
        privacy_entropy_leakage_bits_mean=float(np.mean(leakage)),
        posterior_entropy_bits_mean=float(np.mean(posterior_entropy)),
    )


def estimate_latency_ms(predict_fn, X: np.ndarray, repeats: int = 200) -> float:
    """Estimate inference latency per sample in milliseconds."""

    if X.shape[0] == 0:
        return 0.0
    sample = X[:1]
    for _ in range(5):
        predict_fn(sample)
    start = time.perf_counter()
    for _ in range(repeats):
        predict_fn(sample)
    elapsed = time.perf_counter() - start
    return float((elapsed / repeats) * 1000.0)
