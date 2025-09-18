from pydantic import BaseModel

class EstadosRead(BaseModel):
    estado_id: int
    nombre: str
    model_config = {"from_attributes": True}