"""Carregamento e preparação das bases tabulares públicas."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from sklearn.model_selection import train_test_split

BINARY_COLUMNS = {
    "HighBP", "HighChol", "CholCheck", "Smoker", "Stroke",
    "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies",
    "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost", "DiffWalk",
    "Sex", "Diabetes_binary",
}
ORDINAL_COLUMNS = {"GenHlth", "Age", "Education", "Income"}


def infer_cdc_feature_types(data: pd.DataFrame) -> dict[str, list[str]]:
    """Agrupa colunas conhecidas em binárias, ordinais e numéricas."""

    columns = set(data.columns)
    binary = sorted(columns & BINARY_COLUMNS)
    ordinal = sorted(columns & ORDINAL_COLUMNS)
    numerical = sorted(columns - set(binary) - set(ordinal))
    return {"binárias": binary, "ordinais": ordinal, "numéricas": numerical}


def _sample_rows(
    data: pd.DataFrame,
    target: str,
    sample_size: int | None,
    random_state: int,
    stratify: bool,
) -> pd.DataFrame:
    """Seleciona uma amostra reproduzível sem alterar a distribuição deliberadamente."""

    if sample_size is None or sample_size >= len(data):
        return data.reset_index(drop=True)
    if sample_size <= 0:
        raise ValueError("sample_size deve ser positivo ou None.")
    stratification = data[target] if stratify and data[target].nunique() > 1 else None
    sampled, _ = train_test_split(
        data,
        train_size=sample_size,
        random_state=random_state,
        stratify=stratification,
    )
    return sampled.reset_index(drop=True)


def load_cdc_diabetes(
    sample_size: int | None = None,
    random_state: int = 42,
    stratify: bool = True,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Baixa a base UCI 891, une atributos e alvo e amostra se solicitado.

    Returns:
        Uma dupla ``(dados, metadados)``. Nenhuma linha é imputada ou removida.
    """

    try:
        from ucimlrepo import fetch_ucirepo
    except ImportError as exc:
        raise ImportError(
            "Instale ucimlrepo com `python -m pip install 'ucimlrepo>=0.0.7,<1'`."
        ) from exc

    dataset = fetch_ucirepo(id=891)
    features = dataset.data.features.copy()
    targets = dataset.data.targets.copy()
    if isinstance(targets, pd.Series):
        targets = targets.to_frame()
    if targets.shape[1] != 1:
        raise ValueError("A base UCI 891 deveria ter exatamente um alvo.")
    target_name = str(targets.columns[0])
    if target_name != "Diabetes_binary":
        targets = targets.rename(columns={target_name: "Diabetes_binary"})
        target_name = "Diabetes_binary"
    data = pd.concat(
        [features.reset_index(drop=True), targets.reset_index(drop=True)], axis=1
    )
    data = _sample_rows(data, target_name, sample_size, random_state, stratify)
    metadata = dict(getattr(dataset, "metadata", {}) or {})
    metadata.update(
        {
            "uci_id": 891,
            "target": target_name,
            "sample_size": len(data),
            "feature_types": infer_cdc_feature_types(data),
        }
    )
    return data, metadata


def ensure_medmnist_download(
    data_flag: str = "pneumoniamnist",
    size: int = 64,
    root: str | Path = "data/cache/medmnist",
    timeout: float = 120.0,
) -> Path:
    """Baixa um NPZ oficial do MedMNIST e valida seu checksum MD5.

    A rotina evita depender do downloader do torchvision, mas usa URL e checksum
    publicados pela versão instalada do próprio MedMNIST.
    """

    try:
        from medmnist import INFO
    except ImportError as exc:
        raise ImportError("Instale medmnist com `python -m pip install 'medmnist>=3,<4'`.") from exc
    if data_flag not in INFO:
        raise ValueError(f"data_flag desconhecido: {data_flag}")
    info = INFO[data_flag]
    suffix = "" if size == 28 else f"_{size}"
    url_key = "url" if size == 28 else f"url_{size}"
    md5_key = "MD5" if size == 28 else f"MD5_{size}"
    if url_key not in info or md5_key not in info:
        raise ValueError(f"Tamanho {size} não publicado para {data_flag}.")
    destination = Path(root)
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / f"{data_flag}{suffix}.npz"
    expected = info[md5_key]

    def checksum(file_path: Path) -> str:
        digest = hashlib.md5()  # nosec B324 — checksum de integridade publicado
        with file_path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    if path.exists() and checksum(path) == expected:
        print(f"MedMNIST: usando arquivo validado em {path}")
        return path
    temporary = path.with_suffix(".npz.part")
    try:
        with requests.get(info[url_key], stream=True, timeout=timeout) as response:
            response.raise_for_status()
            with temporary.open("wb") as output:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        output.write(chunk)
        if checksum(temporary) != expected:
            raise RuntimeError("Checksum MD5 do arquivo MedMNIST não confere.")
        temporary.replace(path)
    except (requests.RequestException, OSError) as exc:
        raise RuntimeError(
            "Não foi possível baixar o MedMNIST oficial. Verifique a conexão e o "
            "espaço disponível; nenhum dado alternativo foi utilizado."
        ) from exc
    print(f"MedMNIST: download oficial validado em {path}")
    return path
