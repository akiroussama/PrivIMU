# Run Summary

This file records reproducibility checks performed before submission.

## Scaffold verification

- `pytest -q`: expected to pass unit tests.
- Optional smoke run: create a tiny synthetic MotionSense-like layout and run `python -m privimu.train` to verify that metrics and figures are generated.

## Real training verification

After downloading MotionSense, run:

```bash
make train-rf
python -m privimu.evaluate --metrics reports/metrics.json
```

Then paste the generated values into the report and slides.

## Final submission checklist

- [ ] `reports/metrics.json` generated from real MotionSense data.
- [ ] `reports/confusion_matrix.png` generated.
- [ ] `reports/per_subject_f1.png` generated.
- [ ] `reports/privacy_entropy_curve.png` generated.
- [ ] Slides updated from JSON only.
- [ ] Report updated from JSON only.
- [ ] Streamlit demo tested locally or online.
