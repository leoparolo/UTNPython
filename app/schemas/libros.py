from pydantic import BaseModel, Field, field_validator
from typing import Optional

class LibroBase(BaseModel):
    titulo: str = Field(..., min_length=1)
    autor_id: int
    editorial_id: int
    isbn: Optional[str] = None
    categoria_id: Optional[int] = None
    cantidad_ejemplares: int = Field(0, ge=0)
    ejemplares_disponibles: int = Field(0, ge=0)
    ubicacion_id: Optional[int] = None
    resumen: Optional[str] = None

    # Consistencia básica: disponibles <= cantidad
    @field_validator("ejemplares_disponibles")
    @classmethod
    def validar_stock(cls, v, info):
        data = info.data  # valores ya validados del modelo
        cantidad = data.get("cantidad_ejemplares", 0)
        if v is not None and cantidad is not None and v > cantidad:
            raise ValueError("Los ejemplares disponibles no pueden superar la cantidad total.")
        return v

class LibroCreate(LibroBase):
    pass

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

    model_config = {"from_attributes": True}