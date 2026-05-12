"""Train and evaluate PrivIMU models."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from sklearn.model_selection import GroupKFold, GroupShuffleSplit

from privimu.config import DEFAULT_CHANNELS, SUBJECT_IDS
from privimu.data import build_feature_dataset, build_raw_window_dataset
from privimu.features import WindowConfig, feature_names
from privimu.metrics import align_probabilities, estimate_latency_ms, summarize_classification
from privimu.model_cnn import fit_cnn
from privimu.model_rf import save_model, train_random_forest
from privimu.viz import plot_confusion_matrix, plot_per_subject_f1, plot_privacy_entropy_curve


def _parse_activities(value: str | None) -> list[str] | None:
    if not value:
        return None
    return [item.strip() for item in value.split(",") if item.strip()]


def _safe_model_size_mb(path: Path) -> float | None:
    if not path.exists():
        return None
    return round(path.stat().st_size / (1024 * 1024), 4)


def _rf_cross_validated_predictions(X, y, groups, n_splits: int, n_estimators: int):
    classes = np.asarray(SUBJECT_IDS, dtype=int)
    unique_groups = np.unique(groups)
    if len(unique_groups) >= 2 and n_splits >= 2:
        actual_splits = min(n_splits, len(unique_groups))
        splitter = GroupKFold(n_splits=actual_splits)
        splits = splitter.split(X, y, groups=groups)
        split_strategy = f"GroupKFold(n_splits={actual_splits}, group_key=activity_trial)"
    else:
        splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
        splits = splitter.split(X, y, groups=groups)
        split_strategy = "GroupShuffleSplit(test_size=0.2)"

    proba_oof = np.zeros((len(y), len(classes)), dtype=float)
    covered = np.zeros(len(y), dtype=bool)

    for fold_idx, (train_idx, test_idx) in enumerate(splits, start=1):
        model = train_random_forest(X[train_idx], y[train_idx], n_estimators=n_estimators)
        fold_proba = model.predict_proba(X[test_idx])
        proba_oof[test_idx] = align_probabilities(fold_proba, model.classes_, classes)
        covered[test_idx] = True
        print(f"[PrivIMU] RF fold {fold_idx}: train={len(train_idx)} test={len(test_idx)}")

    if not np.all(covered):
        # This should not happen for GroupKFold, but keeps metrics honest.
        keep = covered
        return y[keep], proba_oof[keep], classes, split_strategy
    return y, proba_oof, classes, split_strategy


def _train_rf(args, output_dir: Path) -> dict:
    config = WindowConfig(args.window_size, args.step_size, args.sampling_rate)
    activities = _parse_activities(args.activities)
    X, y, meta = build_feature_dataset(
        args.data_root,
        config=config,
        channels=DEFAULT_CHANNELS,
        activities=activities,
        max_files=args.max_files,
    )
    groups = meta[args.group_key].to_numpy()
    print(f"[PrivIMU] Dataset: X={X.shape}, subjects={len(np.unique(y))}, groups={len(np.unique(groups))}")

    y_eval, proba, classes, split_strategy = _rf_cross_validated_predictions(
        X, y, groups, n_splits=args.n_splits, n_estimators=args.n_estimators
    )
    summary = summarize_classification(y_eval, proba, classes)
    y_pred = classes[np.argmax(proba, axis=1)]

    models_dir = output_dir / "models"
    reports_dir = output_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / "rf.joblib"
    final_model = train_random_forest(X, y, n_estimators=args.n_estimators)
    save_model(final_model, model_path)

    latency_ms = estimate_latency_ms(final_model.predict_proba, X[: min(len(X), 100)])
    plot_confusion_matrix(y_eval, y_pred, classes, reports_dir / "confusion_matrix.png")
    plot_per_subject_f1(y_eval, y_pred, classes, reports_dir / "per_subject_f1.png")
    plot_privacy_entropy_curve(proba, reports_dir / "privacy_entropy_curve.png")

    return {
        "model": "random_forest",
        "model_path": str(model_path),
        "model_size_mb": _safe_model_size_mb(model_path),
        "n_estimators": args.n_estimators,
        "top1_accuracy": summary.top1_accuracy,
        "top3_accuracy": summary.top3_accuracy,
        "f1_macro": summary.f1_macro,
        "latency_ms_per_window": latency_ms,
        "privacy_entropy_leakage_bits_mean": summary.privacy_entropy_leakage_bits_mean,
        "posterior_entropy_bits_mean": summary.posterior_entropy_bits_mean,
        "split_strategy": split_strategy,
        "n_eval_windows": int(len(y_eval)),
    }, {
        "n_windows": int(X.shape[0]),
        "n_features": int(X.shape[1]),
        "n_subjects": int(len(np.unique(y))),
        "activities": sorted(meta["activity"].unique().tolist()),
        "group_key": args.group_key,
        "n_groups": int(len(np.unique(groups))),
        "feature_names": feature_names(DEFAULT_CHANNELS),
    }


def _train_cnn(args, output_dir: Path) -> dict:
    config = WindowConfig(args.window_size, args.step_size, args.sampling_rate)
    activities = _parse_activities(args.activities)
    X, y, meta = build_raw_window_dataset(
        args.data_root,
        config=config,
        channels=DEFAULT_CHANNELS,
        activities=activities,
        max_files=args.max_files,
    )
    groups = meta[args.group_key].to_numpy()
    classes = np.asarray(SUBJECT_IDS, dtype=int)
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(splitter.split(X, y, groups=groups))
    class_to_zero = {cls: idx for idx, cls in enumerate(classes)}
    y_train_zero = np.asarray([class_to_zero[int(label)] for label in y[train_idx]])
    y_test_zero = np.asarray([class_to_zero[int(label)] for label in y[test_idx]])

    model = fit_cnn(
        X[train_idx],
        y_train_zero,
        X[test_idx],
        y_test_zero,
        n_classes=len(classes),
        epochs=args.epochs,
        batch_size=args.batch_size,
    )
    proba = model.predict(X[test_idx], verbose=0)
    summary = summarize_classification(y[test_idx], proba, classes)
    y_pred = classes[np.argmax(proba, axis=1)]

    models_dir = output_dir / "models"
    reports_dir = output_dir / "reports"
    models_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / "cnn.keras"
    model.save(model_path)
    latency_ms = estimate_latency_ms(lambda sample: model.predict(sample, verbose=0), X[test_idx])

    plot_confusion_matrix(y[test_idx], y_pred, classes, reports_dir / "confusion_matrix.png")
    plot_per_subject_f1(y[test_idx], y_pred, classes, reports_dir / "per_subject_f1.png")
    plot_privacy_entropy_curve(proba, reports_dir / "privacy_entropy_curve.png")

    return {
        "model": "1d_cnn",
        "model_path": str(model_path),
        "model_size_mb": _safe_model_size_mb(model_path),
        "top1_accuracy": summary.top1_accuracy,
        "top3_accuracy": summary.top3_accuracy,
        "f1_macro": summary.f1_macro,
        "latency_ms_per_window": latency_ms,
        "privacy_entropy_leakage_bits_mean": summary.privacy_entropy_leakage_bits_mean,
        "posterior_entropy_bits_mean": summary.posterior_entropy_bits_mean,
        "split_strategy": "GroupShuffleSplit(test_size=0.2, group_key=activity_trial)",
        "n_eval_windows": int(len(test_idx)),
    }, {
        "n_windows": int(X.shape[0]),
        "n_features": int(X.shape[1] * X.shape[2]),
        "n_subjects": int(len(np.unique(y))),
        "activities": sorted(meta["activity"].unique().tolist()),
        "group_key": args.group_key,
        "n_groups": int(len(np.unique(groups))),
        "feature_names": DEFAULT_CHANNELS,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Train PrivIMU identity re-identification models.")
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    parser.add_argument("--model", choices=["rf", "cnn"], default="rf")
    parser.add_argument("--window-size", type=int, default=50)
    parser.add_argument("--step-size", type=int, default=25)
    parser.add_argument("--sampling-rate", type=float, default=50.0)
    parser.add_argument("--activities", default=None, help="Comma-separated activity codes, e.g. wlk,jog")
    parser.add_argument("--group-key", choices=["activity_trial", "trial_instance"], default="activity_trial")
    parser.add_argument("--n-splits", type=int, default=5)
    parser.add_argument("--n-estimators", type=int, default=200)
    parser.add_argument("--max-files", type=int, default=None, help="Debug option for smoke runs")
    parser.add_argument("--epochs", type=int, default=12)
    parser.add_argument("--batch-size", type=int, default=128)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.model == "rf":
        model_metrics, dataset_info = _train_rf(args, output_dir)
    else:
        model_metrics, dataset_info = _train_cnn(args, output_dir)

    metrics = {
        "project": "PrivIMU",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": {
            "name": "MotionSense",
            "data_root": str(args.data_root),
            **dataset_info,
        },
        "preprocessing": {
            "window_size_samples": args.window_size,
            "step_size_samples": args.step_size,
            "sampling_rate_hz": args.sampling_rate,
            "normalization": "z-score per window and per channel",
            "channels": DEFAULT_CHANNELS,
        },
        "primary_result": model_metrics,
        "command_hint": "python -m privimu.train --data-root data/raw/motionsense --model rf --output-dir .",
        "figures": {
            "confusion_matrix": "reports/confusion_matrix.png",
            "per_subject_f1": "reports/per_subject_f1.png",
            "privacy_entropy_curve": "reports/privacy_entropy_curve.png",
        },
    }
    metrics_path = output_dir / "reports" / "metrics.json"
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics["primary_result"], indent=2))
    print(f"[PrivIMU] Wrote {metrics_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
