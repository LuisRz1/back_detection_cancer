import numpy as np
import tensorflow as tf
import cv2
from PIL import Image
import io
import tempfile
from .heatmap import preprocess_image, generate_pseudo_heatmap

# Clases del modelo
CLASSES = ['akiec', 'bcc', 'bkl', 'mel', 'nv']

# Cargar el modelo entrenado
model = tf.keras.models.load_model("app/model/modelo_0-4_tuned.keras")

# Zonas de lesión codificadas
AREA_CODES = {
    'abdomen': 0, 'back': 1, 'chest': 2, 'ear': 3, 'face': 4,
    'foot': 5, 'genital': 6, 'hand': 7, 'lower extremity': 8,
    'neck': 9, 'scalp': 10, 'trunk': 11, 'unknown': 12, 'upper extremity': 13
}

def encode_gender(gender: str) -> int:
    gender = gender.strip().lower()
    if gender == "female":
        return 0
    elif gender == "male":
        return 1
    raise ValueError(f"Valor de género no válido: {gender}")

def encode_area(area: str) -> int:
    area = area.strip().lower()
    if area not in AREA_CODES:
        raise ValueError(f"Área no reconocida: '{area}'")
    return AREA_CODES[area]

def predict(image_bytes: bytes, metadata: dict) -> dict:
    try:
        # Procesar imagen: bytes → RGB array
        image_array = preprocess_image(image_bytes)

        # Generar mapa de calor
        heatmap_array = generate_pseudo_heatmap(image_array)

        # Redimensionar y preparar para el modelo
        heatmap_resized = cv2.resize(heatmap_array, (224, 224))
        img_input = np.expand_dims(heatmap_resized, axis=0)

        # Procesar metadatos
        age = float(metadata['age'])
        gender = encode_gender(metadata['gender'])
        area = encode_area(metadata['lesionArea'])

        meta_input = np.array([[age, gender, area]])

        # Predicción
        preds = model.predict([img_input, meta_input])[0]
        pred_idx = int(np.argmax(preds))
        confidence = float(preds[pred_idx])
        label = CLASSES[pred_idx]

        return {
            "diagnosis": label,
            "confidence": confidence,
            "probabilities": {
                class_name: float(prob)
                for class_name, prob in zip(CLASSES, preds)
            }
        }
    except Exception as e:
        raise ValueError(f"Error al procesar la predicción: {str(e)}")