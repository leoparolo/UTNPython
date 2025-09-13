from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.prestamos import db_prestamos as db
from app.core.libros import db_libros
from app.core.usuarios import db as db_usuarios

router = APIRouter(tags=["Frontend Prestamos"])
templates = Jinja2Templates(directory="templates")

@router.get("/prestamos", response_class=HTMLResponse)
async def list_prestamos(request: Request):
    prestamos = db.get_todos()
    return templates.TemplateResponse("prestamos/list.html", {"request": request, "prestamos": prestamos})

@router.get("/prestamos/create", response_class=HTMLResponse)
async def mostrar_formulario_creacion(request: Request):
    libros = db_libros.get_todos()
    usuarios = db_usuarios.get_todos()
    
    # Si necesitas pasar datos extra (usuarios, libros, etc.), agrégalos aquí
    return templates.TemplateResponse("prestamos/create.html", {
        "request": request,
        "libros": libros,
        "usuarios": usuarios
        })

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
    
@router.post("/", response_class=HTMLResponse)
async def crear_prestamo_frontend(
    request: Request,
    usuario_id: int = Form(...),
    libro_id: int = Form(...)
):
    try:
        prestamo, error = db.crear(usuario_id=usuario_id, libro_id=libro_id)
        if error:
            raise Exception(error)
        return HTTPException(status_code=303)
    except Exception as e:
        usuarios = db_usuarios.get_todos()
        libros = db_libros.get_todos()
        return templates.TemplateResponse(
            "prestamos/create.html",
            {
                "request": request,
                "usuarios": usuarios,
                "libros": libros,
                "error": "No se pudo crear el préstamo. " + str(e)
            },
            status_code=400
        )