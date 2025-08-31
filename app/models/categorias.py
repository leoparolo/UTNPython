from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Categoria(Base):
    __tablename__ = 'categorias'
    categoria_id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)

    libro = relationship("Libro", back_populates="libros")
