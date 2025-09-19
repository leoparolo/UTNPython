from pydantic import BaseModel, Field
from datetime import date
from typing import Literal

PrestamoEstado = Literal["activo"]

class PrestamoCreate(BaseModel):
    usuario_id: int = Field(..., ge=1, description="ID de usuario debe ser positivo")
    libro_id: int = Field(..., ge=1, description="ID de libro debe ser positivo")

class PrestamoDevolucion(BaseModel):
    fecha_devolucion: date | None = None

class PrestamoRead(BaseModel):
    prestamo_id: int
    usuario_id: int
    libro_id: int
    fecha_prestamo: date
    fecha_devolucion_esperada: date
    estado_id: int

    model_config = {"from_attributes": True}

class PrestamoDetalle(PrestamoRead):
    usuario_nombre: str | None = None
    libro_titulo: str | None = None

class PrestamoDetalleRead(BaseModel):
    prestamo_id: int = Field(..., ge=1, description="ID del préstamo debe ser positivo")
