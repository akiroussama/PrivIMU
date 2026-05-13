# PrivIMU Artifact Index

This file is the professor-facing map of the whole project. Every artifact should either be present in the repository or clearly marked as generated.

| # | Artifact | Path / Link | Status | Why it matters |
|---:|---|---|---|---|
| 1 | Public repository | `https://github.com/akiroussama/PrivIMU` | To publish | Main source of truth |
| 2 | README premium | `README.md` | Ready | Quick project understanding |
| 3 | Dataset downloader | `data/download.py` | Ready | Reproducibility |
| 4 | Feature pipeline | `src/privimu/features.py` | Ready | Scientific method |
| 5 | Data loader | `src/privimu/data.py` | Ready | MotionSense integration |
| 6 | Random Forest model | `src/privimu/model_rf.py` | Ready | Interpretable baseline |
| 7 | 1D-CNN model | `src/privimu/model_cnn.py` | Ready | Deep-learning extension |
| 8 | Training script | `src/privimu/train.py` | Ready | Metrics generation |
| 9 | Evaluation checker | `src/privimu/evaluate.py` | Ready | Anti-hallucination gate |
| 10 | Live demo app | `streamlit_app.py` | Ready scaffold | WOW effect in soutenance |
| 11 | Metrics JSON | `reports/metrics.json` | Generated 2026-05-13 (RF 200 trees, 5-fold GroupKFold) | Only valid numerical source |
| 12 | Confusion matrix | `reports/confusion_matrix.png` | Generated 2026-05-13 | Visual evidence |
| 13 | Per-subject F1 | `reports/per_subject_f1.png` | Generated 2026-05-13 | Fairness and targeting analysis |
| 14 | Entropy curve | `reports/privacy_entropy_curve.png` | Generated 2026-05-13 | Privacy leakage visualization |
| 15 | Colab notebook | `notebooks/PrivIMU_MotionSense_Demo.ipynb` | Ready scaffold | Reproduce without local setup |
| 16 | Experiment protocol | `docs/EXPERIMENT_PROTOCOL.md` | Ready | Methodological defense |
| 17 | Ethics and limits | `docs/ETHICS_AND_LIMITS.md` | Ready | Responsible security framing |
| 18 | Related work table | `docs/SOTA_TABLE.md` | Draft | Scientific credibility |
| 19 | Deck HTML source | `slides/PrivIMU_deck.html` | Ready v2 (2026-05-13) | Master template, edit then re-render |
| 20 | Final PowerPoint | `slides/PrivIMU_final.pptx` | Ready v2 (2026-05-13) | 15 slides, full-bleed images + speaker notes |
| 21 | Final PDF slides | `slides/PrivIMU_final.pdf` | Ready v2 (2026-05-13) | 15-page 16:9 deck rendered from HTML |
| 22 | PPTX builder | `slides/build_pptx.py` | Ready | Renders PDF → PPTX with embedded notes |
| 23 | Speaker notes | `slides/speaker_notes/M{1..5}*.md` | Ready (M5 refreshed) | 5 × 3 min orchestration |
| 24 | Report HTML source | `report/PrivIMU_report.html` | Ready v1 (2026-05-13) | Single-file report, KaTeX, print-ready |
| 25 | Report PDF | `report/PrivIMU_report.pdf` | Ready v1 (2026-05-13) | 12-page academic document, A4 |
| 26 | Report Markdown (legacy) | `report/PrivIMU_report.md` | Superseded by HTML/PDF | Kept for reference |
| 27 | Tests | `tests/` | Ready | Engineering quality |
| 28 | CI workflow | `.github/workflows/tests.yml` | Ready | Public quality signal |
| 29 | Release tag | `v1.0-submission` | Pending | Frozen final version |
| 30 | Deployment guide | `docs/DEPLOYMENT.md` | Ready | Colab and Streamlit deployment values |
| 31 | Streamlit demo CSVs | `examples/wlk_7/sub_*.csv` | Ready | Real MotionSense walking samples |

## Submission principle

The professor should be able to open this file and verify the effort in less than two minutes.

