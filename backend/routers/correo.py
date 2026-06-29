from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import smtplib
from datetime import datetime

from database import get_db
from dependencies import get_current_user
from models import Usuario, Cliente, CorreoHistorial
from config import settings

router = APIRouter(
    prefix="/correo",
    tags=["Correos"]
)


class EnviarCorreo(BaseModel):
    cliente_id: int
    asunto: str
    contenido: str
    proyecto: str = "CRM Freelancer"


@router.post("/enviar")
def enviar_correo(
    datos: EnviarCorreo,
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

    # Crear el mensaje
    mensaje = MIMEText(datos.contenido, "plain", "utf-8")

    mensaje["Subject"] = str(Header(datos.asunto, "utf-8"))
    mensaje["From"] = formataddr(("CRM Freelancer", settings.SMTP_EMAIL))
    mensaje["To"] = cliente.email

    try:

        servidor = smtplib.SMTP(
            settings.SMTP_SERVER,
            settings.SMTP_PORT
        )

        servidor.starttls()

        servidor.login(
            settings.SMTP_EMAIL,
            settings.SMTP_PASSWORD
        )

        servidor.send_message(mensaje)

        servidor.quit()

        historial = CorreoHistorial(
            cliente_id=cliente.id,
            usuario_id=usuario.id,
            proyecto=datos.proyecto,
            asunto=datos.asunto,
            contenido=datos.contenido,
            fecha=datetime.now()
        )

        db.add(historial)
        db.commit()
        db.refresh(historial)

        return {
            "mensaje": "Correo enviado correctamente."
        }

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )