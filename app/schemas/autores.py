from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, field_validator
from app.schemas.nacionalidades import NacionalidadRead

class AutorBase(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: Optional[date] = None
    biografia: Optional[str] = None

class AutorCreate(AutorBase):
    """Esquema para crear autores"""
    nacionalidad_id: int

class AutorUpdate(BaseModel):
    """Esquema para actualizar (campos opcionales)"""
    nombre: Optional[str] = Field(None, min_length=1)
    apellido: Optional[str] = Field(None, min_length=1)
    fecha_nacimiento: Optional[date] = None
    biografia: Optional[str] = None
    nacionalidad_id: Optional[int] = None

    @field_validator("fecha_nacimiento")
    def validar_fecha(cls, v: Optional[date]): # pylint: disable=no-self-argument
        if v:
            hoy = date.today()
            if v > hoy:
                raise ValueError("La fecha de nacimiento no puede ser futura")
            if (hoy.year - v.year) > 150:
                raise ValueError("La fecha de nacimiento es demasiado antigua")
        return v

class AutorRead(AutorBase):
    autor_id: int
    nacionalidad: Optional[NacionalidadRead] = None
    model_config = {
        "from_attributes": True
    }
