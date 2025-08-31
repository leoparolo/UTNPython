from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Prestamo(Base):
    __tablename__ = 'prestamos'
    prestamo_id = Column(Integer, primary_key=True)
    libro_id = Column(Integer, ForeignKey('libro.libro_id'))
    usuario_id = Column(Integer, ForeignKey('usuario.usuario_id'))
    fecha_prestamo = Column(Date)
    fecha_devolucion_esperada = Column(Date)
    estado = Column(String)

    libro = relationship("Libro", back_populates="prestamos")
    usuario = relationship("Usuario", back_populates="prestamos")
