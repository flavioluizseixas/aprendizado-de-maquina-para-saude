"""Validação manual e curta das fontes externas; exige acesso à internet."""

from __future__ import annotations

import argparse
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

from src.data_loading import ensure_medmnist_download, load_cdc_diabetes
from src.dengue_api import fetch_infodengue
from src.survival_utils import prepare_lung_data

LUNG_URL = "https://vincentarelbundock.github.io/Rdatasets/csv/survival/cancer.csv"


def main(include_medmnist: bool = False) -> None:
    cdc, metadata = load_cdc_diabetes(sample_size=200)
    assert len(cdc) == 200 and metadata["uci_id"] == 891
    print("UCI CDC: OK")

    response = requests.get(LUNG_URL, timeout=30)
    response.raise_for_status()
    lung_raw = pd.read_csv(StringIO(response.text))
    if "time" not in lung_raw:
        print("Rdatasets resposta:", response.url, response.headers.get("content-type"))
        print(response.text[:300])
    lung, report = prepare_lung_data(lung_raw)
    assert len(lung) and report["eventos"] > 0
    print("Rdatasets lung: OK")

    dengue = fetch_infodengue(
        geocode=3303302,
        disease="dengue",
        start_year=2023,
        end_year=2024,
        cache=False,
    )
    assert len(dengue) and dengue["data_iniSE"].is_monotonic_increasing
    print("InfoDengue: OK")

    if include_medmnist:
        from medmnist import PneumoniaMNIST

        root = Path("data/cache/medmnist")
        ensure_medmnist_download("pneumoniamnist", 64, root)
        validation = PneumoniaMNIST(split="val", download=False, size=64, root=str(root))
        assert len(validation) and validation.imgs.shape[1:3] == (64, 64)
        print("PneumoniaMNIST 64: OK")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--medmnist", action="store_true")
    args = parser.parse_args()
    main(include_medmnist=args.medmnist)
