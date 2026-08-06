"""Configuração compartilhada e utilitários de reprodutibilidade."""

from __future__ import annotations

import importlib.metadata
import os
import random
import sys
from pathlib import Path

import numpy as np

RANDOM_STATE = 42
FAST_MODE = True
REPO = "flavioluizseixas/aprendizado-de-maquina-para-saude"
REPO_URL = f"https://github.com/{REPO}.git"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = PROJECT_ROOT / "data" / "cache"

EDUCATIONAL_NOTICE = (
    "Este material tem finalidade exclusivamente educacional. Os resultados não "
    "devem ser usados para diagnóstico, prognóstico, tratamento, gestão assistencial "
    "ou decisão de saúde pública sem validação adequada, análise de contexto e "
    "supervisão de profissionais qualificados."
)


def seed_everything(seed: int = RANDOM_STATE) -> None:
    """Fixa sementes das bibliotecas disponíveis sem exigir TensorFlow."""

    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    try:
        if "tensorflow" not in sys.modules:
            return
        import tensorflow as tf

        tf.keras.utils.set_random_seed(seed)
        try:
            tf.config.experimental.enable_op_determinism()
        except (AttributeError, RuntimeError):
            pass
    except ImportError:
        pass


def running_in_colab() -> bool:
    """Informa se o código está em um runtime do Google Colab."""

    return "google.colab" in sys.modules


def library_versions(packages: tuple[str, ...] | None = None) -> dict[str, str]:
    """Retorna versões instaladas para o registro de reprodutibilidade."""

    packages = packages or (
        "numpy",
        "pandas",
        "scikit-learn",
        "matplotlib",
        "seaborn",
    )
    versions = {"python": sys.version.split()[0]}
    for package in packages:
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = "não instalado"
    return versions
