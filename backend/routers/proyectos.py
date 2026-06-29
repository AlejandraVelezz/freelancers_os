from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Proyecto
from schemas import ProyectoCreate
from dependencies import get_current_user
from models import Usuario


router = APIRouter(
    prefix="/proyectos",
    tags=["Proyectos"]
)


# ==========================
# LISTAR TODOS
# ==========================

@router.get("/")
def listar_proyectos(db: Session = Depends(get_db)):
    return db.query(Proyecto).all()


# ==========================
# LISTAR POR CLIENTE
# ==========================

@router.get("/cliente/{cliente_id}")
def listar_por_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):

    return db.query(Proyecto).filter(
        Proyecto.cliente_id == cliente_id,
        Proyecto.usuario_id == usuario.id
    ).all()


# ==========================
# CREAR
# ==========================

@router.post("/")
def crear_proyecto(
    proyecto: ProyectoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):

    nuevo = Proyecto(
        nombre=proyecto.nombre,
        descripcion=proyecto.descripcion,
        estado=proyecto.estado,
        cliente_id=proyecto.cliente_id,
        usuario_id=usuario.id
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo

# ==========================
# ACTUALIZAR
# ==========================

@router.put("/{id}")
def actualizar_proyecto(
    id: int,
    proyecto: ProyectoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):

    existente = db.query(Proyecto).filter(
        Proyecto.id == id,
        Proyecto.usuario_id == usuario.id
    ).first()

    if existente is None:
        raise HTTPException(
            status_code=404,
            detail="Proyecto no encontrado"
        )

    existente.nombre = proyecto.nombre
    existente.descripcion = proyecto.descripcion
    existente.estado = proyecto.estado
    existente.cliente_id = proyecto.cliente_id

    db.commit()
    db.refresh(existente)

    return existente

# ==========================
# ELIMINAR
# ==========================

@router.delete("/{id}")
def eliminar_proyecto(
    id: int,
    db: Session = Depends(get_db)
):

    proyecto = db.query(Proyecto).filter(
        Proyecto.id == id
    ).first()

    if proyecto is None:
        raise HTTPException(
            status_code=404,
            detail="Proyecto no encontrado"
        )

    db.delete(proyecto)
    db.commit()

    return {
        "mensaje": "Proyecto eliminado"
    }