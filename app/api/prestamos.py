from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from app.core.prestamos import db_prestamos
from app.schemas.prestamos import PrestamoCreate, PrestamoRead

router = APIRouter(prefix="/prestamos", tags=["Préstamos API"])

@router.get("/", response_model=List[PrestamoRead])
def listar_prestamos(
    estado: Optional[str] = None,
    usuario_id: Optional[int] = None,
    libro_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=200),
):
    return db_prestamos.get_todos(estado=estado, usuario_id=usuario_id, libro_id=libro_id, page=page, size=size)

@router.get("/{prestamo_id}", response_model=PrestamoRead)
def obtener_prestamo(prestamo_id: int):
    prestamo = db_prestamos.get_por_id(prestamo_id)
    if not prestamo:
        raise HTTPException(404, "Préstamo no encontrado")
    return prestamo

@router.post("/", response_model=PrestamoRead, status_code=status.HTTP_201_CREATED)
def crear_prestamo(data: PrestamoCreate):
    prestamo, error = db_prestamos.crear(usuario_id=data.usuario_id, libro_id=data.libro_id)
    if error:
        # 400 si es regla de negocio, 404 si no existe, 409 si conflicto de estado/stock
        if error in ("Usuario o Libro inexistente",):
            raise HTTPException(404, error)
        if error in ("No hay ejemplares disponibles de este libro",
                     "Ya existe un préstamo pendiente de este libro para el usuario",
                     "Usuario no habilitado para préstamos"):
            raise HTTPException(409, error)
        raise HTTPException(400, error)
    return prestamo

@router.post("/{prestamo_id}/devolver", response_model=PrestamoRead)
def devolver_prestamo(prestamo_id: int):
    prestamo, error = db_prestamos.devolver(prestamo_id)
    if error:
        if error == "Préstamo no encontrado":
            raise HTTPException(404, error)
        raise HTTPException(400, error)
    return prestamo
