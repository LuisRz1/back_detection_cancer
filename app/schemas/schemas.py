from pydantic import BaseModel
from typing import Dict, Literal

# Datos del usuario (opcional para uso futuro en validaciones)
class UserFormData(BaseModel):
    firstName: str
    lastName: str
    age: int
    gender: Literal["male", "female"]
    lesionArea: str

# Solo los campos que el modelo necesita (opcional si se usa validación interna)
class PredictionMetadata(BaseModel):
    age: int
    gender: Literal["male", "female"]
    lesionArea: str

# Esquema de respuesta que incluye diagnosis, confidence y TODAS las probabilidades
class SkinAnalysisResult(BaseModel):
    diagnosis: Literal["akiec", "bcc", "bkl", "mel", "nv"]
    confidence: float
    probabilities: Dict[str, float]  # ← Agregado para ver distribución de clases

    class Config:
        orm_mode = True