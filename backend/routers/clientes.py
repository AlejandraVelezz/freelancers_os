from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from models import Cliente, Usuario
from security import hash_password

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


# ==========================================
# OBTENER CLIENTES
# ==========================================

@router.get("/", response_model=List[dict])
def obtener_clientes(db: Session = Depends(get_db)):

    clientes = db.query(Cliente).all()

    return [
        {
            "id": c.id,
            "nombre": c.nombre,
            "empresa": c.empresa,
            "email": c.email,
            "telefono": c.telefono,
            "usuario_id": c.usuario_id
        }
        for c in clientes
    ]


# ==========================================
# CREAR CLIENTE
# ==========================================

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente_data: dict, db: Session = Depends(get_db)):

    try:

        # Verificar que no exista un usuario con ese correo
        existe = db.query(Usuario).filter(
            Usuario.email == cliente_data["email"]
        ).first()

        if existe:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un usuario con ese correo."
            )

        # Crear usuario para que el cliente pueda iniciar sesión
        nuevo_usuario = Usuario(
            nombre=cliente_data["nombre"],
            email=cliente_data["email"],
            password=hash_password(cliente_data["password"]),
            tipo_usuario="cliente",
            fecha_registro=datetime.now()
        )

        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        # Crear cliente asociado al usuario
        nuevo_cliente = Cliente(
            nombre=cliente_data["nombre"],
            empresa=cliente_data.get("empresa"),
            email=cliente_data["email"],
            telefono=cliente_data.get("telefono"),
            usuario_id=nuevo_usuario.id
        )

        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)

        return {
            "mensaje": "Cliente creado correctamente.",
            "cliente_id": nuevo_cliente.id,
            "usuario_id": nuevo_usuario.id
        }

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )