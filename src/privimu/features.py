"""Windowing and feature extraction for IMU time series."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

EPS = 1e-12


@dataclass(frozen=True)
class WindowConfig:
    """Configuration for fixed-length sliding windows."""

    window_size: int = 50
    step_size: int = 25
    sampling_rate_hz: float = 50.0

    def validate(self) -> None:
        if self.window_size <= 0:
            raise ValueError("window_size must be positive")
        if self.step_size <= 0:
            raise ValueError("step_size must be positive")
        if self.sampling_rate_hz <= 0:
            raise ValueError("sampling_rate_hz must be positive")


def window_signal(signal: np.ndarray, config: WindowConfig) -> np.ndarray:
    """Convert a 2D time series into overlapping windows.

    Parameters
    ----------
    signal:
        Array shaped `(n_samples, n_channels)`.
    config:
        Window length and stride.

    Returns
    -------
    np.ndarray
        Array shaped `(n_windows, window_size, n_channels)`.
    """

    config.validate()
    x = np.asarray(signal, dtype=float)
    if x.ndim != 2:
        raise ValueError("signal must be a 2D array: samples x channels")
    n_samples, n_channels = x.shape
    if n_samples < config.window_size:
        return np.empty((0, config.window_size, n_channels), dtype=float)

    starts = range(0, n_samples - config.window_size + 1, config.step_size)
    windows = [x[start : start + config.window_size] for start in starts]
    return np.stack(windows, axis=0)


def zscore_windows(windows: np.ndarray) -> np.ndarray:
    """Apply z-score normalization per window and per channel."""

    w = np.asarray(windows, dtype=float)
    if w.ndim != 3:
        raise ValueError("windows must be a 3D array: windows x samples x channels")
    mean = w.mean(axis=1, keepdims=True)
    std = w.std(axis=1, keepdims=True)
    std = np.where(std < EPS, 1.0, std)
    return (w - mean) / std


def _rms(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(x))))


def _iqr(x: np.ndarray) -> float:
    q75, q25 = np.percentile(x, [75, 25])
    return float(q75 - q25)


def _skew(x: np.ndarray) -> float:
    centered = x - x.mean()
    std = x.std()
    if std < EPS:
        return 0.0
    return float(np.mean((centered / std) ** 3))


def _kurtosis(x: np.ndarray) -> float:
    centered = x - x.mean()
    std = x.std()
    if std < EPS:
        return 0.0
    return float(np.mean((centered / std) ** 4) - 3.0)


def _spectral_entropy(x: np.ndarray) -> float:
    power = np.abs(np.fft.rfft(x)) ** 2
    total = power.sum()
    if total < EPS:
        return 0.0
    p = power / total
    return float(-np.sum(p * np.log2(p + EPS)))


FEATURE_FUNCTIONS = [
    ("mean", lambda x: float(np.mean(x))),
    ("std", lambda x: float(np.std(x))),
    ("rms", _rms),
    ("min", lambda x: float(np.min(x))),
    ("max", lambda x: float(np.max(x))),
    ("median", lambda x: float(np.median(x))),
    ("iqr", _iqr),
    ("skew", _skew),
    ("kurtosis", _kurtosis),
    ("spectral_entropy", _spectral_entropy),
]


def feature_names(channel_names: list[str]) -> list[str]:
    """Return feature names in the same order as `extract_window_features`."""

    return [f"{channel}__{name}" for channel in channel_names for name, _ in FEATURE_FUNCTIONS]


def extract_window_features(window: np.ndarray) -> np.ndarray:
    """Extract 10 features per channel from one window."""

    w = np.asarray(window, dtype=float)
    if w.ndim != 2:
        raise ValueError("window must be a 2D array: samples x channels")
    values: list[float] = []
    for channel_idx in range(w.shape[1]):
        channel = w[:, channel_idx]
        for _, func in FEATURE_FUNCTIONS:
            value = func(channel)
            if not math.isfinite(value):
                value = 0.0
            values.append(value)
    return np.asarray(values, dtype=float)


def extract_features(windows: np.ndarray) -> np.ndarray:
    """Extract fixed-size features from all windows."""

    w = np.asarray(windows, dtype=float)
    if w.ndim != 3:
        raise ValueError("windows must be a 3D array: windows x samples x channels")
    if w.shape[0] == 0:
        return np.empty((0, w.shape[2] * len(FEATURE_FUNCTIONS)), dtype=float)
    return np.vstack([extract_window_features(window) for window in w])
