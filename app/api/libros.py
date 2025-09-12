from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status, Form
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
def crear_libro(
    titulo: str = Form(...),
    isbn: int = Form(...),
    autor_id: int = Form(...),
    categoria_id: int = Form(...),
    editorial_id: int = Form(...),
    cantidad_ejemplares: int = Form(...),
    ubicacion_id: int = Form(...),
    resumen: str = Form("")
):
    try:
        return db_libros.crear({
            "titulo": titulo,
            "isbn": isbn,
            "autor_id": autor_id,
            "categoria_id": categoria_id,
            "editorial_id": editorial_id,
            "cantidad_ejemplares": cantidad_ejemplares,
            "ubicacion_id": ubicacion_id,
            "resumen": resumen
        })
    except Exception:
        raise HTTPException(400, "No se pudo crear el libro")

@router.post("/{libro_id}/update", response_model=LibroRead)
def actualizar_libro(
    libro_id: int,
    titulo: str = Form(...),
    isbn: int = Form(...),
    autor_id: int = Form(...),
    categoria_id: int = Form(...),
    editorial_id: int = Form(...),
    cantidad_ejemplares: int = Form(...),
    ubicacion_id: int = Form(...),
    resumen: str = Form("")
):
    libro = db_libros.actualizar(libro_id, {
        "titulo": titulo,
        "isbn": isbn,
        "autor_id": autor_id,
        "categoria_id": categoria_id,
        "editorial_id": editorial_id,
        "cantidad_ejemplares": cantidad_ejemplares,
        "ubicacion_id": ubicacion_id,
        "resumen": resumen
    })
    if not libro:
        raise HTTPException(404, "Libro no encontrado")
    return libro

@router.post("/{libro_id}/eliminar", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(libro_id: int):
    libro = db_libros.eliminar(libro_id)
    if not libro:
        raise HTTPException(404, "Libro no encontrado")
