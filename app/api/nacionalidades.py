from fastapi import APIRouter
from app.schemas.nacionalidades import NacionalidadRead
from app.core.nacionalidades import db

router = APIRouter(tags=["Nacionalidades API"])

@router.get("/nacionalidades/",
            response_model=list[NacionalidadRead],
            summary="Listar nacionalidades",
            description="Obtiene todas las nacionalidades de la base de datos.",
            response_description="Lista de nacionalidades")
def listar_nacionalidades():
    return db.get_todos()