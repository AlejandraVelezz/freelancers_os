from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db, Usuario
from app.schemas.auth import (
    UsuarioRegistro,
    UsuarioLogin,
    Token
)

from security import (
    encriptar_password,
    verificar_password,
    crear_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


# ==========================
# REGISTRO
# ==========================

@router.post("/registro")
def registrar(
    usuario: UsuarioRegistro,
    db: Session = Depends(get_db)
):

    existe = db.query(Usuario).filter(
        Usuario.email == usuario.email
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado."
        )

    nuevo = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password=encriptar_password(usuario.password),
        tipo_usuario="usuario"
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {
        "mensaje": "Usuario registrado correctamente"
    }


# ==========================
# LOGIN
# ==========================

@router.post("/login", response_model=Token)
def login(
    datos: UsuarioLogin,
    db: Session = Depends(get_db)
):

    usuario = db.query(Usuario).filter(
        Usuario.email == datos.email
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )

    if not verificar_password(
        datos.password,
        usuario.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )

    token = crear_token({
        "sub": str(usuario.id)
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
