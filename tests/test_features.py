import numpy as np

from privimu.config import DEFAULT_CHANNELS
from privimu.features import WindowConfig, extract_features, feature_names, window_signal, zscore_windows


def test_window_signal_shape():
    signal = np.arange(100 * 6).reshape(100, 6)
    windows = window_signal(signal, WindowConfig(window_size=50, step_size=25))
    assert windows.shape == (3, 50, 6)


def test_zscore_windows_is_stable_for_constant_signal():
    windows = np.ones((2, 50, 6))
    normalized = zscore_windows(windows)
    assert np.all(np.isfinite(normalized))
    assert np.allclose(normalized, 0.0)


def test_extract_features_has_expected_size():
    rng = np.random.default_rng(0)
    windows = rng.normal(size=(4, 50, 6))
    X = extract_features(windows)
    assert X.shape == (4, 60)
    assert len(feature_names(DEFAULT_CHANNELS)) == 60
    assert np.all(np.isfinite(X))
