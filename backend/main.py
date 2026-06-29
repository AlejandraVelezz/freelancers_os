from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db, engine, Base
from models import Usuario

# Importación de Routers
from routers.auth import router as auth_router
from routers.clientes import router as clientes_router  
from routers.proyectos import router as proyectos_router
from routers import ia

from routers.correo import router as correo_router

# Crear las tablas en MySQL/MariaDB si no existen
Base.metadata.create_all(bind=engine)

# ÚNICA DECLARACIÓN DE LA APP
app = FastAPI(
    title="CRM Freelancer",
    version="1.0"
)

# ==========================================
# CONFIGURACIÓN CORS (UNA SOLA VEZ)
# ==========================================
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Permite todas las cabeceras (incluyendo Authorization)
)

# ==========================================
# RUTAS DIRECTAS
# ==========================================
@app.get("/")
def inicio():
    return {
        "mensaje": "CRM Freelancer funcionando correctamente"
    }


@app.get("/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


# ==========================================
# INCLUSIÓN DE ROUTERS
# ==========================================
app.include_router(auth_router)
app.include_router(clientes_router)
app.include_router(proyectos_router)
app.include_router(ia.router)
app.include_router(correo_router)