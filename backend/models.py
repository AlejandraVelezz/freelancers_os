from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    ForeignKey
)

from database import Base


# ==========================================
# USUARIOS
# ==========================================

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    tipo_usuario = Column(String(100), nullable=False)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    fecha_registro = Column(TIMESTAMP)


# ==========================================
# CLIENTES
# ==========================================

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String(150), nullable=False)
    empresa = Column(String(150))
    email = Column(String(150), unique=True)
    telefono = Column(String(50))

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        unique=True
    )

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    empresa = Column(String(150))
    email = Column(String(150), unique=True)
    telefono = Column(String(50))

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id")
    )


# ==========================================
# PROYECTOS
# ==========================================

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    estado = Column(String(50))

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id")
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id")
    )


# ==========================================
# TAREAS
# ==========================================

class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text)
    estado = Column(String(50))

    proyecto_id = Column(
        Integer,
        ForeignKey("proyectos.id")
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id")
    )


# ==========================================
# CORREOS
# ==========================================

class CorreoHistorial(Base):
    __tablename__ = "correos_historial"

    id = Column(Integer, primary_key=True, index=True)

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id")
    )

    proyecto = Column(String(200))

    asunto = Column(String(200))

    contenido = Column(Text, nullable=False)

    fecha = Column(TIMESTAMP)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id")
    )


# ==========================================
# NOTIFICACIONES
# ==========================================

class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id")
    )

    mensaje = Column(Text)

    leida = Column(Integer)

    fecha = Column(TIMESTAMP)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id")
    )