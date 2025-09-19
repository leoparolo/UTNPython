from typing import List
from fastapi import APIRouter
from app.core.roles import db
from app.schemas.roles import RolRead

router = APIRouter(tags=["Roles API"])

@router.get("/roles/", response_model=List[RolRead])
def listar_roles():
    return db.get_todos()
