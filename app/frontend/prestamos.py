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
        libros = await client.get("/libros/")
        usuarios = await client.get("/usuarios/")
        if libros.status_code != 200 or usuarios.status_code != 200:
            raise HTTPException(status_code=500, detail="Error al obtener libros o usuarios")

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

@router.get("/prestamos/{prestamo_id}",
            response_class=HTMLResponse,
            summary="Formulario HTML para actualizar un préstamo.",
            description="Envia un formulario HTML detallando un préstamo específico obtenido desde la API backend.",
            response_description="formulario HTML para ver el detalle de un préstamo.")
async def detalle_prestamo(request: Request, prestamo_id: str):
    try:
        id_prestamo = PrestamoDetalleRead(prestamo_id=prestamo_id)

        async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
            resp_prestamo = await client.get(f"/prestamos/{id_prestamo.prestamo_id}")
            if resp_prestamo.status_code != 200:
                raise HTTPException(
                    status_code=resp_prestamo.status_code,
                    detail=f"Error al obtener el préstamo con ID {id_prestamo.prestamo_id}"
                )
            prestamo = resp_prestamo.json()

        return templates.TemplateResponse("prestamos/detail.html", {
        "request": request,
        "prestamo": prestamo,
        "prestamo_id": id_prestamo.prestamo_id
        })
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"El ID debe ser un número entero positivo. Se recibió: {prestamo_id}"
        ) from e
