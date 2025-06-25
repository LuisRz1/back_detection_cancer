import numpy as np
import tensorflow as tf
import cv2
from PIL import Image
import io
import tempfile
from .heatmap import preprocess_image, generate_pseudo_heatmap

# Clases del modelo
CLASSES = ['nv', 'mel', 'bkl', 'bcc', 'akiec', 'vasc', 'df']

# Cargar el modelo entrenado
model = tf.keras.models.load_model("app/model/modelo_0-4_tuned.keras")

# Zonas de lesión codificadas
AREA_CODES = {
    'back': 0, 'lower extremity': 1, 'trunk': 2, 'upper extremity': 3,
    'abdomen': 5, 'face': 6, 'chest': 7, 'foot': 8, 'unknown': 9,
    'neck': 10, 'scalp': 11, 'hand': 12, 'ear': 13, 'genital': 14, 'acral': 15
}

def encode_gender(gender: str) -> int:
    gender = gender.strip().lower()
    if gender == "female":
        return 1
    elif gender == "male":
        return 0
    else:
        return 2

def one_hot_area(area: str) -> np.ndarray:
    area = area.strip().lower()
    area_idx = AREA_CODES.get(area, 9)  # 'unknown' = 9 por defecto
    one_hot = np.zeros(16)
    if 0 <= area_idx < 16:
        one_hot[area_idx] = 1
    return one_hot[1:]  # Eliminamos la primera columna → 15 columnas

def predict(image_bytes: bytes, metadata: dict) -> dict:
    image_array = preprocess_image(image_bytes)
    heatmap_array = generate_pseudo_heatmap(image_array)

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
        heatmap_bgr = cv2.cvtColor(heatmap_array, cv2.COLOR_RGB2BGR)
        cv2.imwrite(tmp_file.name, heatmap_bgr)
        tmp_path = tmp_file.name

    img = tf.keras.preprocessing.image.load_img(tmp_path, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_input = np.expand_dims(img_array, axis=0)

    age = metadata['age']
    gender = encode_gender(metadata['gender'])
    lesion_area = one_hot_area(metadata['lesionArea'])

    # CORREGIDO
    meta_input = np.array([[age, gender, *lesion_area]])

    preds = model.predict([img_input, meta_input])[0]
    pred_idx = np.argmax(preds)
    confidence = float(preds[pred_idx])
    label = CLASSES[pred_idx]

    return {
        "diagnosis": label,
        "confidence": confidence
    }
