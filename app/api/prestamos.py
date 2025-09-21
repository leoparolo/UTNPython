from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from app.schemas.prestamos import PrestamoCreate, PrestamoRead
from app.core.prestamos import db

router = APIRouter(tags=["Préstamos API"])

@router.get("/prestamos/",
            response_model=list[PrestamoRead],
            summary="Listar préstamos",
            description="Obtiene todos los préstamos de la base de datos.",
            response_description="Lista de préstamos")
def listar_prestamos():
    prestamos = db.get_todos()
    return [
        PrestamoRead(
            prestamo_id=p.prestamo_id,
            usuario=p.usuario,
            libro=p.libro,
            fecha_prestamo=p.fecha_prestamo,
            fecha_devolucion_esperada=p.fecha_devolucion_esperada,
            fecha_devolucion_real=p.fecha_devolucion_real,
            estado=p.estado_calculado
        )
        for p in prestamos
    ]

@router.post("/prestamos/",
            response_model=list[PrestamoRead],
            summary="Crear un préstamo",
            description="Obtiene los datos del préstamo y lo crea en la base de datos."
            )
def crear_prestamo(prestamo: PrestamoCreate):
    data = prestamo.model_dump()
    try:
        prestamo = db.crear(data)
        return RedirectResponse(url="/prestamos", status_code=HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e)) from e


@router.post("/prestamos/{prestamo_id}/devolucion", response_model=PrestamoRead)
def devolver_prestamo(prestamo_id: int):
    prestamo, error = db.devolver(prestamo_id)
    if error:
        if error == "Préstamo no encontrado":
            raise HTTPException(404, error)
        raise HTTPException(400, error)
    return prestamo
