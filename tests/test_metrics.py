import numpy as np

from privimu.metrics import entropy_bits, privacy_entropy_leakage, summarize_classification, top_k_accuracy


def test_top_k_accuracy_with_custom_classes():
    y = np.array([10, 20, 30])
    classes = np.array([10, 20, 30])
    proba = np.array([
        [0.9, 0.1, 0.0],
        [0.3, 0.4, 0.3],
        [0.5, 0.2, 0.3],
    ])
    assert top_k_accuracy(y, proba, classes, k=1) == 2 / 3
    assert top_k_accuracy(y, proba, classes, k=3) == 1.0


def test_entropy_leakage_bounds():
    uniform = np.full((2, 4), 0.25)
    confident = np.array([[0.97, 0.01, 0.01, 0.01]])
    assert np.allclose(privacy_entropy_leakage(uniform), 0.0, atol=1e-6)
    assert privacy_entropy_leakage(confident)[0] > 1.7
    assert entropy_bits(uniform)[0] == 2.0


def test_summarize_classification():
    y = np.array([1, 2, 3])
    classes = np.array([1, 2, 3])
    proba = np.eye(3)
    summary = summarize_classification(y, proba, classes)
    assert summary.top1_accuracy == 1.0
    assert summary.top3_accuracy == 1.0
    assert summary.f1_macro == 1.0
