from pydantic import BaseModel

class CategoriaRead(BaseModel):
    categoria_id: int
    nombre: str
    model_config = {"from_attributes": True}