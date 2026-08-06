"""Comparação low-code e ajuste transparente de classificadores."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

METRICS = ("roc_auc", "f1", "recall", "precision", "balanced_accuracy")


def _pipeline(model: BaseEstimator, scale: bool = False) -> Pipeline:
    steps: list[tuple[str, Any]] = [("imputer", SimpleImputer(strategy="median"))]
    if scale:
        steps.append(("scaler", StandardScaler()))
    steps.append(("model", model))
    return Pipeline(steps)


def get_default_classifiers(random_state: int = 42) -> dict[str, Pipeline]:
    """Cria os quatro modelos do PRD, com pré-processamento no pipeline."""

    return {
        "Regressão logística": _pipeline(
            LogisticRegression(
                max_iter=1_000, class_weight="balanced", random_state=random_state
            ),
            scale=True,
        ),
        "Árvore de decisão": _pipeline(
            DecisionTreeClassifier(class_weight="balanced", random_state=random_state)
        ),
        "Random forest": _pipeline(
            RandomForestClassifier(
                n_estimators=200,
                class_weight="balanced_subsample",
                n_jobs=-1,
                random_state=random_state,
            )
        ),
        "Hist gradient boosting": _pipeline(
            HistGradientBoostingClassifier(random_state=random_state)
        ),
    }


def _requested_metrics(scoring: str | Sequence[str]) -> list[str]:
    requested = [scoring] if isinstance(scoring, str) else list(scoring)
    unknown = set(requested) - set(METRICS)
    if unknown:
        raise ValueError(f"Métricas não suportadas: {sorted(unknown)}")
    return list(dict.fromkeys([*requested, *METRICS]))


def compare_classifiers(
    X: Any,
    y: Any,
    models: Mapping[str, BaseEstimator] | None = None,
    cv: int = 5,
    scoring: str | Sequence[str] = "roc_auc",
    random_state: int = 42,
    n_jobs: int | None = -1,
) -> pd.DataFrame:
    """Compara modelos com exatamente as mesmas partições estratificadas.

    Falhas ficam registradas na coluna ``status`` e não interrompem os demais
    modelos. O método recebe apenas dados de treino; não existe argumento de teste.
    """

    models = models or get_default_classifiers(random_state)
    metrics = _requested_metrics(scoring)
    splitter = StratifiedKFold(n_splits=cv, shuffle=True, random_state=random_state)
    splits = list(splitter.split(X, y))
    rows: list[dict[str, Any]] = []
    for name, estimator in models.items():
        row: dict[str, Any] = {"model": name, "status": "ok"}
        try:
            result = cross_validate(
                estimator,
                X,
                y,
                cv=splits,
                scoring=metrics,
                n_jobs=n_jobs,
                error_score="raise",
                return_train_score=False,
            )
            row["fit_time"] = float(np.mean(result["fit_time"]))
            for metric in METRICS:
                values = result[f"test_{metric}"]
                row[metric] = float(np.mean(values))
                row[f"{metric}_std"] = float(np.std(values, ddof=1))
        except Exception as exc:  # mantém o leaderboard útil para os outros modelos
            row.update({metric: np.nan for metric in METRICS})
            row["fit_time"] = np.nan
            row["status"] = f"falhou: {type(exc).__name__}: {exc}"
        rows.append(row)
    sort_metric = scoring if isinstance(scoring, str) else list(scoring)[0]
    return (
        pd.DataFrame(rows)
        .sort_values(sort_metric, ascending=False, na_position="last")
        .reset_index(drop=True)
    )


def _parameter_spaces() -> dict[str, dict[str, list[Any]]]:
    return {
        "Regressão logística": {
            "model__C": np.logspace(-3, 2, 20).tolist(),
            "model__solver": ["lbfgs", "liblinear"],
        },
        "Árvore de decisão": {
            "model__max_depth": [3, 5, 8, 12, None],
            "model__min_samples_leaf": [1, 2, 5, 10, 20],
            "model__criterion": ["gini", "entropy", "log_loss"],
        },
        "Random forest": {
            "model__n_estimators": [100, 200, 300, 500],
            "model__max_depth": [5, 10, 20, None],
            "model__min_samples_leaf": [1, 2, 5, 10],
            "model__max_features": ["sqrt", "log2", 0.7],
        },
        "Hist gradient boosting": {
            "model__learning_rate": [0.03, 0.05, 0.1, 0.2],
            "model__max_iter": [100, 200, 300],
            "model__max_leaf_nodes": [7, 15, 31, 63],
            "model__l2_regularization": [0.0, 0.1, 1.0, 10.0],
        },
    }


def tune_classifier(
    model_name: str,
    X: Any,
    y: Any,
    cv: int = 5,
    n_iter: int = 20,
    scoring: str = "roc_auc",
    random_state: int = 42,
    n_jobs: int | None = -1,
) -> tuple[BaseEstimator, RandomizedSearchCV]:
    """Executa RandomizedSearchCV somente sobre os dados recebidos."""

    models = get_default_classifiers(random_state)
    spaces = _parameter_spaces()
    if model_name not in models:
        raise ValueError(f"Modelo desconhecido: {model_name}. Opções: {list(models)}")
    if n_iter <= 0:
        raise ValueError("n_iter deve ser positivo.")
    splitter = StratifiedKFold(n_splits=cv, shuffle=True, random_state=random_state)
    search = RandomizedSearchCV(
        estimator=models[model_name],
        param_distributions=spaces[model_name],
        n_iter=n_iter,
        scoring=scoring,
        cv=splitter,
        random_state=random_state,
        n_jobs=n_jobs,
        refit=True,
        return_train_score=False,
        error_score="raise",
    )
    search.fit(X, y)
    return search.best_estimator_, search


def tuning_results_frame(search: RandomizedSearchCV, top: int = 10) -> pd.DataFrame:
    """Resume as melhores configurações sem expor a tabela interna completa."""

    columns = ["rank_test_score", "mean_test_score", "std_test_score", "params"]
    return (
        pd.DataFrame(search.cv_results_)[columns]
        .sort_values("rank_test_score")
        .head(top)
        .reset_index(drop=True)
    )

