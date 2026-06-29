import os
from fastapi import APIRouter, HTTPException
from openai import OpenAI
from app.schemas.ia import PropuestaEmailRequest, EnviarCorreoRequest
from dotenv import load_dotenv
from pathlib import Path

# Buscamos la ruta absoluta exacta de la carpeta crm-backend para leer SU .env
base_dir = Path(__file__).resolve().parent.parent.parent
env_path = base_dir / ".env"
load_dotenv(dotenv_path=env_path)

router = APIRouter(prefix="/ia", tags=["Inteligencia Artificial"])

# Forzamos la lectura limpia de la variable GROQ_API_KEY
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

@router.post("/generar-correo")
async def generar_correo(payload: PropuestaEmailRequest):
    """
    Endpoint que conecta con Groq IA para redactar un correo personalizado
    basado en el cliente, el detalle de la notificación y el tono solicitado.
    """
    # Verificación de seguridad por si la API Key sigue llegando vacía
    if not os.getenv("GROQ_API_KEY"):
        raise HTTPException(
            status_code=500, 
            detail="Error de configuración interna: La clave 'GROQ_API_KEY' no fue encontrada en el archivo .env."
        )
    
    # Construcción del prompt estructurado para la Inteligencia Artificial
    prompt_sistema = (
        "Eres un asistente virtual experto en comunicación y CRM para freelancers. "
        "Tu objetivo es redactar correos electrónicos claros, concisos y profesionales."
    )
    
    prompt_usuario = (
        f"Escribe un correo electrónico dirigido al cliente: '{payload.nombre_cliente}'.\n"
        f"El motivo o detalle de lo que se le va a notificar es el siguiente: '{payload.proyecto_detalle}'.\n"
        f"El tono del mensaje debe ser estrictamente: '{payload.tono}'.\n\n"
        "Por favor, genera únicamente el cuerpo del correo (incluyendo un asunto adecuado al inicio, "
        "saludo, desarrollo y una despedida formal como freelancer). No agregues comentarios extra ni explicaciones."
    )

    try:
        # Petición formal a la API de Groq usando el modelo Llama 3
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ],
            temperature=0.7
        )
        
        # Extraer el texto generado por la IA
        texto_generado = completion.choices[0].message.content
        
        # Retornar la respuesta estructurada exactamente como la espera el Frontend
        return {"correo_generado": texto_generado}

    except Exception as e:
        # Si la API de Groq responde con un error (como el 401), lo capturamos aquí
        print(f"--- ERROR DE CONEXIÓN CON GROQ ---: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error al conectar con el servicio de IA de Groq: {str(e)}"
        )

@router.post("/enviar-correo")
async def enviar_correo(payload: EnviarCorreoRequest):
    return {
        "mensaje": "Correo enviado correctamente",
        "cliente_id": payload.cliente_id,
        "estado" : "Enviado"
    }