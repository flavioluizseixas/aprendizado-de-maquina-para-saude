"""Avaliação de K-means e escolha transparente do número de grupos."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def evaluate_kmeans_range(
    X_scaled: np.ndarray,
    k_values: Iterable[int] = range(2, 9),
    random_state: int = 42,
    silhouette_sample_size: int | None = 10_000,
) -> pd.DataFrame:
    """Calcula inércia e silhouette para cada ``k`` solicitado."""

    X_array = np.asarray(X_scaled)
    rows = []
    for k in k_values:
        if k < 2 or k >= len(X_array):
            raise ValueError("Cada k deve estar entre 2 e n_observações - 1.")
        model = KMeans(n_clusters=k, n_init=10, random_state=random_state)
        labels = model.fit_predict(X_array)
        sample_size = None
        if silhouette_sample_size and len(X_array) > silhouette_sample_size:
            sample_size = silhouette_sample_size
        score = silhouette_score(
            X_array, labels, sample_size=sample_size, random_state=random_state
        )
        rows.append({"k": k, "inércia": model.inertia_, "silhouette": score})
    return pd.DataFrame(rows)


def choose_k(results: pd.DataFrame) -> tuple[int, str]:
    """Usa KneeLocator e recorre ao maior silhouette se não houver cotovelo."""

    try:
        from kneed import KneeLocator

        knee = KneeLocator(
            results["k"], results["inércia"], curve="convex", direction="decreasing"
        ).knee
    except ImportError:
        knee = None
    if knee is not None:
        return int(knee), "cotovelo detectado por KneeLocator"
    best = int(results.loc[results["silhouette"].idxmax(), "k"])
    return best, "fallback transparente: maior silhouette"

