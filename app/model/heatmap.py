import numpy as np
import tensorflow as tf
# from tensorflow.keras.models import Model
import cv2
from PIL import Image
import io

# Preprocesa la imagen a un array RGB de tamaño 224x224
def preprocess_image(image_bytes: bytes) -> np.ndarray:
    try:
        # Verificar que los bytes no estén vacíos
        if not image_bytes:
            raise ValueError("No se proporcionó imagen.")

        # Abrir imagen desde bytes y convertir a RGB
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Redimensionar a 224x224 (tamaño esperado por el modelo)
        image = image.resize((224, 224))

        # Convertir a array numpy
        return np.array(image)

    except Exception as e:
        raise ValueError(f"Error al procesar la imagen: {str(e)}")

# Genera un mapa de calor falso (pseudo-heatmap) a partir de una imagen
def generate_pseudo_heatmap(img_array: np.ndarray) -> np.ndarray:
    try:
        # Validar que sea un array válido con 3 canales
        if img_array.ndim != 3 or img_array.shape[2] != 3:
            raise ValueError("La imagen debe tener 3 canales (RGB)")

        # Redimensionar si no es 224x224
        if img_array.shape[:2] != (224, 224):
            img_array = cv2.resize(img_array, (224, 224))

        # Convertir a escala de grises
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        # Generar heatmap tipo JET
        heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

        # Superponer heatmap con imagen original
        superpuesto = cv2.addWeighted(img_array, 0.6, heatmap, 0.4, 0)

        return superpuesto

    except Exception as e:
        raise ValueError