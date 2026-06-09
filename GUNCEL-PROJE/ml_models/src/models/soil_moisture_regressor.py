"""TensorFlow/Keras Linear Regression model."""

from __future__ import annotations

import tensorflow as tf
from tensorflow import keras


def build_soil_moisture_model(n_features: int, learning_rate: float = 0.01) -> keras.Model:
    """
    Toprak nemi tahmini icin Linear Regression (tek Dense katmani).

    Aktivasyon fonksiyonu yok -> dogrusal regresyon.
    """
    model = keras.Sequential(
        [
            keras.layers.Input(shape=(n_features,), name="features"),
            keras.layers.Dense(1, name="soil_moisture_output"),
        ],
        name="soil_moisture_regressor",
    )
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss="mse",
        metrics=["mae"],
    )
    return model


def train_model(
    model: keras.Model,
    x_train,
    y_train,
    *,
    epochs: int,
    batch_size: int,
    validation_split: float,
    verbose: int = 1,
) -> keras.callbacks.History:
    return model.fit(
        x_train,
        y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=validation_split,
        verbose=verbose,
    )
