import httpx
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.core.logging_config import logger
from app.schemas.prestamos import PrestamoCreate,PrestamoDetalleRead

router = APIRouter(tags=["Frontend Préstamos"])
templates = Jinja2Templates(directory="templates")

@router.get("/prestamos",
            response_class=HTMLResponse,
            summary="Listar prestamos",
            description="Obtiene todos los prestamos desde la API backend y los renderiza en una plantilla HTML.",
            response_description="Página HTML con la lista de prestamos."
            )
async def list_prestamos(request: Request):
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        response = await client.get("/prestamos/")
        if response.status_code != 200:
            error_msg = response.json().get("detail", "Sin detalle en respuesta de API")
            logger.exception("Error al obtener prestamos: %s", error_msg)
            raise HTTPException(status_code=response.status_code,
                                detail="Error al obtener prestamos")
        prestamos = response.json()
        return templates.TemplateResponse("prestamos/list.html", {
        "request": request,
        "prestamos": prestamos,
        "mensaje": None
        })

@router.get("/prestamos/create",
            response_class=HTMLResponse,
            summary="Formulario HTML para crear un préstamo",
            response_description="Devuelve un formulario HTML para crear un nuevo préstamo.")
async def mostrar_formulario_creacion(request: Request):
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        resp_libros = await client.get("/libros/")
        resp_usuarios = await client.get("/usuarios/")
        if resp_libros.status_code != 200 or resp_usuarios.status_code != 200:
            raise HTTPException(status_code=500, detail="Error al obtener libros o usuarios")

        libros = resp_libros.json()
        usuarios = resp_usuarios.json()
    return templates.TemplateResponse("prestamos/create.html", {
        "request": request,
        "libros": libros,
        "usuarios": usuarios
        })

@router.post("/prestamos/",
            response_class=HTMLResponse,
            summary="Crear un préstamo",
            description="Obtiene los datos del formulario, crea un préstamo mediante la API backend y redirige a la lista de préstamos.",
            response_description="formulario HTML listando préstamos.")
async def crear_prestamo_front(
    request: Request,
    usuario_id: int = Form(...),
    libro_id: int = Form(...)
):
    try:
        prestamo_data = PrestamoCreate(usuario_id=usuario_id, libro_id=libro_id)

        async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
            resp = await client.post("/prestamos/", json=prestamo_data.model_dump())

            if resp.status_code not in (200, 303):
                error_msg = resp.json().get("detail", "No se pudo crear el préstamo")
                logger.exception("Error al crear préstamo: %s", error_msg)
                resp_usuarios = await client.get("/usuarios/")
                resp_libros = await client.get("/libros/")
                usuarios = resp_usuarios.json()
                libros = resp_libros.json()
                return templates.TemplateResponse(
                    "prestamos/create.html",
                    {
                        "request": request,
                        "usuarios": usuarios,
                        "libros": libros,
                        "error": "No se pudo crear el préstamo."
                    })

            resp_prestamos = await client.get("/prestamos/")
            prestamos = resp_prestamos.json()  
            mensaje = "Préstamo creado correctamente."

        return templates.TemplateResponse("prestamos/list.html", {
        "request": request,
        "prestamos": prestamos,
        "mensaje": {"tipo": "success", "texto": mensaje}
        })

    except Exception as e:
        resp_usuarios = await client.get("/usuarios/")
        resp_libros = await client.get("/libros/")
        usuarios = resp_usuarios.json()
        libros = resp_libros.json()
        logger.exception("Excepción al crear préstamo: %s", e)
        return templates.TemplateResponse(
            "prestamos/create.html",
            {
                "request": request,
                "usuarios": usuarios,
                "libros": libros,
                "error": "No se pudo crear el préstamo. " + str(e)
            },
            status_code=500
        )

@router.post("/prestamos/{prestamo_id}/finalizar",
            response_class=HTMLResponse,
            summary="Registar la devolución de un préstamo",
            description="Obtiene el préstamo, lo actualiza mediante la API backend y redirige a la lista de préstamos.",
            response_description="formulario HTML listando préstamos.")
async def registrar_devolucion(request: Request, prestamo_id: int):
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        resp = await client.post(f"/prestamos/{prestamo_id}/devolucion")
        if resp.status_code not in (200, 303):
            error_msg = resp.json().get("detail", "Error al registrar devolución")
            logger.exception("Error al registrar devolución: %s", error_msg)
            resp_prestamos = await client.get("/prestamos/")
            prestamos = resp_prestamos.json()  

            return templates.TemplateResponse("prestamos/list.html", {
                "request": request,
                "prestamos": prestamos,
                "mensaje": {"tipo": "danger", "texto": error_msg}
            })

        resp_prestamos = await client.get("/prestamos/")
        prestamos = resp_prestamos.json()  
        mensaje = "El libro fue devuelto correctamente."

        return templates.TemplateResponse("prestamos/list.html", {
        "request": request,
        "prestamos": prestamos,
        "mensaje": {"tipo": "success", "texto": mensaje}
        })