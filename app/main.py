from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import models
from app.db.database import engine
from app.api import router as api_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(api_router)

# Ruta raíz
@app.get("/")
def read_root():
    return {"message": "Backend de detección de cáncer dermatológico activo."}
