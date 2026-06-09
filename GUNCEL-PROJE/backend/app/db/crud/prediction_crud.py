"""ML tahmin CRUD islemleri."""

from __future__ import annotations

from psycopg2.extensions import connection as PgConnection

from app.db.crud.base_crud import execute_returning, fetch_all, fetch_one, to_json


def create_prediction(conn: PgConnection, field_id: str, model_name: str, model_version: str, **kwargs) -> dict:
    return execute_returning(
        conn,
        """
        INSERT INTO ml_predictions
            (field_id, model_name, model_version, prediction_type,
             predicted_value, confidence, input_features)
        VALUES
            (%(field_id)s, %(model_name)s, %(model_version)s, %(prediction_type)s,
             %(predicted_value)s, %(confidence)s, %(input_features)s)
        RETURNING *
        """,
        {
            "field_id": field_id,
            "model_name": model_name,
            "model_version": model_version,
            "prediction_type": kwargs.get("prediction_type", "soil_moisture"),
            "predicted_value": kwargs["predicted_value"],
            "confidence": kwargs.get("confidence"),
            "input_features": to_json(kwargs.get("input_features")),
        },
    )


def get_predictions_by_field(
    conn: PgConnection,
    field_id: str,
    prediction_type: str | None = None,
    limit: int = 50,
) -> list[dict]:
    if prediction_type:
        return fetch_all(
            conn,
            """
            SELECT * FROM ml_predictions
            WHERE field_id = %s AND prediction_type = %s
            ORDER BY predicted_at DESC LIMIT %s
            """,
            (field_id, prediction_type, limit),
        )
    return fetch_all(
        conn,
        "SELECT * FROM ml_predictions WHERE field_id = %s ORDER BY predicted_at DESC LIMIT %s",
        (field_id, limit),
    )


def get_prediction_by_id(conn: PgConnection, prediction_id: int) -> dict | None:
    return fetch_one(conn, "SELECT * FROM ml_predictions WHERE id = %s", (prediction_id,))
