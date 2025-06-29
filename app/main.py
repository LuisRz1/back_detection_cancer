from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Rutas de la API
from app.api import router as api_router



# Inicializar FastAPI
app = FastAPI(
    title="Skin Analysis API",
    description="API para detección de cáncer de piel",
    version="1.0.0",
    docs_url="/docs",  # Habilita Swagger
    redoc_url="/redoc"  # Habilita ReDoc
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Puedes limitar esto a dominios específicos en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(api_router)

# Ruta raíz
@app.get("/")
def read_root():
    return {"message": "Backend de detección de cáncer dermatológico activo."}