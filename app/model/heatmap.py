import numpy as np
import tensorflow as tf
# from tensorflow.keras.models import Model
import cv2
from PIL import Image
import io

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    return np.array(img)

def generate_pseudo_heatmap(img_array: np.ndarray) -> np.ndarray:
    img_resized = cv2.resize(img_array, (224, 224))
    gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)
    heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    superpuesto = cv2.addWeighted(img_resized, 0.6, heatmap, 0.4, 0)
    return superpuesto
