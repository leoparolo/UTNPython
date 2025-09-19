from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from app.schemas.libros import LibroRead, LibroCreate, LibroUpdate
from app.core.libros import db

router = APIRouter(tags=["Libros API"])

@router.get("/libros/",
            response_model=list[LibroRead],
            summary="Listar libros",
            description="Obtiene todos los libros de la base de datos con paginación y búsqueda opcional.",
            response_description="Lista de libros")
def listar_libros():
    return db.get_todos()

@router.get("/libros/{libro_id}",
            response_model=LibroRead,
            summary="Obtener un libro",
            description="Obtiene un libro de la base de datos por su ID.",
            response_description="datos del libro")
def obtener_libro(libro_id: int):
    libro = db.get_por_id(libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@router.post("/libros/",
            response_model=LibroRead,
            summary="Crear un libro",
            description="Obtiene los datos del libro y lo crea en la base de datos.")
def crear_libro(libro: LibroCreate):
    data = libro.model_dump()
    try:
        libro = db.crear(data)
        return RedirectResponse(url="/libros", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.post("/libros/{libro_id}/update",
            response_model=LibroRead,
            summary="Actualizar un libro",
            description="Obtiene los datos del libro y actualiza la información en la base de datos.")
def actualizar_libro(
    libro_id: int,
    libro: LibroUpdate
):
    try:
        datos = libro.model_dump(exclude_unset=True)
        libro = db.actualizar(libro_id, datos)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return RedirectResponse(url="/libros", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.delete("/libros/{libro_id}/eliminar",
            summary="Eliminar un libro",
            description="Elimina un libro de la base de datos por su ID.")
def eliminar_libro(libro_id: int):
    try:
        libro = db.eliminar(libro_id)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return RedirectResponse(url="/libros", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
