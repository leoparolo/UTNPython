from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from app.core.libros import db_libros
from app.schemas.libros import LibroCreate, LibroRead, LibroUpdate

router = APIRouter(prefix="/libros", tags=["Libros API"])

@router.get("/", response_model=List[LibroRead])
def listar_libros(q: Optional[str] = None, page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=200)):
    return db_libros.get_todos(q=q, page=page, size=size)

@router.get("/{libro_id}", response_model=LibroRead)
def obtener_libro(libro_id: int):
    libro = db_libros.get_por_id(libro_id)
    if not libro:
        raise HTTPException(404, "Libro no encontrado")
    return libro

@router.post("/", response_model=LibroRead, status_code=status.HTTP_201_CREATED)
def crear_libro(data: LibroCreate):
    try:
        return db_libros.crear(data.model_dump())
    except Exception:
        raise HTTPException(400, "No se pudo crear el libro")

@router.post("/{libro_id}/update", response_model=LibroRead)
def actualizar_libro(libro_id: int, data: LibroUpdate):
    libro = db_libros.actualizar(libro_id, data.model_dump(exclude_unset=True))
    if not libro:
        raise HTTPException(404, "Libro no encontrado")
    return libro

@router.post("/{libro_id}/eliminar", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(libro_id: int):
    libro = db_libros.eliminar(libro_id)
    if not libro:
        raise HTTPException(404, "Libro no encontrado")
