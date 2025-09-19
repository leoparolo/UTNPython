from pydantic import BaseModel

class UbicacionRead(BaseModel):
    ubicacion_id: int
    nombre: str
    model_config = {"from_attributes": True}