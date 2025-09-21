from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field
from app.schemas.usuarios import UsuarioRead
from app.schemas.libros import LibroRead

PrestamoEstado = Literal["activo"]

class PrestamoCreate(BaseModel):
    usuario_id: int = Field(..., ge=1, description="ID de usuario debe ser positivo")
    libro_id: int = Field(..., ge=1, description="ID de libro debe ser positivo")

class PrestamoDevolucion(BaseModel):
    fecha_devolucion: datetime | None = None

class PrestamoRead(BaseModel):
    prestamo_id: int
    usuario: UsuarioRead
    libro: LibroRead
    fecha_prestamo: datetime
    fecha_devolucion_esperada: datetime
    fecha_devolucion_real: datetime | None = None
    estado: str

    model_config = {"from_attributes": True}

class PrestamoDetalle(PrestamoRead):
    usuario_nombre: str | None = None
    libro_titulo: str | None = None

class PrestamoDetalleRead(BaseModel):
    prestamo_id: int = Field(..., ge=1, description="ID del préstamo debe ser positivo")
