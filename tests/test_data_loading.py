import sys
from types import SimpleNamespace

import pandas as pd

from src.data_loading import infer_cdc_feature_types, load_cdc_diabetes


def test_load_cdc_diabetes_uses_stratified_reproducible_sample(monkeypatch):
    features = pd.DataFrame(
        {"BMI": range(100), "Age": [1, 2, 3, 4] * 25, "HighBP": [0, 1] * 50}
    )
    targets = pd.DataFrame({"Diabetes_binary": [0] * 80 + [1] * 20})
    fake_dataset = SimpleNamespace(
        data=SimpleNamespace(features=features, targets=targets),
        metadata={"name": "fake"},
        variables=pd.DataFrame(
            {
                "name": ["HighBP", "Diabetes_binary"],
                "description": ["0 = no, 1 = yes", "0 = no diabetes, 1 = diabetes"],
            }
        ),
    )
    monkeypatch.setitem(
        sys.modules,
        "ucimlrepo",
        SimpleNamespace(fetch_ucirepo=lambda id: fake_dataset),
    )

    first, metadata = load_cdc_diabetes(sample_size=20, random_state=42)
    second, _ = load_cdc_diabetes(sample_size=20, random_state=42)

    pd.testing.assert_frame_equal(first, second)
    assert len(first) == 20
    assert first["Diabetes_binary"].sum() == 4
    assert metadata["uci_id"] == 891
    assert metadata["variables"].iloc[0]["name"] == "HighBP"


def test_infer_feature_types_keeps_target_out_of_numeric():
    frame = pd.DataFrame(columns=["BMI", "Age", "HighBP", "Diabetes_binary"])
    types = infer_cdc_feature_types(frame)
    assert types["numéricas"] == ["BMI"]
    assert "Diabetes_binary" in types["binárias"]
