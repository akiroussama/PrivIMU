"""Shared constants for PrivIMU."""

from __future__ import annotations

ACTIVITY_LABELS = {
    "dws": "downstairs",
    "ups": "upstairs",
    "wlk": "walking",
    "jog": "jogging",
    "sit": "sitting",
    "std": "standing",
}

DEFAULT_CHANNELS = [
    "rotationRate.x",
    "rotationRate.y",
    "rotationRate.z",
    "userAcceleration.x",
    "userAcceleration.y",
    "userAcceleration.z",
]

SUBJECT_IDS = list(range(1, 25))
SAMPLE_RATE_HZ = 50.0
RANDOM_SEED = 42
