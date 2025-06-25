from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from model.model_loader import predict
from schemas import SkinAnalysisResult

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

@app.post("/analyze", response_model=SkinAnalysisResult)
async def analyze(
    firstName: str = Form(...),
    lastName: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    lesionArea: str = Form(...),
    image: UploadFile = Form(...)
):
    image_bytes = await image.read()
    metadata = {
        "age": age,
        "gender": gender,
        "lesionArea": lesionArea
    }

    result = predict(image_bytes, metadata)
    return SkinAnalysisResult(**result)
