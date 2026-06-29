from pydantic import BaseModel

class PropuestaEmailRequest(BaseModel):
    nombre_cliente: str
    proyecto_detalle: str
    tono: str

class EnviarCorreoRequest(BaseModel):
    nombre_cliente: str
    proyecto_detalle: str
    mensaje: str