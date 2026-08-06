import numpy as np
import pytest

from src.gradcam import make_gradcam_heatmap, show_gradcam

tf = pytest.importorskip("tensorflow")


def test_gradcam_supports_keras_sequential_and_binary_output():
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input((8, 8, 1)),
            tf.keras.layers.Conv2D(2, 3, activation="relu", name="conv"),
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )
    image = np.random.default_rng(42).random((8, 8, 1), dtype=np.float32)
    model(image[None, ...])
    heatmap = make_gradcam_heatmap(image, model, "conv", class_index=1)
    figure, shown = show_gradcam(model, image, "conv", class_index=1)
    assert heatmap.shape == (6, 6)
    assert np.isfinite(heatmap).all() and heatmap.min() >= 0 and heatmap.max() <= 1
    assert shown.shape == heatmap.shape
    assert len(figure.axes) == 3
