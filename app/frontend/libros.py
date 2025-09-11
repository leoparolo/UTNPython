from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.libros import db_libros as db

router = APIRouter(tags=["Frontend Libros"])
templates = Jinja2Templates(directory="templates")

@router.get("/libros", response_class=HTMLResponse)
async def list_libros(request: Request):
    libros = db.get_todos()
    return templates.TemplateResponse("libros/list.html", {"request": request, "libros": libros})

@router.get("/libros/create", response_class=HTMLResponse)
async def mostrar_formulario_creacion(request: Request):
    # Si necesitas pasar datos extra (editoriales, autores, etc.), agrégalos aquí
    return templates.TemplateResponse("libros/create.html", {"request": request})

@router.get("/libros/{libro_id}", response_class=HTMLResponse)
async def detail_libro_html(request: Request, libro_id: str):
    try:
        libro_id_int = int(libro_id)
        if libro_id_int <= 0:
            raise ValueError
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=f"El ID debe ser un número entero positivo. Se recibió: {libro_id}"
        )
    libro = db.get_por_id(libro_id_int)
    if not libro:
        raise HTTPException(
            status_code=404,
            detail=f"Libro con ID {libro_id_int} no encontrado"
        )
    return templates.TemplateResponse("libros/detail.html", {
        "request": request,
        "libro": libro,
        "libro_id": libro_id_int
    })