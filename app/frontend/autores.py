import httpx
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.core.logging_config import logger
from app.schemas.autores import AutorCreate, AutorUpdate


router = APIRouter(tags=["Frontend Autores"])
templates = Jinja2Templates(directory="templates")

@router.get("/autores",
            response_class=HTMLResponse,
            summary="Listar autores",
            description="Obtiene todos los autores desde la API backend y los renderiza en una plantilla HTML.",
            response_description="Página HTML con la lista de autores."
            )
async def list_autores(request: Request):
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        response = await client.get("/autores/")
        if response.status_code != 200:
            error_msg = response.json().get("detail", "Sin detalle en respuesta de API")
            logger.exception("Error al obtener autores: %s", error_msg)
            raise HTTPException(status_code=response.status_code,
                                detail="Error al obtener autores")
        autores = response.json()
        return templates.TemplateResponse("autores/list.html", {
        "request": request,
        "autores": autores,
        "mensaje": None
        })

@router.get("/autores/create",
            response_class=HTMLResponse,
            summary="Formulario HTML para crear un autor",
            response_description="Devuelve un formulario HTML para crear un nuevo autor.")
async def mostrar_formulario_creacion(request: Request):
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        nacionalidades = await client.get("/nacionalidades/")
        if nacionalidades.status_code != 200:
            error_msg = nacionalidades.json().get("detail", "Sin detalle en respuesta de API")
            logger.exception("Error al obtener nacionalidades: %s", error_msg)
            raise HTTPException(status_code=nacionalidades.status_code,
                                detail="Error al obtener nacionalidades")
        nacionalidades = nacionalidades.json()
        return templates.TemplateResponse("autores/create.html", {
        "request": request,
        "nacionalidades": nacionalidades
        })

@router.post("/autores/",
            response_class=HTMLResponse,
            summary="Crear un autor",
            description="Obtiene los datos del formulario, crea un autor mediante la API backend y redirige a la lista de autores.",
            response_description="formulario HTML listando autores.")
async def crear_usuario_front(
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

            if resp.status_code not in (200, 303):
                error_msg = resp.json().get("detail", "No se pudo crear el autor")
                logger.exception("Error al crear autor: %s", error_msg)
                nacionalidades = await client.get("/nacionalidades/")
                if nacionalidades.status_code != 200:
                    error_msg = nacionalidades.json().get("detail", "Sin detalle en respuesta de API")
                    logger.exception("Error al obtener nacionalidades: %s", error_msg)
                    raise HTTPException(status_code=nacionalidades.status_code,
                                        detail="Error al obtener nacionalidades")
                nacionalidades = nacionalidades.json()
                return templates.TemplateResponse("autores/create.html", {
                "request": request,
                "nacionalidades": nacionalidades
                })

            response = await client.get("/autores/")
            autores = response.json()
        mensaje = "Autor creado correctamente."
        return templates.TemplateResponse("autores/list.html", {
        "request": request,
        "autores": autores,
        "mensaje": {"tipo": "success", "texto": mensaje}
        })

    except Exception as e:
        async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
            logger.exception("Error al crear autor: %s", e)
            nacionalidades = await client.get("/nacionalidades/")
            if nacionalidades.status_code != 200:
                error_msg = nacionalidades.json().get("detail", "Sin detalle en respuesta de API")
                logger.exception("Error al obtener nacionalidades: %s", error_msg)
                raise HTTPException(status_code=nacionalidades.status_code,
                                        detail="Error al obtener nacionalidades") from e
            nacionalidades = nacionalidades.json()
            return templates.TemplateResponse("autores/create.html", {
                "request": request,
                "nacionalidades": nacionalidades
                })

@router.get("/autores/{autor_id}",
            response_class=HTMLResponse,
            summary="Formulario HTML para actualizar un autor.",
            description="Envia un formulario HTML detallando un autor específico obtenido desde la API backend.",
            response_description="formulario HTML para ver el detalle de un autor.")
async def detalle_autor(request: Request,autor_id: str):
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        response_autor = await client.get(f"/autores/{autor_id}")
        response_nacionalidades = await client.get("/nacionalidades/")
        if response_autor.status_code != 200:
            error_msg = response_autor.json().get("detail", "Sin detalle en respuesta de API")
            logger.exception("Error al obtener autor: %s", error_msg)
            raise HTTPException(status_code=response_autor.status_code,
                                detail="Error al obtener autor")
        if response_nacionalidades.status_code != 200:
            error_msg = response_nacionalidades.json().get("detail", "Sin detalle en respuesta de API")
            logger.exception("Error al obtener nacionalidades: %s", error_msg)
            raise HTTPException(status_code=response_nacionalidades.status_code,
                                detail="Error al obtener nacionalidades")
        autor = response_autor.json()
        nacionalidades = response_nacionalidades.json()
        try:
            autor_id_int = int(autor_id)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail="El ID del autor debe ser un número entero válido."
            ) from e

    return templates.TemplateResponse("autores/detail.html", {
        "request": request,
        "autor": autor,
        "autor_id": autor_id_int,
        "nacionalidades": nacionalidades
    })

