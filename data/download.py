#!/usr/bin/env python3
"""Download MotionSense from the official GitHub repository.

The script avoids storing raw data in git. It downloads a ZIP archive and extracts
it under data/raw/motionsense by default.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

DEFAULT_URL = "https://github.com/mmalekzadeh/motion-sense/archive/refs/heads/master.zip"


def download_file(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    print(f"[PrivIMU] Downloading {url}")
    with urllib.request.urlopen(url) as response, target.open("wb") as out:
        shutil.copyfileobj(response, out)
    print(f"[PrivIMU] Saved archive to {target}")


def extract_zip(archive: Path, dest: Path, force: bool = False) -> None:
    if dest.exists() and any(dest.iterdir()) and not force:
        raise FileExistsError(
            f"Destination {dest} is not empty. Use --force to overwrite or choose another path."
        )
    if force and dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)
    print(f"[PrivIMU] Extracting to {dest}")
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(dest)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Download the MotionSense dataset archive.")
    parser.add_argument("--url", default=DEFAULT_URL, help="MotionSense ZIP archive URL")
    parser.add_argument("--dest", type=Path, default=Path("data/raw/motionsense"))
    parser.add_argument("--archive", type=Path, default=Path("data/raw/motionsense.zip"))
    parser.add_argument("--force", action="store_true", help="Overwrite destination if it exists")
    args = parser.parse_args(argv)

    download_file(args.url, args.archive)
    extract_zip(args.archive, args.dest, force=args.force)
    print("[PrivIMU] Done. You can now run: make train-rf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
