from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Libro(Base):
    __tablename__ = 'libros'
    libro_id = Column(Integer, primary_key=True)
    titulo = Column(String)
    autor_id = Column(Integer,ForeignKey('autor.autor_id'))
    editorial_id = Column(Integer, ForeignKey('editorial.editorial_id'))
    isbn = Column(String)
    categoria_id = Column(Integer, ForeignKey('categoria.categoria_id'))
    cantidad_ejemplares = Column(Integer)
    ejemplares_disponibles = Column(Integer)
    ubicacion_id = Column(Integer, ForeignKey('ubicacion.ubicacion_id'))
    resumen = Column(String)

    autor = relationship("Autor", back_populates="libros")
    editorial = relationship("Editorial", back_populates="libros")
    ubicacion = relationship("Ubicacion", back_populates="libros")
    categoria = relationship("Categoria", back_populates="libros")
    prestamo = relationship("Prestamo", back_populates="libros")