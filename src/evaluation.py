"""Métricas de classificação com definições explícitas."""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    PrecisionRecallDisplay,
    RocCurveDisplay,
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def _safe_ratio(numerator: float, denominator: float) -> float:
    return float(numerator / denominator) if denominator else float("nan")


def classification_report_health(
    y_true: Any,
    y_pred: Any,
    y_prob: Any | None = None,
) -> dict[str, float | int]:
    """Calcula métricas binárias, incluindo especificidade explícita."""

    y_true_array = np.asarray(y_true).ravel()
    y_pred_array = np.asarray(y_pred).ravel()
    tn, fp, fn, tp = confusion_matrix(
        y_true_array, y_pred_array, labels=[0, 1]
    ).ravel()
    report: dict[str, float | int] = {
        "n": len(y_true_array),
        "verdadeiro_negativo": int(tn),
        "falso_positivo": int(fp),
        "falso_negativo": int(fn),
        "verdadeiro_positivo": int(tp),
        "acurácia": accuracy_score(y_true_array, y_pred_array),
        "acurácia_balanceada": balanced_accuracy_score(y_true_array, y_pred_array),
        "sensibilidade": recall_score(y_true_array, y_pred_array, zero_division=0),
        "especificidade": _safe_ratio(tn, tn + fp),
        "precisão": precision_score(y_true_array, y_pred_array, zero_division=0),
        "f1": f1_score(y_true_array, y_pred_array, zero_division=0),
    }
    if y_prob is not None:
        probabilities = np.asarray(y_prob).ravel()
        report["roc_auc"] = roc_auc_score(y_true_array, probabilities)
        report["pr_auc"] = average_precision_score(y_true_array, probabilities)
    return report


def plot_classification_curves(y_true: Any, y_prob: Any) -> plt.Figure:
    """Desenha curvas ROC e precisão-recall lado a lado."""

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    RocCurveDisplay.from_predictions(y_true, y_prob, ax=axes[0])
    axes[0].plot([0, 1], [0, 1], "--", color="grey", label="Aleatório")
    axes[0].set_title("Curva ROC")
    PrecisionRecallDisplay.from_predictions(y_true, y_prob, ax=axes[1])
    baseline = float(np.mean(np.asarray(y_true)))
    axes[1].axhline(baseline, linestyle="--", color="grey", label="Prevalência")
    axes[1].set_title("Curva precisão-recall")
    axes[1].legend()
    fig.tight_layout()
    return fig


def report_frame(report: dict[str, float | int]) -> pd.DataFrame:
    """Formata um relatório como tabela de uma coluna."""

    return pd.DataFrame.from_dict(report, orient="index", columns=["valor"])

