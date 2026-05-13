from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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
SAMPLE_CSV_PATHS = [
    Path("demo/sample_motionsense_like.csv"),
    Path("demo/motionsense_like_sample.csv"),
    Path("examples/demo_motionsense_like.csv"),
]
OFFICIAL_MOTIONSENSE_ZIP_URL = "https://github.com/mmalekzadeh/motion-sense/raw/master/data/A_DeviceMotion_data.zip"
RAW_DEMO_CSV_URLS = [
    "https://raw.githubusercontent.com/akiroussama/PrivIMU/main/demo/sample_motionsense_like.csv",
    "https://raw.githubusercontent.com/akiroussama/PrivIMU/main/demo/motionsense_like_sample.csv",
    "https://raw.githubusercontent.com/akiroussama/PrivIMU/main/examples/demo_motionsense_like.csv",
]
WINDOW_CONFIG = WindowConfig(window_size=50, step_size=25)
EPS = 1e-12


@st.cache_resource(show_spinner=False)
def load_rf_model():
    """Load the trained RF model when available on disk."""

    if MODEL_PATH.exists():
        return load_model(MODEL_PATH)
    return None


def inject_css() -> None:
    """Small visual polish for the live demo."""

    st.markdown(
        """
        <style>
        .privimu-hero {
            padding: 1.2rem 1.4rem;
            border: 1px solid rgba(125, 211, 252, 0.28);
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(14, 116, 144, 0.18), rgba(30, 41, 59, 0.45));
            margin-bottom: 1.0rem;
        }
        .privimu-hero h1 { margin-bottom: 0.2rem; }
        .privimu-chip {
            display: inline-block;
            padding: 0.25rem 0.55rem;
            margin-right: 0.35rem;
            margin-top: 0.35rem;
            border-radius: 999px;
            border: 1px solid rgba(148, 163, 184, 0.35);
            background: rgba(15, 23, 42, 0.35);
            font-size: 0.82rem;
        }
        .privimu-card {
            padding: 0.9rem 1rem;
            border-radius: 14px;
            border: 1px solid rgba(148, 163, 184, 0.25);
            background: rgba(15, 23, 42, 0.20);
        }
        .privimu-small { color: #94a3b8; font-size: 0.86rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_uploaded_signal(uploaded_file) -> tuple[np.ndarray, str]:
    """Load a MotionSense-like CSV and return the six IMU channels."""

    df = pd.read_csv(uploaded_file)
    unnamed_cols = [col for col in df.columns if str(col).startswith("Unnamed")]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)
    missing = [col for col in DEFAULT_CHANNELS if col not in df.columns]
    if missing:
        st.error(f"Missing columns: {missing}")
        st.info("Expected columns: " + ", ".join(DEFAULT_CHANNELS))
        st.stop()
    label = getattr(uploaded_file, "name", "uploaded_csv")
    return df[DEFAULT_CHANNELS].to_numpy(dtype=float), label


def sample_csv_bytes() -> tuple[bytes, str]:
    """Return a bundled demo CSV when available, otherwise generate one on the fly."""

    for path in SAMPLE_CSV_PATHS:
        if path.exists():
            return path.read_bytes(), path.name
    df = pd.DataFrame(synthetic_imu_signal(subject_id=7), columns=DEFAULT_CHANNELS)
    df.insert(0, "time_s", np.arange(len(df)) / 50.0)
    return df.to_csv(index=False).encode("utf-8"), "sample_motionsense_like.csv"


def plot_signal(signal: np.ndarray, title: str = "IMU signal") -> None:
    """Plot the six IMU channels."""

    frame = pd.DataFrame(signal, columns=DEFAULT_CHANNELS)
    if go is None:
        st.line_chart(frame)
        return

    fig = go.Figure()
    for idx, channel in enumerate(DEFAULT_CHANNELS):
        fig.add_trace(go.Scatter(y=frame[channel], mode="lines", name=channel, line=dict(width=1.3)))
    fig.update_layout(
        height=370,
        margin=dict(l=20, r=20, t=42, b=20),
        title=title,
        xaxis_title="sample index",
        yaxis_title="sensor value",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)


def align_model_probabilities(model, proba: np.ndarray) -> np.ndarray:
    """Align model probability columns to subject IDs 1..24."""

    aligned = np.zeros((proba.shape[0], len(SUBJECT_IDS)), dtype=float)
    for idx, cls in enumerate(model.classes_):
        cls_id = int(cls)
        if 1 <= cls_id <= len(SUBJECT_IDS):
            aligned[:, cls_id - 1] = proba[:, idx]
    row_sums = aligned.sum(axis=1, keepdims=True)
    row_sums = np.where(row_sums < EPS, 1.0, row_sums)
    return aligned / row_sums


def fallback_window_posteriors(n_windows: int, fallback_subject: int, sigma: float) -> np.ndarray:
    """Synthetic posterior trajectory used only before a trained model exists."""

    n_windows = max(1, int(n_windows))
    base = synthetic_probability(fallback_subject, sigma=sigma)
    uniform = np.full(len(SUBJECT_IDS), 1.0 / len(SUBJECT_IDS))
    posteriors = []
    for idx in range(n_windows):
        reveal = 0.18 + 0.82 * ((idx + 1) / n_windows) ** 0.8
        defended_reveal = reveal * max(0.15, 1.0 - sigma * 1.1)
        p = defended_reveal * base + (1.0 - defended_reveal) * uniform
        posteriors.append(p / p.sum())
    return np.vstack(posteriors)


def predict_window_posteriors(model, signal: np.ndarray, sigma: float, fallback_subject: int) -> np.ndarray:
    """Return one posterior distribution per sliding window."""

    rng = np.random.default_rng(42)
    noisy = signal + rng.normal(0, sigma, size=signal.shape)
    windows_raw = window_signal(noisy, WINDOW_CONFIG)
    n_windows = max(1, windows_raw.shape[0])

    if model is None or windows_raw.shape[0] == 0:
        return fallback_window_posteriors(n_windows, fallback_subject, sigma)

    windows = zscore_windows(windows_raw)
    X = extract_features(windows)
    if X.shape[0] == 0:
        return fallback_window_posteriors(n_windows, fallback_subject, sigma)
    return align_model_probabilities(model, model.predict_proba(X))


def aggregate_posterior(window_posteriors: np.ndarray) -> np.ndarray:
    """Aggregate per-window probabilities into one identity posterior."""

    p = np.asarray(window_posteriors, dtype=float).mean(axis=0)
    total = p.sum()
    if total < EPS:
        return np.full(len(SUBJECT_IDS), 1.0 / len(SUBJECT_IDS))
    return p / total


def topk_dataframe(posterior: np.ndarray, k: int = 3) -> pd.DataFrame:
    """Top-k subjects as a small dataframe."""

    top_indices = np.argsort(posterior)[::-1][:k]
    return pd.DataFrame(
        {
            "rank": list(range(1, len(top_indices) + 1)),
            "subject_id": [int(idx + 1) for idx in top_indices],
            "confidence": [float(posterior[idx]) for idx in top_indices],
        }
    )


def summarize_privacy(posterior: np.ndarray) -> dict[str, float]:
    """Compute entropy and leakage for one posterior."""

    posterior_2d = posterior.reshape(1, -1)
    entropy = float(entropy_bits(posterior_2d)[0])
    leakage = float(privacy_entropy_leakage(posterior_2d)[0])
    prior = float(np.log2(len(SUBJECT_IDS)))
    return {"prior_entropy": prior, "posterior_entropy": entropy, "leakage": leakage}


def risk_label(leakage: float) -> str:
    if leakage >= 2.5:
        return "Critical"
    if leakage >= 1.5:
        return "High"
    if leakage >= 0.7:
        return "Moderate"
    return "Low"


def plot_risk_gauge(leakage: float) -> None:
    """Display an intuitive privacy leakage gauge."""

    max_bits = float(np.log2(len(SUBJECT_IDS)))
    if go is None:
        st.progress(min(1.0, leakage / max_bits))
        return
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=leakage,
            number={"suffix": " bits"},
            title={"text": "Privacy leakage ΔH"},
            gauge={
                "axis": {"range": [0, max_bits]},
                "bar": {"thickness": 0.35},
                "steps": [
                    {"range": [0, 0.7], "color": "rgba(34,197,94,0.20)"},
                    {"range": [0.7, 1.5], "color": "rgba(234,179,8,0.20)"},
                    {"range": [1.5, 2.5], "color": "rgba(249,115,22,0.20)"},
                    {"range": [2.5, max_bits], "color": "rgba(239,68,68,0.20)"},
                ],
            },
        )
    )
    fig.update_layout(height=255, margin=dict(l=20, r=20, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)


def detect_identity_lock(posteriors: np.ndarray, threshold: float = 0.35, min_stable_windows: int = 3) -> dict[str, Any]:
    """Detect when the attack becomes stable enough to call an identity lock."""

    p = np.asarray(posteriors, dtype=float)
    top_subjects = np.argmax(p, axis=1) + 1
    top_conf = np.max(p, axis=1)
    step_seconds = WINDOW_CONFIG.step_size / WINDOW_CONFIG.sampling_rate_hz

    for idx in range(max(0, min_stable_windows - 1), len(top_subjects)):
        start = idx - min_stable_windows + 1
        stable_subjects = top_subjects[start : idx + 1]
        stable_conf = top_conf[start : idx + 1]
        if len(set(stable_subjects.tolist())) == 1 and float(stable_conf.mean()) >= threshold:
            return {
                "locked": True,
                "subject_id": int(stable_subjects[-1]),
                "time_s": float(idx * step_seconds),
                "confidence": float(stable_conf.mean()),
            }

    return {
        "locked": False,
        "subject_id": int(top_subjects[-1]),
        "time_s": None,
        "confidence": float(top_conf[-1]),
    }


def render_attack_replay(posteriors: np.ndarray, lock: dict[str, Any]) -> None:
    """WOW feature 1: window-by-window identity reveal."""

    st.subheader("4. WOW #1 — Live identity-lock replay")
    st.caption("The app replays the attack window by window: confidence rises, entropy falls, and the identity stabilizes.")

    top_subjects = np.argmax(posteriors, axis=1) + 1
    top_conf = np.max(posteriors, axis=1)
    leakage_curve = privacy_entropy_leakage(posteriors)
    entropy_curve = entropy_bits(posteriors)
    time_s = np.arange(len(posteriors)) * (WINDOW_CONFIG.step_size / WINDOW_CONFIG.sampling_rate_hz)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("windows analyzed", f"{len(posteriors)}")
    c2.metric("final top-1", f"Subject {int(top_subjects[-1])}")
    c3.metric("final confidence", f"{float(top_conf[-1]) * 100:.1f}%")
    lock_text = f"{lock['time_s']:.1f}s" if lock["locked"] else "not locked"
    c4.metric("identity lock", lock_text)

    if go is None:
        st.line_chart(
            pd.DataFrame(
                {
                    "time_s": time_s,
                    "top1_confidence": top_conf,
                    "leakage_bits": leakage_curve,
                    "posterior_entropy_bits": entropy_curve,
                }
            ).set_index("time_s")
        )
    else:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=time_s,
                y=top_conf,
                mode="lines+markers",
                name="Top-1 confidence",
                yaxis="y",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=time_s,
                y=leakage_curve,
                mode="lines+markers",
                name="Leakage ΔH (bits)",
                yaxis="y2",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=time_s,
                y=entropy_curve,
                mode="lines",
                name="Posterior entropy (bits)",
                yaxis="y2",
                line=dict(dash="dot"),
            )
        )
        fig.update_layout(
            height=360,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis_title="seconds",
            yaxis=dict(title="confidence", range=[0, 1]),
            yaxis2=dict(title="bits", overlaying="y", side="right"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig, use_container_width=True)

    frame_idx = st.slider("Replay frame", 1, len(posteriors), len(posteriors)) - 1
    frame_df = topk_dataframe(posteriors[frame_idx], k=5)
    st.dataframe(frame_df, use_container_width=True, hide_index=True)


def run_defense_sweep(model, signal: np.ndarray, fallback_subject: int, max_sigma: float) -> pd.DataFrame:
    """WOW feature 2: red-team/blue-team sweep across defense strengths."""

    grid = np.linspace(0.0, max_sigma, 11)
    signal_std = float(np.std(signal))
    rows = []
    for sigma_i in grid:
        posteriors_i = predict_window_posteriors(model, signal, sigma=float(sigma_i), fallback_subject=fallback_subject)
        posterior_i = aggregate_posterior(posteriors_i)
        privacy_i = summarize_privacy(posterior_i)
        top_subject = int(np.argmax(posterior_i) + 1)
        top_conf = float(np.max(posterior_i))
        if sigma_i <= 0:
            snr_db = 60.0
        else:
            snr_db = float(20.0 * np.log10((signal_std + EPS) / (sigma_i + EPS)))
        signal_preservation = float(np.clip(1.0 - sigma_i / (signal_std + EPS), 0.0, 1.0))
        rows.append(
            {
                "sigma": float(sigma_i),
                "top_subject": top_subject,
                "top1_confidence": top_conf,
                "posterior_entropy_bits": privacy_i["posterior_entropy"],
                "leakage_bits": privacy_i["leakage"],
                "snr_db_proxy": snr_db,
                "signal_preservation_proxy": signal_preservation,
            }
        )
    return pd.DataFrame(rows)


def render_defense_sweep(sweep_df: pd.DataFrame) -> dict[str, Any]:
    """WOW feature 2 visualization."""

    st.subheader("5. WOW #2 — Defense lab: noise sweep")
    st.caption(
        "Blue-team view: increase Gaussian noise, observe how identity confidence and leakage degrade. "
        "The signal-preservation value is a demo proxy, not a final scientific utility metric."
    )

    max_bits = float(np.log2(len(SUBJECT_IDS)))
    candidates = sweep_df[(sweep_df["top1_confidence"] <= 0.20) | (sweep_df["leakage_bits"] <= 0.70)]
    if len(candidates) > 0:
        recommended = candidates.iloc[0].to_dict()
        recommendation = (
            f"σ ≈ {recommended['sigma']:.2f} reduces top-1 confidence to "
            f"{recommended['top1_confidence'] * 100:.1f}% and leakage to {recommended['leakage_bits']:.2f} bits."
        )
    else:
        recommended = sweep_df.iloc[-1].to_dict()
        recommendation = (
            "The chosen sweep range did not reach the target privacy threshold; "
            f"at σ={recommended['sigma']:.2f}, leakage is {recommended['leakage_bits']:.2f} bits."
        )

    c1, c2, c3 = st.columns(3)
    c1.metric("recommended defense", f"σ={recommended['sigma']:.2f}")
    c2.metric("top-1 after defense", f"{recommended['top1_confidence'] * 100:.1f}%")
    c3.metric("leakage after defense", f"{recommended['leakage_bits']:.2f}/{max_bits:.2f} bits")
    st.success(recommendation)

    if go is None:
        st.line_chart(sweep_df.set_index("sigma")[["top1_confidence", "leakage_bits", "signal_preservation_proxy"]])
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sweep_df["sigma"], y=sweep_df["top1_confidence"], mode="lines+markers", name="Top-1 confidence"))
        fig.add_trace(go.Scatter(x=sweep_df["sigma"], y=sweep_df["leakage_bits"], mode="lines+markers", name="Leakage ΔH (bits)", yaxis="y2"))
        fig.add_trace(go.Scatter(x=sweep_df["sigma"], y=sweep_df["signal_preservation_proxy"], mode="lines+markers", name="Signal preservation proxy"))
        fig.update_layout(
            height=360,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis_title="Gaussian noise σ",
            yaxis=dict(title="confidence / preservation", range=[0, 1]),
            yaxis2=dict(title="leakage bits", overlaying="y", side="right", range=[0, max_bits]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Show defense sweep table"):
        st.dataframe(sweep_df, use_container_width=True, hide_index=True)
    return {"recommended": recommended, "message": recommendation}


def build_evidence_report(
    *,
    source_label: str,
    model_mode: str,
    signal: np.ndarray,
    sigma: float,
    top_df: pd.DataFrame,
    privacy: dict[str, float],
    lock: dict[str, Any],
    sweep_summary: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a compact audit artifact for download."""

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": "PrivIMU",
        "demo_mode": model_mode,
        "source": source_label,
        "signal": {
            "samples": int(signal.shape[0]),
            "channels": DEFAULT_CHANNELS,
            "window_size_samples": WINDOW_CONFIG.window_size,
            "step_size_samples": WINDOW_CONFIG.step_size,
        },
        "defense": {"gaussian_noise_sigma": float(sigma)},
        "identity_posterior_top3": top_df.to_dict(orient="records"),
        "privacy": privacy,
        "identity_lock": lock,
        "defense_sweep": sweep_summary,
        "note": (
            "Interactive demo artifact. Final report-level claims must be backed by reports/metrics.json. "
            "Fallback UI mode is synthetic and should not be reported as measured performance."
        ),
    }


