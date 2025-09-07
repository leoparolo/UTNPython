from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Libro(Base):
    __tablename__ = 'libros'
    libro_id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    autor_id = Column(Integer,ForeignKey('autores.autor_id'), nullable=False)
    editorial_id = Column(Integer, ForeignKey('editoriales.editorial_id'), nullable=False)
    isbn = Column(String,nullable=True)
    categoria_id = Column(Integer, ForeignKey('categorias.categoria_id'),nullable=True)
    cantidad_ejemplares = Column(Integer, nullable=False, default=0)
    ejemplares_disponibles = Column(Integer, nullable=False, default=0)
    ubicacion_id = Column(Integer, ForeignKey('ubicaciones.ubicacion_id'), nullable=True)
    resumen = Column(String, nullable=True)

    autor = relationship("Autor", back_populates="libros")
    editorial = relationship("Editorial", back_populates="libros")
    ubicacion = relationship("Ubicacion", back_populates="libros")
    categoria = relationship("Categoria", back_populates="libros")
    prestamos = relationship("Prestamo", back_populates="libro")