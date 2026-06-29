from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class ClienteCreate(BaseModel):
    nombre: str
    empresa: Optional[str] = None
    email: EmailStr
    telefono: Optional[str] = None


class ClienteResponse(ClienteCreate):
    id: int

    class Config:
        from_attributes = True


class CorreoHistorialResponse(BaseModel):
    id: int
    cliente_id: int
    proyecto: str
    contenido: str
    fecha: datetime

    class Config:
        from_attributes = True