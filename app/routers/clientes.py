from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import (
    get_db,
    Cliente,
    CorreoHistorial
)

from app.schemas import (
    ClienteResponse
)

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


# =====================================
# CLIENTES
# =====================================

@router.get("/", response_model=List[ClienteResponse])
def obtener_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def guardar_cliente(cliente: dict, db: Session = Depends(get_db)):

    nuevo_cliente = Cliente(
        nombre=cliente.get("nombre"),
        empresa=cliente.get("empresa"),
        email=cliente.get("email"),
        telefono=cliente.get("telefono")
    )

    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)

    return nuevo_cliente


# =====================================
# HISTORIAL DE CORREOS IA
# =====================================

@router.post("/{cliente_id}/correos", status_code=status.HTTP_201_CREATED)
def guardar_correo_cliente(
    cliente_id: int,
    correo_data: dict,
    db: Session = Depends(get_db)
):

    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente {cliente_id} no encontrado"
        )

    nuevo_correo = CorreoHistorial(
        cliente_id=cliente_id,
        proyecto=correo_data.get("proyecto", "General"),
        contenido=correo_data.get("contenido"),
        fecha=datetime.utcnow()
    )

    try:
        db.add(nuevo_correo)
        db.commit()
        db.refresh(nuevo_correo)

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {
        "success": True,
        "mensaje": "Correo guardado correctamente",
        "id": nuevo_correo.id
    }


@router.get("/{cliente_id}/correos")
def obtener_historial_correos(
    cliente_id: int,
    db: Session = Depends(get_db)
):

    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    correos = db.query(CorreoHistorial).filter(
        CorreoHistorial.cliente_id == cliente_id
    ).all()

    return correos