import pandas as pd
import pytest

from src.survival_utils import prepare_lung_data, recode_lung_event


def test_lung_event_recode_matches_r_documentation():
    result = recode_lung_event(pd.Series([1, 2, 1, 2]))
    assert result.tolist() == [0, 1, 0, 1]


def test_lung_recode_rejects_unknown_status():
    with pytest.raises(ValueError, match="inesperados"):
        recode_lung_event(pd.Series([0, 1, 2]))


def test_prepare_lung_reports_removed_rows_and_index():
    raw = pd.DataFrame(
        {
            "rownames": [1, 2],
            "time": [10, 20],
            "status": [1, 2],
            "age": [60, 70],
            "sex": [1, 2],
            "ph.ecog": [0, None],
        }
    )
    clean, report = prepare_lung_data(raw)
    assert len(clean) == 1
    assert report["linhas_removidas"] == 1
    assert report["colunas_indice_removidas"] == ["rownames"]

