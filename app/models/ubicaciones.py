from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Ubicacion(Base):
    __tablename__ = 'ubicaciones'
    ubicacion_id = Column(Integer, primary_key=True)
    codigo = Column(String,nullable=False)
    nombre = Column(String,nullable=False)
    tipo = Column(String,nullable=True)
    activo = Column(Integer,nullable=True)

    libros = relationship("Libro", back_populates="ubicacion")
