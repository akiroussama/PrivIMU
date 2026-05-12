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
| 11 | Metrics JSON | `reports/metrics.json` | Generated after training | Only valid numerical source |
| 12 | Confusion matrix | `reports/confusion_matrix.png` | Generated after training | Visual evidence |
| 13 | Per-subject F1 | `reports/per_subject_f1.png` | Generated after training | Fairness and targeting analysis |
| 14 | Entropy curve | `reports/privacy_entropy_curve.png` | Generated after training | Privacy leakage visualization |
| 15 | Colab notebook | `notebooks/PrivIMU_MotionSense_Demo.ipynb` | Ready scaffold | Reproduce without local setup |
| 16 | Experiment protocol | `docs/EXPERIMENT_PROTOCOL.md` | Ready | Methodological defense |
| 17 | Ethics and limits | `docs/ETHICS_AND_LIMITS.md` | Ready | Responsible security framing |
| 18 | Related work table | `docs/SOTA_TABLE.md` | Draft | Scientific credibility |
| 19 | Slides | `slides/slides.md` | Draft | 15-slide story |
| 20 | Speaker notes | `slides/speaker_notes/*.md` | Draft | 5 × 3 min orchestration |
| 21 | Report | `report/PrivIMU_report.md` | Draft | 6–8 page academic document |
| 22 | Tests | `tests/` | Ready | Engineering quality |
| 23 | CI workflow | `.github/workflows/tests.yml` | Ready | Public quality signal |
| 24 | Release tag | `v1.0-submission` | Pending | Frozen final version |

## Submission principle

The professor should be able to open this file and verify the effort in less than two minutes.
