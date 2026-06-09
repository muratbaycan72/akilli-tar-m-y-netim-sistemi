"""ML yapilandirma yukleyici."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "config" / "training_config.yaml"


@dataclass
class TrainingConfig:
    model_name: str
    model_version: str
    features: list[str]
    target: str
    epochs: int
    batch_size: int
    learning_rate: float
    validation_split: float
    random_seed: int
    synthetic_samples: int
    test_size: float
    use_database: bool
    saved_model_dir: Path
    metrics: list[str] = field(default_factory=lambda: ["mae", "rmse", "r2"])

    @classmethod
    def load(cls, path: Path | None = None) -> TrainingConfig:
        with open(path or CONFIG_PATH, encoding="utf-8") as file:
            raw = yaml.safe_load(file)

        paths = raw["paths"]
        saved_dir = ROOT_DIR / paths["saved_model_dir"]
        training = raw["training"]
        data = raw["data"]

        return cls(
            model_name=raw["model"]["name"],
            model_version=raw["model"]["version"],
            features=raw["features"],
            target=raw["target"],
            epochs=training["epochs"],
            batch_size=training["batch_size"],
            learning_rate=training["learning_rate"],
            validation_split=training["validation_split"],
            random_seed=training["random_seed"],
            synthetic_samples=data["synthetic_samples"],
            test_size=data["test_size"],
            use_database=data["use_database"],
            saved_model_dir=saved_dir,
            metrics=raw["evaluation"]["metrics"],
        )
