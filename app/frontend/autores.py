import httpx
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_303_SEE_OTHER
from app.core.config import settings
from app.core.logging_config import logger
from app.schemas.autores import AutorCreate, AutorUpdate
from app.core.flash import set_flash
from app.frontend.http.autores import get as get_autores
from app.frontend.http.autores import get_one as get_autor
from app.frontend.http.nacionalidades import get as get_nacionalidades
from app.frontend.templateResponse.autores import render_detail,render_error_detail,render_list,render_create


router = APIRouter(tags=["Frontend Autores"])
templates = Jinja2Templates(directory="templates")

@router.get("/autores",
            response_class=HTMLResponse,
            summary="Listar autores",
            description="Obtiene todos los autores desde la API backend y los renderiza en una plantilla HTML.",
            response_description="Página HTML con la lista de autores."
            )
async def list_autores(request: Request):
    autores = await get_autores()
    if autores.success:
        autores = autores.data
    else:
        autores = []
    return render_list(request, autores)

@router.get("/autores/create",
            response_class=HTMLResponse,
            summary="Formulario HTML para crear un autor",
            response_description="Devuelve un formulario HTML para crear un nuevo autor.")
async def mostrar_formulario_creacion(request: Request):
    nacionalidades = await get_nacionalidades()
    if nacionalidades.success:
        nacionalidades = nacionalidades.data
    else:
        nacionalidades = []
    return render_create(request,nacionalidades)

@router.post("/autores/",
            response_class=HTMLResponse,
            summary="Crear un autor",
            description="Obtiene los datos del formulario, crea un autor mediante la API backend.",
            response_description="formulario HTML listando autores.")
async def crear_autor_front(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    fecha_nacimiento: str = Form(...),
    nacionalidad_id: int = Form(...),
    biografia: str = Form(...)
):
    valores = {
        "nombre": nombre,
        "apellido": apellido,
        "fecha_nacimiento": fecha_nacimiento,
        "nacionalidad_id": nacionalidad_id,
        "biografia": biografia
    }
    try:
        autor = AutorCreate(**valores)
        async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
            resp = await client.post("/autores/", json=autor.model_dump(mode="json"))
            if resp.status_code not in (200,204, 303):
                return RedirectResponse(
                        url="/autores/create",
                        status_code=HTTP_303_SEE_OTHER
                    )
            set_flash(request, "success", "Autor creado correctamente.")
            return RedirectResponse(
                url=request.url_for("list_autores"),
                status_code=HTTP_303_SEE_OTHER
            )
    except Exception:
        return RedirectResponse(
                        url="/autores/create",
                        status_code=HTTP_303_SEE_OTHER
                    )

@router.get("/autores/{autor_id}",
            response_class=HTMLResponse,
            summary="Formulario HTML para actualizar un autor.",
            description="Envia un formulario HTML detallando un autor específico obtenido desde la API backend.",
            response_description="formulario HTML para ver el detalle de un autor.")
async def detalle_autor(request: Request,autor_id: str):
    autor = await get_autor(autor_id)
    if autor.success:
        autor = autor.data
    else:
        autor = []
    nacionalidades = await get_nacionalidades()
    if nacionalidades.success:
        nacionalidades = nacionalidades.data
    else:
        nacionalidades = []
    return render_detail(request,autor,nacionalidades)

@router.post("/autores/{autor_id}/update",
            response_class=HTMLResponse,
            summary="Actualizar un autor",
            description="Obtiene los datos del formulario,actualiza el autor",
            response_description="formulario HTML listando autores")
async def actualizar_autor_front(
    request: Request,
    autor_id: int,
    nombre: str = Form(...),
    apellido: str = Form(...),
    fecha_nacimiento: str = Form(...),
    nacionalidad_id: int = Form(...),
    biografia: str = Form(...)
):
    valores = {
        "autor_id": autor_id,
        "nombre": nombre,
        "apellido": apellido,
        "fecha_nacimiento": fecha_nacimiento,
        "nacionalidad_id": nacionalidad_id,
        "biografia": biografia
    }
    try:
        autor_update = AutorUpdate(**valores)
        async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
            resp = await client.put(
                f"/autores/{autor_id}/update",
                json=autor_update.model_dump(mode="json"))
            if resp.status_code not in (200,204):
                error_msg = resp.json().get("detail", "Sin detalle en respuesta de API")
                logger.exception("Error al actualizar autor %s: %s",autor_id, error_msg)
                return await render_error_detail(request, valores)
        set_flash(request, "success", "Autor actualizado correctamente.")
        return RedirectResponse(
            url="/autores",
            status_code=HTTP_303_SEE_OTHER
        )
    except Exception as e:
        logger.exception("Error al actualizar autor %s: %s", autor_id, e)
        return await render_error_detail(request, valores)

@router.post("/autores/{autor_id}/eliminar",
            response_class=HTMLResponse,
            summary="Eliminar un autor",
            description="Obtiene el ID del autor, lo elimina mediante la API backend",
            response_description="formulario HTML listando autores.")
async def eliminar_autor(request: Request, autor_id: int):
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        response = await client.delete(f"/autores/{autor_id}/eliminar")
        if response.status_code not in (200, 303):
            error_msg = response.json().get("detail", "Sin detalle en respuesta de API")
            logger.exception("Error al eliminar autor %s: %s",autor_id, error_msg)
            raise HTTPException(status_code=response.status_code,
                                detail="Error al eliminar autor")
        set_flash(request, "success", "Autor eliminado correctamente.")
        return RedirectResponse(
            url="/autores",
            status_code=HTTP_303_SEE_OTHER
        )

@router.post("/autores/bio/{autor_id}", response_class=HTMLResponse)
async def obtener_bio_wikipedia(request: Request, autor_id: int):
    autor = await get_autor(autor_id)
    if autor.success:
        autor = autor.data
    else:
        autor = []
    nacionalidades = await get_nacionalidades()
    if nacionalidades.success:
        nacionalidades = nacionalidades.data
    else:
        nacionalidades = []
    async with httpx.AsyncClient(base_url="https://es.wikipedia.org/api") as client_wiki:
        response_wiki = await client_wiki.get(
            f"/rest_v1/page/summary/{autor['nombre'].replace(' ', '_')}")
        if response_wiki.status_code != 200:
            error_msg = response_wiki.json().get("detail", "Sin detalle en respuesta de API")
            logger.exception("Error al obtener biografia de wikipedia: %s", error_msg)
            raise HTTPException(status_code=response_wiki.status_code,
                                detail="Error al obtener biografia wikipedia")
        data = response_wiki.json()
        resumen = data.get("extract", "No se encontró información en Wikipedia.")
        autor['biografia'] = resumen
        return templates.TemplateResponse("autores/detail.html", {
            "request": request,
            "autor": autor,
            "autor_id": autor_id,
            "nacionalidades": nacionalidades
        })
