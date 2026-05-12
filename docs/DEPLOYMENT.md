# PrivIMU deployment guide

## Google Colab

Open the notebook directly from GitHub:

```text
https://colab.research.google.com/github/akiroussama/PrivIMU/blob/main/notebooks/PrivIMU_MotionSense_Demo.ipynb
```

The notebook clones the repository, installs dependencies, downloads MotionSense, trains the Random Forest baseline, and prints the generated `reports/metrics.json` values.

## Streamlit Community Cloud

Use these exact values when creating the app:

```text
Repository: akiroussama/PrivIMU
Branch: main
Main file path: streamlit_app.py
Python version: 3.11 or newer
Suggested app URL/subdomain: privimu
```

The app can run in fallback UI mode before a trained model is committed. After training locally or in Colab, add `models/rf.joblib` and `reports/metrics.json` if you want the public demo to use the real trained Random Forest instead of the synthetic fallback interface.

## Local Windows run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,app]"
pytest -q
.\task.ps1 download
.\task.ps1 train-rf
.\task.ps1 demo
```

## Local Linux/macOS run

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,app]"
pytest -q
make download
make train-rf
make demo
```

## Submission rule

Any number used in slides or in the report must appear in `reports/metrics.json`.
