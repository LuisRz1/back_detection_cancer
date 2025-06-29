from fastapi import APIRouter, UploadFile, Form, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.model.model_loader import predict
from app.schemas.schemas import SkinAnalysisResult
from app.db.database import SessionLocal
from app.db import crud

router = APIRouter()

# Sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint de predicción
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
    try:
        # Leer la imagen como bytes (sin decodificar)
        image_bytes = await file.read()

        # Crear metadata para el modelo
        metadata = {
            "age": age,
            "gender": gender,
            "lesionArea": lesionArea
        }

        # Ejecutar predicción
        result = predict(image_bytes, metadata)

        # Guardar análisis en la BD (sin probabilidades)
        #crud.save_analysis(db, {
        #    "first_name": firstName,
        #    "last_name": lastName,
        #    "age": age,
        #    "gender": gender,
        #    "lesion_area": lesionArea,
        #    "diagnosis": result["diagnosis"],
        #    "image": image_bytes
        #})

        # Retornar predicción (incluye diagnosis y probabilidades)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la predicción: {str(e)}")