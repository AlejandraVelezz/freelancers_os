from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, Proyecto, Cliente
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

# Esquema para recibir los datos del proyecto desde React
class ProyectoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    estado: Optional[str] = "Nuevo"
    cliente_id: int

# Esquema para responder con los datos del proyecto
class ProyectoResponse(ProyectoCreate):
    id: int

@router.post("/", response_model=ProyectoResponse, status_code=status.HTTP_201_CREATED)
def crear_proyecto(proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    """Crea un proyecto en MySQL amarrado a un cliente específico"""
    # Verificamos si el cliente realmente existe antes de asignarle el proyecto
    cliente = db.query(Cliente).filter(Cliente.id == proyecto.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="El cliente especificado no existe.")
        
    nuevo_proyecto = Proyecto(
        nombre=proyecto.nombre,
        descripcion=proyecto.descripcion,
        estado=proyecto.estado,
        cliente_id=proyecto.cliente_id
    )
    db.add(nuevo_proyecto)
    db.commit()
    db.refresh(nuevo_proyecto)
    return nuevo_proyecto

@router.get("/cliente/{cliente_id}")
def obtener_proyectos_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtiene todos los proyectos que le pertenecen a un cliente específico"""
    proyectos = db.query(Proyecto).filter(Proyecto.cliente_id == cliente_id).all()
    return proyectos