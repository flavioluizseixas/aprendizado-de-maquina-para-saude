"""Grad-CAM para classificadores Keras binários."""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def make_gradcam_heatmap(
    image: np.ndarray,
    model: Any,
    last_conv_layer_name: str,
    class_index: int = 1,
) -> np.ndarray:
    """Produz um mapa Grad-CAM normalizado para uma única imagem."""

    try:
        import tensorflow as tf
    except ImportError as exc:
        raise ImportError("Grad-CAM requer TensorFlow 2.16 ou superior.") from exc

    image_batch = np.asarray(image, dtype="float32")
    if image_batch.ndim == 3:
        image_batch = image_batch[None, ...]
    conv_layer = model.get_layer(last_conv_layer_name)
    if not model.inputs or not model.outputs:
        model(image_batch, training=False)
    grad_model = tf.keras.Model(
        inputs=model.inputs[0], outputs=[conv_layer.output, model.outputs[0]]
    )
    with tf.GradientTape() as tape:
        conv_output, predictions = grad_model(image_batch, training=False)
        probability = predictions[:, 0]
        score = probability if class_index == 1 else 1.0 - probability
    gradients = tape.gradient(score, conv_output)
    weights = tf.reduce_mean(gradients, axis=(0, 1, 2))
    heatmap = tf.reduce_sum(conv_output[0] * weights, axis=-1)
    heatmap = tf.maximum(heatmap, 0)
    maximum = tf.reduce_max(heatmap)
    heatmap = tf.where(maximum > 0, heatmap / maximum, heatmap)
    return heatmap.numpy()


def show_gradcam(
    model: Any,
    image: np.ndarray,
    last_conv_layer: str,
    class_index: int = 1,
    alpha: float = 0.45,
) -> tuple[plt.Figure, np.ndarray]:
    """Mostra imagem, mapa e sobreposição; retorna a figura e o mapa."""

    heatmap = make_gradcam_heatmap(image, model, last_conv_layer, class_index)
    base = np.squeeze(np.asarray(image))
    target_size = (int(base.shape[1]), int(base.shape[0]))
    overlay_heatmap = np.asarray(
        Image.fromarray(np.uint8(255 * heatmap)).resize(target_size, Image.Resampling.BILINEAR),
        dtype=float,
    ) / 255.0
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.2))
    axes[0].imshow(base, cmap="gray")
    axes[0].set_title("Imagem")
    axes[1].imshow(heatmap, cmap="jet")
    axes[1].set_title("Grad-CAM")
    axes[2].imshow(base, cmap="gray")
    axes[2].imshow(overlay_heatmap, cmap="jet", alpha=alpha)
    axes[2].set_title("Sobreposição")
    for axis in axes:
        axis.axis("off")
    fig.tight_layout()
    return fig, heatmap
