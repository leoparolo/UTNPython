from typing import List
from fastapi import APIRouter
from app.core.estados_usuarios import db
from app.schemas.estados_usuario import EstadosRead

router = APIRouter(tags=["Estados usuario API"])

@router.get("/api/estados/", response_model=List[EstadosRead])
def listar_estados():
    return db.get_todos()