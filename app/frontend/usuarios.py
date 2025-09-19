import httpx
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.schemas.usuarios import UsuarioCreate,UsuarioUpdate
from app.core.logging_config import logger

router = APIRouter(tags=["Frontend Usuarios"])
templates = Jinja2Templates(directory="templates")

def render_create_form(
    request: Request,
    roles: list,
    valores: dict,
    error: str | None = None,
    status_code: int = 200,
):
    """Renderiza el formulario de creación de usuarios con datos y error opcional."""
    return templates.TemplateResponse(
        "usuarios/create.html",
        {
            "request": request,
            "roles": roles,
            "valores": valores,
            "error": error,
        },
        status_code=status_code,
    )


async def get_roles(client: httpx.AsyncClient):
    """Obtiene roles desde la API backend."""
    response_roles = await client.get("/roles/")
    return response_roles.json() if response_roles.status_code == 200 else []


@router.get("/usuarios",
            response_class=HTMLResponse,
            summary="Listar usuarios",
            description="Obtiene todos los usuarios desde la API backend y los renderiza en una plantilla HTML.",
            response_description="Página HTML con la lista de usuarios."
            )
async def list_usuarios(request: Request):
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        response = await client.get("/usuarios/")
        if response.status_code != 200:
            error_msg = response.json().get("detail", "Sin detalle en respuesta de API")
            logger.exception("Error al obtener usuarios: %s", error_msg)
            raise HTTPException(status_code=response.status_code,
                                detail="Error al obtener usuarios")
        usuarios = response.json()
        return templates.TemplateResponse("usuarios/list.html", {
        "request": request,
        "usuarios": usuarios,
        "mensaje": None
    })


@router.get("/usuarios/create",
            response_class=HTMLResponse,
            summary="Formulario HTML para crear un usuario",
            response_description="Devuelve un formulario HTML para crear un nuevo usuario.")
async def mostrar_formulario_creacion(request: Request):
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        roles = await get_roles(client)

    return templates.TemplateResponse("usuarios/create.html", {
        "request": request,
        "roles": roles,
        "valores": {} 
    })

@router.post("/usuarios/",
            response_class=HTMLResponse,
            summary="Crear un usuario",
            description="Obtiene los datos del formulario, crea un usuario mediante la API backend y redirige a la lista de usuarios.",
            response_description="formulario HTML listando usuarios.")
async def crear_usuario_front(
    request: Request,
    dni: str = Form(...),
    nombre: str = Form(...),
    apellido: str = Form(...),
    email: str = Form(...),
    rol_id: int = Form(...),
):
    valores = {
        "dni": dni,
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "rol_id": rol_id,
    }

    try:
        usuario = UsuarioCreate(**valores)

        async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
            resp = await client.post("/usuarios/", json=usuario.model_dump())

            if resp.status_code not in (200, 303):
                error_msg = resp.json().get("detail", "No se pudo crear el usuario")
                logger.exception("Error al crear usuario: %s", error_msg)
                roles = await get_roles(client)
                return render_create_form(request, roles, valores, error_msg)

            response = await client.get("/usuarios/")
            usuarios = response.json()
        mensaje = "Usuario creado correctamente."
        return templates.TemplateResponse("usuarios/list.html", {
            "request": request, 
            "usuarios": usuarios,
            "mensaje": {"tipo": "success", "texto": mensaje}
        })

    except Exception as e:
        async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
            roles = await get_roles(client)

        logger.exception("Excepción al crear usuario: %s", e)
        return render_create_form(
            request,
            roles,
            valores,
            "No se pudo crear el usuario",
            status_code=500)

@router.get("/usuarios/{usuario_id}",
            response_class=HTMLResponse,
            summary="Formulario HTML para actualizar un usuario.",
            description="Envia un formulario HTML detallando un usuario específico obtenido desde la API backend.",
            response_description="formulario HTML para ver el detalle de un usuario.")
async def detalle_usuario(request: Request, usuario_id: int):
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        response_usuario = await client.get(f"/usuarios/{usuario_id}")
        response_roles = await client.get("/roles/")
        response_estados = await client.get("/estados/")
        if (response_usuario.status_code != 200 or
            response_roles.status_code != 200 or
            response_estados.status_code != 200):
            raise HTTPException(status_code=500,
                                detail="Error al obtener datos del usuario, roles o estados")
        usuario = response_usuario.json()
        roles = response_roles.json()
        estados = response_estados.json()

    return templates.TemplateResponse("usuarios/detail.html", {
        "request": request,
        "usuario": usuario,
        "roles": roles,
        "estados": estados
    })

@router.post("/usuarios/{usuario_id}/update",
            response_class=HTMLResponse,
            summary="Actualizar un usuario",
            description="Obtiene los datos del formulario, actualiza el usuario mediante la API backend y redirige a la lista de usuarios.",
            response_description="formulario HTML listando usuarios")
async def actualizar_usuario_front(
    request: Request,
    usuario_id: int,
    dni: str = Form(...),
    nombre: str = Form(...),
    apellido: str = Form(...),
    email: str = Form(...),
    rol_id: int = Form(...),
    estado_id: int = Form(...),
):
    valores = {
        "dni": dni,
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "rol_id": rol_id,
        "estado_id": estado_id,
    }

    try:
        usuario_update = UsuarioUpdate(**valores)

        async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
            resp = await client.post(
                f"/usuarios/{usuario_id}/update",
                json=usuario_update.model_dump())

        if resp.status_code not in (200, 303):
            async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
                roles = (await client.get("/roles/")).json()
                estados = (await client.get("/estados/")).json()

            return templates.TemplateResponse(
                "usuarios/detail.html",
                {
                    "request": request,
                    "usuario": valores,
                    "roles": roles,
                    "estados": estados,
                    "error": "No se pudo actualizar el usuario",
                },
                status_code=resp.status_code,
            )

        async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
            response = await client.get("/usuarios/")
            usuarios = response.json()

        mensaje = "Usuario actualizado correctamente."
        return templates.TemplateResponse("usuarios/list.html", {
            "request": request,
            "usuarios": usuarios,
            "mensaje": {"tipo": "success", "texto": mensaje}
        })

    except Exception as e:
        logger.exception("Error al actualizar usuario %s: %s", usuario_id, e)
        return templates.TemplateResponse(
            "usuarios/detail.html",
            {
                "request": request,
                "usuario": valores,
                "error": f"No se pudo actualizar el usuario: {e}",
            },
            status_code=500,
        )

@router.post("/usuarios/{usuario_id}/eliminar",
            response_class=HTMLResponse,
            summary="Eliminar un usuario",
            description="Obtiene el ID del usuario, lo elimina mediante la API backend y redirige a la lista de usuarios.",
            response_description="formulario HTML listando usuarios.")
async def eliminar_usuario(request: Request, usuario_id: int):
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        response = await client.delete(f"/usuarios/{usuario_id}/eliminar")
        tipo = "success"
        if response.status_code != 303:
            mensaje = f"No se pudo eliminar el usuario: {response.text}"
            tipo = "danger"
        else:
            mensaje = "Usuario eliminado correctamente."
            tipo = "success"
        usuarios_response = await client.get("/usuarios/")
        if usuarios_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error al obtener la lista de usuarios")
        usuarios = usuarios_response.json()
    return templates.TemplateResponse(
        "usuarios/list.html",
        {"request": request,
        "usuarios": usuarios,
        "mensaje": {"tipo": tipo, "texto": mensaje}}
    )
