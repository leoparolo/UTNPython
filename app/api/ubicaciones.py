from typing import List
from fastapi import APIRouter
from app.core.ubicaciones import db
from app.schemas.ubicaciones import UbicacionRead

router = APIRouter(tags=["Ubicaciones API"])

@router.get("/ubicaciones/", response_model=List[UbicacionRead])
def listar_ubicaciones():
    return db.get_todos()
