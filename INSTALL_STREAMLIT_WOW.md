# Install Streamlit WOW update

From PowerShell, at the root of the PrivIMU repository:

```powershell
Expand-Archive -Force .\PrivIMU_streamlit_3wow_features_overlay.zip -DestinationPath .
python -m py_compile streamlit_app.py
pytest -q
streamlit run streamlit_app.py
```

Then commit:

```powershell
git add streamlit_app.py docs/STREAMLIT_WOW_FEATURES.md README.md
git commit -m "feat: add Streamlit privacy lab WOW features" `
  -m "Verified-By: python -m py_compile streamlit_app.py && pytest -q" `
  -m "Refs: PRIVIMU_BRIEF.md"
git push
```
