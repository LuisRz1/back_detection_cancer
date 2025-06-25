import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
import cv2
from PIL import Image
import io

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    return np.array(img)

def generate_gradcam(model, img_array: np.ndarray, layer_name: str = "conv5_block3_out"):
    # Preprocess for model
    x = img_array / 255.0
    x = np.expand_dims(x, axis=0)

    grad_model = Model(
        [model.inputs], [model.get_layer(layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(x)
        class_idx = tf.argmax(predictions[0])
        loss = predictions[:, class_idx]

    grads = tape.gradient(loss, conv_outputs)[0]
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1))
    conv_outputs = conv_outputs[0]

    heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)
    heatmap = np.maximum(heatmap, 0)
    heatmap /= tf.math.reduce_max(heatmap)
    heatmap = cv2.resize(heatmap.numpy(), (224, 224))
    return heatmap
