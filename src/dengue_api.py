"""Cliente pequeno, validado e com cache para a API InfoDengue."""

from __future__ import annotations

from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from .config import CACHE_DIR

INFODENGUE_URL = "https://info.dengue.mat.br/api/alertcity"
DATE_COLUMN = "data_iniSE"
TARGET_COLUMNS = {"casos_est", "casos"}


def _cache_path(
    geocode: int, disease: str, start_year: int, end_year: int, cache_dir: Path
) -> Path:
    safe_disease = "".join(char for char in disease if char.isalnum() or char in "-_")
    return cache_dir / f"infodengue_{geocode}_{safe_disease}_{start_year}_{end_year}.csv"


def validate_infodengue(data: pd.DataFrame) -> pd.DataFrame:
    """Valida colunas, converte datas e preserva ausências como ausências."""

    if data.empty:
        raise ValueError("A API retornou uma tabela vazia.")
    if DATE_COLUMN not in data:
        raise ValueError(f"Resposta sem a coluna obrigatória {DATE_COLUMN!r}.")
    if not TARGET_COLUMNS.intersection(data.columns):
        raise ValueError("Resposta sem `casos_est` ou `casos`.")
    frame = data.copy()
    frame[DATE_COLUMN] = pd.to_datetime(frame[DATE_COLUMN], errors="coerce")
    if frame[DATE_COLUMN].isna().any():
        raise ValueError("Há datas inválidas em data_iniSE.")
    return frame.sort_values(DATE_COLUMN).drop_duplicates(DATE_COLUMN).reset_index(drop=True)


def missing_week_intervals(data: pd.DataFrame) -> pd.DataFrame:
    """Lista saltos maiores que sete dias, sem preencher valores."""

    dates = pd.to_datetime(data[DATE_COLUMN]).sort_values().reset_index(drop=True)
    differences = dates.diff().dt.days
    positions = differences[differences > 7].index
    return pd.DataFrame(
        {
            "após": [dates.iloc[position - 1] for position in positions],
            "antes": [dates.iloc[position] for position in positions],
            "semanas_ausentes": [int(differences.iloc[position] // 7 - 1) for position in positions],
        }
    )


def fetch_infodengue(
    geocode: int = 3303302,
    disease: str = "dengue",
    start_year: int = 2016,
    end_year: int = 2025,
    cache: bool = True,
    timeout: float = 30.0,
    cache_dir: str | Path | None = None,
    fallback_geocode: int | None = None,
    session: Any | None = None,
) -> pd.DataFrame:
    """Baixa, valida e organiza dados semanais do InfoDengue.

    O fallback só ocorre quando ``fallback_geocode`` é fornecido explicitamente.
    Erros nunca são substituídos por dados sintéticos.
    """

    if start_year > end_year:
        raise ValueError("start_year não pode ser posterior a end_year.")
    destination = Path(cache_dir) if cache_dir else CACHE_DIR
    path = _cache_path(geocode, disease, start_year, end_year, destination)
    downloaded_at = datetime.now(timezone.utc).isoformat()
    if cache and path.exists():
        frame = validate_infodengue(pd.read_csv(path))
        cache_time = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()
        frame.attrs.update({"source": "cache", "downloaded_at": cache_time})
        return frame

    client = session or requests
    params = {
        "geocode": geocode,
        "disease": disease,
        "format": "csv",
        "ew_start": 1,
        "ew_end": 53,
        "ey_start": start_year,
        "ey_end": end_year,
    }
    try:
        response = client.get(INFODENGUE_URL, params=params, timeout=timeout)
        response.raise_for_status()
        raw = pd.read_csv(StringIO(response.text))
        frame = validate_infodengue(raw)
    except (requests.RequestException, pd.errors.ParserError, ValueError) as exc:
        if fallback_geocode is not None and fallback_geocode != geocode:
            fallback = fetch_infodengue(
                fallback_geocode,
                disease,
                start_year,
                end_year,
                cache,
                timeout,
                destination,
                None,
                client,
            )
            fallback.attrs["fallback_from"] = geocode
            return fallback
        raise RuntimeError(
            "Não foi possível acessar a API do InfoDengue. Verifique conexão, "
            "período e código IBGE. Nenhum dado sintético foi utilizado."
        ) from exc
    if cache:
        destination.mkdir(parents=True, exist_ok=True)
        frame.to_csv(path, index=False)
    frame.attrs.update(
        {
            "source": INFODENGUE_URL,
            "downloaded_at": downloaded_at,
            "geocode": geocode,
            "disease": disease,
        }
    )
    return frame
