from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from app.schemas.autores import AutorRead, AutorCreate, AutorUpdate
from app.core.autores import db

router = APIRouter(tags=["Autores API"])

@router.get("/autores/",
            response_model=list[AutorRead],
            summary="Listar autores",
            description="Obtiene todos los autores de la base de datos.",
            response_description="Lista de autores")
def listar_autores():
    return db.get_todos()

@router.get("/autores/{autor_id}",
            response_model=AutorRead,
            summary="Obtener un autor",
            description="Obtiene un autor de la base de datos por su ID.",
            response_description="datos del autor")
def obtener_autor(autor_id: int):
    autor = db.get_por_id(autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor

@router.post("/autores/",
            response_model=AutorRead,
            summary="Crear un autor",
            description="Obtiene los datos del autor y lo crea en la base de datos.")
def crear_autor(autor: AutorCreate):
    data = autor.model_dump()
    try:
        autor = db.crear(data)
        return RedirectResponse(url="/autores", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.post("/autores/{autor_id}/update",
            response_model=AutorRead,
            summary="Actualizar un autor",
            description="Obtiene los datos del autor y actualiza la información en la base de datos.")
def actualizar_autor(
    autor_id: int,
    autor: AutorUpdate
):
    try:
        datos = autor.model_dump(exclude_unset=True)
        autor = db.actualizar(autor_id, datos)
        if not autor:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return RedirectResponse(url="/autores", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.delete("/autores/{autor_id}/eliminar",
            response_model=AutorRead,
            summary="Eliminar un autor",
            description="Elimina un autor de la base de datos por su ID.")
def eliminar_autor(autor_id: int):
    try:
        autor = db.eliminar(autor_id)
        if not autor:
            raise HTTPException(status_code=404, detail="Autor no encontrado")
        return RedirectResponse(url="/autores", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
