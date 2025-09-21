from datetime import date
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
    fecha_devolucion_real = Column(Date, nullable=True)
    estado = Column(String,nullable=False)

    libro = relationship("Libro", back_populates="prestamos")
    usuario = relationship("Usuario", back_populates="prestamos")

    @property
    def estado_calculado(self) -> str:
        if self.fecha_devolucion_real:
            return "D"  # Devuelto
        elif self.fecha_devolucion_esperada < date.today():
            return "A"  # Atrasado
        elif self.fecha_prestamo > date.today():
            return "P"  # Pendiente (aún no empezó)
        else:
            return "E"  # En curso
