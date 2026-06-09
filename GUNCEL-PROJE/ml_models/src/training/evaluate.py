"""Model degerlendirme scripti."""

from __future__ import annotations

import argparse
import logging

import tensorflow as tf

from src.config import TrainingConfig
from src.data.loader import load_training_data
from src.data.preprocessor import prepare_data
from src.utils.metrics import compute_metrics

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def evaluate_saved_model(config: TrainingConfig | None = None) -> dict:
    config = config or TrainingConfig.load()
    model_path = config.saved_model_dir / "model.keras"

    if not model_path.exists():
        raise FileNotFoundError(f"Model bulunamadi: {model_path}. Once egitim calistirin.")

    model = tf.keras.models.load_model(model_path)
    df = load_training_data(config.use_database, config.synthetic_samples)
    prepared = prepare_data(
        df,
        feature_names=config.features,
        target=config.target,
        test_size=config.test_size,
        random_seed=config.random_seed,
    )

    y_pred = model.predict(prepared.x_test, verbose=0).flatten()
    metrics = compute_metrics(prepared.y_test, y_pred)
    logger.info("Degerlendirme metrikleri: %s", metrics)
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Kayitli modeli degerlendir")
    parser.parse_args()
    metrics = evaluate_saved_model()
    print(f"MAE={metrics['mae']}  RMSE={metrics['rmse']}  R2={metrics['r2']}")


if __name__ == "__main__":
    main()
