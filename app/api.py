from fastapi import APIRouter, UploadFile, Form, File, Depends
from sqlalchemy.orm import Session

from app.model.model_loader import predict
from app.schemas.schemas import SkinAnalysisResult
from app.db.database import SessionLocal
from app.db import crud

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/predict", response_model=SkinAnalysisResult)
async def analyze_skin(
    file: UploadFile = File(...),
    firstName: str = Form(...),
    lastName: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    lesionArea: str = Form(...),
    db: Session = Depends(get_db)
):
    image_bytes = await file.read()

    metadata = {
        "age": age,
        "gender": gender,
        "lesionArea": lesionArea
    }

    result = predict(image_bytes, metadata)

    # Guardar en base de datos
    crud.save_analysis(db, {
        "first_name": firstName,
        "last_name": lastName,
        "age": age,
        "gender": gender,
        "lesionArea": lesionArea,
        "diagnosis": result["diagnosis"],
        "confidence": result["confidence"]
    })

    # Construir respuesta completa
    return {
        "diagnosis": result["diagnosis"],
        "confidence": result["confidence"],
        "findings": f"Lesión clasificada como {result['diagnosis'].upper()} con {result['confidence']:.2%} de confianza.",
        "recommendations": ["Consultar dermatólogo", "Evitar exposición solar directa"],
        "urgency": "routine",
        "nextSteps": ["Agendar cita médica", "Monitoreo de evolución"],
        "diagnosisName": result["diagnosis"].upper(),
        "description": f"{result['diagnosis'].upper()} es una categoría identificada automáticamente. Se recomienda confirmación médica."
    }
