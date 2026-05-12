from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

try:
    import plotly.graph_objects as go
except ImportError:  # pragma: no cover
    go = None

from privimu.config import DEFAULT_CHANNELS, SUBJECT_IDS
from privimu.demo_samples import synthetic_imu_signal, synthetic_probability
from privimu.features import WindowConfig, extract_features, window_signal, zscore_windows
from privimu.metrics import entropy_bits, privacy_entropy_leakage
from privimu.model_rf import load_model

st.set_page_config(page_title="PrivIMU", page_icon="🛡️", layout="wide")

MODEL_PATH = Path("models/rf.joblib")


def load_rf_model():
    if MODEL_PATH.exists():
        return load_model(MODEL_PATH)
    return None


def load_uploaded_signal(uploaded_file) -> np.ndarray:
    df = pd.read_csv(uploaded_file)
    unnamed_cols = [col for col in df.columns if str(col).startswith("Unnamed")]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)
    missing = [col for col in DEFAULT_CHANNELS if col not in df.columns]
    if missing:
        st.error(f"Missing columns: {missing}")
        st.stop()
    return df[DEFAULT_CHANNELS].to_numpy(dtype=float)


def plot_signal(signal: np.ndarray):
    if go is None:
        st.line_chart(pd.DataFrame(signal, columns=DEFAULT_CHANNELS))
        return
    fig = go.Figure()
    for idx, channel in enumerate(DEFAULT_CHANNELS):
        fig.add_trace(go.Scatter(y=signal[:, idx], mode="lines", name=channel))
    fig.update_layout(height=360, margin=dict(l=20, r=20, t=30, b=20), title="IMU signal")
    st.plotly_chart(fig, use_container_width=True)


def predict_distribution(model, signal: np.ndarray, sigma: float, fallback_subject: int) -> np.ndarray:
    noisy = signal + np.random.default_rng(42).normal(0, sigma, size=signal.shape)
    if model is None:
        return synthetic_probability(fallback_subject, sigma=sigma)
    windows = zscore_windows(window_signal(noisy, WindowConfig(window_size=50, step_size=25)))
    if windows.shape[0] == 0:
        st.warning("Signal too short. Need at least 50 samples.")
        return synthetic_probability(fallback_subject, sigma=sigma)
    X = extract_features(windows)
    proba = model.predict_proba(X).mean(axis=0)
    aligned = np.zeros(len(SUBJECT_IDS), dtype=float)
    for idx, cls in enumerate(model.classes_):
        aligned[int(cls) - 1] = proba[idx]
    if aligned.sum() <= 0:
        return synthetic_probability(fallback_subject, sigma=sigma)
    return aligned / aligned.sum()


st.title("PrivIMU — Motion Anonymity Attack Demo")
st.caption("Academic IoT-security demo: anonymous-looking IMU signals can leak behavioral identity patterns.")

model = load_rf_model()
mode_label = "trained RF model" if model is not None else "fallback UI mode — train the model to enable real predictions"
st.info(f"Current mode: {mode_label}")

with st.sidebar:
    st.header("Input")
    fallback_subject = st.slider("Demo subject ID", 1, 24, 7)
    sigma = st.slider("Gaussian noise defense σ", 0.0, 1.0, 0.0, 0.05)
    uploaded = st.file_uploader("Upload MotionSense-like CSV", type=["csv"])

if uploaded is not None:
    signal = load_uploaded_signal(uploaded)
else:
    signal = synthetic_imu_signal(subject_id=fallback_subject)

noisy_signal = signal + np.random.default_rng(123).normal(0, sigma, size=signal.shape)

left, right = st.columns([1.4, 1.0])
with left:
    st.subheader("1. Anonymous IMU signal")
    plot_signal(noisy_signal)

with right:
    st.subheader("2. Identity posterior")
    posterior = predict_distribution(model, signal, sigma=sigma, fallback_subject=fallback_subject)
    top_indices = np.argsort(posterior)[::-1][:3]
    top_df = pd.DataFrame(
        {
            "rank": [1, 2, 3],
            "subject_id": [int(idx + 1) for idx in top_indices],
            "confidence": [float(posterior[idx]) for idx in top_indices],
        }
    )
    st.dataframe(top_df, use_container_width=True, hide_index=True)
    st.bar_chart(top_df.set_index("subject_id")["confidence"])

st.subheader("3. Privacy entropy score")
posterior_2d = posterior.reshape(1, -1)
entropy = float(entropy_bits(posterior_2d)[0])
leakage = float(privacy_entropy_leakage(posterior_2d)[0])
prior = float(np.log2(len(SUBJECT_IDS)))
col1, col2, col3 = st.columns(3)
col1.metric("Prior entropy", f"{prior:.2f} bits")
col2.metric("Posterior entropy", f"{entropy:.2f} bits")
col3.metric("Leakage ΔH", f"{leakage:.2f} bits")

st.caption(
    "Final numerical claims must come from reports/metrics.json. "
    "The fallback mode is only for demonstrating the interface before training."
)
