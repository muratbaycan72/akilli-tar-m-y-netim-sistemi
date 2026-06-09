"""Model egitim scripti."""

from __future__ import annotations

import argparse
import logging
from datetime import datetime, timezone

import numpy as np

from src.config import TrainingConfig
from src.data.loader import load_training_data
from src.data.preprocessor import prepare_data
from src.models.soil_moisture_regressor import build_soil_moisture_model, train_model
from src.utils.metrics import compute_metrics, metrics_meet_threshold
from src.utils.model_io import save_artifacts

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def run_training(config: TrainingConfig | None = None, verbose: int = 1) -> dict:
    config = config or TrainingConfig.load()
    logger.info("Veri yukleniyor (use_database=%s)...", config.use_database)
    df = load_training_data(config.use_database, config.synthetic_samples)
    logger.info("Veri seti: %d ornek", len(df))

    prepared = prepare_data(
        df,
        feature_names=config.features,
        target=config.target,
        test_size=config.test_size,
        random_seed=config.random_seed,
    )

    model = build_soil_moisture_model(
        n_features=len(config.features),
        learning_rate=config.learning_rate,
    )
    logger.info("Model egitimi basliyor (%d epoch)...", config.epochs)
    history = train_model(
        model,
        prepared.x_train,
        prepared.y_train,
        epochs=config.epochs,
        batch_size=config.batch_size,
        validation_split=config.validation_split,
        verbose=verbose,
    )

    y_pred = model.predict(prepared.x_test, verbose=0).flatten()
    metrics = compute_metrics(prepared.y_test, y_pred)
    logger.info("Test metrikleri: %s", metrics)

    metadata = {
        "model_name": config.model_name,
        "model_version": config.model_version,
        "feature_names": config.features,
        "target": config.target,
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "training_samples": len(prepared.x_train),
        "test_samples": len(prepared.x_test),
        "metrics": metrics,
        "epochs": config.epochs,
        "passed_quality_check": metrics_meet_threshold(metrics),
        "final_loss": float(history.history["loss"][-1]),
        "final_val_loss": float(history.history.get("val_loss", [0])[-1]),
    }

    save_artifacts(config.saved_model_dir, model, prepared.scaler, metadata)
    logger.info("Model kaydedildi: %s", config.saved_model_dir)
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Toprak nemi regresyon modeli egit")
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--use-db", action="store_true", help="PostgreSQL'den veri cek")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    config = TrainingConfig.load()
    if args.epochs:
        config = TrainingConfig(
            **{**config.__dict__, "epochs": args.epochs}
        )
    if args.use_db:
        config = TrainingConfig(
            **{**config.__dict__, "use_database": True}
        )

    result = run_training(config, verbose=0 if args.quiet else 1)
    print(f"\nEgitim tamamlandi. R2={result['metrics']['r2']}, MAE={result['metrics']['mae']}")


if __name__ == "__main__":
    main()
