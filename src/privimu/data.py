"""MotionSense loading utilities."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from privimu.config import ACTIVITY_LABELS, DEFAULT_CHANNELS
from privimu.features import WindowConfig, extract_features, window_signal, zscore_windows

MOTION_FILE_RE = re.compile(
    r"(?P<activity>dws|ups|wlk|jog|sit|std)_(?P<trial>\d+).*[\\/]sub_(?P<subject>\d+)\.csv$"
)


@dataclass(frozen=True)
class MotionFile:
    """Metadata for one MotionSense CSV file."""

    path: Path
    activity: str
    trial: int
    subject: int

    @property
    def activity_name(self) -> str:
        return ACTIVITY_LABELS.get(self.activity, self.activity)

    @property
    def activity_trial_group(self) -> str:
        return f"{self.activity}_{self.trial:02d}"

    @property
    def trial_instance_group(self) -> str:
        return f"sub{self.subject:02d}_{self.activity}_{self.trial:02d}"


def parse_motion_file(path: Path) -> MotionFile:
    """Parse activity, trial, and subject from a MotionSense CSV path."""

    p = Path(path)
    match = MOTION_FILE_RE.search(str(p))
    if not match:
        raise ValueError(f"Cannot parse MotionSense metadata from path: {p}")
    return MotionFile(
        path=p,
        activity=match.group("activity"),
        trial=int(match.group("trial")),
        subject=int(match.group("subject")),
    )


def _has_subject_csv_files(path: Path) -> bool:
    """Return True when a directory contains MotionSense subject CSV files."""

    return any(path.rglob("sub_*.csv"))


def resolve_device_motion_root(data_root: Path) -> Path:
    """Find MotionSense DeviceMotion CSVs from common extraction layouts.

    The official ``A_DeviceMotion_data.zip`` may extract either as an
    ``A_DeviceMotion_data`` folder or directly as activity folders. The older
    downloader also extracted the whole GitHub repo, where the dataset archive
    is nested under ``motion-sense-master/data``. This resolver accepts all
    layouts that contain ``sub_*.csv`` files.
    """

    root = Path(data_root)
    candidates = [
        root / "A_DeviceMotion_data",
        root / "data" / "A_DeviceMotion_data",
        root / "motion-sense-master" / "data" / "A_DeviceMotion_data",
        root / "motion-sense-main" / "data" / "A_DeviceMotion_data",
    ]
    for candidate in candidates:
        if candidate.is_dir() and _has_subject_csv_files(candidate):
            return candidate

    for candidate in root.rglob("A_DeviceMotion_data"):
        if candidate.is_dir() and _has_subject_csv_files(candidate):
            return candidate

    if root.is_dir() and _has_subject_csv_files(root):
        return root

    nested_zip = next(root.rglob("A_DeviceMotion_data.zip"), None) if root.exists() else None
    hint = f" Found nested archive {nested_zip}; extract it first." if nested_zip else ""
    raise FileNotFoundError(
        f"Could not find MotionSense CSV files under {root}.{hint} Run data/download.py --force first."
    )


def iter_motion_files(data_root: Path, activities: Iterable[str] | None = None) -> list[MotionFile]:
    """List MotionSense CSV files with parsed metadata."""

    device_root = resolve_device_motion_root(data_root)
    allowed = set(activities) if activities else set(ACTIVITY_LABELS)
    files: list[MotionFile] = []
    for csv_path in sorted(device_root.rglob("sub_*.csv")):
        try:
            item = parse_motion_file(csv_path)
        except ValueError:
            continue
        if item.activity in allowed:
            files.append(item)
    if not files:
        raise FileNotFoundError(f"No MotionSense CSV files found in {device_root}")
    return files


def load_motion_csv(path: Path, channels: list[str] | None = None) -> np.ndarray:
    """Load selected sensor channels from a MotionSense CSV file."""

    selected = channels or DEFAULT_CHANNELS
    df = pd.read_csv(path)
    unnamed_cols = [col for col in df.columns if col.startswith("Unnamed")]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)
    missing = [col for col in selected if col not in df.columns]
    if missing:
        raise ValueError(f"Missing expected channels in {path}: {missing}")
    return df[selected].to_numpy(dtype=float)


def build_feature_dataset(
    data_root: Path,
    config: WindowConfig,
    channels: list[str] | None = None,
    activities: Iterable[str] | None = None,
    max_files: int | None = None,
) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    """Build a tabular feature dataset for identity classification.

    Returns
    -------
    X:
        Feature matrix shaped `(n_windows, n_features)`.
    y:
        Subject IDs in the range 1..24.
    meta:
        One metadata row per window.
    """

    selected = channels or DEFAULT_CHANNELS
    motion_files = iter_motion_files(data_root, activities=activities)
    if max_files is not None:
        motion_files = motion_files[:max_files]

    X_parts: list[np.ndarray] = []
    y_parts: list[np.ndarray] = []
    meta_rows: list[dict[str, object]] = []

    for item in motion_files:
        signal = load_motion_csv(item.path, channels=selected)
        windows = zscore_windows(window_signal(signal, config))
        if windows.shape[0] == 0:
            continue
        features = extract_features(windows)
        X_parts.append(features)
        y_parts.append(np.full(windows.shape[0], item.subject, dtype=int))
        for window_idx in range(windows.shape[0]):
            meta_rows.append(
                {
                    "path": str(item.path),
                    "subject": item.subject,
                    "activity": item.activity,
                    "activity_name": item.activity_name,
                    "trial": item.trial,
                    "window_idx": window_idx,
                    "activity_trial": item.activity_trial_group,
                    "trial_instance": item.trial_instance_group,
                }
            )

    if not X_parts:
        raise ValueError("No windows were generated. Check window_size and input files.")

    X = np.vstack(X_parts)
    y = np.concatenate(y_parts)
    meta = pd.DataFrame(meta_rows)
    return X, y, meta


def build_raw_window_dataset(
    data_root: Path,
    config: WindowConfig,
    channels: list[str] | None = None,
    activities: Iterable[str] | None = None,
    max_files: int | None = None,
) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    """Build raw normalized windows for the 1D-CNN pipeline."""

    selected = channels or DEFAULT_CHANNELS
    motion_files = iter_motion_files(data_root, activities=activities)
    if max_files is not None:
        motion_files = motion_files[:max_files]

    X_parts: list[np.ndarray] = []
    y_parts: list[np.ndarray] = []
    meta_rows: list[dict[str, object]] = []

    for item in motion_files:
        signal = load_motion_csv(item.path, channels=selected)
        windows = zscore_windows(window_signal(signal, config))
        if windows.shape[0] == 0:
            continue
        X_parts.append(windows)
        y_parts.append(np.full(windows.shape[0], item.subject, dtype=int))
        for window_idx in range(windows.shape[0]):
            meta_rows.append(
                {
                    "path": str(item.path),
                    "subject": item.subject,
                    "activity": item.activity,
                    "activity_name": item.activity_name,
                    "trial": item.trial,
                    "window_idx": window_idx,
                    "activity_trial": item.activity_trial_group,
                    "trial_instance": item.trial_instance_group,
                }
            )

    if not X_parts:
        raise ValueError("No windows were generated. Check window_size and input files.")

    X = np.concatenate(X_parts, axis=0)
    y = np.concatenate(y_parts)
    meta = pd.DataFrame(meta_rows)
    return X, y, meta
