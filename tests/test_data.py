from pathlib import Path

import numpy as np
import pandas as pd

from privimu.config import DEFAULT_CHANNELS
from privimu.data import build_feature_dataset, parse_motion_file, resolve_device_motion_root
from privimu.features import WindowConfig


def test_parse_motion_file():
    item = parse_motion_file(Path("data/A_DeviceMotion_data/wlk_3/sub_12.csv"))
    assert item.activity == "wlk"
    assert item.trial == 3
    assert item.subject == 12
    assert item.activity_trial_group == "wlk_03"


def test_build_feature_dataset_from_tiny_layout(tmp_path):
    root = tmp_path / "motionsense" / "data" / "A_DeviceMotion_data" / "wlk_1"
    root.mkdir(parents=True)
    df = pd.DataFrame(np.random.default_rng(0).normal(size=(60, len(DEFAULT_CHANNELS))), columns=DEFAULT_CHANNELS)
    df.to_csv(root / "sub_1.csv", index=False)
    resolved = resolve_device_motion_root(tmp_path / "motionsense")
    assert resolved.name == "A_DeviceMotion_data"
    X, y, meta = build_feature_dataset(
        tmp_path / "motionsense",
        config=WindowConfig(window_size=50, step_size=25),
        activities=["wlk"],
    )
    assert X.shape == (1, 60)
    assert y.tolist() == [1]
    assert meta.iloc[0]["activity"] == "wlk"
