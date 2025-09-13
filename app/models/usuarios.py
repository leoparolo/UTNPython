from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    usuario_id = Column(Integer, primary_key=True)
    dni = Column(String, nullable=False)
    nombre = Column(String,nullable=False)
    apellido = Column(String,nullable=False)
    email = Column(String,nullable=False)
    rol_id = Column(Integer, ForeignKey('roles.rol_id'),nullable=False)
    estado_id = Column(Integer, ForeignKey('estados_usuario.estado_id'),nullable=False)

    prestamos = relationship("Prestamo", back_populates="usuario")
    estado = relationship("EstadoUsuario", back_populates="usuarios")
    rol = relationship("Rol", back_populates="usuarios")
