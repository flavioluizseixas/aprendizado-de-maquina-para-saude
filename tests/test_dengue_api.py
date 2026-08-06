import pandas as pd
import pytest

from src.dengue_api import missing_week_intervals, validate_infodengue


def test_validation_sorts_dates_and_preserves_missing_values():
    raw = pd.DataFrame(
        {"data_iniSE": ["2024-01-15", "2024-01-01"], "casos_est": [None, 3.0]}
    )
    result = validate_infodengue(raw)
    assert result["data_iniSE"].is_monotonic_increasing
    assert result["casos_est"].isna().sum() == 1
    assert missing_week_intervals(result).loc[0, "semanas_ausentes"] == 1


def test_validation_requires_real_target_column():
    with pytest.raises(ValueError, match="casos_est"):
        validate_infodengue(pd.DataFrame({"data_iniSE": ["2024-01-01"]}))

