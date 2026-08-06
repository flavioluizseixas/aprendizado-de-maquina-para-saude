"""Atributos temporais sem informação futura e métricas de previsão."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import numpy as np
import pandas as pd


def make_lag_features(
    series: pd.Series,
    lags: Iterable[int] = (1, 2, 3, 4, 8, 12, 52),
    rolling_windows: Iterable[int] = (4, 8, 12),
    dropna: bool = True,
) -> pd.DataFrame:
    """Cria lags e janelas deslocadas, usando somente observações anteriores."""

    values = pd.Series(series, copy=True).astype(float).sort_index()
    if values.index.has_duplicates:
        raise ValueError("O índice temporal não pode ter datas duplicadas.")
    frame = pd.DataFrame({"target": values})
    for lag in lags:
        if lag <= 0:
            raise ValueError("Todos os lags devem ser positivos.")
        frame[f"lag_{lag}"] = values.shift(lag)
    past = values.shift(1)
    for window in rolling_windows:
        if window <= 1:
            raise ValueError("Janelas móveis devem ser maiores que 1.")
        frame[f"média_móvel_{window}"] = past.rolling(window).mean()
        frame[f"desvio_móvel_{window}"] = past.rolling(window).std()
    if isinstance(values.index, pd.DatetimeIndex):
        week = values.index.isocalendar().week.astype(int).to_numpy()
        frame["semana_seno"] = np.sin(2 * np.pi * week / 52.18)
        frame["semana_cosseno"] = np.cos(2 * np.pi * week / 52.18)
    frame["tendência"] = np.arange(len(frame), dtype=float)
    return frame.dropna() if dropna else frame


def temporal_train_test_split(
    data: pd.DataFrame,
    test_size: int | float = 0.2,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Separa início e fim sem embaralhar."""

    if isinstance(test_size, float):
        if not 0 < test_size < 1:
            raise ValueError("test_size fracionário deve estar entre 0 e 1.")
        n_test = int(np.ceil(len(data) * test_size))
    else:
        n_test = int(test_size)
    if n_test <= 0 or n_test >= len(data):
        raise ValueError("test_size deve deixar observações em treino e teste.")
    return data.iloc[:-n_test].copy(), data.iloc[-n_test:].copy()


def regression_report(y_true: Any, y_pred: Any) -> dict[str, float]:
    """Calcula MAE, RMSE, WAPE e sMAPE com denominadores protegidos."""

    truth = np.asarray(y_true, dtype=float)
    prediction = np.asarray(y_pred, dtype=float)
    error = truth - prediction
    mae = float(np.mean(np.abs(error)))
    rmse = float(np.sqrt(np.mean(error**2)))
    total = float(np.sum(np.abs(truth)))
    wape = float(np.sum(np.abs(error)) / total * 100) if total else float("nan")
    denominator = np.abs(truth) + np.abs(prediction)
    smape_terms = np.divide(
        2 * np.abs(error), denominator, out=np.zeros_like(error), where=denominator != 0
    )
    return {"MAE": mae, "RMSE": rmse, "WAPE (%)": wape, "sMAPE (%)": float(smape_terms.mean() * 100)}

