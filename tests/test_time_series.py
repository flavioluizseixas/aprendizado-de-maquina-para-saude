import numpy as np
import pandas as pd

from src.time_series import make_lag_features, regression_report, temporal_train_test_split


def test_lags_and_windows_only_use_the_past():
    index = pd.date_range("2024-01-01", periods=8, freq="W-MON")
    series = pd.Series(np.arange(1, 9, dtype=float), index=index)
    features = make_lag_features(series, lags=[1, 2], rolling_windows=[3], dropna=False)
    row = features.iloc[4]
    assert row["target"] == 5
    assert row["lag_1"] == 4
    assert row["lag_2"] == 3
    assert row["média_móvel_3"] == 3


def test_changing_future_does_not_change_past_features():
    index = pd.date_range("2024-01-01", periods=10, freq="W-MON")
    original = pd.Series(np.arange(10, dtype=float), index=index)
    changed = original.copy()
    changed.iloc[-1] = 9999
    a = make_lag_features(original, lags=[1], rolling_windows=[3], dropna=False)
    b = make_lag_features(changed, lags=[1], rolling_windows=[3], dropna=False)
    pd.testing.assert_series_equal(a.iloc[-2], b.iloc[-2])


def test_temporal_split_and_metrics():
    frame = pd.DataFrame({"x": range(10)})
    train, test = temporal_train_test_split(frame, test_size=2)
    assert train["x"].max() < test["x"].min()
    report = regression_report([1, 2, 3], [1, 2, 4])
    assert set(report) == {"MAE", "RMSE", "WAPE (%)", "sMAPE (%)"}

