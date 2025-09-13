from pydantic import BaseModel, Field
from datetime import date
from typing import Literal

PrestamoEstado = Literal["activo"]

class PrestamoCreate(BaseModel):
    usuario_id: int
    libro_id: int

class PrestamoDevolucion(BaseModel):
    fecha_devolucion: date | None = None

class PrestamoRead(BaseModel):
    prestamo_id: int
    usuario_id: int
    libro_id: int
    fecha_prestamo: date
    fecha_devolucion_esperada: date
    estado: PrestamoEstado = Field("activo")

    model_config = {"from_attributes": True}

class PrestamoDetalle(PrestamoRead):
    usuario_nombre: str | None = None
    libro_titulo: str | None = None
