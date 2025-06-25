from pydantic import BaseModel
from typing import List, Literal

class UserData(BaseModel):
    firstName: str
    lastName: str
    age: int
    gender: Literal["male", "female", "other"]
    lesionArea: str

class SkinAnalysisResult(BaseModel):
    diagnosis: Literal["nv", "mel", "bkl", "bcc", "akiec", "vasc", "df"]
    confidence: float
    findings: str
    recommendations: List[str]
    urgency: Literal["routine", "soon", "urgent", "immediate"]
    nextSteps: List[str]
    diagnosisName: str
    description: str