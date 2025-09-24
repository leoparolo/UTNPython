from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter
from app.schemas.autores import AutorRead, AutorCreate, AutorUpdate
from app.core.autores import db
from app.core.error import AppException
from app.core.logging_config import logger

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
        raise AppException(
            title="Autor no encontrado",
            detail=f"No existe un autor con id {autor_id}",
            status_code=404,
            type_="about:blank"
        )
    return autor

@router.post("/autores/",
            status_code=204,
            summary="Crear un autor",
            description="Obtiene los datos del autor y lo crea en la base de datos.")
def crear_autor(autor: AutorCreate):
    data = autor.model_dump()
    try:
        db.crear(data)
        return None
    except Exception as e:
        raise AppException(
            title="Error al crear autor",
            detail=str(e),
            status_code=400,
            type_="about:blank"
        ) from e

@router.put("/autores/{autor_id}/update",
            status_code=204,
            summary="Actualizar un autor",
            description="Obtiene los datos del autor y actualiza la información en la base de datos.")
def actualizar_autor(
    autor_id: int,
    autor: AutorUpdate
):
    try:
        datos = autor.model_dump(exclude_unset=True)
        autor_actualizado = db.actualizar(autor_id, datos)
        if not autor_actualizado:
            raise AppException(
                title="Autor no encontrado",
                detail=f"No existe un autor con id {autor_id}",
                status_code=404,
                type_="about:blank"
            )

        return None

    except SQLAlchemyError as e:
        logger.exception("Error de base de datos al actualizar autor %s", autor_id)
        raise AppException(
            title="Error en base de datos",
            detail=str(e),
            status_code=500,
            type_="about:blank"
        ) from e
    except Exception as e:
        logger.exception("Error inesperado al actualizar autor %s", autor_id)
        raise AppException(
            title="Error inesperado",
            detail=str(e),
            status_code=500,
            type_="about:blank"
        ) from e

@router.delete("/autores/{autor_id}/eliminar",
            status_code=204,
            summary="Eliminar un autor",
            description="Elimina un autor de la base de datos por su ID.")
def eliminar_autor(autor_id: int):
    try:
        autor_eliminado = db.eliminar(autor_id)

        if not autor_eliminado:
            raise AppException(
                title="Autor no encontrado",
                detail=f"No existe un autor con id {autor_id}",
                status_code=404,
                type_="about:blank"
            )

        return None

    except SQLAlchemyError as e:
        logger.exception("Error de base de datos al eliminar autor %s", autor_id)
        raise AppException(
            title="Error en base de datos",
            detail=str(e),
            status_code=500,
            type_="about:blank"
        ) from e
    except Exception as e:
        logger.exception("Error inesperado al eliminar autor %s", autor_id)
        raise AppException(
            title="Error inesperado",
            detail=str(e),
            status_code=500,
            type_="about:blank"
        ) from e
