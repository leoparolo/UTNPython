from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.libros import db_libros as db
from app.core.categorias import db as db_cat
from app.core.autores import db as db_aut
from app.core.editoriales import db as db_edit
from app.core.ubicaciones import db as db_ubic


router = APIRouter(tags=["Frontend Libros"])
templates = Jinja2Templates(directory="templates")

@router.get("/libros", response_class=HTMLResponse)
async def list_libros(request: Request):
    libros = db.get_todos()
    return templates.TemplateResponse("libros/list.html", {"request": request, "libros": libros})

@router.get("/libros/create", response_class=HTMLResponse)
async def mostrar_formulario_creacion(request: Request):
    autores = db_aut.get_todos()
    categorias = db_cat.get_todos()
    editoriales = db_edit.get_todos()
    ubicaciones = db_ubic.get_todos()
    return templates.TemplateResponse(
        "libros/create.html",
        {
            "request": request,
            "autores": autores,
            "categorias": categorias,
            "editoriales": editoriales,
            "ubicaciones": ubicaciones
        })

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
    autores = db_aut.get_todos()
    categorias = db_cat.get_todos()
    editoriales = db_edit.get_todos()
    ubicaciones = db_ubic.get_todos()
    return templates.TemplateResponse("libros/detail.html", {
        "request": request,
        "libro": libro,
        "libro_id": libro_id_int,
        "autores": autores,
        "categorias": categorias,
        "editoriales": editoriales,
        "ubicaciones": ubicaciones
    })
    
@router.post("/", response_class=HTMLResponse)
async def crear_libro_frontend(
    request: Request,
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
        db.crear({
            "titulo": titulo,
            "isbn": isbn,
            "autor_id": autor_id,
            "categoria_id": categoria_id,
            "editorial_id": editorial_id,
            "cantidad_ejemplares": cantidad_ejemplares,
            "ubicacion_id": ubicacion_id,
            "resumen": resumen
        })
        return HTMLResponse(status_code=303)
    except Exception as e:
        autores = db_aut.get_todos()
        categorias = db_cat.get_todos()
        editoriales = db_edit.get_todos()
        ubicaciones = db_ubic.get_todos()
        return templates.TemplateResponse(
            "libros/create.html",
            {
                "request": request,
                "autores": autores,
                "categorias": categorias,
                "editoriales": editoriales,
                "ubicaciones": ubicaciones,
                "error": "No se pudo crear el libro. " + str(e)
            },
            status_code=400
        )
        
@router.post("/libros/{libro_id}/update", response_class=HTMLResponse)
async def actualizar_libro_frontend(
    request: Request,
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
    try:
        db.actualizar(libro_id, {
            "titulo": titulo,
            "isbn": isbn,
            "autor_id": autor_id,
            "categoria_id": categoria_id,
            "editorial_id": editorial_id,
            "cantidad_ejemplares": cantidad_ejemplares,
            "ubicacion_id": ubicacion_id,
            "resumen": resumen
        })
        return HTTPException(status_code=303)
    except Exception as e:
        autores = db_aut.get_todos()
        categorias = db_cat.get_todos()
        editoriales = db_edit.get_todos()
        ubicaciones = db_ubic.get_todos()
        libro = db.get_por_id(libro_id)
        return templates.TemplateResponse(
            "libros/detail.html",
            {
                "request": request,
                "libro": libro,
                "libro_id": libro_id,
                "autores": autores,
                "categorias": categorias,
                "editoriales": editoriales,
                "ubicaciones": ubicaciones,
                "error": "No se pudo actualizar el libro. " + str(e)
            },
            status_code=400
        )