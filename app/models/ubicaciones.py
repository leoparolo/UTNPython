from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Ubicacion(Base):
    __tablename__ = 'ubicaciones'
    ubicacion_id = Column(Integer, primary_key=True)
    codigo = Column(String)
    nombre = Column(String)
    tipo = Column(String)
    activo = Column(Integer)

    libros = relationship("Libro", back_populates="ubicaciones")
