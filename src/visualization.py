"""Visualizações pequenas e consistentes para os exercícios."""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .data_loading import BINARY_COLUMNS, ORDINAL_COLUMNS


def plot_variable(
    data: pd.DataFrame,
    column: str,
    target: str | None = None,
    kind: str = "auto",
) -> Any:
    """Escolhe histograma/boxplot ou barras conforme o tipo do atributo."""

    if column not in data:
        raise KeyError(f"Coluna ausente: {column}")
    if target is not None and target not in data:
        raise KeyError(f"Alvo ausente: {target}")
    if kind == "auto":
        kind = "categorical" if column in BINARY_COLUMNS | ORDINAL_COLUMNS else "numeric"
    hue = target if target and target != column else None

    if kind == "numeric":
        fig, axes = plt.subplots(1, 2, figsize=(11, 4))
        sns.histplot(data=data, x=column, hue=hue, kde=True, ax=axes[0])
        if hue:
            sns.boxplot(data=data, x=hue, y=column, ax=axes[1])
        else:
            sns.boxplot(data=data, x=column, ax=axes[1])
        axes[0].set_title(f"Distribuição de {column} (n={len(data):,})")
        axes[1].set_title(f"Resumo de {column}")
    elif kind in {"categorical", "ordinal"}:
        order = sorted(data[column].dropna().unique())
        if hue:
            proportions = pd.crosstab(data[column], data[hue], normalize="index") * 100
            ax = proportions.reindex(order).plot(kind="bar", figsize=(8, 4))
            ax.set_ylabel("Percentual dentro da categoria (%)")
            ax.legend(title=hue)
        else:
            percentages = data[column].value_counts(normalize=True).reindex(order) * 100
            ax = percentages.plot(kind="bar", figsize=(8, 4))
            ax.set_ylabel("Percentual (%)")
        ax.set_title(f"Distribuição de {column} (n={len(data):,})")
        ax.set_xlabel(column)
        fig = ax.figure
    else:
        raise ValueError("kind deve ser 'auto', 'numeric', 'categorical' ou 'ordinal'.")
    fig.tight_layout()
    return fig
