from pydantic import BaseModel

class EditorialRead(BaseModel):
    editorial_id: int
    nombre: str
    model_config = {"from_attributes": True}