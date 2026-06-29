from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ¡Importante!
from app.database import Base, engine
from app.routers import clientes, ia
from app.routers import clientes, ia, proyectos  
from app.routers import clientes, ia, proyectos, tareas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Freelancer CRM API", version="1.0.0")

# CONFIGURACIÓN DE CORS: Permite que React se conecte sin bloqueos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción cambias el "*" por la URL de tu front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes.router)
app.include_router(ia.router)
app.include_router(proyectos.router)
app.include_router(tareas.router)

@app.get("/")
def inicio():
    return {"mensaje": "¡Backend conectado con CORS y MySQL!"}