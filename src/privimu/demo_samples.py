"""Small synthetic signals used when no trained model is available in the demo."""

from __future__ import annotations

import numpy as np

from privimu.config import DEFAULT_CHANNELS


def synthetic_imu_signal(subject_id: int = 7, n_samples: int = 150, noise: float = 0.03) -> np.ndarray:
    """Generate a deterministic IMU-like signal for demo scaffolding.

    This is not used for final metrics. It only keeps the Streamlit interface
    clickable before MotionSense is downloaded and a model is trained.
    """

    rng = np.random.default_rng(subject_id)
    t = np.linspace(0, 3, n_samples)
    base_freq = 1.2 + subject_id * 0.015
    channels = []
    for idx in range(len(DEFAULT_CHANNELS)):
        phase = idx * np.pi / 6
        signal = np.sin(2 * np.pi * base_freq * t + phase)
        signal += 0.35 * np.sin(2 * np.pi * (base_freq * 2.1) * t + phase / 2)
        signal += rng.normal(0, noise, size=n_samples)
        channels.append(signal)
    return np.column_stack(channels)


def synthetic_probability(subject_id: int, sigma: float, n_subjects: int = 24) -> np.ndarray:
    """Synthetic posterior distribution for UI-only fallback mode."""

    rng = np.random.default_rng(subject_id)
    logits = rng.normal(0, 0.4, size=n_subjects)
    logits[subject_id - 1] += max(0.2, 4.0 - sigma * 8.0)
    exp = np.exp(logits - logits.max())
    return exp / exp.sum()
