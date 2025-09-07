from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Prestamo(Base):
    __tablename__ = 'prestamos'
    prestamo_id = Column(Integer, primary_key=True)
    libro_id = Column(Integer, ForeignKey('libros.libro_id'),nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'),nullable=False)
    fecha_prestamo = Column(Date, nullable=False)
    fecha_devolucion_esperada = Column(Date, nullable=False)
    estado = Column(String,nullable=False)

    libro = relationship("Libro", back_populates="prestamos")
    usuario = relationship("Usuario", back_populates="prestamos")
