import numpy as np
import tensorflow as tf
from .heatmap import preprocess_image, generate_pseudo_heatmap

CLASSES = ['nv', 'mel', 'bkl', 'bcc', 'akiec', 'vasc', 'df']

model = tf.keras.models.load_model("") #Ruta del modelo de deteccion

def encode_gender(gender: str) -> int:
    return {'male': 0, 'female': 1, 'other': 2}.get(gender, 2)

def encode_area(area: str) -> int:
    areas = {'torso': 0, 'face': 1, 'arm': 2, 'leg': 3}
    return areas.get(area.lower(), 0)

def predict(image_bytes: bytes, metadata: dict) -> dict:
    image_array = preprocess_image(image_bytes)
    heatmap = generate_pseudo_heatmap(image_array)

    # Combine heatmap + metadata into final input
    flat_image = heatmap.flatten()
    age = metadata['age'] / 100
    gender = encode_gender(metadata['gender']) / 2
    lesion_area = encode_area(metadata['lesionArea']) / 3

    full_input = np.concatenate([flat_image, [age, gender, lesion_area]])
    full_input = full_input.reshape(1, -1)

    preds = model.predict(full_input)[0]
    pred_idx = np.argmax(preds)
    confidence = float(preds[pred_idx])
    label = CLASSES[pred_idx]

    return {
        "diagnosis": label,
        "confidence": confidence,
        # Los siguientes pueden venir de un diccionario como diagnosisInfo
        "findings": "Resultado del análisis automático.",
        "recommendations": ["Consulta dermatológica", "Evitar exposición solar"],
        "urgency": "routine" if label in ["nv", "bkl"] else "immediate",
        "nextSteps": ["Consulta médica especializada"],
        "diagnosisName": label.upper(),
        "description": "Descripción generada automáticamente del diagnóstico"
    }
