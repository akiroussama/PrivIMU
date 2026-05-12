"""Optional 1D-CNN model for raw IMU windows."""

from __future__ import annotations

import numpy as np


def build_cnn(input_shape: tuple[int, int], n_classes: int):
    """Build a compact 1D-CNN.

    TensorFlow is imported lazily so the Random Forest pipeline and unit tests do
    not require a heavy deep-learning installation.
    """

    try:
        import tensorflow as tf
    except ImportError as exc:  # pragma: no cover - depends on optional dependency
        raise ImportError("Install tensorflow or use --model rf") from exc

    inputs = tf.keras.Input(shape=input_shape)
    x = tf.keras.layers.Conv1D(32, 5, padding="same", activation="relu")(inputs)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.MaxPooling1D(2)(x)
    x = tf.keras.layers.Conv1D(64, 5, padding="same", activation="relu")(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Conv1D(64, 3, padding="same", activation="relu")(x)
    x = tf.keras.layers.GlobalAveragePooling1D()(x)
    x = tf.keras.layers.Dropout(0.25)(x)
    outputs = tf.keras.layers.Dense(n_classes, activation="softmax")(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def fit_cnn(
    X_train: np.ndarray,
    y_train_zero_based: np.ndarray,
    X_val: np.ndarray,
    y_val_zero_based: np.ndarray,
    n_classes: int,
    epochs: int = 12,
    batch_size: int = 128,
):
    """Train the compact 1D-CNN."""

    model = build_cnn(input_shape=X_train.shape[1:], n_classes=n_classes)
    try:
        import tensorflow as tf
    except ImportError as exc:  # pragma: no cover
        raise ImportError("Install tensorflow or use --model rf") from exc

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy", patience=3, restore_best_weights=True, mode="max"
        )
    ]
    model.fit(
        X_train,
        y_train_zero_based,
        validation_data=(X_val, y_val_zero_based),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        verbose=2,
    )
    return model
