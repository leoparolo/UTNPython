from pydantic import BaseModel

class NacionalidadRead(BaseModel):
    nacionalidad_id: int
    sdes: str
    model_config = {"from_attributes": True}