# Data directory

This directory intentionally does not version raw MotionSense files.

Expected layout after download:

```text
data/raw/motionsense/
└── motion-sense-master/
    └── data/
        └── A_DeviceMotion_data/
            ├── dws_1/
            │   ├── sub_1.csv
            │   └── ...
            └── ...
```

Download command:

```bash
python data/download.py --dest data/raw/motionsense
```

The loader resolves several common layouts automatically, as long as it can find a folder named `A_DeviceMotion_data`.
