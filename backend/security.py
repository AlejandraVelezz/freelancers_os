from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt

from config import settings


# ==========================
# Encriptar contraseña
# ==========================

def hash_password(password: str):
    password = password[:72]  # bcrypt solo soporta 72 bytes
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


# ==========================
# Verificar contraseña
# ==========================

def verificar_password(password_plana: str, password_encriptada: str):
    password_plana = password_plana[:72]

    return bcrypt.checkpw(
        password_plana.encode("utf-8"),
        password_encriptada.encode("utf-8")
    )


# ==========================
# Crear Token JWT
# ==========================

def crear_token(data: dict):
    datos = data.copy()

    expiracion = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    datos.update({"exp": expiracion})

    token = jwt.encode(
        datos,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token


# ==========================
# Verificar Token
# ==========================

def verificar_token(token: str):

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload

    except JWTError:
        return None