"""Evaluate generated metrics and enforce submission gates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


DEFAULT_GATES = {
    "top1_accuracy": 0.65,
    "top3_accuracy": 0.80,
    "f1_macro": 0.60,
    "latency_ms_per_window": 100.0,
}


def load_metrics(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Metrics file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def check_metrics(metrics: dict, strict: bool = False) -> list[str]:
    result = metrics.get("primary_result", {})
    warnings: list[str] = []
    for key, threshold in DEFAULT_GATES.items():
        if key not in result:
            warnings.append(f"Missing metric: {key}")
            continue
        value = float(result[key])
        if key == "latency_ms_per_window":
            passed = value <= threshold
            symbol = "<="
        else:
            passed = value >= threshold
            symbol = ">="
        if not passed:
            warnings.append(f"Gate not reached: {key}={value:.4f} expected {symbol} {threshold}")
    if strict and warnings:
        raise AssertionError("\n".join(warnings))
    return warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check PrivIMU generated metrics.")
    parser.add_argument("--metrics", type=Path, default=Path("reports/metrics.json"))
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)

    metrics = load_metrics(args.metrics)
    result = metrics.get("primary_result", {})
    print("PrivIMU metrics summary")
    for key in ["model", "top1_accuracy", "top3_accuracy", "f1_macro", "latency_ms_per_window", "privacy_entropy_leakage_bits_mean"]:
        if key in result:
            print(f"- {key}: {result[key]}")

    warnings = check_metrics(metrics, strict=args.strict)
    if warnings:
        print("\nSubmission gates requiring attention:")
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("\nAll default gates are reached.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
