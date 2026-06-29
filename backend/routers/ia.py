from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from groq import Groq
import traceback
import json

from config import settings
from database import get_db
from dependencies import get_current_user
from models import Cliente, Usuario

router = APIRouter(
    prefix="/ia",
    tags=["Inteligencia Artificial"]
)

client = Groq(
    api_key=settings.GROQ_API_KEY
)


class SolicitudCorreo(BaseModel):
    cliente_id: int
    detalles: str
    tono: str


@router.post("/generar-correo")
def generar_correo(
    datos: SolicitudCorreo,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):

    cliente = db.query(Cliente).filter(
        Cliente.id == datos.cliente_id
    ).first()

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado."
        )

    prompt = f"""
Eres un asistente experto redactando correos para un CRM de freelancers.

INFORMACIÓN DEL REMITENTE

Nombre:
{usuario.nombre}

Correo:
{usuario.email}

Cargo:
{usuario.tipo_usuario}

--------------------------------------

INFORMACIÓN DEL DESTINATARIO

Nombre:
{cliente.nombre}

Empresa:
{cliente.empresa}

Correo:
{cliente.email}

--------------------------------------

TONO

{datos.tono}

--------------------------------------

MOTIVO

{datos.detalles}

--------------------------------------

INSTRUCCIONES

Responde únicamente en formato JSON.

Ejemplo:

{{
    "asunto": "Avance del proyecto",
    "contenido": "Hola..."
}}

No agregues texto adicional.
"""

    try:

        respuesta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un experto redactando correos empresariales."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=700
        )

        texto = respuesta.choices[0].message.content

        texto = texto.replace("```json", "").replace("```", "").strip()

        try:
            datos_correo = json.loads(texto)

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="La IA devolvió un formato JSON inválido."
            )

        return {
            "remitente": usuario.nombre,
            "correo_remitente": usuario.email,
            "destinatario": cliente.nombre,
            "correo_destinatario": cliente.email,
            "empresa": cliente.empresa,
            "asunto": datos_correo["asunto"],
            "correo": datos_correo["contenido"]
        }

    except Exception:

        traceback.print_exc()

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Error interno. Revisa la terminal del backend."
        )