"""Preparação explícita da base NCCTG Lung para análise de sobrevivência."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import numpy as np
import pandas as pd


def recode_lung_event(status: pd.Series) -> pd.Series:
    """Converte status do R (1=censurado, 2=óbito) em evento binário."""

    observed = set(status.dropna().astype(int).unique())
    if not observed.issubset({1, 2}):
        raise ValueError(f"status contém códigos inesperados: {sorted(observed)}")
    event = status.map({1: 0, 2: 1})
    return event.astype("Int64")


def prepare_lung_data(
    data: pd.DataFrame,
    required_columns: Iterable[str] = ("time", "status", "age", "sex", "ph.ecog"),
    missing: str = "drop",
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Remove índice do Rdatasets, recodifica evento e trata ausências."""

    frame = data.copy()
    index_columns = [column for column in ("rownames", "Unnamed: 0") if column in frame]
    frame = frame.drop(columns=index_columns)
    required = list(required_columns)
    absent = set(required) - set(frame.columns)
    if absent:
        raise ValueError(f"Colunas obrigatórias ausentes: {sorted(absent)}")
    frame["event"] = recode_lung_event(frame["status"])
    frame["sex_label"] = frame["sex"].map({1: "Masculino", 2: "Feminino"})
    frame["sex_female"] = frame["sex"].map({1: 0, 2: 1})
    before = len(frame)
    model_columns = ["time", "event", "age", "sex", "sex_female", "ph.ecog"]
    if missing == "drop":
        frame = frame.dropna(subset=model_columns).copy()
    else:
        raise ValueError("A estratégia suportada é missing='drop', sempre explícita.")
    frame["event"] = frame["event"].astype(int)
    report = {
        "linhas_originais": before,
        "linhas_removidas": before - len(frame),
        "linhas_finais": len(frame),
        "colunas_indice_removidas": index_columns,
        "estratégia_ausências": "remoção completa nas variáveis do modelo",
        "censurados": int((frame["event"] == 0).sum()),
        "eventos": int((frame["event"] == 1).sum()),
    }
    return frame.reset_index(drop=True), report


def hazard_ratio_table(summary: pd.DataFrame) -> pd.DataFrame:
    """Extrai HR e intervalo de confiança de um resumo do lifelines."""

    candidates = {
        "coef": "coeficiente",
        "exp(coef)": "HR",
        "exp(coef) lower 95%": "IC 95% inferior",
        "exp(coef) upper 95%": "IC 95% superior",
        "p": "p-valor",
    }
    present = [column for column in candidates if column in summary]
    return summary[present].rename(columns=candidates)

