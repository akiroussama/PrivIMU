# Colab troubleshooting

## `Could not find A_DeviceMotion_data under data/raw/motionsense`

This happens when the full MotionSense repository ZIP was extracted instead of the
nested DeviceMotion dataset ZIP.

Quick repair inside Colab:

```python
from pathlib import Path
from zipfile import ZipFile

root = Path("data/raw/motionsense")
nested = list(root.rglob("A_DeviceMotion_data.zip"))
print("nested archives:", nested)
assert nested, "No nested A_DeviceMotion_data.zip found. Rerun data/download.py --force."

with ZipFile(nested[0]) as zf:
    zf.extractall(root)

print("csv files:", len(list(root.rglob("sub_*.csv"))))
```

Then rerun:

```bash
python -m privimu.train --data-root data/raw/motionsense --model rf --output-dir . --window-size 50 --step-size 25 --n-splits 5
```

Permanent fix:

```bash
python data/download.py --dest data/raw/motionsense --force
```

The fixed downloader now uses the official MotionSense DeviceMotion ZIP directly:

```text
https://github.com/mmalekzadeh/motion-sense/raw/master/data/A_DeviceMotion_data.zip
```