@router.post("/autores/{autor_id}/update",
            response_class=HTMLResponse,
            summary="Actualizar un autor",
            description="Obtiene los datos del formulario, actualiza el autor mediante la API backend y redirige a la lista de autores.",
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
            resp = await client.post(
                f"/autores/{autor_id}/update",
                json=autor_update.model_dump())

        if resp.status_code not in (200, 303):
            async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
                response_nacionalidades = await client.get("/nacionalidades/")
                nacionalidades = response_nacionalidades.json()
            return templates.TemplateResponse("autores/detail.html", {
                "request": request,
                "autor": valores,
                "autor_id": autor_id,
                "nacionalidades": nacionalidades,
                "error": "No se pudo actualizar el autor:",
            })

        async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
            response = await client.get("/autores/")
            autores = response.json()

        mensaje = "Autor actualizado correctamente."
        return templates.TemplateResponse("autores/list.html", {
        "request": request,
        "autores": autores,
        "mensaje": {"tipo": "success", "texto": mensaje}
        })

    except Exception as e:
        logger.exception("Error al actualizar autor %s: %s", autor_id, e)
        return templates.TemplateResponse(
            "usuarios/detail.html",
            {
                "request": request,
                "usuario": valores,
                "error": f"No se pudo actualizar el usuario: {e}",
            },
            status_code=500,
        )

@router.post("/autores/{autor_id}/eliminar",
            response_class=HTMLResponse,
            summary="Eliminar un autor",
            description="Obtiene el ID del autor, lo elimina mediante la API backend y redirige a la lista de autores.",
            response_description="formulario HTML listando autores.")
async def eliminar_autor(request: Request, autor_id: int):
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        response = await client.delete(f"/autores/{autor_id}/eliminar")
        tipo = "success"
        if response.status_code != 303:
            mensaje = f"No se pudo eliminar el autor: {response.text}"
            tipo = "danger"
        else:
            mensaje = "Autor eliminado correctamente."
            tipo = "success"
        response_autores = await client.get("/autores/")
        if response_autores.status_code != 200:
            error_msg = response_autores.json().get("detail", "Sin detalle en respuesta de API")
            logger.exception("Error al obtener autores: %s", error_msg)
            raise HTTPException(status_code=response_autores.status_code,
                                detail="Error al obtener autores")
        autores = response_autores.json()
        return templates.TemplateResponse("autores/list.html", {
            "request": request,
            "autores": autores,
            "mensaje": {"tipo": tipo, "texto": mensaje}
        })

# @router.get("/autores/bio/{autor_id}", response_class=HTMLResponse)
# async def obtener_bio_wikipedia(request: Request, autor_id: int):
#     print("entro al metodo")
#     resumen = None
#     error = None

#     autor = db.get_por_id(autor_id)
#     nacionalidades = db_nacionalidades.get_todos(order_by=Nacionalidad.sdes)

#     if autor and autor.nombre:
#         nombre_wiki = autor.nombre.replace(" ", "_") 
#         url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{nombre_wiki}"
#         print(url)
#         async with httpx.AsyncClient() as client:
#             resp = await client.get(url)
#             if resp.status_code == 200:
#                 data = resp.json()
#                 resumen = data.get("extract")
#                 autor.biografia = resumen
#             else:
#                 error = "No se encontró información en Wikipedia."
#     else:
#         error = "No se encontró el autor en la base de datos."

#     return templates.TemplateResponse(
#         "autores/detail.html",
#         {
#             "request": request,
#             "autor": autor,
#             "autor_id": autor_id,
#             "nacionalidades": nacionalidades
#         }
#     )
