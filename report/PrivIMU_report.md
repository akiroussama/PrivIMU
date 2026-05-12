# PrivIMU — Motion Anonymity Attack on IoT Sensor Data

## Abstract

PrivIMU investigates whether smartphone IMU signals that appear anonymous can still reveal the identity of an enrolled user. Using the public MotionSense dataset, we build a reproducible pipeline for windowing, feature extraction, model training, evaluation, and live demonstration.

## 1. Introduction

IoT devices increasingly collect inertial signals through accelerometers and gyroscopes. These signals often appear harmless because they lack direct personal identifiers. However, movement can encode behavioral patterns. This project studies whether such patterns can be used for re-identification in a controlled dataset.

## 2. Related work

To complete from `docs/SOTA_TABLE.md`. The final report should connect human activity recognition, sensor-data privacy, and behavioral biometrics.

## 3. Dataset

PrivIMU uses MotionSense. The final report must cite the official dataset repository and papers. The experiment uses the DeviceMotion folder and selects gyroscope rotation rate plus user acceleration channels.

## 4. Methodology

The pipeline segments signals into 1-second windows at 50 Hz, with 50% overlap. Each window is normalized using z-score normalization per channel. The Random Forest baseline receives 60 extracted features.

## 5. Results

Final numerical values must be copied from `reports/metrics.json` after running the training script.

| Metric | Value |
|---|---:|
| Top-1 accuracy | generated |
| Top-3 accuracy | generated |
| F1-macro | generated |
| Latency per window | generated |
| Privacy entropy leakage | generated |

## 6. Discussion

PrivIMU should be interpreted as a privacy-risk demonstration, not as a universal biometric system. The main security implication is that IoT systems should treat motion traces as privacy-sensitive, even when they do not contain direct identifiers.

## 7. Limits

- closed-set identification;
- 24 subjects;
- phone-in-pocket context;
- dataset-specific conditions;
- Gaussian noise is illustrative only.

## 8. Conclusion

Anonymous-looking IMU signals can contain behavioral information. PrivIMU provides a reproducible mini-lab to measure and visualize this risk.
