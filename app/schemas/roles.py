from pydantic import BaseModel

class RolRead(BaseModel):
    rol_id: int
    nombre: str
    model_config = {"from_attributes": True}