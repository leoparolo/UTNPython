from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_303_SEE_OTHER
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, HTTPException
from app.schemas.usuarios import UsuarioCreate, UsuarioUpdate, UsuarioRead
from app.core.usuarios import db



router = APIRouter(tags=["Usuarios API"])

@router.get("/api/usuarios/", response_model=list[UsuarioRead])
def listar_usuarios():
    return db.get_todos()

@router.get("/api/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: int):
    usuario = db.get_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/api/usuarios/", response_model=UsuarioRead)
def crear_usuario(usuario: UsuarioCreate):
    data = usuario.model_dump()
    data["estado_id"] = 1  # Asignar estado por defecto (Activo)
    try:
        db.crear(data)
        return RedirectResponse(url="/usuarios", status_code=HTTP_303_SEE_OTHER)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=400,
            detail="El DNI ya existe. Ingrese un valor diferente."
        ) from exc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/api/usuarios/{usuario_id}/update", response_model=UsuarioRead)
def actualizar_usuario(
    usuario_id: int,
    usuario: UsuarioUpdate
):
    try:
        datos = usuario.model_dump(exclude_unset=True)
        usuario = db.actualizar(usuario_id, datos)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return RedirectResponse(url="/usuarios", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.post("/api/usuarios/{usuario_id}/eliminar", response_model=UsuarioRead)
def eliminar_usuario(usuario_id: int):
    try:
        usuario = db.eliminar(usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return RedirectResponse(url="/usuarios", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
