from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.prestamos import db_prestamos as db

router = APIRouter(tags=["Frontend Prestamos"])
templates = Jinja2Templates(directory="templates")

@router.get("/prestamos", response_class=HTMLResponse)
async def list_prestamos(request: Request):
    prestamos = db.get_todos()
    return templates.TemplateResponse("prestamos/list.html", {"request": request, "prestamos": prestamos})

@router.get("/prestamos/create", response_class=HTMLResponse)
async def mostrar_formulario_creacion(request: Request):
    # Si necesitas pasar datos extra (usuarios, libros, etc.), agrégalos aquí
    return templates.TemplateResponse("prestamos/create.html", {"request": request})

@router.get("/prestamos/{prestamo_id}", response_class=HTMLResponse)
async def detail_prestamo_html(request: Request, prestamo_id: str):
    try:
        prestamo_id_int = int(prestamo_id)
        if prestamo_id_int <= 0:
            raise ValueError
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=f"El ID debe ser un número entero positivo. Se recibió: {prestamo_id}"
        )
    prestamo = db.get_por_id(prestamo_id_int)
    if not prestamo:
        raise HTTPException(
            status_code=404,
            detail=f"Préstamo con ID {prestamo_id_int} no encontrado"
        )
    return templates.TemplateResponse("prestamos/detail.html", {
        "request": request,
        "prestamo": prestamo,
        "prestamo_id": prestamo_id_int
    })