def report_to_markdown(report: dict[str, Any]) -> str:
    """Human-readable attack report."""

    top_lines = [
        f"{row['rank']}. Subject {row['subject_id']} — {row['confidence'] * 100:.2f}%"
        for row in report["identity_posterior_top3"]
    ]
    lock = report["identity_lock"]
    lock_line = (
        f"Identity lock reached at {lock['time_s']:.2f}s on Subject {lock['subject_id']}"
        if lock.get("locked")
        else "No stable identity lock reached under the selected threshold"
    )
    privacy = report["privacy"]
    sweep_message = "not computed"
    if report.get("defense_sweep"):
        sweep_message = report["defense_sweep"].get("message", "computed")

    return f"""# PrivIMU attack evidence card

Generated at: `{report['generated_at_utc']}`  
Source: `{report['source']}`  
Mode: `{report['demo_mode']}`  
Noise defense σ: `{report['defense']['gaussian_noise_sigma']:.2f}`

## Top-3 identity posterior

{chr(10).join(top_lines)}

## Privacy entropy

- Prior entropy: `{privacy['prior_entropy']:.3f}` bits
- Posterior entropy: `{privacy['posterior_entropy']:.3f}` bits
- Leakage ΔH: `{privacy['leakage']:.3f}` bits
- Risk label: `{risk_label(float(privacy['leakage']))}`

## Live replay

{lock_line}

## Defense sweep

{sweep_message}

## Reproducibility note

This is an interactive Streamlit evidence card. Final scientific claims in the slides and report must come from `reports/metrics.json` generated by the versioned training/evaluation pipeline.
"""


