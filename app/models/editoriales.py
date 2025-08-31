from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Editorial(Base):
    __tablename__ = 'editoriales'
    editorial_id = Column(Integer, primary_key=True)
    nombre = Column(String)
    direccion = Column(String)
    telefono = Column(String)
    email = Column(String)

    libros = relationship("Libro", back_populates="editoriales")
