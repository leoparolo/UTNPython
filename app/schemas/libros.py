from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.autores import AutorRead
from app.schemas.categorias import CategoriaRead
from app.schemas.editoriales import EditorialRead
from app.schemas.ubicaciones import UbicacionRead

class LibroBase(BaseModel):
    titulo: str = Field(..., min_length=1)

class LibroCreate(LibroBase):
    isbn: str
    autor_id: int
    categoria_id: int
    editorial_id: int
    cantidad_ejemplares: int = Field(..., ge=0)
    ubicacion_id: int
    resumen: Optional[str] = None

class LibroUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1)
    autor_id: Optional[int] = None
    editorial_id: Optional[int] = None
    isbn: Optional[str] = None
    categoria_id: Optional[int] = None
    cantidad_ejemplares: Optional[int] = Field(None, ge=0)
    ejemplares_disponibles: Optional[int] = Field(None, ge=0)
    ubicacion_id: Optional[int] = None
    resumen: Optional[str] = None

class LibroRead(LibroBase):
    libro_id: int
    isbn: str
    autor: AutorRead
    resumen: Optional[str] = None
    categoria: CategoriaRead
    editorial: EditorialRead
    ejemplares_disponibles: int
    cantidad_ejemplares: int
    ubicacion: UbicacionRead

    model_config = {"from_attributes": True}
