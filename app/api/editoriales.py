from typing import List
from fastapi import APIRouter
from app.core.editoriales import db
from app.schemas.editoriales import EditorialRead

router = APIRouter(tags=["Editoriales API"])

@router.get("/editoriales/", response_model=List[EditorialRead])
def listar_editoriales():
    return db.get_todos()
