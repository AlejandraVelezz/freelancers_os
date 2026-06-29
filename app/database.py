from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import DateTime
from datetime import datetime

# 1. URL DE CONEXIÓN A MYSQL
# Cambia 'root' y 'tu_contraseña' por los datos de tu MySQL local
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/crm_freelancer"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para usar la BD en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 2. MODELOS DE LAS TABLAS (ESTRUCTURA MYSQL)
# ==========================================

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    empresa = Column(String(150), nullable=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    telefono = Column(String(50), nullable=True)

    proyectos = relationship("Proyecto", back_populates="cliente", cascade="all, delete-orphan")


class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(String(50), default="Nuevo")
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"))

    cliente = relationship("Cliente", back_populates="proyectos")
    tareas = relationship("Tarea", back_populates="proyecto", cascade="all, delete-orphan")


class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer,ForeignKey("clientes.id", ondelete="CASCADE"))
    asunto = Column(String(200), nullable=False)
    mensaje = Column(Text, nullable=False)
    estado = Column(String(50), default="enviado")
    tipo = Column(String(50), default="Correo")
    fecha = Column(DateTime, default= datetime.utcnow)


class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(String(50), default="Pendiente")
    proyecto_id = Column(Integer, ForeignKey("proyectos.id", ondelete="CASCADE"))

    proyecto = relationship("Proyecto", back_populates="tareas")

class CorreoHistorial(Base):
    __tablename__ = "correos_historial"

    id = Column(Integer, primary_key=True, index=True)

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id", ondelete="CASCADE")
    )

    proyecto = Column(String(200))
    contenido = Column(Text, nullable=False)

    fecha = Column(DateTime, default=datetime.utcnow)

