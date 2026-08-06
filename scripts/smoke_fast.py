"""Smoke test rápido dos fluxos locais, sem rede nem treinamento de imagens."""

from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification

from src.clustering import evaluate_kmeans_range
from src.evaluation import classification_report_health
from src.model_selection import compare_classifiers, get_default_classifiers
from src.reinforcement_env import DengueInventoryEnv, train_q_learning
from src.time_series import make_lag_features, temporal_train_test_split


def main() -> None:
    X, y = make_classification(n_samples=120, n_features=7, random_state=42)
    models = get_default_classifiers()
    models["Random forest"].set_params(model__n_jobs=1)
    board = compare_classifiers(X, y, models=models, cv=2, n_jobs=1)
    assert len(board) == 4 and board["roc_auc"].notna().all()
    assert classification_report_health(y, y)["especificidade"] == 1.0

    cluster_result = evaluate_kmeans_range(X[:60], k_values=[2, 3], silhouette_sample_size=None)
    assert cluster_result.shape == (2, 3)

    env = DengueInventoryEnv(np.tile([4, 8, 12, 8], 8))
    q_table, history = train_q_learning(env, episodes=10)
    assert q_table.shape == (9, 3) and len(history) == 10

    index = pd.date_range("2022-01-03", periods=80, freq="W-MON")
    features = make_lag_features(pd.Series(np.arange(80.0), index=index))
    train, test = temporal_train_test_split(features, 10)
    assert train.index.max() < test.index.min()
    print("OK: fluxos rápidos de classificação, clustering, reforço e tempo.")


if __name__ == "__main__":
    main()
