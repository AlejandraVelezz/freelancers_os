from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, Tarea, Proyecto
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/tareas", tags=["Tareas"])

# Esquema para recibir los datos de la tarea desde React
class TareaCreate(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    estado: Optional[str] = "Pendiente"
    proyecto_id: int

# Esquema para responder con los datos de la tarea
class TareaResponse(TareaCreate):
    id: int

@router.post("/", response_model=TareaResponse, status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea: TareaCreate, db: Session = Depends(get_db)):
    """Crea una tarea en MySQL amarrada a un proyecto específico"""
    proyecto = db.query(Proyecto).filter(Proyecto.id == tarea.proyecto_id).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="El proyecto especificado no existe.")
        
    nueva_tarea = Tarea(
        titulo=tarea.titulo,
        descripcion=tarea.descripcion,
        estado=tarea.estado,
        proyecto_id=tarea.proyecto_id
    )
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)
    return nueva_tarea

@router.get("/proyecto/{proyecto_id}")
def obtener_tareas_por_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    """Obtiene todas las tareas que le pertenecen a un proyecto específico"""
    tareas = db.query(Tarea).filter(Tarea.proyecto_id == proyecto_id).all()
    return tareas

@router.put("/{tarea_id}/cambiar-estado")
def cambiar_estado_tarea(tarea_id: int, estado: str, db: Session = Depends(get_db)):
    """Permite marcar una tarea como 'Completada' o 'En Progreso'"""
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada.")
    
    tarea.estado = estado
    db.commit()
    return {"mensaje": "Estado actualizado con éxito", "nuevo_estado": tarea.estado}