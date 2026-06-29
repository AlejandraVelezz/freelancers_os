from pydantic import BaseModel, EmailStr
from typing import Optional


# ==================================================
# LOGIN
# ==================================================

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


# ==================================================
# REGISTRO
# ==================================================

class UsuarioRegistro(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    tipo_usuario: str = "usuario"


# ==================================================
# RESPUESTA USUARIO
# ==================================================

class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    tipo_usuario: str

    class Config:
        from_attributes = True


# ==================================================
# TOKEN
# ==================================================

from typing import Dict, Any

class Token(BaseModel):
    access_token: str
    token_type: str
    usuario: Dict[str, Any]


# ==================================================
# CLIENTES
# ==================================================

class ClienteBase(BaseModel):
    nombre: str
    empresa: Optional[str] = None
    email: EmailStr
    telefono: Optional[str] = None


class ClienteCreate(ClienteBase):
    password: str


class ClienteResponse(ClienteBase):
    id: int
    usuario_id: int

    class Config:
        from_attributes = True


# ==================================================
# PROYECTOS
# ==================================================

class ProyectoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    estado: str = "Pendiente"


class ProyectoCreate(ProyectoBase):
    cliente_id: int


class ProyectoResponse(ProyectoBase):
    id: int
    cliente_id: int
    usuario_id: int

    class Config:
        from_attributes = True


# ==================================================
# TAREAS
# ==================================================

class TareaBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    estado: str = "Pendiente"


class TareaCreate(TareaBase):
    proyecto_id: int
    usuario_id: int


class TareaResponse(TareaBase):
    id: int
    proyecto_id: int
    usuario_id: int

    class Config:
        from_attributes = True


# ==================================================
# HISTORIAL DE CORREOS
# ==================================================

class CorreoCreate(BaseModel):
    cliente_id: int
    proyecto: str
    contenido: str
    usuario_id: int


class CorreoResponse(CorreoCreate):
    id: int

    class Config:
        from_attributes = True