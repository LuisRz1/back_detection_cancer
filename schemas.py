from pydantic import BaseModel
from typing import List, Literal

# Esto es lo que se recibe en el backend
class UserFormData(BaseModel):
    firstName: str
    lastName: str
    age: int
    gender: Literal["male", "female", "other"]
    lesionArea: str

# Este esquema representa solo lo que el modelo necesita
class PredictionMetadata(BaseModel):
    age: int
    gender: Literal["male", "female", "other"]
    lesionArea: str

# Este esquema representa la respuesta que devuelve el backend al frontend
class SkinAnalysisResult(BaseModel):
    diagnosis: Literal["nv", "mel", "bkl", "bcc", "akiec", "vasc", "df"]
    confidence: float
    findings: str
    recommendations: List[str]
    urgency: Literal["routine", "soon", "urgent", "immediate"]
    nextSteps: List[str]
    diagnosisName: str
    description: str
