import inspect

from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier

from src.model_selection import compare_classifiers, tune_classifier


def test_leaderboard_has_required_metrics_and_records_failures():
    X, y = make_classification(n_samples=100, n_features=6, random_state=42)
    models = {"Árvore pequena": DecisionTreeClassifier(max_depth=2, random_state=42)}
    leaderboard = compare_classifiers(X, y, models=models, cv=2, n_jobs=1)
    required = {
        "model",
        "status",
        "fit_time",
        "roc_auc",
        "f1",
        "recall",
        "precision",
        "balanced_accuracy",
    }
    assert required.issubset(leaderboard.columns)
    assert leaderboard.loc[0, "status"] == "ok"


def test_tuning_interface_cannot_receive_test_data():
    signature = inspect.signature(tune_classifier)
    assert "X_test" not in signature.parameters
    assert "y_test" not in signature.parameters


def test_tuning_returns_fitted_search():
    X, y = make_classification(n_samples=80, n_features=5, random_state=42)
    best, search = tune_classifier(
        "Árvore de decisão", X, y, cv=2, n_iter=1, n_jobs=1
    )
    assert hasattr(best, "predict")
    assert search.best_params_

