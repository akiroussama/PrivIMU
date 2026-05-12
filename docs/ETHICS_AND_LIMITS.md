# Ethics and Limits

## Responsible purpose

PrivIMU is a defensive academic demonstration. The goal is to show that "anonymous" sensor traces may still contain behavioral information and should be protected by privacy-by-design practices.

## What the project does not do

- It does not identify real people outside MotionSense.
- It does not collect new personal data.
- It does not bypass an authentication system.
- It does not claim universal biometric identification.
- It does not claim that Gaussian noise is a complete privacy solution.

## Main limitations

1. **Closed-set setup**: the model predicts among enrolled subjects only.
2. **Dataset size**: MotionSense has 24 subjects, so results are not universal.
3. **Device position**: the data were collected with a phone in a pocket; other positions may change the signal.
4. **Context sensitivity**: activity, route, shoes, sensor quality, and sampling rate can affect performance.
5. **Defense simplification**: Gaussian noise is a pedagogical mitigation, not formal differential privacy.

## Defenses to discuss

- Data minimization: collect only what is necessary.
- On-device inference: avoid uploading raw IMU traces.
- Feature-level sharing: transmit less identifiable summaries.
- Differential privacy: formal privacy budget when feasible.
- Federated learning: train without centralizing raw traces.
- Access control and transparency: make sensor collection visible and revocable.

## Presentation wording

Recommended sentence:

> PrivIMU does not prove that every IMU trace identifies everyone. It shows that in a controlled public dataset, motion traces can behave as quasi-identifiers, so IoT systems should treat them as privacy-sensitive data.
