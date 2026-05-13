#!/usr/bin/env python3
"""Download and extract MotionSense DeviceMotion CSV files.

This script intentionally downloads the official DeviceMotion archive, not the
whole GitHub repository. The training pipeline expects MotionSense CSV files such
as ``wlk_7/sub_1.csv`` under ``data/raw/motionsense``.

It also handles the common mistake where the repository ZIP was downloaded
instead: if a nested ``A_DeviceMotion_data.zip`` is found after extraction, the
script extracts it automatically.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

DEFAULT_URL = "https://github.com/mmalekzadeh/motion-sense/raw/master/data/A_DeviceMotion_data.zip"
REPO_ZIP_URL = "https://github.com/mmalekzadeh/motion-sense/archive/refs/heads/master.zip"
EXPECTED_DIR = "A_DeviceMotion_data"


def download_file(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    print(f"[PrivIMU] Downloading {url}")
    with urllib.request.urlopen(url) as response, target.open("wb") as out:
        shutil.copyfileobj(response, out)
    print(f"[PrivIMU] Saved archive to {target}")


def _safe_extract_zip(archive: Path, dest: Path) -> None:
    """Extract a ZIP file while protecting against path traversal."""

    dest_resolved = dest.resolve()
    with zipfile.ZipFile(archive) as zf:
        for member in zf.infolist():
            target = (dest / member.filename).resolve()
            if not str(target).startswith(str(dest_resolved)):
                raise RuntimeError(f"Unsafe path in zip archive: {member.filename}")
        zf.extractall(dest)


def _has_subject_csv_files(path: Path) -> bool:
    return any(path.rglob("sub_*.csv"))


def _find_device_motion_dir(dest: Path) -> Path | None:
    candidates = [
        dest / EXPECTED_DIR,
        dest / "data" / EXPECTED_DIR,
        dest / "motion-sense-master" / "data" / EXPECTED_DIR,
        dest / "motion-sense-main" / "data" / EXPECTED_DIR,
    ]
    for candidate in candidates:
        if candidate.is_dir() and _has_subject_csv_files(candidate):
            return candidate
    for candidate in dest.rglob(EXPECTED_DIR):
        if candidate.is_dir() and _has_subject_csv_files(candidate):
            return candidate
    if _has_subject_csv_files(dest):
        return dest
    return None


def _extract_nested_device_motion_zip(dest: Path) -> bool:
    """Extract a nested A_DeviceMotion_data.zip if the repo ZIP was downloaded."""

    nested_zips = sorted(dest.rglob(f"{EXPECTED_DIR}.zip"))
    if not nested_zips:
        return False

    nested = nested_zips[0]
    print(f"[PrivIMU] Found nested dataset archive: {nested}")
    print(f"[PrivIMU] Extracting nested MotionSense archive to {dest}")
    _safe_extract_zip(nested, dest)
    return True


def extract_zip(archive: Path, dest: Path, force: bool = False) -> Path:
    if dest.exists() and any(dest.iterdir()) and not force:
        existing = _find_device_motion_dir(dest)
        if existing is not None:
            print(f"[PrivIMU] Dataset already available at {existing}")
            return existing
        raise FileExistsError(
            f"Destination {dest} is not empty but MotionSense CSV files were not found. "
            "Use --force to overwrite or run the one-cell Colab repair snippet."
        )

    if force and dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)

    print(f"[PrivIMU] Extracting to {dest}")
    _safe_extract_zip(archive, dest)

    device_root = _find_device_motion_dir(dest)
    if device_root is None:
        _extract_nested_device_motion_zip(dest)
        device_root = _find_device_motion_dir(dest)

    if device_root is None:
        raise FileNotFoundError(
            f"Could not find MotionSense subject CSV files after extracting {archive}. "
            f"Tip: use the official dataset URL: {DEFAULT_URL}"
        )

    csv_count = len(list(device_root.rglob("sub_*.csv")))
    print(f"[PrivIMU] Verified dataset root: {device_root}")
    print(f"[PrivIMU] Found {csv_count} MotionSense subject CSV files")
    return device_root


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Download the MotionSense DeviceMotion dataset archive.")
    parser.add_argument("--url", default=DEFAULT_URL, help="MotionSense ZIP archive URL")
    parser.add_argument("--dest", type=Path, default=Path("data/raw/motionsense"))
    parser.add_argument("--archive", type=Path, default=Path("data/raw/A_DeviceMotion_data.zip"))
    parser.add_argument("--force", action="store_true", help="Overwrite destination if it exists")
    parser.add_argument(
        "--repo-zip",
        action="store_true",
        help="Download the whole MotionSense repository ZIP, then auto-extract the nested dataset ZIP.",
    )
    args = parser.parse_args(argv)

    url = REPO_ZIP_URL if args.repo_zip else args.url
    download_file(url, args.archive)
    extract_zip(args.archive, args.dest, force=args.force)
    print("[PrivIMU] Done. Next: python -m privimu.train --data-root data/raw/motionsense --model rf --output-dir .")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
