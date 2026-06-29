import os
from pydantic_settings import BaseSettings

# Aquí cargamos la API Key de Groq de forma segura desde las variables de entorno (.env)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Tu variable SECRET_KEY que usa la aplicación
SECRET_KEY = os.getenv("SECRET_KEY", "Aa333216")
