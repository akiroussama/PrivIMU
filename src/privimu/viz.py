"""Visualization helpers for generated reports."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, f1_score

from privimu.metrics import entropy_bits, privacy_entropy_leakage


def plot_confusion_matrix(y_true, y_pred, classes, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cm = confusion_matrix(y_true, y_pred, labels=classes)
    fig, ax = plt.subplots(figsize=(9, 8))
    image = ax.imshow(cm)
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title("PrivIMU confusion matrix")
    ax.set_xlabel("Predicted subject")
    ax.set_ylabel("True subject")
    ax.set_xticks(range(len(classes)))
    ax.set_yticks(range(len(classes)))
    ax.set_xticklabels(classes, rotation=90, fontsize=6)
    ax.set_yticklabels(classes, fontsize=6)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_per_subject_f1(y_true, y_pred, classes, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    scores = f1_score(y_true, y_pred, labels=classes, average=None, zero_division=0)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar([str(cls) for cls in classes], scores)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Subject ID")
    ax.set_ylabel("F1 score")
    ax.set_title("Per-subject F1")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_privacy_entropy_curve(proba, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ent = entropy_bits(proba)
    leak = privacy_entropy_leakage(proba)
    order = np.argsort(leak)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(leak[order], label="ΔH leakage bits")
    ax.plot(ent[order], label="Posterior entropy bits")
    ax.set_xlabel("Windows sorted by leakage")
    ax.set_ylabel("Bits")
    ax.set_title("Privacy entropy profile")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
