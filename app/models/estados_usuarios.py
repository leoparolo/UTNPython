from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class EstadoUsuario(Base):
    __tablename__ = 'estados_usuarios'
    estado_id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)

    usuarios = relationship("Usuario", back_populates="estado")
