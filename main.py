from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from model.model_loader import predict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

@app.post("/predict")
async def analyze_skin(
    file: UploadFile = File(...),
    firstName: str = Form(...),  # Solo para registrar, no entra al modelo
    lastName: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    lesionArea: str = Form(...)
):
    image_bytes = await file.read()

    # Solo estos se usan en el modelo
    metadata = {
        "age": age,
        "gender": gender,
        "lesionArea": lesionArea
    }

    # Lógica de predicción
    result = predict(image_bytes, metadata)

    # Opcional: añadir info del paciente a la respuesta si deseas log completo
    result.update({
        "firstName": firstName,
        "lastName": lastName
    })

    return result
