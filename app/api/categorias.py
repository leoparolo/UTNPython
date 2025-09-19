from typing import List
from fastapi import APIRouter
from app.core.categorias import db
from app.schemas.categorias import CategoriaRead

router = APIRouter(tags=["Editoriales API"])

@router.get("/categorias/", response_model=List[CategoriaRead])
def listar_categorias():
    return db.get_todos()
