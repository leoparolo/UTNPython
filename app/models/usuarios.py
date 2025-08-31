from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    usuario_id = Column(Integer, primary_key=True)
    dni = Column(String)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    rol_id = Column(Integer, ForeignKey('roles.rol_id'))
    estado_id = Column(Integer, ForeignKey('estados_usuarios.estado_id'))

    prestamos = relationship("Prestamo", back_populates="usuarios")
    estados_usuarios = relationship("EstadoUsuario", back_populates="usuarios")
    roles = relationship("Rol", back_populates="usuarios")
