# Run from the root of the PrivIMU repository AFTER extracting this ZIP with -Force.
# The ZIP already contains the replacement streamlit_app.py and docs/STREAMLIT_WOW_FEATURES.md.

$ErrorActionPreference = "Stop"
Write-Host "Verifying PrivIMU Streamlit WOW update..."

if (-not (Test-Path "streamlit_app.py")) {
    Write-Error "streamlit_app.py not found. Run this script from the repository root."
}

python -m py_compile streamlit_app.py
pytest -q

Write-Host "Done. Suggested commit:"
Write-Host "git add streamlit_app.py docs/STREAMLIT_WOW_FEATURES.md README.md"
Write-Host "git commit -m 'feat: add Streamlit privacy lab WOW features' -m 'Verified-By: python -m py_compile streamlit_app.py && pytest -q' -m 'Refs: PRIVIMU_BRIEF.md'"