def render_evidence_center(report: dict[str, Any]) -> None:
    """WOW feature 3: downloadable attack evidence card."""

    st.subheader("6. WOW #3 — One-click evidence card")
    st.caption("A professor can download exactly what happened in the demo: input, top-3 identity, entropy leakage, defense setting.")

    json_payload = json.dumps(report, indent=2, ensure_ascii=False)
    md_payload = report_to_markdown(report)

    c1, c2, c3 = st.columns([1, 1, 2])
    c1.download_button(
        "Download JSON evidence",
        data=json_payload.encode("utf-8"),
        file_name="privimu_attack_evidence.json",
        mime="application/json",
        use_container_width=True,
    )
    c2.download_button(
        "Download Markdown card",
        data=md_payload.encode("utf-8"),
        file_name="privimu_attack_evidence.md",
        mime="text/markdown",
        use_container_width=True,
    )
    with c3:
        st.code(
            f"Anonymous IMU → Top-3 identity + ΔH={report['privacy']['leakage']:.2f} bits ({risk_label(report['privacy']['leakage'])})",
            language="text",
        )

    with st.expander("Preview evidence card"):
        st.markdown(md_payload)


inject_css()
model = load_rf_model()
model_mode = "trained RF model" if model is not None else "fallback UI mode — train RF to enable real predictions"

