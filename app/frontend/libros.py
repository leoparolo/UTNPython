import httpx
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.core.logging_config import logger
from app.schemas.libros import LibroCreate, LibroUpdate


router = APIRouter(tags=["Frontend Libros"])
templates = Jinja2Templates(directory="templates")

@router.get("/libros",
            response_class=HTMLResponse,
            summary="Listar libros",
            description="Obtiene todos los libros desde la API backend y los renderiza en una plantilla HTML.",
            response_description="Página HTML con la lista de libros."
            )
async def list_libros(request: Request):
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        response = await client.get("/libros/")
        if response.status_code != 200:
            error_msg = response.json().get("detail", "Sin detalle en respuesta de API")
            logger.exception("Error al obtener libros: %s", error_msg)
            raise HTTPException(status_code=response.status_code,
                                detail="Error al obtener libros")
        libros = response.json()
    return templates.TemplateResponse("libros/list.html", {
        "request": request,
        "libros": libros,
        "mensaje": None
        })

@router.get("/libros/create",
            response_class=HTMLResponse,
            summary="Formulario HTML para crear un libro",
            response_description="Devuelve un formulario HTML para crear un nuevo libro.")
async def mostrar_formulario_creacion(request: Request):
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        resp_autores = await client.get("/autores/")
        resp_categorias = await client.get("/categorias/")
        resp_editoriales = await client.get("/editoriales/")
        resp_ubicaciones = await client.get("/ubicaciones/")
        
        autores = resp_autores.json() if resp_autores.status_code == 200 else []
        categorias = resp_categorias.json() if resp_categorias.status_code == 200 else []
        editoriales = resp_editoriales.json() if resp_editoriales.status_code == 200 else []
        ubicaciones = resp_ubicaciones.json() if resp_ubicaciones.status_code == 200 else []
        
    return templates.TemplateResponse(
        "libros/create.html",
        {
            "request": request,
            "autores": autores,
            "categorias": categorias,
            "editoriales": editoriales,
            "ubicaciones": ubicaciones
        })

@router.post("/libros/",
            response_class=HTMLResponse,
            summary="Crear un libro",
            description="Obtiene los datos del formulario, crea un libro mediante la API backend y redirige a la lista de libros.",
            response_description="formulario HTML listando libros.")
async def crear_libro_front(
    request: Request,
    titulo: str = Form(...),
    isbn: str = Form(...),
    autor_id: int = Form(...),
    categoria_id: int = Form(...),
    editorial_id: int = Form(...),
    cantidad_ejemplares: int = Form(...),
    ubicacion_id: int = Form(...),
    resumen: str = Form(...)
):
    valores = {
        "titulo": titulo,
        "isbn": isbn,
        "autor_id": autor_id,
        "categoria_id": categoria_id,
        "editorial_id": editorial_id,
        "cantidad_ejemplares": cantidad_ejemplares,
        "ubicacion_id": ubicacion_id,
        "resumen": resumen
    }

    try:
        autor = LibroCreate(**valores)

        async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
            resp = await client.post("/libros/", json=autor.model_dump(mode="json"))

            if resp.status_code not in (200, 303):
                error_msg = resp.json().get("detail", "No se pudo crear el libro")
                logger.exception("Error al crear libro: %s", error_msg)
                resp_autores = await client.get("/autores/")
                resp_categorias = await client.get("/categorias/")
                resp_editoriales = await client.get("/editoriales/")
                resp_ubicaciones = await client.get("/ubicaciones/")

                autores = resp_autores.json() if resp_autores.status_code == 200 else []
                categorias = resp_categorias.json() if resp_categorias.status_code == 200 else []
                editoriales = resp_editoriales.json() if resp_editoriales.status_code == 200 else []
                ubicaciones = resp_ubicaciones.json() if resp_ubicaciones.status_code == 200 else []

                return templates.TemplateResponse(
                    "libros/create.html",
                    {
                        "request": request,
                        "autores": autores,
                        "categorias": categorias,
                        "editoriales": editoriales,
                        "ubicaciones": ubicaciones
                    })
            response = await client.get("/libros/")
            libros = response.json()
        mensaje = "Libro creado correctamente."
        return templates.TemplateResponse("libros/list.html", {
        "request": request,
        "libros": libros,
        "mensaje": {"tipo": "success", "texto": mensaje}
        })

    except Exception as e:
        async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
            logger.exception("Error al crear libro: %s", e)
            resp_autores = await client.get("/autores/")
            resp_categorias = await client.get("/categorias/")
            resp_editoriales = await client.get("/editoriales/")
            resp_ubicaciones = await client.get("/ubicaciones/")

            autores = resp_autores.json() if resp_autores.status_code == 200 else []
            categorias = resp_categorias.json() if resp_categorias.status_code == 200 else []
            editoriales = resp_editoriales.json() if resp_editoriales.status_code == 200 else []
            ubicaciones = resp_ubicaciones.json() if resp_ubicaciones.status_code == 200 else []

            return templates.TemplateResponse(
                "libros/create.html",
                {
                    "request": request,
                    "autores": autores,
                    "categorias": categorias,
                    "editoriales": editoriales,
                    "ubicaciones": ubicaciones
                })

