from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_303_SEE_OTHER
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, HTTPException
from app.schemas.usuarios import UsuarioCreate, UsuarioUpdate, UsuarioRead
from app.core.usuarios import db

router = APIRouter(tags=["Usuarios API"])

@router.get("/usuarios/",
            response_model=list[UsuarioRead],
            summary="Listar usuarios",
            description="Obtiene todos los usuarios de la base de datos.",
            response_description="Lista de usuarios")
def listar_usuarios():
    return db.get_todos()

@router.get("/usuarios/{usuario_id}",
            response_model=UsuarioRead,
            summary="Obtener un usuario",
            description="Obtiene un usuario de la base de datos por su ID.",
            response_description="datos del usuario")
def obtener_usuario(usuario_id: int):
    usuario = db.get_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/usuarios/",
            response_model=UsuarioRead,
            summary="Crear un usuario",
            description="Obtiene los datos del usuario y lo crea en la base de datos.")
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


@router.post("/usuarios/{usuario_id}/update",
            response_model=UsuarioRead,
            summary="Actualizar un usuario",
            description="Obtiene los datos del usuario y actualiza la información en la base de datos.")
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

@router.delete("/usuarios/{usuario_id}/eliminar",
            response_model=UsuarioRead,
            summary="Eliminar un usuario",
            description="Elimina un usuario de la base de datos por su ID.")
def eliminar_usuario(usuario_id: int):
    try:
        usuario = db.eliminar(usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return RedirectResponse(url="/usuarios", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