st.markdown(
    """
    <div class="privimu-hero">
      <h1>PrivIMU — Motion Anonymity Attack Demo</h1>
      <div class="privimu-small">Academic IoT-security demo: anonymous-looking accelerometer + gyroscope traces can leak behavioral identity patterns.</div>
      <span class="privimu-chip">Red team: re-identification</span>
      <span class="privimu-chip">Blue team: noise defense</span>
      <span class="privimu-chip">Reproducible: metrics.json</span>
    </div>
    """,
    unsafe_allow_html=True,
)

if model is None:
    st.warning(
        "Current mode: fallback UI mode. The app remains clickable for deployment review, "
        "but real identity predictions require `models/rf.joblib` generated by `python -m privimu.train --model rf`."
    )
else:
    st.success("Current mode: trained Random Forest model loaded from models/rf.joblib.")

with st.sidebar:
    st.header("Input")
    fallback_subject = st.slider("Demo subject ID", 1, 24, 7)
    sigma = st.slider("Gaussian noise defense σ", 0.0, 1.0, 0.0, 0.05)
    uploaded = st.file_uploader("Upload MotionSense-like CSV", type=["csv"])

    st.divider()
    st.header("WOW controls")
    lock_threshold = st.slider("Identity-lock threshold", 0.05, 0.80, 0.35, 0.05)
    max_sweep_sigma = st.slider("Defense sweep max σ", 0.10, 1.50, 1.00, 0.10)
    run_sweep = st.toggle("Run blue-team sweep", value=True)

    st.divider()
    st.caption("Need a CSV for the upload box?")
    sample_bytes, sample_name = sample_csv_bytes()
    st.download_button(
        label="Download demo CSV",
        data=sample_bytes,
        file_name=sample_name,
        mime="text/csv",
        help="Synthetic MotionSense-like file with the six IMU columns used by PrivIMU.",
        use_container_width=True,
    )
    st.markdown("Raw demo CSV on GitHub:")
    for idx, url in enumerate(RAW_DEMO_CSV_URLS, start=1):
        st.markdown(f"- [mirror {idx}]({url})")
    st.markdown(f"[Official MotionSense DeviceMotion ZIP]({OFFICIAL_MOTIONSENSE_ZIP_URL})")
    st.caption("Extract the ZIP, then upload a file like A_DeviceMotion_data/wlk_7/sub_1.csv.")