@router.get("/libros/{libro_id}",
            response_class=HTMLResponse,
            summary="Formulario HTML para actualizar un libro.",
            description="Envia un formulario HTML detallando un libro específico obtenido desde la API backend.",
            response_description="formulario HTML para ver el detalle de un libro.")
async def detalle_libro(request: Request, libro_id: str):
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        resp_libro = await client.get(f"/libros/{libro_id}")
        resp_autores = await client.get("/autores/")
        resp_categorias = await client.get("/categorias/")
        resp_editoriales = await client.get("/editoriales/")
        resp_ubicaciones = await client.get("/ubicaciones/")

        libro = resp_libro.json() if resp_libro.status_code == 200 else None
        autores = resp_autores.json() if resp_autores.status_code == 200 else []
        categorias = resp_categorias.json() if resp_categorias.status_code == 200 else []
        editoriales = resp_editoriales.json() if resp_editoriales.status_code == 200 else []
        ubicaciones = resp_ubicaciones.json() if resp_ubicaciones.status_code == 200 else []
    return templates.TemplateResponse("libros/detail.html", {
        "request": request,
        "libro": libro,
        "autores": autores,
        "categorias": categorias,
        "editoriales": editoriales,
        "ubicaciones": ubicaciones
    })

@router.post("/libros/{libro_id}/update",
            response_class=HTMLResponse,
            summary="Actualizar un libro",
            description="Obtiene los datos del formulario, actualiza el libro mediante la API backend y redirige a la lista de libros.",
            response_description="formulario HTML listando libros")
async def actualizar_libro_front(
    request: Request,
    libro_id: int,
    titulo: str = Form(...),
    isbn: str = Form(...),
    autor_id: int = Form(...),
    categoria_id: int = Form(...),
    editorial_id: int = Form(...),
    cantidad_ejemplares: int = Form(...),
    ubicacion_id: int = Form(...),
    resumen: str = Form(...)
):
    valores = {
        "libro_id": libro_id,
        "titulo": titulo,
        "isbn": isbn,
        "autor_id": autor_id,
        "categoria_id": categoria_id,
        "editorial_id": editorial_id,
        "cantidad_ejemplares": cantidad_ejemplares,
        "ubicacion_id": ubicacion_id,
        "resumen": resumen
    }

    try:
        libro_update = LibroUpdate(**valores)

        async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
            resp = await client.post(
                f"/libros/{libro_id}/update",
                json=libro_update.model_dump())

        if resp.status_code not in (200, 303):
            async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
                resp_libro = await client.get(f"/libros/{libro_id}")
                resp_autores = await client.get("/autores/")
                resp_categorias = await client.get("/categorias/")
                resp_editoriales = await client.get("/editoriales/")
                resp_ubicaciones = await client.get("/ubicaciones/")

                libro = resp_libro.json() if resp_libro.status_code == 200 else None
                autores = resp_autores.json() if resp_autores.status_code == 200 else []
                categorias = resp_categorias.json() if resp_categorias.status_code == 200 else []
                editoriales = resp_editoriales.json() if resp_editoriales.status_code == 200 else []
                ubicaciones = resp_ubicaciones.json() if resp_ubicaciones.status_code == 200 else []
            return templates.TemplateResponse("libros/detail.html", {
                "request": request,
                "libro": libro,
                "autores": autores,
                "categorias": categorias,
                "editoriales": editoriales,
                "ubicaciones": ubicaciones
            })

        async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
            response = await client.get("/libros/")
            libros = response.json()

        mensaje = "Libro actualizado correctamente."
        return templates.TemplateResponse("libros/list.html", {
        "request": request,
        "libros": libros,
        "mensaje": {"tipo": "success", "texto": mensaje}
        })

    except Exception as e:
        logger.exception("Error al actualizar libro %s: %s", libro_id, e)
        return templates.TemplateResponse("libros/detail.html", {
                "request": request,
                "libro": [],
                "autores": [],
                "categorias": [],
                "editoriales": [],
                "ubicaciones": []
            })

@router.post("/libros/{libro_id}/eliminar",
            response_class=HTMLResponse,
            summary="Eliminar un libro",
            description="Obtiene el ID del libro, lo elimina mediante la API backend y redirige a la lista de libros.",
            response_description="formulario HTML listando libros.")
async def eliminar_libro(request: Request, libro_id: int):
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        response = await client.delete(f"/libros/{libro_id}/eliminar")
        tipo = "success"
        if response.status_code != 303:
            mensaje = f"No se pudo eliminar el libro: {response.text}"
            tipo = "danger"
        else:
            mensaje = "Libro eliminado correctamente."
            tipo = "success"
        response_libros = await client.get("/libros/")
        if response_libros.status_code != 200:
            error_msg = response_libros.json().get("detail", "Sin detalle en respuesta de API")
            logger.exception("Error al obtener libros: %s", error_msg)
            raise HTTPException(status_code=response_libros.status_code,
                                detail="Error al obtener libros")
        libros = response_libros.json()
        return templates.TemplateResponse("libros/list.html", {
        "request": request,
        "libros": libros,
        "mensaje": {"tipo": tipo, "texto": mensaje}
        })
