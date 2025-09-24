from fastapi.templating import Jinja2Templates
from app.frontend.http.nacionalidades import get as get_nacionalidades
from app.core.flash import get_flash
templates = Jinja2Templates(directory="templates")

def render_list(request,autores):
    return templates.TemplateResponse("autores/list.html", {
        "request": request,
        "autores": autores,
        "mensaje": get_flash(request)
    })

def render_create(request,nacionalidades):
    return templates.TemplateResponse("autores/create.html", {
        "request": request,
        "nacionalidades": nacionalidades,
        "mensaje": get_flash(request)
    })

def render_detail(request,autor,nacionalidades,error=None):
    return templates.TemplateResponse("autores/detail.html", {
        "request": request,
        "autor": autor,
        "nacionalidades": nacionalidades,
        "error": error
    })

async def render_error_detail(request, autor):
    result = await get_nacionalidades()
    if result.success:
        nacionalidades = result.data
    else:
        print("Hubo un error:", result.error)
        nacionalidades = []
    return render_detail(request,
                        autor,
                        nacionalidades,
                        error="No se pudo actualizar el autor")
