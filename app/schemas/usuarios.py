from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.schemas.roles import RolRead
from app.schemas.estados_usuario import EstadosRead

class UsuarioBase(BaseModel):
    dni: str = Field(..., min_length=7, max_length=12)
    nombre: str = Field(..., min_length=1)
    apellido: str = Field(..., min_length=1)
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    """Esquema para crear usuarios (estado se setea en backend)"""
    rol_id: int

class UsuarioUpdate(BaseModel):
    """Esquema para actualizar (campos opcionales)"""
    dni: Optional[str] = Field(None, min_length=7, max_length=12)
    nombre: Optional[str] = Field(None, min_length=1)
    apellido: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    rol_id: Optional[int] = None
    estado_id: Optional[int] = None

class UsuarioRead(UsuarioBase):
    usuario_id: int
    rol: RolRead
    estado: EstadosRead

    model_config = {"from_attributes": True}