if uploaded is not None:
    signal, source_label = load_uploaded_signal(uploaded)
else:
    signal = synthetic_imu_signal(subject_id=fallback_subject)
    source_label = f"synthetic demo signal for subject {fallback_subject}"

noisy_signal = signal + np.random.default_rng(123).normal(0, sigma, size=signal.shape)
window_posteriors = predict_window_posteriors(model, signal, sigma=sigma, fallback_subject=fallback_subject)
posterior = aggregate_posterior(window_posteriors)
top_df = topk_dataframe(posterior, k=3)
privacy = summarize_privacy(posterior)
lock = detect_identity_lock(window_posteriors, threshold=lock_threshold)

left, right = st.columns([1.35, 1.0])
with left:
    st.subheader("1. Anonymous IMU signal")
    st.caption(f"Source: {source_label} · samples: {signal.shape[0]} · channels: {len(DEFAULT_CHANNELS)}")
    plot_signal(noisy_signal, title="IMU signal after selected defense noise")

with right:
    st.subheader("2. Identity posterior")
    st.dataframe(top_df, use_container_width=True, hide_index=True)
    st.bar_chart(top_df.set_index("subject_id")["confidence"])
    plot_risk_gauge(privacy["leakage"])

st.subheader("3. Privacy entropy score")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Prior entropy", f"{privacy['prior_entropy']:.2f} bits")
col2.metric("Posterior entropy", f"{privacy['posterior_entropy']:.2f} bits")
col3.metric("Leakage ΔH", f"{privacy['leakage']:.2f} bits")
col4.metric("Risk label", risk_label(privacy["leakage"]))

render_attack_replay(window_posteriors, lock)

sweep_summary = None
if run_sweep:
    sweep_df = run_defense_sweep(model, signal, fallback_subject=fallback_subject, max_sigma=max_sweep_sigma)
    sweep_summary = render_defense_sweep(sweep_df)
else:
    st.info("Blue-team sweep disabled in the sidebar. Enable it to show the defense frontier.")

report = build_evidence_report(
    source_label=source_label,
    model_mode=model_mode,
    signal=signal,
    sigma=sigma,
    top_df=top_df,
    privacy=privacy,
    lock=lock,
    sweep_summary=sweep_summary,
)
render_evidence_center(report)

st.caption(
    "Final numerical claims in the slides/report must come from reports/metrics.json. "
    "Fallback UI mode is only for demonstrating the interface before training."
)
