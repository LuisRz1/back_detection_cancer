from fastapi import APIRouter, UploadFile, Form, File, Depends
from sqlalchemy.orm import Session
from app.model.model_loader import predict
from app.schemas.schemas import SkinAnalysisResult
from app.db.database import SessionLocal
from app.db import crud

router = APIRouter()


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
    # Leer la imagen original en bytes
    image_bytes = await file.read()

    metadata = {
        "age": age,
        "gender": gender,
        "lesionArea": lesionArea
    }

    # Ejecutar la predicción
    result = predict(image_bytes, metadata)

    # Guardar en la base de datos solo los campos solicitados
    crud.save_analysis(db, {
        "first_name": firstName,
        "last_name": lastName,
        "age": age,
        "gender": gender,
        "lesion_area": lesionArea,
        "diagnosis": result["diagnosis"],
        "image": image_bytes  # guarda el binario original
    })

    return result
