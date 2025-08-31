from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Rol(Base):
    __tablename__ = 'roles'
    rol_id = Column(Integer, primary_key=True)
    nombre = Column(String)
    dias_prestamos = Column(Integer)

    usuario = relationship("Usuario", back_populates="roles")