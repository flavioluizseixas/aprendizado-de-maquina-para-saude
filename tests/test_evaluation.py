import math

from src.evaluation import classification_report_health


def test_specificity_is_calculated_explicitly():
    report = classification_report_health(
        y_true=[0, 0, 0, 0, 1, 1],
        y_pred=[0, 0, 0, 1, 1, 0],
        y_prob=[0.1, 0.2, 0.3, 0.8, 0.9, 0.4],
    )
    assert math.isclose(report["especificidade"], 3 / 4)
    assert math.isclose(report["sensibilidade"], 1 / 2)
    assert report["falso_positivo"] == 1
    assert report["falso_negativo"] == 1
    assert "roc_auc" in report and "pr_auc" in report


def test_report_handles_absent_negative_class_without_crashing():
    report = classification_report_health([1, 1], [1, 0])
    assert math.isnan(report["especificidade"])

